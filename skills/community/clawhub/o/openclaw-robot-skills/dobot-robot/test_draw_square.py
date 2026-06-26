#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOBOT CR10A - 画正方形测试
在 Z=400mm 水平面画 100mm 正方形
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

def get_current_pose(dashboard):
    result = dashboard.GetPose()
    match = re.search(r'\{([^}]+)\}', result)
    if match:
        coords = [float(c) for c in match.group(1).split(',')]
        return {
            'x': coords[0], 'y': coords[1], 'z': coords[2],
            'rx': coords[3], 'ry': coords[4], 'rz': coords[5]
        }
    return None

def wait_motion_complete(timeout=10):
    global feed_data
    for i in range(timeout * 10):
        if feed_data['robot_mode'] == 5:
            return True
        sleep(0.1)
    return False

def move_to(dashboard, x, y, z, rx, ry, rz, label):
    """移动到指定点"""
    print(f"\n  移动到 {label}: ({x:.1f}, {y:.1f}, {z:.1f})")
    result = dashboard.MovJ(x, y, z, rx, ry, rz, 0)  # coordinateMode=0 笛卡尔模式
    print(f"  命令：{result}")
    code, cmd_id = parse_result(result)
    if code == 0:
        print(f"  状态：[OK] 命令接受 (ID={cmd_id})")
        wait_motion_complete()
        actual = get_current_pose(dashboard)
        if actual:
            print(f"  实际：X={actual['x']:.1f}, Y={actual['y']:.1f}, Z={actual['z']:.1f}")
        return True
    else:
        print(f"  状态：[ERROR] 错误码 {code}")
        return False

try:
    print("=" * 70)
    print("DOBOT CR10A - Draw 100mm Square")
    print("在 Z=400mm 水平面画 100mm 正方形")
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
    
    # 获取当前位置
    print("\n" + "=" * 70)
    print("当前位置")
    print("=" * 70)
    current = get_current_pose(dashboard)
    if current:
        print(f"  X={current['x']:.1f}, Y={current['y']:.1f}, Z={current['z']:.1f}")
        print(f"  RX={current['rx']:.1f}, RY={current['ry']:.1f}, RZ={current['rz']:.1f}")
    
    # 定义正方形四个角点 (Z=400mm 水平面)
    # 假设当前姿态 RX=180, RY=90, RZ=0
    z_height = 400.0
    rx, ry, rz = 180.0, 90.0, 0.0
    
    # 正方形起点 (从当前位置附近开始)
    start_x = 0.0
    start_y = -250.0
    
    square_points = [
        (start_x, start_y, "A - 起点"),
        (start_x + 100, start_y, "B - 向右 100mm"),
        (start_x + 100, start_y + 100, "C - 向上 100mm"),
        (start_x, start_y + 100, "D - 向左 100mm"),
        (start_x, start_y, "A - 返回起点"),
    ]
    
    print("\n" + "=" * 70)
    print("正方形路径")
    print("=" * 70)
    print(f"  Z 高度：{z_height:.1f}mm")
    print(f"  姿态：RX={rx:.1f}, RY={ry:.1f}, RZ={rz:.1f}")
    print(f"  边长：100mm")
    print("\n  路径:")
    for i, (x, y, label) in enumerate(square_points):
        print(f"    {i+1}. {label}: ({x:.1f}, {y:.1f}, {z_height:.1f})")
    
    # 先移动到起点
    print("\n" + "=" * 70)
    print("开始画正方形")
    print("=" * 70)
    
    success_count = 0
    for i, (x, y, label) in enumerate(square_points):
        if move_to(dashboard, x, y, z_height, rx, ry, rz, label):
            success_count += 1
        sleep(0.5)
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("结果汇总")
    print("=" * 70)
    print(f"  总点数：{len(square_points)}")
    print(f"  成功：{success_count}")
    print(f"  成功率：{success_count/len(square_points)*100:.1f}%")
    
    # 最终位置
    print("\n" + "=" * 70)
    print("最终位置")
    print("=" * 70)
    final = get_current_pose(dashboard)
    if final:
        print(f"  X={final['x']:.1f}, Y={final['y']:.1f}, Z={final['z']:.1f}")
        print(f"  RX={final['rx']:.1f}, RY={final['ry']:.1f}, RZ={final['rz']:.1f}")
    
    # 下使能
    dashboard.DisableRobot()
    
    # 清理
    stop_feedback = True
    dashboard.close()
    feedback.close()
    
    print("\n" + "=" * 70)
    print("SQUARE DRAW TEST COMPLETED")
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
