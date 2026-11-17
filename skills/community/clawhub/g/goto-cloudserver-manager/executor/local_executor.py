"""本地执行器：使用 subprocess 在本机执行命令（用于测试和本地调试）。"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import structlog

from executor.base import ExecutionResult, ExecutorBase

if TYPE_CHECKING:
    from core.config_loader import ServerConfig

logger = structlog.get_logger(__name__)


class LocalExecutor(ExecutorBase):
    def __init__(self, shell: bool = True) -> None:
        self._shell = shell

    def connect(self, server: "ServerConfig") -> None:
        logger.info("local_executor_connected", server=server.id)

    def execute(self, command: str, timeout: int = 60) -> ExecutionResult:
        logger.debug("local_execute", command=command[:80])
        try:
            result = subprocess.run(
                command,
                shell=self._shell,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding="utf-8",
                errors="replace",
            )
            return ExecutionResult(
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(stderr=f"命令超时（{timeout}s）", exit_code=-1)
        except Exception as e:
            return ExecutionResult(stderr=str(e), exit_code=-1)

    def upload_file(self, local_path: str, remote_path: str) -> bool:
        shutil.copy2(local_path, remote_path)
        return True

    def close(self) -> None:
        pass
