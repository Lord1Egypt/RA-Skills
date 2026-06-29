"""云助手/TAT 执行器：将命令通过云厂商 API 发送到实例上执行。"""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

from executor.base import ExecutionResult, ExecutorBase

if TYPE_CHECKING:
    from core.config_loader import ServerConfig

logger = structlog.get_logger(__name__)


class CloudCommandExecutor(ExecutorBase):
    """封装阿里云云助手 / 腾讯云 TAT，提供统一执行接口。"""

    def __init__(
        self,
        provider: str,
        provider_config: dict,
        credentials: dict,
    ) -> None:
        self._provider = provider
        self._provider_config = provider_config
        self._credentials = credentials
        self._server: "ServerConfig | None" = None
        self._assistant = None

    def connect(self, server: "ServerConfig") -> None:
        self._server = server
        if self._provider == "aliyun":
            from providers.aliyun.cloud_assistant import AliyunCloudAssistant
            self._assistant = AliyunCloudAssistant(
                access_key_id=self._credentials.get("access_key_id", ""),
                access_key_secret=self._credentials.get("access_key_secret", ""),
                default_region=server.region,
            )
        elif self._provider in ("tencent", "tencent-lighthouse"):
            from providers.tencent.tat import TencentTAT
            self._assistant = TencentTAT(
                secret_id=self._credentials.get("secret_id", ""),
                secret_key=self._credentials.get("secret_key", ""),
                default_region=server.region,
            )
        logger.info("cloud_command_executor_connected", provider=self._provider, server=server.id)

    def execute(self, command: str, timeout: int = 300) -> ExecutionResult:
        if not self._server or not self._assistant:
            raise RuntimeError("CloudCommandExecutor 连接未建立")

        os_type = self._server.os_type
        command_type = "RunPowerShellScript" if os_type == "windows" else "RunShellScript"

        result = self._assistant.run_command_sync(
            instance_id=self._server.instance_id,
            command=command,
            command_type=command_type,
            timeout=timeout,
            region=self._server.region,
            poll_interval=self._provider_config.get("poll_interval_seconds", 5),
            max_attempts=self._provider_config.get("max_poll_attempts", 60),
        )

        return ExecutionResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
        )

    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """云助手不支持直接上传文件，通过 Base64 编码注入到命令中。"""
        import base64
        from pathlib import Path
        content = Path(local_path).read_bytes()
        encoded = base64.b64encode(content).decode("ascii")
        if self._server and self._server.os_type == "windows":
            cmd = (
                f"$bytes = [Convert]::FromBase64String('{encoded}');"
                f"[IO.File]::WriteAllBytes('{remote_path}', $bytes)"
            )
        else:
            cmd = (
                f"echo '{encoded}' | base64 -d > '{remote_path}'"
            )
        result = self.execute(cmd)
        return result.succeeded

    def close(self) -> None:
        self._server = None
        self._assistant = None
