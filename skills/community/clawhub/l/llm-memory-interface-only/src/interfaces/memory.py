"""
记忆管理接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None
    embedding: Optional[List[float]] = None


class MemoryInterface(ABC):
    """记忆管理接口 - 纯接口定义"""
    
    @abstractmethod
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            metadata: 元数据
            
        Returns:
            记忆ID
        """
        pass
    
    @abstractmethod
    def get(self, memory_id: str) -> Optional[MemoryEntry]:
        """
        获取记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            记忆条目，不存在则返回 None
        """
        pass
    
    @abstractmethod
    def update(self, memory_id: str, content: Optional[str] = None, 
               metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        更新记忆
        
        Args:
            memory_id: 记忆ID
            content: 新内容（可选）
            metadata: 新元数据（可选）
            
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """
        删除记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def list(self, limit: int = 100, offset: int = 0) -> List[MemoryEntry]:
        """
        列出记忆
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            记忆列表
        """
        pass
