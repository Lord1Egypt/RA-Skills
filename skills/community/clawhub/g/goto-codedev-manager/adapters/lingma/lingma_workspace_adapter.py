"""Lingma 兼容入口。

Lingma IDE 已升级为 QoerCN，因此保留 `lingma` adapter key 作为向后兼容别名，
实际通过 Qoer CLI 读取项目数据并下达任务指令。
"""

from __future__ import annotations

from adapters.qoer.qoer_cli_adapter import QoerCliAdapter


class LingmaWorkspaceAdapter(QoerCliAdapter):
    name = "lingma"
    type = "cli"
