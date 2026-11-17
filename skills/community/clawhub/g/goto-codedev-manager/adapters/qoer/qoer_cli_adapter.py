"""QoerCN CLI 适配器。

Lingma IDE 已升级为 QoerCN，本适配器通过 Qoer CLI 读取项目数据并下达任务指令。
"""

from __future__ import annotations

from adapters.generic.configured_cli_adapter import ConfiguredCliAdapter


class QoerCliAdapter(ConfiguredCliAdapter):
    name = "qoer"
    type = "cli"
    default_command = "qoer"
    default_project_args = ["project", "read", "--workspace", "{repo_path}"]
    default_task_args = ["task", "run", "--workspace", "{repo_path}", "--prompt", "{prompt}"]
    default_open_args = ["open", "--workspace", "{repo_path}"]
