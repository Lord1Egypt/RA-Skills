"""
双轨并行架构 - 桶-链融合模块

本模块是融合层的总控，整合关联、验证、摘要功能。
"""

from typing import List, Dict, Any
from pydantic import BaseModel
from ..buckets.topic_cluster import TopicCluster
from ..chains.base_chain import BaseExtractedChain, ChainType
from .bucket_chain_linker import BucketChainLinker, BucketChainLink
from .cross_validator import CrossValidator, ValidationResult
from .multi_dimension_summary import (
    MultiDimensionSummaryGenerator,
    MultiDimensionSummary
)
from ..triggers.coordinated_extraction_trigger import (
    CoordinatedExtractionTrigger,
    ExtractionAction
)


class BucketChainFusion(BaseModel):
    """
    桶-链融合层
    
    整合关联、验证、摘要功能，提供完整的融合服务。
    """
    
    def __init__(self):
        super().__init__()
        self.linker = BucketChainLinker()
        self.validator = CrossValidator()
        self.summary_generator = MultiDimensionSummaryGenerator()
        self.trigger = CoordinatedExtractionTrigger()
    
    def link_buckets_and_chains(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]]
    ) -> List[BucketChainLink]:
        """
        关联桶和链
        
        Args:
            clusters: 话题簇列表
            chains: 链字典
        
        Returns:
            关联列表
        """
        return self.linker.link_buckets_and_chains(clusters, chains)
    
    def validate_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> ValidationResult:
        """
        验证一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            验证结果
        """
        return self.validator.validate_consistency(cluster, chain)
    
    def cross_validate_all(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]],
        links: List[BucketChainLink]
    ) -> List[ValidationResult]:
        """
        交叉验证所有关联
        
        Args:
            clusters: 话题簇列表
            chains: 链字典
            links: 关联列表
        
        Returns:
            验证结果列表
        """
        results = []
        
        for link in links:
            # 找到对应的簇和链
            cluster = next(
                (c for c in clusters if c.cluster_id == link.cluster_id),
                None
            )
            
            if not cluster:
                continue
            
            chain = None
            for chain_type, chain_list in chains.items():
                for c in chain_list:
                    if c.chain_id == link.chain_id:
                        chain = c
                        break
                if chain:
                    break
            
            if not chain:
                continue
            
            # 验证
            result = self.validator.validate_consistency(cluster, chain)
            results.append(result)
        
        return results
    
    def generate_summary(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]],
        links: List[BucketChainLink] = None
    ) -> MultiDimensionSummary:
        """
        生成多维摘要
        
        Args:
            clusters: 话题簇列表
            chains: 链字典
            links: 关联列表（可选）
        
        Returns:
            多维摘要
        """
        return self.summary_generator.generate_summary(clusters, chains, links)
    
    def evaluate_extraction_opportunity(
        self,
        clusters: List[TopicCluster],
        chain_buffers: Dict[ChainType, Any]  # ChainBuffer
    ) -> ExtractionAction:
        """
        评估提炼机会
        
        Args:
            clusters: 话题簇列表
            chain_buffers: 链缓冲区字典
        
        Returns:
            提取动作
        """
        return self.trigger.evaluate_extraction_opportunity(clusters, chain_buffers)
    
    def full_fusion_pipeline(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]],
        chain_buffers: Dict[ChainType, Any] = None
    ) -> Dict[str, Any]:
        """
        完整的融合流程
        
        Args:
            clusters: 话题簇列表
            chains: 链字典
            chain_buffers: 链缓冲区字典（可选）
        
        Returns:
            融合结果字典
        """
        result = {
            "links": [],
            "validations": [],
            "summary": None,
            "action": None,
            "stats": {}
        }
        
        # 步骤1：关联
        links = self.link_buckets_and_chains(clusters, chains)
        result["links"] = links
        result["stats"]["link_count"] = len(links)
        
        # 步骤2：交叉验证
        if links:
            validations = self.cross_validate_all(clusters, chains, links)
            result["validations"] = validations
            
            passed_count = sum(1 for v in validations if v.passed)
            result["stats"]["validation_passed"] = passed_count
            result["stats"]["validation_total"] = len(validations)
        
        # 步骤3：生成摘要
        summary = self.generate_summary(clusters, chains, links)
        result["summary"] = summary
        
        # 步骤4：评估提炼机会（如果有链缓冲区）
        if chain_buffers:
            action = self.evaluate_extraction_opportunity(clusters, chain_buffers)
            result["action"] = action
            result["stats"]["extraction_action"] = action.action
        
        return result
