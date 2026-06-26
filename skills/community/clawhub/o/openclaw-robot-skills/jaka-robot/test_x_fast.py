from jaka_skill import JAKARobot
import time

r = JAKARobot('192.168.28.18')
r.connect()
r.enable_robot()
time.sleep(0.5)

s = r.get_state()
tcp = s['tcp_position']
print('当前 X:', round(tcp[0],1), 'mm')

target = [tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5]]
print('目标 X:', round(target[0],1), 'mm')

# 用更快的速度 (之前成功的参数)
result = r.move_linear(target, speed=200)
print('结果:', result)

time.sleep(3)
s2 = r.get_state()
print('新 X:', round(s2['tcp_position'][0],1), 'mm')
print('移动:', round(s2['tcp_position'][0]-tcp[0],1), 'mm')

r.disconnect()
