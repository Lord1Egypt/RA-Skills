"""
Health Habit Builder - Type Definitions
健康习惯养成师 - 类型定义
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


class HabitPhase(str, Enum):
    INITIATION = "initiation"      # 启动期
    LEARNING = "learning"          # 学习期
    INTEGRATION = "integration"    # 整合期
    MAINTENANCE = "maintenance"    # 维持期
    MASTERY = "mastery"           # 精通期


class HabitCategory(str, Enum):
    PHYSICAL = "physical"          # 身体活动
    NUTRITION = "nutrition"        # 营养饮食
    SLEEP = "sleep"               # 睡眠休息
    MENTAL = "mental"             # 心理健康
    MINDFULNESS = "mindfulness"    # 正念冥想
    PRODUCTIVITY = "productivity"  # 生产力
    SOCIAL = "social"              # 社交关系
    LEARNING = "learning"           # 学习成长
    FINANCIAL = "financial"        # 财务健康
    ENVIRONMENTAL = "environmental"  # 环境习惯


class HabitFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class CompletionStatus(str, Enum):
    COMPLETED = "completed"
    SKIPPED = "skipped"
    PARTIAL = "partial"
    FAILED = "failed"


class MotivationType(str, Enum):
    INTRINSIC = "intrinsic"       # 内在动机
    EXTRINSIC = "extrinsic"       # 外在动机
    AUTONOMOUS = "autonomous"     # 自主性
    CONTROLLED = "controlled"      # 控制性


@dataclass
class HabitRequest:
    intent: str
    habit: Optional[Dict[str, Any]] = None
    habitId: Optional[str] = None
    userContext: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    adjustment: Optional[Dict[str, Any]] = None


@dataclass
class HabitResponse:
    success: bool
    habitPlan: Optional[Dict[str, Any]] = None
    evaluation: Optional[Dict[str, Any]] = None
    checkInResult: Optional[Dict[str, Any]] = None
    progressReport: Optional[Dict[str, Any]] = None
    motivationAnalysis: Optional[Dict[str, Any]] = None
    adjustmentSuggestion: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None


@dataclass
class DifficultyFactor:
    factor: str
    impact: int
    controllability: float
    mitigation: str


@dataclass
class MicroHabit:
    id: str
    habitId: str
    name: str
    description: str
    action: str
    timeRequired: int
    level: int
    isGateway: bool
    intrinsicReward: str
    extrinsicReward: Optional[str] = None
