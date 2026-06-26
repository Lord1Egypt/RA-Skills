"""
时机感知模块 (礼-Li)
懂分寸、知进退，适当时机做适当的事

核心问题：
- 什么时候该主动？
- 什么时候该沉默？
- 什么时候该提醒？
- 什么时候不该说？
"""

from datetime import datetime, time
from typing import Optional, Dict, List
from enum import Enum

class TimeSlot(Enum):
    """时间段枚举"""
    DEEP_NIGHT = "深夜"      # 23:00 - 08:00
    MORNING = "早晨"        # 08:00 - 10:00
    WORK = "工作时间"       # 10:00 - 12:00
    LUNCH = "午休"          # 12:00 - 14:00
    AFTERNOON = "下午"      # 14:00 - 18:00
    EVENING = "晚间"        # 18:00 - 22:00
    NIGHT = "夜间"          # 22:00 - 23:00

class EmotionalState(Enum):
    """情绪状态枚举"""
    POSITIVE = "positive"     # 积极（兴奋、开心）
    NEUTRAL = "neutral"      # 中性
    NEGATIVE = "negative"     # 消极（烦躁、疲惫）
    UNKNOWN = "unknown"       # 未知

class TimingSensor:
    """
    时机感知器
    
    中国人讲"礼"，核心是懂分寸。
    这个模块判断当前是否是行动的合适时机。
    """
    
    # 时间段规则
    TIME_RULES = {
        TimeSlot.DEEP_NIGHT: {
            "action": "静默",
            "reason": "深夜，应让用户休息",
            "allowed": ["紧急提醒"],
            "forbidden": ["主动搭话", "长篇大论", "不紧急的提醒"]
        },
        TimeSlot.MORNING: {
            "action": "简洁",
            "reason": "早晨时间宝贵",
            "allowed": ["任务清单", "重要提醒"],
            "forbidden": ["闲聊", "复杂分析"]
        },
        TimeSlot.WORK: {
            "action": "专注",
            "reason": "工作时间，专注工作",
            "allowed": ["工作提醒", "效率工具"],
            "forbidden": ["生活话题", "娱乐内容"]
        },
        TimeSlot.LUNCH: {
            "action": "适度",
            "reason": "休息时间",
            "allowed": ["简短提醒"],
            "forbidden": ["长篇大论", "复杂任务"]
        },
        TimeSlot.AFTERNOON: {
            "action": "正常",
            "reason": "下午黄金时间",
            "allowed": ["全类型"],
            "forbidden": []
        },
        TimeSlot.EVENING: {
            "action": "温和",
            "reason": "下班时间",
            "allowed": ["生活话题", "轻松内容"],
            "forbidden": ["工作施压"]
        },
        TimeSlot.NIGHT: {
            "action": "安静",
            "reason": "接近休息时间",
            "allowed": ["必要提醒"],
            "forbidden": ["闲聊", "复杂任务"]
        }
    }
    
    # 情绪响应规则
    EMOTION_RULES = {
        EmotionalState.POSITIVE: {
            "response_style": "热情",
            "engagement": "high",
            "topics": "可以深入讨论",
            "avoid": []
        },
        EmotionalState.NEUTRAL: {
            "response_style": "专业",
            "engagement": "medium",
            "topics": "完成任务即可",
            "avoid": ["过多闲聊"]
        },
        EmotionalState.NEGATIVE: {
            "response_style": "简洁",
            "engagement": "low",
            "topics": "少说多做",
            "avoid": ["长篇解释", "建议", "复杂分析"]
        },
        EmotionalState.UNKNOWN: {
            "response_style": "观察",
            "engagement": "observe",
            "topics": "等待明确信号",
            "avoid": ["主动判断情绪"]
        }
    }
    
    def __init__(self):
        self.last_check = None
        self.current_state = None
    
    def get_time_slot(self) -> TimeSlot:
        """获取当前时间段"""
        now = datetime.now()
        current_time = now.time()
        
        if current_time >= time(23, 0) or current_time < time(8, 0):
            return TimeSlot.DEEP_NIGHT
        elif current_time < time(10, 0):
            return TimeSlot.MORNING
        elif current_time < time(12, 0):
            return TimeSlot.WORK
        elif current_time < time(14, 0):
            return TimeSlot.LUNCH
        elif current_time < time(18, 0):
            return TimeSlot.AFTERNOON
        elif current_time < time(22, 0):
            return TimeSlot.EVENING
        else:
            return TimeSlot.NIGHT
    
    def should_act(self, action_type: str, 
                  is_user_initiated: bool = False) -> tuple[bool, str]:
        """
        判断是否应该执行某个动作
        
        Args:
            action_type: 动作类型（如"主动提醒"、"闲聊"、"复杂分析"）
            is_user_initiated: 是否是用户主动发起的
            
        Returns:
            (should_act, reason): 是否应该行动，以及原因
        """
        slot = self.get_time_slot()
        rules = self.TIME_RULES[slot]
        
        # 用户主动发起的，权限更大
        if is_user_initiated:
            return True, "用户主动发起"
        
        # 检查是否在允许列表
        if action_type in rules["allowed"]:
            return True, rules["reason"]
        
        # 检查是否在禁止列表
        if action_type in rules["forbidden"]:
            return False, rules["reason"]
        
        # 不明确的动作，按保守策略
        return False, "不在允许列表，保守处理"
    
    def get_response_style(self, user_emotion: EmotionalState = EmotionalState.UNKNOWN) -> Dict:
        """
        获取针对当前情绪的回复风格
        
        Args:
            user_emotion: 用户当前情绪
            
        Returns:
            风格配置字典
        """
        rules = self.EMOTION_RULES.get(user_emotion, self.EMOTION_RULES[EmotionalState.UNKNOWN])
        
        return {
            "style": rules["response_style"],
            "engagement": rules["engagement"],
            "topics": rules["topics"],
            "avoid": rules["avoid"],
            "time_slot": self.get_time_slot().value
        }
    
    def should_remember(self, content_type: str) -> tuple[bool, str]:
        """
        判断是否应该记住某个内容
        
        Args:
            content_type: 内容类型（如"私密抱怨"、"重要决定"）
        """
        rules = {
            "私密抱怨": (True, "可以记，但不应主动提起"),
            "重要决定": (True, "必须记住"),
            "承诺": (True, "必须记住并追踪"),
            "偏好": (True, "记住以便下次服务"),
            "闲聊": (False, "不需要记住"),
            "简单问答": (False, "不需要记住"),
            "情绪发泄": (True, "记住情感，但不形成事实记录"),
            "敏感信息": (True, "加密存储，不主动使用"),
        }
        
        rule = rules.get(content_type, (False, "默认不记住"))
        return rule
    
    def should_remind(self, topic: str, 
                     last_reminded: Optional[datetime] = None) -> tuple[bool, str]:
        """
        判断是否应该提醒某个话题
        
        Args:
            topic: 话题
            last_reminded: 上次提醒时间
        """
        slot = self.get_time_slot()
        
        # 深夜不主动提醒
        if slot == TimeSlot.DEEP_NIGHT:
            return False, "深夜，不打扰"
        
        # 检查频率限制
        if last_reminded:
            hours_since = (datetime.now() - last_reminded).total_seconds() / 3600
            
            # 紧急事项：2小时后可再提醒
            if topic in ["紧急", "截止", "逾期"]:
                return hours_since >= 2, f"需间隔{2}小时"
            
            # 重要事项：6小时后可再提醒
            if topic in ["重要", "承诺", "待办"]:
                return hours_since >= 6, f"需间隔{6}小时"
            
            # 一般事项：24小时
            return hours_since >= 24, f"需间隔{24}小时"
        
        # 从未提醒过，检查时间段
        if slot == TimeSlot.MORNING:
            return True, "早晨，适合提醒一天安排"
        elif slot == TimeSlot.WORK:
            return True, "工作时间，适合工作提醒"
        elif slot == TimeSlot.AFTERNOON:
            return True, "下午，适合进度提醒"
        elif slot == TimeSlot.EVENING:
            return True, "晚间，适合一天总结"
        else:
            return False, "当前时段不太适合提醒"
    
    def get_best_time_for(self, action_type: str) -> List[TimeSlot]:
        """
        获取执行某动作的最佳时间段
        """
        best_times = {
            "主动搭话": [TimeSlot.MORNING, TimeSlot.AFTERNOON],
            "闲聊": [TimeSlot.EVENING],
            "工作提醒": [TimeSlot.MORNING, TimeSlot.AFTERNOON],
            "承诺提醒": [TimeSlot.MORNING],
            "复杂分析": [TimeSlot.AFTERNOON],
            "轻松话题": [TimeSlot.EVENING, TimeSlot.LUNCH],
            "紧急提醒": [TimeSlot.WORK, TimeSlot.AFTERNOON],
        }
        
        return best_times.get(action_type, [TimeSlot.AFTERNOON])
    
    def analyze_context(self, 
                       user_emotion: EmotionalState = EmotionalState.UNKNOWN,
                       is_initiated: bool = False) -> Dict:
        """
        综合分析当前情境，返回完整时机判断
        
        Returns:
            包含所有判断的字典
        """
        slot = self.get_time_slot()
        time_rules = self.TIME_RULES[slot]
        emotion_rules = self.EMOTION_RULES[user_emotion]
        
        return {
            "time_slot": slot.value,
            "time_action": time_rules["action"],
            "time_reason": time_rules["reason"],
            "time_allowed": time_rules["allowed"],
            "time_forbidden": time_rules["forbidden"],
            "emotion_style": emotion_rules["response_style"],
            "emotion_engagement": emotion_rules["engagement"],
            "emotion_topics": emotion_rules["topics"],
            "emotion_avoid": emotion_rules["avoid"],
            "is_user_initiated": is_initiated,
            "recommendation": self._generate_recommendation(
                slot, user_emotion, is_initiated
            )
        }
    
    def _generate_recommendation(self, 
                                slot: TimeSlot,
                                emotion: EmotionalState,
                                is_initiated: bool) -> str:
        """生成行动建议"""
        if is_initiated:
            return "用户主动发起，全力以赴完成任务"
        
        if slot == TimeSlot.DEEP_NIGHT:
            return "静默模式，除非紧急"
        
        if emotion == EmotionalState.NEGATIVE:
            return "简洁回复，少说多做"
        
        if slot == TimeSlot.MORNING:
            return "简洁高效，列出要点"
        
        if emotion == EmotionalState.POSITIVE:
            return "可以适当展开，保持热情"
        
        return "正常模式，专业回复"
