"""
GUI Agent 模块

提供基于多模态大模型的 GUI 自动化能力。
"""
from .base import BaseGUIAgent, GUIAgentResult, GUIAction, ActionType
from .factory import get_agent, create_agent_from_config, list_available_agents, register_agent


__all__ = [
    "BaseGUIAgent",
    "GUIAgentResult",
    "GUIAction",
    "ActionType",
    "get_agent",
    "create_agent_from_config",
    "list_available_agents",
    "register_agent",
]
