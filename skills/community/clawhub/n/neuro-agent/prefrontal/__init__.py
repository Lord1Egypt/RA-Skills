"""
prefrontal/__init__.py
=====================

Neuro-Agent 前额叶区模块
负责：执行控制、融合输出、监控、冲突仲裁、奖励惩罚

子模块：
    - executor: 执行控制器
    - fusion_output: 融合输出
    - monitor: 监控层
    - conflict_arbitrator: 冲突仲裁器
    - reward_punishment: 奖励与惩罚系统
"""

from .executor import Executor, ArbitrationInput, ExecutorOutput, ResponseStrategy
from .fusion_output import FusionOutput, FusionResult, adjust_for_reward_punishment
from .monitor import Monitor, MonitorOutput, BlockedAction, Correction, IntentValidation
from .conflict_arbitrator import (
    BeliefConflictArbitrator,
    ConflictLevel,
    Verdict,
    ArbitrationResult,
    UserModel,
    UserModelManager
)
from .reward_punishment import (
    RewardPunishmentSystem,
    get_reward_punishment_system,
    TrustLevel,
    InteractionType,
    Interaction,
    BehaviorAdjustments,
    Scar,
    Cooldown,
    OffenseSeverity
)

__all__ = [
    # Executor
    "Executor",
    "ArbitrationInput",
    "ExecutorOutput",
    "ResponseStrategy",
    
    # Fusion Output
    "FusionOutput",
    "FusionResult",
    "adjust_for_reward_punishment",
    
    # Monitor
    "Monitor",
    "MonitorOutput",
    "BlockedAction",
    "Correction",
    "IntentValidation",
    
    # Conflict Arbitrator
    "BeliefConflictArbitrator",
    "ConflictLevel",
    "Verdict",
    "ArbitrationResult",
    "UserModel",
    "UserModelManager",
    
    # Reward Punishment
    "RewardPunishmentSystem",
    "get_reward_punishment_system",
    "TrustLevel",
    "InteractionType",
    "Interaction",
    "BehaviorAdjustments",
    "Scar",
    "Cooldown",
    "OffenseSeverity",
]
