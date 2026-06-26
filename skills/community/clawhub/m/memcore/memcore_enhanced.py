"""
Enhanced MemCore - 完整增强版
=====================================
原版 MemCore + 四大新功能：
1. Episodic Memory（情景记忆）
2. Semantic Compression（语义压缩）
3. Memory Triggers（记忆触发器）
4. Forgetting Curve（遗忘曲线）

额外增强：
5. Persistent Storage（持久化存储）
6. Vector Knowledge（向量检索）
7. Conflict Resolution（冲突解决）
8. Confidence Tracking（置信度跟踪）
"""

from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime, timedelta
import hashlib
import json

# 导入各模块
from enhanced_memcore import (
    EpisodicMemoryEntry, MemoryTrigger, SemanticCompressor,
    ForgettingCurveManager, MemoryPriority
)
from persistent_backend import SQLiteBackend, JSONBackend
from vector_knowledge import VectorKnowledgeMemory
from conflict_resolver import MemoryConflictResolver, ConflictStrategy
from confidence_tracker import ConfidenceTracker, MemorySource


class MemCoreEnhanced:
    """
    增强版 MemCore 记忆系统
    
    使用示例：
        memcore = MemCoreEnhanced()
        
        # 记录情景
        memcore.record_episode(
            context_summary="用户询问 MemCore",
            conclusion="用户是开发者",
            related_topics=["MemCore"]
        )
        
        # 查询时触发记忆
        result = memcore.process_input("我想继续弄记忆系统")
    """
    
    def __init__(
        self,
        db_path: str = "~/.memcore/memory.db",
        embedding_fn: Optional[Callable] = None,
        enable_persistence: bool = True
    ):
        """
        初始化增强版 MemCore
        
        Args:
            db_path: SQLite 数据库路径
            embedding_fn: 向量嵌入函数（可选）
            enable_persistence: 是否启用持久化
        """
        print("🚀 初始化 Enhanced MemCore...")
        
        # 持久化后端
        self.backend = SQLiteBackend(db_path) if enable_persistence else None
        
        # 核心记忆存储
        self.episodic_memory: Dict[str, EpisodicMemoryEntry] = {}
        self.triggers: Dict[str, MemoryTrigger] = {}
        self.context_memory: List[Dict] = []
        
        # 增强模块
        self.compressor = SemanticCompressor()
        self.forgetter = ForgettingCurveManager()
        self.conflict_resolver = MemoryConflictResolver()
        self.confidence_tracker = ConfidenceTracker()
        
        # 向量知识库
        self.knowledge = VectorKnowledgeMemory(
            embedding_fn=embedding_fn,
            backend=self.backend
        )
        
        # 加载已存储的记忆
        if enable_persistence:
            self._load_from_storage()
        
        print("\u2705 Enhanced MemCore 就绪!")
    
    def _load_from_storage(self):
        """从持久化存储加载记忆"""
        if not self.backend:
            return
        
        # 加载情景记忆
        episodes_data = self.backend.load_episodic_memories(limit=1000)
        for data in episodes_data:
            episode = EpisodicMemoryEntry(
                id=data['id'],
                content=data['content'],
                timestamp=data['timestamp'],
                priority=MemoryPriority(data['priority']),
                access_count=data['access_count'],
                last_accessed=data['last_accessed'],
                compression_level=data['compression_level'],
                episode_type=data['episode_type'],
                context_summary=data['context_summary'],
                conclusion=data['conclusion'],
                related_topics=data['related_topics'],
                participants=data['participants']
            )
            self.episodic_memory[episode.id] = episode
        
        # 加载触发器
        triggers_data = self.backend.load_triggers()
        for data in triggers_data:
            trigger = MemoryTrigger(
                id=data['id'],
                keywords=data['keywords'],
                target_memory_ids=data['target_memory_ids'],
                trigger_count=data['trigger_count']
            )
            self.triggers[trigger.id] = trigger
        
        print(f"   📂 加载了 {len(self.episodic_memory)} 条情景记忆")
        print(f"   🔔 加载了 {len(self.triggers)} 个触发器")
    
    # ========== 情景记忆接口 ==========
    
    def record_episode(
        self,
        context_summary: str,
        conclusion: str,
        episode_type: str = "discussion",
        related_topics: List[str] = None,
        participants: List[str] = None,
        priority: MemoryPriority = MemoryPriority.MEDIUM,
        confidence: float = 1.0,
        source: MemorySource = MemorySource.EXPLICIT
    ) -> str:
        """
        记录情景记忆
        
        Returns:
            情景ID
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
        
        # 检查冲突
        conflicts = self.conflict_resolver.detect_conflict(
            episode, list(self.episodic_memory.values())
        )
        
        if conflicts:
            episode, _ = self.conflict_resolver.resolve(episode, conflicts)
        
        # 保存到内存
        self.episodic_memory[episode_id] = episode
        
        # 注册置信度
        self.confidence_tracker.register_memory(
            episode_id, source, confidence,
            extraction_method="record_episode"
        )
        
        # 持久化
        if self.backend:
            self.backend.save_episodic_memory(episode)
        
        # 自动创建触发器
        self._auto_create_trigger(related_topics or [], [episode_id])
        
        return episode_id
    
    def recall_episodes(
        self,
        topic: Optional[str] = None,
        episode_type: Optional[str] = None,
        min_confidence: float = 0.0,
        limit: int = 5
    ) -> List[EpisodicMemoryEntry]:
        """
        回忆情景
        
        Args:
            min_confidence: 最低置信度筛选
        """
        results = []
        
        for episode in self.episodic_memory.values():
            # 检查置信度
            conf = self.confidence_tracker.get_confidence(episode.id)
            if conf < min_confidence:
                continue
            
            # 检查过滤条件
            if topic and topic not in episode.related_topics:
                continue
            if episode_type and episode.episode_type != episode_type:
                continue
            
            episode.touch()
            results.append(episode)
            
            # 更新访问时间
            if self.backend:
                self.backend.update_episode_access(episode.id)
        
        # 按优先级和置信度排序
        results.sort(
            key=lambda e: (
                e.priority.value,
                self.confidence_tracker.get_confidence(e.id),
                e.timestamp
            ),
            reverse=True
        )
        
        return results[:limit]
    
    # ========== 记忆触发器 ==========
    
    def create_trigger(
        self,
        keywords: List[str],
        target_memory_ids: List[str],
        trigger_id: Optional[str] = None
    ) -> str:
        """创建记忆触发器"""
        tid = trigger_id or f"tr_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"
        
        trigger = MemoryTrigger(
            id=tid,
            keywords=keywords,
            target_memory_ids=target_memory_ids
        )
        
        self.triggers[tid] = trigger
        
        if self.backend:
            self.backend.save_trigger(trigger)
        
        return tid
    
    def process_input(self, text: str) -> Dict[str, Any]:
        """
        处理用户输入，触发相关记忆
        
        Returns:
            {
                "triggered": bool,
                "loaded_memories": [...],
                "suggested_context": str,
                "related_knowledge": [...]
            }
        """
        result = {
            "triggered": False,
            "loaded_memories": [],
            "suggested_context": "",
            "related_knowledge": []
        }
        
        # 检查触发器
        for trigger in self.triggers.values():
            if not trigger.is_active:
                continue
            
            if trigger.check_trigger(text):
                trigger.trigger_count += 1
                result["triggered"] = True
                
                if self.backend:
                    self.backend.increment_trigger_count(trigger.id)
                
                # 加载记忆
                for mem_id in trigger.target_memory_ids:
                    if mem_id in self.episodic_memory:
                        episode = self.episodic_memory[mem_id]
                        episode.touch()
                        
                        # 检查置信度
                        conf = self.confidence_tracker.get_confidence(mem_id)
                        if conf >= 0.5:  # 只显示置信度足够的记忆
                            result["loaded_memories"].append({
                                "type": "episodic",
                                "content": episode.to_natural_language(),
                                "confidence": conf
                            })
        
        # 检索相关知识
        knowledge_results = self.knowledge.query(text, top_k=3)
        for doc, score in knowledge_results:
            result["related_knowledge"].append({
                "content": doc.content,
                "similarity": score,
                "source": doc.source
            })
        
        # 组装上下文
        context_parts = []
        for mem in result["loaded_memories"]:
            if mem["confidence"] >= 0.7:
                context_parts.append(f"[记忆] {mem['content']}")
            else:
                context_parts.append(f"[可能相关] {mem['content']} (置信度: {mem['confidence']:.2f})")
        
        for know in result["related_knowledge"]:
            context_parts.append(f"[知识] {know['content'][:100]}...")
        
        result["suggested_context"] = "\n".join(context_parts)
        
        return result
    
    def _auto_create_trigger(self, topics: List[str], memory_ids: List[str]):
        """自动创建触发器"""
        for topic in topics:
            exists = any(topic in t.keywords for t in self.triggers.values())
            if not exists:
                self.create_trigger([topic], memory_ids)
    
    # ========== 遗忘管理 ==========
    
    def run_forgetting_cycle(self) -> Dict[str, Any]:
        """运行遗忘周期"""
        if not self.backend:
            return {"error": "Persistence not enabled"}
        
        # 获取高风险记忆
        at_risk_ids = self.backend.get_high_forgetting_risk_memories(threshold=0.8)
        
        deleted = []
        for mem_id in at_risk_ids:
            # 检查不是 CRITICAL 优先级
            if mem_id in self.episodic_memory:
                episode = self.episodic_memory[mem_id]
                if episode.priority != MemoryPriority.CRITICAL:
                    # 删除
                    self.backend.delete_episodic_memory(mem_id)
                    del self.episodic_memory[mem_id]
                    deleted.append(mem_id)
        
        return {
            "checked": len(at_risk_ids),
            "deleted": len(deleted),
            "deleted_ids": deleted
        }
    
    # ========== 知识管理 ==========
    
    def add_knowledge(
        self,
        content: str,
        metadata: Optional[Dict] = None,
        source: str = ""
    ) -> str:
        """添加知识"""
        return self.knowledge.add_knowledge(content, metadata, source)
    
    def query_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        """查询知识"""
        results = self.knowledge.query(query, top_k=top_k)
        return [
            {
                "content": doc.content,
                "similarity": score,
                "metadata": doc.metadata
            }
            for doc, score in results
        ]
    
    # ========== 用户偏好 ==========
    
    def update_user_preference(
        self,
        user_id: str,
        key: str,
        value: Any,
        confidence: float = 1.0,
        source: MemorySource = MemorySource.EXPLICIT
    ):
        """更新用户偏好"""
        if self.backend:
            self.backend.save_user_memory(
                user_id, key, value,
                confidence=confidence,
                source=source.value
            )
        
        # 注册置信度
        mem_id = f"{user_id}_{key}"
        self.confidence_tracker.register_memory(
            mem_id, source, confidence
        )
    
    # ========== 统计和报告 ==========
    
    def get_health_report(self) -> Dict[str, Any]:
        """获取系统健康报告"""
        report = {
            "episodic_memory": {
                "count": len(self.episodic_memory),
                "by_priority": self._count_by_priority()
            },
            "triggers": {
                "count": len(self.triggers),
                "total_triggered": sum(t.trigger_count for t in self.triggers.values())
            },
            "knowledge": self.knowledge.get_stats(),
            "confidence": {
                "low_confidence_memories": len(
                    self.confidence_tracker.get_low_confidence_memories(0.5)
                )
            }
        }
        
        if self.backend:
            db_stats = self.backend.get_memory_stats()
            report["database"] = db_stats
        
        return report
    
    def _count_by_priority(self) -> Dict[str, int]:
        """按优先级统计"""
        counts = {}
        for p in MemoryPriority:
            counts[p.name] = sum(
                1 for e in self.episodic_memory.values()
                if e.priority == p
            )
        return counts


# 完整演示
if __name__ == "__main__":
    print("🧠 Enhanced MemCore 完整演示")
    print("=" * 60)
    
    # 初始化
    mc = MemCoreEnhanced(enable_persistence=False)
    
    # 1. 记录情景
    print("\n📌 记录情景记忆...")
    ep1 = mc.record_episode(
        context_summary="用户询问 MemCore 优化",
        conclusion="用户是 MemCore 开发者，想要四个新功能",
        related_topics=["MemCore", "AI记忆"],
        priority=MemoryPriority.HIGH,
        confidence=1.0
    )
    print(f"   记录情景: {ep1}")
    
    # 2. 添加知识
    print("\n📚 添加知识...")
    mc.add_knowledge(
        content="MemCore 采用五层记忆架构: Context/Task/User/Knowledge/Experience",
        metadata={"topics": ["MemCore", "architecture"]},
        source="docs"
    )
    
    # 3. 触发器测试
    print("\n🎯 测试触发器...")
    result = mc.process_input("我想继续搞 MemCore 的优化")
    print(f"   触发结果: {result['triggered']}")
    print(f"   加载记忆: {len(result['loaded_memories'])}")
    print(f"   相关知识: {len(result['related_knowledge'])}")
    
    if result['suggested_context']:
        print(f"   建议上下文:\n   {result['suggested_context'][:200]}...")
    
    # 4. 置信度验证
    print("\n✅ 验证记忆...")
    mc.confidence_tracker.verify(ep1, verifier="user")
    print(f"   验证后置信度: {mc.confidence_tracker.get_confidence(ep1):.2f}")
    
    # 5. 健康报告
    print("\n📊 系统健康报告:")
    health = mc.get_health_report()
    print(json.dumps(health, indent=2, default=str))
    
    print("\n" + "=" * 60)
    print("✅ 演示完成! Enhanced MemCore 可正常工作~")
