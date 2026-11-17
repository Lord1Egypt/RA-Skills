"""VS Code CLI 适配器。

VS Code 的工作区打开、项目读取与任务下达统一走 `code` CLI；同时保留读取/运行
`.vscode/tasks.json` 的能力。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from adapters.generic.configured_cli_adapter import ConfiguredCliAdapter
from executor.base import ExecutionResult

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


class VscodeTasksAdapter(ConfiguredCliAdapter):
    name = "vscode"
    type = "cli"
    default_command = "code"

    # ── VS Code 特有：读取并运行 .vscode/tasks.json 任务 ──────────────────
    def list_tasks(self, ws: "WorkspaceConfig") -> list[dict]:
        tasks_path = Path(ws.path) / ".vscode" / "tasks.json"
        if not tasks_path.exists():
            return []
        # tasks.json 允许 JSONC 注释；做一次宽松解析
        text = tasks_path.read_text(encoding="utf-8")
        text = "\n".join(line for line in text.splitlines() if not line.strip().startswith("//"))
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return []
        return data.get("tasks", [])

    def run_task(self, ws: "WorkspaceConfig", label: str, timeout: int = 600) -> ExecutionResult:
        for task in self.list_tasks(ws):
            if task.get("label") == label and task.get("command"):
                cmd = task["command"]
                args = task.get("args") or []
                full = cmd if not args else cmd + " " + " ".join(args)
                return self._executor.execute(full, cwd=ws.path, timeout=timeout)
        return ExecutionResult(stderr=f"未在 .vscode/tasks.json 找到任务 '{label}'", exit_code=1)
