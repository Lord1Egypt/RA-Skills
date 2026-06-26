#!/usr/bin/env python3
"""
TM Robot - 圆弧运动测试
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot
import asyncio

async def test():
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
    pose = await robot.get_pose()
    if pose:
        print(f'X={pose.x:7.1f}mm, Y={pose.y:7.1f}mm, Z={pose.z:7.1f}mm')
        print(f'RX={pose.rx:7.1f}°, RY={pose.ry:7.1f}°, RZ={pose.rz:7.1f}°')
    
    # 圆弧运动
    print('\n[圆弧运动]')
    print('中间点：X+50mm, Y+50mm')
    print('终点：X+100mm, Y+0mm')
    
    # 计算目标点（基于当前位置）
    if pose:
        point1 = [pose.x + 50, pose.y + 50, pose.z, pose.rx, pose.ry, pose.rz]
        point2 = [pose.x + 100, pose.y, pose.z, pose.rx, pose.ry, pose.rz]
    else:
        point1 = [500, -100, 400, 180, 0, 90]
        point2 = [550, -100, 400, 180, 0, 90]
    
    print(f'\n中间点：{point1[:3]}')
    print(f'终点：{point2[:3]}')
    
    success = await robot.move_circle(point1, point2, speed=0.3)
    
    if success:
        print('[OK] 圆弧运动完成')
        
        # 读取新位置
        print('\n[新位置]')
        pose2 = await robot.get_pose()
        if pose2:
            print(f'X={pose2.x:7.1f}mm, Y={pose2.y:7.1f}mm, Z={pose2.z:7.1f}mm')
    else:
        print('[FAIL] 圆弧运动失败')
    
    await robot.disconnect()
    print('\n' + '='*70)

asyncio.run(test())
