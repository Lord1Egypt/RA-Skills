"""云厂商适配器抽象基类。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ServerInstance:
    instance_id: str
    name: str
    status: str                        # running / stopped / starting / stopping
    os_type: str                       # windows / linux
    public_ip: str = ""
    private_ip: str = ""
    region: str = ""
    tags: dict[str, str] = field(default_factory=dict)
    raw: dict = field(default_factory=dict)


@dataclass
class CommandResult:
    invocation_id: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    status: str = "Finished"           # Running / Finished / Failed / Stopped
    started_at: datetime | None = None
    finished_at: datetime | None = None

    @property
    def succeeded(self) -> bool:
        return self.status == "Finished" and self.exit_code == 0


class CloudProviderBase(ABC):
    """所有云厂商适配器的统一接口。"""

    @abstractmethod
    def list_instances(self, region: str) -> list[ServerInstance]:
        """列出指定区域的所有云服务器实例。"""

    @abstractmethod
    def get_instance(self, instance_id: str, region: str = "") -> ServerInstance:
        """获取单个实例详情。"""

    @abstractmethod
    def run_command(
        self,
        instance_id: str,
        command: str,
        command_type: str = "RunShellScript",  # RunShellScript / RunPowerShellScript / RunBatScript
        timeout: int = 300,
        region: str = "",
    ) -> str:
        """在实例上执行命令，返回 invocation_id。"""

    @abstractmethod
    def get_command_result(self, invocation_id: str, region: str = "") -> CommandResult:
        """查询命令执行结果。"""

    def run_command_sync(
        self,
        instance_id: str,
        command: str,
        command_type: str = "RunShellScript",
        timeout: int = 300,
        region: str = "",
        poll_interval: int = 5,
        max_attempts: int = 60,
    ) -> CommandResult:
        """同步执行命令：轮询直到完成或超时。"""
        import time
        invocation_id = self.run_command(instance_id, command, command_type, timeout, region)
        for _ in range(max_attempts):
            result = self.get_command_result(invocation_id, region)
            if result.status in ("Finished", "Failed", "Stopped"):
                return result
            time.sleep(poll_interval)
        return CommandResult(
            invocation_id=invocation_id,
            status="Timeout",
            exit_code=-1,
            stderr=f"命令执行超时（{max_attempts * poll_interval}s）",
        )

    @abstractmethod
    def reboot_instance(self, instance_id: str, region: str = "") -> bool:
        """重启实例。"""

    @abstractmethod
    def describe_security_groups(self, instance_id: str, region: str = "") -> list[dict]:
        """获取实例关联的安全组规则。"""

    @abstractmethod
    def update_security_group_rule(
        self,
        security_group_id: str,
        port: int,
        protocol: str = "TCP",
        source_cidr: str = "10.0.0.0/8",
        action: str = "accept",
        region: str = "",
    ) -> bool:
        """添加/修改安全组规则（仅允许内网段，不对公网开放数据库端口）。"""
