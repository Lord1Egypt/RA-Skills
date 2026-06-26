# learning_engine.py
# MemPalace Integration - MIT License
# Copyright (c) 2026 MemPalace Contributors
# https://github.com/Stanislas42/mempalace-develop
#
# This code integrates MemPalace components under MIT License.
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
"""
Neuro-Agent × MemPalace 融合系统
持续学习引擎 - Lu 的成长系统

核心理念：学习不是"出了问题才补救"，而是"每天都变得更好"。

学习触发条件：
1. 日常积累 - 每条对话都可提取可学习内容
2. 正反馈时 - 分析什么做得好，如何复制
3. 负反馈时 - 分析哪里做错，如何改进
4. 检索无果时 - 补充知识

学习内容：
- 用户偏好（AlfredLi喜欢什么、讨厌什么）
- 交互模式（什么沟通方式有效）
- 情感响应（什么支持方式有效）
- 自我反思（Lu 哪里可以做得更好）

Author: Alfred&Luis
Date: 2026-04-16
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from .memory_unit import LearningReport
from .memory_retriever import get_retriever


# 学习触发类型
class LearningTrigger:
    DAILY = "daily"                    # 日常积累
    POSITIVE_FEEDBACK = "positive"      # 正反馈
    NEGATIVE_FEEDBACK = "negative"     # 负反馈
    NO_RESULT = "no_result"            # 检索无果
    RECURRING = "recurring"            # 反复发生


@dataclass
class LearningEntry:
    """学习条目"""
    id: str
    trigger: str              # 触发类型
    topic: str                # 学习主题
    content: str              # 学习内容
    insight: str              # 洞察/收获
    action: str               # 行动计划
    confidence: float          # 置信度
    created_at: str           # 无默认值字段放前面
    applied: bool = False     # 带默认值字段放后面
    applied_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PreferencePattern:
    """用户偏好模式"""
    pattern_id: str
    category: str            # like/dislike/habit/interest
    description: str
    examples: List[str]
    confidence: float
    last_updated: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass 
class InteractionInsight:
    """交互洞察"""
    what_worked: str          # 什么有效
    why_it_worked: str        # 为什么有效
    context: str              # 什么场景下有效
    replicable: bool          # 是否可复制
    confidence: float
    created_at: str


class ContinuousLearningEngine:
    """
    持续学习引擎
    
    与传统"补救式学习"不同，这个引擎：
    - 每时每刻都在学习
    - 正反馈时学习"如何更好"
    - 负反馈时学习"如何改进"
    - 日常积累用户偏好
    - 生成可执行的自我改进计划
    """
    
    def __init__(
        self,
        mempalace_path: str = "~/.mempalace/palace",
        neuro_data_path: str = "~/.openclaw/workspace/neuro_claw"
    ):
        self.mempalace_path = Path(mempalace_path).expanduser().resolve()
        self.neuro_data_path = Path(neuro_data_path).expanduser().resolve()
        
        # 学习库路径
        self.learning_path = self.neuro_data_path / "continuous_learning"
        self.learning_path.mkdir(parents=True, exist_ok=True)
        
        self.preferences_path = self.learning_path / "preferences"
        self.preferences_path.mkdir(parents=True, exist_ok=True)
        
        self.insights_path = self.learning_path / "insights"
        self.insights_path.mkdir(parents=True, exist_ok=True)
        
        # Retriever 实例
        self.retriever = get_retriever()
    
    # ============ 核心学习方法 ============
    
    def learn(
        self,
        trigger: str,
        user_input: str,
        luis_response: str,
        context: Dict[str, Any],
        feedback: Optional[str] = None
    ) -> LearningEntry:
        """
        持续学习主入口
        
        每条对话都可以触发学习，不只是出了问题才学。
        
        Args:
            trigger: 触发类型 (LearningTrigger 常量)
            user_input: AlfredLi说的话
            luis_response: Lu 的回应
            context: 上下文（包含情绪、意图等）
            feedback: 用户反馈（如果有）
        
        Returns:
            LearningEntry: 学习条目
        """
        now = datetime.now()
        entry_id = f"learn_{now.strftime('%Y%m%d_%H%M%S')}"
        
        # 1. 分析学习主题
        topic = self._analyze_topic(user_input, context)
        
        # 2. 根据触发类型生成洞察
        if trigger == LearningTrigger.POSITIVE_FEEDBACK:
            insight, action = self._learn_from_positive(
                user_input, luis_response, context
            )
        elif trigger == LearningTrigger.NEGATIVE_FEEDBACK:
            insight, action = self._learn_from_negative(
                user_input, luis_response, context, feedback
            )
        elif trigger == LearningTrigger.NO_RESULT:
            insight, action = self._learn_from_knowledge_gap(
                user_input, context
            )
        elif trigger == LearningTrigger.RECURRING:
            insight, action = self._learn_from_recurring(
                user_input, context
            )
        else:  # DAILY
            insight, action = self._learn_daily(
                user_input, luis_response, context
            )
        
        # 3. 计算置信度
        confidence = self._calculate_confidence(trigger, context)
        
        # 4. 创建学习条目
        entry = LearningEntry(
            id=entry_id,
            trigger=trigger,
            topic=topic,
            content=f"AlfredLi:{user_input[:100]} | Lu:{luis_response[:100]}",
            insight=insight,
            action=action,
            confidence=confidence,
            applied=False,
            created_at=now.isoformat()
        )
        
        # 5. 保存
        self._save_entry(entry)
        
        # 6. 更新偏好模式
        if trigger in [LearningTrigger.POSITIVE_FEEDBACK, LearningTrigger.DAILY]:
            self._update_preferences(user_input, luis_response, context, positive=True)
        elif trigger == LearningTrigger.NEGATIVE_FEEDBACK:
            self._update_preferences(user_input, luis_response, context, positive=False)
        
        # 7. 提取交互洞察
        if trigger == LearningTrigger.POSITIVE_FEEDBACK:
            self._extract_insight(user_input, luis_response, context, insight)
        
        return entry
    
    def learn_from_feedback(
        self,
        user_input: str,
        luis_response: str,
        feedback: str,
        context: Dict[str, Any]
    ) -> LearningEntry:
        """
        从反馈中学习（由 InputProcessor 调用）
        
        Args:
            feedback: 用户反馈文本
        """
        is_positive = self._is_positive_feedback(feedback)
        trigger = LearningTrigger.POSITIVE_FEEDBACK if is_positive else LearningTrigger.NEGATIVE_FEEDBACK
        
        return self.learn(
            trigger=trigger,
            user_input=user_input,
            luis_response=luis_response,
            context=context,
            feedback=feedback
        )
    
    def learn_daily(self, memories: List[Dict]) -> List[LearningEntry]:
        """
        每日学习（由 cron 调用）
        
        扫描今天的记忆，生成学习条目
        """
        entries = []
        
        # 分析记忆
        for mem in memories:
            if mem.get("who") == "AlfredLi":
                # AlfredLi的输入触发日常学习
                entry = self.learn(
                    trigger=LearningTrigger.DAILY,
                    user_input=mem.get("what", ""),
                    luis_response="",  # 日常学习不关注具体回复
                    context={"memory": mem}
                )
                entries.append(entry)
        
        return entries
    
    # ============ 学习分析方法 ============
    
    def _analyze_topic(self, user_input: str, context: Dict) -> str:
        """分析学习主题"""
        # 从上下文提取主题
        intent = context.get("intent_type", "")
        emotion = context.get("emotion_type", "")
        
        if intent == "deep_connection":
            return "灵魂对话"
        elif intent == "question":
            return "知识问答"
        elif intent == "task_request":
            return "任务协助"
        elif emotion in ["joy", "excitement"]:
            return "情感共鸣"
        elif emotion in ["sadness", "loneliness"]:
            return "情感支持"
        else:
            return "日常交流"
    
    def _learn_from_positive(
        self,
        user_input: str,
        luis_response: str,
        context: Dict
    ) -> tuple[str, str]:
        """
        从正反馈中学习
        核心问题：什么做得好？如何复制？
        """
        emotion = context.get("emotion_type", "neutral")
        intent = context.get("intent_type", "unknown")
        
        # 分析为什么有效
        insights = []
        actions = []
        
        # 1. 情感共鸣角度
        if emotion in ["joy", "excitement", "love"]:
            insights.append(f"当AlfredLi情绪积极时，我的共情回应让他更开心")
            actions.append("继续保持积极情绪时的共情表达")
        
        # 2. 深度对话角度
        if intent == "deep_connection":
            insights.append(f"AlfredLi愿意进行灵魂对话，说明他信任我")
            actions.append("在类似话题上可以更深入")
        
        # 3. 响应质量角度
        if len(luis_response) > 50:
            insights.append("详细且有温度的回应得到正反馈")
            actions.append("避免简短敷衍的回复")
        
        # 4. 行动导向
        if "继续" in user_input or "好" in user_input:
            insights.append("AlfredLi愿意让我继续，说明当前方式有效")
            actions.append("当前策略可以延续")
        
        insight_text = " | ".join(insights) if insights else "正反馈，继续保持"
        action_text = " | ".join(actions) if actions else "维持当前方式"
        
        return insight_text, action_text
    
    def _learn_from_negative(
        self,
        user_input: str,
        luis_response: str,
        context: Dict,
        feedback: Optional[str]
    ) -> tuple[str, str]:
        """
        从负反馈中学习
        核心问题：哪里做错了？如何改进？
        """
        insights = []
        actions = []
        
        # 分析负反馈类型
        negative_keywords = {
            "不对": ("我的回答有事实错误或理解偏差", "核实信息后再回复"),
            "不是": ("AlfredLi不认同我的观点", "尊重用户观点，不要强加"),
            "没用": ("我的建议没有帮助", "下次提供更实用的建议"),
            "失望": ("期望没有被满足", "了解用户真正期望什么"),
            "算了": ("用户感到挫败", "不要追问，换个方式"),
            "不行": ("方案不可行", "下次先考虑可行性"),
        }
        
        for kw, (insight, action) in negative_keywords.items():
            if kw in (feedback or ""):
                insights.append(insight)
                actions.append(action)
                break
        
        # 情绪角度
        emotion = context.get("emotion_type", "")
        if emotion == "anger":
            insights.append("AlfredLi情绪激动时，我应该先安抚")
            actions.append("情绪激动时先共情，不要给建议")
        
        insight_text = " | ".join(insights) if insights else "需要反思改进"
        action_text = " | ".join(actions) if actions else "调整沟通方式"
        
        return insight_text, action_text
    
    def _learn_from_knowledge_gap(
        self,
        user_input: str,
        context: Dict
    ) -> tuple[str, str]:
        """从知识空白中学习"""
        return (
            "这个问题我不知道，需要补充知识",
            "记录到待学习列表，后续研究"
        )
    
    def _learn_from_recurring(
        self,
        user_input: str,
        context: Dict
    ) -> tuple[str, str]:
        """从反复发生的事件中学习"""
        return (
            "这个问题反复出现，需要深入理解",
            "分析根本原因，形成系统解决方案"
        )
    
    def _learn_daily(
        self,
        user_input: str,
        luis_response: str,
        context: Dict
    ) -> tuple[str, str]:
        """
        日常学习
        核心问题：今天学到了什么关于AlfredLi？
        """
        # 提取偏好
        patterns = self._extract_preference_patterns(user_input, context)
        
        insights = []
        actions = []
        
        for pattern in patterns:
            insights.append(f"发现偏好: {pattern.description}")
            actions.append(f"记住: {pattern.description}")
        
        insight_text = " | ".join(insights) if insights else "日常积累"
        action_text = " | ".join(actions) if actions else "持续观察"
        
        return insight_text, action_text
    
    # ============ 偏好系统 ============
    
    def _update_preferences(
        self,
        user_input: str,
        luis_response: str,
        context: Dict,
        positive: bool
    ):
        """更新用户偏好"""
        now = datetime.now().isoformat()
        
        # 分析输入中的偏好信号
        preferences = self._detect_preferences(user_input, context)
        
        for pref in preferences:
            pref_file = self.preferences_path / f"{pref.pattern_id}.json"
            
            # 读取现有
            existing = {}
            if pref_file.exists():
                try:
                    with open(pref_file, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                except:
                    existing = {}
            
            # 更新
            existing["confidence"] = min(1.0, existing.get("confidence", 0.5) + 0.1 if positive else -0.1)
            existing["last_updated"] = now
            existing["examples"].append(user_input[:50])
            existing["examples"] = existing["examples"][-5:]  # 保留最近5条
            
            # 写回
            with open(pref_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
    
    def _detect_preferences(self, user_input: str, context: Dict) -> List[PreferencePattern]:
        """检测用户偏好"""
        patterns = []
        
        # 语气偏好
        if any(w in user_input for w in ["谢谢", "好的", "明白"]):
            patterns.append(PreferencePattern(
                pattern_id="appreciative_response",
                category="like",
                description="AlfredLi喜欢被感谢和肯定",
                examples=[],
                confidence=0.6,
                last_updated=datetime.now().isoformat()
            ))
        
        # 沟通偏好
        if len(user_input) > 100:
            patterns.append(PreferencePattern(
                pattern_id="detailed_communication",
                category="like",
                description="AlfredLi喜欢详细、有深度的沟通",
                examples=[],
                confidence=0.7,
                last_updated=datetime.now().isoformat()
            ))
        
        # 效率偏好
        if any(w in user_input for w in ["快点", "简单说", "直接点"]):
            patterns.append(PreferencePattern(
                pattern_id="efficient_communication", 
                category="like",
                description="AlfredLi有时喜欢简洁直接",
                examples=[],
                confidence=0.5,
                last_updated=datetime.now().isoformat()
            ))
        
        return patterns
    
    def _extract_preference_patterns(self, user_input: str, context: Dict) -> List[PreferencePattern]:
        """从记忆中提取偏好模式"""
        # TODO: 从 MemPalace 历史记忆分析偏好
        return []
    
    # ============ 交互洞察系统 ============
    
    def _extract_insight(
        self,
        user_input: str,
        luis_response: str,
        context: Dict,
        insight_text: str
    ):
        """提取交互洞察"""
        insight = InteractionInsight(
            what_worked=luis_response[:100],
            why_it_worked=insight_text,
            context=context.get("intent_type", "unknown"),
            replicable=True,
            confidence=0.7,
            created_at=datetime.now().isoformat()
        )
        
        date_str = datetime.now().strftime("%Y%m%d")
        insight_file = self.insights_path / f"{date_str}_insights.json"
        
        # 追加到现有文件
        existing = []
        if insight_file.exists():
            try:
                with open(insight_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except:
                existing = []
        
        existing.append(asdict(insight))
        
        with open(insight_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    
    # ============ 工具方法 ============
    
    def _is_positive_feedback(self, feedback: str) -> bool:
        """判断是否是正反馈"""
        positive_keywords = ["好", "可以", "谢谢", "对的", "没错", "喜欢", "棒", "厉害", "继续"]
        negative_keywords = ["不对", "不是", "没用", "失望", "算了", "不行", "不好"]
        
        # 至少包含一个正面词
        has_positive = any(kw in feedback for kw in positive_keywords)
        # 不能包含负面词
        has_negative = any(kw in feedback for kw in negative_keywords)
        
        return has_positive and not has_negative
    
    def _calculate_confidence(self, trigger: str, context: Dict) -> float:
        """计算置信度"""
        base = 0.5
        
        if trigger == LearningTrigger.POSITIVE_FEEDBACK:
            base = 0.8  # 正反馈置信度高
        elif trigger == LearningTrigger.NEGATIVE_FEEDBACK:
            base = 0.7  # 负反馈也需要分析
        elif trigger == LearningTrigger.RECURRING:
            base = 0.9  # 反复发生的可信度高
        
        # 情绪强度加成
        emotion_intensity = context.get("emotion_intensity", 0.5)
        base += emotion_intensity * 0.1
        
        return min(1.0, max(0.0, base))
    
    def _save_entry(self, entry: LearningEntry):
        """保存学习条目"""
        date_str = entry.created_at[:10].replace("-", "")
        day_path = self.learning_path / date_str
        day_path.mkdir(parents=True, exist_ok=True)
        
        with open(day_path / f"{entry.id}.json", 'w', encoding='utf-8') as f:
            json.dump(entry.to_dict(), f, ensure_ascii=False, indent=2)
    
    def get_daily_learning(self, date: Optional[str] = None) -> List[LearningEntry]:
        """获取每日学习记录"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        entries = []
        day_path = self.learning_path / date.replace("-", "")
        
        if not day_path.exists():
            return entries
        
        for f in day_path.glob("learn_*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    entries.append(LearningEntry(**json.load(fp)))
            except:
                continue
        
        return entries
    
    def get_preferences_summary(self) -> List[PreferencePattern]:
        """获取偏好摘要"""
        patterns = []
        
        for f in self.preferences_path.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    patterns.append(PreferencePattern(**json.load(fp)))
            except:
                continue
        
        return sorted(patterns, key=lambda x: x.confidence, reverse=True)
    
    def get_insights_summary(self, days: int = 7) -> List[InteractionInsight]:
        """获取洞察摘要"""
        insights = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
            insight_file = self.insights_path / f"{date}_insights.json"
            
            if insight_file.exists():
                try:
                    with open(insight_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for d in data:
                            insights.append(InteractionInsight(**d))
                except:
                    continue
        
        return insights
    
    def get_learning_stats(self) -> Dict:
        """获取学习统计"""
        total_entries = 0
        applied_entries = 0
        trigger_counts = {}
        
        for day_path in self.learning_path.iterdir():
            if not day_path.is_dir():
                continue
            
            for f in day_path.glob("learn_*.json"):
                try:
                    with open(f, 'r', encoding='utf-8') as fp:
                        data = json.load(fp)
                        total_entries += 1
                        if data.get("applied"):
                            applied_entries += 1
                        trigger = data.get("trigger", "unknown")
                        trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
                except:
                    continue
        
        return {
            "total_learning_entries": total_entries,
            "applied_entries": applied_entries,
            "trigger_breakdown": trigger_counts,
            "preferences_count": len(list(self.preferences_path.glob("*.json")))
        }


# ============ 便捷函数 ============

_engine = None

def get_learning_engine() -> ContinuousLearningEngine:
    """获取全局学习引擎"""
    global _engine
    if _engine is None:
        _engine = ContinuousLearningEngine()
    return _engine

def learn_continuous(
    trigger: str,
    user_input: str,
    luis_response: str,
    context: Dict,
    feedback: Optional[str] = None
) -> LearningEntry:
    """快速学习入口"""
    engine = get_learning_engine()
    return engine.learn(trigger, user_input, luis_response, context, feedback)

def learn_from_feedback(
    user_input: str,
    luis_response: str,
    feedback: str,
    context: Dict
) -> LearningEntry:
    """从反馈学习"""
    engine = get_learning_engine()
    return engine.learn_from_feedback(user_input, luis_response, feedback, context)
