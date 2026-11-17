import jkrc
import time
import math

print('=== 水平整圆测试 - 直径 20mm (360 度) ===')
r = jkrc.RC('192.168.28.18')
r.login()
r.enable_robot()
time.sleep(1)

# J3=90, J5=90
r.joint_move((0, 0, math.pi/2, 0, math.pi/2, 0), 0, 1, 1.0)
time.sleep(2)

tcp = r.get_actual_tcp_position()[1]
print(f'起点：X={tcp[0]:.1f}, Y={tcp[1]:.1f}, Z={tcp[2]:.1f} mm')

# 画圆参数
R = 10  # 半径 10mm
cx, cy, cz = tcp[0], tcp[1], tcp[2]
print(f'圆心：({cx:.1f}, {cy:.1f}, {cz:.1f})')
print(f'半径：{R}mm, 直径：{R*2}mm')

# 起点 (0 度)
start = (cx+R, cy, cz, tcp[3], tcp[4], tcp[5])
print(f'起点 (0 度): ({start[0]:.1f}, {start[1]:.1f})')

# 移动到起点
print('\n1. 移动到起点...')
r.linear_move_extend(start, 0, 1, 200, 100, 0.1)
time.sleep(1)

# 4 段 90 度圆弧 = 360 度整圆
print('\n2. 画整圆 (4 段×90 度 = 360 度)...')
arcs = [
    {'name': '0-90', 'end': (cx, cy+R, cz), 'mid': (cx+R*0.707, cy+R*0.707, cz)},
    {'name': '90-180', 'end': (cx-R, cy, cz), 'mid': (cx-R*0.707, cy+R*0.707, cz)},
    {'name': '180-270', 'end': (cx, cy-R, cz), 'mid': (cx-R*0.707, cy-R*0.707, cz)},
    {'name': '270-360', 'end': (cx+R, cy, cz), 'mid': (cx+R*0.707, cy-R*0.707, cz)}
]

start_time = time.time()
for i, arc in enumerate(arcs, 1):
    end_pos = (arc['end'][0], arc['end'][1], arc['end'][2], tcp[3], tcp[4], tcp[5])
    mid_pos = (arc['mid'][0], arc['mid'][1], arc['mid'][2], tcp[3], tcp[4], tcp[5])
    
    result = r.circular_move(end_pos, mid_pos, 0, 0, 100, 50, 0.1)
    
    # 轮询等待完成
    for j in range(30):
        time.sleep(0.2)
        if r.is_in_pos()[1]:
            break
    
    pos = r.get_actual_tcp_position()[1]
    print(f'   第{i}段 {arc["name"]}: {result} -> ({pos[0]:.1f}, {pos[1]:.1f})')

elapsed = time.time() - start_time
print(f'\n3. 整圆完成！耗时：{elapsed:.2f}s')

# 验证
final = r.get_actual_tcp_position()[1]
error = math.sqrt((final[0]-start[0])**2 + (final[1]-start[1])**2)
print(f'\n起点：({start[0]:.1f}, {start[1]:.1f})')
print(f'终点：({final[0]:.1f}, {final[1]:.1f})')
print(f'闭合误差：{error:.2f}mm')

if error < 1:
    print('OK: 整圆测试成功！')
else:
    print(f'WARN: 误差{error:.2f}mm')

r.logout()
