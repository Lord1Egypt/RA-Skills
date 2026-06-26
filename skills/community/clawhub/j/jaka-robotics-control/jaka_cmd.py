"""
JAKA Robot Command Line Tool
命令行控制 JAKA 协作机器人

用法:
    python jaka_cmd.py state           # 读取当前状态
    python jaka_cmd.py home             # 回零位
    python jaka_cmd.py joint 90 90 90 90 90 90   # 关节运动(角度)
    python jaka_cmd.py linear 300 0 200 180 0 0  # 直线运动(mm,度)
    python jaka_cmd.py io 1 on          # 设置DO1为ON
    python jaka_cmd.py io 1 off         # 设置DO1为OFF
"""

import sys
import math

# 配置机器人 IP
ROBOT_IP = "192.168.28.18"

# 导入 JAKA Skill
sys.path.insert(0, __file__.rsplit('\\', 1)[0] if '\\' in __file__ else __file__.rsplit('/', 1)[0])
try:
    from jaka_skill import JAKARobot
except ImportError:
    print("[错误] 无法导入 jaka_skill，请确保 jaka_skill.py 在同一目录")
    sys.exit(1)


def cmd_state():
    """读取机器人状态"""
    robot = JAKARobot(ROBOT_IP)
    if not robot.connect():
        return
    
    state = robot.get_state()
    print("\n=== 机器人状态 ===")
    print(f"连接状态: {'已连接' if state.get('connected') else '未连接'}")
    
    if state.get('joints_deg'):
        print(f"关节角度(°): {state['joints_deg']}")
    if state.get('tcp_position'):
        p = state['tcp_position']
        print(f"末端位置: X={p[0]:.1f}mm, Y={p[1]:.1f}mm, Z={p[2]:.1f}mm")
        print(f"          RX={p[3]:.1f}°, RY={p[4]:.1f}°, RZ={p[5]:.1f}°")
    
    robot.disconnect()


def cmd_home():
    """回零位"""
    robot = JAKARobot(ROBOT_IP)
    if not robot.connect():
        return
    
    print("执行回零...")
    robot.home()
    robot.disconnect()


def cmd_joint(args):
    """关节运动（角度）"""
    if len(args) < 6:
        print("[错误] 需要6个关节角度: joint 90 90 90 90 90 90")
        return
    
    try:
        joints_deg = [float(a) for a in args[:6]]
        joints_rad = [j * math.pi / 180 for j in joints_deg]
    except ValueError:
        print("[错误] 无效的角度值")
        return
    
    robot = JAKARobot(ROBOT_IP)
    if not robot.connect():
        return
    
    print(f"关节运动: {joints_deg}°")
    robot.move_joint(joints_rad, speed=0.3)
    robot.disconnect()


def cmd_linear(args):
    """直线运动（mm, 度）"""
    if len(args) < 6:
        print("[错误] 需要6个参数: linear 300 0 200 180 0 0")
        print("       [x, y, z, rx, ry, rz] - 位置(mm) + 姿态(度)")
        return
    
    try:
        pose = [float(a) for a in args[:6]]
    except ValueError:
        print("[错误] 无效的参数值")
        return
    
    robot = JAKARobot(ROBOT_IP)
    if not robot.connect():
        return
    
    print(f"直线运动: 位置={pose[:3]}mm, 姿态={pose[3:]}°")
    robot.move_linear(pose, speed=100)
    robot.disconnect()


def cmd_io(args):
    """设置 I/O"""
    if len(args) < 2:
        print("[错误] 用法: io <引脚号> <on|off>")
        return
    
    try:
        pin = int(args[0])
        value = args[1].lower() == 'on'
    except ValueError:
        print("[错误] 无效的参数")
        return
    
    robot = JAKARobot(ROBOT_IP)
    if not robot.connect():
        return
    
    robot.set_io(pin, value)
    robot.disconnect()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n可用命令:")
        print("  state           - 读取当前状态")
        print("  home            - 回零位")
        print("  joint <j1> <j2> <j3> <j4> <j5> <j6>  - 关节运动(角度)")
        print("  linear <x> <y> <z> <rx> <ry> <rz>      - 直线运动(mm,度)")
        print("  io <pin> <on|off>                      - 设置数字输出")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if cmd == 'state':
        cmd_state()
    elif cmd == 'home':
        cmd_home()
    elif cmd == 'joint':
        cmd_joint(args)
    elif cmd == 'linear':
        cmd_linear(args)
    elif cmd == 'io':
        cmd_io(args)
    else:
        print(f"[错误] 未知命令: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
