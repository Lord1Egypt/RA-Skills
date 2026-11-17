"""华为云远程命令执行（通过 SSH/WinRM，无云助手时的通用通道）。"""

# 华为云无统一云助手，命令执行直接委托 executor/ssh_executor.py 和 executor/winrm_executor.py。
# 本模块保留扩展点，用于未来华为云 CMS（Cloud Management Service）API 支持。

from providers.base import CommandResult


class HuaweiRemoteCommand:
    """占位类：华为云命令执行通过 SSH/WinRM executor 完成。"""

    def run_via_ssh(self, host: str, command: str, ssh_executor) -> CommandResult:
        result = ssh_executor.execute(command)
        return CommandResult(
            invocation_id=f"ssh-{host}",
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            status="Finished" if result.exit_code == 0 else "Failed",
        )
