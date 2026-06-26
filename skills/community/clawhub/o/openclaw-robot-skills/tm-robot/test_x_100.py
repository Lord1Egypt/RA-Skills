#!/usr/bin/env python3
"""
TM Robot - 直线运动测试
使用新添加的 move_relative_line 方法
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot
import asyncio

async def test():
    print('='*70)
    print('TM Robot 直线运动测试 - X 轴 +100mm')
    print('='*70)
    
    robot = TMRobot('192.168.1.13')
    
    # 连接
    print('\n[连接]')
    await robot.connect_svr()
    await robot.connect_sct()
    
    # 当前位置
    print('\n[当前位置]')
    pose = await robot.get_pose()
    if pose:
        print(f'X={pose.x:7.1f}mm, Y={pose.y:7.1f}mm, Z={pose.z:7.1f}mm')
        print(f'RX={pose.rx:7.1f}°, RY={pose.ry:7.1f}°, RZ={pose.rz:7.1f}°')
    
    # X 轴运动 100mm
    print('\n[直线运动] X 轴 +100mm, 速度 20%')
    success = await robot.move_relative_line([100, 0, 0, 0, 0, 0], speed=0.2)
    
    if success:
        print('[OK] 运动完成')
        
        # 读取新位置
        print('\n[新位置]')
        pose2 = await robot.get_pose()
        if pose2:
            print(f'X={pose2.x:7.1f}mm, Y={pose2.y:7.1f}mm, Z={pose2.z:7.1f}mm')
            print(f'\n[验证] X 轴移动了 {pose2.x - pose.x:.1f}mm')
    else:
        print('[FAIL] 运动失败')
    
    await robot.disconnect()
    print('\n' + '='*70)

asyncio.run(test())
