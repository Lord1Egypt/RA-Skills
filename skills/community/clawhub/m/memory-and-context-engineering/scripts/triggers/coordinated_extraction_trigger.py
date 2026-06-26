"""
双轨并行架构 - 协同提取触发器模块

本模块实现协同提炼的决策逻辑。
"""

from typing import List, Dict
from pydantic import BaseModel, Field
from ..buckets.topic_cluster import TopicCluster
from ..chains.base_chain import ChainType
from ..chains.chain_buffer import ChainBuffer


class ExtractionAction(BaseModel):
    """
    提取动作
    
    Attributes:
        action: 动作类型
        reason: 原因说明
        confidence: 置信度（0-1）
        factors: 因素字典
        target_pairs: 目标对列表
        metadata: 扩展元数据
    """
    
    action: str = Field(description="动作类型: COORDINATED_EXTRACTION/BUCKET_EXTRACTION/CHAIN_EXTRACTION/WAIT")
    reason: str = Field(description="原因说明")
    confidence: float = Field(ge=0.0, le=1.0, description="置信度")
    factors: Dict = Field(default_factory=dict, description="决策因素")
    target_pairs: List[tuple] = Field(default_factory=list, description="目标对")
    metadata: Dict = Field(default_factory=dict, description="扩展元数据")


class CoordinatedExtractionTrigger(BaseModel):
    """
    协同提取触发器
    
    评估是否应该进行协同提炼。
    """
    
    # 阈值配置
    BUCKET_READINESS_THRESHOLD: float = 0.7
    CHAIN_READINESS_THRESHOLD: float = 0.7
    COMPLEMENTARITY_THRESHOLD: float = 0.5
    COORDINATION_THRESHOLD: float = 0.7
    
    def evaluate_extraction_opportunity(
        self,
        clusters: List[TopicCluster],
        chain_buffers: Dict[ChainType, ChainBuffer]
    ) -> ExtractionAction:
        """
        评估提炼机会
        
        Args:
            clusters: 话题簇列表
            chain_buffers: 链缓冲区字典
        
        Returns:
            提取动作
        """
        # 检查1：桶是否达到提取条件
        bucket_ready = self._check_bucket_readiness(clusters)
        
        # 检查2：链是否达到提取条件
        chain_ready = self._check_chain_readiness(chain_buffers)
        
        # 检查3：桶-链是否形成互补组合
        complementary_pairs = self._find_complementary_pairs(
            clusters,
            chain_buffers
        )
        complementarity_score = self._calculate_complementarity_score(
            complementary_pairs
        )
        
        # 检查4：整体质量评估
        quality_score = self._check_overall_quality(clusters, chain_buffers)
        
        # 决策因素
        factors = {
            "bucket_ready": bucket_ready,
            "chain_ready": chain_ready,
            "complementarity": complementarity_score,
            "quality": quality_score
        }
        
        # 决策逻辑
        if bucket_ready and chain_ready and complementarity_score >= self.COMPLEMENTARITY_THRESHOLD:
            # 协同提取
            score = (
                bucket_ready * 0.3 +
                chain_ready * 0.3 +
                complementarity_score * 0.25 +
                quality_score * 0.15
            )
            
            if score >= self.COORDINATION_THRESHOLD:
                return ExtractionAction(
                    action="COORDINATED_EXTRACTION",
                    reason=f"桶和链都满足条件，且互补性得分 {complementarity_score:.2f}",
                    confidence=score,
                    factors=factors,
                    target_pairs=complementary_pairs
                )
        
        if bucket_ready:
            return ExtractionAction(
                action="BUCKET_EXTRACTION",
                reason="桶满足提取条件",
                confidence=bucket_ready,
                factors=factors
            )
        
        if chain_ready:
            return ExtractionAction(
                action="CHAIN_EXTRACTION",
                reason="链满足提取条件",
                confidence=chain_ready,
                factors=factors
            )
        
        return ExtractionAction(
            action="WAIT",
            reason="未达到提取条件",
            confidence=0.0,
            factors=factors
        )
    
    def _check_bucket_readiness(self, clusters: List[TopicCluster]) -> float:
        """
        检查桶就绪状态
        
        Args:
            clusters: 话题簇列表
        
        Returns:
            就绪分数（0-1）
        """
        if not clusters:
            return 0.0
        
        ready_clusters = [
            c for c in clusters 
            if c.is_ready_for_extraction(self.BUCKET_READINESS_THRESHOLD)
        ]
        
        # 就绪簇的比例
        readiness_ratio = len(ready_clusters) / len(clusters)
        
        # 平均优先级
        avg_priority = sum(c.priority for c in clusters) / len(clusters)
        
        # 综合评分
        score = (readiness_ratio * 0.7) + (avg_priority * 0.3)
        
        return score
    
    def _check_chain_readiness(self, chain_buffers: Dict[ChainType, ChainBuffer]) -> float:
        """
        检查链就绪状态
        
        Args:
            chain_buffers: 链缓冲区字典
        
        Returns:
            就绪分数（0-1）
        """
        if not chain_buffers:
            return 0.0
        
        ready_count = 0
        total_confidence = 0.0
        
        for chain_type, buffer in chain_buffers.items():
            # 检查缓冲区是否就绪
            if buffer.avg_confidence >= self.CHAIN_READINESS_THRESHOLD:
                ready_count += 1
            total_confidence += buffer.avg_confidence
        
        # 就绪缓冲区的比例
        readiness_ratio = ready_count / len(chain_buffers)
        
        # 平均置信度
        avg_confidence = total_confidence / len(chain_buffers)
        
        # 综合评分
        score = (readiness_ratio * 0.7) + (avg_confidence * 0.3)
        
        return score
    
    def _find_complementary_pairs(
        self,
        clusters: List[TopicCluster],
        chain_buffers: Dict[ChainType, ChainBuffer]
    ) -> List[tuple]:
        """
        寻找互补的桶-链对
        
        Args:
            clusters: 话题簇列表
            chain_buffers: 链缓冲区字典
        
        Returns:
            互补对列表 [(cluster_id, chain_id), ...]
        """
        pairs = []
        
        for cluster in clusters:
            # 只检查有相关链的簇
            if cluster.related_chains:
                for chain_id in cluster.related_chains:
                    pairs.append((cluster.cluster_id, chain_id))
        
        return pairs
    
    def _calculate_complementarity_score(self, pairs: List[tuple]) -> float:
        """
        计算互补性得分
        
        Args:
            pairs: 互补对列表
        
        Returns:
            互补性得分（0-1）
        """
        if not pairs:
            return 0.0
        
        # 简化计算：基于互补对的数量
        # 假设5个互补对为满分
        score = min(1.0, len(pairs) / 5.0)
        
        return score
    
    def _check_overall_quality(
        self,
        clusters: List[TopicCluster],
        chain_buffers: Dict[ChainType, ChainBuffer]
    ) -> float:
        """
        检查整体质量
        
        Args:
            clusters: 话题簇列表
            chain_buffers: 链缓冲区字典
        
        Returns:
            质量得分（0-1）
        """
        factors = []
        
        # 桶的质量
        if clusters:
            avg_coherence = sum(c.coherence for c in clusters) / len(clusters)
            factors.append(avg_coherence)
        
        # 链的质量
        if chain_buffers:
            avg_chain_confidence = sum(
                b.avg_confidence 
                for b in chain_buffers.values()
            ) / len(chain_buffers)
            factors.append(avg_chain_confidence)
        
        if not factors:
            return 0.0
        
        return sum(factors) / len(factors)
    
    def update_thresholds(
        self,
        bucket_threshold: float | None = None,
        chain_threshold: float | None = None,
        complementarity_threshold: float | None = None,
        coordination_threshold: float | None = None
    ) -> None:
        """
        更新阈值配置
        
        Args:
            bucket_threshold: 桶就绪阈值
            chain_threshold: 链就绪阈值
            complementarity_threshold: 互补性阈值
            coordination_threshold: 协同阈值
        """
        if bucket_threshold is not None:
            self.BUCKET_READINESS_THRESHOLD = bucket_threshold
        
        if chain_threshold is not None:
            self.CHAIN_READINESS_THRESHOLD = chain_threshold
        
        if complementarity_threshold is not None:
            self.COMPLEMENTARITY_THRESHOLD = complementarity_threshold
        
        if coordination_threshold is not None:
            self.COORDINATION_THRESHOLD = coordination_threshold
