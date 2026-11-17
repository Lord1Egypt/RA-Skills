"""实体提取协调器：选定技术栈适配器，从变更文件解析实体（Agent 无关）。

本模块刻意保持薄——真正的解析逻辑在 stacks/<stack>/ 里。这样新增技术栈时，
变更识别与建表判定逻辑都不用改。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from executor.local_executor import LocalExecutor
from stacks.base import EntityDef
from stacks.registry import resolve_stack

if TYPE_CHECKING:
    from core.config_loader import ConfigLoader, WorkspaceConfig


def extract_entities(
    ws: "WorkspaceConfig",
    config: "ConfigLoader",
    files: list[str],
    executor: LocalExecutor | None = None,
) -> list[EntityDef]:
    adapter = resolve_stack(ws, config, executor)
    return adapter.extract_entities(ws, files)
