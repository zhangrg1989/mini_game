import math
import numpy as np
import pygame
from pygame.locals import MOUSEBUTTONUP

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

space = 60  # 四周留下的边距
cell_size = 30  # 每个格子大小
cell_num = 19

grid_size = cell_size * cell_num  + space * 2  # 棋盘的大小
screen = pygame.display.set_mode((grid_size, grid_size))  # 设置窗口长宽

chess_arr = []
chess_his = []
flag = 1  # 1绿 2红
step=60 #定义双方步数
game_state = 0  # 游戏状态 0.布局状态 1.演化状态 2.表示绿胜 3.表示红胜
cells = np.zeros((cell_num,cell_num))

fclock = pygame.time.Clock()
fps = 1

def gen_next(s):
    print(s)
    s2 = np.zeros((cell_num,cell_num))
    for i in range(len(s)):
        for j in range(len(s[i])):
            x=(i-1+cell_num)%cell_num
            y=(j-1+cell_num)%cell_num
            m=(i+1)%cell_num
            n=(j+1)%cell_num
            arround = np.array([[s[x,y],s[x,j],s[x,n]],
                            [s[i,y],0,s[i,n]],
                            [s[m,y],s[m,j],s[m,n]]])
            if np.count_nonzero(arround) == 3 and  np.sum(arround==1) > 1 : s2[i,j] = 1
            elif np.count_nonzero(arround) == 3  and np.sum(arround==2) > 1 : s2[i,j] = 2
            elif np.count_nonzero(arround) == 2: s2[i,j] = s[i,j]
            else :s2[i,j] = 0
    return s2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((WHITE))  # 将界面设置为白色


    myfont = pygame.font.Font(None, 40)
    white = 210, 210, 0
    text = "remain steps : " + str(step)
    # text = "%s win" % ('green' if game_state == 2 else 'red')
    textImage = myfont.render(text, True, white)
    screen.blit(textImage, (5, 5))

    # 画网格线
    for x in range(0, cell_size * (cell_num + 1), cell_size):
        pygame.draw.line(screen, (200, 200, 200), (x + space, 0 + space),
                         (x + space, cell_size * (cell_num) + space), 1)
    for y in range(0, cell_size * (cell_num + 1), cell_size):
        pygame.draw.line(screen, (200, 200, 200), (0 + space, y + space),
                         (cell_size * (cell_num) + space, y + space), 1)

    if game_state == 0:
        if event.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()  # 获取鼠标位置
            xi = int(math.floor((x - space) * 1.0 / cell_size))  # 获取到x方向下取整的序号
            yi = int(math.floor((y - space) * 1.0 / cell_size))  # 获取到y方向下取整的序号
            if xi >= 0 and xi < cell_num and yi >= 0 and yi < cell_num and (xi, yi, 1) not in chess_arr \
                    and (xi, yi, 2) not in chess_arr:
                if step>0 :
                    step -= 1
                    chess_arr.append((xi, yi, flag))
                    flag =2 if flag == 1 else 1
                else:
                    game_state=1
                    for x, y, c in chess_arr:
                        cells[y, x] = c

        for x, y, c in chess_arr:
            chess_color = (GREEN) if c == 1 else (RED)
            pygame.draw.rect(screen, chess_color, ((x * cell_size + 1 + space, y * cell_size + 1 + space), (29, 29)))
    elif game_state == 1:
        fclock.tick(fps)
        if cells.tolist() in chess_his :
            green_cnt= np.sum(cells == 1)
            red_cnt  = np.sum(cells == 2)
            if green_cnt > red_cnt :
                game_state = 2
            elif red_cnt > green_cnt :
                game_state = 3
            else:
                game_state = 4
        else:
            chess_his.append(cells.tolist())
            cells_next= gen_next(cells)
            cells=cells_next
            print(cells)

            for i in range(len(cells)):
                for j in range(len(cells[i])):
                    if cells[i,j] == 1:
                        chess_color = GREEN
                    elif cells[i,j] == 2:
                        chess_color = RED
                    else:
                        chess_color = WHITE
                    pygame.draw.rect(screen, chess_color,
                                     ((j * cell_size + 1 + space, i * cell_size + 1 + space), (29, 29)))

            if cells.sum() >0 :
                if np.sum(cells==1) == 0 :
                    game_state = 3
                elif np.sum(cells==2) == 0 :
                    game_state = 2
    else:
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                if cells[i, j] == 1:
                    chess_color = GREEN
                elif cells[i, j] == 2:
                    chess_color = RED
                else:
                    chess_color = WHITE
                pygame.draw.rect(screen, chess_color,
                                 ((j * cell_size + 1 + space, i * cell_size + 1 + space), (29, 29)))
        myfont = pygame.font.Font(None, 60)
        white = 210, 210, 0
        win_text = "%s win" % ('green' if game_state == 2 else ( 'red' if game_state ==3 else 'none'))
        textImage = myfont.render(win_text, True, white)
        screen.blit(textImage, (260, 320))

    pygame.display.update()