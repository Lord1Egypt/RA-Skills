import jkrc

robot = jkrc.RC("192.168.28.18")
print("登录...")
result = robot.login()
print(f"登录结果: {result}")

if result[0] == 0:
    print("\n=== 可用的方法 ===")
    methods = [m for m in dir(robot) if not m.startswith('_')]
    for m in methods:
        print(f"  {m}")
    
    print("\n=== 测试获取状态 ===")
    # 尝试不同的API
    try:
        print("尝试 get_tcp_position...")
        pos = robot.get_tcp_position(0)
        print(f"  TCP位置: {pos}")
    except Exception as e:
        print(f"  错误: {e}")
    
    robot.logout()
    print("\n完成!")
else:
    print("登录失败")
