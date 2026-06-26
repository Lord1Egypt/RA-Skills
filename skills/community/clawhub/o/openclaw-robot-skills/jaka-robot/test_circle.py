import jkrc
import time
import math

print('=== 水平圆测试 - 直径 20mm ===')
r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(1)

# J3=90, J5=90
r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 1, 1.0)
time.sleep(2)

tcp = r.get_actual_tcp_position()[1]
print(f'起点 TCP: X={tcp[0]:.1f}, Y={tcp[1]:.1f}, Z={tcp[2]:.1f} mm')

# 画圆参数
R = 10  # 半径 10mm
cx, cy, cz = tcp[0], tcp[1], tcp[2]  # 圆心
print(f'圆心：({cx:.1f}, {cy:.1f}, {cz:.1f})')
print(f'半径：{R}mm')

# 起点：(cx+R, cy, cz)
start = (cx+R, cy, cz, tcp[3], tcp[4], tcp[5])
print(f'起点：({start[0]:.1f}, {start[1]:.1f}, {start[2]:.1f})')

# 先移动到起点
print('\n1. 移动到起点...')
r.linear_move_extend(start, 0, 1, 200, 100, 0.1)
time.sleep(1)

# 4 段 90 度圆弧
arcs = [
    {'end': (cx, cy+R, cz, tcp[3], tcp[4], tcp[5]), 'mid': (cx+R*0.707, cy+R*0.707, cz, tcp[3], tcp[4], tcp[5])},
    {'end': (cx-R, cy, cz, tcp[3], tcp[4], tcp[5]), 'mid': (cx-R*0.707, cy+R*0.707, cz, tcp[3], tcp[4], tcp[5])},
    {'end': (cx, cy-R, cz, tcp[3], tcp[4], tcp[5]), 'mid': (cx-R*0.707, cy-R*0.707, cz, tcp[3], tcp[4], tcp[5])},
    {'end': (cx+R, cy, cz, tcp[3], tcp[4], tcp[5]), 'mid': (cx+R*0.707, cy-R*0.707, cz, tcp[3], tcp[4], tcp[5])}
]

print('\n2. 开始画圆...')
start_time = time.time()
for i, arc in enumerate(arcs, 1):
    result = r.circular_move(arc['end'], arc['mid'], 0, 0, 100, 50, 0.1)
    # 轮询等待
    for j in range(20):
        time.sleep(0.2)
        if r.is_in_pos()[1]:
            break
    print(f'   第{i}段：{result}')

elapsed = time.time() - start_time
print(f'\n3. 完成！耗时：{elapsed:.2f}s')

# 验证
final = r.get_actual_tcp_position()[1]
print(f'终点：X={final[0]:.1f}, Y={final[1]:.1f}, Z={final[2]:.1f} mm')
error = math.sqrt((final[0]-start[0])**2 + (final[1]-start[1])**2)
print(f'闭合误差：{error:.2f}mm')

r.logout()
