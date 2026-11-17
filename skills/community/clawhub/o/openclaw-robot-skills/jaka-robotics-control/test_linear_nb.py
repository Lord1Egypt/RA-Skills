import jkrc
import time

robot = jkrc.RC('192.168.28.18')
robot.login()
robot.enable_robot()
time.sleep(0.5)

tcp = robot.get_actual_tcp_position()[1]
print('当前 X:', round(tcp[0],1), 'mm')

target = (tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('目标 X:', round(target[0],1), 'mm')

robot.set_rapidrate(0.5)

# 非阻塞模式
result = robot.linear_move(target, 0, 0, 0.5)
print('发送:', result)

# 轮询等待
for i in range(20):
    time.sleep(0.5)
    in_motion = robot.is_in_servomove()
    if in_motion[1] == False:
        print('完成 after', i*0.5, 's')
        break

new_tcp = robot.get_actual_tcp_position()[1]
print('新 X:', round(new_tcp[0],1), 'mm')
print('移动:', round(new_tcp[0]-tcp[0],1), 'mm')

robot.logout()
