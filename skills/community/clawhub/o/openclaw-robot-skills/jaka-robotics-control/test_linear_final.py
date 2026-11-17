import jkrc
import time

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(0.5)

tcp = r.get_actual_tcp_position()[1]
print('当前 TCP:', [round(x,1) for x in tcp])

target = (tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('目标 X:', round(target[0],1), 'mm')

# 设置速度倍率
r.set_rapidrate(0.5)

# 非阻塞模式
result = r.linear_move(target, 0, 0, 0.5)
print('发送:', result)

# 轮询等待完成
for i in range(40):
    time.sleep(0.5)
    in_pos = r.is_in_pos()
    if in_pos[1] == True:
        print('完成 after', i*0.5, 's')
        break

new_tcp = r.get_actual_tcp_position()[1]
print('新 TCP:', [round(x,1) for x in new_tcp])
print('X 移动:', round(new_tcp[0]-tcp[0],1), 'mm')

r.logout()
