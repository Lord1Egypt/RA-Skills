import jkrc
import time

robot = jkrc.RC('192.168.28.18')
robot.login()
robot.enable_robot()
time.sleep(0.5)

tcp = robot.get_actual_tcp_position()[1]
print('当前 TCP:', [round(x,1) for x in tcp])

# 目标 X+30mm，保持其他不变
target = (tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('目标 X:', round(target[0],1), 'mm')

# 设置速度
robot.set_rapidrate(0.5)

# 直线运动 - 绝对模式，阻塞
print('开始直线运动...')
result = robot.linear_move(target, 0, 1, 0.5)
print('结果:', result)

time.sleep(2)
new_tcp = robot.get_actual_tcp_position()[1]
print('新 TCP:', [round(x,1) for x in new_tcp])
print('X 移动:', round(new_tcp[0]-tcp[0],1), 'mm')

robot.logout()
