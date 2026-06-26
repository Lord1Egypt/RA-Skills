"""
Adapters package

机器人适配器模块
"""

from .base import (
    RobotAdapter,
    RobotCapability,
    RobotState,
    ActionResult,
    RobotType,
    ActionStatus,
)

__all__ = [
    "RobotAdapter",
    "RobotCapability",
    "RobotState",
    "ActionResult",
    "RobotType",
    "ActionStatus",
]
