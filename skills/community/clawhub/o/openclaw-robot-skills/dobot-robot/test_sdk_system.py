#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOBOT CR10A - SDK 系统测试 (P0 优先级)
测试基础功能和数字 IO
"""

import sys
from pathlib import Path
import threading
from time import sleep
import re

sys.path.insert(0, str(Path(__file__).parent / "official-sdk"))

from dobot_api import DobotApiDashboard, DobotApiFeedBack

ROBOT_IP = "47.112.191.146"

# 反馈数据
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

def test_separator(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

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
    
    # ========== P0-1: 清除错误 ==========
    test_separator("P0-1: ClearError")
    result = dashboard.ClearError()
    print(f"Result: {result}")
    sleep(0.5)
    
    # ========== P0-2: 使能机器人 ==========
    test_separator("P0-2: EnableRobot")
    result = dashboard.EnableRobot()
    print(f"Result: {result}")
    code, _ = parse_result(result)
    if code != 0:
        print(f"[ERROR] Enable failed: {code}")
        sys.exit(1)
    print("[OK] Robot enabled")
    sleep(1)
    
    # ========== P0-3: 获取当前状态 ==========
    test_separator("P0-3: GetAngle & GetPose")
    
    # 关节角度
    result = dashboard.GetAngle()
    print(f"Joint Angles: {result}")
    match = re.search(r'\{([^}]+)\}', result)
    if match:
        joints = [float(c) for c in match.group(1).split(',')]
        print(f"  J1={joints[0]:.1f}, J2={joints[1]:.1f}, J3={joints[2]:.1f}")
        print(f"  J4={joints[3]:.1f}, J5={joints[4]:.1f}, J6={joints[5]:.1f}")
    
    # 笛卡尔坐标
    result = dashboard.GetPose()
    print(f"Cartesian Pose: {result}")
    match = re.search(r'\{([^}]+)\}', result)
    if match:
        coords = [float(c) for c in match.group(1).split(',')]
        print(f"  X={coords[0]:.1f}, Y={coords[1]:.1f}, Z={coords[2]:.1f}")
        print(f"  RX={coords[3]:.1f}, RY={coords[4]:.1f}, RZ={coords[5]:.1f}")
    
    # ========== P0-4: 机器人模式 ==========
    test_separator("P0-4: RobotMode")
    mode = feed_data['robot_mode']
    print(f"Current Robot Mode: {mode}")
    mode_desc = {
        0: "断电",
        1: "上电中",
        2: "错误",
        3: "禁用",
        4: "运行中",
        5: "空闲",
        6: "初始化",
        7: "运动中",
        8: "暂停",
        9: "保持"
    }
    print(f"Description: {mode_desc.get(mode, 'Unknown')}")
    
    # ========== P0-5: 速度比例 ==========
    test_separator("P0-5: SpeedFactor")
    result = dashboard.SpeedFactor(50)
    print(f"Set speed to 50%: {result}")
    sleep(0.5)
    
    # ========== P0-6: 加速度比例 ==========
    test_separator("P0-6: AccJ & AccL")
    result = dashboard.AccJ(50)
    print(f"Set joint acceleration to 50%: {result}")
    result = dashboard.AccL(50)
    print(f"Set linear acceleration to 50%: {result}")
    sleep(0.5)
    
    # ========== P0-7: 速度指令 ==========
    test_separator("P0-7: VelJ & VelL")
    result = dashboard.VelJ(50)
    print(f"Set joint velocity to 50%: {result}")
    result = dashboard.VelL(50)
    print(f"Set linear velocity to 50%: {result}")
    sleep(0.5)
    
    # ========== P1-1: 设置负载 ==========
    test_separator("P1-1: SetPayload")
    result = dashboard.SetPayload(1.5, 0, 0, 50)  # 1.5kg, 中心偏移
    print(f"Set payload 1.5kg: {result}")
    sleep(0.5)
    
    # ========== P1-2: 数字输出测试 ==========
    test_separator("P1-2: Digital Output (DO)")
    print("Testing DO pins 0-3...")
    for i in range(4):
        result = dashboard.DO(i, 1)  # ON
        print(f"  DO[{i}]=ON: {result}")
        sleep(0.3)
        result = dashboard.DO(i, 0)  # OFF
        print(f"  DO[{i}]=OFF: {result}")
        sleep(0.3)
    
    # ========== P1-3: 读取数字输入 ==========
    test_separator("P1-3: Digital Input (DI)")
    print("Reading DI pins 0-7...")
    for i in range(8):
        try:
            result = dashboard.DI(i)
            print(f"  DI[{i}]: {result}")
            sleep(0.1)
        except Exception as e:
            print(f"  DI[{i}]: Error - {e}")
    
    # ========== P1-4: 工具 DO ==========
    test_separator("P1-4: Tool DO")
    result = dashboard.ToolDO(0, 1)
    print(f"ToolDO[0]=ON: {result}")
    sleep(0.5)
    result = dashboard.ToolDO(0, 0)
    print(f"ToolDO[0]=OFF: {result}")
    sleep(0.5)
    
    # ========== P1-5: 模拟输出 ==========
    test_separator("P1-5: Analog Output (AO)")
    result = dashboard.AO(0, 5.0)
    print(f"Set AO[0]=5.0V: {result}")
    sleep(0.5)
    result = dashboard.AO(0, 0.0)
    print(f"Set AO[0]=0.0V: {result}")
    sleep(0.5)
    
    # ========== P1-6: 模拟输入 ==========
    test_separator("P1-6: Analog Input (AI)")
    try:
        result = dashboard.AI(0)
        print(f"AI[0]: {result}")
    except Exception as e:
        print(f"AI[0] Error: {e}")
    
    # ========== P2-1: 碰撞等级 ==========
    test_separator("P2-1: SetCollisionLevel")
    result = dashboard.SetCollisionLevel(3)
    print(f"Set collision level to 3 (medium): {result}")
    sleep(0.5)
    
    # ========== P2-2: 回退距离 ==========
    test_separator("P2-2: SetBackDistance")
    result = dashboard.SetBackDistance(10)
    print(f"Set back distance to 10mm: {result}")
    sleep(0.5)
    
    # ========== P2-3: 六维力传感器 ==========
    test_separator("P2-3: Force Sensor")
    try:
        result = dashboard.GetForce()
        print(f"Force sensor data: {result}")
    except Exception as e:
        print(f"Force sensor not available: {e}")
    
    # ========== P0-8: 运动测试 - 相对关节运动 ==========
    test_separator("P0-8: RelJointMovJ")
    print("Move J3 +10 degrees...")
    result = dashboard.RelJointMovJ(0, 0, 10, 0, 0, 0)
    print(f"Command: {result}")
    code, cmd_id = parse_result(result)
    if code == 0:
        sleep(2)
        result = dashboard.GetAngle()
        print(f"After move: {result}")
    
    # ========== P0-9: 返回初始位置 ==========
    test_separator("P0-9: Return to Home")
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
    print("SDK SYSTEM TEST COMPLETED")
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
