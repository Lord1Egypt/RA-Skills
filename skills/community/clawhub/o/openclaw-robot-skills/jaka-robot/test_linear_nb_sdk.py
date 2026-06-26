import jkrc
import time
import math

print('=== JAKA SDK 直线运动 X+20mm (非阻塞) ===')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()

# 回零 + J3=90, J5=90
r.joint_move((0,0,0,0,0,0), 0, 0, 0.5)
for i in range(30):
    time.sleep(0.3)
    if r.is_in_pos()[1]: break

r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 0, 0.5)
for i in range(30):
    time.sleep(0.3)
    if r.is_in_pos()[1]: break

joint = r.get_actual_joint_position()[1]
print('关节:', [round(j*180/math.pi,1) for j in joint])

tcp = r.get_actual_tcp_position()[1]
print('TCP:', [round(x,1) for x in tcp])

# X+20mm 非阻塞
target = (tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('目标 X:', round(target[0],1))

r.set_rapidrate(0.8)
result = r.linear_move(target, 0, 0, 0.8)  # 非阻塞
print('发送:', result)

# 轮询等待完成
for i in range(60):
    time.sleep(0.5)
    if r.is_in_pos()[1]:
        print('完成 after', i*0.5, 's')
        break

new_tcp = r.get_actual_tcp_position()[1]
moved = new_tcp[0] - tcp[0]
print('X 移动:', round(moved,1), 'mm')

if abs(moved - 20) < 1:
    print('OK: 20mm')
elif abs(moved - 20) < 3:
    print('OK: 误差', round(abs(moved-20),1), 'mm')
else:
    print('FAIL:', moved, 'mm')

r.logout()
