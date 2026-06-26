import jkrc
import time
import math

print('=== JAKA SDK 直线运动测试 X+20mm ===')
print('姿态要求：J3=90°, J5=90°')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(0.5)

# 1. 回零
print('1. 回零...')
r.joint_move((0,0,0,0,0,0), 0, 1, 0.5)
time.sleep(3)

# 2. J3=90, J5=90
print('2. J3=90°, J5=90°...')
r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 1, 0.5)
time.sleep(3)

joint = r.get_actual_joint_position()[1]
print('   关节:', [round(j*180/math.pi,1) for j in joint])

# 3. 获取当前 TCP
tcp = r.get_actual_tcp_position()[1]
print('   TCP:', [round(x,1) for x in tcp])

# 4. 直线运动 X+20mm
# 参数：end_pos(mm,弧度), move_mode(0=绝对), is_block(1=阻塞), speed(0-1)
target = (tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
print('   目标 X:', round(target[0],1), 'mm')

# 设置速度倍率
r.set_rapidrate(0.8)

# 直线运动 - 阻塞模式
print('   开始移动...')
result = r.linear_move(target, 0, 1, 0.8)
print('   结果:', result)

# 等待
time.sleep(3)

# 5. 验证
new_tcp = r.get_actual_tcp_position()[1]
print('   新 TCP:', [round(x,1) for x in new_tcp])
moved = new_tcp[0] - tcp[0]
print('   X 移动:', round(moved,1), 'mm')

if abs(moved - 20) < 1:
    print('✅ 成功：移动 20mm')
elif abs(moved - 20) < 3:
    print('⚠️ 接近：误差', round(abs(moved-20),1), 'mm')
else:
    print('❌ 偏差大')

r.logout()
print('完成!')
