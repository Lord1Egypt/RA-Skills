"""阿里云 ECS 实例管理适配器。"""

from __future__ import annotations

import structlog
from providers.base import CloudProviderBase, CommandResult, ServerInstance

logger = structlog.get_logger(__name__)


class AliyunECS(CloudProviderBase):
    """阿里云 ECS 实例管理（列举实例、重启、安全组）。

    命令执行通过 AliyunCloudAssistant 完成，此类专注实例生命周期管理。
    """

    def __init__(self, access_key_id: str, access_key_secret: str, default_region: str = "cn-hangzhou") -> None:
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

    def list_instances(self, region: str = "") -> list[ServerInstance]:
        region = region or self._default_region
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.DescribeInstancesRequest(region_id=region, page_size=100)
        response = client.describe_instances(request)
        instances = []
        for inst in (response.body.instances.instance or []):
            instances.append(ServerInstance(
                instance_id=inst.instance_id,
                name=inst.instance_name or "",
                status=inst.status or "",
                os_type="windows" if "windows" in (inst.osname or "").lower() else "linux",
                public_ip=(inst.public_ip_address.ip_address or [""])[0] if inst.public_ip_address else "",
                private_ip=(inst.inner_ip_address.ip_address or [""])[0] if inst.inner_ip_address else "",
                region=region,
                tags={t.tag_key: t.tag_value for t in (inst.tags.tag or []) if t.tag_key},
                raw=inst.to_map() if hasattr(inst, "to_map") else {},
            ))
        logger.info("aliyun_list_instances", region=region, count=len(instances))
        return instances

    def get_instance(self, instance_id: str, region: str = "") -> ServerInstance:
        region = region or self._default_region
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.DescribeInstancesRequest(
            region_id=region,
            instance_ids=f'["{instance_id}"]',
        )
        response = client.describe_instances(request)
        instances = response.body.instances.instance or []
        if not instances:
            raise ValueError(f"ECS 实例 '{instance_id}' 在区域 '{region}' 中未找到")
        inst = instances[0]
        return ServerInstance(
            instance_id=inst.instance_id,
            name=inst.instance_name or "",
            status=inst.status or "",
            os_type="windows" if "windows" in (inst.osname or "").lower() else "linux",
            public_ip=(inst.public_ip_address.ip_address or [""])[0] if inst.public_ip_address else "",
            private_ip=(inst.inner_ip_address.ip_address or [""])[0] if inst.inner_ip_address else "",
            region=region,
        )

    def run_command(self, instance_id: str, command: str, command_type: str = "RunShellScript",
                    timeout: int = 300, region: str = "") -> str:
        # 实际命令执行委托给 AliyunCloudAssistant
        from providers.aliyun.cloud_assistant import AliyunCloudAssistant
        assistant = AliyunCloudAssistant(self._ak_id, self._ak_secret, region or self._default_region)
        return assistant.run_command(instance_id, command, command_type, timeout, region)

    def get_command_result(self, invocation_id: str, region: str = "") -> CommandResult:
        from providers.aliyun.cloud_assistant import AliyunCloudAssistant
        assistant = AliyunCloudAssistant(self._ak_id, self._ak_secret, region or self._default_region)
        return assistant.get_command_result(invocation_id, region)

    def reboot_instance(self, instance_id: str, region: str = "") -> bool:
        region = region or self._default_region
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.RebootInstanceRequest(instance_id=instance_id, force_stop=False)
        client.reboot_instance(request)
        logger.info("aliyun_reboot_instance", instance_id=instance_id, region=region)
        return True

    def describe_security_groups(self, instance_id: str, region: str = "") -> list[dict]:
        region = region or self._default_region
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        inst = self.get_instance(instance_id, region)
        request = ecs_models.DescribeSecurityGroupsRequest(region_id=region)
        response = client.describe_security_groups(request)
        groups = response.body.security_groups.security_group or []
        return [{"id": g.security_group_id, "name": g.security_group_name} for g in groups]

    def update_security_group_rule(
        self,
        security_group_id: str,
        port: int,
        protocol: str = "TCP",
        source_cidr: str = "10.0.0.0/8",
        action: str = "accept",
        region: str = "",
    ) -> bool:
        region = region or self._default_region
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.AuthorizeSecurityGroupRequest(
            region_id=region,
            security_group_id=security_group_id,
            ip_protocol=protocol,
            port_range=f"{port}/{port}",
            source_cidr_ip=source_cidr,
            policy="accept",
        )
        client.authorize_security_group(request)
        logger.info("aliyun_sg_rule_added", sg_id=security_group_id, port=port, source=source_cidr)
        return True
