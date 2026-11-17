from jaka_skill import JAKARobot
import time

print('=== JAKA Skills 直线运动测试 X+20mm ===')
r = JAKARobot('192.168.28.18')
r.connect()
r.enable_robot()
time.sleep(0.5)

# 确认当前姿态
s = r.get_state()
print('当前关节:', [round(j,1) for j in s['joints_deg']])
print('当前 TCP:', [round(x,1) for x in s['tcp_position']])

# 沿 X 轴 +20mm
tcp = s['tcp_position']
target = [tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5]]
print('目标 X:', round(target[0],1), 'mm (原:', round(tcp[0],1), '+20)')

# 直线运动 - 速度快 (500mm/s)
print('开始移动...')
result = r.move_linear(target, speed=500)
print('结果:', result)

# 等待完成
time.sleep(3)
s2 = r.get_state()
print('新 TCP:', [round(x,1) for x in s2['tcp_position']])
print('X 移动:', round(s2['tcp_position'][0]-tcp[0],1), 'mm')

# 验证
moved = s2['tcp_position'][0] - tcp[0]
if abs(moved - 20) < 1:
    print('OK: 移动 20mm 成功')
elif abs(moved - 20) < 3:
    print('OK: 移动接近 20mm (误差:', round(abs(moved-20),1), 'mm)')
else:
    print('WARN: 移动距离偏差较大')

r.disconnect()
print('完成!')
