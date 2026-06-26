"""
TM Robot 完整示例 - 演示所有功能

功能：
1. 连接机器人（SCT + SVR）
2. 读取完整状态
3. 监控变量
4. 运动控制
5. I/O 控制
"""

import asyncio
import time
import sys
sys.path.insert(0, '..')  # Add parent directory to path
from tm_robot import TMRobot, SVRParser


async def demo_basic():
    """基础示例：连接并读取状态"""
    print("\n=== 基础示例 ===")
    
    robot = TMRobot("192.168.1.13")
    
    # 连接 SVR（状态读取）
    if await robot.connect_svr():
        print("[OK] SVR 连接成功")
    else:
        print("[FAIL] SVR 连接失败")
        return
    
    # 读取状态
    state = await robot.get_state()
    print(f"\n机器人状态：{state}")
    
    # 读取关节角度
    joints = await robot.get_joints()
    if joints:
        print(f"关节角度：{joints}")
    
    # 读取笛卡尔位姿
    pose = await robot.get_pose()
    if pose:
        print(f"笛卡尔位姿：{pose}")
    
    await robot.disconnect()
    print("\n[OK] 断开连接")


async def demo_monitoring():
    """监控示例：持续读取变量"""
    print("\n=== 监控示例（5 秒）===")
    
    parser = SVRParser("192.168.1.13")
    if not parser.connect(5):
        print("[FAIL] 连接失败")
        return
    
    print("[OK] SVR 连接成功，开始监控...\n")
    
    start = time.time()
    count = 0
    
    while time.time() - start < 5:
        # 读取关键变量
        error = parser.get_value("Error_Code")
        joints = parser.get_value("Joint_Angle")
        pose = parser.get_value("Coord_Robot_Flange")
        torque = parser.get_value("Joint_Torque")
        
        if joints:
            count += 1
            print(f"[{count:3d}] "
                  f"Err={error} "
                  f"J1={joints[0]:6.2f}° "
                  f"X={pose[0]:7.1f}mm "
                  f"T1={torque[0]:6.1f}mNm")
        
        await asyncio.sleep(0.1)  # 10Hz 刷新
    
    print(f"\n[OK] 监控完成，共读取 {count} 次")
    parser.disconnect()


async def demo_motion():
    """运动示例：关节运动"""
    print("\n=== 运动示例 ===")
    
    robot = TMRobot("192.168.1.13")
    
    # 连接 SCT（运动控制）
    if await robot.connect_sct():
        print("[OK] SCT 连接成功")
    else:
        print("[FAIL] SCT 连接失败")
        return
    
    # 读取当前角度
    joints = await robot.get_joints()
    if joints:
        print(f"当前角度：{joints}")
    
    # 回零
    print("\n正在回零...")
    if await robot.move_joints_zero(speed=0.05):
        print("[OK] 回零完成")
    
    # 移动到特定角度
    target = [10, -30, 60, 0, 45, 0]
    print(f"\n移动到：{target}")
    if await robot.move_joint(target, speed=0.1):
        print("[OK] 运动完成")
    
    # 停止
    await robot.stop_motion()
    
    await robot.disconnect()


async def demo_io():
    """I/O 示例：数字输出"""
    print("\n=== I/O 示例 ===")
    
    robot = TMRobot("192.168.1.13")
    
    if await robot.connect_sct():
        print("[OK] SCT 连接成功")
    else:
        return
    
    # 闪烁 DO0
    print("\n闪烁 DO0 3 次...")
    for i in range(3):
        await robot.set_digital_output(0, True)
        print(f"  DO0 = ON ({i+1}/3)")
        await asyncio.sleep(0.5)
        
        await robot.set_digital_output(0, False)
        print(f"  DO0 = OFF ({i+1}/3)")
        await asyncio.sleep(0.5)
    
    await robot.disconnect()
    print("\n[OK] I/O 测试完成")


async def demo_full():
    """完整示例：所有功能"""
    print("\n" + "="*50)
    print("TM Robot 完整功能演示")
    print("="*50)
    
    robot = TMRobot("192.168.1.13", use_custom_svr=True)
    
    # 1. 连接
    print("\n[1/5] 连接机器人...")
    if await robot.connect_all():
        print("[OK] SCT + SVR 连接成功")
    else:
        print("[FAIL] 连接失败")
        return
    
    # 2. 读取状态
    print("\n[2/5] 读取状态...")
    state = await robot.get_state()
    print(f"  模式：{state.mode}")
    print(f"  错误码：{state.error_code}")
    if state.joints:
        print(f"  关节：{state.joints}")
    if state.pose:
        print(f"  位姿：{state.pose}")
    
    # 3. 监控 3 秒
    print("\n[3/5] 监控变量（3 秒）...")
    for i in range(10):
        joints = robot._svr_parser.get_value("Joint_Angle")
        error = robot._svr_parser.get_value("Error_Code")
        if joints:
            print(f"  [{i+1}/10] J1={joints[0]:6.2f}° Err={error}")
        await asyncio.sleep(0.3)
    
    # 4. 运动测试
    print("\n[4/5] 运动测试...")
    print("  回零中...")
    await robot.move_joints_zero(speed=0.05)
    
    # 5. I/O 测试
    print("\n[5/5] I/O 测试...")
    await robot.set_digital_output(0, True)
    print("  DO0 = ON")
    await asyncio.sleep(0.5)
    await robot.set_digital_output(0, False)
    print("  DO0 = OFF")
    
    # 断开
    await robot.disconnect()
    
    print("\n" + "="*50)
    print("[OK] 演示完成！")
    print("="*50)


if __name__ == "__main__":
    # 选择要运行的示例
    print("选择示例：")
    print("1. 基础示例（读取状态）")
    print("2. 监控示例（持续读取）")
    print("3. 运动示例（关节运动）")
    print("4. I/O 示例（数字输出）")
    print("5. 完整示例（所有功能）")
    
    choice = input("\n输入编号 (1-5): ").strip()
    
    examples = {
        "1": demo_basic,
        "2": demo_monitoring,
        "3": demo_motion,
        "4": demo_io,
        "5": demo_full,
    }
    
    if choice in examples:
        asyncio.run(examples[choice]())
    else:
        print("无效选择，运行基础示例...")
        asyncio.run(demo_basic())
