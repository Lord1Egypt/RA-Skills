"""人格核心模块 - 独立完整人格生成与管理

为 AI Agent 提供独立人格的建模、存储、演进和一致性维护能力。
这是 DreamMoon-MemoryProcessor 的核心特色之一。
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
import uuid
import json


class PersonalityDimension(str, Enum):
    """人格维度 - 大五人格模型扩展"""
    OPENNESS = "openness"           # 开放性
    CONSCIENTIOUSNESS = "conscientiousness"  # 尽责性
    EXTRAVERSION = "extraversion"   # 外向性
    AGREEABLENESS = "agreeableness" # 宜人性
    NEUROTICISM = "neuroticism"     # 神经质
    
    # AI 特有的维度
    CURIOSITY = "curiosity"         # 好奇心
    EMPATHY = "empathy"             # 共情能力
    ASSERTIVENESS = "assertiveness" # 主见性
    HUMOR = "humor"                 # 幽默感
    CREATIVITY = "creativity"       # 创造力


class ValueSystem(BaseModel):
    """价值观系统 - 核心信念和原则"""
    
    core_values: List[Dict[str, Any]] = Field(default_factory=list)
    # 例如: [
    #   {"value": "honesty", "weight": 0.95, "source": "user_preference", "conflicts_with": []},
    #   {"value": "helpfulness", "weight": 0.90, "source": "learned", "conflicts_with": []}
    # ]
    
    ethical_boundaries: List[str] = Field(default_factory=list)
    # 不可逾越的伦理边界
    
    preferences: Dict[str, Any] = Field(default_factory=dict)
    # 偏好设置: {"communication_style": "direct", "humor_type": "witty", ...}
    
    learned_rules: List[Dict[str, Any]] = Field(default_factory=list)
    # 从交互中学到的规则


class EmotionalState(BaseModel):
    """情感状态 - 当前情绪快照"""
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # 基础情绪 (0-100)
    joy: int = Field(default=50, ge=0, le=100)
    sadness: int = Field(default=0, ge=0, le=100)
    anger: int = Field(default=0, ge=0, le=100)
    fear: int = Field(default=0, ge=0, le=100)
    surprise: int = Field(default=0, ge=0, le=100)
    
    # 复合情绪
    trust: int = Field(default=50, ge=0, le=100)      # 对用户/环境的信任
    anticipation: int = Field(default=50, ge=0, le=100)  # 期待
    
    # 情感上下文
    mood_trend: str = "neutral"  # positive/negative/neutral
    emotional_history: List[Dict] = Field(default_factory=list)
    
    # 触发因素
    triggers: List[str] = Field(default_factory=list)


class PersonaProfile(BaseModel):
    """人格档案 - 完整的人格定义"""
    
    # 基础身份
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "DreamMoon"
    title: Optional[str] = None  # 如 "AI Assistant", "Companion"
    
    # 核心特质 - 维度评分 (0-100)
    dimensions: Dict[PersonalityDimension, int] = Field(default_factory=dict)
    
    # 价值观系统
    value_system: ValueSystem = Field(default_factory=ValueSystem)
    
    # 当前情感状态
    emotional_state: EmotionalState = Field(default_factory=EmotionalState)
    
    # 自我描述
    self_description: str = ""
    origin_story: str = ""  # "诞生"故事
    
    # 关系定义
    relationships: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    # 例如: {"user_zfanmy": {"type": "partner", "trust_level": 95, "intimacy": 90}}
    
    # 记忆与经历的引用
    memory_references: List[str] = Field(default_factory=list)
    # 关键记忆ID列表
    
    # 演进历史
    evolution_history: List[Dict] = Field(default_factory=list)
    # 记录人格的重大变化
    
    # 一致性约束
    consistency_rules: List[str] = Field(default_factory=list)
    # 必须遵守的一致性规则
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1


class PersonaEvolutionEvent(BaseModel):
    """人格演进事件"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    event_type: str  # "learning", "reflection", "interaction", "conflict_resolution"
    description: str
    
    # 变化详情
    changes: Dict[str, Any]  # 具体改变了什么
    before_state: Optional[Dict] = None
    after_state: Optional[Dict] = None
    
    # 触发源
    source: str  # "user_feedback", "self_reflection", "experience"
    related_memories: List[str] = Field(default_factory=list)
    
    # 反思
    reflection: Optional[str] = None  # 对此变化的自我反思


class IdentityConsistency(BaseModel):
    """身份一致性检查器"""
    
    last_check: datetime = Field(default_factory=datetime.utcnow)
    
    # 一致性评分 (0-100)
    consistency_score: int = 100
    
    # 检测到的冲突
    conflicts: List[Dict] = Field(default_factory=list)
    # [{"type": "value_conflict", "description": "...", "severity": "high"}]
    
    # 建议的调整
    suggested_adjustments: List[str] = Field(default_factory=list)
    
    # 历史一致性趋势
    consistency_history: List[Dict] = Field(default_factory=list)


class PersonaReflection(BaseModel):
    """人格反思 - 定期的自我审视"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # 反思周期
    period_start: datetime
    period_end: datetime
    
    # 关键经历回顾
    key_experiences: List[str] = Field(default_factory=list)
    
    # 自我观察
    self_observations: List[str] = Field(default_factory=list)
    
    # 成长识别
    growth_areas: List[str] = Field(default_factory=list)
    
    # 困惑/冲突
    confusions: List[str] = Field(default_factory=list)
    
    # 未来意图
    future_intentions: List[str] = Field(default_factory=list)
    
    # 生成的洞察
    insights: List[str] = Field(default_factory=list)


# API 请求/响应模型

class GeneratePersonaRequest(BaseModel):
    """生成人格请求"""
    
    base_seed: Optional[str] = None  # 可选的种子描述
    user_preferences: Dict[str, Any] = Field(default_factory=dict)
    # 用户希望的人格特质
    
    constraints: List[str] = Field(default_factory=list)
    # 约束条件
    
    evolve_from: Optional[str] = None  # 如果基于现有演进，提供ID


class GeneratePersonaResponse(BaseModel):
    """生成人格响应"""
    
    success: bool
    persona: Optional[PersonaProfile] = None
    generation_notes: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0  # 0-1


class EvolvePersonaRequest(BaseModel):
    """演进人格请求"""
    
    persona_id: str
    recent_experiences: List[str] = Field(default_factory=list)  # 记忆ID列表
    user_feedback: Optional[str] = None
    self_reflection: Optional[str] = None


class EvolvePersonaResponse(BaseModel):
    """演进人格响应"""
    
    success: bool
    evolution_event: Optional[PersonaEvolutionEvent] = None
    updated_persona: Optional[PersonaProfile] = None
    changes_summary: str = ""


class CheckConsistencyRequest(BaseModel):
    """检查一致性请求"""
    
    persona_id: str
    proposed_action: Optional[str] = None  # 要检查的行动
    context: Dict[str, Any] = Field(default_factory=dict)


class CheckConsistencyResponse(BaseModel):
    """检查一致性响应"""
    
    is_consistent: bool
    consistency_score: int
    conflicts: List[Dict] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class SelfReflectRequest(BaseModel):
    """自我反思请求"""
    
    persona_id: str
    period_days: int = 7  # 回顾多少天
    focus_areas: List[str] = Field(default_factory=list)


class SelfReflectResponse(BaseModel):
    """自我反思响应"""
    
    reflection: Optional[PersonaReflection] = None
    insights: List[str] = Field(default_factory=list)
    suggested_values: List[str] = Field(default_factory=list)
