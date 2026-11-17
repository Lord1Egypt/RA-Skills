"""
nvidia-llm — 英伟达大模型智能路由 Skill
========================================
作者: 用户
版本: 1.1.0

核心: AutoRouter — 自动路由 + 熔断保护 + 延迟优化 + 自动降级
新增: 订阅授权 + VIP + 微信支付 + 邀请奖励
"""

from .core import (
    AutoRouter, LLM, CircuitBreaker,
    chat, stream, pick, models, search, status,
    subscription_status, subscribe, activate, invite, my_invite_code,
    MODELS, REASONING_MODELS, FALLBACK_CHAINS,
)

__version__ = "1.1.0"
__author__ = "用户"

__all__ = [
    "AutoRouter", "LLM", "CircuitBreaker",
    "chat", "stream", "pick", "models", "search", "status",
    "subscription_status", "subscribe", "activate", "invite", "my_invite_code",
    "MODELS", "REASONING_MODELS", "FALLBACK_CHAINS",
]