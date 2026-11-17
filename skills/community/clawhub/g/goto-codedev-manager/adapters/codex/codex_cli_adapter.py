"""Codex CLI 适配器（priority 1）。

通过 `codex exec`（非交互模式）在工作区下达开发任务，回收输出。代码改动落在工作区，
由 core/ 通过 Git Diff 识别，不依赖 Codex 的内部状态。
"""

from __future__ import annotations

import shutil
import uuid
from typing import TYPE_CHECKING

from adapters.base import CodingAgentAdapter, TaskHandle

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


class CodexCliAdapter(CodingAgentAdapter):
    name = "codex"
    type = "cli"

    @property
    def command(self) -> str:
        return self._config.get("command") or "codex"

    def is_available(self) -> bool:
        return shutil.which(self.command) is not None

    def assign_coding_task(self, ws: "WorkspaceConfig", prompt: str, timeout: int = 1800) -> TaskHandle:
        handle_id = f"codex-{uuid.uuid4().hex[:8]}"
        # codex exec：非交互执行一次性任务；--full-auto 允许其在工作区内自动读写文件
        result = self._executor.execute(
            [self.command, "exec", "--full-auto", prompt],
            cwd=ws.repo_path,
            timeout=timeout,
        )
        return TaskHandle(
            id=handle_id,
            agent=self.name,
            status="completed" if result.succeeded else "failed",
            output=result.stdout,
            error=result.stderr,
        )
