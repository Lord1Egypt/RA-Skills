from jaka_skill import JAKARobot
import time

print('=== JAKA Skills 直线运动测试 ===')
r = JAKARobot('192.168.28.18')
r.connect()
r.enable_robot()
time.sleep(0.5)

# 获取当前状态
s = r.get_state()
tcp = s['tcp_position']
print('当前 TCP:', [round(x,1) for x in tcp])
print('当前关节:', [round(j,1) for j in s['joints_deg']])

# 沿 X 轴 +30mm
target = [tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5]]
print('目标 X:', round(target[0],1), 'mm (原:', round(tcp[0],1), '+30)')

# 直线运动 - 速度 500mm/s
print('开始移动...')
result = r.move_linear(target, speed=500)
print('结果:', result)

time.sleep(3)
s2 = r.get_state()
print('新 TCP:', [round(x,1) for x in s2['tcp_position']])
print('X 移动:', round(s2['tcp_position'][0]-tcp[0],1), 'mm')

r.disconnect()
print('完成!')
