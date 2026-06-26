import jkrc
import time
import math

print('=== JAKA 直线运动 X+30mm 测试 ===')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(0.5)

# 1. 回零
print('1. 回零...')
r.joint_move((0,0,0,0,0,0), 0, 1, 0.3)
time.sleep(3)

# 2. J3=90, J5=90
print('2. 移动 J3,J5 到 90 度...')
target_j = (0, 0, math.pi/2, 0, math.pi/2, 0)
r.set_rapidrate(0.5)
r.joint_move(target_j, 0, 1, 0.5)
time.sleep(3)

joint = r.get_actual_joint_position()[1]
print('   关节:', [round(j*180/math.pi,1) for j in joint])

# 3. 直线运动 X+30
tcp = r.get_actual_tcp_position()[1]
print('3. 当前 TCP:', [round(x,1) for x in tcp])

target = (tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('   目标 X:', round(target[0],1), 'mm')

r.set_rapidrate(0.8)
result = r.linear_move(target, 0, 1, 0.8)
print('   结果:', result)

time.sleep(3)
new = r.get_actual_tcp_position()[1]
print('   新 TCP:', [round(x,1) for x in new])
print('   X 移动:', round(new[0]-tcp[0],1), 'mm')

r.logout()
print('完成!')
