#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connectors 包入口：统一注册与工厂。"""
try:
    from .im_connector import BaseIMConnector
    from .dingtalk import DingTalkConnector
    from .wecom import WeComConnector
    from .feishu import FeishuConnector
except ImportError:  # 作为独立脚本直接运行时
    from im_connector import BaseIMConnector
    from dingtalk import DingTalkConnector
    from wecom import WeComConnector
    from feishu import FeishuConnector

_REGISTRY = {
    "dingtalk": DingTalkConnector,
    "wecom": WeComConnector,
    "feishu": FeishuConnector,
}


def get_connector(platform):
    """按平台名实例化连接器；platform ∈ {dingtalk, wecom, feishu}。"""
    cls = _REGISTRY.get(platform)
    if not cls:
        raise ValueError(f"未知 IM 平台：{platform}（可选 {list(_REGISTRY)}）")
    return cls()


def list_platforms():
    return list(_REGISTRY.keys())


__all__ = [
    "BaseIMConnector", "DingTalkConnector", "WeComConnector",
    "FeishuConnector", "get_connector", "list_platforms",
]
