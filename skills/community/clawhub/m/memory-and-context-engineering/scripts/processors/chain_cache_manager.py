"""
双轨并行架构 - 链缓存管理器模块

本模块实现链信息的缓存和索引系统。
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import OrderedDict
from ..chains.base_chain import BaseExtractedChain, ChainType


class ChainCacheEntry:
    """
    链缓存条目

    Attributes:
        chain_id: 链ID
        chain: 链对象
        chain_type: 链类型
        access_count: 访问次数
        last_accessed: 最后访问时间
        created_at: 创建时间
        ttl: 过期时间（秒）
    """

    def __init__(
        self,
        chain_id: str,
        chain: BaseExtractedChain,
        chain_type: ChainType,
        ttl: int = 300
    ):
        self.chain_id = chain_id
        self.chain = chain
        self.chain_type = chain_type
        self.access_count = 0
        self.last_accessed = datetime.now()
        self.created_at = datetime.now()
        self.ttl = ttl

    def is_expired(self) -> bool:
        """
        检查是否过期

        Returns:
            是否过期
        """
        if self.ttl <= 0:
            return False

        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed > self.ttl

    def access(self) -> None:
        """记录访问"""
        self.access_count += 1
        self.last_accessed = datetime.now()


class ChainCacheManager:
    """
    链缓存管理器

    使用LRU策略管理链缓存。
    """

    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl

        # LRU缓存（使用OrderedDict）
        self.cache: OrderedDict[str, ChainCacheEntry] = OrderedDict()

        # 按链类型分组的索引
        self.type_index: Dict[ChainType, List[str]] = {}

        # 统计信息
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }

    def put(
        self,
        chain_id: str,
        chain: BaseExtractedChain,
        chain_type: ChainType,
        ttl: Optional[int] = None
    ) -> bool:
        """
        将链放入缓存

        Args:
            chain_id: 链ID
            chain: 链对象
            chain_type: 链类型
            ttl: 过期时间（秒），None表示使用默认值

        Returns:
            是否成功放入
        """
        # 如果缓存已满，执行LRU淘汰
        if len(self.cache) >= self.max_size and chain_id not in self.cache:
            self._evict_lru()

        # 创建缓存条目
        entry_ttl = ttl if ttl is not None else self.default_ttl
        entry = ChainCacheEntry(
            chain_id=chain_id,
            chain=chain,
            chain_type=chain_type,
            ttl=entry_ttl
        )

        self.cache[chain_id] = entry

        # 更新类型索引
        if chain_type not in self.type_index:
            self.type_index[chain_type] = []
        if chain_id not in self.type_index[chain_type]:
            self.type_index[chain_type].append(chain_id)

        return True

    def get(self, chain_id: str) -> Optional[BaseExtractedChain]:
        """
        从缓存获取链

        Args:
            chain_id: 链ID

        Returns:
            链对象，如果不存在或已过期返回None
        """
        self.stats['total_requests'] += 1

        if chain_id not in self.cache:
            self.stats['misses'] += 1
            return None

        entry = self.cache[chain_id]

        # 检查是否过期
        if entry.is_expired():
            # 移除过期条目
            self._remove_entry(chain_id)
            self.stats['misses'] += 1
            return None

        # 记录访问并更新LRU
        entry.access()
        self.cache.move_to_end(chain_id)

        self.stats['hits'] += 1
        return entry.chain

    def get_by_type(self, chain_type: ChainType) -> List[BaseExtractedChain]:
        """
        按类型获取所有链

        Args:
            chain_type: 链类型

        Returns:
            链列表
        """
        if chain_type not in self.type_index:
            return []

        chains = []
        chain_ids_to_remove = []

        for chain_id in self.type_index[chain_type]:
            chain = self.get(chain_id)
            if chain is not None:
                chains.append(chain)
            else:
                chain_ids_to_remove.append(chain_id)

        # 清理失效的ID
        for chain_id in chain_ids_to_remove:
            self.type_index[chain_type].remove(chain_id)

        return chains

    def _evict_lru(self) -> None:
        """淘汰最近最少使用的条目"""
        if not self.cache:
            return

        # 获取最旧的条目
        oldest_id = next(iter(self.cache))
        self._remove_entry(oldest_id)
        self.stats['evictions'] += 1

    def _remove_entry(self, chain_id: str) -> None:
        """移除缓存条目"""
        if chain_id not in self.cache:
            return

        entry = self.cache[chain_id]
        chain_type = entry.chain_type

        # 从缓存中移除
        del self.cache[chain_id]

        # 从类型索引中移除
        if chain_type in self.type_index:
            if chain_id in self.type_index[chain_type]:
                self.type_index[chain_type].remove(chain_id)

    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self.type_index.clear()

    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        hit_rate = 0.0
        if self.stats['total_requests'] > 0:
            hit_rate = self.stats['hits'] / self.stats['total_requests']

        return {
            **self.stats,
            'hit_rate': hit_rate,
            'size': len(self.cache),
            'max_size': self.max_size
        }
