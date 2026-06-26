"""
记忆存储接口定义
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class IMemoryStore(ABC):
    """
    记忆存储接口

    实现类必须提供以下方法：
    - store(): 存储记忆
    - retrieve(): 检索记忆
    - list(): 列出记忆
    """

    @abstractmethod
    def store(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        存储记忆

        Args:
            content: 记忆内容
            metadata: 元数据

        Returns:
            str: 记忆 ID
        """
        pass

    @abstractmethod
    def retrieve(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        检索记忆

        Args:
            memory_id: 记忆 ID

        Returns:
            Optional[Dict]: 记忆内容
        """
        pass

    @abstractmethod
    def list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        列出记忆

        Args:
            limit: 数量限制
            offset: 偏移量

        Returns:
            List[Dict]: 记忆列表
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        统计记忆数量

        Returns:
            int: 记忆总数
        """
        pass
