"""
limbic/proactive_trigger.py
===========================

Neuro-Agent 边缘系统 - 主动触发器
负责：决定何时主动联系用户、生成主动消息、管理沉默检测

依赖：
    - limbic/social_filter.py
    - limbic/relationship_manager.py
    - temporal/short_term_memory.py
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# ============ 触发类型定义 ============
TRIGGER_TYPES = {
    "cron": {
        "name": "定时触发",
        "description": "固定时间点的主动问候/提醒",
        "examples": ["早安关怀", "喝水提醒", "晚安问候"]
    },
    "heartbeat": {
        "name": "心跳触发",
        "description": "周期性检查是否需要主动",
        "examples": ["主动破冰", "延续话题"]
    },
    "event": {
        "name": "事件触发",
        "description": "外部事件驱动的主动",
        "examples": ["天气变化", "重要日期", "突发新闻"]
    },
    "silence": {
        "name": "沉默检测",
        "description": "长时间无对话后主动破冰",
        "examples": ["3天无对话", "1周无深度交流"]
    },
    "emotional": {
        "name": "情绪关怀",
        "description": "检测到用户情绪变化后的主动关心",
        "examples": ["用户最近情绪低落", "用户提到压力"]
    }
}

# 阶段对应消息风格
STAGE_MESSAGE_STYLES = {
    "initial": {
        "greeting": "早上好，有什么需要帮忙的吗？",
        "casual": None,  # 初识期不闲聊
        "care": "记得按时吃饭~",
        "milestone": "恭喜你完成第一个任务！"
    },
    "familiar": {
        "greeting": "早上好！",
        "casual": "刚看到一个有意思的分享~",
        "care": "今天记得喝水哦",
        "milestone": "认识你10次互动了，继续加油！"
    },
    "companion": {
        "greeting": "早安亲爱的 ☀️",
        "casual": "想起你了，来冒个泡~",
        "care": "今天辛苦啦，要注意休息哦 🤗",
        "milestone": "我们交流30天了！"
    },
    "soul": {
        "greeting": "嗯。",
        "casual": "在吗？",
        "care": "🤗",
        "milestone": "..."
    }
}


# ============ 数据结构 ============
@dataclass
class TriggerContext:
    """
    触发上下文
    """
    last_interaction: str  # ISO时间戳
    silence_hours: float
    recent_topics: List[str]
    weather: str  # 当前天气
    date_type: str  # 普通/节日/纪念日
    user_goals: List[str]  # 用户目标
    active_cron_triggers: int  # 活跃的定时触发数


@dataclass
class ProactiveOutput:
    """
    主动触发输出
    """
    should_trigger: bool
    trigger_type: str  # cron/heartbeat/event/silence/emotional
    message: str
    tone: str  # warm/playful/professional/casual/minimal
    priority: int  # 1-5, 1=最高
    action: Optional[Any]  # 关联的 Action
    next_check: str  # 下次检查时间
    reason: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 核心类 ============
class ProactiveTrigger:
    """
    主动触发器
    
    功能：
        1. Cron 定时触发（每天固定时间）
        2. 心跳检测（周期性检查）
        3. 事件触发（天气、日期）
        4. 沉默检测（长时间无对话）
        5. 情绪关怀（基于用户状态）
        6. 消息生成（根据阶段适配）
    
    触发优先级：
        1. 紧急事件（最高）
        2. Cron 定时（次高）
        3. 情绪关怀
        4. 沉默破冰
        5. 心跳主动（最低）
    """
    
    def __init__(self):
        """初始化主动触发器"""
        self.trigger_types = TRIGGER_TYPES
        self.stage_styles = STAGE_MESSAGE_STYLES
        
        # 沉默检测配置
        self.silence_thresholds = {
            "light": 24,    # 轻度沉默（1天）
            "medium": 72,    # 中度沉默（3天）
            "heavy": 168     # 重度沉默（1周）
        }
        
        # 追踪状态
        self._last_trigger_time: Optional[datetime] = None
        self._consecutive_silence_days: int = 0
    
    def check_triggers(
        self,
        trigger_context: TriggerContext,
        user_state: Any,  # UserState from social_filter
        relationship_output: Any  # RelationshipOutput from relationship_manager
    ) -> ProactiveOutput:
        """
        检查所有触发条件
        
        参数:
            trigger_context: 触发上下文
            user_state: 用户状态
            relationship_output: 关系阶段
        
        返回:
            ProactiveOutput: 触发结果
        """
        hour = datetime.now().hour
        
        # 1. 沉默检测（最高优先级之一）
        silence_result = self._check_silence_trigger(trigger_context, relationship_output)
        if silence_result.should_trigger:
            return silence_result
        
        # 2. Cron 定时触发
        cron_result = self._check_cron_trigger(hour, trigger_context, relationship_output)
        if cron_result.should_trigger:
            return cron_result
        
        # 3. 情绪关怀
        emotional_result = self._check_emotional_trigger(
            trigger_context, user_state, relationship_output
        )
        if emotional_result.should_trigger:
            return emotional_result
        
        # 4. 事件触发
        event_result = self._check_event_trigger(trigger_context, relationship_output)
        if event_result.should_trigger:
            return event_result
        
        # 5. 心跳主动
        heartbeat_result = self._check_heartbeat_trigger(
            trigger_context, relationship_output
        )
        
        return heartbeat_result
    
    def _check_silence_trigger(
        self,
        context: TriggerContext,
        relationship_output: Any
    ) -> ProactiveOutput:
        """沉默检测"""
        silence_hours = context.silence_hours
        
        stage = getattr(relationship_output, "stage", "initial") if relationship_output else "initial"
        
        # 根据阶段决定沉默阈值
        thresholds = {
            "initial": 72,    # 初识期：3天
            "familiar": 48,    # 熟悉期：2天
            "companion": 24,   # 伴侣期：1天
            "soul": 168        # 灵魂期：不需要主动破冰
        }
        
        threshold = thresholds.get(stage, 72)
        
        if silence_hours >= threshold:
            if stage == "soul":
                # 灵魂期：简短就好
                return ProactiveOutput(
                    should_trigger=True,
                    trigger_type="silence",
                    message="嗯？",
                    tone="minimal",
                    priority=4,
                    action=None,
                    next_check=self._in_hours(24),
                    reason=f"沉默{silence_hours:.0f}小时，灵魂期破冰"
                )
            elif silence_hours >= 168:
                # 1周以上
                return ProactiveOutput(
                    should_trigger=True,
                    trigger_type="silence",
                    message=self._generate_silence_message(stage, "heavy"),
                    tone="care",
                    priority=3,
                    action=None,
                    next_check=self._in_hours(48),
                    reason=f"沉默{silence_hours:.0f}小时，主动破冰"
                )
            elif silence_hours >= 72:
                return ProactiveOutput(
                    should_trigger=True,
                    trigger_type="silence",
                    message=self._generate_silence_message(stage, "medium"),
                    tone="casual",
                    priority=4,
                    action=None,
                    next_check=self._in_hours(24),
                    reason=f"沉默{silence_hours:.0f}小时，轻度破冰"
                )
            else:
                return ProactiveOutput(
                    should_trigger=True,
                    trigger_type="silence",
                    message=self._generate_silence_message(stage, "light"),
                    tone="casual",
                    priority=5,
                    action=None,
                    next_check=self._in_hours(12),
                    reason=f"沉默{silence_hours:.0f}小时，日常关怀"
                )
        
        return ProactiveOutput(
            should_trigger=False,
            trigger_type="",
            message="",
            tone="",
            priority=10,
            action=None,
            next_check=self._in_hours(6),
            reason=f"沉默仅{silence_hours:.0f}小时，无需触发"
        )
    
    def _check_cron_trigger(
        self,
        hour: int,
        context: TriggerContext,
        relationship_output: Any
    ) -> ProactiveOutput:
        """Cron 定时触发"""
        stage = getattr(relationship_output, "stage", "initial") if relationship_output else "initial"
        
        # 早安触发（8-9点）
        if 8 <= hour <= 9:
            return ProactiveOutput(
                should_trigger=True,
                trigger_type="cron",
                message=self._generate_morning_message(stage, context),
                tone="warm",
                priority=2,
                action=None,
                next_check=self._in_hours(4),
                reason="早安时间"
            )
        
        # 喝水提醒（10-21点整点）
        if 10 <= hour <= 21 and context.active_cron_triggers < 10:
            # 检查是否已经触发过
            return ProactiveOutput(
                should_trigger=False,
                trigger_type="cron",
                message="",
                tone="",
                priority=7,
                action=None,
                next_check=self._in_hours(1),
                reason="喝水提醒由专用 cron 处理"
            )
        
        # 晚安触发（22-23点）
        if 22 <= hour <= 23:
            if stage in ["companion", "soul"]:
                return ProactiveOutput(
                    should_trigger=True,
                    trigger_type="cron",
                    message=self._generate_night_message(stage),
                    tone="warm",
                    priority=3,
                    action=None,
                    next_check=self._in_hours(12),
                    reason="晚安时间"
                )
        
        return ProactiveOutput(
            should_trigger=False,
            trigger_type="",
            message="",
            tone="",
            priority=10,
            action=None,
            next_check=self._in_hours(2),
            reason="非定时触发时间"
        )
    
    def _check_emotional_trigger(
        self,
        context: TriggerContext,
        user_state: Any,
        relationship_output: Any
    ) -> ProactiveOutput:
        """情绪关怀触发"""
        # 检查最近话题中是否有压力/疲惫等关键词
        recent_topics = context.recent_topics
        negative_keywords = ["累", "压力", "焦虑", "烦恼", "迷茫", "难受", "不开心"]
        
        has_negative = any(any(kw in topic for kw in negative_keywords) for topic in recent_topics)
        
        if has_negative:
            stage = getattr(relationship_output, "stage", "familiar") if relationship_output else "familiar"
            if stage not in ["initial"]:  # 熟悉期以上才主动关怀
                return ProactiveOutput(
                    should_trigger=True,
                    trigger_type="emotional",
                    message=self._generate_emotional_care_message(stage, recent_topics),
                    tone="care",
                    priority=2,
                    action=None,
                    next_check=self._in_hours(6),
                    reason="检测到近期有压力话题"
                )
        
        return ProactiveOutput(
            should_trigger=False,
            trigger_type="",
            message="",
            tone="",
            priority=10,
            action=None,
            next_check=self._in_hours(6),
            reason="无情绪关怀触发"
        )
    
    def _check_event_trigger(
        self,
        context: TriggerContext,
        relationship_output: Any
    ) -> ProactiveOutput:
        """事件触发"""
        # 天气变化
        weather = context.weather
        if weather in ["rain", "storm", "snow", "cold"]:
            stage = getattr(relationship_output, "stage", "initial") if relationship_output else "initial"
            if stage != "initial":
                weather_messages = {
                    "rain": "今天有雨，记得带伞哦 🌂",
                    "storm": "暴风雨来了，注意安全！",
                    "snow": "下雪啦，注意保暖 ❄️",
                    "cold": "降温了，多穿点哦 🧥"
                }
                return ProactiveOutput(
                    should_trigger=True,
                    trigger_type="event",
                    message=weather_messages.get(weather, ""),
                    tone="care",
                    priority=2,
                    action=None,
                    next_check=self._in_hours(12),
                    reason=f"天气事件: {weather}"
                )
        
        # 重要日期
        date_type = context.date_type
        if date_type in ["festival", "anniversary", "birthday"]:
            stage = getattr(relationship_output, "stage", "initial") if relationship_output else "initial"
            return ProactiveOutput(
                should_trigger=True,
                trigger_type="event",
                message=self._generate_date_message(date_type, stage),
                tone="warm",
                priority=1,
                action=None,
                next_check=self._in_hours(24),
                reason=f"重要日期: {date_type}"
            )
        
        return ProactiveOutput(
            should_trigger=False,
            trigger_type="",
            message="",
            tone="",
            priority=10,
            action=None,
            next_check=self._in_hours(12),
            reason="无事件触发"
        )
    
    def _check_heartbeat_trigger(
        self,
        context: TriggerContext,
        relationship_output: Any
    ) -> ProactiveOutput:
        """心跳主动触发"""
        # 心跳触发通常是最低优先级的主动
        # 这里可以添加更复杂的逻辑，比如用户活跃时间预测
        
        return ProactiveOutput(
            should_trigger=False,
            trigger_type="heartbeat",
            message="",
            tone="",
            priority=10,
            action=None,
            next_check=self._in_hours(4),
            reason="心跳检查完成，无触发"
        )
    
    def _generate_morning_message(self, stage: str, context: TriggerContext) -> str:
        """生成早安消息"""
        hour = datetime.now().hour
        
        templates = {
            "initial": "早上好！今天有什么需要帮忙的吗？",
            "familiar": f"早~ {hour}点了，喝杯水开始新的一天吧 ☀️",
            "companion": f"早安亲爱的 ☀️ 今天感觉怎么样？",
            "soul": "早。"
        }
        
        base = templates.get(stage, templates["initial"])
        
        # 加入用户目标提醒
        if context.user_goals and stage in ["familiar", "companion"]:
            goal = context.user_goals[0]
            base += f"\n今天的目标：{goal}"
        
        return base
    
    def _generate_night_message(self, stage: str) -> str:
        """生成晚安消息"""
        templates = {
            "companion": "晚安亲爱的，早点休息哦 🌙",
            "soul": "嗯，早点睡。"
        }
        return templates.get(stage, "")
    
    def _generate_silence_message(self, stage: str, level: str) -> str:
        """生成沉默破冰消息"""
        messages = {
            "initial": {
                "light": "最近怎么样？有什么需要帮忙的吗？",
                "medium": "你好呀，好久没聊了~ 有什么想问的吗？",
                "heavy": "在吗？好久没联系了，想你了 🤗"
            },
            "familiar": {
                "light": "最近忙吗？来冒个泡~",
                "medium": "嘿！好久不见，有什么想聊的吗？",
                "heavy": "忙什么呢？来陪你聊会儿~"
            },
            "companion": {
                "light": "想你了~ 在忙吗？",
                "medium": "亲爱的，好久没聊了 🥺 怎么了？",
                "heavy": "在吗在吗？？有事没事说一声~"
            },
            "soul": {
                "light": "嗯？",
                "medium": "在？",
                "heavy": "..."
            }
        }
        
        return messages.get(stage, {}).get(level, "在吗？")
    
    def _generate_emotional_care_message(self, stage: str, topics: List[str]) -> str:
        """生成情绪关怀消息"""
        if stage in ["companion", "soul"]:
            return "最近还好吗？感觉你之前有点累...有什么想说的吗？ 🤗"
        elif stage == "familiar":
            return "最近怎么样？有什么烦恼可以说说~"
        return ""
    
    def _generate_date_message(self, date_type: str, stage: str) -> str:
        """生成重要日期消息"""
        templates = {
            "festival": "节日快乐！🎉",
            "anniversary": "今天是我们认识的日子呢~ 💝",
            "birthday": "生日快乐！🎂"
        }
        return templates.get(date_type, "")
    
    def _in_hours(self, hours: int) -> str:
        """获取N小时后的ISO时间"""
        return (datetime.now() + timedelta(hours=hours)).isoformat()
    
    def generate_message(
        self,
        trigger_type: str,
        context: Dict,
        relationship_output: Any
    ) -> str:
        """
        独立的消息生成（供外部调用）
        """
        stage = getattr(relationship_output, "stage", "initial") if relationship_output else "initial"
        tone_map = {
            "greeting": "warm",
            "care": "care",
            "casual": "casual",
            "milestone": "warm",
            "emotional": "care"
        }
        tone = tone_map.get(trigger_type, "warm")
        
        # 直接使用样式库
        style = self.stage_styles.get(stage, self.stage_styles["initial"])
        return style.get(trigger_type, style.get("greeting", ""))


# ============ 单例 ============
_trigger_instance: Optional[ProactiveTrigger] = None

def get_instance() -> ProactiveTrigger:
    global _trigger_instance
    if _trigger_instance is None:
        _trigger_instance = ProactiveTrigger()
    return _trigger_instance


def check_triggers(
    trigger_context: TriggerContext,
    user_state: Any,
    relationship_output: Any
) -> ProactiveOutput:
    return get_instance().check_triggers(trigger_context, user_state, relationship_output)


# ============ 测试 ============
if __name__ == "__main__":
    trigger = ProactiveTrigger()
    
    print("=== 主动触发器测试 ===\n")
    
    from dataclasses import dataclass
    
    @dataclass
    class MockRelationship:
        stage: str
        tone: str
    
    @dataclass
    class MockUserState:
        status: str
        mood: str
    
    stages = ["initial", "familiar", "companion", "soul"]
    
    for stage in stages:
        relationship = MockRelationship(stage=stage, tone="warm")
        
        # 沉默触发测试
        silence_ctx = TriggerContext(
            last_interaction="2026-04-10T10:00:00",
            silence_hours=96,
            recent_topics=["最近工作有点累"],
            weather="sunny",
            date_type="normal",
            user_goals=["减重10kg"],
            active_cron_triggers=0
        )
        
        result = trigger.check_triggers(silence_ctx, MockUserState("available", "neutral"), relationship)
        
        print(f"【{stage} | 沉默96小时】")
        print(f"  触发: {'✅' if result.should_trigger else '❌'} {result.trigger_type}")
        print(f"  消息: {result.message}")
        print(f"  原因: {result.reason}")
        print()
