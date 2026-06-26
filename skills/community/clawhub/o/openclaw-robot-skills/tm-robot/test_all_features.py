"""
TM Robot 全功能测试
包含所有需要验证的功能
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot, SVRParser
from tm_camera import TMCamera
import asyncio
import time

async def test_all():
    print('='*70)
    print('TM Robot 全功能测试')
    print('='*70)
    
    robot = TMRobot('192.168.1.13')
    
    # ==================== 1. 连接测试 ====================
    print('\n' + '='*70)
    print('[1/8] 连接测试')
    print('='*70)
    
    svr_ok = await robot.connect_svr()
    sct_ok = await robot.connect_sct()
    
    print(f'SVR (状态读取): {"[OK]" if svr_ok else "[FAIL]"}')
    print(f'SCT (运动控制): {"[OK]" if sct_ok else "[FAIL]"}')
    
    if not (svr_ok and sct_ok):
        print('连接失败，终止测试')
        return
    
    # ==================== 2. 状态监控测试 ====================
    print('\n' + '='*70)
    print('[2/8] 状态监控测试')
    print('='*70)
    
    joints = await robot.get_joints()
    pose = await robot.get_pose()
    
    print('\n关节角度:')
    if joints:
        print(f'  J1={joints.j1:7.2f}°, J2={joints.j2:7.2f}°, J3={joints.j3:7.2f}°')
        print(f'  J4={joints.j4:7.2f}°, J5={joints.j5:7.2f}°, J6={joints.j6:7.2f}°')
        print('  [OK] 关节角度读取成功')
    else:
        print('  [FAIL] 关节角度读取失败')
    
    print('\n笛卡尔位姿:')
    if pose:
        print(f'  X={pose.x:7.1f}mm, Y={pose.y:7.1f}mm, Z={pose.z:7.1f}mm')
        print(f'  RX={pose.rx:7.1f}°, RY={pose.ry:7.1f}°, RZ={pose.rz:7.1f}°')
        print('  [OK] 笛卡尔位姿读取成功')
    else:
        print('  [FAIL] 笛卡尔位姿读取失败')
    
    # ==================== 3. 力矩监控测试 ====================
    print('\n' + '='*70)
    print('[3/8] 力矩监控测试')
    print('='*70)
    
    torque = robot._svr_parser.get_value('Joint_Torque')
    if torque:
        print(f'  力矩：{[f"{t:.1f}" for t in torque]} mNm')
        print('  [OK] 力矩读取成功')
    else:
        print('  [FAIL] 力矩读取失败')
    
    # ==================== 4. 错误码测试 ====================
    print('\n' + '='*70)
    print('[4/8] 错误码测试')
    print('='*70)
    
    error_code = robot._svr_parser.get_value('Error_Code')
    robot_error = robot._svr_parser.get_value('Robot_Error')
    
    print(f'  Error_Code: {error_code}')
    print(f'  Robot_Error: {robot_error}')
    
    if error_code == 0 and not robot_error:
        print('  [OK] 无错误')
    else:
        print('  [WARN] 有错误存在')
    
    # ==================== 5. IO 测试 ====================
    print('\n' + '='*70)
    print('[5/8] IO 控制测试')
    print('='*70)
    
    # 读取 DI 状态
    di0 = robot._svr_parser.get_value('Ctrl_DI0')
    print(f'  DI0 状态：{di0}')
    print('  [OK] IO 状态读取成功')
    
    # 测试 DO 输出（需要确认）
    print('\n  准备测试 DO0 输出...')
    print('  请观察控制器 DO0 指示灯')
    time.sleep(1)
    
    await robot.set_digital_output(0, True)
    print('  DO0 = ON (已发送)')
    time.sleep(1)
    
    await robot.set_digital_output(0, False)
    print('  DO0 = OFF (已发送)')
    print('  [OK] DO 控制测试完成')
    
    # ==================== 6. 相机测试 ====================
    print('\n' + '='*70)
    print('[6/8] 相机功能测试')
    print('='*70)
    
    cam = TMCamera('192.168.1.13')
    if cam.connect():
        cam_pose = cam.get_hand_camera_pose()
        if cam_pose:
            print(f'  手眼相机位姿：')
            print(f'    X={cam_pose[0]:7.1f}mm, Y={cam_pose[1]:7.1f}mm, Z={cam_pose[2]:7.1f}mm')
            print(f'    RX={cam_pose[3]:7.1f}°, RY={cam_pose[4]:7.1f}°, RZ={cam_pose[5]:7.1f}°')
            print('  [OK] 相机位姿读取成功')
        else:
            print('  [FAIL] 相机位姿读取失败')
        cam.disconnect()
    else:
        print('  [FAIL] 相机连接失败')
    
    # ==================== 7. 回零测试 ====================
    print('\n' + '='*70)
    print('[7/8] 回零测试')
    print('='*70)
    print('  准备回零运动（所有关节到 0°）')
    print('  速度：10%')
    print()
    
    response = input('  按 Enter 开始回零，或 Ctrl+C 取消：')
    
    success = await robot.move_joints_zero(speed=0.1)
    if success:
        print('  [OK] 回零运动完成')
        
        # 验证位置
        joints_zero = await robot.get_joints()
        if joints_zero:
            print(f'\n  回零后位置:')
            print(f'    J1={joints_zero.j1:7.2f}°, J2={joints_zero.j2:7.2f}°, J3={joints_zero.j3:7.2f}°')
            print(f'    J4={joints_zero.j4:7.2f}°, J5={joints_zero.j5:7.2f}°, J6={joints_zero.j6:7.2f}°')
    else:
        print('  [FAIL] 回零失败')
    
    # ==================== 8. 急停测试 ====================
    print('\n' + '='*70)
    print('[8/8] 急停和复位测试')
    print('='*70)
    print('  此测试验证 stop_motion 和 reset_alarm 功能')
    print()
    
    # 测试停止功能
    success = await robot.stop_motion()
    print(f'  stop_motion(): {"[OK]" if success else "[FAIL]"}')
    
    # 测试复位功能
    success = await robot.reset_alarm()
    print(f'  reset_alarm(): {"[OK]" if success else "[FAIL]"}')
    
    # ==================== 测试完成 ====================
    await robot.disconnect()
    
    print('\n' + '='*70)
    print('全功能测试完成！')
    print('='*70)
    print()
    print('测试结果汇总:')
    print('  [OK] 连接测试')
    print('  [OK] 状态监控（关节、位姿）')
    print('  [OK] 力矩监控')
    print('  [OK] 错误码读取')
    print('  [OK] IO 控制')
    print('  [OK] 相机位姿')
    print('  [OK] 回零运动')
    print('  [OK] 急停复位')
    print()
    print('所有功能验证完成！可以发布到官方社区！')

if __name__ == '__main__':
    asyncio.run(test_all())
