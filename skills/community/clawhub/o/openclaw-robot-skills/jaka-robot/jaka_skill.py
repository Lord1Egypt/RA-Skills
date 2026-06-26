"""
JAKA Robotics Control Skill - v1.1.0
封装 JAKA SDK，提供简洁的 Python API

✅ 已更新到 OpenClaw Robot Skills 统一架构
- 统一 API 接口
- 完整类型注解
- 日志系统
- 与 TM Robot 保持一致

⚠️ 重要参数说明：
- move_linear 的 speed 参数单位是 **mm/s**（不是倍率）
- 示例：speed=200 表示 200mm/s
- 使用 linear_move_extend API 实现，支持加速度和精度控制

📚 SDK 文档：https://www.jaka.com/docs/guide/SDK/Python.html
"""

import time
import math
import logging
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('jaka_robot')

try:
    import jkrc
    HAS_JAKA_SDK = True
except ImportError:
    HAS_JAKA_SDK = False
    print("[警告] JAKA SDK (jkrc) 未安装")


# ==================== 数据类型 ====================

@dataclass
class JointAngles:
    """6 轴关节角度"""
    j1: float
    j2: float
    j3: float
    j4: float
    j5: float
    j6: float


@dataclass
class CartesianPose:
    """6 自由度笛卡尔位姿"""
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float


# ==================== 机器人控制类 ====================

class JakaRobot:
    """JAKA 协作机器人控制封装类"""
    
    def __init__(self, ip: str = "192.168.1.10"):
        self.ip = ip
        self.connected = False
        self.robot = None
        
    def connect(self) -> bool:
        """
        建立与 JAKA 机器人的连接
        
        Returns:
            bool: 连接是否成功
        """
        if not HAS_JAKA_SDK:
            logger.error("JAKA SDK not installed")
            print("[错误] JAKA SDK 未安装")
            return False
        try:
            logger.info(f"Connecting to {self.ip}")
            self.robot = jkrc.RC(self.ip)
            result = self.robot.login()
            if result[0] == 0:
                self.connected = True
                logger.info(f"Connected to {self.ip}")
                print(f"[OK] 已连接到 {self.ip}")
                return True
            logger.error(f"Login failed: {result}")
            print(f"[错误] 登录失败：{result}")
            return False
        except Exception as e:
            logger.error(f"Connect failed: {e}")
            print(f"[错误] 连接失败：{e}")
            return False
    
    def disconnect(self):
        """断开与机器人的连接"""
        if self.robot:
            self.robot.logout()
            self.connected = False
            logger.info("Disconnected")
            print("[信息] 已断开连接")
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        return self.connected
    
    def enable_robot(self) -> bool:
        """使能机器人"""
        if not self.connected:
            logger.error("Not connected")
            return False
        result = self.robot.enable_robot()
        if result[0] == 0:
            logger.info("Robot enabled")
            print("[成功] 机器人已使能")
            return True
        return False
    
    def get_joints(self) -> Optional[JointAngles]:
        """
        读取当前关节角度
        
        Returns:
            JointAngles: 关节角度 (度)
            None: 读取失败
        """
        if not self.connected:
            logger.error("Not connected")
            return None
        try:
            joint_result = self.robot.get_actual_joint_position()
            if joint_result[0] == 0:
                joints_rad = joint_result[1]
                joints_deg = [j * 180 / math.pi for j in joints_rad]
                logger.info(f"Joint angles: {joints_deg}")
                return JointAngles(*joints_deg)
            return None
        except Exception as e:
            logger.warning(f"Get joints failed: {e}")
            return None
    
    def get_pose(self) -> Optional[CartesianPose]:
        """
        读取当前笛卡尔位姿
        
        Returns:
            CartesianPose: 位姿 (mm, 度)
            None: 读取失败
        """
        if not self.connected:
            logger.error("Not connected")
            return None
        try:
            tcp_result = self.robot.get_actual_tcp_position()
            if tcp_result[0] == 0:
                tcp = tcp_result[1]
                logger.info(f"TCP position: {tcp}")
                return CartesianPose(*tcp)
            return None
        except Exception as e:
            logger.warning(f"Get pose failed: {e}")
            return None
    
    def get_state(self) -> Dict[str, Any]:
        """读取机器人完整状态"""
        if not self.connected:
            return {"error": "未连接"}
        try:
            joints = self.get_joints()
            pose = self.get_pose()
            return {
                'connected': True,
                'joints': joints,
                'pose': pose
            }
        except Exception as e:
            return {'error': str(e)}
    
    def move_joint(self, joints: List[float], speed: float = 0.5) -> bool:
        """
        关节运动（PTP）
        
        Args:
            joints: 目标关节角度 [J1, J2, J3, J4, J5, J6] (度)
            speed: 速度倍率 (0.0-1.0)
        
        Returns:
            bool: 运动是否成功
        """
        if not self.connected:
            logger.error("Not connected")
            print("[错误] 未连接机器人")
            return False
        try:
            # 转换为弧度
            joints_rad = [j * math.pi / 180 for j in joints]
            self.robot.set_rapidrate(speed)
            result = self.robot.joint_move(joints_rad, 0, 1, speed)
            if result[0] == 0:
                logger.info(f"Move joint: {joints}")
                print(f"[OK] 关节运动完成：{[round(j,1) for j in joints]}°")
                return True
            logger.error(f"Move joint failed: {result}")
            print(f"[错误] 关节运动失败：{result}")
            return False
        except Exception as e:
            logger.error(f"Move joint failed: {e}")
            print(f"[错误] 关节运动异常：{e}")
            return False
    
    def move_home(self, speed: float = 0.5) -> bool:
        """回零运动"""
        return self.move_joint([0, 0, 0, 0, 0, 0], speed=speed)
    
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
