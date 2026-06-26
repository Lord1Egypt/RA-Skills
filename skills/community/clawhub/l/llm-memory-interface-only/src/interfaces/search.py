"""
搜索接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SearchMode(Enum):
    """搜索模式"""
    FAST = "fast"           # 快速模式：仅 FTS
    BALANCED = "balanced"   # 平衡模式：向量 + FTS
    FULL = "full"           # 完整模式：向量 + FTS + LLM


@dataclass
class SearchResult:
    """搜索结果"""
    id: str
    content: str
    score: float
    source: str  # "vector" | "fts" | "hybrid"
    metadata: Dict[str, Any]


class SearchInterface(ABC):
    """搜索接口 - 纯接口定义"""
    
    @abstractmethod
    def search(self, query: str, mode: SearchMode = SearchMode.BALANCED,
               top_k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """
        搜索记忆
        
        Args:
            query: 查询文本
            mode: 搜索模式
            top_k: 返回数量
            filters: 过滤条件
            
        Returns:
            搜索结果列表
        """
        pass
    
    @abstractmethod
    def hybrid_search(self, query: str, top_k: int = 10,
                      vector_weight: float = 0.5) -> List[SearchResult]:
        """
        混合搜索（向量 + FTS）
        
        Args:
            query: 查询文本
            top_k: 返回数量
            vector_weight: 向量权重
            
        Returns:
            搜索结果列表
        """
        pass
    
    @abstractmethod
    def fts_search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """
        全文搜索
        
        Args:
            query: 查询文本
            top_k: 返回数量
            
        Returns:
            搜索结果列表
        """
        pass
