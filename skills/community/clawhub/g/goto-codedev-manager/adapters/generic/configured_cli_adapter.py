"""配置驱动的 IDE CLI 适配器。

用于接入 QoerCN、Trae、Cursor、Qoder、VS Code 等 IDE CLI。每个 IDE 的真实命令
可能随版本变化，因此命令参数由 adapters.yaml 配置，代码只负责统一执行协议。
"""

from __future__ import annotations

import shlex
import shutil
import uuid
from typing import TYPE_CHECKING, Any

from adapters.base import CodingAgentAdapter, ProjectContext, TaskHandle

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig
    from executor.base import ExecutorBase


class ConfiguredCliAdapter(CodingAgentAdapter):
    name = "configured_cli"
    type = "cli"

    default_command = ""
    default_project_args: list[str] = ["project", "read", "--workspace", "{repo_path}"]
    default_task_args: list[str] = [
        "task",
        "run",
        "--workspace",
        "{repo_path}",
        "--prompt",
        "{prompt}",
    ]
    default_open_args: list[str] = ["open", "--workspace", "{repo_path}"]

    def __init__(
        self,
        config: dict | None = None,
        executor: "ExecutorBase | None" = None,
        adapter_name: str | None = None,
    ) -> None:
        super().__init__(config=config, executor=executor)
        if adapter_name:
            self.name = adapter_name

    @property
    def command(self) -> str:
        return self._config.get("command") or self.default_command or self.name

    def is_available(self) -> bool:
        return bool(self.command) and shutil.which(self.command) is not None

    def open_workspace(self, ws: "WorkspaceConfig") -> None:
        args = self._args("open_args", ws)
        if args:
            self._executor.execute([self.command, *args], cwd=ws.repo_path, timeout=self._timeout("read_timeout", 60))

    def read_project_context(self, ws: "WorkspaceConfig") -> ProjectContext:
        ctx = super().read_project_context(ws)
        args = self._args("project_args", ws)
        if not args:
            return ctx
        result = self._executor.execute(
            [self.command, *args],
            cwd=ws.repo_path,
            timeout=self._timeout("read_timeout", 60),
        )
        ctx.summary = result.stdout.strip() if result.succeeded else result.stderr.strip()
        return ctx

    def assign_coding_task(self, ws: "WorkspaceConfig", prompt: str, timeout: int = 1800) -> TaskHandle:
        args = self._args("task_args", ws, prompt=prompt)
        if not args:
            return TaskHandle(
                id=f"{self.name}-{uuid.uuid4().hex[:8]}",
                agent=self.name,
                status="failed",
                error=f"adapters.yaml 未配置 {self.name}.task_args，无法下达任务指令",
            )
        result = self._executor.execute([self.command, *args], cwd=ws.repo_path, timeout=timeout)
        return TaskHandle(
            id=f"{self.name}-{uuid.uuid4().hex[:8]}",
            agent=self.name,
            status="completed" if result.succeeded else "failed",
            output=result.stdout,
            error=result.stderr,
        )

    def _timeout(self, key: str, default: int) -> int:
        try:
            return int(self._config.get(key, default))
        except (TypeError, ValueError):
            return default

    def _args(self, key: str, ws: "WorkspaceConfig", prompt: str = "") -> list[str]:
        raw = self._config.get(key)
        if raw is None:
            raw = getattr(self, f"default_{key}", [])
        return self._format_args(raw, ws, prompt)

    def _format_args(self, raw: Any, ws: "WorkspaceConfig", prompt: str) -> list[str]:
        values = {
            "prompt": prompt,
            "workspace": ws.path,
            "repo_path": ws.repo_path,
            "workspace_id": ws.id,
            "workspace_name": ws.name,
            "stack": ws.stack,
        }
        if isinstance(raw, str):
            return shlex.split(raw.format(**values), posix=False)
        if isinstance(raw, list):
            return [str(arg).format(**values) for arg in raw]
        return []
