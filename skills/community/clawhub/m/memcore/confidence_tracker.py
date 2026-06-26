"""
Confidence Tracking for Enhanced MemCore
记忆置信度跟踪系统
每条记忆都有可置信度和来源溯源
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MemorySource(Enum):
    """记忆来源类型"""
    EXPLICIT = "explicit"           # 用户明确说的
    IMPLICIT = "implicit"           # 系统推断的
    INFERRED = "inferred"           # 基于上下文推断
    IMPORTED = "imported"           # 从外部导入
    DERIVED = "derived"             # 派生自其他记忆


@dataclass
class MemoryProvenance:
    """记忆溯源信息"""
    source: MemorySource
    original_query: Optional[str] = None  # 原始用户查询
    extraction_method: str = ""           # 提取方法
    parent_memory_id: Optional[str] = None  # 父记忆ID
    created_by: str = "system"            # 创建者
    chain_of_thought: List[str] = field(default_factory=list)  # 推理链
    verification_history: List[Dict] = field(default_factory=list)


@dataclass
class ConfidenceMetrics:
    """置信度指标"""
    base_confidence: float = 1.0           # 基础置信度
    verification_count: int = 0          # 验证次数
    contradiction_count: int = 0         # 被质疑次数
    access_count: int = 0                # 被使用次数
    last_verified: Optional[datetime] = None
    stability_score: float = 1.0         # 稳定性分数
    
    @property
    def effective_confidence(self) -> float:
        """计算有效置信度"""
        # 验证次数加成
        verification_bonus = min(self.verification_count * 0.1, 0.3)
        
        # 矛盾惩罚
        contradiction_penalty = min(self.contradiction_count * 0.2, 0.5)
        
        # 时间衰减（如果很久没验证）
        time_penalty = 0
        if self.last_verified:
            days_since = (datetime.now() - self.last_verified).days
            time_penalty = min(days_since * 0.01, 0.2)
        
        confidence = self.base_confidence + verification_bonus - contradiction_penalty - time_penalty
        return max(0.1, min(1.0, confidence))  # 限制在 0.1-1.0


class ConfidenceTracker:
    """
    记忆置信度跟踪器
    负责：
    1. 记录来源
    2. 跟踪验证
    3. 计算置信度
    4. 提供溯源链
    """
    
    def __init__(self):
        self.provenance_store: Dict[str, MemoryProvenance] = {}
        self.confidence_store: Dict[str, ConfidenceMetrics] = {}
    
    def register_memory(
        self,
        memory_id: str,
        source: MemorySource,
        base_confidence: float = 1.0,
        **metadata
    ) -> ConfidenceMetrics:
        """
        注册新记忆的溯源信息
        
        Args:
            memory_id: 记忆唯一ID
            source: 来源类型
            base_confidence: 基础置信度
            **metadata: 额外元数据
        """
        # 创建溯源记录
        provenance = MemoryProvenance(
            source=source,
            original_query=metadata.get('original_query'),
            extraction_method=metadata.get('extraction_method', 'direct'),
            parent_memory_id=metadata.get('parent_memory_id'),
            created_by=metadata.get('created_by', 'system'),
            chain_of_thought=metadata.get('chain_of_thought', [])
        )
        self.provenance_store[memory_id] = provenance
        
        # 创建置信度指标
        metrics = ConfidenceMetrics(
            base_confidence=base_confidence,
            verification_count=0,
            contradiction_count=0
        )
        self.confidence_store[memory_id] = metrics
        
        return metrics
    
    def verify(self, memory_id: str, verifier: str = "user", notes: str = ""):
        """
        验证记忆（增加置信度）
        
        Args:
            memory_id: 记忆ID
            verifier: 验证者
            notes: 验证注释
        """
        if memory_id not in self.confidence_store:
            return
        
        metrics = self.confidence_store[memory_id]
        metrics.verification_count += 1
        metrics.last_verified = datetime.now()
        
        # 记录验证历史
        if memory_id in self.provenance_store:
            self.provenance_store[memory_id].verification_history.append({
                'timestamp': datetime.now().isoformat(),
                'verifier': verifier,
                'notes': notes
            })
    
    def contradict(self, memory_id: str, reason: str = ""):
        """
        质疑/否定记忆（降低置信度）
        """
        if memory_id not in self.confidence_store:
            return
        
        metrics = self.confidence_store[memory_id]
        metrics.contradiction_count += 1
        metrics.stability_score *= 0.8  # 稳定性下降
        
        if memory_id in self.provenance_store:
            self.provenance_store[memory_id].verification_history.append({
                'timestamp': datetime.now().isoformat(),
                'verifier': 'user',
                'notes': f"被质疑: {reason}",
                'type': 'contradiction'
            })
    
    def get_confidence(self, memory_id: str) -> float:
        """获取记忆的有效置信度"""
        if memory_id not in self.confidence_store:
            return 0.5  # 未知记忆给中等置信度
        
        return self.confidence_store[memory_id].effective_confidence
    
    def get_provenance(self, memory_id: str) -> Optional[MemoryProvenance]:
        """获取记忆溯源"""
        return self.provenance_store.get(memory_id)
    
    def get_confidence_report(self, memory_id: str) -> Dict[str, Any]:
        """获取详细的置信度报告"""
        if memory_id not in self.confidence_store:
            return {"error": "Memory not found"}
        
        metrics = self.confidence_store[memory_id]
        provenance = self.provenance_store.get(memory_id)
        
        return {
            'memory_id': memory_id,
            'effective_confidence': metrics.effective_confidence,
            'base_confidence': metrics.base_confidence,
            'verification_count': metrics.verification_count,
            'contradiction_count': metrics.contradiction_count,
            'stability_score': metrics.stability_score,
            'source': provenance.source.value if provenance else 'unknown',
            'extraction_method': provenance.extraction_method if provenance else 'unknown',
            'verification_history': provenance.verification_history if provenance else [],
            'trust_level': self._categorize_trust(metrics.effective_confidence)
        }
    
    def _categorize_trust(self, confidence: float) -> str:
        """将置信度分类为信任等级"""
        if confidence >= 0.9:
            return "💚 高度可信 (High Trust)"
        elif confidence >= 0.7:
            return "💛 可信 (Trusted)"
        elif confidence >= 0.5:
            return "💚 需要验证 (Needs Verification)"
        else:
            return "🔴 可疑 (Questionable)"
    
    def export_provenance_chain(self, memory_id: str) -> List[Dict]:
        """
        导出溯源链（追溯到原始来源）"""
        chain = []
        current_id = memory_id
        
        while current_id:
            provenance = self.provenance_store.get(current_id)
            if not provenance:
                break
            
            metrics = self.confidence_store.get(current_id)
            chain.append({
                'memory_id': current_id,
                'source': provenance.source.value,
                'confidence': metrics.effective_confidence if metrics else 0,
                'extraction_method': provenance.extraction_method
            })
            
            current_id = provenance.parent_memory_id
        
        return list(reversed(chain))  # 从原始到当前
    
    def get_low_confidence_memories(self, threshold: float = 0.5) -> List[str]:
        """获取低置信度的记忆ID列表"""
        low_conf = []
        for mem_id, metrics in self.confidence_store.items():
            if metrics.effective_confidence < threshold:
                low_conf.append(mem_id)
        return low_conf


# 测试代码
if __name__ == "__main__":
    print("🧠 测试 Confidence Tracker...")
    
    tracker = ConfidenceTracker()
    
    # 注册新记忆
    print("\n✅ 注册记忆...")
    tracker.register_memory(
        memory_id="mem_001",
        source=MemorySource.EXPLICIT,
        base_confidence=1.0,
        extraction_method="user_input",
        original_query="我叫露丝"
    )
    
    tracker.register_memory(
        memory_id="mem_002",
        source=MemorySource.INFERRED,
        base_confidence=0.6,
        extraction_method="context_inference",
        original_query=""
    )
    
    # 查看置信度
    print(f"mem_001 置信度: {tracker.get_confidence('mem_001'):.2f}")
    print(f"mem_002 置信度: {tracker.get_confidence('mem_002'):.2f}")
    
    # 验证记忆
    print("\n✅ 用户验证记忆...")
    tracker.verify("mem_001", verifier="user", notes="确认正确")
    tracker.verify("mem_001", verifier="user")
    
    print(f"mem_001 验证后置信度: {tracker.get_confidence('mem_001'):.2f}")
    
    # 质疑记忆
    print("\n❌ 质疑记忆...")
    tracker.contradict("mem_002", reason="用户否认")
    print(f"mem_002 质疑后置信度: {tracker.get_confidence('mem_002'):.2f}")
    
    # 详细报告
    print("\n📊 置信度报告 mem_001:")
    report = tracker.get_confidence_report("mem_001")
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    print("✅ 置信度跟踪测试完成!")
