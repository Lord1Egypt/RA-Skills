import sys
sys.path.insert(0, "C:\\Users\\JMO\\.openclaw\\workspace\\skills\\jaka-robotics-control")
from jaka_skill import JAKARobot

print("=== JAKA MiniCobo 完整测试 ===")
print()

robot = JAKARobot("192.168.28.18")

# 连接
if not robot.connect():
    print("连接失败!")
    exit(1)

# 获取状态
print()
state = robot.get_state()
print(f"关节角度(°): {state.get('joints_deg')}")
print(f"TCP位置(mm): {[round(x, 1) for x in state.get('tcp_position', [])[:3]]}")

# 测试关节运动
print()
print("测试关节运动到 [0, 0, 0, 0, 0, 0]...")
robot.move_joint([0, 0, 0, 0, 0, 0], speed=0.3)

# 断开
robot.disconnect()
print()
print("=== 测试完成 ===")
