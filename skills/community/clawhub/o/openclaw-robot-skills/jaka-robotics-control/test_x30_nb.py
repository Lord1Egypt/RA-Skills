import jkrc
import time
import math

print('=== JAKA 直线运动 X+30mm (非阻塞) ===')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(0.5)

# 回零
print('回零...')
r.joint_move((0,0,0,0,0,0), 0, 0, 0.3)
for i in range(20):
    time.sleep(0.5)
    if r.is_in_pos()[1]: break

# J3=90, J5=90
print('J3,J5 到 90 度...')
r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 0, 0.5)
for i in range(20):
    time.sleep(0.5)
    if r.is_in_pos()[1]: break

joint = r.get_actual_joint_position()[1]
print('关节:', [round(j*180/math.pi,1) for j in joint])

# 直线运动 X+30
tcp = r.get_actual_tcp_position()[1]
print('TCP:', round(tcp[0],1), 'mm')

target = (tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
r.set_rapidrate(0.8)
result = r.linear_move(target, 0, 0, 0.8)
print('发送:', result)

# 轮询等待
for i in range(40):
    time.sleep(0.5)
    if r.is_in_pos()[1]:
        print('完成 after', i*0.5, 's')
        break

new = r.get_actual_tcp_position()[1]
print('新 X:', round(new[0],1), 'mm')
print('移动:', round(new[0]-tcp[0],1), 'mm')

r.logout()
