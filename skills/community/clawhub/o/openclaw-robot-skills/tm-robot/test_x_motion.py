"""
X 轴方向运动测试
沿 X 方向运动 100mm
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot
import asyncio

async def test_x_motion():
    print('='*70)
    print('TM Robot X 轴方向运动测试')
    print('='*70)
    
    robot = TMRobot('192.168.1.13')
    
    # 连接
    print('\n[连接]')
    await robot.connect_svr()
    await robot.connect_sct()
    
    # 获取当前笛卡尔位姿
    print('\n[读取当前笛卡尔位姿]')
    pose = await robot.get_pose()
    
    if pose:
        print(f'当前位姿:')
        print(f'  X = {pose.x:7.1f} mm')
        print(f'  Y = {pose.y:7.1f} mm')
        print(f'  Z = {pose.z:7.1f} mm')
        print(f'  RX= {pose.rx:7.1f} deg')
        print(f'  RY= {pose.ry:7.1f} deg')
        print(f'  RZ= {pose.rz:7.1f} deg')
        
        # 计算目标位置：X + 100mm
        target_x = pose.x + 100
        print(f'\n目标位置: X = {target_x:7.1f} mm (当前 X + 100mm)')
        
        # 尝试直线运动
        print('\n[尝试直线运动]')
        print('方法1: 使用 move_lin_cart 或类似方法...')
        
        # 检查可用方法
        if hasattr(robot._sct_conn, 'move_lin_cart'):
            print('找到 move_lin_cart 方法')
            try:
                target = [target_x, pose.y, pose.z, pose.rx, pose.ry, pose.rz]
                await robot._sct_conn.move_lin_cart(target, speed_perc=0.3)
                print('[OK] 直线运动完成')
            except Exception as e:
                print(f'[FAIL] {e}')
        else:
            print('未找到 move_lin_cart 方法')
            print('\n检查所有可用运动方法:')
            for attr in dir(robot._sct_conn):
                if 'move' in attr.lower() or 'lin' in attr.lower() or 'cart' in attr.lower():
                    print(f'  {attr}')
        
        # 读取运动后位置
        print('\n[读取运动后位置]')
        pose2 = await robot.get_pose()
        if pose2:
            print(f'运动后位姿:')
            print(f'  X = {pose2.x:7.1f} mm')
            print(f'  Y = {pose2.y:7.1f} mm')
            print(f'  Z = {pose2.z:7.1f} mm')
            
            if abs(pose2.x - target_x) < 5:
                print(f'\n[OK] X 轴运动成功！移动了 {pose2.x - pose.x:.1f} mm')
            else:
                print(f'\n[WARN] X 轴运动结果不符')
    else:
        print('[FAIL] 无法读取笛卡尔位姿')
    
    await robot.disconnect()
    print('\n' + '='*70)

asyncio.run(test_x_motion())
