"""
Enhanced MemCore - 优化版五层记忆架构 + 四大增强模块
========================================================
在原 MemCore 基础上新增：
1. Episodic Memory（情景记忆）- 记录具体事件和结论
2. Semantic Compression（语义压缩）- 自动压缩冗余信息
3. Memory Triggers（记忆触发器）- 关键词触发的记忆加载
4. Forgetting Curve（遗忘曲线）- 模拟人类遗忘机制
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import math


class MemoryPriority(Enum):
    """记忆优先级"""
    CRITICAL = 5    # 关键信息（如用户名字、重要偏好）
    HIGH = 4        # 重要信息
    MEDIUM = 3      # 一般信息
    LOW = 2         # 次要信息
    EPHEMERAL = 1   # 临时信息


@dataclass
class MemoryEntry:
    """记忆条目基类"""
    id: str
    content: Any
    timestamp: datetime
    priority: MemoryPriority
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    compression_level: int = 0  # 被压缩次数
    
    def touch(self):
        """访问时更新"""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def get_forgetting_score(self, now: datetime = None) -> float:
        """
        计算遗忘分数 (0-1, 越高越应该被遗忘)
        基于艾宾浩斯遗忘曲线简化模型
        """
        if now is None:
            now = datetime.now()
        
        age_hours = (now - self.timestamp).total_seconds() / 3600
        last_access_hours = (now - self.last_accessed).total_seconds() / 3600
        
        # 基础遗忘曲线: R = e^(-t/S) 其中 S 是记忆强度
        # 优先级越高，记忆强度越大
        strength = self.priority.value * (1 + self.access_count * 0.1)
        base_retention = math.exp(-age_hours / (strength * 24))
        
        # 最近访问奖励
        recent_bonus = math.exp(-last_access_hours / 24) * 0.3
        
        # 压缩惩罚（被压缩过的记忆更容易遗忘）
        compression_penalty = self.compression_level * 0.1
        
        retention = base_retention + recent_bonus - compression_penalty
        return max(0, min(1, 1 - retention))  # 转换为遗忘分数


@dataclass
class EpisodicMemoryEntry:
    """
    情景记忆条目
    记录: "上次我们讨论X时，结论是Y"
    """
    # 基础字段
    id: str
    content: Any
    timestamp: datetime
    priority: MemoryPriority
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    compression_level: int = 0
    
    # 情景特有字段
    episode_type: str = "discussion"  # 如 "discussion", "decision", "event"
    participants: List[str] = field(default_factory=list)
    context_summary: str = ""  # 背景摘要
    conclusion: str = ""       # 结论/结果
    related_topics: List[str] = field(default_factory=list)
    
    def touch(self):
        """访问时更新"""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def get_forgetting_score(self, now: datetime = None) -> float:
        """计算遗忘分数"""
        if now is None:
            now = datetime.now()
        
        age_hours = (now - self.timestamp).total_seconds() / 3600
        last_access_hours = (now - self.last_accessed).total_seconds() / 3600
        
        strength = self.priority.value * (1 + self.access_count * 0.1)
        base_retention = math.exp(-age_hours / (strength * 24))
        recent_bonus = math.exp(-last_access_hours / 24) * 0.3
        compression_penalty = self.compression_level * 0.1
        
        retention = base_retention + recent_bonus - compression_penalty
        return max(0, min(1, 1 - retention))
    
    def to_natural_language(self) -> str:
        """转换为自然语言描述"""
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M")
        return f"[{time_str}] {self.episode_type}: 关于 '{self.context_summary}' 的讨论，结论是：{self.conclusion}"


@dataclass
class MemoryTrigger:
    """记忆触发器"""
    id: str
    keywords: List[str]           # 触发关键词
    target_memory_ids: List[str]  # 要加载的记忆ID
    trigger_count: int = 0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def check_trigger(self, text: str) -> bool:
        """检查文本是否触发"""
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in self.keywords)


class SemanticCompressor:
    """
    语义压缩器
    将多条消息/记忆压缩为一条摘要
    """
    
    def __init__(self, llm_compress_fn: Optional[Callable] = None):
        """
        Args:
            llm_compress_fn: 可选的 LLM 压缩函数
        """
        self.llm_compress_fn = llm_compress_fn
        self.compression_threshold = 5  # 多少条记录触发压缩
    
    def should_compress(self, entries: List[MemoryEntry]) -> bool:
        """判断是否需要压缩"""
        return len(entries) >= self.compression_threshold
    
    def compress_context_memory(self, messages: List[Dict]) -> Dict:
        """
        压缩上下文记忆
        将 N 条对话消息压缩为 1 条摘要
        """
        if len(messages) < self.compression_threshold:
            return None
        
        # 简单的规则压缩（实际可用 LLM）
        topics = self._extract_topics(messages)
        summary = f"[压缩记忆] 讨论了: {', '.join(topics)} (共{len(messages)}条消息)"
        
        return {
            "role": "system",
            "content": summary,
            "is_compressed": True,
            "original_count": len(messages),
            "compression_timestamp": datetime.now().isoformat()
        }
    
    def compress_episodic_memories(self, episodes: List[EpisodicMemoryEntry]) -> EpisodicMemoryEntry:
        """
        压缩多个情景记忆为一个
        """
        if not episodes:
            return None
        
        # 聚合相关主题
        all_topics = set()
        all_conclusions = []
        for ep in episodes:
            all_topics.update(ep.related_topics)
            all_conclusions.append(ep.conclusion)
        
        combined_conclusion = " | ".join(all_conclusions[:3])
        if len(all_conclusions) > 3:
            combined_conclusion += f" 等{len(all_conclusions)}个结论"
        
        compressed = EpisodicMemoryEntry(
            id=f"compressed_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}",
            content=f"压缩了{len(episodes)}个相关情景",
            timestamp=datetime.now(),
            priority=max(ep.priority for ep in episodes),
            episode_type="compressed",
            context_summary=f"涉及主题: {', '.join(list(all_topics)[:5])}",
            conclusion=combined_conclusion,
            related_topics=list(all_topics)
        )
        compressed.compression_level = 1
        
        return compressed
    
    def _extract_topics(self, messages: List[Dict]) -> List[str]:
        """简单主题提取（可用 NLP 改进）"""
        # 这里简化处理，实际可用关键词提取
        return list(set([m.get("content", "")[:20] + "..." for m in messages[:3]]))


class ForgettingCurveManager:
    """
    遗忘曲线管理器
    模拟人类遗忘，定期清理低价值记忆
    """
    
    def __init__(
        self,
        forgetting_threshold: float = 0.8,  # 遗忘分数超过此值则清理
        check_interval_hours: int = 24
    ):
        self.forgetting_threshold = forgetting_threshold
        self.check_interval_hours = check_interval_hours
        self.last_check = datetime.now()
    
    def should_forget(self, entry: MemoryEntry) -> bool:
        """判断是否应该遗忘该记忆"""
        # 关键记忆永不忘却
        if entry.priority == MemoryPriority.CRITICAL:
            return False
        
        score = entry.get_forgetting_score()
        return score > self.forgetting_threshold
    
    def apply_forgetting(self, memory_store: Dict[str, MemoryEntry]) -> List[str]:
        """
        执行遗忘，返回被删除的记忆ID
        """
        now = datetime.now()
        
        # 检查间隔
        if (now - self.last_check).total_seconds() < self.check_interval_hours * 3600:
            return []
        
        self.last_check = now
        forgotten_ids = []
        
        for mem_id, entry in list(memory_store.items()):
            if self.should_forget(entry):
                del memory_store[mem_id]
                forgotten_ids.append(mem_id)
        
        return forgotten_ids
    
    def get_memory_stats(self, memory_store: Dict[str, MemoryEntry]) -> Dict:
        """获取记忆统计信息"""
        if not memory_store:
            return {}
        
        scores = [e.get_forgetting_score() for e in memory_store.values()]
        priorities = [e.priority.value for e in memory_store.values()]
        
        return {
            "total_memories": len(memory_store),
            "avg_forgetting_score": sum(scores) / len(scores),
            "high_risk_count": sum(1 for s in scores if s > self.forgetting_threshold),
            "avg_priority": sum(priorities) / len(priorities),
            "at_risk_ids": [
                mid for mid, e in memory_store.items()
                if e.get_forgetting_score() > self.forgetting_threshold
            ]
        }


class EnhancedMemoryRouter:
    """
    增强版记忆路由器
    整合新功能的中央控制器
    """
    
    def __init__(self, llm_compress_fn: Optional[Callable] = None):
        # 原有五层记忆
        self.context_memory: List[Dict] = []
        self.task_memory: Dict[str, Any] = {}
        self.user_memory: Dict[str, MemoryEntry] = {}
        self.knowledge_memory: Dict[str, Any] = {}
        self.experience_memory: Dict[str, Any] = {}
        
        # 新增四层
        self.episodic_memory: Dict[str, EpisodicMemoryEntry] = {}
        self.triggers: Dict[str, MemoryTrigger] = {}
        
        # 管理器
        self.compressor = SemanticCompressor(llm_compress_fn)
        self.forgetter = ForgettingCurveManager()
    
    # ========== 情景记忆接口 ==========
    
    def record_episode(
        self,
        episode_type: str,
        context_summary: str,
        conclusion: str,
        related_topics: List[str] = None,
        participants: List[str] = None,
        priority: MemoryPriority = MemoryPriority.MEDIUM
    ) -> str:
        """
        记录一个情景记忆
        
        示例:
            router.record_episode(
                episode_type="discussion",
                context_summary="用户询问 MemCore 优化建议",
                conclusion="建议添加 Episodic Memory 等四个模块",
                related_topics=["MemCore", "AI记忆", "架构设计"],
                priority=MemoryPriority.HIGH
            )
        """
        episode_id = f"ep_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]}"
        
        episode = EpisodicMemoryEntry(
            id=episode_id,
            content=f"{context_summary} -> {conclusion}",
            timestamp=datetime.now(),
            priority=priority,
            episode_type=episode_type,
            context_summary=context_summary,
            conclusion=conclusion,
            related_topics=related_topics or [],
            participants=participants or []
        )
        
        self.episodic_memory[episode_id] = episode
        
        # 自动创建记忆触发器
        self._auto_create_trigger(related_topics or [], [episode_id])
        
        return episode_id
    
    def recall_episodes(
        self,
        topic: str = None,
        episode_type: str = None,
        limit: int = 5
    ) -> List[EpisodicMemoryEntry]:
        """回忆相关情景"""
        results = []
        
        for episode in self.episodic_memory.values():
            match = True
            if topic and topic not in episode.related_topics:
                match = False
            if episode_type and episode.episode_type != episode_type:
                match = False
            
            if match:
                episode.touch()  # 访问即强化记忆
                results.append(episode)
        
        # 按优先级和时间排序
        results.sort(key=lambda e: (e.priority.value, e.timestamp), reverse=True)
        return results[:limit]
    
    # ========== 记忆触发器接口 ==========
    
    def create_trigger(
        self,
        keywords: List[str],
        target_memory_ids: List[str],
        trigger_id: str = None
    ) -> str:
        """
        创建记忆触发器
        
        示例:
            router.create_trigger(
                keywords=["项目X", "Project X"],
                target_memory_ids=["ep_abc123", "user_pref_456"]
            )
        """
        tid = trigger_id or f"tr_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"
        
        trigger = MemoryTrigger(
            id=tid,
            keywords=keywords,
            target_memory_ids=target_memory_ids
        )
        
        self.triggers[tid] = trigger
        return tid
    
    def process_input(self, text: str) -> Dict[str, Any]:
        """
        处理用户输入，检查触发器并加载相关记忆
        
        Returns:
            {
                "triggered": bool,
                "loaded_memories": [...],
                "suggested_context": str
            }
        """
        result = {
            "triggered": False,
            "loaded_memories": [],
            "suggested_context": ""
        }
        
        for trigger in self.triggers.values():
            if not trigger.is_active:
                continue
            
            if trigger.check_trigger(text):
                trigger.trigger_count += 1
                result["triggered"] = True
                
                # 加载相关记忆
                for mem_id in trigger.target_memory_ids:
                    if mem_id in self.episodic_memory:
                        episode = self.episodic_memory[mem_id]
                        episode.touch()
                        result["loaded_memories"].append(episode.to_natural_language())
                    elif mem_id in self.user_memory:
                        entry = self.user_memory[mem_id]
                        entry.touch()
                        result["loaded_memories"].append(f"[用户偏好] {entry.content}")
        
        if result["loaded_memories"]:
            result["suggested_context"] = "\n".join(result["loaded_memories"])
        
        return result
    
    def _auto_create_trigger(self, topics: List[str], memory_ids: List[str]):
        """自动为新主题创建触发器"""
        for topic in topics:
            # 检查是否已有该主题的触发器
            exists = any(
                topic in t.keywords for t in self.triggers.values()
            )
            if not exists:
                self.create_trigger([topic], memory_ids)
    
    # ========== 语义压缩接口 ==========
    
    def compress_memories(self, memory_type: str = "context") -> Optional[Any]:
        """
        执行语义压缩
        
        Args:
            memory_type: "context" | "episodic"
        """
        if memory_type == "context":
            if self.compressor.should_compress([
                MemoryEntry(id=str(i), content=m, timestamp=datetime.now(), priority=MemoryPriority.LOW)
                for i, m in enumerate(self.context_memory)
            ]):
                compressed = self.compressor.compress_context_memory(self.context_memory)
                if compressed:
                    # 保留最近的2条，其余替换为压缩版本
                    self.context_memory = self.context_memory[-2:] + [compressed]
                    return compressed
        
        elif memory_type == "episodic":
            # 压缩相似的情景记忆
            episodes = list(self.episodic_memory.values())
            if len(episodes) >= 10:
                # 按主题分组压缩
                by_topic = {}
                for ep in episodes:
                    for topic in ep.related_topics:
                        by_topic.setdefault(topic, []).append(ep)
                
                for topic, eps in by_topic.items():
                    if len(eps) >= 5:
                        compressed = self.compressor.compress_episodic_memories(eps)
                        # 删除原记忆，添加压缩版
                        for ep in eps:
                            del self.episodic_memory[ep.id]
                        self.episodic_memory[compressed.id] = compressed
        
        return None
    
    # ========== 遗忘曲线接口 ==========
    
    def run_forgetting_cycle(self) -> Dict:
        """
        运行遗忘周期
        
        Returns:
            统计信息
        """
        stats_before = self.forgetter.get_memory_stats(self.episodic_memory)
        
        # 执行遗忘
        forgotten = self.forgetter.apply_forgetting(self.episodic_memory)
        
        stats_after = self.forgetter.get_memory_stats(self.episodic_memory)
        
        return {
            "forgotten_ids": forgotten,
            "forgotten_count": len(forgotten),
            "stats_before": stats_before,
            "stats_after": stats_after
        }
    
    def get_memory_health(self) -> Dict:
        """获取记忆健康报告"""
        return {
            "episodic_memory": self.forgetter.get_memory_stats(self.episodic_memory),
            "trigger_count": len(self.triggers),
            "context_size": len(self.context_memory),
            "total_stored": len(self.episodic_memory) + len(self.user_memory)
        }
    
    # ========== 原有接口（保持兼容） ==========
    
    def add_to_context(self, message: Dict):
        """添加上下文消息"""
        self.context_memory.append(message)
        
        # 自动压缩检查
        if len(self.context_memory) > 20:
            self.compress_memories("context")
    
    def update_user_memory(self, key: str, value: Any, priority: MemoryPriority = MemoryPriority.MEDIUM):
        """更新用户记忆"""
        entry = MemoryEntry(
            id=f"user_{key}",
            content=value,
            timestamp=datetime.now(),
            priority=priority
        )
        self.user_memory[key] = entry


# ========== 使用示例 ==========

def demo():
    """演示增强版 MemCore 的使用"""
    
    print("=" * 60)
    print("🧠 Enhanced MemCore Demo")
    print("=" * 60)
    
    # 初始化
    router = EnhancedMemoryRouter()
    
    # 1. 记录情景记忆
    print("\n📌 记录情景记忆...")
    ep1 = router.record_episode(
        episode_type="discussion",
        context_summary="用户询问 MemCore 优化建议",
        conclusion="建议添加 Episodic Memory 等四个模块",
        related_topics=["MemCore", "AI记忆", "架构设计"],
        priority=MemoryPriority.HIGH
    )
    print(f"   记录情景: {ep1}")
    
    ep2 = router.record_episode(
        episode_type="decision",
        context_summary="确定使用 MIT-0 许可证",
        conclusion="MemCore 采用 MIT-0 开源许可证",
        related_topics=["MemCore", "开源", "许可证"],
        priority=MemoryPriority.MEDIUM
    )
    print(f"   记录情景: {ep2}")
    
    # 2. 自动触发器工作
    print("\n🎯 测试记忆触发器...")
    result = router.process_input("我想了解一下 MemCore 的架构")
    if result["triggered"]:
        print("   ✓ 触发成功！")
        print(f"   加载记忆:\n   {result['suggested_context']}")
    
    # 3. 回忆功能
    print("\n🔍 回忆关于 'MemCore' 的情景...")
    episodes = router.recall_episodes(topic="MemCore")
    for ep in episodes:
        print(f"   - {ep.to_natural_language()}")
    
    # 4. 模拟时间流逝，测试遗忘
    print("\n⏰ 模拟遗忘周期...")
    # 添加一些低优先级临时记忆
    for i in range(5):
        router.record_episode(
            episode_type="temp",
            context_summary=f"临时测试记忆 {i}",
            conclusion=f"测试结论 {i}",
            related_topics=["test"],
            priority=MemoryPriority.EPHEMERAL
        )
    
    # 手动设置旧时间戳来模拟
    for ep in router.episodic_memory.values():
        if ep.episode_type == "temp":
            ep.timestamp = datetime.now() - timedelta(days=30)
            ep.last_accessed = datetime.now() - timedelta(days=30)
    
    health_before = router.get_memory_health()
    print(f"   遗忘前: {health_before['episodic_memory']['total_memories']} 条记忆")
    
    result = router.run_forgetting_cycle()
    print(f"   遗忘后: 清理了 {result['forgotten_count']} 条记忆")
    
    # 5. 健康报告
    print("\n📊 记忆健康报告:")
    health = router.get_memory_health()
    print(f"   - 情景记忆: {health['episodic_memory']['total_memories']} 条")
    print(f"   - 触发器: {health['trigger_count']} 个")
    print(f"   - 平均遗忘风险: {health['episodic_memory'].get('avg_forgetting_score', 0):.2f}")
    
    print("\n" + "=" * 60)
    print("✅ Demo 完成!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
