import jkrc
import time

print("=== JAKA MiniCobo 连接测试 ===")
print(f"目标IP: 192.168.28.18")
print()

robot = jkrc.RC("192.168.28.18")
print("1. 创建 RC 对象成功")

print("2. 尝试登录...")
result = robot.login()
print(f"   登录结果: {result}")

if result[0] == 0:
    print("3. 连接成功!")
    print("4. 获取关节坐标...")
    joint = robot.joint_get_coordinates(0)
    print(f"   关节坐标: {joint}")
    print("5. 登出...")
    robot.logout()
    print("完成!")
else:
    print(f"   登录失败，错误码: {result[0]}")
    # 获取详细错误信息
    print(f"   可能原因: 网络不通 / SDK未开启 / 机器人未上电")
