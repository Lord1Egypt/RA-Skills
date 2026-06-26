#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOBOT CR10A - 运动指令测试
测试 MovL, Arc, Circle 等运动指令
"""

import sys
from pathlib import Path
import threading
from time import sleep
import re

sys.path.insert(0, str(Path(__file__).parent / "official-sdk"))

from dobot_api import DobotApiDashboard, DobotApiFeedBack

ROBOT_IP = "47.112.191.146"

feed_data = {'robot_mode': -1, 'command_id': 0}
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
                }
        except:
            pass
        sleep(0.1)

def parse_result(value_recv):
    if "Not Tcp" in value_recv:
        return [1, 0]
    numbers = re.findall(r'-?\d+', value_recv)
    return [int(numbers[0]), int(numbers[1]) if len(numbers) > 1 else 0]

def wait_motion_complete(dashboard, target_cmd_id, timeout=15):
    global feed_data
    for i in range(timeout * 10):
        mode = feed_data['robot_mode']
        cmd_id = feed_data['command_id']
        if mode == 5 and cmd_id >= target_cmd_id:
            return True
        sleep(0.1)
    return False

def test_separator(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def show_pose(dashboard):
    result = dashboard.GetPose()
    match = re.search(r'\{([^}]+)\}', result)
    if match:
        coords = [float(c) for c in match.group(1).split(',')]
        print(f"  Pose: X={coords[0]:.1f}, Y={coords[1]:.1f}, Z={coords[2]:.1f}")
        print(f"        RX={coords[3]:.1f}, RY={coords[4]:.1f}, RZ={coords[5]:.1f}")

try:
    # ========== 连接 ==========
    test_separator("STEP 1: CONNECT")
    dashboard = DobotApiDashboard(ROBOT_IP, 29999)
    feedback = DobotApiFeedBack(ROBOT_IP, 30004)
    print("[OK] Connected")
    
    t = threading.Thread(target=feedback_thread_func, args=(feedback,))
    t.daemon = True
    t.start()
    sleep(0.5)
    
    # ========== 初始化 ==========
    test_separator("STEP 2: INITIALIZE")
    dashboard.ClearError()
    dashboard.EnableRobot()
    print("[OK] Robot enabled")
    sleep(1)
    
    # 移动到起始位置
    print("Move to home position...")
    result = dashboard.MovJ(0, -300, 500, 180, 90, 0, coordinateMode=1)
    print(f"Command: {result}")
    sleep(2)
    show_pose(dashboard)
    
    # ========== TEST 1: MovL 直线运动 ==========
    test_separator("TEST 1: MovL (Linear Motion)")
    print("Note: MovL may return -2 in simulation (not supported)")
    print("Move in straight line to [100, -250, 450, 180, 90, 0]")
    
    result = dashboard.MovL(100, -250, 450, 180, 90, 0, coordinateMode=0)
    print(f"Command: {result}")
    code, cmd_id = parse_result(result)
    
    if code == 0:
        print(f"[OK] Command accepted (ID={cmd_id})")
        sleep(2)
        show_pose(dashboard)
    else:
        print(f"[INFO] MovL returned {code} (simulation may not support)")
    
    sleep(1)
    
    # ========== TEST 2: 返回起点 ==========
    test_separator("TEST 2: Return to Start")
    print("Return to [0, -300, 500, 180, 90, 0]")
    result = dashboard.MovJ(0, -300, 500, 180, 90, 0, coordinateMode=1)
    print(f"Command: {result}")
    sleep(2)
    show_pose(dashboard)
    
    sleep(1)
    
    # ========== TEST 3: 相对运动 ==========
    test_separator("TEST 3: RelJointMovJ")
    print("Relative joint move: J3 +10 degrees")
    result = dashboard.RelJointMovJ(0, 0, 10, 0, 0, 0)
    print(f"Command: {result}")
    code, cmd_id = parse_result(result)
    if code == 0:
        sleep(2)
        show_pose(dashboard)
    else:
        print(f"[INFO] RelJointMovJ returned {code}")
    
    sleep(1)
    
    # ========== TEST 4: Arc 圆弧运动 ==========
    test_separator("TEST 4: Arc (Circular Arc)")
    print("Arc: Current pos -> Via point -> End point")
    print("Starting from current position...")
    
    # 先移动到圆弧起点
    print("Move to arc start: [0, -200, 400, 180, 90, 0]")
    result = dashboard.MovL(0, -200, 400, 180, 90, 0, coordinateMode=0)
    print(f"Command: {result}")
    sleep(2)
    
    # 圆弧：经过点 (100,-150,400), 终点 (200,-200,400)
    # Arc 只需要 2 个点：via 点和终点，起点是当前位置
    print("Arc via [100, -150, 400] to [200, -200, 400]")
    result = dashboard.Arc(
        100, -150, 400, 180, 90, 0,    # 经过点
        200, -200, 400, 180, 90, 0,    # 终点
        coordinateMode=0
    )
    print(f"Command: {result}")
    code, cmd_id = parse_result(result)
    
    if code == 0:
        print(f"[OK] Arc command accepted (ID={cmd_id})")
        if wait_motion_complete(dashboard, cmd_id):
            print("[OK] Arc motion completed")
            show_pose(dashboard)
        else:
            print("[WARN] Arc motion timeout")
    else:
        print(f"[ERROR] Arc failed with code {code}")
    
    sleep(2)
    
    # ========== TEST 5: Circle 整圆运动 ==========
    test_separator("TEST 5: Circle (Full Circle)")
    print("Circle: 3 points define circle, complete full rotations")
    
    # 移动到圆起点
    print("Move to circle start: [0, -200, 400, 180, 90, 0]")
    result = dashboard.MovL(0, -200, 400, 180, 90, 0, coordinateMode=0)
    sleep(2)
    
    # 整圆：经过点、终点、圈数
    print("Circle via [100, -100, 400] to [0, 0, 400], count=1")
    result = dashboard.Circle(
        100, -100, 400, 180, 90, 0,    # 经过点
        0, 0, 400, 180, 90, 0,         # 终点
        coordinateMode=0,
        count=1
    )
    print(f"Command: {result}")
    code, cmd_id = parse_result(result)
    
    if code == 0:
        print(f"[OK] Circle command accepted (ID={cmd_id})")
        if wait_motion_complete(dashboard, cmd_id, timeout=20):
            print("[OK] Circle motion completed")
            show_pose(dashboard)
        else:
            print("[WARN] Circle motion timeout")
    else:
        print(f"[ERROR] Circle failed with code {code}")
    
    sleep(2)
    
    # ========== TEST 5: ServoJ 关节伺服 ==========
    test_separator("TEST 5: ServoJ (Joint Servo)")
    print("ServoJ for dynamic control (may not work in simulation)")
    result = dashboard.ServoJ(0, 0, 90, 0, 90, 0, t=0.1)
    print(f"Command: {result}")
    sleep(1)
    
    # ========== TEST 6: ServoP 笛卡尔伺服 ==========
    test_separator("TEST 6: ServoP (Cartesian Servo)")
    result = dashboard.ServoP(0, -300, 500, 180, 90, 0, t=0.1)
    print(f"Command: {result}")
    sleep(1)
    
    # ========== 返回初始位置 ==========
    test_separator("STEP 9: RETURN TO HOME")
    print("Return to home position...")
    result = dashboard.MovJ(0, 0, 90, 0, 90, 0, coordinateMode=1)
    print(f"Command: {result}")
    sleep(2)
    
    # ========== 最终状态 ==========
    test_separator("FINAL STATUS")
    result = dashboard.GetAngle()
    print(f"Final Joint Angles: {result}")
    result = dashboard.GetPose()
    print(f"Final Cartesian Pose: {result}")
    
    # ========== 下使能 ==========
    test_separator("DisableRobot")
    result = dashboard.DisableRobot()
    print(f"Result: {result}")
    
    # 清理
    stop_feedback = True
    dashboard.close()
    feedback.close()
    
    print("\n" + "=" * 70)
    print("MOTION COMMAND TEST COMPLETED")
    print("=" * 70)
    
except KeyboardInterrupt:
    print("\n\n[!] Interrupted by user")
    stop_feedback = True
    try:
        dashboard.DisableRobot()
        dashboard.close()
        feedback.close()
    except:
        pass
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
