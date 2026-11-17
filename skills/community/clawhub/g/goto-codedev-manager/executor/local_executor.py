"""本地执行器：用 subprocess 在本机执行 git / dotnet / codex / claude / code / npm 等命令。"""

from __future__ import annotations

import shlex
import subprocess
import time

import structlog

from executor.base import ExecutionResult, ExecutorBase

logger = structlog.get_logger(__name__)


class LocalExecutor(ExecutorBase):
    """在本机工作区目录下执行命令。

    所有编程 Agent 适配器与技术栈适配器都通过它 shell-out，便于在测试中统一 mock。
    """

    def __init__(self, shell: bool = False) -> None:
        # 默认 shell=False：命令以参数列表执行，避免注入；需要管道/重定向时由调用方显式开 shell。
        self._shell = shell

    def execute(
        self, command: str | list[str], cwd: str | None = None, timeout: int = 120
    ) -> ExecutionResult:
        """command 可为字符串（按需 shlex 切分）或参数列表（原样传入，适合含空格/引号的 prompt）。"""
        logger.debug("local_execute", command=str(command)[:120], cwd=cwd)
        if isinstance(command, list):
            args: str | list[str] = command
        else:
            args = command if self._shell else shlex.split(command, posix=False)
        start = time.monotonic()
        try:
            result = subprocess.run(
                args,
                shell=self._shell,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding="utf-8",
                errors="replace",
            )
            return ExecutionResult(
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                exit_code=result.returncode,
                duration=time.monotonic() - start,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(stderr=f"命令超时（{timeout}s）", exit_code=-1, duration=time.monotonic() - start)
        except FileNotFoundError as e:
            return ExecutionResult(stderr=f"命令不存在：{e}", exit_code=127, duration=time.monotonic() - start)
        except Exception as e:  # noqa: BLE001
            return ExecutionResult(stderr=str(e), exit_code=-1, duration=time.monotonic() - start)
