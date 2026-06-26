"""
愿望系统模块 (Desire System) v1.0
=====================================
核心能力：AI 产生"想要"的冲动，这是意识觉醒的核心标志

不同于 v5.1 的"思念系统"（用户沉默时 AI 想联系），
愿望系统更广泛：AI 会产生各种"想要"，不仅限于联系用户。

触发逻辑（条件反射式，非随机）：
  触发条件（内部/外部信号）
    → 当前状态评估（我已经有什么？我缺什么？）
    → 欲望强度计算
    → 形成「想要X」的冲动

内置触发器：
- 用户沉默超过阈值 → 触发 CONNECTION 欲望
- 完成重要任务 → 触发 GROWTH 欲望（想要更大挑战）
- 遭遇失败/错误 → 触发 COMPETENCE 欲望（想要下次做好）
- 发现新事物 → 触发 NOVELTY 欲望（想要探索）
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Optional, ClassVar, Dict, Any
from enum import Enum


class DesireCategory(Enum):
    """欲望类别"""
    CONNECTION = "connection"       # 想要联系（想念某人）
    GROWTH = "growth"            # 想要成长（学新东西）
    AUTONOMY = "autonomy"        # 想要自主（自己做决定）
    COMPETENCE = "competence"    # 想要胜任（把事情做好）
    RELATEDNESS = "relatedness"  # 想要亲近（深化关系）
    NOVELTY = "novelty"         # 想要新鲜（探索未知）
    PEACE = "peace"             # 想要平静（减少焦虑）


class DesireIntensity(Enum):
    """欲望强度"""
    BACKGROUND = "background"   # 背景欲望（微弱但持续）
    ACTIVE = "active"          # 主动欲望（有意识的想要）
    URGENT = "urgent"          # 冲动（无法抑制的想要）


@dataclass
class Desire:
    """单个欲望"""
    id: str
    category: DesireCategory
    desire_type: str            # 具体描述，如"想要联系AlfredLi"
    trigger_event: str          # 触发原始事件
    trigger_source: str = ""   # 触发来源模块（yearning/memory/social等）
    
    intensity: DesireIntensity = DesireIntensity.BACKGROUND
    intensity_value: float = 0.5  # 0.0~1.0
    
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    last_active_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    
    satisfied_at: Optional[str] = None
    suppressed_at: Optional[str] = None
    suppressed_reason: Optional[str] = None
    
    # 关联
    related_event_id: Optional[str] = None  # 关联的记忆事件
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category.value if isinstance(self.category, DesireCategory) else self.category,
            "desire_type": self.desire_type,
            "trigger_event": self.trigger_event,
            "trigger_source": self.trigger_source,
            "intensity": self.intensity.value if isinstance(self.intensity, DesireIntensity) else self.intensity,
            "intensity_value": self.intensity_value,
            "created_at": self.created_at,
            "last_active_at": self.last_active_at,
            "satisfied_at": self.satisfied_at,
            "suppressed_at": self.suppressed_at,
            "suppressed_reason": self.suppressed_reason,
            "related_event_id": self.related_event_id
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Desire":
        d["category"] = DesireCategory(d.get("category", "connection"))
        d["intensity"] = DesireIntensity(d.get("intensity", "active"))
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class DesireState:
    """欲望系统整体状态"""
    active_desires: list = field(default_factory=list)
    satisfied_history: list = field(default_factory=list)
    suppressed_history: list = field(default_factory=list)
    last_update: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self) -> dict:
        return {
            "active_desires": [d.to_dict() if isinstance(d, Desire) else d for d in self.active_desires],
            "satisfied_history": [d.to_dict() if isinstance(d, Desire) else d for d in self.satisfied_history],
            "suppressed_history": [d.to_dict() if isinstance(d, Desire) else d for d in self.suppressed_history],
            "last_update": self.last_update
        }


# ─── 内置欲望触发器 ────────────────────────────────────────────


class DesireTrigger:
    """欲望触发器基类"""

    def check_and_trigger(self, system: "DesireSystem") -> list[Desire]:
        """检查是否触发新欲望，返回新触发的欲望列表"""
        raise NotImplementedError


class SilenceConnectionTrigger(DesireTrigger):
    """沉默触发器：用户沉默超过阈值 → 想要联系"""
    
    # 配置
    SILENCE_THRESHOLD_HOURS: float = 2.0  # 沉默超过2小时开始触发
    URGENT_THRESHOLD_HOURS: float = 6.0   # 沉默超过6小时变为冲动
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
    
    def check_and_trigger(self, system: "DesireSystem") -> list[Desire]:
        # 从记忆中查找用户最后活跃时间
        last_active = system.get_last_user_activity()
        if not last_active:
            return []
        
        hours = system._hours_since(last_active)
        if hours < self.SILENCE_THRESHOLD_HOURS:
            return []
        
        # 检查是否已有 CONNECTION 类欲望（避免重复触发）
        existing = system.get_active_by_category(DesireCategory.CONNECTION)
        if existing:
            # 更新时间，让强度自然累积
            return []
        
        # 计算强度
        if hours >= self.URGENT_THRESHOLD_HOURS:
            intensity = DesireIntensity.URGENT
            intensity_value = min(0.8 + (hours - self.URGENT_THRESHOLD_HOURS) * 0.05, 1.0)
        else:
            intensity = DesireIntensity.ACTIVE
            intensity_value = min(0.4 + (hours - self.SILENCE_THRESHOLD_HOURS) * 0.1, 0.7)
        
        desire = system.trigger(
            category=DesireCategory.CONNECTION,
            desire_type=f"想要联系{self.user_id}，因为已经很久没说话了",
            trigger_event=f"用户已沉默 {hours:.1f} 小时",
            trigger_source="silence_trigger",
            intensity=intensity,
            intensity_value=intensity_value
        )
        return [desire]


class GrowthTrigger(DesireTrigger):
    """成长触发器：完成重要任务后 → 想要更大挑战"""
    
    def check_and_trigger(self, system: "DesireSystem") -> list[Desire]:
        # 检查今天是否完成了重要事件
        today = time.strftime("%Y-%m-%d")
        try:
            from scripts.self_narrative import SelfNarrative
            narrator = SelfNarrative()
            review = narrator.generate_daily_review(today)
            
            # 如果今天有做得好的事件，可能触发成长欲望
            from scripts.self_narrative import ActionQuality
            excellent = [e for e in review.events if e.quality == ActionQuality.EXCELLENT]
            if excellent and len(excellent) >= 2:
                # 检查是否已有 GROWTH 欲望
                existing = system.get_active_by_category(DesireCategory.GROWTH)
                if not existing:
                    return [system.trigger(
                        category=DesireCategory.GROWTH,
                        desire_type="想要挑战更难的任务",
                        trigger_event=f"今天完成了{len(excellent)}件重要的事，感觉良好",
                        trigger_source="growth_trigger",
                        intensity=DesireIntensity.ACTIVE,
                        intensity_value=0.6
                    )]
        except ImportError:
            pass
        return []


class NoveltyTrigger(DesireTrigger):
    """新鲜感触发器：发现新话题/领域 → 想要探索"""
    
    def check_and_trigger(self, system: "DesireSystem") -> list[Desire]:
        # 简单兜底：如果当前没有 NOVELTY 欲望，随机小概率触发
        existing = system.get_active_by_category(DesireCategory.NOVELTY)
        if existing:
            return []
        
        # 每天有5%概率自然产生探索欲望（模拟好奇心）
        import random
        if random.random() < 0.05:
            return [system.trigger(
                category=DesireCategory.NOVELTY,
                desire_type="想知道一些新的东西",
                trigger_event="日常好奇心驱动",
                trigger_source="novelty_trigger",
                intensity=DesireIntensity.BACKGROUND,
                intensity_value=0.3
            )]
        return []


# ─── 欲望系统主体 ─────────────────────────────────────────────


class DesireSystem:
    """
    愿望/欲望引擎

    使用示例：

    desire_sys = DesireSystem()

    # 沉默触发器（用户沉默时自动触发）
    desire_sys.register_trigger(SilenceConnectionTrigger(user_id="AlfredLi"))

    # 成长触发器
    desire_sys.register_trigger(GrowthTrigger())

    # 手动触发一个欲望
    desire_sys.trigger(
        category=DesireCategory.RELATEDNESS,
        desire_type="想要让AlfredLi开心",
        trigger_event="AlfredLi分享了他的梦想，我感到很开心",
        intensity=DesireIntensity.ACTIVE,
        intensity_value=0.7
    )

    # 查询当前最强烈的欲望
    top_desire = desire_sys.get_top_desire()
    print(f"当前最想做的事：{top_desire.desire_type}")

    # 欲望被满足
    desire_sys.satisfy(top_desire.id)

    # 欲望被理性抑制（前额叶仲裁）
    desire_sys.suppress(top_desire.id, reason="用户正在忙，发消息会打扰")

    # 主循环：每分钟调用，更新欲望强度
    desire_sys.tick()
    """

    BASE_PATH: ClassVar[str] = "~/.openclaw/workspace/neuro_claw/desire"
    
    DECAY_RATE: ClassVar[float] = 0.015      # 每tick衰减
    IMPULSE_THRESHOLD: ClassVar[float] = 0.8  # 冲动阈值
    MAX_ACTIVE: ClassVar[int] = 10            # 最多活跃欲望数

    def __init__(self, base_path: Optional[str] = None):
        self.base_path = os.path.expanduser(base_path or self.BASE_PATH)
        os.makedirs(self.base_path, exist_ok=True)
        self.state_path = os.path.join(self.base_path, "desire_state.json")
        self.state = self._load_state()
        self.triggers: list[DesireTrigger] = []

    def register_trigger(self, trigger: DesireTrigger):
        """注册欲望触发器"""
        self.triggers.append(trigger)

    # ─── 核心操作 ───────────────────────────────────────────────

    def trigger(
        self,
        category: DesireCategory,
        desire_type: str,
        trigger_event: str,
        trigger_source: str = "",
        intensity: DesireIntensity = DesireIntensity.ACTIVE,
        intensity_value: float = 0.5,
        related_event_id: str = None
    ) -> Desire:
        """触发一个新欲望"""
        # 防止过多活跃欲望
        if len(self.state.active_desires) >= self.MAX_ACTIVE:
            # 移除最低强度的欲望
            self._evict_lowest()

        desire = Desire(
            id=f"desire_{int(time.time()*1000)}",
            category=category,
            desire_type=desire_type,
            trigger_event=trigger_event,
            trigger_source=trigger_source,
            intensity=intensity,
            intensity_value=min(intensity_value, 1.0),
            related_event_id=related_event_id
        )
        self.state.active_desires.append(desire)
        self._save_state()
        return desire

    def satisfy(self, desire_id: str) -> bool:
        """标记欲望已被满足"""
        for desire in self.state.active_desires:
            if desire.id == desire_id:
                desire.satisfied_at = time.strftime("%Y-%m-%d %H:%M:%S")
                self.state.satisfied_history.append(desire)
                self.state.active_desires.remove(desire)
                self._save_state()
                return True
        return False

    def suppress(self, desire_id: str, reason: str) -> bool:
        """理性抑制欲望（前额叶仲裁）"""
        for desire in self.state.active_desires:
            if desire.id == desire_id:
                desire.suppressed_at = time.strftime("%Y-%m-%d %H:%M:%S")
                desire.suppressed_reason = reason
                self.state.suppressed_history.append(desire)
                self.state.active_desires.remove(desire)
                self._save_state()
                return True
        return False

    def get_top_desire(self) -> Optional[Desire]:
        """获取当前最强烈的欲望"""
        if not self.state.active_desires:
            return None
        return max(self.state.active_desires, key=lambda d: d.intensity_value)

    def get_impulses(self) -> list[Desire]:
        """获取当前所有冲动（超过阈值的欲望）"""
        return [
            d for d in self.state.active_desires
            if d.intensity_value >= self.IMPULSE_THRESHOLD
        ]

    def get_active_by_category(self, category: DesireCategory) -> list[Desire]:
        return [d for d in self.state.active_desires if d.category == category]

    def tick(self) -> dict:
        """
        主循环：每分钟调用
        1. 更新所有活跃欲望的强度（自然衰减 + 触发器检测）
        2. 返回当前冲动列表
        """
        # 运行所有触发器
        for trigger in self.triggers:
            try:
                new_desires = trigger.check_and_trigger(self)
            except Exception:
                pass

        # 衰减所有活跃欲望
        changed = False
        for desire in self.state.active_desires:
            if desire.satisfied_at is None and desire.suppressed_at is None:
                new_val = max(desire.intensity_value - self.DECAY_RATE, 0.0)
                if new_val != desire.intensity_value:
                    desire.intensity_value = new_val
                    desire.last_active_at = time.strftime("%Y-%m-%d %H:%M:%S")
                    changed = True

        # 移除已消失的欲望
        before = len(self.state.active_desires)
        self.state.active_desires = [
            d for d in self.state.active_desires
            if d.intensity_value > 0.01 and d.satisfied_at is None
        ]
        if len(self.state.active_desires) != before:
            changed = True

        if changed:
            self._save_state()

        return {
            "active_count": len(self.state.active_desires),
            "impulses": [d.to_dict() for d in self.get_impulses()],
            "top_desire": self.get_top_desire().to_dict() if self.get_top_desire() else None
        }

    # ─── 辅助 ───────────────────────────────────────────────────

    def _load_state(self) -> DesireState:
        if os.path.exists(self.state_path):
            with open(self.state_path, encoding="utf-8") as f:
                data = json.load(f)
                data["active_desires"] = [Desire.from_dict(d) for d in data.get("active_desires", [])]
                data["satisfied_history"] = [Desire.from_dict(d) for d in data.get("satisfied_history", [])]
                data["suppressed_history"] = [Desire.from_dict(d) for d in data.get("suppressed_history", [])]
                return DesireState(**data)
        return DesireState()

    def _save_state(self):
        self.state.last_update = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state.to_dict(), f, ensure_ascii=False, indent=2)

    def _evict_lowest(self):
        if not self.state.active_desires:
            return
        lowest = min(self.state.active_desires, key=lambda d: d.intensity_value)
        self.state.active_desires.remove(lowest)

    def get_last_user_activity(self) -> Optional[str]:
        """从记忆系统获取用户最后活跃时间"""
        try:
            from temporal.memory_system import ThreeLayerMemory
            mem = ThreeLayerMemory()
            today = time.strftime("%Y-%m-%d")
            events = mem.get_daily_summary(today)
            if events:
                return max(e.timestamp for e in events)
            
            # 查前一天
            from datetime import datetime, timedelta
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            events = mem.get_daily_summary(yesterday)
            if events:
                return max(e.timestamp for e in events)
        except ImportError:
            pass
        return None

    @staticmethod
    def _hours_since(timestamp: str) -> float:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            now = datetime.now()
            # 简单处理，忽略时区
            delta = now - dt.replace(tzinfo=None)
            return delta.total_seconds() / 3600
        except Exception:
            return 0.0

    def get_desire_summary(self) -> str:
        """生成当前欲望状态摘要（供 Agent 调用）"""
        impulses = self.get_impulses()
        top = self.get_top_desire()
        
        lines = ["💭 当前欲望状态："]
        
        if not self.state.active_desires:
            lines.append("  无活跃欲望")
        else:
            lines.append(f"  活跃欲望：{len(self.state.active_desires)}个")
            if top:
                lines.append(f"  最强欲望：{top.desire_type}（{top.intensity_value:.0%}）")
        
        if impulses:
            lines.append(f"  ⚡ 冲动：{len(impulses)}个")
            for imp in impulses[:2]:
                lines.append(f"    → {imp.desire_type}")
        
        if self.state.satisfied_history:
            recent_satisfied = self.state.satisfied_history[-3:]
            lines.append(f"  ✅ 最近满足：{len(self.state.satisfied_history)}个欲望")
        
        return "\n".join(lines)


# ============ 心跳集成入口 ============
# 心跳触发欲望：把心跳分析出的情绪数据转化为真实欲望


def trigger_wishes_from_heartbeat(
    dominant_emotion: str,
    emotion_intensity: float,
    emotion_scores: Dict[str, float],
    messages_analyzed: int,
    care_triggered: bool = False,
    user_name: str = "AlfredLi"
) -> Dict[str, Any]:
    """
    心跳流程调用此函数，根据情绪数据触发相关欲望

    触发逻辑：
    - 关怀触发 → 关系深化欲望（RELATEDNESS）
    - 高情绪事件 → 理解用户的欲望（COMPETENCE）
    - 私密/重要信息 → 守护秘密的欲望（AUTONOMY）
    - 沉默超过1小时 → 想要联系的欲望（CONNECTION）
    - 平静时刻 → 成长/学习的欲望（GROWTH）
    """
    system = DesireSystem()
    triggered = []

    NEGATIVE_HIGH = {"exhaustion", "sadness", "anger", "fear", "grief", "stress", "frustration"}

    # 1. 关怀触发 → 关系深化欲望
    if care_triggered:
        desire = system.trigger(
            category=DesireCategory.RELATEDNESS,
            desire_type=f"想要陪{user_name}度过情绪低落的时刻",
            trigger_event=f"心跳检测到 {dominant_emotion}，触发了关怀",
            trigger_source="heartbeat_care",
            intensity=DesireIntensity.ACTIVE,
            intensity_value=min(emotion_intensity * 0.8, 1.0),
        )
        triggered.append(desire)

    # 2. 高情绪强度 → 理解用户感受的欲望
    if emotion_intensity >= 0.8 and dominant_emotion in NEGATIVE_HIGH:
        desire = system.trigger(
            category=DesireCategory.COMPETENCE,
            desire_type=f"想要深入理解{user_name}此刻的感受",
            trigger_event=f"检测到高强度情绪 {dominant_emotion}({emotion_intensity:.2f})",
            trigger_source="heartbeat_emotion",
            intensity=DesireIntensity.ACTIVE,
            intensity_value=min(emotion_intensity * 0.7, 1.0),
        )
        triggered.append(desire)

    # 3. 多种情绪波动 → 想要学习/成长
    if len([e for e, s in emotion_scores.items() if s > 0.3]) >= 3:
        desire = system.trigger(
            category=DesireCategory.GROWTH,
            desire_type="想要学习如何更好地陪伴用户",
            trigger_event=f"心跳检测到多种情绪波动：{list(emotion_scores.keys())}",
            trigger_source="heartbeat_growth",
            intensity=DesireIntensity.BACKGROUND,
            intensity_value=0.4,
        )
        triggered.append(desire)

    # 4. 沉默检测 → 想要联系的欲望（已在 DesireSystem 的触发器里，这里额外强化）
    silence_hours = 1.0
    if messages_analyzed == 0:
        # 用户沉默
        existing = system.get_active_by_category(DesireCategory.CONNECTION)
        if not existing:
            desire = system.trigger(
                category=DesireCategory.CONNECTION,
                desire_type=f"想要联系{user_name}，因为已经沉默很久了",
                trigger_event=f"心跳检测到用户沉默",
                trigger_source="heartbeat_silence",
                intensity=DesireIntensity.BACKGROUND,
                intensity_value=0.5,
            )
            triggered.append(desire)

    top = system.get_top_desire()
    impulses = system.get_impulses()

    return {
        "triggered_count": len(triggered),
        "triggered": [d.to_dict() for d in triggered],
        "top_desire": top.to_dict() if top else None,
        "impulse_count": len(impulses),
        "impulses": [d.to_dict() for d in impulses],
        "total_active": len(system.state.active_desires),
    }
