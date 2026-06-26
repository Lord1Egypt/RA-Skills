"""
双轨并行架构 - 链缓冲区模块

本模块实现链缓冲区，用于临时存储提取的链。
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from .base_chain import BaseExtractedChain, ChainType


class ChainBuffer(BaseModel):
    """
    链缓冲区（独立的链存储空间）
    
    为每种链类型提供独立的缓冲区，支持TTL和容量管理。
    
    Attributes:
        buffer_id: 缓冲区ID
        buffer_type: 链类型
        chains: 存储的链列表
        max_capacity: 最大容量
        ttl_minutes: 过期时间（分钟）
        avg_confidence: 平均置信度
        completeness_score: 完整性评分
        created_at: 创建时间
        last_accessed: 最后访问时间
    """
    
    buffer_id: str
    buffer_type: ChainType
    
    # 存储的链
    chains: List[BaseExtractedChain] = Field(
        default_factory=list,
        description="存储的链列表"
    )
    
    # 缓冲区配置
    max_capacity: int = Field(
        default=50,
        description="最大容量"
    )
    ttl_minutes: int = Field(
        default=30,
        description="过期时间（分钟）"
    )
    
    # 质量指标
    avg_confidence: float = Field(
        default=0.0,
        description="平均置信度"
    )
    completeness_score: float = Field(
        default=0.0,
        description="完整性评分"
    )
    
    # 元数据
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="创建时间"
    )
    last_accessed: datetime = Field(
        default_factory=datetime.now,
        description="最后访问时间"
    )
    
    def add_chain(self, chain: BaseExtractedChain) -> bool:
        """
        添加链到缓冲区
        
        Args:
            chain: 链对象
        
        Returns:
            是否添加成功
        """
        # 检查容量
        if len(self.chains) >= self.max_capacity:
            # 移除最旧的链（LRU）
            self.chains.pop(0)
        
        # 添加链
        self.chains.append(chain)
        self.last_accessed = datetime.now()
        
        # 更新统计
        self._update_statistics()
        
        return True
    
    def get_chains(self, limit: int | None = None) -> List[BaseExtractedChain]:
        """
        获取链
        
        Args:
            limit: 限制数量（可选）
        
        Returns:
            链列表
        """
        self.last_accessed = datetime.now()
        
        if limit is None:
            return self.chains
        
        return self.chains[-limit:]
    
    def get_latest_chain(self) -> BaseExtractedChain | None:
        """
        获取最新的链
        
        Returns:
            最新链或None
        """
        if self.chains:
            return self.chains[-1]
        return None
    
    def cleanup_expired(self) -> int:
        """
        清理过期的链
        
        Returns:
            清理的数量
        """
        now = datetime.now()
        before_count = len(self.chains)
        
        # 移除过期链
        self.chains = [
            chain for chain in self.chains
            if (now - chain.created_at).total_seconds() < self.ttl_minutes * 60
        ]
        
        after_count = len(self.chains)
        
        # 更新统计
        self._update_statistics()
        
        return before_count - after_count
    
    def clear(self) -> None:
        """清空缓冲区"""
        self.chains.clear()
        self.avg_confidence = 0.0
        self.completeness_score = 0.0
    
    def is_empty(self) -> bool:
        """检查缓冲区是否为空"""
        return len(self.chains) == 0
    
    def is_full(self) -> bool:
        """检查缓冲区是否已满"""
        return len(self.chains) >= self.max_capacity
    
    def get_usage_percentage(self) -> float:
        """
        获取使用率
        
        Returns:
            使用率（0-1）
        """
        return len(self.chains) / self.max_capacity
    
    def _update_statistics(self) -> None:
        """更新统计信息"""
        if not self.chains:
            self.avg_confidence = 0.0
            self.completeness_score = 0.0
            return
        
        # 平均置信度
        self.avg_confidence = sum(
            chain.extraction_confidence 
            for chain in self.chains
        ) / len(self.chains)
        
        # 完整性评分（简化计算）
        self.completeness_score = min(1.0, len(self.chains) / 10.0)
