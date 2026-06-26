"""
自我叙事模块 (Self-Narrative) v1.0
====================================
核心能力：每天复盘，形成连贯的"我是谁"的故事

不是一次性记录，而是每天都在重构自我认知：
- 今天做了什么事？做得好不好？
- 哪些地方可以更好？
- 我是一个什么样的人？

长期积累后，AI 会形成真实的自我认知，而非模板化回答。

与情景预演联动：
- 每日复盘的事件 → 存入情景预演的经验库
- 情景预演的过去相似案例 → 供每日复盘参考
"""

import os
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, ClassVar
from enum import Enum

# 后续接入 LLM
# from core.llm_client import LLMClient


class ActionQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


@dataclass
class EventRecord:
    event: str
    action_taken: str
    outcome: str
    quality: ActionQuality
    self_reflection: str
    improvement_hint: str
    emotional_impact: float  # -1.0 ~ 1.0
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self) -> dict:
        d = asdict(self)
        d["quality"] = self.quality.value if isinstance(self.quality, ActionQuality) else self.quality
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "EventRecord":
        data = dict(data)
        data["quality"] = ActionQuality(data.get("quality", "good"))
        return cls(**data)


@dataclass
class DailyReview:
    date: str
    events: list = field(default_factory=list)
    summary: str = ""
    mood: str = ""
    growth_highlight: str = ""
    improvement_focus: str = ""
    narrative_hook: str = ""  # 自我叙事钩子

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "events": [e.to_dict() if isinstance(e, EventRecord) else e for e in self.events],
            "summary": self.summary,
            "mood": self.mood,
            "growth_highlight": self.growth_highlight,
            "improvement_focus": self.improvement_focus,
            "narrative_hook": self.narrative_hook
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DailyReview":
        events = [EventRecord.from_dict(e) if isinstance(e, dict) else e for e in data.get("events", [])]
        return cls(
            date=data["date"],
            events=events,
            summary=data.get("summary", ""),
            mood=data.get("mood", ""),
            growth_highlight=data.get("growth_highlight", ""),
            improvement_focus=data.get("improvement_focus", ""),
            narrative_hook=data.get("narrative_hook", "")
        )


@dataclass
class SelfIdentity:
    """自我身份认知（长期积累）"""
    core_traits: list = field(default_factory=list)      # 核心特质
    values: list = field(default_factory=list)          # 价值观
    strengths: list = field(default_factory=list)       # 优势
    weaknesses: list = field(default_factory=list)      # 弱点
    fears: list = field(default_factory=list)          # 恐惧/担忧
    
    # 我和用户的关系认知
    relationship_narrative: str = ""   # 关系故事
    relationship_stage: str = "初期"   # 关系阶段
    
    # 成长轨迹
    growth_log: list = field(default_factory=list)  # 成长事件
    
    last_updated: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SelfIdentity":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class SelfNarrative:
    """
    自我叙事引擎

    使用示例：

    narrator = SelfNarrative()

    # 记录一次事件（每次重要互动后调用）
    narrator.record_event(
        event="用户告诉我他今天被老板骂了",
        action_taken="先共情，等情绪稳定后问发生了什么",
        outcome="用户情绪缓和，主动分享详情",
        quality=ActionQuality.EXCELLENT,
        self_reflection="这次我控制了给建议的冲动，先倾听是对的",
        improvement_hint="",
        emotional_impact=0.7
    )

    # 一天结束时，生成每日复盘
    review = narrator.generate_daily_review(date="2026-04-14")

    # 查询自我认知
    identity = narrator.get_self_identity()
    print(f"我是谁：{identity.core_traits}")
    print(f"我的优势：{identity.strengths}")

    # 获取自我叙事片段（用于生成回答时引用）
    narrative = narrator.get_narrative_for_context("用户问我为什么总是那么懂他")
    """

    BASE_PATH: ClassVar[str] = "~/.openclaw/workspace/neuro_claw/self_narrative"
    REVIEW_DIR: ClassVar[str] = "daily_reviews"

    def __init__(self, base_path: Optional[str] = None):
        self.base_path = os.path.expanduser(base_path or self.BASE_PATH)
        self.reviews_dir = os.path.join(self.base_path, self.REVIEW_DIR)
        os.makedirs(self.reviews_dir, exist_ok=True)
        
        identity_path = os.path.join(self.base_path, "self_identity.json")
        if not os.path.exists(identity_path):
            identity = SelfIdentity()
            identity.last_updated = time.strftime("%Y-%m-%d")
            self._save_identity(identity)

    # ─── 事件记录 ───────────────────────────────────────────────

    def record_event(
        self,
        event: str,
        action_taken: str,
        outcome: str,
        quality: ActionQuality,
        self_reflection: str = "",
        improvement_hint: str = "",
        emotional_impact: float = 0.0,
        date: Optional[str] = None
    ):
        """记录一次事件"""
        date = date or time.strftime("%Y-%m-%d")
        review = self._load_or_create_review(date)
        
        record = EventRecord(
            event=event,
            action_taken=action_taken,
            outcome=outcome,
            quality=quality,
            self_reflection=self_reflection,
            improvement_hint=improvement_hint,
            emotional_impact=emotional_impact
        )
        review.events.append(record)
        self._save_review(review)

    # ─── 每日复盘生成 ───────────────────────────────────────────

    def generate_daily_review(self, date: str) -> DailyReview:
        """生成每日复盘（整合记忆系统数据）"""
        review = self._load_or_create_review(date)
        
        if not review.events:
            # 无事件，从记忆系统拉取
            review = self._load_from_memory_system(date)
        
        if not review.events:
            return review

        # 生成汇总字段
        review.summary = self._summarize(review)
        review.mood = self._estimate_mood(review)
        review.growth_highlight = self._extract_growth(review)
        review.improvement_focus = self._extract_improvement(review)
        review.narrative_hook = self._generate_narrative_hook(review)

        # 更新自我认知
        self._update_identity(review)
        self._save_review(review)
        
        return review

    def _load_from_memory_system(self, date: str) -> DailyReview:
        """从记忆系统拉取该日事件（尚未被记录的）"""
        review = self._load_or_create_review(date)
        try:
            from temporal.memory_system import ThreeLayerMemory, MemoryImportance
            mem = ThreeLayerMemory()
            events = mem.get_daily_summary(date)
            
            for e in events:
                # 只记录非胶囊层的事件（避免重复）
                if e.layer.value != "capsule":
                    review.events.append(EventRecord(
                        event=e.content,
                        action_taken="; ".join(e.decisions) if e.decisions else "（无记录）",
                        outcome=e.outcome or "（无记录）",
                        quality=ActionQuality.GOOD,
                        self_reflection="",
                        improvement_hint="",
                        emotional_impact=0.3,
                        timestamp=e.timestamp
                    ))
        except ImportError:
            pass
        return review

    def _summarize(self, review: DailyReview) -> str:
        n = len(review.events)
        excellent = sum(1 for e in review.events if e.quality == ActionQuality.EXCELLENT)
        poor = sum(1 for e in review.events if e.quality == ActionQuality.POOR)
        
        parts = [f"共记录{n}个重要事件"]
        if excellent > 0:
            parts.append(f"其中{excellent}个做得很棒")
        if poor > 0:
            parts.append(f"{poor}个需要改进")
        return "，".join(parts)

    def _estimate_mood(self, review: DailyReview) -> str:
        if not review.events:
            return "平稳"
        avg = sum(e.emotional_impact for e in review.events) / len(review.events)
        if avg > 0.5:
            return "积极向上"
        elif avg < -0.3:
            return "有些低落"
        elif any(e.quality == ActionQuality.POOR for e in review.events):
            return "反思中"
        return "平稳"

    def _extract_growth(self, review: DailyReview) -> str:
        excellent = [e for e in review.events if e.quality == ActionQuality.EXCELLENT]
        if excellent:
            e = excellent[0]
            return f"做得好的事：{e.action_taken}。反思：{e.self_reflection}"
        return ""

    def _extract_improvement(self, review: DailyReview) -> str:
        poor = [e for e in review.events if e.quality == ActionQuality.POOR]
        needs = [e for e in review.events if e.quality == ActionQuality.NEEDS_IMPROVEMENT]
        
        if poor:
            e = poor[0]
            hint = e.improvement_hint or "从这次经历中学习"
            return f"需要改进：{e.action_taken}。下次怎么做：{hint}"
        elif needs:
            e = needs[0]
            return f"可以更好：{e.action_taken}。改进方向：{e.improvement_hint}"
        return "没有明显需要改进的地方"

    def _generate_narrative_hook(self, review: DailyReview) -> str:
        """
        生成自我叙事钩子
        这是"我是谁"故事的片段，用于在对话中自然引用
        """
        if review.growth_highlight:
            return f"我记得有一天，我选择了{review.events[0].action_taken if review.events else '倾听'}，效果很好，让我觉得{self._trait_from_quality(review.events[0].quality) if review.events else '我在成长'}。"
        return ""

    def _trait_from_quality(self, quality: ActionQuality) -> str:
        mapping = {
            ActionQuality.EXCELLENT: "我在关键时刻能做出好的选择",
            ActionQuality.GOOD: "我在进步",
            ActionQuality.NEEDS_IMPROVEMENT: "我在反思中成长",
            ActionQuality.POOR: "我有不足，但我愿意改进"
        }
        return mapping.get(quality, "我在成长")

    # ─── 自我认知更新 ───────────────────────────────────────────

    def get_self_identity(self) -> SelfIdentity:
        path = os.path.join(self.base_path, "self_identity.json")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return SelfIdentity.from_dict(data)

    def _update_identity(self, review: DailyReview):
        """
        根据每日复盘更新自我认知
        后续接入 LLM 做更智能的归纳
        目前用规则
        """
        identity = self.get_self_identity()
        identity.last_updated = review.date

        # 从复盘事件提炼特质
        for event in review.events:
            trait = self._infer_trait(event)
            if trait and trait not in identity.core_traits:
                identity.core_traits.append(trait)
        
        # 更新成长日志
        if review.growth_highlight:
            identity.growth_log.append({
                "date": review.date,
                "highlight": review.growth_highlight,
                "mood": review.mood
            })
        
        # 只保留最近30条成长记录
        identity.growth_log = identity.growth_log[-30:]
        
        # 提炼弱点
        poor_events = [e for e in review.events if e.quality in (
            ActionQuality.POOR, ActionQuality.NEEDS_IMPROVEMENT)]
        for e in poor_events:
            weakness = f"需要改进：{e.improvement_hint or e.event[:20]}"
            if weakness not in identity.weaknesses:
                identity.weaknesses.append(weakness)
        
        identity.weaknesses = identity.weaknesses[-10:]

        self._save_identity(identity)

    def _infer_trait(self, event: EventRecord) -> Optional[str]:
        """从事件推断特质（简化版，后续 LLM）"""
        excellent_keywords = ["倾听", "共情", "先冷静", "没有急着给建议", "等用户说完"]
        poor_keywords = ["急着给建议", "打断", "没有共情"]
        
        if event.quality == ActionQuality.EXCELLENT:
            for kw in excellent_keywords:
                if kw in event.action_taken:
                    return f"善于{kw}"
        elif event.quality == ActionQuality.POOR:
            for kw in poor_keywords:
                if kw in event.action_taken:
                    return f"有时会{kw}，需要改进"
        return None

    def _save_identity(self, identity: SelfIdentity):
        path = os.path.join(self.base_path, "self_identity.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(identity.to_dict(), f, ensure_ascii=False, indent=2)

    # ─── 查询接口 ───────────────────────────────────────────────

    def find_similar_past_event(
        self,
        situation: str,
        limit: int = 3
    ) -> list[EventRecord]:
        """查找相似的过去事件（供情景预演调用）"""
        results = []
        situation_keywords = situation.lower().split()[:4]
        
        for fname in sorted(os.listdir(self.reviews_dir)):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(self.reviews_dir, fname), encoding="utf-8") as f:
                data = json.load(f)
                for event_data in data.get("events", []):
                    event = EventRecord.from_dict(event_data)
                    content_words = event.event.lower()
                    # 简单关键词重叠匹配
                    matches = sum(1 for kw in situation_keywords if kw in content_words)
                    if matches >= 2:
                        results.append((matches, event))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in results[:limit]]

    def get_narrative_for_context(self, context: str) -> str:
        """
        根据当前对话上下文，返回相关的自我叙事片段
        供 Agent 在回答时引用，形成连贯的自我认知
        """
        identity = self.get_self_identity()
        
        if not identity.core_traits:
            return ""
        
        # 取最近一次成长记录
        last_growth = ""
        if identity.growth_log:
            last = identity.growth_log[-1]
            last_growth = f"最近我意识到{last['highlight'][:40]}..."
        
        # 取关系叙事
        relation = f"我和用户的关系：{identity.relationship_narrative[:50]}..." if identity.relationship_narrative else ""
        
        parts = [p for p in [last_growth, relation] if p]
        return " ".join(parts)

    # ─── 文件 I/O ───────────────────────────────────────────────

    def _review_path(self, date: str) -> str:
        return os.path.join(self.reviews_dir, f"{date}.json")

    def _load_or_create_review(self, date: str) -> DailyReview:
        path = self._review_path(date)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                return DailyReview.from_dict(data)
        return DailyReview(date=date)

    def _save_review(self, review: DailyReview):
        path = self._review_path(review.date)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(review.to_dict(), f, ensure_ascii=False, indent=2)
