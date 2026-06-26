"""
双轨并行架构 - 多维摘要模块

本模块实现桶-链融合的多维摘要生成。
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from ..buckets.topic_cluster import TopicCluster
from ..chains.base_chain import BaseExtractedChain, ChainType
from ..chains.causal_chain import ExtractedCausalChain
from ..chains.logic_chain import ExtractedLogicChain
from ..chains.operation_chain import ExtractedOperationChain
from ..chains.narrative_chain import ExtractedNarrativeChain
from ..chains.time_chain import ExtractedTimeChain


class MultiDimensionSummary(BaseModel):
    """
    多维摘要
    
    融合桶和链信息的综合摘要。
    
    Attributes:
        topic_summary: 话题概述
        dominant_keywords: 主导关键词
        causal_summary: 因果摘要
        logic_summary: 逻辑摘要
        operation_summary: 操作摘要
        narrative_summary: 叙事摘要
        time_summary: 时间摘要
        bucket_chain_relations: 桶-链关联关系
        completeness_score: 完整性评分
        consistency_score: 一致性评分
        metadata: 扩展元数据
    """
    
    # 语义维度
    topic_summary: str = Field(description="话题概述")
    dominant_keywords: List[str] = Field(default_factory=list, description="主导关键词")
    
    # 结构维度
    causal_summary: str = Field(default="", description="因果摘要")
    logic_summary: str = Field(default="", description="逻辑摘要")
    operation_summary: str = Field(default="", description="操作摘要")
    narrative_summary: str = Field(default="", description="叙事摘要")
    time_summary: str = Field(default="", description="时间摘要")
    
    # 关联维度
    bucket_chain_relations: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="桶-链关联关系"
    )
    
    # 综合评估
    completeness_score: float = Field(default=0.0, description="完整性评分")
    consistency_score: float = Field(default=0.0, description="一致性评分")
    
    # 元数据
    metadata: Dict = Field(default_factory=dict, description="扩展元数据")
    
    def to_long_term_memory_data(self) -> Dict[str, Any]:
        """
        转换为长期记忆数据
        
        Returns:
            长期记忆数据字典
        """
        # 根据摘要内容映射到相应的记忆类型
        data = {
            "topic": self.topic_summary,
            "keywords": self.dominant_keywords,
            "causal": self.causal_summary,
            "logic": self.logic_summary,
            "operation": self.operation_summary,
            "narrative": self.narrative_summary,
            "time": self.time_summary,
            "relations": self.bucket_chain_relations,
            "quality": {
                "completeness": self.completeness_score,
                "consistency": self.consistency_score
            }
        }
        
        return data
    
    def get_text_summary(self, max_length: int = 500) -> str:
        """
        生成文本摘要
        
        Args:
            max_length: 最大长度
        
        Returns:
            文本摘要
        """
        parts = []
        
        # 话题概述
        if self.topic_summary:
            parts.append(f"话题: {self.topic_summary}")
        
        # 结构摘要
        if self.causal_summary:
            parts.append(f"因果: {self.causal_summary}")
        if self.logic_summary:
            parts.append(f"逻辑: {self.logic_summary}")
        if self.operation_summary:
            parts.append(f"操作: {self.operation_summary}")
        if self.narrative_summary:
            parts.append(f"叙事: {self.narrative_summary}")
        if self.time_summary:
            parts.append(f"时间: {self.time_summary}")
        
        # 组合摘要
        summary = "\n".join(parts)
        
        # 截断
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
        
        return summary


class MultiDimensionSummaryGenerator(BaseModel):
    """
    多维摘要生成器
    
    融合桶和链信息生成多维摘要。
    """
    
    def generate_summary(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]],
        links: List[Any] = None
    ) -> MultiDimensionSummary:
        """
        生成多维摘要
        
        Args:
            clusters: 话题簇列表
            chains: 链类型到链列表的映射
            links: 桶-链关联列表（可选）
        
        Returns:
            多维摘要
        """
        # 生成语义维度摘要
        topic_summary, dominant_keywords = self._generate_topic_summary(clusters)
        
        # 生成结构维度摘要
        chain_summaries = self._generate_chain_summaries(chains)
        
        # 生成关联维度摘要
        bucket_chain_relations = self._generate_relations_summary(links)
        
        # 计算综合评估
        completeness, consistency = self._calculate_scores(
            clusters, chains
        )
        
        # 创建摘要对象
        summary = MultiDimensionSummary(
            topic_summary=topic_summary,
            dominant_keywords=dominant_keywords,
            causal_summary=chain_summaries.get("causal", ""),
            logic_summary=chain_summaries.get("logic", ""),
            operation_summary=chain_summaries.get("operation", ""),
            narrative_summary=chain_summaries.get("narrative", ""),
            time_summary=chain_summaries.get("time", ""),
            bucket_chain_relations=bucket_chain_relations,
            completeness_score=completeness,
            consistency_score=consistency
        )
        
        return summary
    
    def _generate_topic_summary(
        self,
        clusters: List[TopicCluster]
    ) -> tuple[str, List[str]]:
        """
        生成话题摘要
        
        Args:
            clusters: 话题簇列表
        
        Returns:
            (话题概述, 主导关键词列表)
        """
        if not clusters:
            return "无话题信息", []
        
        # 选择优先级最高的簇
        top_cluster = max(clusters, key=lambda c: c.priority)
        
        # 话题概述
        topic_summary = f"{top_cluster.topic_label}（{len(top_cluster.items)}项）"
        
        # 主导关键词
        dominant_keywords = list(top_cluster.keywords)[:5]
        
        return topic_summary, dominant_keywords
    
    def _generate_chain_summaries(
        self,
        chains: Dict[ChainType, List[BaseExtractedChain]]
    ) -> Dict[str, str]:
        """
        生成链摘要
        
        Args:
            chains: 链字典
        
        Returns:
            链类型到摘要的映射
        """
        summaries = {}
        
        for chain_type, chain_list in chains.items():
            if not chain_list:
                continue
            
            # 选择置信度最高的链
            top_chain = max(chain_list, key=lambda c: c.extraction_confidence)
            
            # 生成摘要
            summary = top_chain.to_summary()
            summaries[chain_type.value] = summary
        
        return summaries
    
    def _generate_relations_summary(
        self,
        links: List[Any]
    ) -> List[Dict[str, Any]]:
        """
        生成关联摘要
        
        Args:
            links: 关联列表
        
        Returns:
            关联摘要列表
        """
        if not links:
            return []
        
        relations = []
        
        for link in links[:10]:  # 最多返回10个关联
            relation = {
                "cluster_id": getattr(link, 'cluster_id', ''),
                "chain_id": getattr(link, 'chain_id', ''),
                "strength": getattr(link, 'strength', 0.0),
                "link_type": getattr(link, 'link_type', '')
            }
            relations.append(relation)
        
        return relations
    
    def _calculate_scores(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]]
    ) -> tuple[float, float]:
        """
        计算综合评估分数
        
        Args:
            clusters: 话题簇列表
            chains: 链字典
        
        Returns:
            (完整性得分, 一致性得分)
        """
        # 完整性：基于覆盖的维度
        dimensions = 0
        if clusters:
            dimensions += 1
        for chain_type in [ChainType.CAUSAL, ChainType.LOGIC, ChainType.OPERATION]:
            if chain_type in chains and chains[chain_type]:
                dimensions += 1
        
        # 最多5个维度（话题 + 4种链类型）
        completeness = dimensions / 5.0
        
        # 一致性：基于质量和置信度
        quality_factors = []
        
        if clusters:
            avg_coherence = sum(c.coherence for c in clusters) / len(clusters)
            quality_factors.append(avg_coherence)
        
        for chain_list in chains.values():
            if chain_list:
                avg_confidence = sum(
                    c.extraction_confidence 
                    for c in chain_list
                ) / len(chain_list)
                quality_factors.append(avg_confidence)
        
        if quality_factors:
            consistency = sum(quality_factors) / len(quality_factors)
        else:
            consistency = 0.0
        
        return completeness, consistency
