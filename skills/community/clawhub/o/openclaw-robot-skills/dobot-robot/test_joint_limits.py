#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOBOT CR10A - 关节限位测试
测试 J1-J6 每个关节的正负方向运动
"""

import sys
from pathlib import Path
import threading
from time import sleep
import re

sys.path.insert(0, str(Path(__file__).parent / "official-sdk"))

from dobot_api import DobotApiDashboard, DobotApiFeedBack

ROBOT_IP = "47.112.191.146"

# 关节运动范围参考值 (度)
JOINT_LIMITS = {
    'J1': (-180, 180),
    'J2': (-135, 135),
    'J3': (-150, 150),
    'J4': (-180, 180),
    'J5': (-180, 180),
    'J6': (-360, 360),
}

feed_data = {'robot_mode': -1, 'command_id': 0, 'joints': [0]*6}
stop_feedback = False

def feedback_thread_func(feedback):
    global feed_data, stop_feedback
    while not stop_feedback:
        try:
            info = feedback.feedBackData()
            if info and hex(info['TestValue'][0]) == '0x123456789abcdef':
                feed_data = {
                    'robot_mode': info['RobotMode'][0],
                    'command_id': info['CurrentCommandId'][0],
                    'joints': list(info['QActual'][0:6]),
                }
        except:
            pass
        sleep(0.1)

def parse_result(value_recv):
    if "Not Tcp" in value_recv:
        return [1, 0]
    numbers = re.findall(r'-?\d+', value_recv)
    return [int(numbers[0]), int(numbers[1]) if len(numbers) > 1 else 0]

def get_current_joints(dashboard):
    """获取当前关节角度"""
    result = dashboard.GetAngle()
    match = re.search(r'\{([^}]+)\}', result)
    if match:
        return [float(c) for c in match.group(1).split(',')]
    return None

def wait_motion_complete(timeout=10):
    """等待运动完成"""
    global feed_data
    for i in range(timeout * 10):
        if feed_data['robot_mode'] == 5:
            return True
        sleep(0.1)
    return False

def test_joint_move(dashboard, joint_name, target_joints, direction):
    """测试单个关节运动"""
    print(f"\n  测试 {joint_name} {direction} 方向...")
    print(f"  目标角度：{target_joints}")
    
    result = dashboard.MovJ(*target_joints, 1)  # coordinateMode=1 关节模式
    print(f"  命令返回：{result}")
    
    code, cmd_id = parse_result(result)
    if code == 0:
        print(f"  状态：[OK] 命令接受 (ID={cmd_id})")
        if wait_motion_complete():
            actual = get_current_joints(dashboard)
            if actual:
                print(f"  实际角度：{[f'{a:.1f}' for a in actual]}")
                return True
        else:
            print(f"  状态：[WARN] 运动超时")
            return False
    else:
        print(f"  状态：[ERROR] 错误码 {code}")
        return False

try:
    print("=" * 70)
    print("DOBOT CR10A - Joint Limit Test")
    print("测试 J1-J6 每个关节的正负限位")
    print("=" * 70)
    
    # 连接
    dashboard = DobotApiDashboard(ROBOT_IP, 29999)
    feedback = DobotApiFeedBack(ROBOT_IP, 30004)
    print("\n[OK] Connected")
    
    t = threading.Thread(target=feedback_thread_func, args=(feedback,))
    t.daemon = True
    t.start()
    sleep(0.5)
    
    # 使能
    dashboard.ClearError()
    result = dashboard.EnableRobot()
    print(f"EnableRobot: {result}")
    sleep(1)
    
    # 获取初始位置
    print("\n" + "=" * 70)
    print("初始位置")
    print("=" * 70)
    initial_joints = get_current_joints(dashboard)
    if initial_joints:
        for i, name in enumerate(['J1', 'J2', 'J3', 'J4', 'J5', 'J6']):
            print(f"  {name}: {initial_joints[i]:.1f}°")
    
    # 测试每个关节
    joint_names = ['J1', 'J2', 'J3', 'J4', 'J5', 'J6']
    test_results = {name: {'positive': False, 'negative': False} for name in joint_names}
    
    for i, joint_name in enumerate(joint_names):
        print("\n" + "=" * 70)
        print(f"测试 {joint_name} (轴 {i+1})")
        print(f"  范围：{JOINT_LIMITS[joint_name][0]}° ~ {JOINT_LIMITS[joint_name][1]}°")
        print("=" * 70)
        
        # 先回到中间位置
        print("\n[复位] 回到中间位置...")
        mid_joints = initial_joints.copy()
        mid_joints[i] = 0  # 当前关节归零
        result = dashboard.MovJ(*mid_joints, 1)
        print(f"  命令：{result}")
        sleep(2)
        
        # 测试正方向
        positive_joints = initial_joints.copy()
        positive_joints[i] = min(initial_joints[i] + 30, JOINT_LIMITS[joint_name][1])
        test_results[joint_name]['positive'] = test_joint_move(
            dashboard, joint_name, positive_joints, "正"
        )
        sleep(1)
        
        # 测试负方向
        negative_joints = initial_joints.copy()
        negative_joints[i] = max(initial_joints[i] - 30, JOINT_LIMITS[joint_name][0])
        test_results[joint_name]['negative'] = test_joint_move(
            dashboard, joint_name, negative_joints, "负"
        )
        sleep(1)
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    print(f"{'关节':<8} {'正方向':<10} {'负方向':<10}")
    print("-" * 30)
    for name in joint_names:
        pos = "[OK]" if test_results[name]['positive'] else "[FAIL]"
        neg = "[OK]" if test_results[name]['negative'] else "[FAIL]"
        print(f"{name:<8} {pos:<10} {neg:<10}")
    
    # 返回初始位置
    print("\n" + "=" * 70)
    print("返回初始位置")
    print("=" * 70)
    result = dashboard.MovJ(*initial_joints, 1)
    print(f"命令：{result}")
    sleep(2)
    
    # 最终状态
    final_joints = get_current_joints(dashboard)
    if final_joints:
        print("\n最终关节角度:")
        for i, name in enumerate(joint_names):
            print(f"  {name}: {final_joints[i]:.1f}°")
    
    # 下使能
    dashboard.DisableRobot()
    
    # 清理
    stop_feedback = True
    dashboard.close()
    feedback.close()
    
    print("\n" + "=" * 70)
    print("JOINT LIMIT TEST COMPLETED")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    stop_feedback = True
    try:
        dashboard.close()
        feedback.close()
    except:
        pass
