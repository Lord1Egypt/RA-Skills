# Agent Memory System
# Copyright (C) 2024 kiwifruit
#
# This file is part of Agent Memory System.
#
# Agent Memory System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agent Memory System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agent Memory System.  If not, see <https://www.gnu.org/licenses/>.


"""
三层缓存 - Multi-Layer Cache

实现三层缓存架构，用于检索性能优化。

缓存架构：
- L1 缓存（内存）：最近访问的记忆（1000条），最快访问
- L2 缓存（Redis）：热点记忆（10000条），较快访问
- L3 缓存（磁盘）：冷记忆索引，较慢访问

核心特性：
- LRU-K 淘汰算法（考虑访问频率和时间衰减）
- 自动缓存预热（预加载热点数据）
- 缓存命中率统计
- 读写分离优化

性能目标：
- L1 命中率：> 80%
- L1+L2 命中率：> 95%
- L1 延迟：< 1ms
- L2 延迟：< 5ms
- L3 延迟：< 20ms
"""

import time
import json
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field

# 延迟导入 BloomFilter，支持无 mmh3 环境运行
try:
    from bloom_filter import BloomFilter
    BLOOM_FILTER_AVAILABLE = True
except ImportError:
    BLOOM_FILTER_AVAILABLE = False
    BloomFilter = None  # type: ignore


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    timestamp: datetime
    access_count: int = 0
    last_access_time: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_score(self, decay_rate: float = 0.1) -> float:
        """
        计算缓存条目的LRU-K得分

        Score = (Access_Count × Frequency_Weight) + (Recency × Recency_Weight)
        """
        # 访问频率得分
        frequency_score = self.access_count

        # 新鲜度得分（时间衰减）
        time_since_access = (datetime.now() - self.last_access_time).total_seconds() / 3600  # 小时
        recency_score = max(0, 1 - decay_rate * time_since_access)

        # 综合得分
        final_score = frequency_score * 0.7 + recency_score * 0.3

        return final_score


class L1MemoryCache:
    """
    L1 内存缓存

    特性：
    - 使用 OrderedDict 实现 O(1) 访问和更新
    - LRU-K 淘汰算法
    - Bloom Filter 快速过滤
    """

    def __init__(
        self,
        max_size: int = 1000,
        decay_rate: float = 0.1,
        bloom_filter_size: int = 10000,
    ):
        self.max_size = max_size
        self.decay_rate = decay_rate

        # 使用 OrderedDict 存储（自动维护访问顺序）
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()

        # Bloom Filter 用于快速过滤
        self.bloom_filter = BloomFilter(
            expected_items=bloom_filter_size,
            false_positive_rate=0.01,
        )

        # 统计信息
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
        }

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        # 先用 Bloom Filter 快速检查
        if not self.bloom_filter.contains(key):
            self.stats["misses"] += 1
            return None

        if key not in self.cache:
            self.stats["misses"] += 1
            return None

        # 更新访问信息
        entry = self.cache[key]
        entry.access_count += 1
        entry.last_access_time = datetime.now()

        # 移到末尾（表示最近访问）
        self.cache.move_to_end(key)

        self.stats["hits"] += 1
        return entry.value

    def set(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """设置缓存值"""
        # 添加到 Bloom Filter
        self.bloom_filter.add(key)

        # 创建缓存条目
        entry = CacheEntry(
            key=key,
            value=value,
            timestamp=datetime.now(),
            metadata=metadata or {},
        )

        # 如果已存在，更新
        if key in self.cache:
            self.cache[key] = entry
            self.cache.move_to_end(key)
        else:
            # 检查是否需要淘汰
            if len(self.cache) >= self.max_size:
                self._evict()

            self.cache[key] = entry

    def _evict(self) -> None:
        """
        淘汰最低得分的条目（LRU-K 算法）
        """
        if not self.cache:
            return

        # 找到得分最低的条目
        min_key = None
        min_score = float('inf')

        for key, entry in self.cache.items():
            score = entry.calculate_score(self.decay_rate)
            if score < min_score:
                min_score = score
                min_key = key

        if min_key:
            del self.cache[min_key]
            self.stats["evictions"] += 1

    def delete(self, key: str) -> bool:
        """删除缓存条目"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self.bloom_filter = BloomFilter(
            expected_items=10000,
            false_positive_rate=0.01,
        )
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0

        return {
            **self.stats,
            "size": len(self.cache),
            "hit_rate": hit_rate,
            "usage_percent": len(self.cache) / self.max_size * 100,
        }


class L2RedisCache:
    """
    L2 Redis 缓存

    特性：
    - 分布式缓存支持
    - 更大的容量
    - 支持 TTL 自动过期
    """

    def __init__(
        self,
        redis_client: Any,  # Redis 客户端
        max_size: int = 10000,
        ttl_seconds: int = 3600,  # 1小时过期
    ):
        self.redis_client = redis_client
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

        # 缓存键前缀
        self.key_prefix = "memory_cache:l2:"

        # 统计信息
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
        }

    def _make_key(self, key: str) -> str:
        """生成 Redis 键"""
        return f"{self.key_prefix}{key}"

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            redis_key = self._make_key(key)
            data = self.redis_client.get(redis_key)

            if data is None:
                self.stats["misses"] += 1
                return None

            # 反序列化
            value = json.loads(data)
            self.stats["hits"] += 1
            return value
        except Exception as e:
            print(f"Redis get error: {e}")
            self.stats["misses"] += 1
            return None

    def set(self, key: str, value: Any) -> None:
        """设置缓存值"""
        try:
            redis_key = self._make_key(key)
            data = json.dumps(value, ensure_ascii=False)

            # 设置值和 TTL
            self.redis_client.setex(redis_key, self.ttl_seconds, data)

            # 检查是否超过最大容量（Redis 会自动淘汰，但这里主动检查）
            current_size = self.redis_client.dbsize()
            if current_size > self.max_size:
                self.stats["evictions"] += 1

        except Exception as e:
            print(f"Redis set error: {e}")

    def delete(self, key: str) -> bool:
        """删除缓存条目"""
        try:
            redis_key = self._make_key(key)
            result = self.redis_client.delete(redis_key)
            return result > 0
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

    def clear(self) -> None:
        """清空所有 L2 缓存"""
        try:
            pattern = f"{self.key_prefix}*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Redis clear error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0

        return {
            **self.stats,
            "current_size": self.redis_client.dbsize(),
            "hit_rate": hit_rate,
        }


class L3DiskCache:
    """
    L3 磁盘缓存

    特性：
    - 存储冷记忆索引
    - 持久化存储
    - 支持快速检索
    """

    def __init__(
        self,
        cache_dir: str = "./cache/l3",
        index_file: str = "index.json",
    ):
        import os

        self.cache_dir = cache_dir
        self.index_file = index_file
        self.index_path = os.path.join(cache_dir, index_file)

        # 确保目录存在
        os.makedirs(cache_dir, exist_ok=True)

        # 加载索引
        self.index = self._load_index()

        # 统计信息
        self.stats = {
            "hits": 0,
            "misses": 0,
        }

    def _load_index(self) -> Dict[str, Dict[str, Any]]:
        """加载索引"""
        import os

        if not os.path.exists(self.index_path):
            return {}

        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Load index error: {e}")
            return {}

    def _save_index(self) -> None:
        """保存索引"""
        try:
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Save index error: {e}")

    def _get_file_path(self, key: str) -> str:
        """生成文件路径"""
        import hashlib
        # 使用 MD5 哈希避免文件名过长
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return f"{self.cache_dir}/{hash_key}.json"

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        import os

        if key not in self.index:
            self.stats["misses"] += 1
            return None

        file_path = self._get_file_path(key)

        if not os.path.exists(file_path):
            # 索引存在但文件不存在，清理索引
            del self.index[key]
            self._save_index()
            self.stats["misses"] += 1
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.stats["hits"] += 1
                return data
        except Exception as e:
            print(f"Disk get error: {e}")
            self.stats["misses"] += 1
            return None

    def set(self, key: str, value: Any) -> None:
        """设置缓存值"""
        file_path = self._get_file_path(key)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(value, f, ensure_ascii=False, indent=2)

            # 更新索引
            self.index[key] = {
                "file_path": file_path,
                "timestamp": datetime.now().isoformat(),
                "size": len(json.dumps(value)),
            }
            self._save_index()

        except Exception as e:
            print(f"Disk set error: {e}")

    def delete(self, key: str) -> bool:
        """删除缓存条目"""
        import os

        if key not in self.index:
            return False

        file_path = self._get_file_path(key)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)

            del self.index[key]
            self._save_index()
            return True
        except Exception as e:
            print(f"Disk delete error: {e}")
            return False

    def clear(self) -> None:
        """清空所有缓存"""
        import os
        import shutil

        try:
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
                os.makedirs(self.cache_dir)

            self.index = {}
        except Exception as e:
            print(f"Disk clear error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0

        return {
            **self.stats,
            "total_files": len(self.index),
            "hit_rate": hit_rate,
        }


class MultiLayerCache:
    """
    三层缓存管理器

    缓存层次：
    - L1: 内存缓存（最快，容量最小）
    - L2: Redis 缓存（较快，容量中等）
    - L3: 磁盘缓存（最慢，容量最大）

    查询策略：
    1. 先查 L1，命中则返回
    2. 未命中则查 L2，命中则提升到 L1
    3. 未命中则查 L3，命中则提升到 L2 和 L1

    写入策略：
    1. 写入 L1
    2. 异步写入 L2 和 L3
    """

    def __init__(
        self,
        redis_client: Optional[Any] = None,
        l1_size: int = 1000,
        l2_size: int = 10000,
        l3_dir: str = "./cache/l3",
    ):
        # 初始化各层缓存
        self.l1_cache = L1MemoryCache(max_size=l1_size)
        self.l2_cache = L2RedisCache(redis_client, max_size=l2_size) if redis_client else None
        self.l3_cache = L3DiskCache(cache_dir=l3_dir)

        # 全局统计
        self.global_stats = {
            "l1_hits": 0,
            "l2_hits": 0,
            "l3_hits": 0,
            "total_misses": 0,
        }

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值（三层查找）

        返回：
            缓存值，如果所有层都未命中则返回 None
        """
        # L1 查找
        value = self.l1_cache.get(key)
        if value is not None:
            self.global_stats["l1_hits"] += 1
            return value

        # L2 查找
        if self.l2_cache:
            value = self.l2_cache.get(key)
            if value is not None:
                self.global_stats["l2_hits"] += 1
                # 提升到 L1
                self.l1_cache.set(key, value)
                return value

        # L3 查找
        value = self.l3_cache.get(key)
        if value is not None:
            self.global_stats["l3_hits"] += 1
            # 提升到 L2 和 L1
            if self.l2_cache:
                self.l2_cache.set(key, value)
            self.l1_cache.set(key, value)
            return value

        # 全部未命中
        self.global_stats["total_misses"] += 1
        return None

    def set(self, key: str, value: Any, write_all_layers: bool = True) -> None:
        """
        设置缓存值

        参数：
            key: 缓存键
            value: 缓存值
            write_all_layers: 是否写入所有层（默认 True）
        """
        # 写入 L1
        self.l1_cache.set(key, value)

        if write_all_layers:
            # 写入 L2（异步）
            if self.l2_cache:
                self.l2_cache.set(key, value)

            # 写入 L3（异步）
            self.l3_cache.set(key, value)

    def delete(self, key: str) -> None:
        """删除所有层的缓存"""
        self.l1_cache.delete(key)
        if self.l2_cache:
            self.l2_cache.delete(key)
        self.l3_cache.delete(key)

    def clear(self) -> None:
        """清空所有层的缓存"""
        self.l1_cache.clear()
        if self.l2_cache:
            self.l2_cache.clear()
        self.l3_cache.clear()
        self.global_stats = {
            "l1_hits": 0,
            "l2_hits": 0,
            "l3_hits": 0,
            "total_misses": 0,
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取综合统计信息"""
        total_requests = sum(self.global_stats.values())
        overall_hit_rate = (
            (self.global_stats["l1_hits"] + self.global_stats["l2_hits"] + self.global_stats["l3_hits"]) /
            total_requests
            if total_requests > 0 else 0
        )

        return {
            "global": {
                **self.global_stats,
                "overall_hit_rate": overall_hit_rate,
                "total_requests": total_requests,
            },
            "l1": self.l1_cache.get_stats(),
            "l2": self.l2_cache.get_stats() if self.l2_cache else None,
            "l3": self.l3_cache.get_stats(),
        }


# 使用示例
if __name__ == "__main__":
    print("=== 三层缓存示例 ===")

    # 创建缓存（不使用 Redis）
    cache = MultiLayerCache(
        redis_client=None,  # 可以传入真实的 Redis 客户端
        l1_size=100,
        l3_dir="./test_cache",
    )

    # 写入缓存
    print("\n写入测试数据...")
    for i in range(200):
        cache.set(f"key_{i}", {"value": f"data_{i}", "index": i})

    # 读取测试
    print("\n读取测试...")
    # 第一次读取（应该从 L1 读取）
    start = time.time()
    value1 = cache.get("key_50")
    l1_time = time.time() - start
    print(f"第一次读取 key_50: {value1}, 耗时: {l1_time*1000:.3f}ms")

    # 模拟 L1 缓存被清理
    cache.l1_cache.clear()

    # 第二次读取（应该从 L3 读取并提升到 L1）
    start = time.time()
    value2 = cache.get("key_50")
    l3_time = time.time() - start
    print(f"第二次读取 key_50: {value2}, 耗时: {l3_time*1000:.3f}ms")

    # 批量测试
    print("\n批量读取测试...")
    for i in range(100):
        cache.get(f"key_{i}")

    # 显示统计信息
    stats = cache.get_stats()
    print("\n=== 统计信息 ===")
    print(f"L1 命中: {stats['global']['l1_hits']}")
    print(f"L2 命中: {stats['global']['l2_hits']}")
    print(f"L3 命中: {stats['global']['l3_hits']}")
    print(f"未命中: {stats['global']['total_misses']}")
    print(f"总体命中率: {stats['global']['overall_hit_rate']:.2%}")
    print(f"\nL1 统计: {stats['l1']}")
    print(f"L3 统计: {stats['l3']}")

    # 清理测试缓存
    import shutil
    if os.path.exists("./test_cache"):
        shutil.rmtree("./test_cache")
