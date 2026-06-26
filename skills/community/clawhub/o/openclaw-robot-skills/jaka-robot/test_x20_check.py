import jkrc
import time
import math

print('=== X+20mm 姿态检查 ===')

r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()

# 阻塞模式确保到位
print('回零...')
r.joint_move((0,0,0,0,0,0), 0, 1, 0.5)
time.sleep(2)

print('J3=90, J5=90...')
r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 1, 0.5)
time.sleep(2)

# 验证姿态
joint = r.get_actual_joint_position()[1]
j3 = joint[2]*180/math.pi
j5 = joint[4]*180/math.pi
print('关节:', [round(j,1) for j in [j3, j5]])

if abs(j3-90)<1 and abs(j5-90)<1:
    tcp = r.get_actual_tcp_position()[1]
    print('TCP:', round(tcp[0],1), 'mm')
    
    target = (tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5])
    r.set_rapidrate(0.8)
    
    start = time.time()
    result = r.linear_move(target, 0, 0, 0.8)
    print('发送:', result)
    
    for i in range(30):
        time.sleep(0.3)
        if r.is_in_pos()[1]:
            print('完成:', round(time.time()-start,1), 's')
            break
    
    new = r.get_actual_tcp_position()[1]
    moved = new[0] - tcp[0]
    print('移动:', round(moved,1), 'mm')
    
    if abs(moved-20) < 2:
        print('OK')
    else:
        print('误差:', round(abs(moved-20),1), 'mm')
else:
    print('姿态不对!')

r.logout()
