"""
temporal/short_term_memory.py
==============================

Neuro-Agent 短期记忆池
负责：最近 5 轮对话的短期记忆、话题追踪、情绪趋势

数据目录：
    ~/.openclaw/workspace/neuro_claw/capsules/short_term/
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# ============ 路径配置 ============
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SHORT_TERM_FILE = DATA_DIR / "short_term.json"

# ============ 常量 ============
MAX_TURNS = 5  # 保留最近 5 轮对话
TOPIC_WINDOW = 3  # 用于判断话题的窗口大小


# ============ 数据结构 ============
@dataclass
class MemoryTurn:
    """
    对话轮次记录
    
    属性说明：
        - turn_id: 轮次 ID（递增）
        - user_input: 用户输入
        - agent_response: AI 回应
        - emotions: 该轮情绪标签列表
        - capsule_ids: 该轮创建的胶囊 ID 列表
        - timestamp: 时间戳
        - topic: 该轮识别的话题
    """
    turn_id: int
    user_input: str
    agent_response: str
    emotions: List[str]
    capsule_ids: List[str]
    timestamp: str
    topic: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict) -> 'MemoryTurn':
        return cls(**d)


@dataclass
class TopicInfo:
    """
    话题信息
    """
    topic: str
    turn_ids: List[int]  # 涉及该话题的轮次
    first_mentioned: str  # 首次提及时间
    last_mentioned: str  # 最后提及时间
    mention_count: int   # 提及次数


@dataclass
class ShortTermOutput:
    """
    短期记忆输出
    """
    recent_turns: List[MemoryTurn]
    current_topic: str
    mood_trend: List[str]  # 最近几轮的情绪趋势
    topic_history: List[TopicInfo]
    
    @property
    def turn_count(self) -> int:
        return len(self.recent_turns)


# ============ 核心类 ============
class ShortTermMemory:
    """
    短期记忆池
    
    功能：
        - 维护最近 N 轮对话（默认5轮）
        - 追踪当前话题
        - 记录情绪趋势
        - 管理话题历史
        - 触发记忆晋升判断
    """
    
    def __init__(self, max_turns: int = None):
        """
        初始化短期记忆池
        
        参数:
            max_turns: 最大保留轮次，默认 5
        """
        self.max_turns = max_turns or MAX_TURNS
        self.turns: List[MemoryTurn] = []
        self.turn_counter = 0
        self.topics: Dict[str, TopicInfo] = {}
        
        # 加载已有数据
        self._load()
    
    # ============ 对话轮次操作 ============
    
    def add_turn(
        self,
        user_input: str,
        agent_response: str,
        emotions: List[str] = None,
        capsule_ids: List[str] = None,
        topic: str = None
    ) -> MemoryTurn:
        """
        添加对话轮次
        
        参数:
            user_input: 用户输入
            agent_response: AI 回应
            emotions: 情绪标签列表
            capsule_ids: 创建的胶囊 ID 列表
            topic: 识别到的话题
        
        返回:
            MemoryTurn: 创建的轮次记录
        """
        self.turn_counter += 1
        
        emotions = emotions or []
        capsule_ids = capsule_ids or []
        
        # 识别话题
        if topic is None:
            topic = self._detect_topic(user_input)
        
        turn = MemoryTurn(
            turn_id=self.turn_counter,
            user_input=user_input,
            agent_response=agent_response,
            emotions=emotions,
            capsule_ids=capsule_ids,
            timestamp=datetime.now().isoformat(),
            topic=topic
        )
        
        # 添加到列表
        self.turns.append(turn)
        
        # 维护最大轮次
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)
        
        # 更新话题追踪
        self._update_topic(topic, turn.turn_id)
        
        # 保存
        self._save()
        
        return turn
    
    def get_recent(self, count: int = None) -> List[MemoryTurn]:
        """
        获取最近 N 轮对话
        
        参数:
            count: 获取数量，默认全部
        
        返回:
            List[MemoryTurn]
        """
        count = count or len(self.turns)
        return self.turns[-count:]
    
    def get_turn(self, turn_id: int) -> Optional[MemoryTurn]:
        """
        获取指定轮次
        
        参数:
            turn_id: 轮次 ID
        
        返回:
            MemoryTurn 或 None
        """
        for turn in self.turns:
            if turn.turn_id == turn_id:
                return turn
        return None
    
    def get_all_turns(self) -> List[MemoryTurn]:
        """获取所有轮次"""
        return self.turns.copy()
    
    # ============ 话题追踪 ============
    
    def get_current_topic(self) -> str:
        """
        获取当前话题
        
        基于最近 N 轮对话中出现频率最高的话题
        
        返回:
            str: 当前话题（如果是 "unknown" 表示无明确话题）
        """
        if not self.turns:
            return "unknown"
        
        # 统计最近几轮的话题
        recent = self.turns[-TOPIC_WINDOW:]
        topic_counts: Dict[str, int] = {}
        
        for turn in recent:
            topic = turn.topic if turn.topic else "unknown"
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        if not topic_counts:
            return "unknown"
        
        # 返回出现最多的
        return max(topic_counts.items(), key=lambda x: x[1])[0]
    
    def get_topic_history(self, limit: int = 10) -> List[TopicInfo]:
        """
        获取话题历史
        
        参数:
            limit: 返回数量上限
        
        返回:
            List[TopicInfo]: 按提及次数排序
        """
        topics = list(self.topics.values())
        topics.sort(key=lambda x: x.mention_count, reverse=True)
        return topics[:limit]
    
    def get_topic_turns(self, topic: str) -> List[MemoryTurn]:
        """
        获取涉及某话题的所有轮次
        
        参数:
            topic: 话题名称
        
        返回:
            List[MemoryTurn]
        """
        topic_info = self.topics.get(topic)
        if not topic_info:
            return []
        
        turns = []
        for turn_id in topic_info.turn_ids:
            turn = self.get_turn(turn_id)
            if turn:
                turns.append(turn)
        return turns
    
    def _detect_topic(self, text: str) -> str:
        """
        简单话题检测
        
        基于关键词匹配
        后续可以升级为更复杂的 NLP 分类
        
        参数:
            text: 输入文本
        
        返回:
            str: 话题名称
        """
        text = text.lower()
        
        # 工作相关
        work_keywords = ["工作", "上班", "老板", "同事", "公司", "面试", "求职", "辞职", "加班", "工资", "升职", "job", "work"]
        if any(kw in text for kw in work_keywords):
            return "工作"
        
        # 生活相关
        life_keywords = ["吃饭", "睡觉", "做饭", "家务", "搬家", "装修", "生活"]
        if any(kw in text for kw in life_keywords):
            return "生活"
        
        # 情感相关
        emotion_keywords = ["男/女", "朋友", "家人", "对象", "恋人", "约会", "分手", "吵架", "感情", "爱", "love"]
        if any(kw in text for kw in emotion_keywords):
            return "情感"
        
        # 健康相关
        health_keywords = ["身体", "健康", "运动", "减肥", "生病", "医院", "医生", "吃药"]
        if any(kw in text for kw in health_keywords):
            return "健康"
        
        # 学习相关
        study_keywords = ["学习", "考试", "读书", "课程", "上课", "作业", "毕业"]
        if any(kw in text for kw in study_keywords):
            return "学习"
        
        # 娱乐相关
        entertainment_keywords = ["电影", "电视", "游戏", "音乐", "旅游", "旅行", "逛街", "购物"]
        if any(kw in text for kw in entertainment_keywords):
            return "娱乐"
        
        # 科技相关
        tech_keywords = ["手机", "电脑", "软件", "app", "网站", "ai", "人工智能", "技术"]
        if any(kw in text for kw in tech_keywords):
            return "科技"
        
        # 财务相关
        money_keywords = ["钱", "理财", "投资", "买房", "贷款", "信用卡", "存款", "money"]
        if any(kw in text for kw in money_keywords):
            return "财务"
        
        return "闲聊"  # 默认话题
    
    def _update_topic(self, topic: str, turn_id: int):
        """更新话题追踪"""
        now = datetime.now().isoformat()
        
        if topic in self.topics:
            info = self.topics[topic]
            if turn_id not in info.turn_ids:
                info.turn_ids.append(turn_id)
            info.last_mentioned = now
            info.mention_count += 1
        else:
            self.topics[topic] = TopicInfo(
                topic=topic,
                turn_ids=[turn_id],
                first_mentioned=now,
                last_mentioned=now,
                mention_count=1
            )
    
    # ============ 情绪追踪 ============
    
    def get_mood_trend(self, count: int = None) -> List[str]:
        """
        获取情绪趋势
        
        参数:
            count: 获取最近几轮的情绪
        
        返回:
            List[str]: 情绪标签列表
        """
        count = count or self.max_turns
        recent = self.turns[-count:]
        
        trend = []
        for turn in recent:
            if turn.emotions:
                # 取该轮最强的情绪
                trend.append(turn.emotions[0])
            else:
                trend.append("neutral")
        
        return trend
    
    def get_dominant_emotion(self) -> str:
        """
        获取当前主导情绪
        
        基于最近几轮出现最多的情绪
        
        返回:
            str: 主导情绪标签
        """
        recent = self.turns[-TOPIC_WINDOW:]
        emotion_counts: Dict[str, int] = {}
        
        for turn in recent:
            for emotion in turn.emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if not emotion_counts:
            return "neutral"
        
        return max(emotion_counts.items(), key=lambda x: x[1])[0]
    
    def is_emotion_escalating(self) -> bool:
        """
        判断情绪是否在升级
        
        基于连续3轮情绪强度变化
        
        返回:
            bool: 是否在升级
        """
        if len(self.turns) < 3:
            return False
        
        # 简化版本：检查是否有连续的负面情绪
        recent = self.turns[-3:]
        negative = ["sadness", "anger", "anxiety", "fear", "frustration"]
        
        count = sum(1 for turn in recent if any(e in negative for e in turn.emotions))
        return count >= 2
    
    # ============ 记忆晋升判断 ============
    
    def should_promote(self, capsule_id: str) -> bool:
        """
        判断胶囊是否应该从短期晋升到长期
        
        条件：在最近 N 轮中被提及 >= 2 次
        
        参数:
            capsule_id: 胶囊 ID
        
        返回:
            bool: 是否应该晋升
        """
        mention_count = 0
        
        for turn in self.turns:
            if capsule_id in turn.capsule_ids:
                mention_count += 1
        
        return mention_count >= 2
    
    def get_promotion_candidates(self) -> List[str]:
        """
        获取应该晋升的胶囊 ID 列表
        
        返回:
            List[str]: 胶囊 ID 列表
        """
        candidates = []
        
        for turn in self.turns:
            for capsule_id in turn.capsule_ids:
                if self.should_promote(capsule_id):
                    if capsule_id not in candidates:
                        candidates.append(capsule_id)
        
        return candidates
    
    # ============ 上下文构建 ============
    
    def build_context(self) -> Dict[str, Any]:
        """
        构建上下文供其他模块使用
        
        返回:
            Dict: 包含当前状态的所有上下文信息
        """
        return {
            "turn_count": len(self.turns),
            "current_topic": self.get_current_topic(),
            "dominant_emotion": self.get_dominant_emotion(),
            "mood_trend": self.get_mood_trend(),
            "is_emotion_escalating": self.is_emotion_escalating(),
            "recent_topics": [t.topic for t in self.get_topic_history(5)],
            "total_capsules_in_session": sum(len(t.capsule_ids) for t in self.turns)
        }
    
    # ============ 持久化 ============
    
    def _save(self):
        """保存到文件"""
        try:
            data = {
                "turn_counter": self.turn_counter,
                "turns": [t.to_dict() for t in self.turns],
                "topics": {
                    name: asdict(info) for name, info in self.topics.items()
                }
            }
            
            with open(SHORT_TERM_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"[ShortTermMemory] 保存失败: {e}")
    
    def _load(self):
        """从文件加载（兼容新旧两种格式）"""
        if not SHORT_TERM_FILE.exists():
            return
        
        try:
            with open(SHORT_TERM_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 旧格式：直接是数组 [{}]
            # 新格式：{turns: [...], turn_counter: int, topics: {...}}
            if isinstance(data, list):
                turns_raw = data
            elif isinstance(data, dict):
                self.turn_counter = data.get("turn_counter", 0)
                turns_raw = data.get("turns", [])
                self.topics = {
                    name: TopicInfo(**info) 
                    for name, info in data.get("topics", {}).items()
                }
            else:
                turns_raw = []
            
            # 字段兼容：旧格式用 user/agent，新格式用 user_input/agent_response
            def _normalize(t: Dict) -> Dict:
                t = dict(t)  # 不修改原数据
                # 字段兼容：旧格式 user/agent → 新格式 user_input/agent_response
                if "user_input" not in t and "user" in t:
                    t["user_input"] = t.pop("user")
                    t["agent_response"] = t.pop("agent")
                # 移除 MemoryTurn 不认识的字段
                t.pop("emotion", None)   # 旧字段，已转为 emotions
                t.pop("intent", None)    # 旧字段，未使用
                # 补齐缺失字段
                if "emotions" not in t:
                    t["emotions"] = []
                if "capsule_ids" not in t:
                    t["capsule_ids"] = []
                if "topic" not in t:
                    t["topic"] = ""
                if "turn_id" not in t:
                    t["turn_id"] = 0
                return t
            
            self.turns = [MemoryTurn.from_dict(_normalize(t)) for t in turns_raw]
            
        except Exception as e:
            print(f"[ShortTermMemory] 加载失败: {e}")
    
    def clear(self):
        """清空短期记忆"""
        self.turns.clear()
        self.topics.clear()
        self.turn_counter = 0
        self._save()
    
    def export(self) -> Dict[str, Any]:
        """
        导出所有数据
        
        返回:
            Dict: 完整数据
        """
        return {
            "turns": [t.to_dict() for t in self.turns],
            "topics": {
                name: asdict(info) for name, info in self.topics.items()
            },
            "stats": {
                "total_turns": len(self.turns),
                "total_topics": len(self.topics),
                "total_capsules": sum(len(t.capsule_ids) for t in self.turns)
            }
        }


# ============ 单例模式 ============
_memory_instance: Optional[ShortTermMemory] = None

def get_instance() -> ShortTermMemory:
    """获取 ShortTermMemory 单例"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = ShortTermMemory()
    return _memory_instance


# ============ 快捷函数 ============
def add_turn(
    user_input: str,
    agent_response: str,
    emotions: List[str] = None,
    capsule_ids: List[str] = None
) -> MemoryTurn:
    """快捷添加轮次"""
    return get_instance().add_turn(
        user_input=user_input,
        agent_response=agent_response,
        emotions=emotions,
        capsule_ids=capsule_ids
    )

def get_recent_turns(count: int = 5) -> List[MemoryTurn]:
    """快捷获取最近轮次"""
    return get_instance().get_recent(count)

def get_current_context() -> Dict[str, Any]:
    """快捷获取当前上下文"""
    return get_instance().build_context()


# ============ 测试 ============
if __name__ == "__main__":
    stm = ShortTermMemory()
    
    # 模拟对话
    print("=== 模拟对话 ===")
    
    turn1 = stm.add_turn(
        user_input="今天工作好累啊，老板又骂我了",
        agent_response="听起来确实很累，被老板骂肯定不好受",
        emotions=["sadness", "frustration"]
    )
    print(f"轮次1: topic={turn1.topic}")
    
    turn2 = stm.add_turn(
        user_input="想辞职了，不想干了",
        agent_response="有这种想法很正常，不过我们可以先聊聊具体是什么让你这么疲惫",
        emotions=["frustration", "anger"]
    )
    print(f"轮次2: topic={turn2.topic}")
    
    turn3 = stm.add_turn(
        user_input="算了，说说别的吧，你们最近有什么新功能吗？",
        agent_response="最近确实更新了很多功能哦...",
        emotions=["neutral"]
    )
    print(f"轮次3: topic={turn3.topic}")
    
    # 查询状态
    print("\n=== 当前状态 ===")
    print(f"轮次总数: {len(stm.get_all_turns())}")
    print(f"当前话题: {stm.get_current_topic()}")
    print(f"主导情绪: {stm.get_dominant_emotion()}")
    print(f"情绪趋势: {stm.get_mood_trend()}")
    print(f"情绪升级: {stm.is_emotion_escalating()}")
    
    print("\n=== 话题历史 ===")
    for topic in stm.get_topic_history():
        print(f"  {topic.topic}: {topic.mention_count}次")
    
    print("\n=== 上下文 ===")
    print(stm.build_context())
