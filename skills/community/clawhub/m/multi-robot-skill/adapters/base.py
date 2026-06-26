"""
基础适配器接口和数据模型

定义了所有机器人适配器必须实现的接口。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
import time


class RobotType(Enum):
    """机器人类型"""
    MANIPULATOR = "manipulator"  # 机械臂
    QUADRUPED = "quadruped"      # 四足机器人
    WHEELED = "wheeled"          # 轮式机器人
    HUMANOID = "humanoid"        # 人形机器人
    AERIAL = "aerial"            # 无人机


class ActionStatus(Enum):
    """动作执行状态"""
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    IN_PROGRESS = "in_progress"


@dataclass
class RobotCapability:
    """机器人能力描述"""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        return f"{self.name}: {self.description}"


@dataclass
class RobotState:
    """机器人状态"""
    robot_name: str
    connected: bool = False
    busy: bool = False
    position: Optional[Dict[str, float]] = None
    battery: Optional[float] = None
    temperature: Optional[float] = None
    error_message: Optional[str] = None
    last_update: float = field(default_factory=time.time)
    custom_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "robot_name": self.robot_name,
            "connected": self.connected,
            "busy": self.busy,
            "position": self.position,
            "battery": self.battery,
            "temperature": self.temperature,
            "error_message": self.error_message,
            "last_update": self.last_update,
            **self.custom_data
        }


@dataclass
class ActionResult:
    """动作执行结果"""
    status: ActionStatus
    message: str = ""
    data: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    error: Optional[Exception] = None

    @property
    def success(self) -> bool:
        return self.status == ActionStatus.SUCCESS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "message": self.message,
            "data": self.data,
            "execution_time": self.execution_time,
            "error": str(self.error) if self.error else None
        }


class RobotAdapter(ABC):
    """
    机器人适配器基类

    所有机器人适配器必须继承此类并实现抽象方法。
    """

    def __init__(self, name: str, endpoint: str, **config):
        """
        初始化适配器

        Args:
            name: 机器人名称（唯一标识）
            endpoint: 机器人端点（URL、IP等）
            **config: 其他配置参数
        """
        self.name = name
        self.endpoint = endpoint
        self.config = config
        self.robot_type = RobotType.MANIPULATOR  # 子类应覆盖
        self._state = RobotState(robot_name=name)
        self._capabilities: List[RobotCapability] = []

    @abstractmethod
    def connect(self) -> bool:
        """
        连接到机器人

        Returns:
            bool: 连接是否成功
        """
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """
        断开与机器人的连接

        Returns:
            bool: 断开是否成功
        """
        pass

    @abstractmethod
    def execute_action(self, action: str, params: Optional[Dict[str, Any]] = None) -> ActionResult:
        """
        执行动作

        Args:
            action: 动作名称
            params: 动作参数

        Returns:
            ActionResult: 执行结果
        """
        pass

    @abstractmethod
    def get_state(self) -> RobotState:
        """
        获取机器人当前状态

        Returns:
            RobotState: 机器人状态
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[RobotCapability]:
        """
        获取机器人能力列表

        Returns:
            List[RobotCapability]: 能力列表
        """
        pass

    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self._state.connected

    def is_busy(self) -> bool:
        """检查是否正在执行任务"""
        return self._state.busy

    def can_execute(self, action: str) -> bool:
        """
        检查是否支持某个动作

        Args:
            action: 动作名称

        Returns:
            bool: 是否支持
        """
        return any(cap.name == action for cap in self.get_capabilities())

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, type={self.robot_type.value})"

    def __repr__(self):
        return self.__str__()
