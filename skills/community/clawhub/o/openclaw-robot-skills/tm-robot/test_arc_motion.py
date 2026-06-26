"""
圆弧运动测试
测试 techmanpy 支持的圆弧指令
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot
import asyncio

async def test_arc():
    print('='*70)
    print('TM Robot 圆弧运动测试')
    print('='*70)
    
    robot = TMRobot('192.168.1.13')
    
    # 连接
    print('\n[连接]')
    await robot.connect_svr()
    await robot.connect_sct()
    
    # 当前位置
    print('\n[当前位置]')
    joints = await robot.get_joints()
    if joints:
        print(f'J1={joints.j1:6.1f}°, J2={joints.j2:6.1f}°, J3={joints.j3:6.1f}°')
        print(f'J4={joints.j4:6.1f}°, J5={joints.j5:6.1f}°, J6={joints.j6:6.1f}°')
    
    # 测试圆弧运动
    print('\n[圆弧运动测试]')
    print('尝试使用 move_arc 方法...')
    
    # 检查是否有 move_arc 方法
    if hasattr(robot._sct_conn, 'move_arc'):
        print('发现 move_arc 方法')
        # 圆弧运动需要：起点、中间点、终点
        # 从当前位置到中间点再到终点
        via_point = [10, -20, 80, 0, 80, 0]  # 中间点
        end_point = [0, 0, 90, 0, 90, 0]      # 终点
        
        try:
            await robot._sct_conn.move_arc(via_point, end_point, speed_perc=0.3)
            print('[OK] 圆弧运动完成')
        except Exception as e:
            print(f'[FAIL] 圆弧运动失败：{e}')
    else:
        print('未找到 move_arc 方法')
        print('可用方法：')
        for attr in dir(robot._sct_conn):
            if 'move' in attr.lower() and not attr.startswith('_'):
                print(f'  {attr}')
    
    # 测试直线运动
    print('\n[直线运动测试]')
    print('尝试使用 move_lin 方法...')
    
    if hasattr(robot._sct_conn, 'move_lin'):
        print('发现 move_lin 方法')
        target_pose = [400, -100, 400, 180, 0, 90]  # X, Y, Z, RX, RY, RZ
        
        try:
            await robot._sct_conn.move_lin(target_pose, speed_perc=0.3)
            print('[OK] 直线运动完成')
        except Exception as e:
            print(f'[FAIL] 直线运动失败：{e}')
    else:
        print('未找到 move_lin 方法')
    
    # 回到安全位置
    print('\n[返回安全位置]')
    await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.3)
    print('完成')
    
    await robot.disconnect()

asyncio.run(test_arc())
