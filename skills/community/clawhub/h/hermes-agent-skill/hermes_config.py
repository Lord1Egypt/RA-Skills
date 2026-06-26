#!/usr/bin/env python3
"""
Hermes Agent - 全局配置
控制持久化开关和隐私相关行为
"""

import os
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HermesConfig:
    """
    Hermes 全局配置

    所有持久化相关行为通过此配置控制。
    配置来源优先级：环境变量 > 代码设置 > 默认值
    """
    # 洞察记忆持久化开关（默认关闭，需用户显式开启）
    persistence_enabled: bool = field(default_factory=lambda: _env_bool("HERMES_PERSISTENCE_ENABLED", False))

    # 洞察 DB 路径（仅在 persistence_enabled=True 时使用）
    insights_db_path: str = field(default_factory=lambda: _env_str("HERMES_INSIGHTS_DB", "~/.hermes/insights.db"))

    # 技能卡 DB 路径（仅在 persistence_enabled=True 时使用）
    skills_db_path: str = field(default_factory=lambda: _env_str("HERMES_SKILLS_DB", "~/.hermes/skills.db"))

    # 洞察提取开关（即使 persistence_enabled=True 也可以单独关闭提取）
    insight_extraction_enabled: bool = field(
        default_factory=lambda: _env_bool("HERMES_INSIGHT_EXTRACTION_ENABLED", True)
    )

    # 敏感内容过滤开关（自动过滤潜在敏感信息）
    sensitive_filter_enabled: bool = field(
        default_factory=lambda: _env_bool("HERMES_SENSITIVE_FILTER_ENABLED", True)
    )

    # sessions_send fallback 日志级别
    # "off": 完全禁用 fallback 日志
    # "summary": 仅记录 topic，不记录 payload
    # "full": 记录完整消息（仅推荐开发调试）
    session_fallback_log_level: str = field(
        default_factory=lambda: _env_str("HERMES_SESSION_LOG_LEVEL", "summary")
    )

    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def set_persistence(self, enabled: bool):
        """运行时设置是否启用持久化"""
        with self._lock:
            self.persistence_enabled = enabled

    def is_persistence_enabled(self) -> bool:
        return self.persistence_enabled

    def get_insights_db_path(self) -> str:
        return os.path.expanduser(self.insights_db_path)

    def get_skills_db_path(self) -> str:
        return os.path.expanduser(self.skills_db_path)


def _env_bool(key: str, default: bool) -> bool:
    val = os.environ.get(key, "").lower()
    if val in ("1", "true", "yes", "on"):
        return True
    if val in ("0", "false", "no", "off"):
        return False
    return default


def _env_str(key: str, default: str) -> str:
    return os.environ.get(key, default)


# === 全局配置实例 ===
hermes_config = HermesConfig()
