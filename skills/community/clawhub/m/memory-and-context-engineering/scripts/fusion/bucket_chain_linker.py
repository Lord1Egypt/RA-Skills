"""
双轨并行架构 - 桶-链关联模块

本模块实现桶与链之间的关联机制。
"""

from typing import List, Dict
from pydantic import BaseModel, Field
from ..buckets.topic_cluster import TopicCluster
from ..chains.base_chain import BaseExtractedChain, ChainType


class BucketChainLink(BaseModel):
    """
    桶-链关联
    
    Attributes:
        cluster_id: 话题簇ID
        chain_id: 链ID
        link_type: 关联类型
        strength: 关联强度（0-1）
        evidence: 关联证据列表
        metadata: 扩展元数据
    """
    
    cluster_id: str = Field(description="话题簇ID")
    chain_id: str = Field(description="链ID")
    link_type: str = Field(description="关联类型: content_match/time_window/semantic_similarity")
    strength: float = Field(ge=0.0, le=1.0, description="关联强度")
    evidence: List[str] = Field(default_factory=list, description="关联证据")
    metadata: Dict = Field(default_factory=dict, description="扩展元数据")


class BucketChainLinker(BaseModel):
    """
    桶-链关联器
    
    使用多种策略建立桶与链之间的关联。
    """
    
    # 策略权重
    CONTENT_MATCH_WEIGHT: float = 0.4
    SEMANTIC_SIMILARITY_WEIGHT: float = 0.4
    TIME_WINDOW_WEIGHT: float = 0.2
    
    # 阈值配置
    LINK_STRENGTH_THRESHOLD: float = 0.5
    MIN_EVIDENCE_COUNT: int = 1
    
    def link_buckets_and_chains(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]]
    ) -> List[BucketChainLink]:
        """
        关联桶和链
        
        Args:
            clusters: 话题簇列表
            chains: 链类型到链列表的映射
        
        Returns:
            关联列表
        """
        links = []
        
        for cluster in clusters:
            for chain_type, chain_list in chains.items():
                for chain in chain_list:
                    # 计算关联强度
                    strength, link_type, evidence = self._calculate_link_strength(
                        cluster, chain
                    )
                    
                    # 只保留强关联
                    if strength >= self.LINK_STRENGTH_THRESHOLD and len(evidence) >= self.MIN_EVIDENCE_COUNT:
                        link = BucketChainLink(
                            cluster_id=cluster.cluster_id,
                            chain_id=chain.chain_id,
                            link_type=link_type,
                            strength=strength,
                            evidence=evidence
                        )
                        links.append(link)
                        
                        # 更新簇的关联信息
                        cluster.related_chains.append(chain.chain_id)
        
        return links
    
    def _calculate_link_strength(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> tuple[float, str, List[str]]:
        """
        计算关联强度
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            (强度, 关联类型, 证据列表)
        """
        evidence = []
        strengths = []
        
        # 策略1：内容匹配
        content_strength, content_evidence = self._content_matching_score(
            cluster, chain
        )
        if content_strength > 0:
            strengths.append(content_strength)
            evidence.extend(content_evidence)
        
        # 策略2：语义相似度
        semantic_strength, semantic_evidence = self._semantic_similarity_score(
            cluster, chain
        )
        if semantic_strength > 0:
            strengths.append(semantic_strength)
            evidence.extend(semantic_evidence)
        
        # 策略3：时间窗口（如果链有时间信息）
        time_strength, time_evidence = self._time_window_score(
            cluster, chain
        )
        if time_strength > 0:
            strengths.append(time_strength)
            evidence.extend(time_evidence)
        
        # 综合评分
        if not strengths:
            return 0.0, "no_link", []
        
        overall_strength = sum(strengths) / len(strengths)
        
        # 确定主要关联类型
        link_type = self._determine_link_type(strengths, evidence)
        
        return overall_strength, link_type, evidence
    
    def _content_matching_score(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> tuple[float, List[str]]:
        """
        内容匹配评分
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            (分数, 证据列表)
        """
        evidence = []
        
        # 提取簇的所有内容
        cluster_text = ""
        for item in cluster.items:
            if hasattr(item, 'content'):
                cluster_text += item.content + " "
        
        chain_text = chain.content
        
        # 简单的词重叠计算
        cluster_words = set(cluster_text.lower().split())
        chain_words = set(chain_text.lower().split())
        
        if not chain_words:
            return 0.0, []
        
        # 计算重叠率
        overlap = cluster_words & chain_words
        if overlap:
            overlap_rate = len(overlap) / len(chain_words)
            evidence.append(f"内容重叠: {len(overlap)} 个词")
            return overlap_rate * self.CONTENT_MATCH_WEIGHT, evidence
        
        return 0.0, []
    
    def _semantic_similarity_score(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> tuple[float, List[str]]:
        """
        语义相似度评分（基于关键词）
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            (分数, 证据列表)
        """
        evidence = []
        
        # 提取链的关键词
        chain_keywords = self._extract_chain_keywords(chain)
        
        if not chain_keywords or not cluster.keywords:
            return 0.0, []
        
        # 计算关键词重叠
        overlap = cluster.keywords & chain_keywords
        
        if overlap:
            overlap_rate = len(overlap) / len(chain_keywords)
            evidence.append(f"关键词匹配: {', '.join(list(overlap)[:3])}")
            return overlap_rate * self.SEMANTIC_SIMILARITY_WEIGHT, evidence
        
        return 0.0, []
    
    def _time_window_score(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> tuple[float, List[str]]:
        """
        时间窗口评分
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            (分数, 证据列表)
        """
        evidence = []
        
        # 检查链是否有时间信息
        if not hasattr(chain, 'created_at'):
            return 0.0, []
        
        chain_time = chain.created_at
        cluster_time = cluster.last_updated
        
        # 计算时间差（秒）
        time_diff = abs((chain_time - cluster_time).total_seconds())
        
        # 时间窗口：5分钟内高相关性
        if time_diff < 300:  # 5分钟
            score = 1.0 - (time_diff / 300)
            evidence.append(f"时间差: {time_diff}秒")
            return score * self.TIME_WINDOW_WEIGHT, evidence
        
        return 0.0, []
    
    def _determine_link_type(
        self,
        strengths: List[float],
        evidence: List[str]
    ) -> str:
        """
        确定主要关联类型
        
        Args:
            strengths: 各策略的分数列表
            evidence: 证据列表
        
        Returns:
            关联类型
        """
        # 根据证据关键词判断
        for ev in evidence:
            if "内容重叠" in ev:
                return "content_match"
            elif "关键词匹配" in ev:
                return "semantic_similarity"
            elif "时间差" in ev:
                return "time_window"
        
        # 默认
        return "mixed"
    
    def _extract_chain_keywords(self, chain: BaseExtractedChain) -> set:
        """
        从链提取关键词
        
        Args:
            chain: 链
        
        Returns:
            关键词集合
        """
        words = chain.content.split()
        stop_words = {'的', '是', '在', '和', '了', '有', '我', '你', '他', 'the', 'is', 'and', 'or', 'of', 'to'}
        keywords = {word for word in words if len(word) > 1 and word not in stop_words}
        return keywords
