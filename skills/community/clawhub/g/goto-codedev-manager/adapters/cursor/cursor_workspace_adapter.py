"""Cursor CLI 适配器。

Cursor 的控制统一通过 CLI 完成；项目读取和任务下达参数由 adapters.yaml 配置。
"""

from __future__ import annotations

from adapters.generic.configured_cli_adapter import ConfiguredCliAdapter


class CursorWorkspaceAdapter(ConfiguredCliAdapter):
    name = "cursor"
    type = "cli"
    default_command = "cursor"
