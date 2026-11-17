"""
意图安全与审计模块

实现高风险意图安全保障，采用"纵深防御"策略：
- 操作白名单：只允许预定义的安全操作
- 权限分级：用户只能执行其权限范围内的操作
- 审计日志：记录所有操作，便于事后审查
- 操作确认：敏感操作需要二次确认

Author: kiwifruit
License: GPL-3.0
"""

from .intent_safety_manager import (
    IntentSafetyManager,
    OperationType,
    PermissionLevel,
    OperationResult,
    AuditLog,
    OperationRisk,
)
from .intent_safety_manager import create_intent_safety_manager

__all__ = [
    'IntentSafetyManager',
    'OperationType',
    'PermissionLevel',
    'OperationResult',
    'AuditLog',
    'OperationRisk',
    'create_intent_safety_manager',
]
