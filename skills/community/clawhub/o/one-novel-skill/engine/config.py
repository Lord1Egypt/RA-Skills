#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py — 统一配置参数

将 pipeline.py 和 orchestrator.py 中的所有硬编码值抽取至此。
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PipelineConfig:
    """管线配置参数"""

    # A/B 风格触发条件
    ab_style_chapters: List[int] = field(default_factory=lambda: [1, 2, 3, 10, 20, 50, 100])
    ab_style_mod: int = 50  # 每 N 章触发

    # L3 三段变体生成
    l3_enabled: bool = True
    l3_env_var: str = "NOVEL_L3"

    # 批处理超时
    batch_timeout_env: str = "NOVEL_BATCH_TIMEOUT"
    default_batch_timeout: int = 0  # 0 = 无限制

    # 深度审查触发条件
    deep_review_yellow_min_issues: int = 3
    deep_review_red_min_issues: int = 3

    # 伏笔密度阈值
    foreshadow_high_density: float = 8.0  # 每千字
    foreshadow_low_density: float = 0.5

    # 稳定性检查
    char_disappear_threshold: int = 30  # 消失多少章标记异常
    emotion_streak_threshold: int = 5  # 连续多少章同一情绪标记

    # 反思机制
    reflection_enabled: bool = True

    # 分形叙事校验
    fractal_chapter_threshold: int = 400  # 开篇超过此字数提醒


@dataclass
class ErrorMessages:
    """统一错误消息"""
    NO_PROVIDER = "没有可用的 LLM provider"
    EMPTY_GENERATION = "生成空文本"
    PERSISTENCE_FAIL = "持久化失败"
    TRANSACTION_FAIL = "事务提交失败"


# 全局实例
DEFAULT_CONFIG = PipelineConfig()
ERROR_MSG = ErrorMessages()
