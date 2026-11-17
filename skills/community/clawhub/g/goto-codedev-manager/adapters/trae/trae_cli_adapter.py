"""Trae CLI 适配器。

通过 Trae CLI 直接读取项目数据并下达任务指令，避免人工 IDE 控制路径。
"""

from __future__ import annotations

from adapters.generic.configured_cli_adapter import ConfiguredCliAdapter


class TraeCliAdapter(ConfiguredCliAdapter):
    name = "trae"
    type = "cli"
    default_command = "trae"
    default_project_args = ["project", "read", "--workspace", "{repo_path}"]
    default_task_args = ["task", "run", "--workspace", "{repo_path}", "--prompt", "{prompt}"]
    default_open_args = ["open", "--workspace", "{repo_path}"]
