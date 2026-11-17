"""WinRM 执行器：通过 pywinrm 在 Windows Server 上执行 PowerShell / Bat 命令。"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import winrm
import structlog

from executor.base import ExecutionResult, ExecutorBase

if TYPE_CHECKING:
    from core.config_loader import ServerConfig

logger = structlog.get_logger(__name__)


class WinRMExecutor(ExecutorBase):
    def __init__(
        self,
        username: str = "Administrator",
        password: str = "",
        port: int = 5986,
        use_ssl: bool = True,
    ) -> None:
        self._username = username
        self._password = password
        self._port = port
        self._use_ssl = use_ssl
        self._protocol: str = "https" if use_ssl else "http"
        self._session: winrm.Session | None = None
        self._host: str = ""

    def connect(self, server: "ServerConfig") -> None:
        # 同 SSHExecutor：优先使用 public_ip，OpenClaw 通常运行在云外部，无法依赖内网 IP 连通
        host = getattr(server, "public_ip", "") or getattr(server, "private_ip", "")
        self._host = host
        transport = "ssl" if self._use_ssl else "ntlm"
        self._session = winrm.Session(
            target=f"{self._protocol}://{host}:{self._port}/wsman",
            auth=(self._username, self._password),
            transport=transport,
            server_cert_validation="ignore",  # 自签名证书时忽略
        )
        logger.info("winrm_connected", host=host, port=self._port, ssl=self._use_ssl)

    def execute(self, command: str, timeout: int = 60) -> ExecutionResult:
        if not self._session:
            raise RuntimeError("WinRM 连接未建立，请先调用 connect()")
        logger.debug("winrm_execute", host=self._host, command=command[:80])
        # PowerShell 执行
        result = self._session.run_ps(command)
        out = result.std_out.decode("utf-8", errors="replace")
        err = result.std_err.decode("utf-8", errors="replace")
        exit_code = result.status_code
        logger.debug("winrm_result", exit_code=exit_code, stdout_len=len(out))
        return ExecutionResult(stdout=out, stderr=err, exit_code=exit_code)

    def execute_cmd(self, command: str, args: list[str] | None = None) -> ExecutionResult:
        """执行 cmd.exe 命令（非 PowerShell）。"""
        if not self._session:
            raise RuntimeError("WinRM 连接未建立")
        result = self._session.run_cmd(command, args or [])
        return ExecutionResult(
            stdout=result.std_out.decode("utf-8", errors="replace"),
            stderr=result.std_err.decode("utf-8", errors="replace"),
            exit_code=result.status_code,
        )

    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """通过 PowerShell 脚本内容写入方式上传文件（无 SFTP，需分块）。"""
        if not self._session:
            raise RuntimeError("WinRM 连接未建立")
        content = Path(local_path).read_bytes()
        # Base64 编码后通过 PowerShell 写入（适合中小文件 < 10MB）
        import base64
        encoded = base64.b64encode(content).decode("ascii")
        ps_script = (
            f"$bytes = [Convert]::FromBase64String('{encoded}');"
            f"[IO.File]::WriteAllBytes('{remote_path}', $bytes)"
        )
        result = self.execute(ps_script)
        if result.succeeded:
            logger.info("winrm_upload", local=local_path, remote=remote_path)
        return result.succeeded

    def close(self) -> None:
        self._session = None
        logger.debug("winrm_disconnected", host=self._host)

    def execute_sql(self, db_type: str, sql: str, timeout: int = 60) -> ExecutionResult:
        """Windows 上执行 SQL，SQL Server 使用 sqlcmd，MySQL/PostgreSQL 使用各自 CLI。"""
        if db_type == "sqlserver":
            # sqlcmd 使用 Windows 集成验证
            ps = f"sqlcmd -S localhost -E -Q \"{sql.replace(chr(34), chr(39))}\""
        elif db_type == "mysql":
            ps = f'& "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe" -u root -e "{sql}"'
        elif db_type == "postgresql":
            ps = f'& "C:\\Program Files\\PostgreSQL\\15\\bin\\psql.exe" -U postgres -c "{sql}"'
        else:
            ps = sql
        return self.execute(ps, timeout=timeout)
