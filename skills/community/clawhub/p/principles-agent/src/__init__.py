"""
principles-agent
===============
基于第一性原理的迭代式 Agent 框架，OpenClaw 实现。

核心：
- 第一性原理需求解构
- 原子任务拆解
- 迭代式精炼
- 依赖感知调度
- 分层验证
- 全局整合
"""

from orchestrator import PrinciplesOrchestrator
from types_def import (
    Goal,
    FundamentalTruth,
    SubTask,
    ExecutionPlan,
    TaskResult,
    FinalResult,
    RefinementDecision,
    RefinementType
)

__version__ = "0.1.0"
__author__ = "OpenClaw"

__all__ = [
    "PrinciplesOrchestrator",
    "Goal",
    "FundamentalTruth",
    "SubTask",
    "ExecutionPlan",
    "TaskResult",
    "FinalResult",
    "RefinementDecision",
    "RefinementType"
]
