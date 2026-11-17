import jkrc

robot = jkrc.RC("192.168.28.18")
print("=== JAKA MiniCobo 连接测试 ===")
print()

print("1. 登录...")
result = robot.login()
print(f"   结果: {'成功' if result[0] == 0 else '失败'}")

if result[0] == 0:
    print()
    print("2. 获取机器人状态...")
    state = robot.get_robot_status_simple()
    print(f"   状态: {state}")
    
    print()
    print("3. 获取关节位置...")
    joint = robot.get_actual_joint_position()
    print(f"   关节角度: {joint}")
    
    print()
    print("4. 获取TCP位置...")
    tcp = robot.get_actual_tcp_position()
    print(f"   TCP位置: {tcp}")
    
    print()
    print("5. 关节限位...")
    j1 = robot.get_joint_position(1)
    j2 = robot.get_joint_position(2)
    print(f"   J1: {j1}, J2: {j2}")
    
    print()
    robot.logout()
    print("=== 测试完成 ===")
else:
    print("登录失败!")
