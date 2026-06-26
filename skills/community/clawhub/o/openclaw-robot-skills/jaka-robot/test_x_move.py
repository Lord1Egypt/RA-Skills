from jaka_skill import JAKARobot
import time

robot = JAKARobot('192.168.28.18')
robot.connect()
robot.enable_robot()
time.sleep(0.5)

state = robot.get_state()
tcp = state['tcp_position']
print(f'当前TCP: X={tcp[0]:.1f}, Y={tcp[1]:.1f}, Z={tcp[2]:.1f} mm')

# 沿X轴+30mm
target = [tcp[0]+30, tcp[1], tcp[2], 0, 0, 0]
print(f'目标X: {target[0]:.1f}mm')

result = robot.move_linear(target, speed=100)
print(f'结果: {result}')

time.sleep(2)

new_state = robot.get_state()
new_tcp = new_state['tcp_position']
print(f'新TCP: X={new_tcp[0]:.1f}mm')
print(f'移动距离: {new_tcp[0]-tcp[0]:.1f}mm')

robot.disconnect()
