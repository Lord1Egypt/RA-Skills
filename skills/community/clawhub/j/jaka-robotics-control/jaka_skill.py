"""
JAKA Robotics Control Skill
封装 JAKA SDK，提供简洁的 Python API

⚠️ 重要参数说明：
- move_linear 的 speed 参数单位是 **mm/s**（不是倍率）
- 示例：speed=200 表示 200mm/s
- 使用 linear_move_extend API 实现，支持加速度和精度控制

📚 SDK 文档：https://www.jaka.com/docs/guide/SDK/Python.html
"""

import time
import math
from typing import List, Optional, Dict, Any

try:
    import jkrc
    HAS_JAKA_SDK = True
except ImportError:
    HAS_JAKA_SDK = False
    print("[警告] JAKA SDK (jkrc) 未安装")


class JAKARobot:
    """JAKA 协作机器人控制封装类"""
    
    def __init__(self, ip: str):
        self.ip = ip
        self.connected = False
        self.robot = None
        
    def connect(self) -> bool:
        if not HAS_JAKA_SDK:
            print("[错误] JAKA SDK 未安装")
            return False
        try:
            self.robot = jkrc.RC(self.ip)
            result = self.robot.login()
            if result[0] == 0:
                self.connected = True
                print(f"[成功] 已连接到 {self.ip}")
                return True
            print(f"[错误] 登录失败：{result}")
            return False
        except Exception as e:
            print(f"[错误] 连接失败：{e}")
            return False
    
    def disconnect(self):
        if self.robot:
            self.robot.logout()
            self.connected = False
            print("[信息] 已断开连接")
    
    def enable_robot(self) -> bool:
        if not self.connected:
            return False
        result = self.robot.enable_robot()
        if result[0] == 0:
            print("[成功] 机器人已使能")
            return True
        return False
    
    def get_state(self) -> Dict[str, Any]:
        if not self.connected:
            return {"error": "未连接"}
        try:
            joint_result = self.robot.get_actual_joint_position()
            tcp_result = self.robot.get_actual_tcp_position()
            joints = joint_result[1] if joint_result[0] == 0 else None
            tcp = tcp_result[1] if tcp_result[0] == 0 else None
            state = {'connected': True, 'joints_rad': joints, 'tcp_position': tcp}
            if joints:
                state['joints_deg'] = [round(j * 180 / math.pi, 2) for j in joints]
            return state
        except Exception as e:
            return {'error': str(e)}
    
    def move_joint(self, joints: List[float], speed: float = 0.5) -> bool:
        """关节运动（弧度制）"""
        if not self.connected:
            print("[错误] 未连接机器人")
            return False
        try:
            self.robot.set_rapidrate(speed)
            result = self.robot.joint_move(joints, 0, 1, speed)
            if result[0] == 0:
                print(f"[成功] 关节运动完成：{[round(j*180/math.pi,1) for j in joints]}°")
                return True
            print(f"[错误] 关节运动失败：{result}")
            return False
        except Exception as e:
            print(f"[错误] 关节运动异常：{e}")
            return False
    
    def move_linear(self, pose: List[float], speed: float = 200) -> bool:
        """
        直线运动（mm/度制）
        
        Args:
            pose: [x, y, z, rx, ry, rz] 位置 (mm) + 姿态 (度)
            speed: 速度 mm/s (默认 200mm/s)
        """
        if not self.connected:
            print("[错误] 未连接机器人")
            return False
        try:
            # 转换为弧度
            pose_rad = (
                pose[0], pose[1], pose[2],
                pose[3] * math.pi / 180,
                pose[4] * math.pi / 180,
                pose[5] * math.pi / 180
            )
            
            # linear_move_extend: speed(mm/s), acc(mm/s^2), tol(mm)
            acc = speed / 2
            tol = 0.1
            result = self.robot.linear_move_extend(pose_rad, 0, 0, speed, acc, tol)
            
            if result[0] != 0:
                print(f"[错误] 直线运动失败：{result}")
                return False
            
            # 轮询等待完成
            for i in range(100):
                time.sleep(0.2)
                if self.robot.is_in_pos()[1]:
                    break
            
            print(f"[成功] 直线运动完成：{pose[:3]}mm, 速度{speed}mm/s")
            return True
        except Exception as e:
            print(f"[错误] 直线运动异常：{e}")
            return False
    
    def home(self) -> bool:
        return self.move_joint([0, 0, 0, 0, 0, 0], speed=0.3)


def quick_connect(ip: str = "192.168.28.18") -> JAKARobot:
    robot = JAKARobot(ip)
    robot.connect()
    return robot
