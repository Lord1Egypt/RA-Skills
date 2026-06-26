import jkrc
import time
import math

print('=== X+20mm 最佳测试 ===')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()

# 回零（阻塞确保到位）
r.joint_move((0,0,0,0,0,0), 0, 1, 0.5)
time.sleep(2)

# J3=90, J5=90（阻塞确保到位）
r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 1, 0.5)
time.sleep(2)

joint = r.get_actual_joint_position()[1]
print('关节:', [round(j*180/math.pi,1) for j in joint])

tcp = r.get_actual_tcp_position()[1]
print('TCP:', [round(x,1) for x in tcp])

# X+20 非阻塞
target = (tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('目标 X:', round(target[0],1))

r.set_rapidrate(0.8)
result = r.linear_move(target, 0, 0, 0.8)

start = time.time()
for i in range(25):
    time.sleep(0.2)
    if r.is_in_pos()[1]:
        print('完成:', round(time.time()-start,2), 's')
        break

new = r.get_actual_tcp_position()[1]
moved = new[0] - tcp[0]
print('移动:', round(moved,1), 'mm')
print('耗时:', round(time.time()-start,2), 's')

r.logout()
