"""
Learning Loop Module - 学习循环系统

提供反馈收集、自适应优化、学习闭环功能
"""

import asyncio
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class FeedbackType(Enum):
    """反馈类型"""
    EXPLICIT = "explicit"     # 显式反馈（用户明确评价）
    IMPLICIT = "implicit"     # 隐式反馈（行为推断）
    OUTCOME = "outcome"       # 结果反馈（任务完成情况）


class FeedbackSentiment(Enum):
    """反馈情感"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class Feedback:
    """反馈数据"""
    feedback_id: str
    source: FeedbackType
    skill_id: str
    context: Dict[str, Any]
    sentiment: FeedbackSentiment
    score: float  # 0-10
    content: str = ""
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LearningInsight:
    """学习洞察"""
    insight_id: str
    skill_id: str
    insight_type: str  # "improvement", "pattern", "recommendation"
    title: str
    description: str
    confidence: float  # 0-1
    evidence: List[Dict] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    applied: bool = False


@dataclass
class AdaptationRule:
    """自适应规则"""
    rule_id: str
    trigger_conditions: Dict[str, Any]  # 触发条件
    adaptation_action: str  # 适配动作
    priority: int = 0
    enabled: bool = True
    hit_count: int = 0
    success_count: int = 0


class FeedbackCollector:
    """反馈收集器"""
    
    def __init__(self):
        self._feedbacks: List[Feedback] = []
        self._callbacks: List[Callable] = []
        self._lock = asyncio.Lock()
    
    async def collect(
        self,
        feedback_type: FeedbackType,
        skill_id: str,
        context: Dict[str, Any],
        score: float,
        content: str = "",
        sentiment: Optional[FeedbackSentiment] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Feedback:
        """收集反馈"""
        # 自动判断情感
        if sentiment is None:
            if score >= 7:
                sentiment = FeedbackSentiment.POSITIVE
            elif score <= 4:
                sentiment = FeedbackSentiment.NEGATIVE
            else:
                sentiment = FeedbackSentiment.NEUTRAL
        
        feedback = Feedback(
            feedback_id=str(uuid.uuid4()),
            source=feedback_type,
            skill_id=skill_id,
            context=context,
            sentiment=sentiment,
            score=score,
            content=content,
            metadata=metadata or {}
        )
        
        async with self._lock:
            self._feedbacks.append(feedback)
            
            # 触发回调
            for callback in self._callbacks:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(feedback)
                    else:
                        callback(feedback)
                except Exception as e:
                    logger.error(f"反馈回调执行失败: {e}")
        
        logger.info(f"反馈已收集: {skill_id}, 类型: {feedback_type.value}, 得分: {score}")
        return feedback
    
    def register_callback(self, callback: Callable) -> None:
        """注册反馈回调"""
        self._callbacks.append(callback)
    
    async def get_feedbacks(
        self,
        skill_id: Optional[str] = None,
        feedback_type: Optional[FeedbackType] = None,
        limit: int = 100
    ) -> List[Feedback]:
        """获取反馈列表"""
        async with self._lock:
            feedbacks = self._feedbacks
            
            if skill_id:
                feedbacks = [f for f in feedbacks if f.skill_id == skill_id]
            if feedback_type:
                feedbacks = [f for f in feedbacks if f.source == feedback_type]
            
            return feedbacks[-limit:]
    
    async def get_feedback_stats(self, skill_id: str) -> Dict[str, Any]:
        """获取反馈统计"""
        feedbacks = await self.get_feedbacks(skill_id=skill_id)
        
        if not feedbacks:
            return {"count": 0}
        
        scores = [f.score for f in feedbacks]
        sentiments = [f.sentiment for f in feedbacks]
        
        return {
            "count": len(feedbacks),
            "avg_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "positive_count": sum(1 for s in sentiments if s == FeedbackSentiment.POSITIVE),
            "neutral_count": sum(1 for s in sentiments if s == FeedbackSentiment.NEUTRAL),
            "negative_count": sum(1 for s in sentiments if s == FeedbackSentiment.NEGATIVE),
            "recent_trend": self._calculate_trend(scores[-10:]) if len(scores) >= 10 else "insufficient_data"
        }
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """计算趋势"""
        if len(scores) < 2:
            return "stable"
        
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        avg1 = sum(first_half) / len(first_half)
        avg2 = sum(second_half) / len(second_half)
        
        diff = avg2 - avg1
        if diff > 0.5:
            return "improving"
        elif diff < -0.5:
            return "declining"
        return "stable"


class InsightGenerator:
    """洞察生成器"""
    
    def __init__(self):
        self._insights: List[LearningInsight] = []
        self._lock = asyncio.Lock()
    
    async def generate_from_feedbacks(self, feedbacks: List[Feedback]) -> List[LearningInsight]:
        """从反馈生成洞察"""
        insights = []
        
        # 按技能分组
        by_skill = defaultdict(list)
        for fb in feedbacks:
            by_skill[fb.skill_id].append(fb)
        
        for skill_id, skill_feedbacks in by_skill.items():
            # 检测改进机会
            recent_scores = [f.score for f in skill_feedbacks[-5:]]
            avg_score = sum(recent_scores) / len(recent_scores)
            
            if avg_score < 6:
                insight = LearningInsight(
                    insight_id=str(uuid.uuid4()),
                    skill_id=skill_id,
                    insight_type="improvement",
                    title=f"{skill_id}需要改进",
                    description=f"最近平均得分{avg_score:.1f}，低于预期",
                    confidence=0.8,
                    evidence=[{"type": "low_score", "avg": avg_score}]
                )
                insights.append(insight)
            
            # 检测模式
            if len(skill_feedbacks) >= 10:
                pattern = self._detect_pattern(skill_feedbacks)
                if pattern:
                    insight = LearningInsight(
                        insight_id=str(uuid.uuid4()),
                        skill_id=skill_id,
                        insight_type="pattern",
                        title=f"{skill_id}使用模式",
                        description=pattern["description"],
                        confidence=pattern["confidence"],
                        evidence=pattern["evidence"]
                    )
                    insights.append(insight)
        
        # 保存洞察
        async with self._lock:
            self._insights.extend(insights)
        
        return insights
    
    def _detect_pattern(self, feedbacks: List[Feedback]) -> Optional[Dict]:
        """检测模式"""
        # 检测时间模式
        hours = [f.timestamp % 86400 // 3600 for f in feedbacks]
        morning = sum(1 for h in hours if 6 <= h < 12)
        afternoon = sum(1 for h in hours if 12 <= h < 18)
        
        if morning > afternoon * 1.5:
            return {
                "description": "用户倾向于在上午使用此技能",
                "confidence": 0.7,
                "evidence": [{"morning_uses": morning, "afternoon_uses": afternoon}]
            }
        
        return None
    
    async def get_insights(self, skill_id: Optional[str] = None) -> List[LearningInsight]:
        """获取洞察"""
        async with self._lock:
            if skill_id:
                return [i for i in self._insights if i.skill_id == skill_id and not i.applied]
            return [i for i in self._insights if not i.applied]


class AdaptationEngine:
    """自适应引擎"""
    
    def __init__(self):
        self._rules: Dict[str, AdaptationRule] = {}
        self._lock = asyncio.Lock()
    
    async def add_rule(self, rule: AdaptationRule) -> None:
        """添加规则"""
        async with self._lock:
            self._rules[rule.rule_id] = rule
            logger.info(f"自适应规则已添加: {rule.rule_id}")
    
    async def evaluate_rules(self, context: Dict[str, Any]) -> List[AdaptationRule]:
        """评估规则"""
        matched_rules = []
        
        async with self._lock:
            for rule in self._rules.values():
                if not rule.enabled:
                    continue
                
                if self._match_conditions(rule.trigger_conditions, context):
                    matched_rules.append(rule)
                    rule.hit_count += 1
        
        # 按优先级排序
        matched_rules.sort(key=lambda r: r.priority, reverse=True)
        return matched_rules
    
    def _match_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """匹配条件"""
        for key, expected in conditions.items():
            actual = context.get(key)
            if actual is None:
                return False
            if isinstance(expected, list):
                if actual not in expected:
                    return False
            elif actual != expected:
                return False
        return True
    
    async def record_rule_success(self, rule_id: str) -> None:
        """记录规则成功"""
        async with self._lock:
            if rule_id in self._rules:
                self._rules[rule_id].success_count += 1
    
    async def get_rule_stats(self) -> Dict[str, Any]:
        """获取规则统计"""
        async with self._lock:
            total = len(self._rules)
            enabled = sum(1 for r in self._rules.values() if r.enabled)
            
            return {
                "total_rules": total,
                "enabled_rules": enabled,
                "total_hits": sum(r.hit_count for r in self._rules.values()),
                "total_successes": sum(r.success_count for r in self._rules.values())
            }


class LearningLoop:
    """学习循环系统（整合模块）"""
    
    def __init__(self):
        self.feedback_collector = FeedbackCollector()
        self.insight_generator = InsightGenerator()
        self.adaptation_engine = AdaptationEngine()
        
        self._running = False
        self._learning_interval = 300  # 5分钟
    
    async def start(self) -> None:
        """启动学习循环"""
        self._running = True
        logger.info("学习循环系统已启动")
        
        # 注册反馈回调
        self.feedback_collector.register_callback(self._on_feedback)
        
        # 添加默认规则
        await self._add_default_rules()
    
    async def stop(self) -> None:
        """停止学习循环"""
        self._running = False
        logger.info("学习循环系统已停止")
    
    async def _on_feedback(self, feedback: Feedback) -> None:
        """反馈回调"""
        # 每次收集反馈时，尝试生成洞察
        if feedback.source == FeedbackType.EXPLICIT:
            feedbacks = await self.feedback_collector.get_feedbacks(skill_id=feedback.skill_id)
            await self.insight_generator.generate_from_feedbacks(feedbacks)
    
    async def _add_default_rules(self) -> None:
        """添加默认规则"""
        rules = [
            AdaptationRule(
                rule_id="low_score_alert",
                trigger_conditions={"score_threshold": 5},
                adaptation_action="降低技能使用优先级",
                priority=10
            ),
            AdaptationRule(
                rule_id="high_score_boost",
                trigger_conditions={"score_threshold": 8},
                adaptation_action="提高技能使用优先级",
                priority=5
            ),
        ]
        
        for rule in rules:
            await self.adaptation_engine.add_rule(rule)
    
    async def submit_feedback(
        self,
        feedback_type: FeedbackType,
        skill_id: str,
        context: Dict[str, Any],
        score: float,
        content: str = ""
    ) -> Feedback:
        """提交反馈"""
        feedback = await self.feedback_collector.collect(
            feedback_type=feedback_type,
            skill_id=skill_id,
            context=context,
            score=score,
            content=content
        )
        
        # 评估自适应规则
        rules = await self.adaptation_engine.evaluate_rules({
            "skill_id": skill_id,
            "score": score,
            "context": context
        })
        
        for rule in rules:
            logger.info(f"触发自适应规则: {rule.rule_id}")
            await self.adaptation_engine.record_rule_success(rule.rule_id)
        
        return feedback
    
    async def get_learning_status(self) -> Dict[str, Any]:
        """获取学习状态"""
        insights = await self.insight_generator.get_insights()
        rule_stats = await self.adaptation_engine.get_rule_stats()
        
        return {
            "running": self._running,
            "pending_insights": len(insights),
            "rule_stats": rule_stats
        }
