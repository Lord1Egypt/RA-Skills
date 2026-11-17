"""Claude Code CLI 适配器（priority 2）。

通过 `claude -p`（print / 非交互模式）在工作区下达开发任务。
"""

from __future__ import annotations

import shutil
import uuid
from typing import TYPE_CHECKING

from adapters.base import CodingAgentAdapter, TaskHandle

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


class ClaudeCliAdapter(CodingAgentAdapter):
    name = "claude_code"
    type = "cli"

    @property
    def command(self) -> str:
        return self._config.get("command") or "claude"

    def is_available(self) -> bool:
        return shutil.which(self.command) is not None

    def assign_coding_task(self, ws: "WorkspaceConfig", prompt: str, timeout: int = 1800) -> TaskHandle:
        handle_id = f"claude-{uuid.uuid4().hex[:8]}"
        # -p 非交互；--permission-mode acceptEdits 允许其在工作区内落盘修改
        result = self._executor.execute(
            [self.command, "-p", prompt, "--permission-mode", "acceptEdits"],
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
