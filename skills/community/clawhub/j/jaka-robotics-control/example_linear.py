"""
JAKA 直线运动示例 - 正确速度参数用法

⚠️ 重要：speed 参数单位是 mm/s，不是倍率！
"""

from jaka_skill import JAKARobot
import time
import math

def main():
    print("=" * 50)
    print("JAKA 直线运动测试 - 速度参数示例")
    print("=" * 50)
    
    # 连接机器人
    robot = JAKARobot("192.168.28.18")
    robot.connect()
    robot.enable_robot()
    time.sleep(0.5)
    
    # 准备姿态：J3=90°, J5=90°
    print("\n1. 准备姿态...")
    robot.move_joint([0, 0, math.pi/2, 0, math.pi/2, 0], speed=0.8)
    time.sleep(2)
    
    # 获取当前位置
    state = robot.get_state()
    tcp = state['tcp_position']
    print(f"   当前 TCP: X={tcp[0]:.1f}mm")
    
    # 测试不同速度
    print("\n2. 测试不同速度参数...")
    
    for speed in [100, 200, 400]:
        print(f"\n   测试 speed={speed}mm/s:")
        
        # 获取当前位置
        state = robot.get_state()
        tcp = state['tcp_position']
        
        # X+10mm
        target = [tcp[0]+10, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5]]
        
        start = time.time()
        result = robot.move_linear(target, speed=speed)
        elapsed = time.time() - start
        
        # 验证
        state2 = robot.get_state()
        moved = state2['tcp_position'][0] - tcp[0]
        
        print(f"   移动：{moved:.1f}mm, 耗时：{elapsed:.2f}s, 速度：{moved/elapsed:.1f}mm/s")
        
        time.sleep(1)
    
    # 回到原点
    print("\n3. 回到原点...")
    robot.move_joint([0, 0, 0, 0, 0, 0], speed=0.5)
    
    robot.disconnect()
    print("\n完成!")

if __name__ == "__main__":
    main()
