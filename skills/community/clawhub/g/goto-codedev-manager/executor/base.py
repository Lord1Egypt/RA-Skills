"""执行器抽象基类与统一执行结果（与 goto-cloudserver-manager 同结构）。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    duration: float = 0.0

    @property
    def succeeded(self) -> bool:
        return self.exit_code == 0

    def __bool__(self) -> bool:
        return self.succeeded


class ExecutorBase(ABC):
    """所有执行器的统一接口。"""

    @abstractmethod
    def execute(self, command: str, cwd: str | None = None, timeout: int = 120) -> ExecutionResult:
        """执行命令，返回 stdout / stderr / exit_code。"""
