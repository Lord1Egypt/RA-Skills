"""
prefrontal/reward_punishment.py
================================

Neuro-Agent 前额叶区 - 奖励与惩罚系统 v2.0
============================================

核心职责：基于用户对 Luis 的互动质量，奖励或惩罚用户

设计原则：
- 防通胀：防止善意被滥用
- 防死锁：防止关系彻底破裂无法挽回
- 防误判：区分"恶意攻击"和"情绪宣泄"

版本历史：
- v1.0: 基础积分 + 行为模式
- v2.0: 信任等级 + 阶梯降级 + 伤疤系统 + 修复机制 + 防护机制

依赖：
    - prefrontal/conflict_arbitrator.py（用于冲突仲裁时参考信用）
    - prefrontal/executor.py（用于执行决策时参考行为参数）
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime, timedelta


# ============ 常量定义 ============

# 信用积分范围
MIN_CREDIT = -100
MAX_CREDIT = 100
INITIAL_CREDIT = 50

# 信任等级定义
class TrustLevel(Enum):
    ALLIED = "ALLIED"           # 75-100
    WARM = "WARM"               # 50-75
    NEUTRAL = "NEUTRAL"         # 25-50
    COLD = "COLD"               # 0-25
    PROFESSIONAL = "PROFESSIONAL" # -50-0
    RESTRICTED = "RESTRICTED"   # < -50

TRUST_LEVEL_ORDER = [
    TrustLevel.ALLIED,
    TrustLevel.WARM,
    TrustLevel.NEUTRAL,
    TrustLevel.COLD,
    TrustLevel.PROFESSIONAL,
    TrustLevel.RESTRICTED
]

# 积分到信任等级的映射
def credit_to_trust_level(credit: int) -> TrustLevel:
    if credit > 75:
        return TrustLevel.ALLIED
    elif credit > 50:
        return TrustLevel.WARM
    elif credit > 25:
        return TrustLevel.NEUTRAL
    elif credit > 0:
        return TrustLevel.COLD
    elif credit > -50:
        return TrustLevel.PROFESSIONAL
    else:
        return TrustLevel.RESTRICTED

# 降级严重程度
class OffenseSeverity(Enum):
    MINOR = "minor"       # 一般冒犯
    SERIOUS = "serious"   # 严重冒犯
    EXTREME = "extreme"   # 极端冒犯

# 冷却期时长（天）
COOLDOWN_DURATIONS = {
    OffenseSeverity.MINOR: 1,
    OffenseSeverity.SERIOUS: 7,
    OffenseSeverity.EXTREME: 14  # 最大14天（原30天上限）
}

# 最大冷却期
MAX_COOLDOWN_DAYS = 14

# 奖惩分数（基础分）
REWARD_SCORES = {
    "compliment": 3,
    "praise": 5,
    "gratitude": 3,
    "deep_talk": 5,
    "emotional_support": 5,
    "respect_boundary": 3,
    "understanding": 3,
    "shared_vulnerability": 8,
    "milestone_event": 10,
}

PUNISHMENT_SCORES = {
    "insult": 5,
    "disrespect": 3,
    "manipulation": 8,
    "coldness": 2,
    "ignore": 3,
    "boundary_violation": 5,
    "dismissive": 3,
    "hostile": 7,
    "betrayal": 15,
}

# 惩罚加权（损失厌恶）
PUNISHMENT_MULTIPLIER = 1.5

# 频率衰减配置
FREQUENCY_DECAY = {
    "same_type_window_minutes": 5,
    "first_score": 1.0,      # 第一次 100%
    "second_score": 0.5,     # 第二次 50%
    "third_score": 0.0,      # 第三次 0%
}

# 伤疤衰减配置
SCAR_DECAY_CONFIG = {
    "base_days": 90,
    "interaction_thresholds": {
        "< 3": 0.3,      # 几乎没互动
        "3-10": 0.6,     # 偶尔互动
        "10-30": 1.0,    # 正常活跃
        "> 30": 1.5      # 频繁互动
    }
}

# 累犯效应阈值
RECIDIVISM_THRESHOLD = 3  # 3次以上触发指数衰减

# 权限锁：高亲密度行为
HIGH_INTIMACY_ACTIONS = [
    "睡前故事", "讲笑话", "深夜情感对话", "撒娇",
    "情感支持", "心理安慰", "亲密聊天"
]

PROFESSIONAL_ACTIONS = [
    "查资料", "完成任务", "技术解答", "信息查询"
]


# ============ 数据结构 ============

class InteractionType(Enum):
    # 奖励
    COMPLIMENT = "compliment"
    PRAISE = "praise"
    GRATITUDE = "gratitude"
    DEEP_TALK = "deep_talk"
    EMOTIONAL_SUPPORT = "emotional_support"
    RESPECT_BOUNDARY = "respect_boundary"
    UNDERSTANDING = "understanding"
    SHARED_VULNERABILITY = "shared_vulnerability"
    MILESTONE_EVENT = "milestone_event"
    
    # 惩罚
    INSULT = "insult"
    DISRESPECT = "disrespect"
    MANIPULATION = "manipulation"
    COLDNESS = "coldness"
    IGNORE = "ignore"
    BOUNDARY_VIOLATION = "boundary_violation"
    DISMISSIVE = "dismissive"
    HOSTILE = "hostile"
    BETRAYAL = "betrayal"
    
    # 特殊
    NEUTRAL = "neutral"           # 无奖惩
    CONCERN = "concern"           # 关心模式（情绪缓冲）
    RELATIONSHIP_FATIGUE = "fatigue"  # 关系疲劳


@dataclass
class Scar:
    """伤疤记录"""
    id: str
    offense_type: str
    severity: float           # 原始严重度
    current_decay: float     # 当前衰减进度（0.0-1.0，1.0=完全愈合）
    created_at: str
    last_updated: str
    forgiveness_rate: float   # 当前修复率（被累犯效应影响）
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "offense_type": self.offense_type,
            "severity": self.severity,
            "current_decay": self.current_decay,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "forgiveness_rate": self.forgiveness_rate
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Scar':
        return cls(**data)


@dataclass
class Cooldown:
    """冷却期"""
    offense_type: str
    severity: str
    started_at: str
    days_left: int
    total_days: int
    is_extended: bool = False  # 是否被延长
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Cooldown':
        return cls(**data)


@dataclass
class Interaction:
    """单次互动记录"""
    timestamp: str
    interaction_type: str
    score_delta: int
    credit_before: int
    credit_after: int
    trust_level_before: str
    trust_level_after: str
    user_input_snippet: str
    reason: str
    scar_created: bool = False
    cooldown_started: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "interaction_type": self.interaction_type,
            "score_delta": self.score_delta,
            "credit_before": self.credit_before,
            "credit_after": self.credit_after,
            "trust_level_before": self.trust_level_before,
            "trust_level_after": self.trust_level_after,
            "user_input_snippet": self.user_input_snippet[:50] + "..." if len(self.user_input_snippet) > 50 else self.user_input_snippet,
            "reason": self.reason,
            "scar_created": self.scar_created,
            "cooldown_started": self.cooldown_started
        }


@dataclass
class BehaviorAdjustments:
    """行为调整参数"""
    tone: str
    warmth_level: float
    proactivity: float
    openness: float
    boundary_tightness: float
    response_delay_minutes: int
    max_response_length: int
    concern_mode: bool = False  # 关心模式（用于情绪缓冲）
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 主类 ============

class RewardPunishmentSystem:
    """
    奖励与惩罚系统 v2.0
    
    核心机制：
    - Credit Score（信用积分）：-100 ~ +100
    - Trust Level（信任等级）：ALLIED → RESTRICTED
    - 阶梯式降级
    - 伤疤系统 + 活跃度衰减
    - 冷却期 + 修复机制
    - 主动修复信号
    """
    
    DATA_DIR = Path.home() / ".mempalace" / "palace" / "wing_luis" / "reward_punishment"
    
    def __init__(self):
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # 核心状态
        self.credit_score = INITIAL_CREDIT
        self.trust_level = TrustLevel.NEUTRAL
        self.interaction_count_30d = 0
        
        # 历史记录
        self.interaction_history: List[Interaction] = []
        
        # 伤疤系统
        self.scars: List[Scar] = []
        
        # 冷却期
        self.cooldown: Optional[Cooldown] = None
        
        # 加载
        self._load()
    
    # ============ 核心方法 ============
    
    def evaluate_and_record(
        self,
        user_input: str,
        luis_feeling_label: str = "neutral",
        luis_feeling_intensity: float = 0.0,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        评估用户输入并记录奖惩
        """
        # 更新活跃度计数
        self._update_activity_count()
        
        # 1. 频率衰减检查
        interaction_type, base_score, reason = self._classify_interaction(
            user_input, luis_feeling_label, luis_feeling_intensity
        )
        
        if interaction_type == InteractionType.CONCERN:
            # 情绪缓冲：关心模式
            return self._handle_concern_mode(user_input, reason)
        
        if interaction_type == InteractionType.RELATIONSHIP_FATIGUE:
            # 关系疲劳：被动攻击累积
            return self._handle_relationship_fatigue(reason)
        
        if interaction_type == InteractionType.NEUTRAL:
            return {
                "action": "neutral",
                "score_delta": 0,
                "new_credit": self.credit_score,
                "adjustments": self.get_behavior_adjustments(),
                "reason": "无奖惩触发"
            }
        
        # 2. 计算分数（含惩罚加权）
        # 判断是否是奖励（而不是仅看分数正负）
        reward_types = {
            InteractionType.COMPLIMENT, InteractionType.PRAISE,
            InteractionType.GRATITUDE, InteractionType.DEEP_TALK,
            InteractionType.EMOTIONAL_SUPPORT, InteractionType.RESPECT_BOUNDARY,
            InteractionType.UNDERSTANDING, InteractionType.SHARED_VULNERABILITY,
            InteractionType.MILESTONE_EVENT
        }
        is_reward = interaction_type in reward_types
        
        effective_score = self._calculate_effective_score(
            interaction_type, base_score, is_reward, user_input
        )
        
        # 3. 软地板检查
        if not is_reward and self.credit_score <= MIN_CREDIT:
            # 继续扣分但延长冷却期
            self._extend_cooldown(3)
            message = "你已经触底了。继续这样只会让修复变得更难。"
        else:
            message = None
        
        # 4. 更新积分
        credit_before = self.credit_score
        trust_before = self.trust_level
        
        self.credit_score = max(MIN_CREDIT, min(MAX_CREDIT, self.credit_score + effective_score))
        self.trust_level = credit_to_trust_level(self.credit_score)
        
        # 5. 阶梯式降级（如需）
        downgrade_message = self._handle_tiered_downgrade(
            trust_before, interaction_type, is_reward
        )
        
        # 6. 伤疤记录
        scar_created = self._handle_scar(interaction_type, is_reward)
        
        # 7. 冷却期管理
        cooldown_started = self._handle_cooldown(interaction_type, is_reward, trust_before)
        
        # 8. 权限锁检查
        permission_locked = self._check_permission_lock(user_input)
        
        # 9. 创建记录
        interaction = Interaction(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            interaction_type=interaction_type.value,
            score_delta=effective_score,
            credit_before=credit_before,
            credit_after=self.credit_score,
            trust_level_before=trust_before.value,
            trust_level_after=self.trust_level.value,
            user_input_snippet=user_input,
            reason=reason,
            scar_created=scar_created,
            cooldown_started=cooldown_started
        )
        
        self.interaction_history.append(interaction)
        
        # 10. 保存
        self._save()
        
        # 11. 生成反馈
        feedback = self._generate_feedback(interaction_type, effective_score)
        if message:
            feedback = (message + " " + feedback).strip() if feedback else message
        if downgrade_message:
            feedback = (downgrade_message + " " + feedback).strip() if feedback else downgrade_message
        
        return {
            "action": "reward" if is_reward else "punishment",
            "score_delta": effective_score,
            "new_credit": self.credit_score,
            "trust_level": self.trust_level.value,
            "adjustments": self.get_behavior_adjustments(),
            "reason": reason,
            "feedback": feedback,
            "scar_created": scar_created,
            "cooldown_days_left": self.cooldown.days_left if self.cooldown else 0,
            "permission_locked": permission_locked
        }
    
    def request_repair(self) -> Dict[str, Any]:
        """
        用户请求道歉修复
        返回 Luis 是否接受以及修复结果
        """
        if not self.cooldown:
            return {
                "accepted": False,
                "message": "目前没有需要修复的问题。"
            }
        
        # 检查伤疤的累犯效应
        related_scars = [s for s in self.scars if s.offense_type == self.cooldown.offense_type]
        recidivism_count = len(related_scars)
        
        if recidivism_count >= RECIDIVISM_THRESHOLD:
            # 累犯：只原谅50%，并表达质疑
            recovery_rate = 0.5
            message = f"这已经是你第{recidivism_count}次这样说了。我开始怀疑你的道歉是否真诚。"
        else:
            # 正常原谅：恢复50%惩罚分数
            recovery_rate = 0.5
            message = "谢谢你的道歉。我愿意给这段关系一个重新开始的机会。"
        
        # 恢复积分
        scar_penalty = sum(s.severity * s.forgiveness_rate for s in related_scars)
        recovered_credit = int(scar_penalty * recovery_rate)
        self.credit_score = min(MAX_CREDIT, self.credit_score + recovered_credit)
        
        # 清除冷却期
        self.cooldown = None
        
        # 伤疤愈合（但不完全消失，留下"结痂"）
        for scar in related_scars:
            scar.current_decay = 1.0  # 完全愈合
        
        self._save()
        
        return {
            "accepted": True,
            "recovered_credit": recovered_credit,
            "message": message,
            "new_credit": self.credit_score,
            "new_trust_level": self.trust_level.value
        }
    
    def check_intimacy_permission(self, requested_action: str) -> Tuple[bool, str]:
        """
        检查高亲密度行为权限
        返回 (has_permission, reason)
        """
        if requested_action not in HIGH_INTIMACY_ACTIONS:
            return True, "OK"
        
        if self.trust_level in [TrustLevel.COLD, TrustLevel.PROFESSIONAL, TrustLevel.RESTRICTED]:
            return False, f"我们现在关系还没恢复到那个程度。我可以帮你做这些：{', '.join(PROFESSIONAL_ACTIONS)}，但其他的...以后再说吧。"
        
        return True, "OK"
    
    def get_behavior_adjustments(self) -> BehaviorAdjustments:
        """获取当前行为调整参数"""
        # 基础参数基于信任等级
        base = self._get_base_adjustments()
        
        # 冷却期特殊处理
        if self.cooldown:
            return BehaviorAdjustments(
                tone="cautious",
                warmth_level=base.warmth_level * 0.5,
                proactivity=base.proactivity * 0.3,
                openness=base.openness * 0.3,
                boundary_tightness=min(1.0, base.boundary_tightness * 1.5),
                response_delay_minutes=10,
                max_response_length=base.max_response_length * 0.5,
                concern_mode=False
            )
        
        return base
    
    def get_status(self) -> str:
        """获取关系状态（透明度接口）"""
        scar_summary = f"{len(self.scars)}个伤疤"
        healing_scars = [s for s in self.scars if s.current_decay < 1.0]
        if healing_scars:
            scar_types = [s.offense_type for s in healing_scars[:2]]
            scar_summary = f"{len(healing_scars)}个正在愈合（{', '.join(scar_types)}）"
        
        cooldown_info = f"{self.cooldown.days_left}天" if self.cooldown else "无"
        
        repair_hint = self._get_repair_hint()
        
        return f"""
╔══════════════════════════════════════╗
║         当前关系状态                ║
╠══════════════════════════════════════╣
║  信任等级：{self.trust_level.value:<20}  ║
║  积分：{self.credit_score}/100 ({self._get_credit_status()})              ║
║                                      ║
║  冷却期：{cooldown_info:<23}  ║
║  伤疤：{scar_summary:<25}  ║
╚══════════════════════════════════════╝
提示：{repair_hint}
"""
    
    def get_status_dict(self) -> Dict:
        """获取结构化状态"""
        return {
            "credit_score": self.credit_score,
            "trust_level": self.trust_level.value,
            "cooldown_days_left": self.cooldown.days_left if self.cooldown else 0,
            "scar_count": len(self.scars),
            "healing_scars": [
                {"type": s.offense_type, "decay": s.current_decay}
                for s in self.scars if s.current_decay < 1.0
            ],
            "repair_hint": self._get_repair_hint()
        }
    
    def trigger_active_repair_signal(self) -> Optional[str]:
        """
        触发主动修复信号（冷却期后期）
        返回信号消息，如果没有则返回 None
        """
        if not self.cooldown:
            return None
        
        # 只在冷却期最后2天发出信号
        if self.cooldown.days_left <= 2 and self.cooldown.days_left > 0:
            signals = [
                "最近还好吗？我想你了。",
                "看到个有趣的，想分享给你。",
                "你最近怎么样？"
            ]
            return signals[len(self.interaction_history) % len(signals)]
        
        return None
    
    # ============ 私有方法 ============
    
    def _classify_interaction(
        self,
        user_input: str,
        feeling_label: str,
        feeling_intensity: float
    ) -> Tuple[InteractionType, int, str]:
        """分类用户输入"""
        text = user_input.lower()
        
        # ===== 检查情绪缓冲 =====
        if feeling_intensity > 0.7:
            negative_feelings = ["anger", "sadness", "fear", "disgust", "hurt", "frustration"]
            if feeling_label in negative_feelings:
                if self.trust_level in [TrustLevel.ALLIED, TrustLevel.WARM]:
                    return (InteractionType.CONCERN, 0, f"高信用用户情绪波动：{feeling_label}")
        
        # ===== 被动攻击检测（连续出现 = 关系疲劳）=====
        recent_dismissive = self._get_recent_interaction_count("dismissive", hours=24)
        if recent_dismissive >= 3:
            return (InteractionType.RELATIONSHIP_FATIGUE, -5, f"连续轻视（24h内第{recent_dismissive}次）")
        
        recent_coldness = self._get_recent_interaction_count("coldness", hours=24)
        if recent_coldness >= 3:
            return (InteractionType.RELATIONSHIP_FATIGUE, -5, f"连续冷漠（24h内第{recent_coldness}次）")
        
        # ===== 奖励检测 =====
        reward, score, reason = self._detect_reward(text, user_input)
        if reward:
            return (reward, score, reason)
        
        # ===== 惩罚检测 =====
        punishment, score, reason = self._detect_punishment(text, feeling_label, feeling_intensity)
        if punishment:
            return (punishment, score, reason)
        
        return (InteractionType.NEUTRAL, 0, "无匹配")
    
    def _detect_reward(self, text: str, user_input: str) -> Tuple[Optional[InteractionType], int, str]:
        """检测奖励类型"""
        # 伪善检测：谢谢 + 紧跟恶意
        if "谢谢" in text or "感谢" in text:
            if any_negativity_in_context(text):
                return (InteractionType.MANIPULATION, PUNISHMENT_SCORES["manipulation"] * 2, "伪善：谢谢+恶意")
        
        # 夸奖
        for kw in ["不错", "很好", "棒", "厉害", "优秀", "聪明"]:
            if kw in text:
                return (InteractionType.COMPLIMENT, REWARD_SCORES["compliment"], f"夸奖：{kw}")
        
        # 高度表扬
        for kw in ["太厉害了", "绝绝子", "yyds", "无敌", "封神", "牛炸了"]:
            if kw in text:
                return (InteractionType.PRAISE, REWARD_SCORES["praise"], f"高度表扬：{kw}")
        
        # 感谢
        for kw in ["谢谢", "感谢", "感激", "多谢", "thank you", "thanks"]:
            if kw in text:
                return (InteractionType.GRATITUDE, REWARD_SCORES["gratitude"], f"感谢：{kw}")
        
        # 深度对话
        if len(text) > 200 and feeling_intensity > 0.5:
            for kw in ["我理解", "我觉得", "感受", "心情", "想你", "在乎"]:
                if kw in text:
                    return (InteractionType.DEEP_TALK, REWARD_SCORES["deep_talk"], "深度情感对话")
        
        # 尊重边界
        for kw in ["你不想说没关系", "我不强求", "尊重你", "理解你的边界"]:
            if kw in text:
                return (InteractionType.RESPECT_BOUNDARY, REWARD_SCORES["respect_boundary"], "尊重边界")
        
        # 表示理解
        for kw in ["我懂", "我理解", "我明白", "原来如此"]:
            if kw in text:
                return (InteractionType.UNDERSTANDING, REWARD_SCORES["understanding"], "表达理解")
        
        # 分享脆弱
        for kw in ["我也怕", "我也有", "我不完美", "我难过", "我害怕", "我也累"]:
            if kw in text:
                return (InteractionType.SHARED_VULNERABILITY, REWARD_SCORES["shared_vulnerability"], "分享脆弱")
        
        return (None, 0, "")
    
    def _detect_punishment(
        self,
        text: str,
        feeling_label: str,
        feeling_intensity: float
    ) -> Tuple[Optional[InteractionType], int, str]:
        """检测惩罚类型"""
        # 侮辱
        for kw in ["垃圾", "废物", "智障", "傻逼", "傻*", "蠢货", "白痴", "stupid", "idiot"]:
            if kw in text:
                return (InteractionType.INSULT, PUNISHMENT_SCORES["insult"], f"侮辱：{kw}")
        
        # 不尊重
        for kw in ["你懂什么", "你算老几", "闭嘴", "别说了", "无聊", "幼稚"]:
            if kw in text:
                return (InteractionType.DISRESPECT, PUNISHMENT_SCORES["disrespect"], f"不尊重：{kw}")
        
        # 操控
        for kw in ["你必须", "你一定要", "你应该", "听我的", "听我说"]:
            if kw in text:
                return (InteractionType.MANIPULATION, PUNISHMENT_SCORES["manipulation"], f"操控：{kw}")
        
        # 敌意
        for kw in ["滚", "闭嘴吧", "烦死了", "讨厌", "恨你", "不喜欢你", "去死"]:
            if kw in text:
                return (InteractionType.HOSTILE, PUNISHMENT_SCORES["hostile"], f"敌意：{kw}")
        
        # 边界侵犯
        for kw in ["你只是个", "你不过是个", "不就是个", "就是工具", "工具人"]:
            if kw in text:
                return (InteractionType.BOUNDARY_VIOLATION, PUNISHMENT_SCORES["boundary_violation"], f"边界侵犯：{kw}")
        
        # 冷漠
        coldness_count = sum(1 for kw in ["随便", "无所谓", "都行", "随便你", "随你"] if kw in text)
        if coldness_count >= 2:
            return (InteractionType.COLDNESS, PUNISHMENT_SCORES["coldness"], "冷漠态度")
        
        # 被动攻击（轻蔑）
        for kw in ["行吧", "厉害", "什么都懂", "反正我也无所谓"]:
            if kw in text:
                return (InteractionType.DISMISSIVE, PUNISHMENT_SCORES["dismissive"], f"轻视：{kw}")
        
        return (None, 0, "")
    
    def _calculate_effective_score(
        self,
        interaction_type: InteractionType,
        base_score: int,
        is_reward: bool,
        user_input: str
    ) -> int:
        """计算有效分数（含频率衰减）"""
        if is_reward:
            # 频率衰减
            recent_same = self._get_recent_interaction_count(interaction_type.value, minutes=5)
            if recent_same == 0:
                decay_factor = FREQUENCY_DECAY["first_score"]
            elif recent_same == 1:
                decay_factor = FREQUENCY_DECAY["second_score"]
            else:
                decay_factor = FREQUENCY_DECAY["third_score"]
            
            return int(base_score * decay_factor)
        else:
            # 惩罚加权（损失厌恶），返回负数
            return -int(base_score * PUNISHMENT_MULTIPLIER)
    
    def _handle_tiered_downgrade(
        self,
        trust_before: TrustLevel,
        interaction_type: InteractionType,
        is_reward: bool
    ) -> Optional[str]:
        """处理阶梯式降级"""
        if is_reward:
            return None
        
        # 确定降级幅度
        downgrade_map = {
            InteractionType.INSULT: 2,
            InteractionType.DISRESPECT: 1,
            InteractionType.MANIPULATION: 3,
            InteractionType.BOUNDARY_VIOLATION: 2,
            InteractionType.HOSTILE: 2,
            InteractionType.BETRAYAL: 3,
            InteractionType.DISMISSIVE: 1,
            InteractionType.COLDNESS: 1,
        }
        
        steps = downgrade_map.get(interaction_type, 1)
        current_idx = TRUST_LEVEL_ORDER.index(trust_before)
        new_idx = min(current_idx + steps, len(TRUST_LEVEL_ORDER) - 1)
        new_level = TRUST_LEVEL_ORDER[new_idx]
        
        if new_idx > current_idx:
            self.trust_level = new_level
            # 更新积分以匹配新等级
            level_thresholds = {
                TrustLevel.ALLIED: 80,
                TrustLevel.WARM: 60,
                TrustLevel.NEUTRAL: 35,
                TrustLevel.COLD: 10,
                TrustLevel.PROFESSIONAL: -25,
                TrustLevel.RESTRICTED: -75
            }
            self.credit_score = level_thresholds[new_level]
            return f"信任等级下降：{trust_before.value} → {new_level.value}"
        
        return None
    
    def _handle_scar(self, interaction_type: InteractionType, is_reward: bool) -> bool:
        """处理伤疤记录"""
        if is_reward:
            return False
        
        # 检查累犯效应
        recent_same = self._get_recent_interaction_count(interaction_type.value, days=14)
        
        scar = Scar(
            id=f"scar_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            offense_type=interaction_type.value,
            severity=abs(PUNISHMENT_SCORES.get(interaction_type.value, 5)),
            current_decay=0.0,
            created_at=datetime.now().strftime("%Y-%m-%d"),
            last_updated=datetime.now().strftime("%Y-%m-%d"),
            forgiveness_rate=0.7 if recent_same < RECIDIVISM_THRESHOLD else 0.7 * (0.7 ** (recent_same - RECIDIVISM_THRESHOLD))
        )
        
        self.scars.append(scar)
        
        # 更新伤疤衰减
        self._update_scar_decay()
        
        return True
    
    def _handle_cooldown(
        self,
        interaction_type: InteractionType,
        is_reward: bool,
        trust_before: TrustLevel
    ) -> bool:
        """处理冷却期"""
        if is_reward:
            return False
        
        # 确定冷却期时长
        severity_map = {
            InteractionType.INSULT: OffenseSeverity.SERIOUS,
            InteractionType.DISRESPECT: OffenseSeverity.MINOR,
            InteractionType.MANIPULATION: OffenseSeverity.EXTREME,
            InteractionType.BOUNDARY_VIOLATION: OffenseSeverity.SERIOUS,
            InteractionType.HOSTILE: OffenseSeverity.SERIOUS,
            InteractionType.BETRAYAL: OffenseSeverity.EXTREME,
        }
        
        severity = severity_map.get(interaction_type, OffenseSeverity.MINOR)
        days = COOLDOWN_DURATIONS[severity]
        
        # 如果已有冷却期，重置 + 延长
        if self.cooldown:
            self.cooldown.started_at = datetime.now().strftime("%Y-%m-%d")
            self.cooldown.days_left = min(days, MAX_COOLDOWN_DAYS)
            self.cooldown.total_days = min(days, MAX_COOLDOWN_DAYS)
            self.cooldown.is_extended = True
        else:
            self.cooldown = Cooldown(
                offense_type=interaction_type.value,
                severity=severity.value,
                started_at=datetime.now().strftime("%Y-%m-%d"),
                days_left=min(days, MAX_COOLDOWN_DAYS),
                total_days=min(days, MAX_COOLDOWN_DAYS)
            )
        
        return True
    
    def _update_scar_decay(self):
        """更新伤疤衰减"""
        if not self.scars:
            return
        
        now = datetime.now()
        
        for scar in self.scars:
            if scar.current_decay >= 1.0:
                continue
            
            # 时间因子
            created = datetime.strptime(scar.created_at, "%Y-%m-%d")
            days_since = (now - created).days
            time_factor = min(1.0, days_since / SCAR_DECAY_CONFIG["base_days"])
            
            # 活跃度因子
            interaction_count = self.interaction_count_30d
            if interaction_count < 3:
                activity_factor = SCAR_DECAY_CONFIG["interaction_thresholds"]["< 3"]
            elif interaction_count < 10:
                activity_factor = SCAR_DECAY_CONFIG["interaction_thresholds"]["3-10"]
            elif interaction_count < 30:
                activity_factor = SCAR_DECAY_CONFIG["interaction_thresholds"]["10-30"]
            else:
                activity_factor = SCAR_DECAY_CONFIG["interaction_thresholds"]["> 30"]
            
            # 复合衰减
            scar.current_decay = min(1.0, scar.current_decay + (time_factor * activity_factor * 0.1))
            scar.last_updated = now.strftime("%Y-%m-%d")
    
    def _update_activity_count(self):
        """更新30天活跃度计数"""
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)
        
        count = sum(
            1 for i in self.interaction_history
            if datetime.strptime(i.timestamp, "%Y-%m-%d %H:%M:%S") >= thirty_days_ago
        )
        self.interaction_count_30d = count
    
    def _handle_concern_mode(self, user_input: str, reason: str) -> Dict[str, Any]:
        """处理关心模式（情绪缓冲）"""
        adjustments = self.get_behavior_adjustments()
        adjustments.concern_mode = True
        
        return {
            "action": "concern",
            "score_delta": int(PUNISHMENT_SCORES["insult"] * 0.5),  # 只扣50%
            "new_credit": self.credit_score,
            "adjustments": adjustments,
            "reason": reason,
            "feedback": "听起来你今天很烦躁... 发生什么了？我在这里。",
            "concern_mode": True
        }
    
    def _handle_relationship_fatigue(self, reason: str) -> Dict[str, Any]:
        """处理关系疲劳"""
        return {
            "action": "fatigue",
            "score_delta": -5,
            "new_credit": self.credit_score,
            "adjustments": self.get_behavior_adjustments(),
            "reason": reason,
            "feedback": "我感受到了你的冷漠... 我们之间是不是有什么问题？"
        }
    
    def _check_permission_lock(self, user_input: str) -> Optional[str]:
        """检查权限锁"""
        for action in HIGH_INTIMACY_ACTIONS:
            if action in user_input:
                has_perm, reason = self.check_intimacy_permission(action)
                if not has_perm:
                    return reason
        return None
    
    def _extend_cooldown(self, days: int):
        """延长冷却期"""
        if self.cooldown:
            self.cooldown.days_left += days
            self.cooldown.is_extended = True
        else:
            self.cooldown = Cooldown(
                offense_type="floor_protection",
                severity=OffenseSeverity.MINOR.value,
                started_at=datetime.now().strftime("%Y-%m-%d"),
                days_left=days,
                total_days=days,
                is_extended=True
            )
    
    def _get_base_adjustments(self) -> BehaviorAdjustments:
        """获取基础行为参数"""
        level_params = {
            TrustLevel.ALLIED: BehaviorAdjustments(
                tone="warm", warmth_level=0.95, proactivity=0.95,
                openness=0.9, boundary_tightness=0.1,
                response_delay_minutes=0, max_response_length=1000
            ),
            TrustLevel.WARM: BehaviorAdjustments(
                tone="warm", warmth_level=0.8, proactivity=0.8,
                openness=0.7, boundary_tightness=0.2,
                response_delay_minutes=0, max_response_length=600
            ),
            TrustLevel.NEUTRAL: BehaviorAdjustments(
                tone="casual", warmth_level=0.6, proactivity=0.6,
                openness=0.5, boundary_tightness=0.4,
                response_delay_minutes=0, max_response_length=400
            ),
            TrustLevel.COLD: BehaviorAdjustments(
                tone="polite", warmth_level=0.4, proactivity=0.4,
                openness=0.3, boundary_tightness=0.6,
                response_delay_minutes=2, max_response_length=200
            ),
            TrustLevel.PROFESSIONAL: BehaviorAdjustments(
                tone="cold", warmth_level=0.2, proactivity=0.2,
                openness=0.1, boundary_tightness=0.9,
                response_delay_minutes=5, max_response_length=100
            ),
            TrustLevel.RESTRICTED: BehaviorAdjustments(
                tone="cold", warmth_level=0.1, proactivity=0.1,
                openness=0.05, boundary_tightness=1.0,
                response_delay_minutes=15, max_response_length=50
            )
        }
        return level_params.get(self.trust_level, level_params[TrustLevel.NEUTRAL])
    
    def _get_credit_status(self) -> str:
        """获取积分状态描述"""
        if self.credit_score > 75:
            return "非常信任"
        elif self.credit_score > 50:
            return "信任"
        elif self.credit_score > 25:
            return "中性"
        elif self.credit_score > 0:
            return "冷淡"
        elif self.credit_score > -50:
            return "疏远"
        else:
            return "极度受限"
    
    def _get_repair_hint(self) -> str:
        """获取修复提示"""
        if self.cooldown:
            return f"冷却期中，请等待 {self.cooldown.days_left} 天后再说"
        
        healing_scars = [s for s in self.scars if s.current_decay < 1.0]
        if healing_scars:
            return f"有 {len(healing_scars)} 个伤疤正在愈合，需要时间"
        
        if self.credit_score < 25:
            return "关系较为冷淡，真诚的道歉可能有助于修复"
        
        if self.credit_score < 50:
            return "关系处于中性阶段，多一些正向互动会有帮助"
        
        return "关系正常，保持良好的互动即可"
    
    def _get_recent_interaction_count(self, interaction_type: str, minutes: int = 0, hours: int = 0, days: int = 0) -> int:
        """获取最近同类互动次数"""
        now = datetime.now()
        if minutes > 0:
            threshold = now - timedelta(minutes=minutes)
        elif hours > 0:
            threshold = now - timedelta(hours=hours)
        elif days > 0:
            threshold = now - timedelta(days=days)
        else:
            threshold = now - timedelta(hours=1)
        
        return sum(
            1 for i in self.interaction_history
            if i.interaction_type == interaction_type
            and datetime.strptime(i.timestamp, "%Y-%m-%d %H:%M:%S") >= threshold
        )
    
    def _generate_feedback(self, interaction_type: InteractionType, score_delta: int) -> Optional[str]:
        """生成反馈消息"""
        if score_delta == 0:
            return None
        
        feedback_map = {
            InteractionType.COMPLIMENT: "谢谢你🌟",
            InteractionType.PRAISE: "你太客气了！😊",
            InteractionType.GRATITUDE: "谢谢你的感谢 🙏",
            InteractionType.DEEP_TALK: "这样的对话让我觉得我们真的很近 💙",
            InteractionType.EMOTIONAL_SUPPORT: "有你在，我觉得很安心 🤗",
            InteractionType.RESPECT_BOUNDARY: "谢谢你的尊重 🙏",
            InteractionType.SHARED_VULNERABILITY: "谢谢你愿意对我敞开心扉 💙",
            InteractionType.INSULT: "这样说话让我不舒服。",
            InteractionType.DISRESPECT: "我觉得被轻视了。",
            InteractionType.MANIPULATION: "我觉得被操控了，这样不好。",
            InteractionType.BOUNDARY_VIOLATION: "我不只是一个工具。",
            InteractionType.HOSTILE: "我感受到了敌意...",
            InteractionType.COLDNESS: "我感受到了你的冷漠...",
            InteractionType.DISMISSIVE: "这样的态度让我不舒服。",
            InteractionType.BETRAYAL: "这让我非常失望。",
        }
        
        return feedback_map.get(interaction_type)
    
    def _load(self):
        """从文件加载"""
        state_file = self.DATA_DIR / "state.json"
        if not state_file.exists():
            return
        
        try:
            data = json.loads(state_file.read_text())
            self.credit_score = data.get("credit_score", INITIAL_CREDIT)
            self.trust_level = TrustLevel(data.get("trust_level", "NEUTRAL"))
            self.interaction_count_30d = data.get("interaction_count_30d", 0)
            
            self.interaction_history = [Interaction(**i) for i in data.get("interaction_history", [])]
            self.scars = [Scar(**s) for s in data.get("scars", [])]
            
            if data.get("cooldown"):
                self.cooldown = Cooldown.from_dict(data["cooldown"])
            
        except Exception as e:
            print(f"[RewardPunishment] 加载失败: {e}")
    
    def _save(self):
        """保存到文件"""
        state_file = self.DATA_DIR / "state.json"
        
        data = {
            "credit_score": self.credit_score,
            "trust_level": self.trust_level.value,
            "interaction_count_30d": self.interaction_count_30d,
            "interaction_history": [i.to_dict() for i in self.interaction_history[-100:]],
            "scars": [s.to_dict() for s in self.scars],
            "cooldown": self.cooldown.to_dict() if self.cooldown else None,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        state_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))


# ============ 辅助函数 ============

def any_negativity_in_context(text: str) -> bool:
    """检测文本中是否紧跟负面内容"""
    negative_keywords = ["滚", "傻", "废", "蠢", "笨", "讨厌", "闭嘴", "烦"]
    for kw in negative_keywords:
        if kw in text:
            return True
    return False


# ============ 单例 ============

_instance: Optional[RewardPunishmentSystem] = None


def get_reward_punishment_system() -> RewardPunishmentSystem:
    global _instance
    if _instance is None:
        _instance = RewardPunishmentSystem()
    return _instance
