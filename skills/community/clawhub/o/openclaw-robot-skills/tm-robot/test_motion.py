"""
运动控制测试脚本
安全位置：J3=90°, J5=90°
速度：50%
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot
import asyncio

async def test_motion():
    robot = TMRobot('192.168.1.13')
    
    # 1. 连接
    print('='*60)
    print('TM Robot 运动控制测试')
    print('='*60)
    
    print('\n[1/4] 连接机器人...')
    if await robot.connect_svr():
        print('  [OK] SVR 连接成功')
    else:
        print('  [FAIL] SVR 连接失败')
        return
    
    if await robot.connect_sct():
        print('  [OK] SCT 连接成功')
    else:
        print('  [FAIL] SCT 连接失败')
        return
    
    # 2. 读取当前状态
    print('\n[2/4] 读取当前状态...')
    joints = await robot.get_joints()
    pose = await robot.get_pose()
    
    if joints:
        print(f'\n当前关节角度:')
        print(f'  J1 = {joints.j1:7.3f}°')
        print(f'  J2 = {joints.j2:7.3f}°')
        print(f'  J3 = {joints.j3:7.3f}°')
        print(f'  J4 = {joints.j4:7.3f}°')
        print(f'  J5 = {joints.j5:7.3f}°')
        print(f'  J6 = {joints.j6:7.3f}°')
        
        # 安全检查
        print(f'\n安全检查:')
        j3_safe = abs(joints.j3 - 90) < 5
        j5_safe = abs(joints.j5 - 90) < 5
        print(f'  J3 = {joints.j3:.1f}° {"[OK] 安全" if j3_safe else "[WARN] 注意"}')
        print(f'  J5 = {joints.j5:.1f}° {"[OK] 安全" if j5_safe else "[WARN] 注意"}')
    
    if pose:
        print(f'\n当前笛卡尔位姿:')
        print(f'  X = {pose.x:7.1f} mm')
        print(f'  Y = {pose.y:7.1f} mm')
        print(f'  Z = {pose.z:7.1f} mm')
    
    # 3. 读取力矩
    print('\n[3/4] 读取关节力矩...')
    torque = robot._svr_parser.get_value('Joint_Torque')
    if torque:
        print(f'  力矩：{[f"{t:.1f}" for t in torque]} mNm')
    
    # 4. 运动测试
    print('\n[4/4] 运动测试准备...')
    print(f'  目标位置：[0, 0, 90, 0, 90, 0]')
    print(f'  速度：50%')
    print()
    
    response = input('准备就绪！按 Enter 开始运动，或 Ctrl+C 取消：')
    
    print('\n>>> 开始运动...')
    success = await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.5)
    
    if success:
        print('[OK] 运动完成！')
        
        # 读取运动后位置
        print('\n运动后位置：')
        joints_after = await robot.get_joints()
        if joints_after:
            print(f'  J1 = {joints_after.j1:7.3f}°')
            print(f'  J2 = {joints_after.j2:7.3f}°')
            print(f'  J3 = {joints_after.j3:7.3f}°')
            print(f'  J4 = {joints_after.j4:7.3f}°')
            print(f'  J5 = {joints_after.j5:7.3f}°')
            print(f'  J6 = {joints_after.j6:7.3f}°')
    else:
        print('[FAIL] 运动失败')
    
    await robot.disconnect()
    print('\n' + '='*60)
    print('测试完成')
    print('='*60)

if __name__ == '__main__':
    asyncio.run(test_motion())
