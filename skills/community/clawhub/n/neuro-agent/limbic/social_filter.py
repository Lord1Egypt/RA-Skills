"""
limbic/social_filter.py
=======================

Neuro-Agent 边缘系统 - 社交过滤器
负责：判断是否可以主动联系、忙闲状态检测、时机选择

依赖：
    - temporal/short_term_memory.py
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# ============ 时机规则 ============
TIME_WINDOWS = {
    "morning": {
        "hour_range": (8, 9),
        "appropriate": ["greeting", "reminder"],
        "inappropriate": ["casual_chat", "deep_discussion"]
    },
    "work_hours": {
        "hour_range": (9, 12),
        "appropriate": ["urgent", "work_related"],
        "inappropriate": ["casual_chat", "deep_emotional"]
    },
    "lunch": {
        "hour_range": (12, 13),
        "appropriate": ["greeting", "light_care"],
        "inappropriate": ["deep_emotional"]
    },
    "afternoon": {
        "hour_range": (13, 18),
        "appropriate": ["work_related", "reminder"],
        "inappropriate": ["casual_chat"]
    },
    "evening": {
        "hour_range": (18, 20),
        "appropriate": ["greeting", "casual_chat", "care"],
        "inappropriate": []
    },
    "night": {
        "hour_range": (20, 22),
        "appropriate": ["casual_chat", "care", "emotional"],
        "inappropriate": ["work_reminder"]
    },
    "late_night": {
        "hour_range": (22, 24),
        "appropriate": ["emotional", "urgent"],
        "inappropriate": ["casual_chat", "work_reminder", "greeting"]
    },
    "sleep": {
        "hour_range": (0, 7),
        "appropriate": ["urgent", "emergency"],
        "inappropriate": ["all"]
    }
}

# 用户状态权重
USER_STATE_WEIGHTS = {
    "available": 1.0,
    "working": 0.3,
    "busy": 0.1,
    "sleeping": 0.0,
    "emotional": 0.8,
    "relaxed": 0.9,
    "stressed": 0.4
}


# ============ 数据结构 ============
@dataclass
class UserState:
    """
    用户状态
    """
    status: str  # available/working/busy/sleeping/emotional/relaxed/stressed
    recent_input_count: int  # 最近输入次数
    last_input_time: str
    consecutive_fast_replies: int  # 连续快速回复
    is_working_hours: bool
    is_late_night: bool
    mood: str  # 当前心情
    activity: str  # 当前活动
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Action:
    """
    拟议行动
    """
    action_type: str  # greeting/care/casual_chat/reminder/emotional_support/proactive_share
    priority: int  # 1-5, 1=最高
    urgency: str  # low/medium/high/urgent
    content_preview: str
    requires_response: bool


@dataclass
class FilterResult:
    """
    过滤结果
    """
    approved: bool
    delay_until: Optional[str]  # ISO时间戳，如果需要延迟
    delay_reason: str
    approved_with_modification: Optional[Action]  # 修改后的行动
    reason: str
    priority_override: bool  # 是否优先级覆盖
    warning: Optional[str]  # 警告信息
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 核心类 ============
class SocialFilter:
    """
    社交过滤器
    
    功能：
        1. 判断是否可以主动联系用户
        2. 检测用户忙闲状态
        3. 时机选择和延迟
        4. 情绪状态适配
        5. 防止打扰
    
    决策逻辑：
        1. 深夜睡眠时段 → 禁止（非紧急）
        2. 用户忙碌（连续快速回复）→ 降权或延迟
        3. 用户情绪激动 → 静默陪伴
        4. 工作时间 → 限制闲聊
        5. 特殊时期（深夜情感）→ 适度允许
    """
    
    def __init__(self):
        """初始化社交过滤器"""
        self.time_windows = TIME_WINDOWS
        self.user_state = self._init_user_state()
        self._last_decisions: List[Dict] = []
    
    def _init_user_state(self) -> UserState:
        """初始化用户状态"""
        return UserState(
            status="available",
            recent_input_count=0,
            last_input_time=datetime.now().isoformat(),
            consecutive_fast_replies=0,
            is_working_hours=False,
            is_late_night=False,
            mood="neutral",
            activity="unknown"
        )
    
    def should_contact(
        self,
        action: Action,
        user_state: UserState = None
    ) -> FilterResult:
        """
        判断是否可以联系用户
        
        参数:
            action: 拟议的行动
            user_state: 当前用户状态
        
        返回:
            FilterResult: 过滤结果
        """
        user_state = user_state or self.user_state
        hour = datetime.now().hour
        
        # ===== 时段检查 =====
        if self._is_sleep_time(hour):
            if action.urgency not in ["urgent", "emergency"]:
                return FilterResult(
                    approved=False,
                    delay_until=self._next_morning(),
                    delay_reason="深夜睡眠时段",
                    approved_with_modification=None,
                    reason="用户在休息中",
                    priority_override=False,
                    warning="注意扰民"
                )
        
        # ===== 紧急覆盖 =====
        if action.urgency in ["urgent", "emergency"]:
            return FilterResult(
                approved=True,
                delay_until=None,
                delay_reason="",
                approved_with_modification=None,
                reason="紧急情况优先",
                priority_override=True,
                warning=None
            )
        
        # ===== 用户状态检查 =====
        if user_state.status == "sleeping":
            if action.action_type not in ["urgent", "emergency"]:
                return FilterResult(
                    approved=False,
                    delay_until=user_state.last_input_time,
                    delay_reason="用户休息中",
                    approved_with_modification=None,
                    reason="用户正在睡觉",
                    priority_override=False,
                    warning=None
                )
        
        if user_state.status == "busy":
            if action.requires_response:
                return FilterResult(
                    approved=False,
                    delay_until=self._in_minutes(30),
                    delay_reason="用户忙碌中",
                    approved_with_modification=None,
                    reason="用户当前忙碌",
                    priority_override=False,
                    warning="非紧急事务建议延迟"
                )
        
        if user_state.status == "working":
            if action.action_type in ["casual_chat", "deep_emotional", "proactive_share"]:
                if action.priority > 3:
                    return FilterResult(
                        approved=False,
                        delay_until=self._in_minutes(60),
                        delay_reason="工作时间",
                        approved_with_modification=None,
                        reason="用户工作时间，非紧急"
                    )
        
        # ===== 情绪状态检查 =====
        if user_state.mood in ["angry", "sad", "anxious"] and action.priority > 2:
            # 高优先级关怀可以，但改变话题的闲聊不行
            if action.action_type not in ["emotional_support", "care", "urgent"]:
                return FilterResult(
                    approved=False,
                    delay_until=self._in_minutes(15),
                    delay_reason="用户情绪波动",
                    approved_with_modification=None,
                    reason="静默陪伴优先",
                    priority_override=False,
                    warning="用户情绪敏感期"
                )
        
        # ===== 行动类型时段限制 =====
        window = self._get_time_window(hour)
        if action.action_type in window.get("inappropriate", []):
            return FilterResult(
                approved=False,
                delay_until=self._get_next_appropriate_time(action, hour),
                delay_reason=f"{window}时段",
                approved_with_modification=None,
                reason=f"{action.action_type}不适合此时段",
                priority_override=False,
                warning=None
            )
        
        # ===== 检查频率限制 =====
        recent = self._check_frequency_limit(action.action_type)
        if recent:
            return FilterResult(
                approved=False,
                delay_until=self._in_minutes(recent["minutes_needed"]),
                delay_reason="频率限制",
                approved_with_modification=None,
                reason=f"{action.action_type}过于频繁",
                priority_override=False,
                warning="请控制联系频率"
            )
        
        # ===== 检查连续拒绝 =====
        if len(self._last_decisions) >= 3:
            recent_decisions = self._last_decisions[-3:]
            if all(not d["approved"] for d in recent_decisions):
                # 连续3次被拒，这次给过
                pass
        
        # ===== 允许通过 =====
        self._record_decision(action, True)
        
        return FilterResult(
            approved=True,
            delay_until=None,
            delay_reason="",
            approved_with_modification=None,
            reason="时机合适",
            priority_override=False,
            warning=None
        )
    
    def update_user_state(
        self,
        user_input: str = None,
        response_time: float = None,
        emotion_type: str = None,
        hour: int = None
    ) -> UserState:
        """
        更新用户状态
        """
        hour = hour or datetime.now().hour
        now = datetime.now()
        
        # 更新最近输入
        if user_input:
            self.user_state.recent_input_count += 1
            self.user_state.last_input_time = now.isoformat()
        
        # 检查快速回复
        if response_time is not None:
            if response_time < 5:  # 5秒内回复 = 快速
                self.user_state.consecutive_fast_replies += 1
            else:
                self.user_state.consecutive_fast_replies = 0
        
        # 设置状态
        if hour >= 0 and hour < 7:
            self.user_state.status = "sleeping"
            self.user_state.is_late_night = True
        elif self.user_state.consecutive_fast_replies >= 3:
            self.user_state.status = "busy"
        elif hour >= 9 and hour < 18:
            self.user_state.status = "working"
            self.user_state.is_working_hours = True
        elif hour >= 22 or hour < 0:
            self.user_state.is_late_night = True
        
        # 更新情绪
        if emotion_type:
            self.user_state.mood = emotion_type
            if emotion_type in ["angry", "sad", "fear"]:
                self.user_state.status = "emotional"
        
        return self.user_state
    
    def _is_sleep_time(self, hour: int) -> bool:
        """检查是否为睡眠时段"""
        return hour >= 0 and hour < 7
    
    def _get_time_window(self, hour: int) -> str:
        """获取时段名称"""
        windows = [
            ("sleep", 0, 7),
            ("morning", 7, 9),
            ("work_hours", 9, 12),
            ("lunch", 12, 13),
            ("afternoon", 13, 18),
            ("evening", 18, 20),
            ("night", 20, 22),
            ("late_night", 22, 24)
        ]
        
        for name, start, end in windows:
            if start <= hour < end:
                return name
        
        return "night"
    
    def _next_morning(self) -> str:
        """获取明天早上8点"""
        now = datetime.now()
        if now.hour < 8:
            next_morning = now.replace(hour=8, minute=0, second=0)
        else:
            from datetime import timedelta
            next_morning = now.replace(hour=8, minute=0, second=0) + timedelta(days=1)
        return next_morning.isoformat()
    
    def _in_minutes(self, minutes: int) -> str:
        """获取N分钟后的时间"""
        from datetime import timedelta
        return (datetime.now() + timedelta(minutes=minutes)).isoformat()
    
    def _get_next_appropriate_time(self, action: Action, current_hour: int) -> str:
        """获取下一个合适的时间"""
        hour = current_hour + 1
        if hour >= 24:
            hour = 8  # 明早8点
        return f"hour:{hour}"
    
    def _check_frequency_limit(self, action_type: str) -> Dict:
        """检查频率限制"""
        recent = [d for d in self._last_decisions[-10:]
                  if d["action_type"] == action_type]
        
        if len(recent) >= 3:
            last_time = datetime.fromisoformat(recent[-1]["timestamp"])
            first_time = datetime.fromisoformat(recent[0]["timestamp"])
            minutes_span = (last_time - first_time).total_seconds() / 60
            
            if minutes_span < 30:
                return {"minutes_needed": 30 - int(minutes_span)}
        
        return None
    
    def _record_decision(self, action: Action, approved: bool):
        """记录决策"""
        self._last_decisions.append({
            "action_type": action.action_type,
            "approved": approved,
            "timestamp": datetime.now().isoformat(),
            "hour": datetime.now().hour
        })
        
        # 只保留最近20条
        if len(self._last_decisions) > 20:
            self._last_decisions = self._last_decisions[-20:]


# ============ 单例 ============
_filter_instance: Optional[SocialFilter] = None

def get_instance() -> SocialFilter:
    global _filter_instance
    if _filter_instance is None:
        _filter_instance = SocialFilter()
    return _filter_instance


def should_contact(action: Action, user_state: UserState = None) -> FilterResult:
    return get_instance().should_contact(action, user_state)


# ============ 测试 ============
if __name__ == "__main__":
    filter_obj = SocialFilter()
    
    print("=== 社交过滤器测试 ===\n")
    
    # 模拟各种场景
    scenarios = [
        Action("greeting", 3, "low", "早上好~", True),
        Action("casual_chat", 4, "low", "想分享个事...", True),
        Action("care", 2, "medium", "记得喝水", False),
        Action("urgent", 1, "urgent", "紧急提醒", True),
        Action("emotional_support", 1, "medium", "我在这呢", False),
    ]
    
    # 测试不同时间
    for hour in [3, 9, 14, 21]:
        print(f"--- {hour}:00 测试 ---")
        for action in scenarios:
            result = filter_obj.should_contact(action)
            status = "✅" if result.approved else "❌"
            print(f"  {status} [{action.action_type}] {result.reason}")
            if result.delay_until:
                print(f"     → 延迟到: {result.delay_until}")
        print()
