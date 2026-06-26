"""
安全位置测试脚本
安全位置：J3=90°, J5=90°
"""

import sys
sys.path.insert(0, r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot')
from tm_robot import TMRobot
import asyncio

async def test():
    robot = TMRobot('192.168.1.13')
    
    # 1. 连接 SVR 监控
    print('=== 连接 SVR 监控 ===')
    await robot.connect_svr()
    
    # 2. 读取当前状态
    print('\n=== 当前状态 ===')
    joints = await robot.get_joints()
    pose = await robot.get_pose()
    
    if joints:
        print(f'关节角度：{joints}')
        print(f'  J1={joints.j1:6.2f}°, J2={joints.j2:6.2f}°, J3={joints.j3:6.2f}°')
        print(f'  J4={joints.j4:6.2f}°, J5={joints.j5:6.2f}°, J6={joints.j6:6.2f}°')
    
    if pose:
        print(f'\n笛卡尔位姿：{pose}')
        print(f'  X={pose.x:.1f}mm, Y={pose.y:.1f}mm, Z={pose.z:.1f}mm')
    
    # 3. 读取力矩
    print('\n=== 关节力矩 ===')
    torque = robot._svr_parser.get_value('Joint_Torque')
    if torque:
        print(f'力矩：{[f"{t:.1f}" for t in torque]} mNm')
    
    # 4. 安全位置
    print('\n=== 安全位置 ===')
    safe_pos = [0, 0, 90, 0, 90, 0]
    print(f'目标安全位置：J3=90°, J5=90°')
    print(f'  {safe_pos}')
    
    await robot.disconnect()

if __name__ == '__main__':
    asyncio.run(test())
