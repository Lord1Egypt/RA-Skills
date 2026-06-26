"""
Multi-Robot Coordination Skill for Claude Code

一个专为 Claude Code AI Agent 设计的多机器人协同控制技能包。
"""

__version__ = "1.0.0"
__author__ = "Claude Code"

from .skill import MultiRobotSkill
from .adapters.base import (
    RobotAdapter,
    RobotCapability,
    ActionResult,
    RobotType,
    ActionStatus,
    RobotState
)
from .core.task_planner import TaskPlanner, Task, TaskPlan
from .core.coordinator import Coordinator
from .core.state_manager import StateManager

__all__ = [
    "MultiRobotSkill",
    "RobotAdapter",
    "RobotCapability",
    "ActionResult",
    "RobotType",
    "ActionStatus",
    "RobotState",
    "TaskPlanner",
    "Task",
    "TaskPlan",
    "Coordinator",
    "StateManager",
]
