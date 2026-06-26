"""
Vansbot 机械臂适配器

适配基于 MyCobot 的 Vansbot 机械臂，通过 HTTP API 控制。
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


class VansbotAdapter(RobotAdapter):
    """
    Vansbot 机械臂适配器

    支持的动作：
    - detect_objects: 检测桌面物体
    - move_to_object: 移动到物体上方
    - grab: 抓取物体
    - release: 释放物体
    - move_to_place: 移动到预设位置
    - capture_for_dog: 拍摄定位机器狗篮筐
    - release_to_dog: 将物体放入机器狗篮筐
    """

    def __init__(self, name: str, endpoint: str, **config):
        super().__init__(name, endpoint, **config)
        self.robot_type = RobotType.MANIPULATOR
        self.timeout = config.get("timeout", 60)
        self.session = requests.Session()

        # 定义能力
        self._capabilities = [
            RobotCapability(
                "detect_objects",
                "检测桌面物体",
                {"move_to_capture": "bool", "include_image": "bool"}
            ),
            RobotCapability(
                "move_to_object",
                "移动到物体上方",
                {"object_no": "int"}
            ),
            RobotCapability(
                "grab",
                "抓取物体",
                {}
            ),
            RobotCapability(
                "release",
                "释放物体",
                {}
            ),
            RobotCapability(
                "move_to_place",
                "移动到预设位置",
                {"place_name": "str"}  # capture, drop
            ),
            RobotCapability(
                "capture_for_dog",
                "拍摄定位机器狗篮筐",
                {"move_to_capture": "bool", "include_image": "bool"}
            ),
            RobotCapability(
                "release_to_dog",
                "将物体放入机器狗篮筐",
                {"point_id": "int"}
            ),
        ]

    def connect(self) -> bool:
        """连接到机械臂"""
        try:
            response = self.session.get(
                f"{self.endpoint}/health",
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
                message="机械臂未连接"
            )

        params = params or {}
        start_time = time.time()

        try:
            self._state.busy = True

            if action == "detect_objects":
                result = self._detect_objects(params)
            elif action == "move_to_object":
                result = self._move_to_object(params)
            elif action == "grab":
                result = self._grab()
            elif action == "release":
                result = self._release()
            elif action == "move_to_place":
                result = self._move_to_place(params)
            elif action == "capture_for_dog":
                result = self._capture_for_dog(params)
            elif action == "release_to_dog":
                result = self._release_to_dog(params)
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
                f"{self.endpoint}/health",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self._state.custom_data = data
                self._state.last_update = time.time()
        except Exception as e:
            self._state.error_message = str(e)

        return self._state

    def get_capabilities(self) -> List[RobotCapability]:
        """获取能力列表"""
        return self._capabilities

    # ========== 私有方法：具体动作实现 ==========

    def _detect_objects(self, params: Dict[str, Any]) -> ActionResult:
        """检测物体"""
        response = self.session.post(
            f"{self.endpoint}/capture",
            json=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()

        detections = data.get("detections", [])
        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"检测到 {len(detections)} 个物体",
            data={"detections": detections}
        )

    def _move_to_object(self, params: Dict[str, Any]) -> ActionResult:
        """移动到物体"""
        object_no = params.get("object_no", 0)
        response = self.session.post(
            f"{self.endpoint}/robot/move_to_object",
            json={"object_no": object_no},
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"已移动到物体 {object_no} 上方"
        )

    def _grab(self) -> ActionResult:
        """抓取"""
        response = self.session.post(
            f"{self.endpoint}/robot/grab",
            json={},
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="抓取完成"
        )

    def _release(self) -> ActionResult:
        """释放"""
        response = self.session.post(
            f"{self.endpoint}/robot/release",
            json={},
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="释放完成"
        )

    def _move_to_place(self, params: Dict[str, Any]) -> ActionResult:
        """移动到预设位置"""
        place_name = params.get("place_name", "capture")
        response = self.session.post(
            f"{self.endpoint}/robot/move_to_place",
            json={"place_name": place_name},
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"已移动到位置: {place_name}"
        )

    def _capture_for_dog(self, params: Dict[str, Any]) -> ActionResult:
        """拍摄定位机器狗篮筐"""
        response = self.session.post(
            f"{self.endpoint}/capture_for_finding_dog",
            json=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="已捕获网格图像",
            data=data
        )

    def _release_to_dog(self, params: Dict[str, Any]) -> ActionResult:
        """将物体放入机器狗篮筐"""
        point_id = params.get("point_id")
        if point_id is None:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="缺少参数: point_id"
            )

        response = self.session.post(
            f"{self.endpoint}/robot/release_to_dog",
            json={"point_id": point_id},
            timeout=self.timeout
        )
        response.raise_for_status()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message=f"已将物体放入篮筐（点位 {point_id}）"
        )
