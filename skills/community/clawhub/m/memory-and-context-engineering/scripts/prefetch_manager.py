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
预取管理器 - Prefetch Manager

实现智能预取机制，基于用户行为模式和上下文预测需要的记忆。

预取策略：
1. 最近访问的相关记忆（相似度 > 0.7）
2. 相同任务类型的记忆（task_type 匹配）
3. 时间模式记忆（工作日9点访问过）

核心特性：
- 基于滑动窗口的访问模式学习
- 简单启发式规则（避免过度复杂）
- 预取准确率追踪
- 缓存预热支持

性能目标：
- 预取准确率：> 70%
- 预取时间：< 10ms
- 缓存命中率提升：15-20%
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, field

import hashlib


@dataclass
class PrefetchPrediction:
    """预取预测"""
    predicted_keys: List[str]  # 预测会访问的键
    confidence: float  # 预测置信度
    strategy: str  # 使用的策略
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccessPattern:
    """访问模式"""
    key: str
    access_times: deque  # 访问时间列表
    access_count: int  # 访问次数
    last_access: datetime
    task_type: Optional[str] = None
    context: Optional[str] = None


class PrefetchManager:
    """
    预取管理器

    基于访问模式和上下文预测用户需要的记忆
    """

    def __init__(
        self,
        window_size: int = 100,  # 访问窗口大小
        similarity_threshold: float = 0.7,  # 相似度阈值
        prefetch_limit: int = 10,  # 每次预取的最大数量
        enable_time_pattern: bool = True,  # 是否启用时间模式
    ):
        """
        初始化预取管理器

        参数：
            window_size: 访问模式窗口大小
            similarity_threshold: 相似度阈值
            prefetch_limit: 每次预取的最大数量
            enable_time_pattern: 是否启用时间模式
        """
        self.window_size = window_size
        self.similarity_threshold = similarity_threshold
        self.prefetch_limit = prefetch_limit
        self.enable_time_pattern = enable_time_pattern

        # 访问历史（键 -> 访问模式）
        self.access_patterns: Dict[str, AccessPattern] = {}

        # 访问序列（用于预测下一个访问）
        self.access_sequence: deque = deque(maxlen=window_size)

        # 统计信息
        self.stats = {
            "total_prefetches": 0,
            "prefetch_hits": 0,
            "prefetch_misses": 0,
            "strategies": defaultdict(int),
        }

    def record_access(
        self,
        key: str,
        task_type: Optional[str] = None,
        context: Optional[str] = None,
    ) -> None:
        """
        记录访问

        参数：
            key: 访问的键
            task_type: 任务类型
            context: 上下文
        """
        now = datetime.now()

        # 更新访问模式
        if key not in self.access_patterns:
            self.access_patterns[key] = AccessPattern(
                key=key,
                access_times=deque(maxlen=self.window_size),
                access_count=0,
                last_access=now,
                task_type=task_type,
                context=context,
            )

        pattern = self.access_patterns[key]
        pattern.access_times.append(now)
        pattern.access_count += 1
        pattern.last_access = now

        if task_type:
            pattern.task_type = task_type
        if context:
            pattern.context = context

        # 更新访问序列
        self.access_sequence.append(key)

    def _calculate_similarity(
        self,
        key1: str,
        key2: str,
    ) -> float:
        """
        计算两个键的相似度

        使用简单的 Jaccard 相似度（基于共同子串）
        """
        # 将键转换为字符集合
        set1 = set(key1.lower())
        set2 = set(key2.lower())

        # 计算交集和并集
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return intersection / union

    def _predict_by_sequence(self) -> List[str]:
        """
        基于访问序列预测（序列模式）

        策略：如果经常在访问 A 后访问 B，那么访问 A 后预取 B
        """
        if len(self.access_sequence) < 2:
            return []

        # 获取当前访问的键
        current_key = self.access_sequence[-1]

        # 查找历史中经常在 current_key 之后访问的键
        followers: Dict[str, int] = defaultdict(int)

        for i in range(len(self.access_sequence) - 1):
            if self.access_sequence[i] == current_key:
                next_key = self.access_sequence[i + 1]
                followers[next_key] += 1

        # 排序并返回最常跟随的键
        sorted_followers = sorted(
            followers.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        predicted_keys = [k for k, v in sorted_followers[:self.prefetch_limit]]

        return predicted_keys

    def _predict_by_similarity(self, current_key: str) -> List[str]:
        """
        基于相似度预测（关联模式）

        策略：预取与当前键相似的其他键
        """
        similarities = []

        for key, pattern in self.access_patterns.items():
            if key == current_key:
                continue

            similarity = self._calculate_similarity(current_key, key)
            if similarity >= self.similarity_threshold:
                similarities.append((key, similarity, pattern.access_count))

        # 按相似度和访问次数排序
        similarities.sort(key=lambda x: (x[1], x[2]), reverse=True)

        predicted_keys = [k for k, _, _ in similarities[:self.prefetch_limit]]

        return predicted_keys

    def _predict_by_task_type(self, task_type: str) -> List[str]:
        """
        基于任务类型预测

        策略：预取相同任务类型的记忆
        """
        if not task_type:
            return []

        candidates = []

        for key, pattern in self.access_patterns.items():
            if pattern.task_type == task_type:
                candidates.append((key, pattern.access_count))

        # 按访问次数排序
        candidates.sort(key=lambda x: x[1], reverse=True)

        predicted_keys = [k for k, _ in candidates[:self.prefetch_limit]]

        return predicted_keys

    def _predict_by_time_pattern(self, current_time: datetime) -> List[str]:
        """
        基于时间模式预测

        策略：如果某个时间点经常访问某些键，则在相似时间预取
        """
        if not self.enable_time_pattern:
            return []

        # 计算当前时间特征
        hour = current_time.hour
        weekday = current_time.weekday()

        # 统计相同时间特征的访问
        time_candidates: Dict[str, int] = defaultdict(int)

        for key, pattern in self.access_patterns.items():
            for access_time in pattern.access_times:
                if access_time.hour == hour and access_time.weekday() == weekday:
                    time_candidates[key] += 1

        # 排序
        sorted_candidates = sorted(
            time_candidates.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        predicted_keys = [k for k, _ in sorted_candidates[:self.prefetch_limit // 2]]

        return predicted_keys

    def predict(
        self,
        current_key: Optional[str] = None,
        task_type: Optional[str] = None,
        current_time: Optional[datetime] = None,
    ) -> PrefetchPrediction:
        """
        预测下一步可能访问的键

        参数：
            current_key: 当前访问的键
            task_type: 任务类型
            current_time: 当前时间

        返回：
            预测结果
        """
        if not self.access_sequence:
            return PrefetchPrediction(
                predicted_keys=[],
                confidence=0.0,
                strategy="no_data",
            )

        current_time = current_time or datetime.now()

        # 收集所有预测
        all_predictions: List[Tuple[str, int, str]] = []  # (key, score, strategy)

        # 1. 序列模式预测
        sequence_predictions = self._predict_by_sequence()
        for key in sequence_predictions:
            all_predictions.append((key, 3, "sequence"))

        # 2. 相似度预测
        if current_key:
            similarity_predictions = self._predict_by_similarity(current_key)
            for key in similarity_predictions:
                all_predictions.append((key, 2, "similarity"))

        # 3. 任务类型预测
        if task_type:
            task_predictions = self._predict_by_task_type(task_type)
            for key in task_predictions:
                all_predictions.append((key, 2, "task_type"))

        # 4. 时间模式预测
        time_predictions = self._predict_by_time_pattern(current_time)
        for key in time_predictions:
            all_predictions.append((key, 1, "time_pattern"))

        # 聚合预测（去重并排序）
        key_scores: Dict[str, Tuple[int, str]] = {}
        for key, score, strategy in all_predictions:
            if key not in key_scores:
                key_scores[key] = (score, strategy)
            else:
                # 取最高分数
                if score > key_scores[key][0]:
                    key_scores[key] = (score, strategy)

        # 排序
        sorted_keys = sorted(
            key_scores.items(),
            key=lambda x: x[1][0],
            reverse=True,
        )

        # 限制数量
        predicted_keys = [k for k, _ in sorted_keys[:self.prefetch_limit]]

        # 计算置信度（基于预测数量和分数）
        if not predicted_keys:
            confidence = 0.0
            strategy = "no_prediction"
        else:
            confidence = min(1.0, sum(score for _, (score, _) in sorted_keys) / (self.prefetch_limit * 3))
            strategy = "mixed"

        self.stats["total_prefetches"] += 1
        self.stats["strategies"][strategy] += 1

        return PrefetchPrediction(
            predicted_keys=predicted_keys,
            confidence=confidence,
            strategy=strategy,
            metadata={
                "key_scores": {k: v for k, v in key_scores.items()},
            },
        )

    def prefetch(
        self,
        cache_get_func,  # 从缓存获取数据的函数
        cache_set_func,  # 向缓存设置数据的函数
        current_key: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> List[str]:
        """
        执行预取

        参数：
            cache_get_func: 缓存获取函数
            cache_set_func: 缓存设置函数
            current_key: 当前访问的键
            task_type: 任务类型

        返回：
            成功预取的键列表
        """
        # 预测
        prediction = self.predict(current_key, task_type)

        if not prediction.predicted_keys:
            return []

        # 预取（仅预取不在缓存中的）
        prefetched_keys = []

        for key in prediction.predicted_keys:
            # 检查是否已在缓存中
            if cache_get_func(key) is None:
                # 尝试从存储加载
                try:
                    data = self._load_from_storage(key)
                    if data is not None:
                        cache_set_func(key, data)
                        prefetched_keys.append(key)
                        self.stats["prefetch_hits"] += 1
                    else:
                        self.stats["prefetch_misses"] += 1
                except Exception as e:
                    print(f"Prefetch error for key {key}: {e}")
                    self.stats["prefetch_misses"] += 1

        return prefetched_keys

    def _load_from_storage(self, key: str) -> Optional[Any]:
        """
        从存储加载数据（子类实现）

        这是一个占位方法，实际应用中需要根据存储方式实现
        """
        # 实际应用中，这里会从 Redis、磁盘或其他存储加载数据
        return None

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_attempts = self.stats["prefetch_hits"] + self.stats["prefetch_misses"]
        hit_rate = self.stats["prefetch_hits"] / total_attempts if total_attempts > 0 else 0

        return {
            **self.stats,
            "hit_rate": hit_rate,
            "total_access_patterns": len(self.access_patterns),
            "access_sequence_length": len(self.access_sequence),
        }

    def clear(self) -> None:
        """清空访问历史"""
        self.access_patterns.clear()
        self.access_sequence.clear()
        self.stats = {
            "total_prefetches": 0,
            "prefetch_hits": 0,
            "prefetch_misses": 0,
            "strategies": defaultdict(int),
        }


class CacheWarmer:
    """
    缓存预热器

    在系统启动或低峰期预热缓存
    """

    def __init__(
        self,
        prefetch_manager: PrefetchManager,
        warmup_keys: List[str],
        warmup_percentage: float = 0.2,  # 预热 20% 的数据
    ):
        """
        初始化预热器

        参数：
            prefetch_manager: 预取管理器
            warmup_keys: 需要预热的键列表
            warmup_percentage: 预热百分比
        """
        self.prefetch_manager = prefetch_manager
        self.warmup_keys = warmup_keys
        self.warmup_percentage = warmup_percentage

    def warmup(
        self,
        cache_set_func,
        load_func,
    ) -> int:
        """
        执行缓存预热

        参数：
            cache_set_func: 缓存设置函数
            load_func: 数据加载函数

        返回：
            预热的键数量
        """
        # 计算需要预热的数量
        warmup_count = int(len(self.warmup_keys) * self.warmup_percentage)

        # 选择键（优先选择访问频率高的）
        # 这里简单选择前 N 个键
        selected_keys = self.warmup_keys[:warmup_count]

        # 预热
        warmed_count = 0
        for key in selected_keys:
            try:
                data = load_func(key)
                if data is not None:
                    cache_set_func(key, data)
                    warmed_count += 1
            except Exception as e:
                print(f"Warmup error for key {key}: {e}")

        return warmed_count


# 使用示例
if __name__ == "__main__":
    print("=== 预取管理器示例 ===")

    # 创建预取管理器
    prefetch_manager = PrefetchManager(
        window_size=100,
        similarity_threshold=0.7,
        prefetch_limit=5,
    )

    # 模拟访问历史
    print("\n模拟访问历史...")
    access_history = [
        ("user_profile_1", "user_management", "查看用户信息"),
        ("user_orders_1", "order_management", "查看订单"),
        ("user_profile_2", "user_management", "查看用户信息"),
        ("user_orders_1", "order_management", "查看订单"),
        ("user_profile_1", "user_management", "查看用户信息"),
        ("user_orders_2", "order_management", "查看订单"),
        ("user_profile_3", "user_management", "查看用户信息"),
        ("user_orders_1", "order_management", "查看订单"),
    ]

    for key, task_type, context in access_history:
        prefetch_manager.record_access(key, task_type, context)

    # 预测下一步访问
    print("\n预测下一步访问...")
    prediction = prefetch_manager.predict(
        current_key="user_orders_1",
        task_type="order_management",
    )

    print(f"预测的键: {prediction.predicted_keys}")
    print(f"置信度: {prediction.confidence:.3f}")
    print(f"策略: {prediction.strategy}")

    # 获取统计信息
    stats = prefetch_manager.get_stats()
    print(f"\n统计信息:")
    print(f"  总预取次数: {stats['total_prefetches']}")
    print(f"  访问模式数: {stats['total_access_patterns']}")
    print(f"  访问序列长度: {stats['access_sequence_length']}")

    # 测试时间模式预测
    print("\n测试时间模式预测...")
    prefetch_manager_with_time = PrefetchManager(
        window_size=100,
        enable_time_pattern=True,
    )

    # 模拟在不同时间的访问
    now = datetime.now()
    morning = now.replace(hour=9, minute=0)
    afternoon = now.replace(hour=14, minute=0)

    # 记录早上9点的访问
    for i in range(5):
        prefetch_manager_with_time.record_access(
            f"morning_task_{i}",
            "morning_work",
            context="工作",
        )

    # 模拟现在是早上9点
    prediction = prefetch_manager_with_time.predict(current_time=morning)
    print(f"早上9点预测: {prediction.predicted_keys}")

    # 缓存预热示例
    print("\n缓存预热示例...")
    warmer = CacheWarmer(
        prefetch_manager=prefetch_manager,
        warmup_keys=["user_profile_1", "user_orders_1", "user_profile_2", "user_orders_2"],
        warmup_percentage=0.5,
    )

    def mock_cache_set(key, value):
        print(f"预热缓存: {key}")

    def mock_load(key):
        return f"data_{key}"

    warmed = warmer.warmup(mock_cache_set, mock_load)
    print(f"预热的键数量: {warmed}")
