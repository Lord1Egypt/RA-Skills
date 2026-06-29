"""华为云 ECS 实例管理适配器（第四阶段完整实现，当前提供 SSH fallback 框架）。"""

from __future__ import annotations

import structlog
from providers.base import CloudProviderBase, CommandResult, ServerInstance

logger = structlog.get_logger(__name__)


class HuaweiECS(CloudProviderBase):
    """华为云 ECS 适配器。华为云无统一云助手，默认走 SSH / WinRM。"""

    def __init__(self, access_key_id: str, secret_access_key: str,
                 project_id: str, default_region: str = "cn-east-3") -> None:
        self._ak = access_key_id
        self._sk = secret_access_key
        self._project_id = project_id
        self._default_region = default_region

    def _get_ecs_client(self, region: str):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkecs.v2 import EcsClient
        from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
        creds = BasicCredentials(self._ak, self._sk, self._project_id)
        return EcsClient.new_builder().with_credentials(creds).with_region(EcsRegion.value_of(region)).build()

    def list_instances(self, region: str = "") -> list[ServerInstance]:
        region = region or self._default_region
        from huaweicloudsdkecs.v2 import model as ecs_model
        client = self._get_ecs_client(region)
        request = ecs_model.ListServersDetailsRequest()
        response = client.list_servers_details(request)
        instances = []
        for s in (response.servers or []):
            addresses = s.addresses or {}
            all_ips = [a for nets in addresses.values() for a in nets]
            private_ips = [a.addr for a in all_ips if a.os_ext_ips_type == "fixed"]
            public_ips = [a.addr for a in all_ips if a.os_ext_ips_type == "floating"]
            instances.append(ServerInstance(
                instance_id=s.id,
                name=s.name or "",
                status=s.status or "",
                os_type="windows" if "windows" in (s.os_ext_srv_attr_host or "").lower() else "linux",
                public_ip=public_ips[0] if public_ips else "",
                private_ip=private_ips[0] if private_ips else "",
                region=region,
            ))
        return instances

    def get_instance(self, instance_id: str, region: str = "") -> ServerInstance:
        region = region or self._default_region
        from huaweicloudsdkecs.v2 import model as ecs_model
        client = self._get_ecs_client(region)
        request = ecs_model.ShowServerRequest(server_id=instance_id)
        response = client.show_server(request)
        s = response.server
        addresses = s.addresses or {}
        all_ips = [a for nets in addresses.values() for a in nets]
        private_ips = [a.addr for a in all_ips if a.os_ext_ips_type == "fixed"]
        public_ips = [a.addr for a in all_ips if a.os_ext_ips_type == "floating"]
        return ServerInstance(
            instance_id=s.id,
            name=s.name or "",
            status=s.status or "",
            os_type="windows" if "windows" in (s.os_ext_srv_attr_os_type or "").lower() else "linux",
            public_ip=public_ips[0] if public_ips else "",
            private_ip=private_ips[0] if private_ips else "",
            region=region,
        )

    def run_command(self, instance_id: str, command: str, command_type: str = "RunShellScript",
                    timeout: int = 300, region: str = "") -> str:
        # 华为云走 SSH/WinRM，由 executor 层处理，此处返回占位 ID
        return f"huawei-direct-{instance_id}"

    def get_command_result(self, invocation_id: str, region: str = "") -> CommandResult:
        return CommandResult(invocation_id=invocation_id, status="Finished")

    def reboot_instance(self, instance_id: str, region: str = "") -> bool:
        region = region or self._default_region
        from huaweicloudsdkecs.v2 import model as ecs_model
        client = self._get_ecs_client(region)
        reboot = ecs_model.BatchRebootServersRequestBody(
            reboot=ecs_model.BatchRebootSeversOption(
                type="SOFT",
                servers=[ecs_model.ServerId(id=instance_id)],
            )
        )
        request = ecs_model.BatchRebootServersRequest(body=reboot)
        client.batch_reboot_servers(request)
        return True

    def describe_security_groups(self, instance_id: str, region: str = "") -> list[dict]:
        region = region or self._default_region
        from huaweicloudsdkecs.v2 import model as ecs_model
        client = self._get_ecs_client(region)
        request = ecs_model.ShowServerRequest(server_id=instance_id)
        response = client.show_server(request)
        sg_names = [g.name for g in (response.server.security_groups or [])]
        if not sg_names:
            return []

        from huaweicloudsdkvpc.v3 import VpcClient, model as vpc_model
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkvpc.v3.region.vpc_region import VpcRegion
        creds = BasicCredentials(self._ak, self._sk, self._project_id)
        vpc_client = VpcClient.new_builder().with_credentials(creds).with_region(
            VpcRegion.value_of(region)
        ).build()

        groups = []
        for name in sg_names:
            req = vpc_model.ListSecurityGroupsRequest(name=[name])
            resp = vpc_client.list_security_groups(req)
            for sg in (resp.security_groups or []):
                groups.append({"id": sg.id, "name": sg.name})
        return groups

    def update_security_group_rule(self, security_group_id: str, port: int, protocol: str = "TCP",
                                   source_cidr: str = "10.0.0.0/8", action: str = "accept",
                                   region: str = "") -> bool:
        from providers.huawei.security_group import HuaweiSecurityGroup
        sg = HuaweiSecurityGroup(self._ak, self._sk, self._project_id, region or self._default_region)
        return sg.open_port_for_internal(security_group_id, port, protocol, source_cidr, region)
