"""
双轨并行架构 - 语义桶模块

本模块定义话题簇和语义桶提取器。
"""

from typing import List, Set, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from ..type_defs import SemanticBucketType


class TopicCluster(BaseModel):
    """
    话题簇（语义桶的提炼结果）
    
    通过聚类算法将相似的记忆项聚合。
    
    Attributes:
        cluster_id: 簇ID
        topic_label: 话题标签
        dominant_bucket: 主导桶类型
        keywords: 关键词集合
        items: 包含的记忆项列表
        avg_relevance: 平均相关性
        coherence: 内聚性
        priority: 提炼优先级
        related_chains: 关联的链ID列表
        extraction_candidate: 是否满足提炼条件
        created_at: 创建时间
        last_updated: 最后更新时间
    """
    
    cluster_id: str = Field(description="簇ID")
    topic_label: str = Field(description="话题标签")
    dominant_bucket: SemanticBucketType = Field(description="主导桶类型")
    
    # 关键词
    keywords: Set[str] = Field(default_factory=set)
    
    # 包含的记忆项
    items: List[object] = Field(default_factory=list)
    
    # 质量指标
    avg_relevance: float = Field(default=0.0)
    coherence: float = Field(default=0.0)
    priority: float = Field(default=0.0)
    
    # 关联信息
    related_chains: List[str] = Field(default_factory=list)
    extraction_candidate: bool = False
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def add_item(self, item: object) -> None:
        """
        添加记忆项
        
        Args:
            item: 记忆项
        """
        self.items.append(item)
        self.last_updated = datetime.now()
        
        # 更新关键词
        item_keywords = self._extract_keywords(item)
        self.keywords.update(item_keywords)
        
        # 更新统计
        self._update_statistics()
    
    def _extract_keywords(self, item: object) -> Set[str]:
        """
        从记忆项提取关键词
        
        Args:
            item: 记忆项
        
        Returns:
            关键词集合
        """
        # 简化实现：从content提取关键词
        if hasattr(item, 'content'):
            content = item.content
            # 简单的关键词提取：分词并过滤停用词
            words = content.split()
            stop_words = {'的', '是', '在', '和', '了', '有', '我', '你', '他'}
            keywords = {word for word in words if len(word) > 1 and word not in stop_words}
            return keywords
        return set()
    
    def _update_statistics(self) -> None:
        """更新统计信息"""
        if not self.items:
            self.avg_relevance = 0.0
            self.coherence = 0.0
            return
        
        # 平均相关性
        relevance_scores = []
        for item in self.items:
            if hasattr(item, 'relevance_score'):
                relevance_scores.append(item.relevance_score)
        
        if relevance_scores:
            self.avg_relevance = sum(relevance_scores) / len(relevance_scores)
        
        # 内聚性（简化计算：基于关键词重叠）
        self.coherence = self._calculate_coherence()
    
    def _calculate_coherence(self) -> float:
        """
        计算内聚性
        
        Returns:
            内聚性分数（0-1）
        """
        if len(self.items) < 2:
            return 1.0
        
        # 计算所有项的关键词重叠度
        total_overlap = 0.0
        count = 0
        
        for i, item1 in enumerate(self.items):
            for j, item2 in enumerate(self.items):
                if i < j:
                    keywords1 = self._extract_keywords(item1)
                    keywords2 = self._extract_keywords(item2)
                    
                    if keywords1 and keywords2:
                        overlap = len(keywords1 & keywords2) / len(keywords1 | keywords2)
                        total_overlap += overlap
                        count += 1
        
        if count == 0:
            return 0.0
        
        return total_overlap / count
    
    def is_ready_for_extraction(self, threshold: float = 0.7) -> bool:
        """
        检查是否满足提炼条件
        
        Args:
            threshold: 就绪阈值
        
        Returns:
            是否满足
        """
        # 综合评估：容量、内聚性、优先级
        score = (
            min(1.0, len(self.items) / 5.0) * 0.4 +  # 容量（至少5项）
            self.coherence * 0.3 +                  # 内聚性
            self.priority * 0.3                     # 优先级
        )
        
        return score >= threshold
