"""Qoder CLI 适配器。

Qoder 的控制统一通过 CLI 完成；项目读取和任务下达参数由 adapters.yaml 配置。
"""

from __future__ import annotations

from adapters.generic.configured_cli_adapter import ConfiguredCliAdapter


class QoderWorkspaceAdapter(ConfiguredCliAdapter):
    name = "qoder"
    type = "cli"
    default_command = "qoder"
