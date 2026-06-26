import jkrc
import time
import math

print('=== JAKA 直线运动 X+20mm 最终测试 ===')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(0.5)

# 回零
print('1. 回零...')
r.joint_move((0,0,0,0,0,0), 0, 0, 0.5)
for i in range(30):
    time.sleep(0.3)
    if r.is_in_pos()[1]: break

# J1=90, J3=90, J5=90
print('2. J1,J3,J5 到 90 度...')
r.joint_move((math.pi/2, 0, math.pi/2, 0, math.pi/2, 0), 0, 0, 0.5)
for i in range(30):
    time.sleep(0.3)
    if r.is_in_pos()[1]: break

joint = r.get_actual_joint_position()[1]
print('   关节:', [round(j*180/math.pi,1) for j in joint])

tcp = r.get_actual_tcp_position()[1]
print('   TCP:', [round(x,1) for x in tcp])

# X+20 非阻塞
print('3. 直线运动 X+20mm...')
target = (tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
r.set_rapidrate(0.8)
result = r.linear_move(target, 0, 0, 0.8)
print('   发送:', result)

# 轮询等待
for i in range(50):
    time.sleep(0.5)
    if r.is_in_pos()[1]:
        print('   完成 after', i*0.5, 's')
        break

new = r.get_actual_tcp_position()[1]
print('   新 TCP:', [round(x,1) for x in new])
print('   X 移动:', round(new[0]-tcp[0],1), 'mm')

# 验证
moved = new[0] - tcp[0]
if abs(moved - 20) < 1:
    print('✅ OK: 移动 20mm 成功')
elif abs(moved - 20) < 3:
    print('⚠️ OK: 接近 20mm (误差:', round(abs(moved-20),1), 'mm)')
else:
    print('❌ FAIL: 偏差大 (', round(moved,1), 'mm)')

r.logout()
print('完成!')
