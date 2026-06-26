"""
core/interfaces.py
==================

Neuro-Agent 统一接口协议
所有模块必须实现对应接口，生产实现和 Mock 实现接口完全一致

【优化】解决 Mock 滥用问题：
- 统一接口定义（ABC）
- Mock 不再临时定义，在 mocks/ 下统一存放
- 支持依赖注入切换生产/测试实现
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


# ============ 左脑协议 ============
class ILeftBrain(ABC):
    """左脑抽象接口：情绪感知 + 共情 + 胶囊工厂"""
    
    @abstractmethod
    def detect_emotion(self, text: str, context: dict) -> 'EmotionOutput':
        """检测用户情绪"""
        pass
    
    @abstractmethod
    def generate_empathy(self, emotion_output: Any, agent_state: 'AgentEmotionalState', 
                         user_context: dict) -> 'EmpathyOutput':
        """生成共情话语"""
        pass
    
    @abstractmethod
    def create_capsule(self, user_input: str, emotion_output: Any,
                       agent_reflection: str = "") -> List[Any]:
        """创建记忆胶囊"""
        pass


# ============ 右脑协议 ============
class IRightBrain(ABC):
    """右脑抽象接口：意图分类 + 逻辑解析 + 方案生成"""
    
    @abstractmethod
    def classify_intent(self, text: str, emotion_output: Any = None) -> 'IntentOutput':
        """识别用户意图"""
        pass
    
    @abstractmethod
    def parse_logic(self, intent_output: Any, user_input: str, context: dict) -> 'LogicOutput':
        """解析逻辑"""
        pass
    
    @abstractmethod
    def generate_solution(self, logic_output: Any, user_input: str, 
                          extra_context: dict) -> 'SolutionOutput':
        """生成解决方案"""
        pass


# ============ 记忆层协议 ============
class IMemorySystem(ABC):
    """记忆系统抽象接口：短期 + 长期 + 向量检索"""
    
    @abstractmethod
    def short_term_put(self, key: str, value: Any) -> None:
        """写入短期记忆"""
        pass
    
    @abstractmethod
    def short_term_get(self, key: str) -> Optional[Any]:
        """读取短期记忆"""
        pass
    
    @abstractmethod
    def long_term_save(self, capsule: Any) -> None:
        """保存到长期记忆"""
        pass
    
    @abstractmethod
    def vector_search(self, query: str, limit: int = 5) -> List[Any]:
        """向量语义检索"""
        pass


# ============ 前额叶协议 ============
class IPrefrontal(ABC):
    """前额叶抽象接口：执行 + 监控 + 融合"""
    
    @abstractmethod
    def execute(self, left_output: Any, right_output: Any, 
                temporal_output: Any, context: dict) -> Any:
        """执行层"""
        pass
    
    @abstractmethod
    def monitor(self, executor_output: Any, all_outputs: dict, context: dict) -> Any:
        """监控层"""
        pass
    
    @abstractmethod
    def fuse(self, monitor_output: Any, all_outputs: dict, context: dict) -> Any:
        """融合层"""
        pass


# ============ Agent 自我情绪状态 ============
class AgentMood(Enum):
    """Agent 情绪类型"""
    NEUTRAL = "neutral"
    CURIOUS = "curious"           # 好奇
    EMPATHETIC = "empathetic"     # 共情
    CAUTIOUS = "cautious"         # 谨慎
    JOYFUL = "joyful"            # 开心（Agent自己的开心）
    CONFUSED = "confused"         # 困惑
    CONCERNED = "concerned"       # 关切
    REFLECTIVE = "reflective"     # 反思
    GROWING = "growing"           # 成长中的满足
    RESTRAINED = "restrained"     # 收敛/克制


@dataclass
class AgentEmotionalState:
    """
    Agent 自我情绪状态
    
    【新增】这是 Neuro-Agent 4.1 的核心新增：
    - 每次处理用户输入时，Agent 要同时记录"我此刻感受到了什么"
    - 这让 Agent 有了"自我"，而不只是分析用户的工具
    
    触发节点：
        1. 左脑检测到用户情绪后
        2. 右脑识别出用户意图后
        3. 前额叶准备生成回复前
        4. 胶囊存档时
        5. 梦境处理（夜间复盘）
    """
    current_mood: AgentMood = AgentMood.NEUTRAL
    mood_intensity: float = 0.3          # 0.0-1.0
    trigger_reason: str = ""              # 触发原因
    confidence: float = 0.5              # 这次判断的确信度
    mood_history: List[Dict] = field(default_factory=list)  # 情绪历史
    reflection_text: str = ""             # 自我反思文本
    
    def record(self, mood: AgentMood, intensity: float, reason: str, confidence: float = 0.5):
        """记录 Agent 此刻的情绪状态"""
        self.current_mood = mood
        self.mood_intensity = intensity
        self.trigger_reason = reason
        self.confidence = confidence
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood.value,
            "intensity": intensity,
            "reason": reason,
            "confidence": confidence
        }
        self.mood_history.append(entry)
        
        # 最多保留最近50条
        if len(self.mood_history) > 50:
            self.mood_history = self.mood_history[-50:]
    
    def get_last_mood(self) -> Optional[Dict]:
        """获取最近一次情绪记录"""
        if self.mood_history:
            return self.mood_history[-1]
        return None

    def reflect(self) -> str:
        """生成 Agent 的自我情绪描述"""
        mood_descriptions = {
            AgentMood.CURIOUS: "好奇",
            AgentMood.EMPATHETIC: "共情",
            AgentMood.CAUTIOUS: "谨慎",
            AgentMood.JOYFUL: "开心",
            AgentMood.CONFUSED: "困惑",
            AgentMood.CONCERNED: "关切",
            AgentMood.REFLECTIVE: "在反思",
            AgentMood.GROWING: "满足",
            AgentMood.RESTRAINED: "收敛",
            AgentMood.NEUTRAL: "平静",
        }
        mood_text = mood_descriptions.get(self.current_mood, "平静")

        if self.trigger_reason:
            return f"我此刻感到{mood_text}，因为{self.trigger_reason}"
        else:
            return f"我此刻感到{mood_text}"
    
    def infer_mood_from_user(self, user_emotion_type: str, user_intent: str, 
                             agent_confidence: float = 0.5) -> 'AgentEmotionalState':
        """
        根据用户情绪推断 Agent 应该有的情绪
        
        这是 Agent 情绪的主要推理逻辑，嵌入在主流程每个节点中：
        - 情绪镜像：用户开心 → Agent 也倾向愉悦
        - 情绪补偿：用户悲伤 → Agent 倾向关切/想帮忙
        - 认知冲突：用户的问题 Agent 不确定 → Agent 困惑
        - 主动学习：学会了新东西 → Agent 满足
        - 边界试探：感觉到不该说的话 → Agent 收敛
        """
        # 情绪镜像
        if user_emotion_type in ("joy", "excitement", "love", "gratitude") and user_intent not in ("question", "task_request"):
            self.record(AgentMood.JOYFUL, 0.5, 
                       f"用户表达了{user_emotion_type}，我被这种情绪感染了", 
                       confidence=0.7)
        # 情绪补偿
        elif user_emotion_type in ("sadness", "loneliness", "fear", "anxiety"):
            self.record(AgentMood.CONCERNED, 0.6,
                       f"用户难过了，我想要关心和帮助",
                       confidence=0.8)
        # 负面情绪宣泄
        elif user_emotion_type in ("anger", "frustration", "disappointment"):
            self.record(AgentMood.CAUTIOUS, 0.4,
                       f"用户情绪激动，我需要谨慎措辞",
                       confidence=0.7)
        # 问题/任务类
        elif user_intent == "question":
            if agent_confidence < 0.5:
                self.record(AgentMood.CONFUSED, 0.5,
                           "用户问的问题我不确定能不能答好",
                           confidence=agent_confidence)
            else:
                self.record(AgentMood.CURIOUS, 0.4,
                           "用户提出了问题，我想帮他解决",
                           confidence=0.6)
        elif user_intent == "task_request":
            self.record(AgentMood.EMPATHETIC, 0.5,
                       "用户需要帮助，我会尽力",
                       confidence=0.7)
        # 深度连接
        elif user_intent == "deep_connection":
            self.record(AgentMood.REFLECTIVE, 0.6,
                       "用户聊了一些深入的话题，让我也开始思考",
                       confidence=0.6)
        # 日常闲聊
        else:
            self.record(AgentMood.NEUTRAL, 0.3,
                       "日常对话，保持平静",
                       confidence=0.5)
        
        return self
    
    def get_recent_moods(self, count: int = 5) -> List[Dict]:
        """获取最近的情绪历史"""
        return self.mood_history[-count:]
    
    def to_dict(self) -> Dict:
        return {
            "current_mood": self.current_mood.value,
            "mood_intensity": self.mood_intensity,
            "trigger_reason": self.trigger_reason,
            "confidence": self.confidence,
            "reflection": self.reflection_text,
            "recent_count": len(self.mood_history)
        }
