"""通用 CLI 编程 Agent 适配器。

用于接入任意「命令 + prompt」形态的命令行编程 Agent，命令从 adapters.yaml 的
generic_cli.command 读取。调用约定：`<command> <prompt>` 在工作区目录执行。
"""

from __future__ import annotations

import shutil
import uuid
from typing import TYPE_CHECKING

from adapters.base import CodingAgentAdapter, TaskHandle

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


class CliAgentAdapter(CodingAgentAdapter):
    name = "generic_cli"
    type = "cli"

    @property
    def command(self) -> str:
        return self._config.get("command") or ""

    def is_available(self) -> bool:
        return bool(self.command) and shutil.which(self.command) is not None

    def assign_coding_task(self, ws: "WorkspaceConfig", prompt: str, timeout: int = 1800) -> TaskHandle:
        if not self.command:
            return TaskHandle(
                id=f"generic-{uuid.uuid4().hex[:8]}", agent=self.name, status="failed",
                error="adapters.yaml 未配置 generic_cli.command",
            )
        result = self._executor.execute([self.command, prompt], cwd=ws.repo_path, timeout=timeout)
        return TaskHandle(
            id=f"generic-{uuid.uuid4().hex[:8]}",
            agent=self.name,
            status="completed" if result.succeeded else "failed",
            output=result.stdout,
            error=result.stderr,
        )
