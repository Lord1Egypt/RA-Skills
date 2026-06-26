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
重要性评分器 - Importance Scorer

用于对记忆条目进行重要性评分，支持多维度的加权评分模型。

关键特性：
- 多维度评分：相关性、新鲜度、完整性、可操作性
- 可配置权重：不同场景下权重可调整
- 动态调整：支持基于反馈的权重优化

评分模型：
Score = Relevance × Weight1 + Freshness × Weight2 + Completeness × Weight3 + Actionability × Weight4

典型使用场景：
1. 渐进式压缩：根据评分决定压缩级别
2. 记忆筛选：过滤低重要性记忆
3. Token预算分配：优先保留高重要性记忆

评分标准：
- 高分（>0.8）：必须保留，完整内容
- 中分（0.5-0.8）：压缩后保留，摘要或关键点
- 低分（<0.5）：可丢弃，仅保留标签
"""

import math
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class ScoreWeights(BaseModel):
    """
    评分权重配置

    各维度权重之和应为 1.0
    """
    relevance: float = Field(default=0.4, ge=0, le=1, description="相关性权重")
    freshness: float = Field(default=0.3, ge=0, le=1, description="新鲜度权重")
    completeness: float = Field(default=0.2, ge=0, le=1, description="完整性权重")
    actionability: float = Field(default=0.1, ge=0, le=1, description="可操作性权重")

    def validate_sum(self) -> bool:
        """验证权重总和是否为1.0（允许小误差）"""
        total = self.relevance + self.freshness + self.completeness + self.actionability
        return abs(total - 1.0) < 0.01


class ScoreBreakdown(BaseModel):
    """
    评分明细

    展示各维度的得分和权重
    """
    relevance_score: float = Field(ge=0, le=1, description="相关性得分")
    freshness_score: float = Field(ge=0, le=1, description="新鲜度得分")
    completeness_score: float = Field(ge=0, le=1, description="完整性得分")
    actionability_score: float = Field(ge=0, le=1, description="可操作性得分")

    final_score: float = Field(ge=0, le=1, description="最终综合得分")
    weights: ScoreWeights = Field(description="使用的权重配置")

    def get_compression_level(self) -> int:
        """
        根据得分确定压缩级别

        返回：
            0: 原始内容（高分 > 0.8）
            1: 摘要压缩（中分 0.5-0.8）
            2: 关键点提取（低分 < 0.5）
            3: 标签化（极低分 < 0.3）
        """
        if self.final_score > 0.8:
            return 0
        elif self.final_score > 0.5:
            return 1
        elif self.final_score > 0.3:
            return 2
        else:
            return 3


class ImportanceScorer:
    """
    重要性评分器

    对记忆条目进行多维度的加权评分
    """

    def __init__(
        self,
        weights: Optional[ScoreWeights] = None,
        freshness_window_days: int = 7,
        current_time: Optional[datetime] = None,
    ):
        """
        初始化评分器

        参数：
            weights: 评分权重配置（默认使用标准权重）
            freshness_window_days: 新鲜度计算的时间窗口（天）
            current_time: 当前时间（用于测试）
        """
        self.weights = weights or ScoreWeights()
        self.freshness_window_days = freshness_window_days
        self.current_time = current_time or datetime.now()

        # 验证权重总和
        if not self.weights.validate_sum():
            raise ValueError("权重总和必须为 1.0")

    def score_relevance(
        self,
        content: str,
        query_context: str,
        keywords: Optional[List[str]] = None,
    ) -> float:
        """
        评分相关性

        考虑因素：
        1. 内容与查询上下文的匹配度
        2. 关键词出现频率
        3. 语义相似度（简化版：基于关键词重叠）

        参数：
            content: 记忆内容
            query_context: 查询上下文
            keywords: 关键词列表

        返回：
            相关性得分（0-1）
        """
        if not content or not query_context:
            return 0.0

        content_lower = content.lower()
        query_lower = query_context.lower()

        # 计算关键词重叠度
        if keywords:
            keyword_matches = sum(1 for kw in keywords if kw.lower() in content_lower)
            keyword_score = min(keyword_matches / len(keywords), 1.0) if keywords else 0.0
        else:
            # 使用查询词作为关键词
            query_words = query_lower.split()
            keyword_matches = sum(1 for word in query_words if word in content_lower)
            keyword_score = min(keyword_matches / len(query_words), 1.0) if query_words else 0.0

        # 计算文本重叠度
        content_words = set(content_lower.split())
        query_words = set(query_lower.split())
        overlap = len(content_words & query_words)
        text_score = overlap / len(query_words) if query_words else 0.0

        # 综合得分（关键词权重更高）
        relevance_score = keyword_score * 0.7 + text_score * 0.3

        return relevance_score

    def score_freshness(
        self,
        timestamp: datetime,
        decay_rate: float = 0.1,
    ) -> float:
        """
        评分新鲜度

        使用指数衰减模型：
        Freshness = e^(-decay_rate × days_since_creation)

        参数：
            timestamp: 创建时间
            decay_rate: 衰减率（默认 0.1）

        返回：
            新鲜度得分（0-1）
        """
        if not timestamp:
            return 0.0

        days_since = (self.current_time - timestamp).total_seconds() / 86400

        # 使用指数衰减
        freshness_score = math.exp(-decay_rate * days_since)

        # 限制在时间窗口内
        if days_since > self.freshness_window_days:
            freshness_score *= 0.5  # 超出窗口后减半

        return min(freshness_score, 1.0)

    def score_completeness(
        self,
        content: str,
        has_metadata: bool = False,
        has_context: bool = False,
    ) -> float:
        """
        评分完整性

        考虑因素：
        1. 内容长度（太短不完整）
        2. 是否包含元数据
        3. 是否包含上下文信息

        参数：
            content: 记忆内容
            has_metadata: 是否有元数据
            has_context: 是否有上下文

        返回：
            完整性得分（0-1）
        """
        if not content:
            return 0.0

        # 内容长度评分（假设合理长度为 50-500 字符）
        length = len(content)
        if length < 20:
            length_score = 0.3
        elif length < 50:
            length_score = 0.6
        elif length <= 500:
            length_score = 1.0
        else:
            length_score = 0.8  # 太长可能冗余

        # 元数据评分
        metadata_score = 0.2 if has_metadata else 0.0

        # 上下文评分
        context_score = 0.2 if has_context else 0.0

        # 综合得分
        completeness_score = (
            length_score * 0.6 +
            metadata_score * 0.2 +
            context_score * 0.2
        )

        return completeness_score

    def score_actionability(
        self,
        content: str,
        action_keywords: Optional[List[str]] = None,
    ) -> float:
        """
        评分可操作性

        考虑因素：
        1. 是否包含动作动词
        2. 是否包含明确的操作指令
        3. 是否包含可执行的建议

        参数：
            content: 记忆内容
            action_keywords: 动作关键词列表

        返回：
            可操作性得分（0-1）
        """
        if not content:
            return 0.0

        content_lower = content.lower()

        # 默认动作关键词
        default_keywords = [
            "应该", "需要", "必须", "建议", "要求",
            "执行", "实施", "完成", "实现", "处理",
            "should", "need", "must", "suggest", "require",
            "execute", "implement", "complete", "achieve", "handle"
        ]
        keywords = action_keywords or default_keywords

        # 检查动作关键词出现
        action_matches = sum(1 for kw in keywords if kw.lower() in content_lower)
        action_score = min(action_matches / len(keywords), 1.0) if keywords else 0.0

        # 检查是否包含具体指令（包含数字或具体步骤）
        has_instructions = any(
            char.isdigit() for char in content
        ) or any(
            word in content_lower for word in ["步骤", "step", "1.", "2.", "第一", "second"]
        )
        instruction_score = 0.3 if has_instructions else 0.0

        # 综合得分
        actionability_score = action_score * 0.7 + instruction_score * 0.3

        return actionability_score

    def score(
        self,
        content: str,
        query_context: str = "",
        timestamp: Optional[datetime] = None,
        has_metadata: bool = False,
        has_context: bool = False,
        keywords: Optional[List[str]] = None,
    ) -> ScoreBreakdown:
        """
        综合评分

        参数：
            content: 记忆内容
            query_context: 查询上下文
            timestamp: 创建时间
            has_metadata: 是否有元数据
            has_context: 是否有上下文
            keywords: 关键词列表

        返回：
            评分明细对象
        """
        # 计算各维度得分
        relevance_score = self.score_relevance(content, query_context, keywords)
        freshness_score = self.score_freshness(timestamp or self.current_time)
        completeness_score = self.score_completeness(content, has_metadata, has_context)
        actionability_score = self.score_actionability(content, keywords)

        # 计算加权总分
        final_score = (
            relevance_score * self.weights.relevance +
            freshness_score * self.weights.freshness +
            completeness_score * self.weights.completeness +
            actionability_score * self.weights.actionability
        )

        # 创建评分明细
        breakdown = ScoreBreakdown(
            relevance_score=relevance_score,
            freshness_score=freshness_score,
            completeness_score=completeness_score,
            actionability_score=actionability_score,
            final_score=final_score,
            weights=self.weights,
        )

        return breakdown

    def score_batch(
        self,
        items: List[Dict[str, Any]],
        query_context: str = "",
    ) -> List[ScoreBreakdown]:
        """
        批量评分

        参数：
            items: 记忆条目列表，每个条目包含必要字段
            query_context: 查询上下文

        返回：
            评分明细列表
        """
        results = []
        for item in items:
            breakdown = self.score(
                content=item.get("content", ""),
                query_context=query_context,
                timestamp=item.get("timestamp"),
                has_metadata=item.get("has_metadata", False),
                has_context=item.get("has_context", False),
                keywords=item.get("keywords"),
            )
            results.append(breakdown)

        return results

    def adjust_weights(
        self,
        feedback_data: List[Dict[str, Any]],
        learning_rate: float = 0.1,
    ) -> ScoreWeights:
        """
        基于反馈调整权重

        使用简单的梯度下降策略调整权重

        参数：
            feedback_data: 反馈数据列表，每项包含：
                - content: 内容
                - query_context: 查询上下文
                - expected_score: 期望得分
            learning_rate: 学习率

        返回：
            调整后的权重配置
        """
        # 简化的权重调整逻辑
        # 实际应用中可能需要更复杂的优化算法

        adjustment_factors = {
            "relevance": 0.0,
            "freshness": 0.0,
            "completeness": 0.0,
            "actionability": 0.0,
        }

        for feedback in feedback_data:
            # 计算当前得分
            breakdown = self.score(
                content=feedback["content"],
                query_context=feedback["query_context"],
                timestamp=feedback.get("timestamp"),
                has_metadata=feedback.get("has_metadata", False),
                has_context=feedback.get("has_context", False),
            )

            # 计算误差
            error = feedback["expected_score"] - breakdown.final_score

            # 调整各维度权重（根据该维度的贡献）
            adjustment_factors["relevance"] += error * breakdown.relevance_score
            adjustment_factors["freshness"] += error * breakdown.freshness_score
            adjustment_factors["completeness"] += error * breakdown.completeness_score
            adjustment_factors["actionability"] += error * breakdown.actionability_score

        # 应用调整
        new_weights = ScoreWeights(
            relevance=max(0.1, min(0.7, self.weights.relevance + learning_rate * adjustment_factors["relevance"])),
            freshness=max(0.1, min(0.7, self.weights.freshness + learning_rate * adjustment_factors["freshness"])),
            completeness=max(0.1, min(0.7, self.weights.completeness + learning_rate * adjustment_factors["completeness"])),
            actionability=max(0.1, min(0.7, self.weights.actionability + learning_rate * adjustment_factors["actionability"])),
        )

        # 归一化权重
        total = new_weights.relevance + new_weights.freshness + new_weights.completeness + new_weights.actionability
        new_weights = ScoreWeights(
            relevance=new_weights.relevance / total,
            freshness=new_weights.freshness / total,
            completeness=new_weights.completeness / total,
            actionability=new_weights.actionability / total,
        )

        self.weights = new_weights
        return new_weights


# 预定义权重配置
class WeightPresets:
    """预定义的权重配置"""

    STANDARD = ScoreWeights(relevance=0.4, freshness=0.3, completeness=0.2, actionability=0.1)
    """标准配置：平衡所有维度"""

    FRESHNESS_FOCUSED = ScoreWeights(relevance=0.3, freshness=0.5, completeness=0.1, actionability=0.1)
    """新鲜度优先：适用于实时任务"""

    ACTION_FOCUSED = ScoreWeights(relevance=0.2, freshness=0.2, completeness=0.2, actionability=0.4)
    """可操作优先：适用于任务执行"""

    QUALITY_FOCUSED = ScoreWeights(relevance=0.3, freshness=0.2, completeness=0.4, actionability=0.1)
    """质量优先：适用于知识管理"""


# 使用示例
if __name__ == "__main__":
    # 示例1：基本使用
    print("=== 示例1：基本评分 ===")
    scorer = ImportanceScorer(weights=WeightPresets.STANDARD)

    content = "需要完成用户注册功能，包括表单验证和数据库存储"
    breakdown = scorer.score(
        content=content,
        query_context="用户注册功能开发",
        timestamp=datetime.now() - timedelta(days=1),
        has_metadata=True,
        has_context=True,
        keywords=["注册", "表单", "数据库"],
    )

    print(f"内容: {content}")
    print(f"相关性得分: {breakdown.relevance_score:.3f}")
    print(f"新鲜度得分: {breakdown.freshness_score:.3f}")
    print(f"完整性得分: {breakdown.completeness_score:.3f}")
    print(f"可操作性得分: {breakdown.actionability_score:.3f}")
    print(f"最终得分: {breakdown.final_score:.3f}")
    print(f"压缩级别: {breakdown.get_compression_level()}")

    # 示例2：批量评分
    print("\n=== 示例2：批量评分 ===")
    items = [
        {
            "content": "用户登录模块需要添加记住密码功能",
            "timestamp": datetime.now() - timedelta(days=1),
            "has_metadata": True,
            "has_context": True,
        },
        {
            "content": "系统架构设计文档",
            "timestamp": datetime.now() - timedelta(days=30),
            "has_metadata": True,
            "has_context": True,
        },
        {
            "content": "TODO: 修复登录bug",
            "timestamp": datetime.now() - timedelta(hours=2),
            "has_metadata": False,
            "has_context": False,
        },
    ]

    results = scorer.score_batch(items, query_context="系统开发")

    for i, (item, breakdown) in enumerate(zip(items, results)):
        print(f"\n条目 {i+1}:")
        print(f"  内容: {item['content'][:50]}...")
        print(f"  得分: {breakdown.final_score:.3f}")
        print(f"  压缩级别: {breakdown.get_compression_level()}")

    # 示例3：权重调整
    print("\n=== 示例3：权重调整 ===")
    print(f"原始权重: {scorer.weights}")

    feedback_data = [
        {
            "content": "完成API接口开发",
            "query_context": "API开发",
            "expected_score": 0.9,
        },
        {
            "content": "系统架构文档",
            "query_context": "API开发",
            "expected_score": 0.4,
        },
    ]

    new_weights = scorer.adjust_weights(feedback_data, learning_rate=0.2)
    print(f"调整后权重: {new_weights}")

    # 示例4：不同权重配置对比
    print("\n=== 示例4：不同权重配置对比 ===")
    test_content = "需要实现用户权限管理功能，包括角色分配和权限验证"
    test_query = "权限管理系统"

    for preset_name, weights in [
        ("标准配置", WeightPresets.STANDARD),
        ("新鲜度优先", WeightPresets.FRESHNESS_FOCUSED),
        ("可操作优先", WeightPresets.ACTION_FOCUSED),
        ("质量优先", WeightPresets.QUALITY_FOCUSED),
    ]:
        scorer = ImportanceScorer(weights=weights)
        breakdown = scorer.score(content=test_content, query_context=test_query)
        print(f"{preset_name}: 得分={breakdown.final_score:.3f}, 级别={breakdown.get_compression_level()}")
