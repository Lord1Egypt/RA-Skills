#!/usr/bin/env python3
"""
ecosystem/registry.py — 适配器注册表（v1.0.0）

按生态名解析适配器；支持 env `INFOSEEK_ECOSYSTEM` 指定默认生态。
"""

from __future__ import annotations

import os
import sys
from typing import Dict, Optional, Type

from .base import EcosystemAdapter


def _ensure_pkg_root_on_path() -> None:
    """把 ecosystem 的父目录（技能根）加入 sys.path，保证包导入自包含。"""
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)


def _load_adapters() -> Dict[str, Type[EcosystemAdapter]]:
    """懒加载全部内置适配器（每个适配器文件独立、薄、零重依赖）。"""
    _ensure_pkg_root_on_path()
    registry: Dict[str, Type[EcosystemAdapter]] = {}
    adapter_names = [
        'workbuddy', 'ima', 'claude', 'codex', 'dify', 'coze', 'generic_mcp',
        'agentkey',   # P1b: AgentKey 统一 MCP 网关（L1 网关付费层）
    ]
    for mod_name in adapter_names:
        try:
            module = __import__(
                f'ecosystem.adapters.{mod_name}', fromlist=[mod_name])
            for attr in dir(module):
                obj = getattr(module, attr)
                if (isinstance(obj, type) and issubclass(obj, EcosystemAdapter)
                        and obj is not EcosystemAdapter and getattr(obj, 'name', None)):
                    registry[obj.name] = obj
        except Exception as e:  # 单个适配器失败不阻塞整体
            print(f"[ecosystem][warn] 适配器 {mod_name} 加载失败: {e}")
    return registry


REGISTRY: Dict[str, Type[EcosystemAdapter]] = _load_adapters()


def get_adapter(name: str) -> Optional[EcosystemAdapter]:
    """按生态名实例化适配器；未知生态返回 None。"""
    cls = REGISTRY.get(name)
    return cls() if cls else None


def resolve(name: Optional[str] = None) -> EcosystemAdapter:
    """解析适配器：显式 name > env INFOSEEK_ECOSYSTEM > workbuddy 兜底。"""
    target = name or os.environ.get('INFOSEEK_ECOSYSTEM') or 'workbuddy'
    adapter = get_adapter(target)
    if adapter is None:
        raise KeyError(
            f"未知生态 '{target}'。可用: {list(REGISTRY.keys())} "
            f"（或用 env INFOSEEK_ECOSYSTEM 指定）")
    return adapter


def list_adapters() -> list:
    """列出全部已注册适配器（含五件差异摘要）。"""
    return [
        {
            'name': name,
            'display_name': cls.display_name,
            'trigger': cls.trigger_spec(cls()),
            'collection': cls.collection_spec(cls()),
        }
        for name, cls in sorted(REGISTRY.items())
    ]
