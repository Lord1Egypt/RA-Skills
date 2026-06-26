"""
Memory Conflict Resolution for Enhanced MemCore
记忆冲突解决器
处理新旧记忆之间的矛盾
"""

import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import difflib


class ConflictStrategy(Enum):
    """冲突解决策略"""
    TIME_PRIORITY = "time"           # 新的覆盖旧的
    CONFIDENCE_PRIORITY = "confidence"  # 高置信度优先
    MERGE = "merge"                  # 合并如果可能
    KEEP_BOTH = "keep_both"          # 保留两者，标记冲突
    MANUAL_REVIEW = "manual"         # 交给用户确认


@dataclass
class MemoryConflict:
    """记忆冲突记录"""
    new_memory: Any
    existing_memory: Any
    conflict_type: str  # 'contradiction' | 'update' | 'duplicate'
    similarity_score: float  # 主题相似度
    suggested_action: str
    resolved: bool = False
    resolution: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class MemoryConflictResolver:
    """
    记忆冲突解决器
    
    使用场景：
    1. 新记忆与旧记忆矛盾
    2. 多源导入时的数据冲突
    3. 用户反馈导致的记忆修正
    """
    
    def __init__(
        self,
        default_strategy: ConflictStrategy = ConflictStrategy.CONFIDENCE_PRIORITY,
        similarity_threshold: float = 0.6
    ):
        self.default_strategy = default_strategy
        self.similarity_threshold = similarity_threshold  # 判断相似的阈值
        self.conflict_history: List[MemoryConflict] = []
    
    def detect_conflict(
        self,
        new_memory: Any,
        existing_memories: List[Any],
        check_fields: Optional[List[str]] = None
    ) -> List[MemoryConflict]:
        """
        检测潜在冲突
        
        Args:
            new_memory: 新记忆
            existing_memories: 已有记忆列表
            check_fields: 用于比较的字段
            
        Returns:
            冲突列表
        """
        conflicts = []
        
        for existing in existing_memories:
            # 计算主题相似度
            similarity = self._calculate_similarity(new_memory, existing, check_fields)
            
            if similarity >= self.similarity_threshold:
                # 检查是否矛盾
                is_contradiction, reason = self._is_contradictory(
                    new_memory, existing, check_fields
                )
                
                if is_contradiction:
                    conflict = MemoryConflict(
                        new_memory=new_memory,
                        existing_memory=existing,
                        conflict_type='contradiction',
                        similarity_score=similarity,
                        suggested_action=self._suggest_action(new_memory, existing)
                    )
                    conflicts.append(conflict)
                elif similarity > 0.9:
                    # 高度相似，可能是重复
                    conflict = MemoryConflict(
                        new_memory=new_memory,
                        existing_memory=existing,
                        conflict_type='duplicate',
                        similarity_score=similarity,
                        suggested_action='skip'
                    )
                    conflicts.append(conflict)
        
        return conflicts
    
    def resolve(
        self,
        new_memory: Any,
        conflicts: List[MemoryConflict],
        strategy: Optional[ConflictStrategy] = None
    ) -> Tuple[Any, List[MemoryConflict]]:
        """
        解决冲突
        
        Returns:
            (处理后的记忆, 更新后的冲突记录)
        """
        strategy = strategy or self.default_strategy
        
        if not conflicts:
            return new_memory, []
        
        # 按相似度排序，先处理最相似的
        conflicts.sort(key=lambda x: x.similarity_score, reverse=True)
        primary_conflict = conflicts[0]
        existing = primary_conflict.existing_memory
        
        if strategy == ConflictStrategy.TIME_PRIORITY:
            # 新的覆盖旧的
            new_memory = self._mark_outdated(existing)
            primary_conflict.resolved = True
            primary_conflict.resolution = "new_replaces_old"
            
        elif strategy == ConflictStrategy.CONFIDENCE_PRIORITY:
            # 比较置信度
            new_conf = getattr(new_memory, 'confidence', 1.0)
            old_conf = getattr(existing, 'confidence', 1.0)
            
            if new_conf >= old_conf:
                existing = self._mark_outdated(existing)
                primary_conflict.resolved = True
                primary_conflict.resolution = "higher_confidence_new"
            else:
                new_memory = self._mark_pending(new_memory)
                primary_conflict.resolved = True
                primary_conflict.resolution = "lower_confidence_pending"
                
        elif strategy == ConflictStrategy.MERGE:
            # 尝试合并
            merged = self._attempt_merge(new_memory, existing)
            if merged:
                new_memory = merged
                primary_conflict.resolved = True
                primary_conflict.resolution = "merged"
            else:
                # 合并失败，保留两者
                new_memory = self._mark_alternate(new_memory, existing)
                primary_conflict.resolved = True
                primary_conflict.resolution = "kept_both"
                
        elif strategy == ConflictStrategy.KEEP_BOTH:
            # 标记为不同版本
            new_memory = self._mark_alternate(new_memory, existing)
            primary_conflict.resolved = True
            primary_conflict.resolution = "kept_both"
            
        elif strategy == ConflictStrategy.MANUAL_REVIEW:
            # 标记为待确认
            new_memory = self._mark_pending(new_memory, conflicts)
            # 不标记为resolved，等待用户
        
        # 记录冲突历史
        self.conflict_history.extend(conflicts)
        
        return new_memory, conflicts
    
    def _calculate_similarity(
        self,
        mem1: Any,
        mem2: Any,
        check_fields: Optional[List[str]] = None
    ) -> float:
        """计算两条记忆的相似度"""
        
        # 如果有 key 字段，直接比较
        if hasattr(mem1, 'key') and hasattr(mem2, 'key'):
            if mem1.key == mem2.key:
                return 1.0
        
        # 如果有 context_summary，比较文本相似度
        text1 = self._get_comparable_text(mem1, check_fields)
        text2 = self._get_comparable_text(mem2, check_fields)
        
        return difflib.SequenceMatcher(None, text1, text2).ratio()
    
    def _get_comparable_text(self, memory: Any, fields: Optional[List[str]]) -> str:
        """获取可比较的文本"""
        if fields:
            parts = []
            for field in fields:
                val = getattr(memory, field, '')
                parts.append(str(val))
            return ' '.join(parts)
        
        # 默认字段
        for attr in ['content', 'context_summary', 'conclusion', 'value']:
            if hasattr(memory, attr):
                return str(getattr(memory, attr))
        
        return str(memory)
    
    def _is_contradictory(
        self,
        mem1: Any,
        mem2: Any,
        check_fields: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        """判断两条记忆是否矛盾"""
        
        # 如果是同一个 key 但 value 不同，则矛盾
        if hasattr(mem1, 'key') and hasattr(mem2, 'key'):
            if mem1.key == mem2.key:
                val1 = getattr(mem1, 'value', None) or getattr(mem1, 'content', None)
                val2 = getattr(mem2, 'value', None) or getattr(mem2, 'content', None)
                if val1 != val2:
                    return True, f"同一键 '{mem1.key}' 但值不同: {val1} vs {val2}"
        
        # 检查结论矛盾（针对情景记忆）
        if hasattr(mem1, 'conclusion') and hasattr(mem2, 'conclusion'):
            # 如果主题相似但结论完全不同，则可能矛盾
            topics1 = set(getattr(mem1, 'related_topics', []))
            topics2 = set(getattr(mem2, 'related_topics', []))
            
            if topics1 & topics2:  # 有共同主题
                # 简单的反义词检查
                concl1 = mem1.conclusion.lower()
                concl2 = mem2.conclusion.lower()
                
                antonyms = [
                    ('喜欢', '讨厌'),
                    ('赞同', '反对'),
                    ('是', '不是'),
                    ('true', 'false'),
                    ('yes', 'no'),
                    ('good', 'bad')
                ]
                
                for pos, neg in antonyms:
                    if (pos in concl1 and neg in concl2) or (neg in concl1 and pos in concl2):
                        return True, f"结论可能矛盾: {mem1.conclusion} vs {mem2.conclusion}"
        
        return False, ""
    
    def _suggest_action(self, new_mem: Any, existing_mem: Any) -> str:
        """根据特征建议处理方式"""
        new_conf = getattr(new_mem, 'confidence', 1.0)
        old_conf = getattr(existing_mem, 'confidence', 1.0)
        new_time = getattr(new_mem, 'timestamp', datetime.now())
        old_time = getattr(existing_mem, 'timestamp', datetime.now())
        
        if new_conf > old_conf:
            return "新记忆置信度更高，建议覆盖"
        elif new_time > old_time:
            return "新记忆更新，建议更新"
        else:
            return "存在冲突，需要确认"
    
    def _mark_outdated(self, memory: Any) -> Any:
        """标记记忆为过时"""
        if hasattr(memory, 'is_outdated'):
            memory.is_outdated = True
        if hasattr(memory, 'metadata'):
            memory.metadata['status'] = 'outdated'
        return memory
    
    def _mark_pending(self, memory: Any, conflicts: List[MemoryConflict] = None) -> Any:
        """标记记忆为待确认"""
        if hasattr(memory, 'status'):
            memory.status = 'pending_confirmation'
        if hasattr(memory, 'metadata'):
            memory.metadata['status'] = 'pending'
            if conflicts:
                memory.metadata['conflicts_with'] = [
                    c.existing_memory.id if hasattr(c.existing_memory, 'id') else str(c.existing_memory)
                    for c in conflicts
                ]
        return memory
    
    def _mark_alternate(self, new_memory: Any, existing_memory: Any) -> Any:
        """标记为备选版本"""
        if hasattr(new_memory, 'metadata'):
            new_memory.metadata['alternate_of'] = getattr(existing_memory, 'id', 'unknown')
            new_memory.metadata['version'] = 'alternate'
        return new_memory
    
    def _attempt_merge(self, mem1: Any, mem2: Any) -> Optional[Any]:
        """尝试合并两条记忆"""
        # 简单的合并策略：如果主题相同但结论互补，则合并
        if hasattr(mem1, 'related_topics') and hasattr(mem2, 'related_topics'):
            topics1 = set(mem1.related_topics)
            topics2 = set(mem2.related_topics)
            
            if topics1 == topics2:
                # 创建合并后的记忆
                if hasattr(mem1, 'conclusion') and hasattr(mem2, 'conclusion'):
                    merged_conclusion = f"{mem1.conclusion}; 另一观点: {mem2.conclusion}"
                    
                    # 创建新记忆（复制 mem1 并更新）
                    import copy
                    merged = copy.copy(mem1)
                    merged.conclusion = merged_conclusion
                    merged.metadata = getattr(mem1, 'metadata', {}).copy()
                    merged.metadata['merged_from'] = [
                        getattr(mem1, 'id', 'unknown'),
                        getattr(mem2, 'id', 'unknown')
                    ]
                    return merged
        
        return None
    
    def get_conflict_report(self) -> Dict[str, Any]:
        """获取冲突解决报告"""
        total = len(self.conflict_history)
        resolved = sum(1 for c in self.conflict_history if c.resolved)
        pending = total - resolved
        
        by_type = {}
        for c in self.conflict_history:
            by_type[c.conflict_type] = by_type.get(c.conflict_type, 0) + 1
        
        return {
            'total_conflicts': total,
            'resolved': resolved,
            'pending_review': pending,
            'by_type': by_type,
            'recent_conflicts': [
                {
                    'type': c.conflict_type,
                    'similarity': c.similarity_score,
                    'resolved': c.resolved,
                    'resolution': c.resolution
                }
                for c in self.conflict_history[-5:]
            ]
        }


# 测试代码
if __name__ == "__main__":
    print("🧠 测试 Conflict Resolver...")
    
    from dataclasses import dataclass as dc
    
    @dc
    class SimpleMemory:
        id: str
        key: str
        value: str
        confidence: float = 1.0
        timestamp: datetime = field(default_factory=datetime.now)
        is_outdated: bool = False
        status: str = "active"
        metadata: Dict = field(default_factory=dict)
    
    resolver = MemoryConflictResolver()
    
    # 测试数据
    old_mem = SimpleMemory(
        id="m1",
        key="favorite_language",
        value="Python",
        confidence=0.8
    )
    
    new_mem = SimpleMemory(
        id="m2",
        key="favorite_language",
        value="JavaScript",
        confidence=0.9
    )
    
    # 检测冲突
    conflicts = resolver.detect_conflict(new_mem, [old_mem], check_fields=['key'])
    print(f"检测到 {len(conflicts)} 个冲突")
    
    if conflicts:
        print(f"  冲突类型: {conflicts[0].conflict_type}")
        print(f"  相似度: {conflicts[0].similarity_score:.2f}")
        
        # 解决冲突
        resolved_mem, _ = resolver.resolve(new_mem, conflicts)
        print(f"  解决后状态: {getattr(resolved_mem, 'status', 'unknown')}")
    
    print("\n📊 冲突报告:", resolver.get_conflict_report())
    print("✅ 冲突解决测试完成!")
