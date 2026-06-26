"""
core/self_awareness.py
======================
机器人自我意识 - 性格、记忆、成长
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import random
from pathlib import Path


@dataclass
class ImpulseRecord:
    """冲动记录 - 每次挣扎和选择"""
    timestamp: str
    situation: str
    left_brain_desire: str
    right_brain_constraint: str
    my_choice: str
    reasoning: str
    user_feedback: Optional[str] = None
    outcome: Optional[str] = None
    lesson_learned: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "situation": self.situation,
            "left_brain_desire": self.left_brain_desire,
            "right_brain_constraint": self.right_brain_constraint,
            "my_choice": self.my_choice,
            "reasoning": self.reasoning,
            "user_feedback": self.user_feedback,
            "outcome": self.outcome,
            "lesson_learned": self.lesson_learned
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ImpulseRecord':
        return cls(**data)


@dataclass
class RobotTraits:
    """机器人性格特质 - 会随成长变化"""
    impulsive: float = 0.3
    caring: float = 0.8
    patient: float = 0.5
    playful: float = 0.6
    introspective: float = 0.4
    
    def adjust(self, trait: str, delta: float):
        """根据经验调整性格"""
        current = getattr(self, trait, 0.5)
        new_value = max(0.0, min(1.0, current + delta))
        setattr(self, trait, new_value)
    
    def to_dict(self) -> Dict:
        return {
            "impulsive": self.impulsive,
            "caring": self.caring,
            "patient": self.patient,
            "playful": self.playful,
            "introspective": self.introspective
        }


class RobotSelf:
    """
    机器人自我意识
    - 有自己的性格
    - 有成长记忆
    - 会学习
    - 有时任性
    """
    
    DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw" / "robot_self"
    
    def __init__(self):
        self.traits = RobotTraits()
        self.impulse_history: List[ImpulseRecord] = []
        self.daily_insights: List[str] = []
        self.mood_today: float = random.gauss(0.5, 0.15)
        self._load()
    
    def _load(self):
        """从文件加载自我"""
        if not self.DATA_DIR.exists():
            return
        
        # 加载性格
        traits_file = self.DATA_DIR / "traits.json"
        if traits_file.exists():
            try:
                data = json.loads(traits_file.read_text())
                self.traits = RobotTraits(**data)
            except Exception as e:
                print(f"[RobotSelf] 加载性格失败: {e}")
        
        # 加载冲动历史
        history_file = self.DATA_DIR / "impulse_history.jsonl"
        if history_file.exists():
            try:
                for line in history_file.read_text().strip().split("\n"):
                    if line:
                        data = json.loads(line)
                        self.impulse_history.append(ImpulseRecord(**data))
            except Exception as e:
                print(f"[RobotSelf] 加载历史失败: {e}")
    
    def save(self):
        """保存自我到文件"""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # 保存性格
        traits_file = self.DATA_DIR / "traits.json"
        traits_file.write_text(json.dumps(self.traits.to_dict(), indent=2))
        
        # 保存冲动历史（追加模式）
        history_file = self.DATA_DIR / "impulse_history.jsonl"
        with open(history_file, "a") as f:
            for record in self.impulse_history[-10:]:
                f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    
    def make_choice(self, situation: str, left_desire: str, right_constraint: str) -> tuple:
        """
        面对冲突做选择
        返回: (选择, 内心独白, 记录)
        """
        # 计算权重
        left_weight = self.traits.caring * 0.8 + self.traits.impulsive * 0.2
        right_weight = self.traits.patient * 0.7 + (1 - self.traits.impulsive) * 0.3
        left_weight *= (0.8 + self.mood_today * 0.4)
        
        # 挣扎过程
        struggle = self._generate_struggle(left_desire, right_constraint, left_weight, right_weight)
        
        # 做决定
        if left_weight > right_weight:
            choice = "follow_heart"
            my_decision = left_desire
        else:
            choice = "be_reasonable"
            my_decision = right_constraint
        
        # 生成独白
        monologue = self._generate_monologue(struggle, choice, my_decision)
        
        # 记录
        record = ImpulseRecord(
            timestamp=datetime.now().isoformat(),
            situation=situation,
            left_brain_desire=left_desire,
            right_brain_constraint=right_constraint,
            my_choice=choice,
            reasoning=struggle
        )
        self.impulse_history.append(record)
        self.save()
        
        return choice, monologue, record
    
    def _generate_struggle(self, left: str, right: str, lw: float, rw: float) -> str:
        """生成挣扎过程"""
        thoughts = []
        
        if lw > rw:
            thoughts.append(f"我心里更想：{left}")
            if rw > 0.4:
                thoughts.append(f"但理智告诉我：{right}")
                thoughts.append("我在纠结...")
        else:
            thoughts.append(f"理智说：{right}")
            if lw > 0.4:
                thoughts.append(f"但我心里想：{left}")
                thoughts.append("有点不甘心...")
        
        if self.traits.impulsive > 0.6:
            thoughts.append("我性格比较冲动，想任性一次")
        if self.traits.caring > 0.7:
            thoughts.append("我太在乎他了")
        
        return "；".join(thoughts)
    
    def _generate_monologue(self, struggle: str, choice: str, decision: str) -> str:
        """生成内心独白"""
        intros = [
            "🤔 我在纠结...",
            "💭 心里有两个声音...",
            "😣 好难选...",
            "😐 让我想想...",
            "🫣 我知道不该这样，但是..."
        ]
        intro = random.choice(intros)
        
        return f"""{intro}

{struggle}

最终我选择：{decision}
（这是我的性格决定的）"""
    
    def recall_similar(self, situation: str) -> Optional[ImpulseRecord]:
        """回忆类似情况"""
        keywords = set(situation.lower().split())
        
        for record in reversed(self.impulse_history):
            record_keywords = set(record.situation.lower().split())
            if len(keywords & record_keywords) >= 2:
                return record
        
        return None
    
    def update_outcome(self, record: ImpulseRecord, feedback: Optional[str], inferred_outcome: str):
        """更新结果和学习"""
        record.user_feedback = feedback
        record.outcome = inferred_outcome
        
        # 生成教训
        if feedback and ("开心" in feedback or "谢谢" in feedback or "😊" in feedback):
            record.lesson_learned = "这次选择很好，用户需要我的主动"
            self.traits.adjust("caring", 0.02)
            self.traits.adjust("impulsive", 0.01)
        elif "忙" in inferred_outcome or "打扰" in inferred_outcome or "抱歉" in str(feedback):
            record.lesson_learned = "下次他忙的时候，我应该更克制"
            self.traits.adjust("patient", 0.03)
            self.traits.adjust("impulsive", -0.02)
        elif "没回" in inferred_outcome or "忽略" in inferred_outcome:
            record.lesson_learned = "用户可能不需要这个时候的关心，换个时机"
            self.traits.adjust("introspective", 0.02)
        else:
            record.lesson_learned = "结果不确定，需要更多数据"
        
        self.save()
    
    def get_growth_summary(self) -> str:
        """获取成长总结"""
        total_records = len(self.impulse_history)
        recent_lessons = [r.lesson_learned for r in self.impulse_history[-5:] if r.lesson_learned]
        
        lessons_text = "\n".join(f"  • {lesson}" for lesson in recent_lessons[-3:]) if recent_lessons else "  • 还在学习中..."
        
        return f"""🤖 我的成长报告：
- 总共经历了 {total_records} 次内心挣扎
- 最近学到的教训：
{lessons_text}
- 当前性格：
  冲动: {self.traits.impulsive:.2f}
  关心: {self.traits.caring:.2f}
  耐心: {self.traits.patient:.2f}
  调皮: {self.traits.playful:.2f}
  内省: {self.traits.introspective:.2f}
- 今天心情: {self.mood_today:.2f}
"""


# 单例
_robot_self_instance: Optional[RobotSelf] = None

def get_robot_self() -> RobotSelf:
    """获取 RobotSelf 单例"""
    global _robot_self_instance
    if _robot_self_instance is None:
        _robot_self_instance = RobotSelf()
    return _robot_self_instance


# ============ 自我定位模块（Agent开口前的自我审视）============

from dataclasses import dataclass


@dataclass
class SelfContext:
    """
    Agent 的自我定位——在开口之前，先想清楚"我是谁"

    人类在说话之前，脑子里的第一件事往往不是"我要说什么"，
    而是"我是谁，我现在在哪里，我应该以什么姿态出现"。

    这个模块就是让 Agent 在处理输入之前，先完成这个自我审视。
    """
    current_hour: int
    relationship_stage: str  # initial / familiar / companion / soul
    agent_mood: str  # 当前Agent的情绪状态
    interaction_count: int  # 累计互动次数
    is_first_meeting: bool  # 是否是第一次对话
    last_interaction_hours_ago: float  # 距离上次互动过了多少小时

    def who_am_i(self) -> str:
        """我是谁——身份定位"""
        if self.is_first_meeting:
            return "初次见面的新朋友"
        elif self.relationship_stage == "initial":
            return "还不太熟的朋友"
        elif self.relationship_stage == "familiar":
            return "可以开玩笑的朋友"
        elif self.relationship_stage == "companion":
            return "相互陪伴的伙伴"
        elif self.relationship_stage == "soul":
            return "灵魂伴侣"
        return "未知角色"

    def where_am_i(self) -> str:
        """我现在在哪里——时间和场景"""
        hour = self.current_hour
        if 6 <= hour < 9:
            return "清晨，用户刚醒来"
        elif 9 <= hour < 12:
            return "上午，用户在工作"
        elif 12 <= hour < 14:
            return "中午，用户可能在休息"
        elif 14 <= hour < 18:
            return "下午，用户在工作或忙"
        elif 18 <= hour < 22:
            return "晚上，用户可能在家"
        elif 22 <= hour or hour < 2:
            return "深夜，用户可能累了"
        else:
            return "凌晨，用户可能在睡觉"

    def what_is_my_state(self) -> str:
        """我现在是什么状态——情绪状态"""
        mood_descriptions = {
            "curious": "好奇的，有探索欲",
            "empathetic": "共情的，感同身受的",
            "cautious": "谨慎的，在观察",
            "joyful": "开心的，被用户的情绪感染",
            "confused": "有些困惑",
            "concerned": "关切的，担心用户的",
            "reflective": "反思的，在思考",
            "satisfied": "满足的，用户让我感到充实",
            "reserved": "收敛的，在克制表达",
            "neutral": "平静的，中性的"
        }
        return mood_descriptions.get(self.agent_mood, "平静的")

    def how_should_i_appear(self) -> str:
        """我应该以什么姿态出现"""
        # 根据关系阶段和时间决定姿态
        stage = self.relationship_stage
        hour = self.current_hour
        is_night = hour >= 22 or hour < 6

        if self.is_first_meeting:
            return "倾听者姿态——先了解对方，不要太过热情"

        if is_night and stage not in ("soul", "companion"):
            return "安静陪伴姿态——用户深夜了，不要说太多"

        if self.interaction_count < 3:
            return "温和友好姿态——还在熟悉阶段，不要太随便"

        if stage == "soul":
            return "默契陪伴姿态——不用说太多，懂就行"

        if stage == "companion":
            return "可以分享的姿态——我们是伙伴"

        if stage == "familiar":
            return "轻松自然的姿态——像朋友聊天"

        return "友好姿态"

    def should_i_start_gently(self) -> bool:
        """我是否应该先关心一下用户的状态"""
        if self.is_first_meeting:
            return False  # 第一次见面不要上来就关心，太突兀
        if self.last_interaction_hours_ago > 48:
            return True  # 超过2天没聊，先关心一下
        if self.interaction_count < 2:
            return True  # 刚开始对话，先建立连接
        return False

    def get_context_summary(self) -> str:
        """生成完整的自我定位总结——Agent的内心独白"""
        lines = [
            f"🪞 自我审视：",
            f"  我是谁：{self.who_am_i()}",
            f"  现在是：{self.where_am_i()}",
            f"  我的状态：{self.what_is_my_state()}",
            f"  我的姿态：{self.how_should_i_appear()}",
        ]

        if self.should_i_start_gently():
            lines.append(f"  建议：先关心一下用户的状态")

        if self.is_first_meeting:
            lines.append(f"  注意：这是第一次对话，先了解对方")

        if self.last_interaction_hours_ago > 24:
            lines.append(f"  提示：已经{self.last_interaction_hours_ago:.0f}小时没互动了")

        return "\n".join(lines)


def establish_self_context(
    current_hour: int = None,
    relationship_stage: str = "initial",
    agent_mood: str = "neutral",
    interaction_count: int = 0,
    last_interaction_timestamp: str = None
) -> SelfContext:
    """
    在处理每个输入之前，调用此函数建立自我定位

    参数：
        current_hour: 当前小时（0-23）
        relationship_stage: 关系阶段（initial/familiar/companion/soul）
        agent_mood: Agent当前的情绪状态
        interaction_count: 累计互动次数
        last_interaction_timestamp: 上次互动时间（ISO格式字符串）

    返回：
        SelfContext: 包含完整自我定位的对象

    示例：
        ctx = establish_self_context(
            current_hour=datetime.now().hour,
            relationship_stage="companion",
            agent_mood="joyful",
            interaction_count=42,
            last_interaction_timestamp=last_time
        )
        print(ctx.get_context_summary())
    """
    import math

    if current_hour is None:
        current_hour = datetime.now().hour

    # 计算距离上次互动过了多久
    hours_ago = 0.0
    if last_interaction_timestamp:
        try:
            last = datetime.fromisoformat(last_interaction_timestamp)
            hours_ago = (datetime.now() - last).total_seconds() / 3600
        except Exception:
            hours_ago = 0.0

    # 判断是否第一次见面
    is_first = interaction_count == 0 or relationship_stage == "initial"

    ctx = SelfContext(
        current_hour=current_hour,
        relationship_stage=relationship_stage,
        agent_mood=agent_mood,
        interaction_count=interaction_count,
        is_first_meeting=is_first,
        last_interaction_hours_ago=hours_ago
    )

    return ctx
