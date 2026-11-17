import jkrc
import time

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(0.5)

joint = r.get_actual_joint_position()[1]
print('当前:', [round(j*180/3.14159,1) for j in joint])

# 非阻塞模式回零
r.set_rapidrate(0.3)
result = r.joint_move((0,0,0,0,0,0), 0, 0, 0.3)
print('发送:', result)

# 轮询等待
for i in range(30):
    time.sleep(0.5)
    in_pos = r.is_in_pos()
    if in_pos[1] == True:
        print('到位 after', i*0.5, 's')
        break
    if i % 10 == 0:
        print('等待...', i)

new = r.get_actual_joint_position()[1]
print('新:', [round(j*180/3.14159,1) for j in new])

r.logout()
