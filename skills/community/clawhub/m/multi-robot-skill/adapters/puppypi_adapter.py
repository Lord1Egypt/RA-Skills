"""
PuppyPi 机器狗适配器

适配基于 ROS 的 PuppyPi 机器狗，通过 HTTP API 控制。
"""

import requests
import time
from typing import Any, Dict, List, Optional

from .base import (
    RobotAdapter,
    RobotCapability,
    RobotState,
    ActionResult,
    RobotType,
    ActionStatus,
)


class PuppyPiAdapter(RobotAdapter):
    """
    PuppyPi 机器狗适配器

    支持的动作：
    - move_to_zone: 移动到指定区域
    - adjust_posture: 调整姿态（装货/卸货）
    - load: 进入装货姿态
    - unload: 执行卸货动作
    """

    def __init__(self, name: str, endpoint: str, robot_id: int, **config):
        super().__init__(name, endpoint, **config)
        self.robot_type = RobotType.QUADRUPED
        self.robot_id = robot_id
        self.timeout = config.get("timeout", 60)
        self.session = requests.Session()

        # 定义能力
        self._capabilities = [
            RobotCapability(
                "move_to_zone",
                "移动到指定区域",
                {"target_zone": "str"}  # loading, unloading, charging, parking
            ),
            RobotCapability(
                "adjust_posture",
                "调整姿态",
                {"posture": "str"}  # loading, unloading, normal
            ),
            RobotCapability(
                "load",
                "进入装货姿态",
                {"target_zone": "str"}
            ),
            RobotCapability(
                "unload",
                "执行卸货动作",
                {}
            ),
        ]

    def connect(self) -> bool:
        """连接到机器狗"""
        try:
            response = self.session.get(
                f"{self.endpoint}/api/status",
                timeout=5
            )
            self._state.connected = response.status_code == 200
            return self._state.connected
        except Exception as e:
            self._state.connected = False
            self._state.error_message = str(e)
            return False

    def disconnect(self) -> bool:
        """断开连接"""
        self.session.close()
        self._state.connected = False
        return True

    def execute_action(self, action: str, params: Optional[Dict[str, Any]] = None) -> ActionResult:
        """执行动作"""
        if not self.is_connected():
            return ActionResult(
                status=ActionStatus.FAILED,
                message=f"机器狗 {self.name} 未连接"
            )

        params = params or {}
        start_time = time.time()

        try:
            self._state.busy = True

            if action == "move_to_zone":
                result = self._move_to_zone(params)
            elif action == "adjust_posture":
                result = self._adjust_posture(params)
            elif action == "load":
                result = self._load(params)
            elif action == "unload":
                result = self._unload()
            else:
                result = ActionResult(
                    status=ActionStatus.FAILED,
                    message=f"未知动作: {action}"
                )

            result.execution_time = time.time() - start_time
            return result

        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message=f"执行失败: {str(e)}",
                error=e,
                execution_time=time.time() - start_time
            )
        finally:
            self._state.busy = False

    def get_state(self) -> RobotState:
        """获取状态"""
        try:
            response = self.session.get(
                f"{self.endpoint}/api/dogs/{self.robot_id}/status",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                # API 返回的是 pose 而不是 position
                pose = data.get("pose")
                if pose:
                    self._state.position = {
                        "x": pose.get("x"),
                        "y": pose.get("y"),
                        "yaw": pose.get("yaw")
                    }
                self._state.battery = data.get("battery")
                self._state.custom_data = data
                self._state.last_update = time.time()
        except Exception as e:
            self._state.error_message = str(e)

        return self._state

    def get_capabilities(self) -> List[RobotCapability]:
        """获取能力列表"""
        return self._capabilities

    # ========== 私有方法：具体动作实现 ==========

    def _move_to_zone(self, params: Dict[str, Any]) -> ActionResult:
        """移动到区域"""
        target_zone = params.get("target_zone")
        if not target_zone:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="缺少参数: target_zone"
            )

        response = self.session.post(
            f"{self.endpoint}/api/task",
            json={
                "dog_id": self.robot_id,
                "action": "move",
                "target_zone": target_zone
            },
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"{self.name} 已移动到 {target_zone}"
        )

    def _adjust_posture(self, params: Dict[str, Any]) -> ActionResult:
        """调整姿态"""
        posture = params.get("posture", "normal")

        response = self.session.post(
            f"{self.endpoint}/api/task",
            json={
                "dog_id": self.robot_id,
                "action": "posture",
                "posture": posture
            },
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"{self.name} 已调整姿态: {posture}"
        )

    def _load(self, params: Dict[str, Any]) -> ActionResult:
        """进入装货姿态"""
        target_zone = params.get("target_zone", "loading")

        response = self.session.post(
            f"{self.endpoint}/api/task",
            json={
                "dog_id": self.robot_id,
                "action": "load",
                "target_zone": target_zone
            },
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"{self.name} 已进入装货姿态"
        )

    def _unload(self) -> ActionResult:
        """执行卸货"""
        response = self.session.post(
            f"{self.endpoint}/api/task",
            json={
                "dog_id": self.robot_id,
                "action": "unload"
            },
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"{self.name} 已完成卸货"
        )
