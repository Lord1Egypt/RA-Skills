"""腾讯云 TAT（自动化助手）远程命令执行适配器。"""

from __future__ import annotations

import base64
import time

import structlog
from providers.base import CommandResult

logger = structlog.get_logger(__name__)

_CMD_TYPE_MAP = {
    "RunShellScript": "SHELL",
    "RunPowerShellScript": "POWERSHELL",
    "shell": "SHELL",
    "powershell": "POWERSHELL",
}


class TencentTAT:
    def __init__(self, secret_id: str, secret_key: str, default_region: str = "ap-guangzhou") -> None:
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._default_region = default_region

    def _get_client(self, region: str):
        from tencentcloud.common import credential
        from tencentcloud.tat.v20201028 import tat_client
        cred = credential.Credential(self._secret_id, self._secret_key)
        return tat_client.TatClient(cred, region)

    def run_command(self, instance_id: str, command: str, command_type: str = "RunShellScript",
                    timeout: int = 300, region: str = "") -> str:
        region = region or self._default_region
        from tencentcloud.tat.v20201028 import models as tat_models
        client = self._get_client(region)

        content_b64 = base64.b64encode(command.encode("utf-8")).decode("utf-8")
        cmd_type = _CMD_TYPE_MAP.get(command_type, "SHELL")

        req = tat_models.RunCommandRequest()
        req.Content = content_b64
        req.InstanceIds = [instance_id]
        req.CommandType = cmd_type
        req.Timeout = timeout
        req.Username = "root" if cmd_type == "SHELL" else "Administrator"

        response = client.RunCommand(req)
        invocation_id = response.InvocationId
        logger.info("tencent_tat_run", instance_id=instance_id, invocation_id=invocation_id)
        return invocation_id

    def get_command_result(self, invocation_id: str, region: str = "") -> CommandResult:
        region = region or self._default_region
        from tencentcloud.tat.v20201028 import models as tat_models
        client = self._get_client(region)
        req = tat_models.DescribeInvocationTasksRequest()
        # DescribeInvocationTasksRequest 没有 InvocationId 字段（只有 InvocationTaskIds/Filters），
        # 必须用 Filters + "invocation-id" 过滤键按执行活动 ID 查任务，否则请求里不会带任何过滤条件。
        invocation_filter = tat_models.Filter()
        invocation_filter.Name = "invocation-id"
        invocation_filter.Values = [invocation_id]
        req.Filters = [invocation_filter]
        response = client.DescribeInvocationTasks(req)
        tasks = response.InvocationTaskSet or []
        if not tasks:
            return CommandResult(invocation_id=invocation_id, status="Running")
        task = tasks[0]
        stdout = base64.b64decode(task.TaskResult.Output or "").decode("utf-8", errors="replace")
        status_map = {"PENDING": "Running", "DELIVERING": "Running", "RUNNING": "Running",
                      "SUCCESS": "Finished", "FAILED": "Failed", "TIMEOUT": "Stopped"}
        return CommandResult(
            invocation_id=invocation_id,
            stdout=stdout,
            exit_code=task.TaskResult.ExitCode or 0,
            status=status_map.get(task.TaskStatus or "", "Running"),
        )

    def run_command_sync(self, instance_id: str, command: str, command_type: str = "RunShellScript",
                         timeout: int = 300, region: str = "", poll_interval: int = 5,
                         max_attempts: int = 60) -> CommandResult:
        invocation_id = self.run_command(instance_id, command, command_type, timeout, region)
        for _ in range(max_attempts):
            result = self.get_command_result(invocation_id, region)
            if result.status in ("Finished", "Failed", "Stopped"):
                return result
            time.sleep(poll_interval)
        return CommandResult(invocation_id=invocation_id, status="Timeout", exit_code=-1,
                             stderr=f"TAT 命令超时（{max_attempts * poll_interval}s）")
