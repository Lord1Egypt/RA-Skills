#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOBOT CR10A - 关节空间直接控制
设置指定关节角度

目标配置：
- J1 (S 轴): 0 度
- J2 (L 轴): 0 度
- J3 (U 轴): 90 度 ⭐
- J4 (R 轴): 0 度
- J5 (B 轴): 90 度 ⭐
- J6 (T 轴): 0 度
"""

import sys
from pathlib import Path
import threading
from time import sleep
import re

sys.path.insert(0, str(Path(__file__).parent / "official-sdk"))

from dobot_api import DobotApiDashboard, DobotApiFeedBack

print("=" * 70)
print("DOBOT CR10A - Joint Angle Direct Control")
print("=" * 70)
print()
print("Target Joint Angles:")
print("  J1 (S-axis): 0 deg")
print("  J2 (L-axis): 0 deg")
print("  J3 (U-axis): 90 deg [TARGET]")
print("  J4 (R-axis): 0 deg")
print("  J5 (B-axis): 90 deg [TARGET]")
print("  J6 (T-axis): 0 deg")
print()

ROBOT_IP = "47.112.191.146"

# 反馈数据
feed_data = {'robot_mode': -1, 'command_id': 0}
stop_feedback = False

def feedback_thread_func(feedback):
    """反馈线程"""
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
    """等待运动完成"""
    global feed_data
    print(f"Waiting for motion completion (CMD ID={target_cmd_id})...")
    
    for i in range(timeout * 10):
        mode = feed_data['robot_mode']
        cmd_id = feed_data['command_id']
        
        # Mode 5=空闲/完成，Mode 4=运行中，Mode 7=运动中
        if mode == 5 and cmd_id >= target_cmd_id:
            print(f"[OK] Motion completed (mode={mode}, cmd_id={cmd_id})")
            return True
        
        print(f"  Mode={mode}, CmdID={cmd_id}, Target={target_cmd_id}" + " " * 20, end='\r')
        sleep(0.1)
    
    print(f"\n[WARN] Timeout waiting for motion (mode={feed_data['robot_mode']})")
    return False

try:
    # ========== 连接 ==========
    print("[Step 1] Connect")
    print("-" * 70)
    dashboard = DobotApiDashboard(ROBOT_IP, 29999)
    feedback = DobotApiFeedBack(ROBOT_IP, 30004)
    print("[OK] Connected")
    
    # 启动反馈线程
    t = threading.Thread(target=feedback_thread_func, args=(feedback,))
    t.daemon = True
    t.start()
    sleep(0.5)
    
    # ========== 清除错误 ==========
    print("\n[Step 2] ClearError")
    print("-" * 70)
    result = dashboard.ClearError()
    print(f"Result: {result}")
    sleep(0.5)
    
    # ========== 使能机器人 ==========
    print("\n[Step 3] EnableRobot")
    print("-" * 70)
    result = dashboard.EnableRobot()
    print(f"Result: {result}")
    code, _ = parse_result(result)
    if code != 0:
        print(f"[ERROR] Enable failed: {code}")
        sys.exit(1)
    print("[OK] Robot enabled")
    sleep(1)
    
    # ========== 获取当前关节角度 ==========
    print("\n[Step 4] GetPose (Current)")
    print("-" * 70)
    result = dashboard.GetPose()
    print(f"Current Pose: {result}")
    
    # ========== 关节空间运动 - 目标位置 ==========
    print("\n[Step 5] MovJ to Target Joint Configuration")
    print("-" * 70)
    print("Target: J1=0, J2=0, J3=90, J4=0, J5=90, J6=0")
    print("Note: Using MovJ with joint angles directly")
    
    # DOBOT MovJ 支持关节角度输入
    # coordinateMode=1 表示关节坐标模式
    # 格式：MovJ(j1, j2, j3, j4, j5, j6, coordinateMode=1)
    result = dashboard.MovJ(0, 0, 90, 0, 90, 0, coordinateMode=1)
    print(f"Command: {result}")
    code, cmd_id = parse_result(result)
    
    if code == 0:
        print(f"[OK] Command accepted (ID={cmd_id})")
        wait_motion_complete(dashboard, cmd_id)
        
        # 获取实际关节角度
        result = dashboard.GetAngle()
        print(f"Actual Joint Angles: {result}")
        
        # 解析关节角度
        match = re.search(r'\{([^}]+)\}', result)
        if match:
            joints = [float(c) for c in match.group(1).split(',')]
            print(f"J1={joints[0]:.1f}, J2={joints[1]:.1f}, J3={joints[2]:.1f}")
            print(f"J4={joints[3]:.1f}, J5={joints[4]:.1f}, J6={joints[5]:.1f}")
            
            # 验证目标角度
            if abs(joints[2] - 90) < 1 and abs(joints[4] - 90) < 1:
                print("\n[OK] SUCCESS: J3=90, J5=90 achieved!")
            else:
                print("\n[WARN] Joint angles not as expected")
    else:
        print(f"[ERROR] Move failed with code {code}")
    
    sleep(2)
    
    # ========== 获取最终关节角度 ==========
    print("\n[Step 6] GetAngle (Final)")
    print("-" * 70)
    result = dashboard.GetAngle()
    print(f"Final Joint Angles: {result}")
    
    # ========== 下使能 ==========
    print("\n[Step 7] DisableRobot")
    print("-" * 70)
    result = dashboard.DisableRobot()
    print(f"Result: {result}")
    
    # 清理
    stop_feedback = True
    dashboard.close()
    feedback.close()
    
    print("\n" + "=" * 70)
    print("Joint Control Test Completed")
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
