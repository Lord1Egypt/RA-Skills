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
渐进式压缩器 - Progressive Compressor

实现多级渐进式压缩，根据重要性评分动态选择压缩级别。

压缩级别：
- Level 0: 原始内容（100% Token）
- Level 1: 摘要压缩（60% Token）
- Level 2: 关键点提取（30% Token）
- Level 3: 标签化（10% Token）

核心特性：
- 保留原始引用，支持回退
- 按需压缩，避免重复计算
- 支持多级回退
- 压缩质量可验证

使用场景：
1. Token 预算优化
2. 记忆筛选和清理
3. 上下文压缩

依赖：importance_scorer.py（用于重要性评分）
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from .importance_scorer import ImportanceScorer, ScoreBreakdown, WeightPresets


class CompressionLevel(Enum):
    """压缩级别"""
    ORIGINAL = 0  # 原始内容
    SUMMARY = 1   # 摘要压缩
    KEYPOINTS = 2 # 关键点提取
    TAGS = 3      # 标签化


@dataclass
class CompressedEntry:
    """压缩后的条目"""
    original_content: str  # 原始内容（用于回退）
    level: CompressionLevel  # 当前压缩级别
    compressed_content: str  # 压缩后的内容
    score: float  # 重要性得分
    metadata: Dict[str, Any] = field(default_factory=dict)
    compression_ratios: Dict[int, float] = field(default_factory=dict)  # 各级别的压缩比

    def upgrade(self, new_level: CompressionLevel, new_content: str) -> None:
        """升级压缩级别"""
        self.level = new_level
        self.compressed_content = new_content


class ProgressiveCompressor:
    """
    渐进式压缩器

    根据重要性评分动态选择压缩级别
    """

    def __init__(
        self,
        scorer: Optional[ImportanceScorer] = None,
        auto_compress: bool = True,
    ):
        """
        初始化压缩器

        参数：
            scorer: 重要性评分器（默认使用标准配置）
            auto_compress: 是否自动压缩（默认 True）
        """
        self.scorer = scorer or ImportanceScorer(weights=WeightPresets.STANDARD)
        self.auto_compress = auto_compress

        # 压缩缓存（避免重复压缩）
        self.compression_cache: Dict[str, CompressedEntry] = {}

        # 统计信息
        self.stats = {
            "total_compressions": 0,
            "level_0_count": 0,
            "level_1_count": 0,
            "level_2_count": 0,
            "level_3_count": 0,
            "average_token_saving": 0.0,
        }

    def compress_to_level_0(self, content: str, **kwargs) -> str:
        """
        Level 0: 原始内容

        不进行任何压缩，直接返回原始内容
        """
        return content

    def compress_to_level_1(self, content: str, **kwargs) -> str:
        """
        Level 1: 摘要压缩

        策略：
        1. 提取关键句子
        2. 去除冗余信息
        3. 保留核心结构

        目标 Token 使用：60%
        """
        # 简单实现：提取首尾段落 + 中间关键句
        sentences = content.split('。')

        if len(sentences) <= 2:
            return content

        # 保留首尾
        result = [sentences[0], sentences[-1]]

        # 中间提取关键句（每3句取1句）
        middle_sentences = sentences[1:-1]
        for i in range(0, len(middle_sentences), 3):
            if i < len(middle_sentences):
                result.append(middle_sentences[i])

        summary = '。'.join(result)
        if not summary.endswith('。'):
            summary += '。'

        return summary

    def compress_to_level_2(self, content: str, **kwargs) -> str:
        """
        Level 2: 关键点提取

        策略：
        1. 识别关键点（包含数字、引号、列表标记）
        2. 提取动作性语句
        3. 格式化为要点列表

        目标 Token 使用：30%
        """
        # 简单实现：提取包含关键标记的句子
        key_markers = ['需要', '必须', '应该', '重要', '关键', 'TODO', '!', '•', '-', '1.', '2.', '3.']

        sentences = content.split('。')
        keypoints = []

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # 检查是否包含关键标记
            if any(marker in sentence for marker in key_markers):
                keypoints.append(f"• {sentence}")

        # 如果没有提取到关键点，使用简单的句子截断
        if not keypoints and sentences:
            # 保留前30%的句子
            keep_count = max(1, len(sentences) // 3)
            keypoints = [f"• {sentences[i].strip()}" for i in range(keep_count)]

        result = '\n'.join(keypoints)
        return result if result else content[:len(content)//3]

    def compress_to_level_3(self, content: str, **kwargs) -> str:
        """
        Level 3: 标签化

        策略：
        1. 提取关键词和实体
        2. 生成简短标签
        3. 丢弃冗余描述

        目标 Token 使用：10%
        """
        # 简单实现：提取关键词
        import re

        # 移除标点符号
        clean_text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', content)

        # 提取词汇
        words = clean_text.split()

        # 过滤停用词（简化版）
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        keywords = [w for w in words if len(w) > 1 and w not in stop_words]

        # 取前10个关键词
        top_keywords = keywords[:10]

        # 生成标签
        tags = ', '.join(top_keywords)

        return f"[Tags: {tags}]"

    def compress(
        self,
        content: str,
        target_level: Optional[CompressionLevel] = None,
        query_context: str = "",
        **kwargs
    ) -> CompressedEntry:
        """
        压缩内容

        参数：
            content: 原始内容
            target_level: 目标压缩级别（如果为 None，根据重要性自动选择）
            query_context: 查询上下文（用于重要性评分）

        返回：
            压缩条目对象
        """
        # 计算重要性得分
        score_breakdown = self.scorer.score(
            content=content,
            query_context=query_context,
            **kwargs
        )
        score = score_breakdown.final_score

        # 确定压缩级别
        if target_level is None:
            target_level = CompressionLevel(score_breakdown.get_compression_level())

        # 检查缓存
        cache_key = f"{hash(content)}_{target_level.value}"
        if cache_key in self.compression_cache:
            return self.compression_cache[cache_key]

        # 执行压缩
        if target_level == CompressionLevel.ORIGINAL:
            compressed = self.compress_to_level_0(content, **kwargs)
        elif target_level == CompressionLevel.SUMMARY:
            compressed = self.compress_to_level_1(content, **kwargs)
        elif target_level == CompressionLevel.KEYPOINTS:
            compressed = self.compress_to_level_2(content, **kwargs)
        elif target_level == CompressionLevel.TAGS:
            compressed = self.compress_to_level_3(content, **kwargs)
        else:
            compressed = content

        # 计算压缩比
        original_length = len(content)
        compressed_length = len(compressed)
        compression_ratio = compressed_length / original_length if original_length > 0 else 1.0

        # 创建压缩条目
        entry = CompressedEntry(
            original_content=content,
            level=target_level,
            compressed_content=compressed,
            score=score,
            metadata={
                "query_context": query_context,
                "score_breakdown": score_breakdown.model_dump(),
            },
            compression_ratios={
                target_level.value: compression_ratio,
            },
        )

        # 缓存
        self.compression_cache[cache_key] = entry

        # 更新统计
        self.stats["total_compressions"] += 1
        self.stats[f"level_{target_level.value}_count"] += 1

        # 更新平均 Token 节省
        token_saving = (1 - compression_ratio) * 100
        total_compressions = self.stats["total_compressions"]
        current_avg = self.stats["average_token_saving"]
        self.stats["average_token_saving"] = (
            (current_avg * (total_compressions - 1) + token_saving) / total_compressions
        )

        return entry

    def compress_batch(
        self,
        contents: List[str],
        query_context: str = "",
        target_level: Optional[CompressionLevel] = None,
    ) -> List[CompressedEntry]:
        """
        批量压缩

        参数：
            contents: 内容列表
            query_context: 查询上下文
            target_level: 目标压缩级别（如果为 None，根据重要性自动选择）

        返回：
            压缩条目列表
        """
        return [
            self.compress(content, target_level, query_context)
            for content in contents
        ]

    def upgrade(
        self,
        entry: CompressedEntry,
        new_level: CompressionLevel,
    ) -> CompressedEntry:
        """
        升级压缩级别

        参数：
            entry: 原始压缩条目
            new_level: 新的压缩级别

        返回：
            升级后的压缩条目
        """
        if new_level == entry.level:
            return entry

        # 使用原始内容重新压缩
        new_compressed = self.compress(
            content=entry.original_content,
            target_level=new_level,
            query_context=entry.metadata.get("query_context", ""),
        )

        # 保留原有的压缩比记录
        new_compressed.compression_ratios = entry.compression_ratios.copy()
        new_compressed.compression_ratios[new_level.value] = (
            len(new_compressed.compressed_content) / len(entry.original_content)
        )

        return new_compressed

    def downgrade(
        self,
        entry: CompressedEntry,
        new_level: CompressionLevel,
    ) -> CompressedEntry:
        """
        降级压缩级别

        注意：这是"降级"到更低级别（更高压缩比），不是"回退"到原始内容

        参数：
            entry: 原始压缩条目
            new_level: 新的压缩级别（应该比当前级别数字更大）

        返回：
            降级后的压缩条目
        """
        if new_level < entry.level:
            # 如果要提升级别，使用 upgrade
            return self.upgrade(entry, new_level)

        # 直接使用原始内容压缩到新级别
        return self.compress(
            content=entry.original_content,
            target_level=new_level,
            query_context=entry.metadata.get("query_context", ""),
        )

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "cache_size": len(self.compression_cache),
            "cache_entries": list(self.compression_cache.keys())[:10],  # 前10个缓存键
        }


class TokenBudgetManager:
    """
    Token 预算管理器

    管理整体 Token 预算，与渐进式压缩器配合使用
    """

    def __init__(
        self,
        total_budget: int = 10000,
        buffer_ratio: float = 0.1,  # 10% 缓冲
        compressor: Optional[ProgressiveCompressor] = None,
    ):
        """
        初始化预算管理器

        参数：
            total_budget: 总 Token 预算
            buffer_ratio: 缓冲比例
            compressor: 压缩器（默认创建新的）
        """
        self.total_budget = total_budget
        self.buffer_ratio = buffer_ratio
        self.available_budget = total_budget * (1 - buffer_ratio)
        self.used_budget = 0

        self.compressor = compressor or ProgressiveCompressor()

        # 记录已压缩的内容
        self.compressed_entries: List[CompressedEntry] = []

    def add_content(
        self,
        content: str,
        query_context: str = "",
        force_level: Optional[CompressionLevel] = None,
    ) -> CompressedEntry:
        """
        添加内容，自动压缩以适应预算

        参数：
            content: 原始内容
            query_context: 查询上下文
            force_level: 强制使用指定压缩级别

        返回：
            压缩条目
        """
        # 尝试压缩
        entry = self.compressor.compress(
            content=content,
            target_level=force_level,
            query_context=query_context,
        )

        # 检查预算
        content_tokens = len(entry.compressed_content)

        if self.used_budget + content_tokens > self.available_budget:
            # 超预算，需要降级
            print(f"警告：超预算，当前已用 {self.used_budget}/{self.available_budget}")

            # 尝试降级所有条目
            while self.used_budget + content_tokens > self.available_budget:
                # 找到当前级别最低的条目，降级它
                highest_level_entry = max(
                    self.compressed_entries,
                    key=lambda e: e.level.value,
                    default=None,
                )

                if highest_level_entry and highest_level_entry.level.value < 3:
                    # 降级
                    old_level = highest_level_entry.level
                    new_level = CompressionLevel(highest_level_entry.level.value + 1)
                    upgraded = self.compressor.downgrade(highest_level_entry, new_level)

                    # 更新预算
                    old_tokens = len(highest_level_entry.compressed_content)
                    new_tokens = len(upgraded.compressed_content)
                    self.used_budget -= (old_tokens - new_tokens)

                    # 替换条目
                    idx = self.compressed_entries.index(highest_level_entry)
                    self.compressed_entries[idx] = upgraded
                    print(f"降级条目: Level {old_level.value} → {new_level.value}")
                else:
                    # 无法再降级，放弃添加
                    print(f"无法添加内容，预算不足")
                    return entry

        # 添加到列表
        self.compressed_entries.append(entry)
        self.used_budget += content_tokens

        return entry

    def get_compressed_context(self) -> str:
        """
        获取压缩后的上下文（用于发送给模型）
        """
        # 按重要性排序
        sorted_entries = sorted(
            self.compressed_entries,
            key=lambda e: e.score,
            reverse=True,
        )

        # 拼接内容
        context_parts = []
        for entry in sorted_entries:
            context_parts.append(entry.compressed_content)

        return '\n\n'.join(context_parts)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_budget": self.total_budget,
            "available_budget": self.available_budget,
            "used_budget": self.used_budget,
            "usage_ratio": self.used_budget / self.available_budget if self.available_budget > 0 else 0,
            "entry_count": len(self.compressed_entries),
            "average_tokens_per_entry": (
                self.used_budget / len(self.compressed_entries)
                if self.compressed_entries else 0
            ),
            "compressor_stats": self.compressor.get_stats(),
        }


# 使用示例
if __name__ == "__main__":
    print("=== 渐进式压缩器示例 ===")

    # 创建压缩器
    compressor = ProgressiveCompressor()

    # 示例内容
    content = """
    用户注册功能开发需要包含以下几个关键步骤：
    1. 设计注册表单，包括用户名、密码、邮箱等字段
    2. 实现表单验证，确保用户输入的数据格式正确
    3. 将用户数据存储到数据库，密码需要进行加密处理
    4. 发送验证邮件，确认用户邮箱的有效性
    5. 实现登录功能，验证用户身份
    6. 添加记住密码功能，提升用户体验

    在开发过程中需要注意以下要点：
    - 安全性：密码必须使用 BCrypt 或 Argon2 等强加密算法
    - 可用性：表单验证要给出清晰的错误提示
    - 性能：数据库查询要优化，避免慢查询
    """

    # 不同级别的压缩
    print("\n=== Level 0: 原始内容 ===")
    level_0 = compressor.compress_to_level_0(content)
    print(f"长度: {len(level_0)}")
    print(level_0[:200] + "..." if len(level_0) > 200 else level_0)

    print("\n=== Level 1: 摘要压缩 ===")
    level_1 = compressor.compress_to_level_1(content)
    print(f"长度: {len(level_1)} (压缩比: {len(level_1)/len(level_0)*100:.1f}%)")
    print(level_1)

    print("\n=== Level 2: 关键点提取 ===")
    level_2 = compressor.compress_to_level_2(content)
    print(f"长度: {len(level_2)} (压缩比: {len(level_2)/len(level_0)*100:.1f}%)")
    print(level_2)

    print("\n=== Level 3: 标签化 ===")
    level_3 = compressor.compress_to_level_3(content)
    print(f"长度: {len(level_3)} (压缩比: {len(level_3)/len(level_0)*100:.1f}%)")
    print(level_3)

    # 自动压缩
    print("\n=== 自动压缩（根据重要性） ===")
    entry = compressor.compress(content, query_context="用户注册功能")
    print(f"重要性得分: {entry.score:.3f}")
    print(f"压缩级别: {entry.level.name}")
    print(f"压缩后内容: {entry.compressed_content[:200]}...")

    # Token 预算管理
    print("\n=== Token 预算管理示例 ===")
    budget_manager = TokenBudgetManager(total_budget=1000)

    # 添加多个内容
    contents = [
        "用户登录功能需要实现密码验证和会话管理",
        "数据库设计需要考虑数据的一致性和完整性",
        "API 接口需要实现认证和授权机制",
        "前端页面需要响应式设计，适配不同设备",
        "系统需要实现日志记录和错误处理",
        "性能优化需要使用缓存和异步处理",
    ]

    for i, content in enumerate(contents, 1):
        entry = budget_manager.add_content(content, query_context="系统开发")
        print(f"\n添加内容 {i}:")
        print(f"  原始长度: {len(content)}")
        print(f"  压缩级别: {entry.level.name}")
        print(f"  压缩后长度: {len(entry.compressed_content)}")
        print(f"  当前预算使用: {budget_manager.used_budget}/{budget_manager.available_budget}")

    # 统计信息
    print("\n=== 统计信息 ===")
    print(f"压缩器统计: {compressor.get_stats()}")
    print(f"预算管理器统计: {budget_manager.get_stats()}")
