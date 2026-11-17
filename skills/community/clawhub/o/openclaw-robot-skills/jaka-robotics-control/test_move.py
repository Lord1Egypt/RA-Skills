import jkrc

robot = jkrc.RC("192.168.28.18")
robot.login()

print("测试 joint_move...")
# joints, relative, is_block, speed
tests = [
    ([0, 0, 0, 0, 0, 0], 0, 0, 0.3),
    ([0, 0, 0, 0, 0, 0], 0, 1, 0.3),
]

for args in tests:
    try:
        print(f"尝试 joint_move{args}...")
        result = robot.joint_move(*args)
        print(f"  结果: {result}")
        if result[0] == 0:
            print("  成功!")
            break
    except Exception as e:
        print(f"  错误: {e}")

robot.logout()
