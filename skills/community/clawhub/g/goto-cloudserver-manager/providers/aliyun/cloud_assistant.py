"""阿里云云助手（ECS RunCommand）远程命令执行适配器。"""

from __future__ import annotations

import base64
import time

import structlog

from providers.base import CloudProviderBase, CommandResult, ServerInstance

logger = structlog.get_logger(__name__)

# 云助手命令类型映射
_CMD_TYPE_MAP = {
    "RunShellScript": "RunShellScript",
    "RunPowerShellScript": "RunPowerShellScript",
    "RunBatScript": "RunBatScript",
    "shell": "RunShellScript",
    "powershell": "RunPowerShellScript",
    "bat": "RunBatScript",
}


class AliyunCloudAssistant:
    """调用阿里云 ECS RunCommand API 在实例上远程执行命令。"""

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        default_region: str = "cn-hangzhou",
    ) -> None:
        self._ak_id = access_key_id
        self._ak_secret = access_key_secret
        self._default_region = default_region
        self._clients: dict = {}

    def _get_client(self, region: str):
        if region not in self._clients:
            from alibabacloud_ecs20140526.client import Client
            from alibabacloud_tea_openapi import models as open_api_models
            config = open_api_models.Config(
                access_key_id=self._ak_id,
                access_key_secret=self._ak_secret,
                region_id=region,
            )
            self._clients[region] = Client(config)
        return self._clients[region]

    def run_command(
        self,
        instance_id: str,
        command: str,
        command_type: str = "RunShellScript",
        timeout: int = 300,
        region: str = "",
    ) -> str:
        """发送命令到 ECS 实例，返回 invocation_id。"""
        region = region or self._default_region
        cmd_type = _CMD_TYPE_MAP.get(command_type, command_type)

        # 阿里云要求命令内容 Base64 编码
        content_b64 = base64.b64encode(command.encode("utf-8")).decode("utf-8")

        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.RunCommandRequest(
            region_id=region,
            type=cmd_type,
            command_content=content_b64,
            instance_id=[instance_id],
            timeout=timeout,
            content_encoding="Base64",
        )
        response = client.run_command(request)
        invocation_id = response.body.invoke_id
        logger.info(
            "aliyun_cloud_assistant_run",
            instance_id=instance_id,
            invocation_id=invocation_id,
            command_type=cmd_type,
        )
        return invocation_id

    def get_command_result(self, invocation_id: str, region: str = "") -> CommandResult:
        """查询云助手命令执行结果。"""
        region = region or self._default_region
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.DescribeInvocationResultsRequest(
            region_id=region,
            invoke_id=invocation_id,
        )
        response = client.describe_invocation_results(request)
        results = response.body.invocation.invocation_results.invocation_result or []
        if not results:
            return CommandResult(invocation_id=invocation_id, status="Running")

        r = results[0]
        stdout = base64.b64decode(r.output or "").decode("utf-8", errors="replace")
        status_map = {
            "Running": "Running",
            "Stopped": "Stopped",
            "Failed": "Failed",
            "PartialFailed": "Failed",
            "Success": "Finished",
        }
        return CommandResult(
            invocation_id=invocation_id,
            stdout=stdout,
            stderr="",
            exit_code=r.exit_code or 0,
            status=status_map.get(r.invocation_record_status or "", "Running"),
        )

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
        """同步执行：run_command + 轮询 get_command_result 直到完成。"""
        invocation_id = self.run_command(instance_id, command, command_type, timeout, region)
        for attempt in range(max_attempts):
            result = self.get_command_result(invocation_id, region)
            if result.status in ("Finished", "Failed", "Stopped"):
                logger.info(
                    "aliyun_cloud_assistant_done",
                    invocation_id=invocation_id,
                    status=result.status,
                    exit_code=result.exit_code,
                    attempts=attempt + 1,
                )
                return result
            time.sleep(poll_interval)

        return CommandResult(
            invocation_id=invocation_id,
            status="Timeout",
            exit_code=-1,
            stderr=f"命令执行超时（已等待 {max_attempts * poll_interval}s）",
        )
