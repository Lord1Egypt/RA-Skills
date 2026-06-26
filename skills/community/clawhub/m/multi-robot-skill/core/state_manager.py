"""
状态管理器

负责跟踪和管理所有机器人的状态。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import time
import threading

from ..adapters.base import RobotAdapter, RobotState


class SystemStatus(Enum):
    """系统状态"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"


@dataclass
class SystemState:
    """系统状态"""
    status: SystemStatus = SystemStatus.IDLE
    active_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    start_time: Optional[float] = None
    last_update: float = field(default_factory=time.time)


class StateManager:
    """
    状态管理器

    负责跟踪和管理所有机器人的状态。
    """

    def __init__(self):
        self.robots: Dict[str, RobotAdapter] = {}
        self.robot_states: Dict[str, RobotState] = {}
        self.system_state = SystemState()
        self._lock = threading.Lock()
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None

    def register_robot(self, robot: RobotAdapter):
        """注册机器人"""
        with self._lock:
            self.robots[robot.name] = robot
            self.robot_states[robot.name] = robot.get_state()

    def unregister_robot(self, robot_name: str):
        """注销机器人"""
        with self._lock:
            if robot_name in self.robots:
                del self.robots[robot_name]
            if robot_name in self.robot_states:
                del self.robot_states[robot_name]

    def update_robot_state(self, robot_name: str):
        """更新机器人状态"""
        robot = self.robots.get(robot_name)
        if robot:
            with self._lock:
                self.robot_states[robot_name] = robot.get_state()

    def update_all_states(self):
        """更新所有机器人状态"""
        for robot_name in list(self.robots.keys()):
            self.update_robot_state(robot_name)

    def get_robot_state(self, robot_name: str) -> Optional[RobotState]:
        """获取机器人状态"""
        with self._lock:
            return self.robot_states.get(robot_name)

    def get_all_states(self) -> Dict[str, RobotState]:
        """获取所有机器人状态"""
        with self._lock:
            return self.robot_states.copy()

    def get_system_state(self) -> SystemState:
        """获取系统状态"""
        with self._lock:
            return self.system_state

    def set_system_status(self, status: SystemStatus):
        """设置系统状态"""
        with self._lock:
            self.system_state.status = status
            self.system_state.last_update = time.time()

    def start_monitoring(self, interval: float = 1.0):
        """
        启动状态监控

        Args:
            interval: 监控间隔（秒）
        """
        if self._monitoring:
            return

        self._monitoring = True

        def monitor_loop():
            while self._monitoring:
                self.update_all_states()
                time.sleep(interval)

        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        """停止状态监控"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)

    def get_available_robots(self) -> List[str]:
        """获取可用的机器人列表"""
        available = []
        with self._lock:
            for robot_name, state in self.robot_states.items():
                if state.connected and not state.busy:
                    available.append(robot_name)
        return available

    def is_robot_available(self, robot_name: str) -> bool:
        """检查机器人是否可用"""
        state = self.get_robot_state(robot_name)
        if state:
            return state.connected and not state.busy
        return False

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        with self._lock:
            return {
                "system": {
                    "status": self.system_state.status.value,
                    "active_tasks": self.system_state.active_tasks,
                    "completed_tasks": self.system_state.completed_tasks,
                    "failed_tasks": self.system_state.failed_tasks,
                },
                "robots": {
                    name: state.to_dict()
                    for name, state in self.robot_states.items()
                }
            }
