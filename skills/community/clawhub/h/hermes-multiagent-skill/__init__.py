"""
Hermes 协议 - 多智能体高并发调度
突触式通信，毫秒级分发，精准对齐
"""
from .hermes import hermes, HermesRouter, HermesMessage, OpenClawHermes, HermesAgent, HermesSynapse
from .hermes_sessions_integration import hermes_sessions, HermesSessionsIntegration, HermesSubAgent

__all__ = [
    "hermes",
    "HermesRouter",
    "HermesMessage",
    "HermesAgent",
    "HermesSynapse",
    "OpenClawHermes",
    "hermes_sessions",
    "HermesSessionsIntegration",
    "HermesSubAgent",
]
