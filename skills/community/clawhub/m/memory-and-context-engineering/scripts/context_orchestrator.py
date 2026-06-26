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
Agent Memory System - Context Orchestrator（上下文编排器）

=== 依赖与环境声明 ===
- 运行环境：Python >=3.9
- 直接依赖:
  * redis: >=4.5.0
    - 用途：状态协调
  * pydantic: >=2.0.0
    - 用途：配置模型验证
- 标准配置文件:
  ```text
  # requirements.txt
  redis>=4.5.0
  pydantic>=2.0.0
  ```
=== 声明结束 ===

安全提醒：作为总控层，需确保所有子模块的安全性

工具调用集成：
本模块支持 Agent 工具调用的结果验证和上下文编排，详见：
references/agent_tools_use_rules.md

- 支持工具调用结果的预验证和后验证
- 支持错误分类和反思机制
- 与 FallbackManager 集成实现降级策略
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable
import time

from pydantic import BaseModel, Field

from .type_defs import SemanticBucketType, MemoryCategory
from .redis_adapter import RedisAdapter, RedisConfig, create_redis_adapter
from .short_term_redis import ShortTermMemoryRedis, ShortTermRedisConfig
from .token_budget import (
    TokenBudgetManager,
    TokenBudgetConfig,
    TokenType,
    BudgetPolicy,
)


# ============================================================================
# 枚举类型
# ============================================================================


class ContextPriority(str, Enum):
    """上下文优先级"""

    CRITICAL = "critical"  # 关键：必须包含
    HIGH = "high"  # 高优先级
    MEDIUM = "medium"  # 中优先级
    LOW = "low"  # 低优先级
    OPTIONAL = "optional"  # 可选


class CompressionStrategy(str, Enum):
    """压缩策略"""

    PRIORITY_BASED = "priority_based"  # 基于优先级的压缩
    RELEVANCE_BASED = "relevance_based"  # 基于相关性的压缩
    FRESHNESS_BASED = "freshness_based"  # 基于新鲜度的压缩
    COMPOSITE = "composite"  # 综合评分（优先级+相关性+新鲜度）
    RULE_BASED = "rule_based"  # 基于规则的压缩
    CHAIN_AWARE = "chain_aware"  # 链感知压缩（优先保留链信息）


class ContextSource(str, Enum):
    """上下文来源"""

    SYSTEM = "system"  # 系统指令
    USER_INPUT = "user_input"  # 用户输入
    SHORT_TERM_MEMORY = "short_term_memory"  # 短期记忆
    LONG_TERM_MEMORY = "long_term_memory"  # 长期记忆
    RETRIEVAL = "retrieval"  # 检索结果
    TOOL_RESULT = "tool_result"  # 工具返回
    INSIGHT = "insight"  # 洞察建议
    REFLECTION = "reflection"  # 反思信息
    CUSTOM = "custom"  # 自定义来源（用于未知的上下文类型）


# ============================================================================
# 数据模型
# ============================================================================


class ContextBlock(BaseModel):
    """
    上下文块

    表示一个可被编排的上下文单元

    Metadata 规范：
    - subtype: str（可选）- 细粒度类型，如 "tool_prompt", "system_prompt"
    - custom_type: str（仅 CUSTOM 来源必需）- 自定义类型标识
    - version: str（可选）- 版本信息
    - timestamp: str（可选）- 时间戳（ISO 8601 格式）
    - source_id: str（可选）- 来源标识
    - weight: float（可选）- 自定义权重（0.0 - 1.0）
    - extra: dict（可选）- 额外的自定义数据

    链元数据（链感知压缩）：
    - chain_links: list[str]（可选）- 包含的链ID列表
    - chain_types: list[str]（可选）- 包含的链类型列表
    """

    source: ContextSource = Field(description="来源")
    priority: ContextPriority = Field(description="优先级")
    content: str = Field(description="内容")
    token_count: int = Field(default=0, description="Token 数量")
    metadata: dict[str, Any] = Field(default_factory=dict, description="元数据")

    # 用于排序和筛选
    relevance_score: float = Field(default=0.5, description="相关性分数")
    freshness_score: float = Field(default=1.0, description="新鲜度分数")

    # 链元数据（链感知压缩支持）
    chain_links: list[str] = Field(
        default_factory=list,
        description="包含的链ID列表（用于链完整性保持）"
    )
    chain_types: list[str] = Field(
        default_factory=list,
        description="包含的链类型列表（用于链价值评估）"
    )


class CompressionResult(BaseModel):
    """压缩结果"""

    compressed_blocks: list[ContextBlock] = Field(description="压缩后的上下文块列表")
    original_token_count: int = Field(description="原始 token 数")
    compressed_token_count: int = Field(description="压缩后 token 数")
    compression_ratio: float = Field(description="压缩率（压缩后/原始）")
    compression_time: float = Field(description="压缩耗时（秒）")
    removed_blocks: int = Field(description="移除的块数")
    quality_score: float = Field(description="压缩质量评分（0-100）")
    details: dict[str, Any] = Field(default_factory=dict, description="详细信息")


# ============================================================================
# Metadata 规范和验证
# ============================================================================


class MetadataValidator:
    """
    Metadata 验证器

    验证 metadata 字段的合法性和规范性
    """

    # 标准 metadata 字段定义
    STANDARD_FIELDS = {
        "subtype": {"type": str, "required": False, "description": "细粒度类型"},
        "custom_type": {
            "type": str,
            "required": False,  # 仅 CUSTOM 来源时必需
            "description": "自定义类型标识（仅 CUSTOM 来源）",
        },
        "version": {"type": str, "required": False, "description": "版本信息"},
        "timestamp": {
            "type": str,
            "required": False,
            "description": "时间戳（ISO 8601 格式）",
        },
        "source_id": {"type": str, "required": False, "description": "来源标识"},
        "weight": {
            "type": float,
            "required": False,
            "description": "自定义权重（0.0 - 1.0）",
            "min": 0.0,
            "max": 1.0,
        },
        "extra": {"type": dict, "required": False, "description": "额外的自定义数据"},
    }

    @classmethod
    def validate(cls, metadata: dict[str, Any], source: ContextSource) -> ValidationResult:
        """
        验证 metadata 字段

        Args:
            metadata: metadata 字典
            source: 上下文来源

        Returns:
            ValidationResult: 验证结果
        """
        if not metadata:
            return ValidationResult(valid=True, message="metadata 为空，跳过验证")

        errors = []

        # 验证 CUSTOM 来源必须有 custom_type
        if source == ContextSource.CUSTOM:
            if "custom_type" not in metadata:
                errors.append("CUSTOM 来源必须指定 custom_type 字段")

        # 验证标准字段
        for field_name, field_spec in cls.STANDARD_FIELDS.items():
            if field_name in metadata:
                field_value = metadata[field_name]

                # 类型验证
                if not isinstance(field_value, field_spec["type"]):
                    errors.append(
                        f"字段 '{field_name}' 类型错误：期望 {field_spec['type'].__name__}，"
                        f"实际 {type(field_value).__name__}"
                    )
                    continue

                # 范围验证（适用于数值类型）
                if field_name == "weight":
                    if not (0.0 <= field_value <= 1.0):
                        errors.append(f"字段 'weight' 必须在 0.0 - 1.0 范围内，实际值: {field_value}")

                # 格式验证（适用于字符串类型）
                if field_name == "timestamp":
                    if not cls._is_iso8601_timestamp(field_value):
                        errors.append(
                            f"字段 'timestamp' 必须符合 ISO 8601 格式，实际值: {field_value}"
                        )

        if errors:
            return ValidationResult(valid=False, message="; ".join(errors))

        return ValidationResult(valid=True, message="metadata 验证通过")

    @staticmethod
    def _is_iso8601_timestamp(timestamp: str) -> bool:
        """检查字符串是否符合 ISO 8601 格式"""
        import re

        iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$"
        return bool(re.match(iso8601_pattern, timestamp))


class ValidationResult(BaseModel):
    """验证结果"""

    valid: bool = Field(description="是否有效")
    message: str = Field(default="", description="验证消息")
    details: dict[str, Any] = Field(default_factory=dict, description="详细信息")


# ============================================================================
# 阶段 4：性能优化
# ============================================================================


class LRUCache:
    """
    LRU（最近最少使用）缓存实现

    提供高效的缓存淘汰策略和统计功能
    """

    def __init__(self, max_size: int = 1000):
        """
        初始化 LRU 缓存

        Args:
            max_size: 最大缓存大小
        """
        from collections import OrderedDict

        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._hits = 0
        self._misses = 0
        self._access_count = 0

    def get(self, key: str) -> Any | None:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            缓存值（如果存在）
        """
        self._access_count += 1

        if key in self._cache:
            self._hits += 1
            # 移动到末尾（标记为最近使用）
            self._cache.move_to_end(key)
            return self._cache[key]

        self._misses += 1
        return None

    def put(self, key: str, value: Any) -> None:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
        """
        if key in self._cache:
            # 更新现有值并移动到末尾
            self._cache.move_to_end(key)
            self._cache[key] = value
        else:
            # 添加新值
            if len(self._cache) >= self._max_size:
                # 淘汰最久未使用的项
                self._cache.popitem(last=False)
            self._cache[key] = value

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
        self._hits = 0
        self._misses = 0
        self._access_count = 0

    def stats(self) -> dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            统计信息字典
        """
        hit_rate = self._hits / self._access_count if self._access_count > 0 else 0.0

        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "access_count": self._access_count,
            "hit_rate": round(hit_rate, 4),
        }

    def __len__(self) -> int:
        """返回缓存大小"""
        return len(self._cache)


class PerformanceMonitor:
    """
    性能监控器

    监控操作延迟、吞吐量和资源使用
    """

    def __init__(self):
        """初始化性能监控器"""
        import time

        self._operation_times: dict[str, list[float]] = {}
        self._operation_counts: dict[str, int] = {}
        self._start_time = time.time()

    def record_operation(self, operation_name: str, duration: float) -> None:
        """
        记录操作时间

        Args:
            operation_name: 操作名称
            duration: 操作耗时（秒）
        """
        if operation_name not in self._operation_times:
            self._operation_times[operation_name] = []
            self._operation_counts[operation_name] = 0

        self._operation_times[operation_name].append(duration)
        self._operation_counts[operation_name] += 1

    def get_stats(self) -> dict[str, Any]:
        """
        获取性能统计

        Returns:
            性能统计字典
        """
        import time

        stats = {
            "uptime_seconds": round(time.time() - self._start_time, 2),
            "operations": {},
        }

        for op_name, times in self._operation_times.items():
            if times:
                stats["operations"][op_name] = {
                    "count": self._operation_counts[op_name],
                    "total_time": round(sum(times), 4),
                    "avg_time": round(sum(times) / len(times), 4),
                    "min_time": round(min(times), 4),
                    "max_time": round(max(times), 4),
                    "last_time": round(times[-1], 4),
                }

        return stats

    def generate_report(self) -> str:
        """
        生成性能报告

        Returns:
            性能报告字符串
        """
        lines = []
        lines.append("=== 性能监控报告 ===\n")

        stats = self.get_stats()

        lines.append(f"运行时间: {stats['uptime_seconds']} 秒")
        lines.append(f"监控的操作数: {len(stats['operations'])}\n")

        lines.append("【操作统计】")
        for op_name, op_stats in stats["operations"].items():
            lines.append(f"\n  {op_name}:")
            lines.append(f"    调用次数: {op_stats['count']}")
            lines.append(f"    总耗时: {op_stats['total_time']} 秒")
            lines.append(f"    平均耗时: {op_stats['avg_time']} 秒")
            lines.append(f"    最小耗时: {op_stats['min_time']} 秒")
            lines.append(f"    最大耗时: {op_stats['max_time']} 秒")

        return "\n".join(lines)


class BatchProcessor:
    """
    批量处理器

    优化批量处理操作的性能
    """

    @staticmethod
    def validate_metadata_batch(
        metadata_list: list[dict[str, Any]], source_list: list[ContextSource]
    ) -> list[ValidationResult]:
        """
        批量验证 metadata

        Args:
            metadata_list: metadata 列表
            source_list: source 列表

        Returns:
            验证结果列表
        """
        if len(metadata_list) != len(source_list):
            raise ValueError("metadata_list 和 source_list 长度必须相同")

        results = []
        for metadata, source in zip(metadata_list, source_list):
            result = MetadataValidator.validate(metadata, source)
            results.append(result)

        return results

    @staticmethod
    def resolve_priorities_batch_optimized(
        resolver: PriorityResolver, blocks: list[ContextBlock]
    ) -> list[tuple[ContextPriority, str]]:
        """
        优化的批量优先级解析

        Args:
            resolver: 优先级解析器
            blocks: 上下文块列表

        Returns:
            优先级和日志列表
        """
        return [resolver.resolve(block.source, block.metadata) for block in blocks]

    @staticmethod
    def assess_quality_batch(
        assessor: MetadataQualityAssessor,
        blocks: list[ContextBlock],
        custom_types_registry: dict[str, dict],
    ) -> list[QualityAssessment]:
        """
        批量质量评估

        Args:
            assessor: 质量评估器
            blocks: 上下文块列表
            custom_types_registry: 自定义类型注册表

        Returns:
            质量评估结果列表
        """
        return [
            assessor.assess_quality(block.metadata, block.source, custom_types_registry)
            for block in blocks
        ]


# ============================================================================
# 阶段 5.1：上下文压缩
# ============================================================================


class ContextCompressor:
    """
    上下文压缩器

    支持多种压缩策略，减少上下文块的 token 数量
    """

    # 优先级权重（用于综合评分）
    PRIORITY_WEIGHTS: dict[ContextPriority, float] = {
        ContextPriority.CRITICAL: 5.0,
        ContextPriority.HIGH: 4.0,
        ContextPriority.MEDIUM: 3.0,
        ContextPriority.LOW: 2.0,
        ContextPriority.OPTIONAL: 1.0,
    }

    def __init__(
        self,
        enable_auto_compress: bool = False,
        auto_compress_threshold: float = 0.8,
        default_strategy: CompressionStrategy = CompressionStrategy.PRIORITY_BASED,
    ):
        """
        初始化上下文压缩器

        Args:
            enable_auto_compress: 是否启用自动压缩
            auto_compress_threshold: 自动压缩触发阈值（使用率）
            default_strategy: 默认压缩策略
        """
        self._enable_auto_compress = enable_auto_compress
        self._auto_compress_threshold = auto_compress_threshold
        self._default_strategy = default_strategy

        # 链类型权重配置（用于链感知压缩）
        self._chain_type_weights = {
            "causal": 40,
            "logic": 35,
            "operation": 35,
            "narrative": 30,
            "time": 25,
        }

    def set_chain_type_weights(self, weights: dict[str, int]) -> None:
        """
        设置链类型权重

        Args:
            weights: 链类型到权重的映射
        """
        self._chain_type_weights.update(weights)

    def compress(
        self,
        blocks: list[ContextBlock],
        compression_ratio: float = 0.7,
        strategy: CompressionStrategy | None = None,
        min_blocks: int = 1,
        target_tokens: int | None = None,
    ) -> CompressionResult:
        """
        压缩上下文块

        Args:
            blocks: 上下文块列表
            compression_ratio: 压缩比率（保留的 token 比例，0.0 - 1.0）
            strategy: 压缩策略（None 则使用默认策略）
            min_blocks: 最小保留块数
            target_tokens: 目标 token 数（优先级高于 compression_ratio）

        Returns:
            CompressionResult 压缩结果
        """
        import time

        start_time = time.time()
        strategy = strategy or self._default_strategy

        # 计算原始 token 数
        original_token_count = sum(block.token_count for block in blocks)

        # 如果没有块或原始 token 数为 0，直接返回
        if not blocks or original_token_count == 0:
            return CompressionResult(
                compressed_blocks=[],
                original_token_count=original_token_count,
                compressed_token_count=0,
                compression_ratio=0.0,
                compression_time=time.time() - start_time,
                removed_blocks=len(blocks),
                quality_score=100.0,
                details={"strategy": strategy.value, "reason": "No blocks to compress"},
            )

        # 计算目标 token 数
        if target_tokens is not None:
            target_count = target_tokens
        else:
            target_count = int(original_token_count * compression_ratio)

        # 根据策略排序
        if strategy == CompressionStrategy.PRIORITY_BASED:
            sorted_blocks = self._sort_by_priority(blocks)
        elif strategy == CompressionStrategy.RELEVANCE_BASED:
            sorted_blocks = self._sort_by_relevance(blocks)
        elif strategy == CompressionStrategy.FRESHNESS_BASED:
            sorted_blocks = self._sort_by_freshness(blocks)
        elif strategy == CompressionStrategy.COMPOSITE:
            sorted_blocks = self._sort_by_composite(blocks)
        elif strategy == CompressionStrategy.RULE_BASED:
            sorted_blocks = self._sort_by_rules(blocks)
        elif strategy == CompressionStrategy.CHAIN_AWARE:
            sorted_blocks = self._sort_by_chain_aware(blocks)
        else:
            sorted_blocks = self._sort_by_priority(blocks)

        # 选择前 N 个块（保证至少保留 min_blocks 个）
        selected_blocks = []
        current_tokens = 0

        for block in sorted_blocks:
            # 保证至少保留 min_blocks 个块
            if len(selected_blocks) >= min_blocks and current_tokens >= target_count:
                break

            selected_blocks.append(block)
            current_tokens += block.token_count

        # 重新按原始顺序排序（使用索引）
        original_order_map = {i: block for i, block in enumerate(blocks)}
        compressed_block_indices = [i for i, block in enumerate(blocks) if block in selected_blocks]
        compressed_blocks = [original_order_map[i] for i in sorted(compressed_block_indices)]

        # 计算压缩统计
        compressed_token_count = sum(block.token_count for block in compressed_blocks)
        actual_compression_ratio = (
            compressed_token_count / original_token_count if original_token_count > 0 else 0.0
        )
        removed_blocks = len(blocks) - len(compressed_blocks)
        compression_time = time.time() - start_time

        # 计算质量评分
        quality_score = self._calculate_quality_score(
            original_blocks=blocks,
            compressed_blocks=compressed_blocks,
            target_tokens=target_count if target_tokens else int(original_token_count * compression_ratio),
        )

        return CompressionResult(
            compressed_blocks=compressed_blocks,
            original_token_count=original_token_count,
            compressed_token_count=compressed_token_count,
            compression_ratio=round(actual_compression_ratio, 4),
            compression_time=round(compression_time, 4),
            removed_blocks=removed_blocks,
            quality_score=round(quality_score, 2),
            details={
                "strategy": strategy.value,
                "min_blocks": min_blocks,
                "target_ratio": compression_ratio if target_tokens is None else None,
                "target_tokens": target_tokens,
            },
        )

    def auto_compress(
        self,
        blocks: list[ContextBlock],
        max_tokens: int,
        min_blocks: int = 1,
    ) -> CompressionResult | None:
        """
        自动压缩（当 token 数超过 max_tokens 时触发）

        Args:
            blocks: 上下文块列表
            max_tokens: 最大 token 数
            min_blocks: 最小保留块数

        Returns:
            CompressionResult 压缩结果（如果需要压缩则返回结果，否则返回 None）
        """
        current_tokens = sum(block.token_count for block in blocks)

        # 如果当前 token 数未超过阈值，不需要压缩
        if current_tokens <= max_tokens:
            return None

        # 计算需要的压缩比率
        compression_ratio = max_tokens / current_tokens

        # 执行压缩
        return self.compress(
            blocks=blocks,
            compression_ratio=compression_ratio,
            strategy=self._default_strategy,
            min_blocks=min_blocks,
        )

    def _sort_by_priority(self, blocks: list[ContextBlock]) -> list[ContextBlock]:
        """按优先级排序"""
        return sorted(blocks, key=lambda b: (self.PRIORITY_WEIGHTS.get(b.priority, 0), -b.token_count), reverse=True)

    def _sort_by_relevance(self, blocks: list[ContextBlock]) -> list[ContextBlock]:
        """按相关性排序"""
        return sorted(blocks, key=lambda b: (b.relevance_score, -b.token_count), reverse=True)

    def _sort_by_freshness(self, blocks: list[ContextBlock]) -> list[ContextBlock]:
        """按新鲜度排序"""
        return sorted(blocks, key=lambda b: (b.freshness_score, -b.token_count), reverse=True)

    def _sort_by_composite(self, blocks: list[ContextBlock]) -> list[ContextBlock]:
        """按综合评分排序（优先级 + 相关性 + 新鲜度）"""
        def composite_score(block: ContextBlock) -> float:
            priority_weight = self.PRIORITY_WEIGHTS.get(block.priority, 0)
            relevance_weight = block.relevance_score
            freshness_weight = block.freshness_score

            # 归一化权重
            priority_weight = priority_weight / 5.0  # 最大优先级权重为 5

            # 综合评分（可调整权重比例）
            return 0.5 * priority_weight + 0.3 * relevance_weight + 0.2 * freshness_weight

        return sorted(blocks, key=lambda b: (composite_score(b), -b.token_count), reverse=True)

    def _sort_by_rules(self, blocks: list[ContextBlock]) -> list[ContextBlock]:
        """按规则排序（保留关键内容）"""
        # 定义规则优先级
        rule_priority = {
            ContextSource.SYSTEM: 100,
            ContextSource.USER_INPUT: 90,
            ContextPriority.CRITICAL: 80,
            ContextPriority.HIGH: 70,
        }

        def rule_score(block: ContextBlock) -> float:
            # 检查 metadata 中的关键信息
            score = 0

            # 检查来源
            score += rule_priority.get(block.source, 0)

            # 检查优先级
            score += rule_priority.get(block.priority, 0)

            # 检查 metadata 中的关键信息
            if block.metadata.get("subtype") == "system_prompt":
                score += 50
            if block.metadata.get("custom_type"):
                score += 30
            if block.metadata.get("version"):
                score += 10

            # 检查因果链（因果链包含关键的逻辑推导，应优先保留）
            if "causal_chain" in block.metadata:
                score += 30  # 包含因果链的基础权重

                # 因果链越长，权重越高（最多 +50）
                causal_chain = block.metadata["causal_chain"]
                if isinstance(causal_chain, list):
                    chain_length = len(causal_chain)
                    score += min(chain_length * 5, 50)

            return score

        return sorted(blocks, key=lambda b: (rule_score(b), -b.token_count), reverse=True)

    def _sort_by_chain_aware(self, blocks: list[ContextBlock]) -> list[ContextBlock]:
        """
        链感知排序（优先保留包含链信息的块）

        阶段1：链元数据增强
        - 为每种链类型分配权重
        - 基于链数量和类型提升优先级
        - 支持跨块链的识别

        Args:
            blocks: 上下文块列表

        Returns:
            排序后的上下文块列表
        """
        def chain_aware_score(block: ContextBlock) -> float:
            """计算链感知评分"""
            score = 0.0

            # 1. 基础优先级权重
            score += self.PRIORITY_WEIGHTS.get(block.priority, 0) * 10

            # 2. 链类型权重（累加所有链类型的权重）
            for chain_type in block.chain_types:
                score += self._chain_type_weights.get(chain_type, 0)

            # 3. 链数量奖励（跨块链）
            score += len(block.chain_links) * 15

            # 4. 相关性和新鲜度作为辅助因素
            score += block.relevance_score * 10
            score += block.freshness_score * 10

            # 5. 检查metadata中的旧式链标记（向后兼容）
            if "causal_chain" in block.metadata:
                score += 30  # 包含因果链的基础权重
                causal_chain = block.metadata["causal_chain"]
                if isinstance(causal_chain, list):
                    chain_length = len(causal_chain)
                    score += min(chain_length * 5, 50)

            return score

        return sorted(blocks, key=lambda b: (chain_aware_score(b), -b.token_count), reverse=True)

    def _calculate_quality_score(
        self,
        original_blocks: list[ContextBlock],
        compressed_blocks: list[ContextBlock],
        target_tokens: int,
    ) -> float:
        """
        计算压缩质量评分

        Args:
            original_blocks: 原始上下文块列表
            compressed_blocks: 压缩后的上下文块列表
            target_tokens: 目标 token 数

        Returns:
            质量评分（0-100）
        """
        score = 100.0

        # 使用索引追踪块
        compressed_indices = set()
        for i, block in enumerate(original_blocks):
            if block in compressed_blocks:
                compressed_indices.add(i)

        # 检查是否保留了关键块（CRITICAL 和 HIGH）
        for i, block in enumerate(original_blocks):
            if block.priority == ContextPriority.CRITICAL and i not in compressed_indices:
                score -= 20
            elif block.priority == ContextPriority.HIGH and i not in compressed_indices:
                score -= 10

        # token 数量接近度奖励
        compressed_tokens = sum(b.token_count for b in compressed_blocks)
        if compressed_tokens <= target_tokens:
            score += 10
        else:
            # 超过目标 token，按比例扣分
            over_ratio = (compressed_tokens - target_tokens) / target_tokens
            score -= min(over_ratio * 50, 30)

        # 压缩率奖励（压缩率越高，奖励越多）
        compression_ratio = len(compressed_blocks) / len(original_blocks) if original_blocks else 0
        if compression_ratio < 1.0:
            score += (1.0 - compression_ratio) * 10

        return max(0.0, min(100.0, score))


# ============================================================================
# 优先级解析
# ============================================================================


class PriorityResolver:
    """
    优先级解析器（优化版）

    根据 source 和 metadata 解析最终的优先级
    使用 LRU 缓存提升性能
    """

    # 默认优先级（按 source）
    DEFAULT_PRIORITIES: dict[ContextSource, ContextPriority] = {
        ContextSource.SYSTEM: ContextPriority.CRITICAL,
        ContextSource.USER_INPUT: ContextPriority.CRITICAL,
        ContextSource.SHORT_TERM_MEMORY: ContextPriority.HIGH,
        ContextSource.LONG_TERM_MEMORY: ContextPriority.HIGH,
        ContextSource.RETRIEVAL: ContextPriority.MEDIUM,
        ContextSource.TOOL_RESULT: ContextPriority.LOW,
        ContextSource.INSIGHT: ContextPriority.OPTIONAL,
        ContextSource.REFLECTION: ContextPriority.OPTIONAL,
        ContextSource.CUSTOM: ContextPriority.MEDIUM,  # CUSTOM 类型默认为 MEDIUM
    }

    # 动态优先级规则（按 subtype）
    SUBTYPE_RULES: dict[str, dict] = {
        "system_prompt": {"priority": "critical", "weight": 1.0},
        "user_prompt": {"priority": "critical", "weight": 1.0},
        "tool_prompt": {"priority": "medium", "weight": 0.6},
        "conversation_history": {"priority": "high", "weight": 0.8},
        "code_snippet": {"priority": "medium", "weight": 0.5},
        "file_content": {"priority": "medium", "weight": 0.5},
        "api_response": {"priority": "medium", "weight": 0.5},
    }

    # 自定义类型规则（按 custom_type）
    CUSTOM_RULES: dict[str, dict] = {}

    def __init__(self, enable_lru_cache: bool = True, cache_size: int = 1000):
        """
        初始化优先级解析器

        Args:
            enable_lru_cache: 是否启用 LRU 缓存
            cache_size: 缓存大小
        """
        self._enable_lru_cache = enable_lru_cache

        if enable_lru_cache:
            self._priority_cache = LRUCache(max_size=cache_size)
        else:
            self._priority_cache: dict[str, ContextPriority] = {}

    def resolve(
        self, source: ContextSource, metadata: dict[str, Any]
    ) -> tuple[ContextPriority, str]:
        """
        解析优先级

        Args:
            source: 上下文来源
            metadata: metadata 字典

        Returns:
            (优先级, 解析日志)
        """
        # 生成缓存键
        cache_key = self._generate_cache_key(source, metadata)

        # 检查缓存（支持 LRU 缓存和普通字典）
        if self._enable_lru_cache:
            cached_priority = self._priority_cache.get(cache_key)
            if cached_priority is not None:
                return cached_priority, "（从 LRU 缓存获取）"
        else:
            if cache_key in self._priority_cache:
                return self._priority_cache[cache_key], "（从缓存获取）"

        # 解析优先级
        priority, log = self._resolve_impl(source, metadata)

        # 缓存结果
        if self._enable_lru_cache:
            self._priority_cache.put(cache_key, priority)
        else:
            self._priority_cache[cache_key] = priority

        return priority, log

    def _resolve_impl(
        self, source: ContextSource, metadata: dict[str, Any]
    ) -> tuple[ContextPriority, str]:
        """实际的优先级解析实现"""
        steps = []

        # 步骤 1: 检查是否是 CUSTOM 类型
        if source == ContextSource.CUSTOM:
            steps.append("步骤1: 检测到 CUSTOM 类型")
            custom_type = metadata.get("custom_type")
            if custom_type and custom_type in self.CUSTOM_RULES:
                steps.append(f"步骤2: 找到 custom_type 规则: {custom_type}")
                priority = ContextPriority(self.CUSTOM_RULES[custom_type]["priority"])
                return priority, "\n".join(steps)
            elif custom_type:
                steps.append(f"步骤2: custom_type '{custom_type}' 未注册，使用默认优先级")
                return ContextPriority.MEDIUM, "\n".join(steps)
            else:
                steps.append("步骤2: 缺少 custom_type，使用默认优先级")
                return ContextPriority.MEDIUM, "\n".join(steps)

        # 步骤 2: 检查是否有 subtype 规则
        subtype = metadata.get("subtype")
        if subtype and subtype in self.SUBTYPE_RULES:
            steps.append(f"步骤1: 找到 subtype 规则: {subtype}")
            priority = ContextPriority(self.SUBTYPE_RULES[subtype]["priority"])
            return priority, "\n".join(steps)

        # 步骤 3: 检查是否有 source + subtype 组合规则
        if subtype:
            combination_key = f"{source.value}#{subtype}"
            steps.append(f"步骤1: 检查组合规则: {combination_key}")
            # 这里可以扩展组合规则
            steps.append("步骤2: 未找到组合规则，使用默认优先级")

        # 步骤 4: 使用默认优先级
        steps.append(f"使用默认优先级: {source.value}")
        default_priority = self.DEFAULT_PRIORITIES.get(source, ContextPriority.MEDIUM)
        return default_priority, "\n".join(steps)

    def _generate_cache_key(self, source: ContextSource, metadata: dict[str, Any]) -> str:
        """生成缓存键"""
        import hashlib
        import json

        # 将 metadata 转换为排序后的 JSON 字符串
        metadata_str = json.dumps(metadata, sort_keys=True)
        # 生成哈希
        cache_key = f"{source.value}:{hashlib.md5(metadata_str.encode()).hexdigest()}"
        return cache_key

    def register_custom_type(
        self, custom_type: str, priority: ContextPriority, required_fields: list[str] = None
    ) -> None:
        """
        注册自定义类型

        Args:
            custom_type: 自定义类型名称
            priority: 优先级
            required_fields: 必需字段列表
        """
        self.CUSTOM_RULES[custom_type] = {
            "priority": priority.value,
            "required_fields": required_fields or [],
        }
        # 清空缓存
        self._priority_cache.clear()

    def register_subtype_rule(self, subtype: str, priority: ContextPriority, weight: float = 1.0) -> None:
        """
        注册 subtype 规则

        Args:
            subtype: 细粒度类型名称（如 "tool_prompt", "system_prompt"）
            priority: 优先级
            weight: 权重（0.0 - 1.0）
        """
        self.SUBTYPE_RULES[subtype] = {
            "priority": priority.value,
            "weight": weight,
        }
        # 清空缓存
        self._priority_cache.clear()

    def get_custom_types(self) -> dict[str, dict]:
        """获取所有已注册的自定义类型"""
        return dict(self.CUSTOM_RULES)

    def get_subtype_rules(self) -> dict[str, dict]:
        """获取所有 subtype 规则"""
        return dict(self.SUBTYPE_RULES)

    def unregister_custom_type(self, custom_type: str) -> bool:
        """注销自定义类型"""
        if custom_type in self.CUSTOM_RULES:
            del self.CUSTOM_RULES[custom_type]
            self._priority_cache.clear()
            return True
        return False

    def unregister_subtype_rule(self, subtype: str) -> bool:
        """注销 subtype 规则"""
        if subtype in self.SUBTYPE_RULES:
            del self.SUBTYPE_RULES[subtype]
            self._priority_cache.clear()
            return True
        return False

    def resolve_priorities_batch(
        self, blocks: list[ContextBlock]
    ) -> list[tuple[ContextPriority, str]]:
        """批量解析优先级"""
        return [self.resolve(block.source, block.metadata) for block in blocks]

    def clear_cache(self) -> None:
        """清空优先级缓存"""
        self._priority_cache.clear()

    def get_cache_stats(self) -> dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            缓存统计字典
        """
        if self._enable_lru_cache:
            return self._priority_cache.stats()
        else:
            return {
                "type": "dict",
                "size": len(self._priority_cache),
            }

    def enable_lru_cache(self, cache_size: int = 1000) -> None:
        """
        启用 LRU 缓存

        Args:
            cache_size: 缓存大小
        """
        if not self._enable_lru_cache:
            self._enable_lru_cache = True
            self._priority_cache = LRUCache(max_size=cache_size)

    def disable_lru_cache(self) -> None:
        """禁用 LRU 缓存"""
        if self._enable_lru_cache:
            self._enable_lru_cache = False
            self._priority_cache: dict[str, ContextPriority] = {}


class ContextConfig(BaseModel):
    """
    Context Orchestrator 配置

    使用示例：
    ```python
    config = ContextConfig(
        max_context_tokens=32000,
        enable_auto_compression=True,
    )
    ```
    """

    # Token 预算
    max_context_tokens: int = Field(default=32000, description="最大上下文 Token 数")

    # 优先级权重
    priority_weights: dict[str, float] = Field(
        default_factory=lambda: {
            "critical": 1.0,
            "high": 0.8,
            "medium": 0.5,
            "low": 0.3,
            "optional": 0.1,
        },
        description="优先级权重",
    )

    # 自动压缩
    enable_auto_compression: bool = Field(default=True, description="启用自动压缩")

    # 检索配置
    max_retrieval_results: int = Field(default=10, description="最大检索结果数")

    # 短期记忆配置
    max_short_term_items: int = Field(default=50, description="最大短期记忆项数")


class PreparedContext(BaseModel):
    """
    准备好的上下文

    编排器输出的最终上下文结构
    """

    # 最终内容
    content: str = Field(description="完整上下文内容")
    token_count: int = Field(default=0, description="总 Token 数")

    # 组成明细
    blocks: list[ContextBlock] = Field(default_factory=list, description="上下文块列表")

    # 统计信息
    stats: dict[str, Any] = Field(default_factory=dict, description="统计信息")

    # 警告
    warnings: list[str] = Field(default_factory=list, description="警告信息")


# ============================================================================
# 阶段 3：质量评估与生命周期管理
# ============================================================================


class QualityAssessment(BaseModel):
    """质量评估结果"""

    score: float = Field(description="总分 (0-100)")
    completeness_score: float = Field(description="完整性得分")
    accuracy_score: float = Field(description="准确性得分")
    consistency_score: float = Field(description="一致性得分")
    usability_score: float = Field(description="实用性得分")

    issues: list[str] = Field(default_factory=list, description="问题列表")
    recommendations: list[str] = Field(default_factory=list, description="改进建议")


class MetadataQualityAssessor:
    """
    Metadata 质量评估器

    评估 metadata 的完整性、准确性、一致性和实用性
    """

    # 评分权重配置
    WEIGHTS: dict[str, float] = {
        "completeness": 0.4,  # 完整性 40%
        "accuracy": 0.3,      # 准确性 30%
        "consistency": 0.2,   # 一致性 20%
        "usability": 0.1,     # 实用性 10%
    }

    def __init__(self, weights: dict[str, float] | None = None):
        """
        初始化质量评估器

        Args:
            weights: 自定义权重配置
        """
        if weights:
            self.WEIGHTS.update(weights)

    def assess_quality(
        self, metadata: dict[str, Any], source: ContextSource, custom_types_registry: dict[str, dict]
    ) -> QualityAssessment:
        """
        评估 metadata 质量

        Args:
            metadata: metadata 字典
            source: 上下文来源
            custom_types_registry: 自定义类型注册表

        Returns:
            QualityAssessment 评估结果
        """
        issues = []
        recommendations = []

        # 1. 完整性检查
        completeness_score, completeness_issues = self._check_completeness(
            metadata, source, custom_types_registry
        )
        issues.extend(completeness_issues)

        # 2. 准确性检查
        accuracy_score, accuracy_issues = self._check_accuracy(metadata)
        issues.extend(accuracy_issues)

        # 3. 一致性检查
        consistency_score, consistency_issues = self._check_consistency(
            metadata, source, custom_types_registry
        )
        issues.extend(consistency_issues)

        # 4. 实用性检查
        usability_score, usability_recommendations = self._check_usability(metadata)
        recommendations.extend(usability_recommendations)

        # 计算总分
        total_score = (
            completeness_score * self.WEIGHTS["completeness"]
            + accuracy_score * self.WEIGHTS["accuracy"]
            + consistency_score * self.WEIGHTS["consistency"]
            + usability_score * self.WEIGHTS["usability"]
        )

        return QualityAssessment(
            score=round(total_score, 2),
            completeness_score=round(completeness_score, 2),
            accuracy_score=round(accuracy_score, 2),
            consistency_score=round(consistency_score, 2),
            usability_score=round(usability_score, 2),
            issues=issues,
            recommendations=recommendations,
        )

    def _check_completeness(
        self, metadata: dict[str, Any], source: ContextSource, custom_types_registry: dict[str, dict]
    ) -> tuple[float, list[str]]:
        """检查完整性"""
        issues = []

        # CUSTOM 来源必须包含 custom_type
        if source == ContextSource.CUSTOM:
            if "custom_type" not in metadata:
                issues.append("CUSTOM 来源缺少必需字段: custom_type")
                return 0.0, issues

            # 检查 custom_type 是否已注册
            custom_type = metadata["custom_type"]
            if custom_type not in custom_types_registry:
                issues.append(f"custom_type '{custom_type}' 未在注册表中")

        # 推荐字段
        recommended_fields = ["timestamp", "source_id"]
        missing_recommended = [f for f in recommended_fields if f not in metadata]
        if missing_recommended:
            issues.append(f"缺少推荐字段: {', '.join(missing_recommended)}")

        # 计算分数
        if issues:
            score = 0.0 if any("缺少必需字段" in issue for issue in issues) else 50.0
        else:
            score = 100.0

        return score, issues

    def _check_accuracy(self, metadata: dict[str, Any]) -> tuple[float, list[str]]:
        """检查准确性"""
        issues = []

        # 检查 weight 范围
        if "weight" in metadata:
            weight = metadata["weight"]
            if not isinstance(weight, (int, float)):
                issues.append(f"weight 字段类型错误: {type(weight).__name__}")
            elif not (0.0 <= weight <= 1.0):
                issues.append(f"weight 超出范围: {weight}")

        # 检查 timestamp 格式
        if "timestamp" in metadata:
            timestamp = metadata["timestamp"]
            if not MetadataValidator._is_iso8601_timestamp(timestamp):
                issues.append(f"timestamp 格式错误: {timestamp}")

        score = 100.0 if not issues else 0.0
        return score, issues

    def _check_consistency(
        self, metadata: dict[str, Any], source: ContextSource, custom_types_registry: dict[str, dict]
    ) -> tuple[float, list[str]]:
        """检查一致性"""
        issues = []

        # 检查 custom_type 注册一致性
        if source == ContextSource.CUSTOM and "custom_type" in metadata:
            custom_type = metadata["custom_type"]
            if custom_type in custom_types_registry:
                required_fields = custom_types_registry[custom_type].get("required_fields", [])
                for field in required_fields:
                    if field not in metadata:
                        issues.append(f"custom_type '{custom_type}' 缺少必需字段: {field}")

        score = 100.0 if not issues else 0.0
        return score, issues

    def _check_usability(self, metadata: dict[str, Any]) -> tuple[float, list[str]]:
        """检查实用性"""
        recommendations = []

        # 检查是否有有用的 metadata 字段
        useful_fields = ["subtype", "version", "source_id", "timestamp", "weight"]
        has_useful = any(field in metadata for field in useful_fields)

        if not has_useful:
            recommendations.append("建议添加有用的 metadata 字段以提高可追溯性")

        # 检查 extra 字段
        if "extra" in metadata:
            if not isinstance(metadata["extra"], dict):
                recommendations.append("extra 字段应该是字典类型")

        score = 100.0 if has_useful else 50.0
        return score, recommendations


class CustomTypeLifecycleManager:
    """
    自定义类型生命周期管理器

    管理自定义类型的创建、使用、废弃和清理
    """

    def __init__(self, storage_path: str = "usage_stats.json"):
        """
        初始化生命周期管理器

        Args:
            storage_path: 统计数据存储路径
        """
        self._storage_path = storage_path
        self._type_registry: dict[str, dict] = {}
        self._usage_stats: dict[str, dict] = {}
        self._load_usage_stats()

    def register_type(
        self,
        custom_type: str,
        priority: ContextPriority,
        required_fields: list[str] | None = None,
        description: str = "",
        creator: str = "unknown",
    ) -> None:
        """
        注册自定义类型（增强版）

        Args:
            custom_type: 自定义类型名称
            priority: 优先级
            required_fields: 必需字段列表
            description: 描述
            creator: 创建者
        """
        self._type_registry[custom_type] = {
            "priority": priority.value,
            "required_fields": required_fields or [],
            "description": description,
            "creator": creator,
            "created_at": self._get_timestamp(),
            "deprecated": False,
        }
        self._save_usage_stats()

    def track_usage(self, custom_type: str, usage_info: dict[str, Any] | None = None) -> None:
        """
        记录类型使用

        Args:
            custom_type: 自定义类型名称
            usage_info: 使用信息（可选）
        """
        if custom_type not in self._usage_stats:
            self._usage_stats[custom_type] = {
                "count": 0,
                "first_used": None,
                "last_used": None,
            }

        self._usage_stats[custom_type]["count"] += 1
        self._usage_stats[custom_type]["last_used"] = self._get_timestamp()

        if self._usage_stats[custom_type]["first_used"] is None:
            self._usage_stats[custom_type]["first_used"] = self._get_timestamp()

        if usage_info:
            self._usage_stats[custom_type]["last_usage_info"] = usage_info

        self._save_usage_stats()

    def deprecate_type(self, custom_type: str, reason: str = "") -> None:
        """
        废弃类型

        Args:
            custom_type: 自定义类型名称
            reason: 废弃原因
        """
        if custom_type in self._type_registry:
            self._type_registry[custom_type]["deprecated"] = True
            self._type_registry[custom_type]["deprecated_at"] = self._get_timestamp()
            self._type_registry[custom_type]["deprecated_reason"] = reason
            self._save_usage_stats()

    def cleanup_unused_types(self, threshold_days: int = 90) -> list[str]:
        """
        清理长期未使用的类型

        Args:
            threshold_days: 阈值天数（默认 90 天）

        Returns:
            被清理的类型列表
        """
        import time
        from datetime import datetime, timedelta

        threshold = datetime.now() - timedelta(days=threshold_days)
        cleaned_types = []

        for custom_type, stats in list(self._usage_stats.items()):
            last_used = stats.get("last_used")
            if last_used:
                try:
                    last_used_date = datetime.fromisoformat(last_used)
                    if last_used_date < threshold:
                        # 检查是否已废弃
                        if (
                            custom_type in self._type_registry
                            and self._type_registry[custom_type].get("deprecated", False)
                        ):
                            del self._type_registry[custom_type]
                            del self._usage_stats[custom_type]
                            cleaned_types.append(custom_type)
                except ValueError:
                    pass

        if cleaned_types:
            self._save_usage_stats()

        return cleaned_types

    def get_type_stats(self, custom_type: str) -> dict[str, Any] | None:
        """
        获取类型统计信息

        Args:
            custom_type: 自定义类型名称

        Returns:
            统计信息字典
        """
        return self._usage_stats.get(custom_type)

    def get_all_types(self) -> dict[str, dict]:
        """获取所有已注册的类型"""
        return dict(self._type_registry)

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime

        return datetime.now().isoformat()

    def _load_usage_stats(self) -> None:
        """加载统计数据"""
        import json
        import os

        if os.path.exists(self._storage_path):
            try:
                with open(self._storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._type_registry = data.get("type_registry", {})
                    self._usage_stats = data.get("usage_stats", {})
            except Exception:
                # 加载失败，使用空字典
                self._type_registry = {}
                self._usage_stats = {}

    def _save_usage_stats(self) -> None:
        """保存统计数据"""
        import json

        data = {
            "type_registry": self._type_registry,
            "usage_stats": self._usage_stats,
        }

        with open(self._storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class UsageMonitor:
    """
    使用情况监控器

    监控 metadata 的使用情况
    """

    def __init__(self):
        """初始化使用监控器"""
        self._stats: dict[str, Any] = {
            "source_usage": {},
            "subtype_usage": {},
            "custom_type_usage": {},
            "field_usage": {},
        }

    def record_usage(
        self,
        source: ContextSource,
        subtype: str | None = None,
        custom_type: str | None = None,
        metadata_fields: list[str] | None = None,
    ) -> None:
        """
        记录使用

        Args:
            source: 上下文来源
            subtype: 细粒度类型
            custom_type: 自定义类型
            metadata_fields: metadata 字段列表
        """
        # 统计 source 使用
        source_key = source.value
        self._stats["source_usage"][source_key] = self._stats["source_usage"].get(source_key, 0) + 1

        # 统计 subtype 使用
        if subtype:
            self._stats["subtype_usage"][subtype] = self._stats["subtype_usage"].get(subtype, 0) + 1

        # 统计 custom_type 使用
        if custom_type:
            self._stats["custom_type_usage"][
                custom_type
            ] = self._stats["custom_type_usage"].get(custom_type, 0) + 1

        # 统计字段使用
        if metadata_fields:
            for field in metadata_fields:
                self._stats["field_usage"][field] = self._stats["field_usage"].get(field, 0) + 1

    def get_usage_stats(self) -> dict[str, Any]:
        """获取使用统计"""
        return dict(self._stats)

    def generate_usage_report(self) -> str:
        """生成使用报告"""
        lines = []
        lines.append("=== 使用情况报告 ===\n")

        lines.append("【来源使用统计】")
        for source, count in sorted(
            self._stats["source_usage"].items(), key=lambda x: x[1], reverse=True
        ):
            lines.append(f"  {source}: {count} 次")

        lines.append("\n【细粒度类型使用统计】")
        for subtype, count in sorted(
            self._stats["subtype_usage"].items(), key=lambda x: x[1], reverse=True
        ):
            lines.append(f"  {subtype}: {count} 次")

        lines.append("\n【自定义类型使用统计】")
        for custom_type, count in sorted(
            self._stats["custom_type_usage"].items(), key=lambda x: x[1], reverse=True
        ):
            lines.append(f"  {custom_type}: {count} 次")

        lines.append("\n【字段使用统计】")
        for field, count in sorted(
            self._stats["field_usage"].items(), key=lambda x: x[1], reverse=True
        ):
            lines.append(f"  {field}: {count} 次")

        return "\n".join(lines)


class QualityReportGenerator:
    """
    质量报告生成器

    生成质量报告和改进建议
    """

    def __init__(
        self,
        quality_assessor: MetadataQualityAssessor,
        lifecycle_manager: CustomTypeLifecycleManager,
        usage_monitor: UsageMonitor,
    ):
        """
        初始化报告生成器

        Args:
            quality_assessor: 质量评估器
            lifecycle_manager: 生命周期管理器
            usage_monitor: 使用监控器
        """
        self._quality_assessor = quality_assessor
        self._lifecycle_manager = lifecycle_manager
        self._usage_monitor = usage_monitor

    def generate_quality_report(self, blocks: list[ContextBlock]) -> str:
        """
        生成质量报告

        Args:
            blocks: 上下文块列表

        Returns:
            质量报告字符串
        """
        lines = []
        lines.append("=== Metadata 质量报告 ===\n")

        if not blocks:
            lines.append("无上下文块")
            return "\n".join(lines)

        total_score = 0
        low_quality_blocks = []

        for i, block in enumerate(blocks, 1):
            custom_types_registry = self._lifecycle_manager.get_all_types()
            assessment = self._quality_assessor.assess_quality(
                block.metadata, block.source, custom_types_registry
            )

            total_score += assessment.score

            if assessment.score < 70:
                low_quality_blocks.append((i, block.source.value, assessment))

            lines.append(f"【块 {i}】来源: {block.source.value}")
            lines.append(f"  总分: {assessment.score}")
            lines.append(f"  完整性: {assessment.completeness_score}")
            lines.append(f"  准确性: {assessment.accuracy_score}")
            lines.append(f"  一致性: {assessment.consistency_score}")
            lines.append(f"  实用性: {assessment.usability_score}")

            if assessment.issues:
                lines.append("  问题:")
                for issue in assessment.issues:
                    lines.append(f"    - {issue}")

            if assessment.recommendations:
                lines.append("  建议:")
                for rec in assessment.recommendations:
                    lines.append(f"    - {rec}")

            lines.append("")

        # 平均分数
        avg_score = total_score / len(blocks) if blocks else 0
        lines.append(f"\n=== 总结 ===")
        lines.append(f"总块数: {len(blocks)}")
        lines.append(f"平均得分: {avg_score:.2f}")
        lines.append(f"低质量块数: {len(low_quality_blocks)}")

        return "\n".join(lines)

    def generate_type_usage_report(self) -> str:
        """生成类型使用报告"""
        lines = []
        lines.append("=== 自定义类型使用报告 ===\n")

        all_types = self._lifecycle_manager.get_all_types()

        if not all_types:
            lines.append("无已注册的自定义类型")
            return "\n".join(lines)

        for custom_type, type_info in all_types.items():
            stats = self._lifecycle_manager.get_type_stats(custom_type)
            usage_count = stats["count"] if stats else 0

            lines.append(f"【{custom_type}】")
            lines.append(f"  优先级: {type_info.get('priority', 'unknown')}")
            lines.append(f"  描述: {type_info.get('description', 'N/A')}")
            lines.append(f"  创建者: {type_info.get('creator', 'unknown')}")
            lines.append(f"  创建时间: {type_info.get('created_at', 'unknown')}")
            lines.append(f"  使用次数: {usage_count}")

            if type_info.get("deprecated", False):
                lines.append(f"  状态: 已废弃")
                lines.append(f"  废弃原因: {type_info.get('deprecated_reason', 'N/A')}")
            else:
                lines.append(f"  状态: 活跃")

            lines.append("")

        return "\n".join(lines)

    def generate_recommendations(self) -> str:
        """生成改进建议"""
        lines = []
        lines.append("=== 改进建议 ===\n")

        usage_stats = self._usage_monitor.get_usage_stats()

        # 检查未使用的自定义类型
        custom_types = self._lifecycle_manager.get_all_types()
        unused_types = []
        for custom_type, type_info in custom_types.items():
            stats = self._lifecycle_manager.get_type_stats(custom_type)
            if not stats or stats["count"] == 0:
                if not type_info.get("deprecated", False):
                    unused_types.append(custom_type)

        if unused_types:
            lines.append("【未使用的自定义类型】")
            for custom_type in unused_types:
                lines.append(f"  - {custom_type} (建议考虑废弃或删除)")
            lines.append("")

        # 检查高频使用的字段
        field_usage = usage_stats.get("field_usage", {})
        if field_usage:
            lines.append("【高频使用的 metadata 字段】")
            for field, count in sorted(field_usage.items(), key=lambda x: x[1], reverse=True)[:5]:
                lines.append(f"  - {field}: {count} 次")
            lines.append("")

        lines.append("【最佳实践建议】")
        lines.append("  1. 为 CUSTOM 来源始终提供 custom_type 字段")
        lines.append("  2. 添加 timestamp 字段以支持时间相关性分析")
        lines.append("  3. 使用 source_id 追踪数据来源")
        lines.append("  4. 定期清理未使用的自定义类型")
        lines.append("  5. 为高频使用的字段提供文档说明")

        return "\n".join(lines)


# ============================================================================
# Context Orchestrator
# ============================================================================


class ContextOrchestrator:
    """
    上下文编排器（总控层）

    职责：
    - 决定"该让模型看到什么"
    - 决定"按什么顺序看到"
    - 决定"保留什么、丢掉什么"
    - 决定"何时补充什么"

    协调模块：
    - ShortTermMemoryRedis（短期记忆）
    - LongTermMemoryManager（长期记忆）
    - TokenBudgetManager（Token 预算）
    - GlobalStateCapture（状态捕捉）
    - ChainReasoningEnhancer（推理增强）

    使用示例：
    ```python
    from scripts.redis_adapter import create_redis_adapter
    from scripts.context_orchestrator import ContextOrchestrator

    # 初始化
    redis_adapter = create_redis_adapter()
    orchestrator = ContextOrchestrator(
        redis_adapter=redis_adapter,
        user_id="user123",
        session_id="session456",
    )

    # 准备上下文
    context = orchestrator.prepare_context(
        user_input="帮我分析这段代码的性能问题",
        system_instruction="你是一个代码分析专家",
    )

    print(f"Token 数量: {context.token_count}")
    print(f"上下文内容:\\n{context.content}")
    ```
    """

    def __init__(
        self,
        redis_adapter: RedisAdapter,
        user_id: str,
        session_id: str,
        config: ContextConfig | None = None,
        token_budget_config: TokenBudgetConfig | None = None,
    ) -> None:
        """
        初始化上下文编排器

        Args:
            redis_adapter: Redis 适配器
            user_id: 用户 ID
            session_id: 会话 ID
            config: 编排配置
            token_budget_config: Token 预算配置
        """
        self._redis = redis_adapter
        self._user_id = user_id
        self._session_id = session_id
        self._config = config or ContextConfig()

        # 【新增】初始化优先级解析器
        self._priority_resolver = PriorityResolver()

        # 【阶段 5.1】初始化上下文压缩器（默认禁用）
        self._enable_context_compression = False
        self._context_compressor: ContextCompressor | None = None

        # 【阶段 4】初始化性能监控（默认禁用）
        self._enable_performance_monitoring = False
        self._performance_monitor: PerformanceMonitor | None = None

        # 【阶段 3】初始化质量评估与生命周期管理（默认禁用）
        self._enable_quality_assessment = False
        self._quality_assessor: MetadataQualityAssessor | None = None
        self._lifecycle_manager: CustomTypeLifecycleManager | None = None
        self._usage_monitor: UsageMonitor | None = None
        self._report_generator: QualityReportGenerator | None = None

        # 初始化子模块
        self._short_term = ShortTermMemoryRedis(
            redis_adapter=redis_adapter,
            user_id=user_id,
            config=ShortTermRedisConfig(
                max_items=self._config.max_short_term_items,
            ),
        )

        self._token_budget = TokenBudgetManager(
            redis_adapter=redis_adapter,
            session_id=session_id,
            config=token_budget_config or TokenBudgetConfig(
                total_budget=self._config.max_context_tokens,
                policy=BudgetPolicy.COMPRESS,
            ),
        )

        # 【新增】长期记忆管理器（可选）
        self._long_term: Any | None = None

        # 注册的内容提供者
        self._providers: dict[str, Callable[[], list[ContextBlock]]] = {}

    # -----------------------------------------------------------------------
    # 长期记忆绑定
    # -----------------------------------------------------------------------

    def bind_long_term(self, long_term: Any) -> None:
        """
        绑定长期记忆管理器

        Args:
            long_term: LongTermMemoryManager 实例
        """
        self._long_term = long_term

    # -----------------------------------------------------------------------
    # 提供者注册
    # -----------------------------------------------------------------------

    def register_provider(
        self,
        name: str,
        provider: Callable[[], list[ContextBlock]],
    ) -> None:
        """
        注册上下文提供者

        Args:
            name: 提供者名称
            provider: 提供者函数，返回 ContextBlock 列表
        """
        self._providers[name] = provider

    def unregister_provider(self, name: str) -> None:
        """注销上下文提供者"""
        self._providers.pop(name, None)

    # -----------------------------------------------------------------------
    # 核心方法：准备上下文
    # -----------------------------------------------------------------------

    def prepare_context(
        self,
        user_input: str,
        system_instruction: str | None = None,
        retrieval_results: list[str] | None = None,
        tool_results: list[str] | None = None,
        additional_blocks: list[ContextBlock] | None = None,
    ) -> PreparedContext:
        """
        准备完整上下文

        这是编排器的核心方法，执行以下步骤：
        1. 收集所有上下文块
        2. 计算 Token 预算
        3. 按优先级排序
        4. 应用压缩策略
        5. 组装最终上下文

        Args:
            user_input: 用户输入
            system_instruction: 系统指令
            retrieval_results: 检索结果列表
            tool_results: 工具返回列表
            additional_blocks: 额外的上下文块

        Returns:
            PreparedContext 准备好的上下文
        """
        # 开始会话
        self._token_budget.start_session()

        # 收集所有上下文块
        blocks: list[ContextBlock] = []

        # 1. 系统指令（最高优先级）
        if system_instruction:
            block = self._create_block(
                source=ContextSource.SYSTEM,
                priority=ContextPriority.CRITICAL,
                content=system_instruction,
            )
            blocks.append(block)
            self._token_budget.record_text(TokenType.SYSTEM, system_instruction)

        # 2. 用户输入
        block = self._create_block(
            source=ContextSource.USER_INPUT,
            priority=ContextPriority.CRITICAL,
            content=user_input,
        )
        blocks.append(block)
        self._token_budget.record_text(TokenType.USER_INPUT, user_input)

        # 3. 短期记忆
        short_term_blocks = self._collect_short_term_memory()
        blocks.extend(short_term_blocks)

        # 4. 检索结果
        if retrieval_results:
            retrieval_blocks = self._collect_retrieval_results(retrieval_results)
            blocks.extend(retrieval_blocks)

        # 5. 工具返回
        if tool_results:
            tool_blocks = self._collect_tool_results(tool_results)
            blocks.extend(tool_blocks)

        # 6. 注册的提供者
        for name, provider in self._providers.items():
            try:
                provider_blocks = provider()
                blocks.extend(provider_blocks)
            except Exception:
                pass

        # 7. 额外的上下文块
        if additional_blocks:
            blocks.extend(additional_blocks)

        # 应用预算和压缩
        final_blocks, warnings = self._apply_budget(blocks)

        # 组装最终上下文
        content, total_tokens = self._assemble_context(final_blocks)

        # 获取统计
        stats = self._token_budget.get_stats()

        return PreparedContext(
            content=content,
            token_count=total_tokens,
            blocks=final_blocks,
            stats=stats,
            warnings=warnings,
        )

    # -----------------------------------------------------------------------
    # 上下文收集
    # -----------------------------------------------------------------------

    def _create_block(
        self,
        source: ContextSource,
        priority: ContextPriority,
        content: str,
        relevance_score: float = 0.5,
        metadata: dict[str, Any] | None = None,
    ) -> ContextBlock:
        """
        创建上下文块

        【向后兼容】如果未提供 priority，则根据 metadata 自动解析
        """
        metadata = metadata or {}

        # 【向后兼容】如果未提供优先级，则根据 metadata 解析
        # 如果提供了优先级，则使用提供的优先级（旧代码兼容）
        if priority is None:
            resolved_priority, _ = self._priority_resolver.resolve(source, metadata)
        else:
            resolved_priority = priority

        token_count = self._token_budget.count(content)

        return ContextBlock(
            source=source,
            priority=resolved_priority,
            content=content,
            token_count=token_count,
            relevance_score=relevance_score,
            metadata=metadata,
        )

    # -----------------------------------------------------------------------
    # 自定义类型管理（混合方案）
    # -----------------------------------------------------------------------

    def register_custom_type(
        self,
        custom_type: str,
        priority: ContextPriority,
        required_fields: list[str] = None,
    ) -> None:
        """
        注册自定义类型

        Args:
            custom_type: 自定义类型名称（如 "workflow_step", "ui_component"）
            priority: 默认优先级
            required_fields: 必需字段列表

        示例:
            orchestrator.register_custom_type(
                "workflow_step",
                ContextPriority.HIGH,
                required_fields=["step_id", "status"]
            )
        """
        self._priority_resolver.register_custom_type(custom_type, priority, required_fields)

    def register_subtype_rule(
        self, subtype: str, priority: ContextPriority, weight: float = 1.0
    ) -> None:
        """
        注册 subtype 规则

        Args:
            subtype: 细粒度类型名称（如 "tool_prompt", "system_prompt"）
            priority: 优先级
            weight: 权重（0.0 - 1.0）

        示例:
            orchestrator.register_subtype_rule(
                "tool_prompt",
                ContextPriority.MEDIUM,
                weight=0.6
            )
        """
        self._priority_resolver.register_subtype_rule(subtype, priority, weight)

    def get_custom_types(self) -> dict[str, dict]:
        """获取所有已注册的自定义类型"""
        return self._priority_resolver.get_custom_types()

    def get_subtype_rules(self) -> dict[str, dict]:
        """获取所有 subtype 规则"""
        return self._priority_resolver.get_subtype_rules()

    def unregister_custom_type(self, custom_type: str) -> bool:
        """注销自定义类型"""
        return self._priority_resolver.unregister_custom_type(custom_type)

    def unregister_subtype_rule(self, subtype: str) -> bool:
        """注销 subtype 规则"""
        return self._priority_resolver.unregister_subtype_rule(subtype)

    def resolve_block_priority(
        self, block: ContextBlock
    ) -> tuple[ContextPriority, str]:
        """
        解析上下文块的优先级

        Args:
            block: 上下文块

        Returns:
            (优先级, 解析日志)
        """
        return self._priority_resolver.resolve(block.source, block.metadata)

    def debug_context_block(
        self, block: ContextBlock
    ) -> dict[str, Any]:
        """
        调试上下文块

        Args:
            block: 上下文块

        Returns:
            调试信息字典
        """
        priority, resolution_log = self.resolve_block_priority(block)
        validation_result = MetadataValidator.validate(block.metadata, block.source)

        return {
            "source": block.source.value,
            "priority": block.priority.value,
            "resolved_priority": priority.value,
            "metadata": block.metadata,
            "resolution_log": resolution_log,
            "validation": {
                "valid": validation_result.valid,
                "message": validation_result.message,
            },
            "token_count": block.token_count,
        }

    def _collect_short_term_memory(self) -> list[ContextBlock]:
        """收集短期记忆"""
        blocks: list[ContextBlock] = []

        # 获取热数据
        hot_items = self._short_term.get_hot_items(
            limit=self._config.max_short_term_items
        )

        for item in hot_items:
            # 根据桶类型确定优先级
            bucket_type = SemanticBucketType(item.bucket_type)
            priority = self._bucket_to_priority(bucket_type)

            block = self._create_block(
                source=ContextSource.SHORT_TERM_MEMORY,
                priority=priority,
                content=item.content,
                relevance_score=item.relevance_score,
                metadata={
                    "item_id": item.item_id,
                    "bucket_type": item.bucket_type,
                    "topic_label": item.topic_label,
                    "access_count": item.access_count,
                },
            )
            blocks.append(block)
            self._token_budget.record_text(TokenType.MEMORY, item.content)

        return blocks

    def _collect_retrieval_results(
        self,
        results: list[str],
    ) -> list[ContextBlock]:
        """收集检索结果"""
        blocks: list[ContextBlock] = []

        for i, result in enumerate(results[:self._config.max_retrieval_results]):
            block = self._create_block(
                source=ContextSource.RETRIEVAL,
                priority=ContextPriority.MEDIUM,
                content=result,
                relevance_score=1.0 - (i * 0.1),  # 按顺序降低相关性
                metadata={"index": i},
            )
            blocks.append(block)
            self._token_budget.record_text(TokenType.RETRIEVAL, result)

        return blocks

    def _collect_tool_results(
        self,
        results: list[str],
    ) -> list[ContextBlock]:
        """收集工具返回"""
        blocks: list[ContextBlock] = []

        for i, result in enumerate(results):
            # 工具结果可能很长，优先级较低
            block = self._create_block(
                source=ContextSource.TOOL_RESULT,
                priority=ContextPriority.LOW,
                content=result,
                relevance_score=0.5,
                metadata={"index": i},
            )
            blocks.append(block)
            self._token_budget.record_text(TokenType.TOOL_RESULT, result)

        return blocks

    def _bucket_to_priority(self, bucket_type: SemanticBucketType) -> ContextPriority:
        """语义桶类型映射到优先级"""
        mapping = {
            SemanticBucketType.USER_INTENT: ContextPriority.HIGH,
            SemanticBucketType.DECISION_CONTEXT: ContextPriority.HIGH,
            SemanticBucketType.TASK_CONTEXT: ContextPriority.MEDIUM,
            SemanticBucketType.KNOWLEDGE_GAP: ContextPriority.MEDIUM,
            SemanticBucketType.EMOTIONAL_TRACE: ContextPriority.LOW,
        }
        return mapping.get(bucket_type, ContextPriority.MEDIUM)

    # -----------------------------------------------------------------------
    # 预算管理
    # -----------------------------------------------------------------------

    def _apply_budget(
        self,
        blocks: list[ContextBlock],
    ) -> tuple[list[ContextBlock], list[str]]:
        """
        应用 Token 预算

        策略：
        1. 按优先级排序
        2. 计算总 Token
        3. 如果超预算，按优先级裁剪

        Args:
            blocks: 所有上下文块

        Returns:
            (最终上下文块列表, 警告列表)
        """
        warnings: list[str] = []

        # 按优先级排序
        priority_order = {
            ContextPriority.CRITICAL: 0,
            ContextPriority.HIGH: 1,
            ContextPriority.MEDIUM: 2,
            ContextPriority.LOW: 3,
            ContextPriority.OPTIONAL: 4,
        }

        sorted_blocks = sorted(
            blocks,
            key=lambda b: (
                priority_order.get(b.priority, 3),
                -b.relevance_score,  # 同优先级按相关性降序
            ),
        )

        # 计算预算
        total_tokens = sum(b.token_count for b in sorted_blocks)
        max_tokens = self._config.max_context_tokens

        if total_tokens <= max_tokens:
            return sorted_blocks, warnings

        # 超预算，需要裁剪
        warnings.append(
            f"上下文超预算: {total_tokens} > {max_tokens}，将裁剪低优先级内容"
        )

        final_blocks: list[ContextBlock] = []
        current_tokens = 0

        for block in sorted_blocks:
            if current_tokens + block.token_count <= max_tokens:
                final_blocks.append(block)
                current_tokens += block.token_count
            elif block.priority == ContextPriority.CRITICAL:
                # 关键内容必须包含，即使超预算
                final_blocks.append(block)
                current_tokens += block.token_count
                warnings.append(
                    f"关键内容 [{block.source.value}] 超预算但仍保留"
                )
            elif self._config.enable_auto_compression:
                # 尝试压缩
                compressed = self._compress_block(block, max_tokens - current_tokens)
                if compressed:
                    final_blocks.append(compressed)
                    current_tokens += compressed.token_count
                    warnings.append(
                        f"内容 [{block.source.value}] 已压缩"
                    )

        return final_blocks, warnings

    def _compress_block(
        self,
        block: ContextBlock,
        target_tokens: int,
    ) -> ContextBlock | None:
        """
        压缩上下文块

        Args:
            block: 原始上下文块
            target_tokens: 目标 Token 数

        Returns:
            压缩后的上下文块，无法压缩返回 None
        """
        if target_tokens <= 0:
            return None

        content = block.content

        # 简单截断策略
        if len(content) > target_tokens * 4:
            truncated = content[: target_tokens * 4]
            truncated += "\n...[内容已截断]..."

            return ContextBlock(
                source=block.source,
                priority=block.priority,
                content=truncated,
                token_count=target_tokens,
                relevance_score=block.relevance_score * 0.8,
                metadata={**block.metadata, "compressed": True},
            )

        return None

    # -----------------------------------------------------------------------
    # 上下文组装
    # -----------------------------------------------------------------------

    def _assemble_context(
        self,
        blocks: list[ContextBlock],
    ) -> tuple[str, int]:
        """
        组装最终上下文

        Args:
            blocks: 上下文块列表

        Returns:
            (完整上下文字符串, 总 Token 数)
        """
        sections: list[str] = []
        total_tokens = 0

        # 按来源分组
        by_source: dict[ContextSource, list[ContextBlock]] = {}
        for block in blocks:
            if block.source not in by_source:
                by_source[block.source] = []
            by_source[block.source].append(block)

        # 系统指令
        if ContextSource.SYSTEM in by_source:
            for block in by_source[ContextSource.SYSTEM]:
                sections.append(f"[系统指令]\n{block.content}\n")
                total_tokens += block.token_count

        # 短期记忆
        if ContextSource.SHORT_TERM_MEMORY in by_source:
            sections.append("[相关记忆]")
            for block in by_source[ContextSource.SHORT_TERM_MEMORY]:
                sections.append(f"- {block.content}")
                total_tokens += block.token_count
            sections.append("")

        # 检索结果
        if ContextSource.RETRIEVAL in by_source:
            sections.append("[检索结果]")
            for block in by_source[ContextSource.RETRIEVAL]:
                sections.append(f"- {block.content}")
                total_tokens += block.token_count
            sections.append("")

        # 工具返回
        if ContextSource.TOOL_RESULT in by_source:
            sections.append("[工具返回]")
            for block in by_source[ContextSource.TOOL_RESULT]:
                sections.append(f"{block.content}")
                total_tokens += block.token_count
            sections.append("")

        # 洞察
        if ContextSource.INSIGHT in by_source:
            sections.append("[系统建议]")
            for block in by_source[ContextSource.INSIGHT]:
                sections.append(f"- {block.content}")
                total_tokens += block.token_count
            sections.append("")

        # 用户输入
        if ContextSource.USER_INPUT in by_source:
            for block in by_source[ContextSource.USER_INPUT]:
                sections.append(f"[用户输入]\n{block.content}")
                total_tokens += block.token_count

        return "\n".join(sections), total_tokens

    # -----------------------------------------------------------------------
    # 便捷方法
    # -----------------------------------------------------------------------

    def get_short_term_memory(self) -> ShortTermMemoryRedis:
        """获取短期记忆管理器"""
        return self._short_term

    def get_token_budget(self) -> TokenBudgetManager:
        """获取 Token 预算管理器"""
        return self._token_budget

    def store_memory(
        self,
        content: str,
        bucket_type: SemanticBucketType,
        topic_label: str | None = None,
        relevance_score: float = 0.5,
    ) -> str:
        """
        存储到短期记忆（便捷方法）

        Args:
            content: 内容
            bucket_type: 语义桶类型
            topic_label: 话题标签
            relevance_score: 相关性分数

        Returns:
            记忆项 ID
        """
        return self._short_term.store(
            content=content,
            bucket_type=bucket_type,
            topic_label=topic_label,
            relevance_score=relevance_score,
        )

    def end_session(self) -> dict[str, Any]:
        """
        结束会话

        Returns:
            会话统计
        """
        return self._token_budget.end_session()

    # ========================================================================
    # 【新增】测试支持方法
    # ========================================================================

    def select_relevant_memories(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        智能选择相关记忆

        Args:
            query: 查询文本
            top_k: 返回数量

        Returns:
            相关记忆列表
        """
        # 从短期记忆检索
        stm_results = self._short_term.search(query, limit=top_k)

        # 转换为统一格式
        memories: list[dict[str, Any]] = []
        for item in stm_results:
            memories.append({
                "memory_id": item.item_id,
                "content": item.content,
                "bucket_type": item.bucket_type.value,
                "relevance_score": item.relevance_score,
                "source": "short_term",
            })

        return memories[:top_k]

    def get_hot_memories(
        self,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        """
        获取热数据（短期记忆中的高相关性记忆）

        Args:
            limit: 返回数量

        Returns:
            热数据列表
        """
        all_items: list[dict[str, Any]] = []

        # 从所有桶中获取高相关性记忆
        for bucket_type in [
            SemanticBucketType.TASK_CONTEXT,
            SemanticBucketType.DECISION_CONTEXT,
            SemanticBucketType.USER_INTENT,
        ]:
            bucket = self._short_term.get_bucket(bucket_type)
            if bucket:
                # bucket 可能是 dict 类型（来自 short_term_redis）
                if isinstance(bucket, dict):
                    items = bucket.get("items", [])
                else:
                    # bucket 是 SemanticBucket 类型（来自 short_term）
                    items = bucket.get_items(limit=limit)

                for item in items:
                    # 检查 relevance_score
                    relevance_score = getattr(item, 'relevance_score', 0)
                    if relevance_score >= 0.7:
                        all_items.append({
                            "memory_id": getattr(item, 'item_id', ''),
                            "content": getattr(item, 'content', ''),
                            "bucket_type": bucket_type.value,
                            "relevance_score": relevance_score,
                            "created_at": getattr(item, 'created_at', '').isoformat() if hasattr(getattr(item, 'created_at', None), 'isoformat') else None,
                            "source": "short_term",
                        })

        # 按相关性排序并返回
        all_items.sort(key=lambda x: x["relevance_score"], reverse=True)
        return all_items[:limit]

    def get_cold_memories(
        self,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        """
        获取冷数据（长期记忆）

        Args:
            limit: 返回数量

        Returns:
            冷数据列表
        """
        # 从长期记忆获取
        if self._long_term:
            # 获取各类长期记忆
            memories: list[dict[str, Any]] = []

            # 用户画像
            profile = self._long_term.get_user_profile()
            if profile:
                memories.append({
                    "memory_id": profile.profile_id if hasattr(profile, 'profile_id') else "user_profile",
                    "content": str(profile.identity if profile else ""),
                    "category": "user_profile",
                    "relevance_score": 0.6,
                    "source": "long_term",
                })

            # 程序性记忆
            procedural = self._long_term.get_procedural_memory()
            if procedural and procedural.decision_patterns:
                for pattern in procedural.decision_patterns[:limit]:
                    memories.append({
                        "memory_id": pattern.pattern_id,
                        "content": f"{pattern.scenario}: {pattern.decision}",
                        "category": "procedural",
                        "relevance_score": pattern.success_rate,
                        "source": "long_term",
                    })

            return memories[:limit]

        return []

    def get_used_tokens(self) -> int:
        """
        获取已使用的 Token 数

        Returns:
            已使用 Token 数
        """
        return self._token_budget.get_used_tokens()

    def get_remaining_tokens(self) -> int:
        """
        获取剩余 Token 数

        Returns:
            剩余 Token 数
        """
        return self._token_budget.get_remaining_tokens()

    # -----------------------------------------------------------------------
    # 【阶段 5.1】上下文压缩
    # -----------------------------------------------------------------------

    def enable_context_compression(
        self,
        enable_auto_compress: bool = False,
        auto_compress_threshold: float = 0.8,
        default_strategy: CompressionStrategy = CompressionStrategy.PRIORITY_BASED,
    ) -> None:
        """
        启用上下文压缩

        Args:
            enable_auto_compress: 是否启用自动压缩
            auto_compress_threshold: 自动压缩触发阈值
            default_strategy: 默认压缩策略
        """
        self._enable_context_compression = True
        self._context_compressor = ContextCompressor(
            enable_auto_compress=enable_auto_compress,
            auto_compress_threshold=auto_compress_threshold,
            default_strategy=default_strategy,
        )

    def disable_context_compression(self) -> None:
        """禁用上下文压缩"""
        self._enable_context_compression = False
        self._context_compressor = None

    def compress_context(
        self,
        blocks: list[ContextBlock],
        compression_ratio: float = 0.7,
        strategy: CompressionStrategy | None = None,
        min_blocks: int = 1,
        target_tokens: int | None = None,
    ) -> CompressionResult:
        """
        手动压缩上下文块（/compact 命令调用）

        Args:
            blocks: 上下文块列表
            compression_ratio: 压缩比率
            strategy: 压缩策略
            min_blocks: 最小保留块数
            target_tokens: 目标 token 数

        Returns:
            CompressionResult 压缩结果
        """
        if not self._enable_context_compression or not self._context_compressor:
            raise RuntimeError("上下文压缩未启用，请先调用 enable_context_compression()")

        return self._context_compressor.compress(
            blocks=blocks,
            compression_ratio=compression_ratio,
            strategy=strategy,
            min_blocks=min_blocks,
            target_tokens=target_tokens,
        )

    # -----------------------------------------------------------------------
    # 【阶段 4】性能监控与优化
    # -----------------------------------------------------------------------

    def enable_performance_monitoring(self) -> None:
        """启用性能监控"""
        self._enable_performance_monitoring = True
        self._performance_monitor = PerformanceMonitor()

    def disable_performance_monitoring(self) -> None:
        """禁用性能监控"""
        self._enable_performance_monitoring = False
        self._performance_monitor = None

    def get_performance_stats(self) -> dict[str, Any] | None:
        """获取性能统计"""
        if self._enable_performance_monitoring and self._performance_monitor:
            return self._performance_monitor.get_stats()
        return None

    def generate_performance_report(self) -> str | None:
        """生成性能报告"""
        if self._enable_performance_monitoring and self._performance_monitor:
            return self._performance_monitor.generate_report()
        return None

    def get_cache_stats(self) -> dict[str, Any]:
        """获取缓存统计"""
        return self._priority_resolver.get_cache_stats()

    def enable_lru_cache(self, cache_size: int = 1000) -> None:
        """
        启用 LRU 缓存

        Args:
            cache_size: 缓存大小
        """
        self._priority_resolver.enable_lru_cache(cache_size)

    def disable_lru_cache(self) -> None:
        """禁用 LRU 缓存"""
        self._priority_resolver.disable_lru_cache()

    def validate_metadata_batch(
        self, metadata_list: list[dict[str, Any]], source_list: list[ContextSource]
    ) -> list[ValidationResult]:
        """
        批量验证 metadata

        Args:
            metadata_list: metadata 列表
            source_list: source 列表

        Returns:
            验证结果列表
        """
        return BatchProcessor.validate_metadata_batch(metadata_list, source_list)

    # -----------------------------------------------------------------------
    # 【阶段 3】质量评估与生命周期管理
    # -----------------------------------------------------------------------

    def enable_quality_assessment(
        self,
        storage_path: str = "usage_stats.json",
        enable_monitoring: bool = False,
    ) -> None:
        """
        启用质量评估与生命周期管理

        Args:
            storage_path: 统计数据存储路径
            enable_monitoring: 是否启用使用监控（会影响性能）
        """
        self._enable_quality_assessment = True
        self._quality_assessor = MetadataQualityAssessor()
        self._lifecycle_manager = CustomTypeLifecycleManager(storage_path=storage_path)
        self._usage_monitor = UsageMonitor() if enable_monitoring else None
        self._report_generator = None  # 按需创建

    def disable_quality_assessment(self) -> None:
        """禁用质量评估与生命周期管理"""
        self._enable_quality_assessment = False
        self._quality_assessor = None
        self._lifecycle_manager = None
        self._usage_monitor = None
        self._report_generator = None

    def assess_metadata_quality(
        self, metadata: dict[str, Any], source: ContextSource
    ) -> QualityAssessment | None:
        """
        评估 metadata 质量

        Args:
            metadata: metadata 字典
            source: 上下文来源

        Returns:
            质量评估结果（如果未启用质量评估则返回 None）
        """
        if not self._enable_quality_assessment or not self._quality_assessor:
            return None

        custom_types_registry = (
            self._lifecycle_manager.get_all_types() if self._lifecycle_manager else {}
        )
        return self._quality_assessor.assess_quality(metadata, source, custom_types_registry)

    def register_custom_type_with_lifecycle(
        self,
        custom_type: str,
        priority: ContextPriority,
        required_fields: list[str] | None = None,
        description: str = "",
        creator: str = "unknown",
    ) -> None:
        """
        注册自定义类型（带生命周期管理）

        Args:
            custom_type: 自定义类型名称
            priority: 优先级
            required_fields: 必需字段列表
            description: 描述
            creator: 创建者
        """
        # 同时注册到优先级解析器和生命周期管理器
        self._priority_resolver.register_custom_type(custom_type, priority, required_fields)

        if self._enable_quality_assessment and self._lifecycle_manager:
            self._lifecycle_manager.register_type(
                custom_type, priority, required_fields, description, creator
            )

    def track_custom_type_usage(self, custom_type: str, usage_info: dict[str, Any] | None = None) -> None:
        """
        追踪自定义类型使用

        Args:
            custom_type: 自定义类型名称
            usage_info: 使用信息
        """
        if self._enable_quality_assessment and self._lifecycle_manager:
            self._lifecycle_manager.track_usage(custom_type, usage_info)

    def deprecate_custom_type(self, custom_type: str, reason: str = "") -> None:
        """
        废弃自定义类型

        Args:
            custom_type: 自定义类型名称
            reason: 废弃原因
        """
        if self._enable_quality_assessment and self._lifecycle_manager:
            self._lifecycle_manager.deprecate_type(custom_type, reason)

    def cleanup_unused_custom_types(self, threshold_days: int = 90) -> list[str]:
        """
        清理未使用的自定义类型

        Args:
            threshold_days: 阈值天数

        Returns:
            被清理的类型列表
        """
        if self._enable_quality_assessment and self._lifecycle_manager:
            return self._lifecycle_manager.cleanup_unused_types(threshold_days)
        return []

    def get_custom_type_stats(self, custom_type: str) -> dict[str, Any] | None:
        """
        获取自定义类型统计信息

        Args:
            custom_type: 自定义类型名称

        Returns:
            统计信息
        """
        if self._enable_quality_assessment and self._lifecycle_manager:
            return self._lifecycle_manager.get_type_stats(custom_type)
        return None

    def record_metadata_usage(
        self,
        source: ContextSource,
        subtype: str | None = None,
        custom_type: str | None = None,
        metadata_fields: list[str] | None = None,
    ) -> None:
        """
        记录 metadata 使用情况

        Args:
            source: 上下文来源
            subtype: 细粒度类型
            custom_type: 自定义类型
            metadata_fields: metadata 字段列表
        """
        if self._enable_quality_assessment and self._usage_monitor:
            self._usage_monitor.record_usage(source, subtype, custom_type, metadata_fields)

    def get_usage_stats(self) -> dict[str, Any] | None:
        """获取使用统计"""
        if self._enable_quality_assessment and self._usage_monitor:
            return self._usage_monitor.get_usage_stats()
        return None

    def generate_quality_report(self, blocks: list[ContextBlock]) -> str | None:
        """
        生成质量报告

        Args:
            blocks: 上下文块列表

        Returns:
            质量报告字符串（如果未启用质量评估则返回 None）
        """
        if not self._enable_quality_assessment:
            return None

        if not self._report_generator:
            if not self._quality_assessor or not self._lifecycle_manager:
                return None

            usage_monitor = self._usage_monitor or UsageMonitor()
            self._report_generator = QualityReportGenerator(
                self._quality_assessor, self._lifecycle_manager, usage_monitor
            )

        return self._report_generator.generate_quality_report(blocks)

    def generate_type_usage_report(self) -> str | None:
        """
        生成类型使用报告

        Returns:
            类型使用报告字符串（如果未启用质量评估则返回 None）
        """
        if not self._enable_quality_assessment or not self._report_generator:
            return None

        return self._report_generator.generate_type_usage_report()

    def generate_improvement_recommendations(self) -> str | None:
        """
        生成改进建议

        Returns:
            改进建议字符串（如果未启用质量评估则返回 None）
        """
        if not self._enable_quality_assessment or not self._report_generator:
            return None

        return self._report_generator.generate_recommendations()


# ============================================================================
# 工厂函数
# ============================================================================


def create_context_orchestrator(
    redis_host: str = "localhost",
    redis_port: int = 6379,
    user_id: str = "default_user",
    session_id: str = "default_session",
    max_context_tokens: int = 32000,
) -> ContextOrchestrator:
    """
    创建上下文编排器

    Args:
        redis_host: Redis 主机
        redis_port: Redis 端口
        user_id: 用户 ID
        session_id: 会话 ID
        max_context_tokens: 最大上下文 Token 数

    Returns:
        ContextOrchestrator 实例
    """
    redis_adapter = create_redis_adapter(host=redis_host, port=redis_port)
    config = ContextConfig(max_context_tokens=max_context_tokens)

    return ContextOrchestrator(
        redis_adapter=redis_adapter,
        user_id=user_id,
        session_id=session_id,
        config=config,
    )


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    "ContextPriority",
    "ContextSource",
    "ContextBlock",
    "ContextConfig",
    "PreparedContext",
    "ContextOrchestrator",
    "create_context_orchestrator",
    # 【阶段 5.1】上下文压缩
    "CompressionStrategy",
    "CompressionResult",
    "ContextCompressor",
    # Metadata 验证
    "MetadataValidator",
    "ValidationResult",
    # 优先级解析
    "PriorityResolver",
    # 【阶段 3】质量评估与生命周期管理
    "QualityAssessment",
    "MetadataQualityAssessor",
    "CustomTypeLifecycleManager",
    "UsageMonitor",
    "QualityReportGenerator",
    # 【阶段 4】性能优化
    "LRUCache",
    "PerformanceMonitor",
    "BatchProcessor",
]
