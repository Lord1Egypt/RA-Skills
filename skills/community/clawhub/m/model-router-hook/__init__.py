"""
Model Router Hook V4 - 智能模型路由系统

自动根据任务复杂度选择最优 AI 模型。
"""

from .scripts.model_router import (
    ModelRouterHook,
    create_router,
    OpenClawIntegration,
    CostControllerV2,
    ResponseQualityEvaluator,
    ABTestRouter,
    Dashboard,
    ResilientModelRouter,
    understand_intent_v2,
    analyze_complexity,
    SessionMemory,
    GlobalUserMemory,
)

__version__ = "4.0.0"
__all__ = [
    "ModelRouterHook",
    "create_router",
    "OpenClawIntegration",
    "CostControllerV2",
    "ResponseQualityEvaluator",
    "ABTestRouter",
    "Dashboard",
    "ResilientModelRouter",
    "understand_intent_v2",
    "analyze_complexity",
    "SessionMemory",
    "GlobalUserMemory",
]
