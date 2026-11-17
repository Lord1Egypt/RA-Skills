from jaka_skill import JAKARobot
import time

r = JAKARobot('192.168.28.18')
r.connect()
r.enable_robot()
time.sleep(0.5)

s = r.get_state()
tcp = s['tcp_position']
print('当前X:', tcp[0], 'mm')

target = [tcp[0]+30, tcp[1], tcp[2], 0, 0, 0]
print('目标X:', target[0], 'mm')

result = r.move_linear(target, speed=100)
print('结果:', result)

time.sleep(2)
s2 = r.get_state()
print('新X:', s2['tcp_position'][0], 'mm')
print('移动:', s2['tcp_position'][0]-tcp[0], 'mm')

r.disconnect()
