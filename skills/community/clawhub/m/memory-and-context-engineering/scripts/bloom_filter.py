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
布隆过滤器 - Bloom Filter

用于快速判断元素是否可能存在于集合中，用于检索优化中的快速过滤。

关键特性：
- 空间效率高：相比哈希表节省 90% 以上空间
- 误判率可控：可配置误判率（默认 1%）
- 无假阴性：如果判断不在，则一定不在

典型使用场景：
1. 快速过滤不存在的关键词，避免磁盘IO
2. 缓存预热前的存在性检查
3. 减少对Redis的无效查询

核心算法：
- 使用多个哈希函数将元素映射到位数组的多个位置
- 查询时检查所有位置是否都为1
- 误判率公式：ε = (1 - e^(-kn/m))^k
  其中：k=哈希函数数，m=位数组大小，n=元素数量
"""

import math
from typing import Any, Set, List

# 延迟导入 mmh3，支持无 mmh3 环境运行
try:
    import mmh3
    MMH3_AVAILABLE = True
except ImportError:
    MMH3_AVAILABLE = False
    mmh3 = None  # type: ignore


class BloomFilter:
    """
    布隆过滤器实现

    参数：
        expected_items: 预期元素数量
        false_positive_rate: 可接受的误判率（默认 0.01，即 1%）
        hash_count: 哈希函数数量（可选，自动计算）
    """

    def __init__(
        self,
        expected_items: int,
        false_positive_rate: float = 0.01,
        hash_count: int = None
    ):
        if not MMH3_AVAILABLE:
            raise ImportError(
                "mmh3 is required for BloomFilter. "
                "Install it with: pip install mmh3>=3.0.0"
            )
        
        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate

        # 计算最优参数
        self._calculate_optimal_parameters(hash_count)

        # 初始化位数组（使用字节数组节省空间）
        self.bit_array = bytearray(self.bit_size // 8 + 1)
        self.item_count = 0

    def _calculate_optimal_parameters(self, hash_count: int = None):
        """
        计算最优的位数组大小和哈希函数数量

        数学推导：
        最优位数组大小：m = n × log₂(1/ε) × ln2
        最优哈希函数数量：k = (m/n) × ln2 = ln2 × log₂(1/ε)
        """
        # 计算最优位数组大小
        self.bit_size = int(
            -self.expected_items * math.log(self.false_positive_rate) / (math.log(2) ** 2)
        )

        # 计算最优哈希函数数量
        if hash_count is None:
            self.hash_count = int(
                (self.bit_size / self.expected_items) * math.log(2)
            )
        else:
            self.hash_count = hash_count

        # 确保至少有1个哈希函数
        self.hash_count = max(1, self.hash_count)

        # 计算实际误判率
        self.actual_false_positive_rate = (
            (1 - math.exp(-self.hash_count * self.expected_items / self.bit_size))
            ** self.hash_count
        )

    def _get_hash_positions(self, item: str) -> List[int]:
        """
        使用多个哈希函数获取位数组位置

        使用双哈希技术生成多个哈希值：
        hash_i(x) = hash1(x) + i × hash2(x)
        这样只需要计算两次哈希，可以生成任意数量的哈希值
        """
        # 使用mmh3的两种哈希函数
        hash1 = mmh3.hash(item, seed=0)
        hash2 = mmh3.hash(item, seed=1)

        positions = []
        for i in range(self.hash_count):
            # 双哈希技术生成多个位置
            combined_hash = hash1 + i * hash2
            position = abs(combined_hash) % self.bit_size
            positions.append(position)

        return positions

    def add(self, item: Any) -> None:
        """
        添加元素到布隆过滤器

        参数：
            item: 要添加的元素（会转换为字符串）
        """
        item_str = str(item)
        positions = self._get_hash_positions(item_str)

        # 设置所有哈希位置为1
        for position in positions:
            byte_index = position // 8
            bit_offset = position % 8
            self.bit_array[byte_index] |= (1 << bit_offset)

        self.item_count += 1

    def contains(self, item: Any) -> bool:
        """
        检查元素是否可能存在于布隆过滤器中

        返回：
            True: 元素可能存在（可能有误判）
            False: 元素一定不存在（无假阴性）

        参数：
            item: 要检查的元素（会转换为字符串）
        """
        item_str = str(item)
        positions = self._get_hash_positions(item_str)

        # 检查所有哈希位置是否都为1
        for position in positions:
            byte_index = position // 8
            bit_offset = position % 8
            if not (self.bit_array[byte_index] & (1 << bit_offset)):
                return False

        return True

    def add_batch(self, items: List[Any]) -> None:
        """
        批量添加元素

        参数：
            items: 要添加的元素列表
        """
        for item in items:
            self.add(item)

    def contains_batch(self, items: List[Any]) -> List[bool]:
        """
        批量检查元素是否存在

        参数：
            items: 要检查的元素列表

        返回：
            每个元素的存在性结果列表
        """
        return [self.contains(item) for item in items]

    def get_info(self) -> dict:
        """
        获取布隆过滤器的统计信息

        返回：
            包含统计信息的字典
        """
        return {
            "expected_items": self.expected_items,
            "actual_items": self.item_count,
            "bit_size": self.bit_size,
            "hash_count": self.hash_count,
            "target_false_positive_rate": self.false_positive_rate,
            "actual_false_positive_rate": self.actual_false_positive_rate,
            "memory_usage_bytes": len(self.bit_array),
            "memory_usage_kb": len(self.bit_array) / 1024,
        }


class ScalableBloomFilter:
    """
    可扩展布隆过滤器

    当元素数量超过预期时，自动创建新的布隆过滤器
    使用链式结构支持动态扩展

    特性：
    - 动态扩展：元素数量超过预期时自动扩容
    - 渐进式误判率：新过滤器误判率更低
    - 查询优化：从最新过滤器开始查询
    """

    def __init__(
        self,
        initial_size: int = 100000,
        false_positive_rate: float = 0.01,
        growth_rate: float = 2.0,
    ):
        """
        初始化可扩展布隆过滤器

        参数：
            initial_size: 初始容量
            false_positive_rate: 目标误判率
            growth_rate: 扩容倍数（默认2倍）
        """
        self.initial_size = initial_size
        self.false_positive_rate = false_positive_rate
        self.growth_rate = growth_rate

        # 布隆过滤器链表（新过滤器在前）
        self.filters: List[BloomFilter] = []
        self._add_new_filter()

    def _add_new_filter(self):
        """添加新的布隆过滤器"""
        if not self.filters:
            size = self.initial_size
        else:
            size = int(self.filters[0].expected_items * self.growth_rate)

        bf = BloomFilter(size, self.false_positive_rate)
        self.filters.insert(0, bf)

    def add(self, item: Any) -> None:
        """添加元素（只添加到最新的过滤器）"""
        # 检查是否需要扩容
        if self.filters[0].item_count >= self.filters[0].expected_items * 0.8:
            self._add_new_filter()

        self.filters[0].add(item)

    def contains(self, item: Any) -> bool:
        """检查元素是否存在（从最新过滤器开始查询）"""
        for bf in self.filters:
            if bf.contains(item):
                return True
        return False

    def get_info(self) -> dict:
        """获取统计信息"""
        total_items = sum(bf.item_count for bf in self.filters)
        total_memory = sum(bf.get_info()["memory_usage_bytes"] for bf in self.filters)

        return {
            "total_items": total_items,
            "total_filters": len(self.filters),
            "total_memory_bytes": total_memory,
            "total_memory_kb": total_memory / 1024,
            "filters_info": [bf.get_info() for bf in self.filters],
        }


def estimate_memory_usage(
    expected_items: int,
    false_positive_rate: float = 0.01
) -> dict:
    """
    估算布隆过滤器的内存使用

    参数：
        expected_items: 预期元素数量
        false_positive_rate: 目标误判率

    返回：
        内存使用估算结果
    """
    bf = BloomFilter(expected_items, false_positive_rate)
    info = bf.get_info()

    return {
        "expected_items": expected_items,
        "false_positive_rate": false_positive_rate,
        "bit_size": info["bit_size"],
        "hash_count": info["hash_count"],
        "memory_usage_bytes": info["memory_usage_bytes"],
        "memory_usage_kb": info["memory_usage_kb"],
        "bits_per_item": info["bit_size"] / expected_items,
    }


# 使用示例
if __name__ == "__main__":
    # 示例1：基本使用
    print("=== 示例1：基本布隆过滤器 ===")
    bf = BloomFilter(expected_items=10000, false_positive_rate=0.01)

    # 添加一些元素
    test_items = ["apple", "banana", "orange", "grape", "mango"]
    for item in test_items:
        bf.add(item)

    # 测试查询
    print(f"包含 'apple': {bf.contains('apple')}")
    print(f"包含 'banana': {bf.contains('banana')}")
    print(f"包含 'pear' (不存在): {bf.contains('pear')}")

    # 显示统计信息
    info = bf.get_info()
    print(f"\n统计信息:")
    print(f"  预期元素数: {info['expected_items']}")
    print(f"  实际元素数: {info['actual_items']}")
    print(f"  位数组大小: {info['bit_size']} bits")
    print(f"  哈希函数数: {info['hash_count']}")
    print(f"  目标误判率: {info['target_false_positive_rate']}")
    print(f"  实际误判率: {info['actual_false_positive_rate']:.6f}")
    print(f"  内存使用: {info['memory_usage_kb']:.2f} KB")

    # 示例2：可扩展布隆过滤器
    print("\n=== 示例2：可扩展布隆过滤器 ===")
    sbf = ScalableBloomFilter(initial_size=1000, false_positive_rate=0.01)

    # 添加大量元素
    for i in range(3000):
        sbf.add(f"item_{i}")

    info = sbf.get_info()
    print(f"总元素数: {info['total_items']}")
    print(f"过滤器数量: {info['total_filters']}")
    print(f"总内存使用: {info['total_memory_kb']:.2f} KB")

    # 示例3：内存估算
    print("\n=== 示例3：内存使用估算 ===")
    for items in [1000, 10000, 100000, 1000000]:
        usage = estimate_memory_usage(items, 0.01)
        print(f"\n预期 {items:,} 个元素:")
        print(f"  位数组大小: {usage['bit_size']:,} bits")
        print(f"  每元素占用: {usage['bits_per_item']:.2f} bits")
        print(f"  内存使用: {usage['memory_usage_kb']:.2f} KB")
