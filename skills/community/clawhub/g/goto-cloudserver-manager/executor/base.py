"""执行器抽象基类，统一 SSH / WinRM / 云助手 / 本地执行的接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.config_loader import ServerConfig


@dataclass
class ExecutionResult:
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0

    @property
    def succeeded(self) -> bool:
        return self.exit_code == 0

    def __bool__(self) -> bool:
        return self.succeeded


class ExecutorBase(ABC):
    """所有执行器的统一接口。"""

    @abstractmethod
    def connect(self, server: "ServerConfig") -> None:
        """建立连接，server 包含 host / credentials。"""

    @abstractmethod
    def execute(self, command: str, timeout: int = 60) -> ExecutionResult:
        """执行命令，返回 stdout / stderr / exit_code。"""

    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """上传本地文件到远端路径。"""

    @abstractmethod
    def close(self) -> None:
        """关闭连接，释放资源。"""

    def execute_sql(self, db_type: str, sql: str, timeout: int = 60) -> ExecutionResult:
        """执行 SQL 语句（通过命令行工具）。子类可重写以提供原生 SQL 支持。"""
        if db_type == "sqlserver":
            escaped = sql.replace('"', '\\"').replace("'", "\\'")
            cmd = f'sqlcmd -S localhost -E -Q "{escaped}"'
        elif db_type == "mysql":
            escaped = sql.replace('"', '\\"')
            cmd = f'mysql -u root -e "{escaped}"'
        elif db_type == "postgresql":
            cmd = f"psql -U postgres -c \"{sql.replace(chr(34), chr(92) + chr(34))}\""
        elif db_type == "redis":
            cmd = f"redis-cli {sql}"
        else:
            cmd = sql
        return self.execute(cmd, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
