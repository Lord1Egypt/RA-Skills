from jaka_skill import JAKARobot
import time, math

r = JAKARobot('192.168.28.18')
r.connect()
r.enable_robot()
time.sleep(0.5)

s = r.get_state()
tcp = s['tcp_position']
print('当前 TCP:', [round(x,1) for x in tcp])

# 保持当前姿态，只移动 X
target = [tcp[0]+30, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5]]
print('目标 X:', round(target[0],1), 'mm')

# 用关节运动测试
print('尝试关节运动...')
joint = s['joints_rad']
result = r.move_joint(joint, 0.3)
print('关节运动:', result)

r.disconnect()
