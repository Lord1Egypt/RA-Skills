import jkrc
import time
import math

print('=== JAKA SDK 直线运动 X+20mm (高速) ===')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()

# 回零 + J3=90, J5=90
r.joint_move((0,0,0,0,0,0), 0, 0, 0.8)
for i in range(20):
    time.sleep(0.2)
    if r.is_in_pos()[1]: break

r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 0, 0.8)
for i in range(20):
    time.sleep(0.2)
    if r.is_in_pos()[1]: break

tcp = r.get_actual_tcp_position()[1]
print('TCP:', round(tcp[0],1), 'mm')

# X+20mm 高速
target = (tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('目标 X:', round(target[0],1), 'mm')

# 最高速度 1.0
r.set_rapidrate(1.0)
result = r.linear_move(target, 0, 0, 1.0)
print('发送:', result)

# 轮询等待
start = time.time()
for i in range(40):
    time.sleep(0.3)
    if r.is_in_pos()[1]:
        print('完成 after', round(time.time()-start,1), 's')
        break

new_tcp = r.get_actual_tcp_position()[1]
moved = new_tcp[0] - tcp[0]
print('X 移动:', round(moved,1), 'mm')
print('耗时:', round(time.time()-start,1), 's')

if abs(moved - 20) < 1:
    print('OK: 20mm')
else:
    print('误差:', round(abs(moved-20),1), 'mm')

r.logout()
