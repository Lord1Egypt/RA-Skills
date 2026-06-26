import jkrc
import inspect

robot = jkrc.RC("192.168.28.18")
robot.login()

# 查看 joint_move 的签名
sig = inspect.signature(robot.joint_move)
print(f"joint_move 签名: {sig}")

# 查看 linear_move 的签名
sig2 = inspect.signature(robot.linear_move)
print(f"linear_move 签名: {sig2}")

robot.logout()
