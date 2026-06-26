"""
向量后端接口定义
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class IVectorBackend(ABC):
    """
    向量后端接口

    实现类必须提供以下方法：
    - search(): 向量搜索
    - add(): 添加向量
    - delete(): 删除向量
    """

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
        """
        向量搜索

        Args:
            query_vector: 查询向量
            top_k: 返回数量

        Returns:
            List[Dict]: 搜索结果
                - id: str 记忆 ID
                - score: float 相似度分数
                - content: str 记忆内容
        """
        pass

    @abstractmethod
    def add(self, memory_id: str, vector: List[float]) -> bool:
        """
        添加向量

        Args:
            memory_id: 记忆 ID
            vector: 向量数据

        Returns:
            bool: 是否成功
        """
        pass

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """
        删除向量

        Args:
            memory_id: 记忆 ID

        Returns:
            bool: 是否成功
        """
        pass

    @abstractmethod
    def get_backend_name(self) -> str:
        """
        获取后端名称

        Returns:
            str: 后端名称（如 "fts", "native", "gpu"）
        """
        pass
