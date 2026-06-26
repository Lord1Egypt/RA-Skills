"""
向量接口
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class VectorConfig:
    """向量配置"""
    provider: str
    model: str
    dimensions: int
    api_key: Optional[str] = None
    base_url: Optional[str] = None


class VectorInterface(ABC):
    """向量接口 - 纯接口定义"""
    
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        生成向量嵌入
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        pass
    
    @abstractmethod
    def embed_single(self, text: str) -> List[float]:
        """
        生成单个文本的向量嵌入
        
        Args:
            text: 文本
            
        Returns:
            向量
        """
        pass
    
    @abstractmethod
    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算向量相似度
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            相似度分数
        """
        pass
    
    @abstractmethod
    def batch_embed(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        批量生成向量嵌入
        
        Args:
            texts: 文本列表
            batch_size: 批次大小
            
        Returns:
            向量列表
        """
        pass
