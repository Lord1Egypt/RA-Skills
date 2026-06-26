"""
GUI Agent 工厂

根据配置创建对应的 GUI Agent 实例。
"""
from typing import Dict, Any, Optional, Type
from .base import BaseGUIAgent
from .aliyun import AliyunGUIAgent


_agent_registry: Dict[str, Type[BaseGUIAgent]] = {
    "aliyun": AliyunGUIAgent,
    "gui-plus": AliyunGUIAgent,
    "gui-plus-2026-02-26": AliyunGUIAgent,
}


def register_agent(name: str, agent_class: Type[BaseGUIAgent]):
    _agent_registry[name.lower()] = agent_class


def get_agent(name: str = "aliyun", **kwargs) -> BaseGUIAgent:
    name_lower = name.lower()
    if name_lower not in _agent_registry:
        raise ValueError(f"未知的 Agent: {name}，可用: {list(_agent_registry.keys())}")
    
    agent_class = _agent_registry[name_lower]
    return agent_class(**kwargs)


def list_available_agents() -> list:
    return list(_agent_registry.keys())


def create_agent_from_config(config: Dict[str, Any]) -> BaseGUIAgent:
    provider = config.get("provider", "aliyun")
    agent_config = {k: v for k, v in config.items() if k != "provider"}
    return get_agent(provider, **agent_config)
