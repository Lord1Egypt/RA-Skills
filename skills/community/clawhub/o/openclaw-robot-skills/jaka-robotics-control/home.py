from jaka_skill import JAKARobot
import time

print('=== 回零操作 ===')
r = JAKARobot('192.168.28.18')
r.connect()
r.enable_robot()
time.sleep(0.5)

s = r.get_state()
print('当前关节:', [round(j,1) for j in s['joints_deg']])

print('执行回零...')
result = r.move_joint([0, 0, 0, 0, 0, 0], speed=0.3)
print('结果:', result)

time.sleep(3)
s2 = r.get_state()
print('新关节:', [round(j,1) for j in s2['joints_deg']])

r.disconnect()
print('完成!')
