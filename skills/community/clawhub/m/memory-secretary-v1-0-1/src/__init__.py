"""
记忆秘书 (Memory Secretary)
智能记忆管理与优化助手

版本：1.0.0
作者：隐客
描述: 基于规则的智能记忆管理系统，提供主动记忆管理、智能提醒、模式识别等功能
"""

__version__ = '1.0.0'
__author__ = '隐客'
__description__ = '智能记忆管理与优化助手'

# 核心模块
from .memory_secretary_lite import MemorySecretaryLite
from .smart_adaptive import SmartAdaptiveMem0
from .daily_check import DailyMemoryCheck
from .pilot_check import PilotCheckStage3

__all__ = [
    'MemorySecretaryLite',
    'SmartAdaptiveMem0',
    'DailyMemoryCheck',
    'PilotCheckStage3',
]
