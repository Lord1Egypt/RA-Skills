"""
搜索引擎接口定义
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class ISearchEngine(ABC):
    """
    搜索引擎接口

    实现类必须提供以下方法：
    - search(): 搜索记忆
    - add(): 添加记忆
    - delete(): 删除记忆
    """

    @abstractmethod
    def search(self, query: str, top_k: int = 10) -> Dict[str, Any]:
        """
        搜索记忆

        Args:
            query: 查询文本
            top_k: 返回数量

        Returns:
            Dict: 搜索结果
                - results: List[Dict] 记忆列表
                - total: int 总数
                - latency_ms: float 耗时
        """
        pass

    @abstractmethod
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        添加记忆

        Args:
            content: 记忆内容
            metadata: 元数据

        Returns:
            str: 记忆 ID
        """
        pass

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """
        删除记忆

        Args:
            memory_id: 记忆 ID

        Returns:
            bool: 是否成功
        """
        pass

    @abstractmethod
    def get(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        获取单条记忆

        Args:
            memory_id: 记忆 ID

        Returns:
            Optional[Dict]: 记忆内容，不存在返回 None
        """
        pass
