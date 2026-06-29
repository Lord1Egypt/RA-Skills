"""腾讯云 Lighthouse（轻量应用服务器）适配器。

轻量应用服务器与 CVM 是不同的产品线，使用独立的 DescribeInstances / RebootInstances API，
安全组也由实例级"防火墙规则"（FirewallRules）代替 VPC 安全组。命令执行仍复用 TAT 自动化助手——
TAT 的 RunCommand 明确支持 Lighthouse 实例 ID。
"""

from __future__ import annotations

import structlog
from providers.base import CloudProviderBase, CommandResult, ServerInstance

logger = structlog.get_logger(__name__)


class TencentLighthouse(CloudProviderBase):
    """腾讯云 Lighthouse 适配器。命令执行通过 TAT 自动化助手完成。"""

    def __init__(self, secret_id: str, secret_key: str, default_region: str = "ap-guangzhou") -> None:
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._default_region = default_region

    def _get_credential(self):
        from tencentcloud.common import credential
        return credential.Credential(self._secret_id, self._secret_key)

    def _get_client(self, region: str):
        from tencentcloud.lighthouse.v20200324 import lighthouse_client
        return lighthouse_client.LighthouseClient(self._get_credential(), region)

    def list_instances(self, region: str = "") -> list[ServerInstance]:
        region = region or self._default_region
        from tencentcloud.lighthouse.v20200324 import models as lh_models
        client = self._get_client(region)
        req = lh_models.DescribeInstancesRequest()
        req.Limit = 100
        response = client.DescribeInstances(req)
        instances = []
        for inst in (response.InstanceSet or []):
            instances.append(ServerInstance(
                instance_id=inst.InstanceId,
                name=inst.InstanceName or "",
                status=inst.InstanceState or "",
                os_type="windows" if "WINDOWS" in (inst.PlatformType or "").upper() else "linux",
                public_ip=(inst.PublicAddresses or [""])[0],
                private_ip=(inst.PrivateAddresses or [""])[0],
                region=region,
            ))
        logger.info("tencent_lighthouse_list_instances", region=region, count=len(instances))
        return instances

    def get_instance(self, instance_id: str, region: str = "") -> ServerInstance:
        region = region or self._default_region
        from tencentcloud.lighthouse.v20200324 import models as lh_models
        client = self._get_client(region)
        req = lh_models.DescribeInstancesRequest()
        req.InstanceIds = [instance_id]
        response = client.DescribeInstances(req)
        instances = response.InstanceSet or []
        if not instances:
            raise ValueError(f"Lighthouse 实例 '{instance_id}' 未找到")
        inst = instances[0]
        return ServerInstance(
            instance_id=inst.InstanceId,
            name=inst.InstanceName or "",
            status=inst.InstanceState or "",
            os_type="windows" if "WINDOWS" in (inst.PlatformType or "").upper() else "linux",
            public_ip=(inst.PublicAddresses or [""])[0],
            private_ip=(inst.PrivateAddresses or [""])[0],
            region=region,
        )

    def run_command(self, instance_id: str, command: str, command_type: str = "RunShellScript",
                    timeout: int = 300, region: str = "") -> str:
        from providers.tencent.tat import TencentTAT
        tat = TencentTAT(self._secret_id, self._secret_key, region or self._default_region)
        return tat.run_command(instance_id, command, command_type, timeout, region)

    def get_command_result(self, invocation_id: str, region: str = "") -> CommandResult:
        from providers.tencent.tat import TencentTAT
        tat = TencentTAT(self._secret_id, self._secret_key, region or self._default_region)
        return tat.get_command_result(invocation_id, region)

    def reboot_instance(self, instance_id: str, region: str = "") -> bool:
        region = region or self._default_region
        from tencentcloud.lighthouse.v20200324 import models as lh_models
        client = self._get_client(region)
        req = lh_models.RebootInstancesRequest()
        req.InstanceIds = [instance_id]
        client.RebootInstances(req)
        logger.info("tencent_lighthouse_reboot_instance", instance_id=instance_id, region=region)
        return True

    def describe_security_groups(self, instance_id: str, region: str = "") -> list[dict]:
        """Lighthouse 没有独立安全组资源，防火墙规则直接挂在实例上，因此用 instance_id 本身作为 id。"""
        region = region or self._default_region
        from tencentcloud.lighthouse.v20200324 import models as lh_models
        client = self._get_client(region)
        req = lh_models.DescribeFirewallRulesRequest()
        req.InstanceId = instance_id
        client.DescribeFirewallRules(req)
        return [{"id": instance_id, "name": f"{instance_id}-firewall"}]

    def update_security_group_rule(
        self,
        security_group_id: str,
        port: int,
        protocol: str = "TCP",
        source_cidr: str = "10.0.0.0/8",
        action: str = "accept",
        region: str = "",
    ) -> bool:
        """security_group_id 即 describe_security_groups 返回的 instance_id。"""
        if source_cidr == "0.0.0.0/0":
            raise ValueError(f"安全策略禁止将端口 {port} 对公网开放")
        region = region or self._default_region
        import json
        from tencentcloud.lighthouse.v20200324 import models as lh_models
        client = self._get_client(region)
        req = lh_models.CreateFirewallRulesRequest()
        req.from_json_string(json.dumps({
            "InstanceId": security_group_id,
            "FirewallRules": [
                {
                    "Protocol": protocol,
                    "Port": str(port),
                    "CidrBlock": source_cidr,
                    "Action": "ACCEPT",
                    "FirewallRuleDescription": "goto-cloudserver-manager",
                }
            ],
        }))
        client.CreateFirewallRules(req)
        logger.info("tencent_lighthouse_firewall_rule_added", instance_id=security_group_id, port=port, source=source_cidr)
        return True
