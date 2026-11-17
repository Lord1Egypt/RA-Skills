"""腾讯云 CVM 实例管理适配器（第三阶段实现）。"""

from __future__ import annotations

import structlog
from providers.base import CloudProviderBase, CommandResult, ServerInstance

logger = structlog.get_logger(__name__)


class TencentCVM(CloudProviderBase):
    """腾讯云 CVM 适配器。命令执行通过 TAT 自动化助手完成。"""

    def __init__(self, secret_id: str, secret_key: str, default_region: str = "ap-guangzhou") -> None:
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._default_region = default_region

    def _get_credential(self):
        from tencentcloud.common import credential
        return credential.Credential(self._secret_id, self._secret_key)

    def list_instances(self, region: str = "") -> list[ServerInstance]:
        region = region or self._default_region
        from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
        cred = self._get_credential()
        client = cvm_client.CvmClient(cred, region)
        req = cvm_models.DescribeInstancesRequest()
        req.Limit = 100
        response = client.DescribeInstances(req)
        instances = []
        for inst in (response.InstanceSet or []):
            instances.append(ServerInstance(
                instance_id=inst.InstanceId,
                name=inst.InstanceName or "",
                status=inst.InstanceState or "",
                os_type="windows" if "windows" in (inst.OsName or "").lower() else "linux",
                public_ip=(inst.PublicIpAddresses or [""])[0],
                private_ip=(inst.PrivateIpAddresses or [""])[0],
                region=region,
            ))
        return instances

    def get_instance(self, instance_id: str, region: str = "") -> ServerInstance:
        region = region or self._default_region
        from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
        cred = self._get_credential()
        client = cvm_client.CvmClient(cred, region)
        req = cvm_models.DescribeInstancesRequest()
        req.InstanceIds = [instance_id]
        response = client.DescribeInstances(req)
        instances = response.InstanceSet or []
        if not instances:
            raise ValueError(f"CVM 实例 '{instance_id}' 未找到")
        inst = instances[0]
        return ServerInstance(
            instance_id=inst.InstanceId,
            name=inst.InstanceName or "",
            status=inst.InstanceState or "",
            os_type="windows" if "windows" in (inst.OsName or "").lower() else "linux",
            public_ip=(inst.PublicIpAddresses or [""])[0],
            private_ip=(inst.PrivateIpAddresses or [""])[0],
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
        from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
        cred = self._get_credential()
        client = cvm_client.CvmClient(cred, region)
        req = cvm_models.RebootInstancesRequest()
        req.InstanceIds = [instance_id]
        client.RebootInstances(req)
        return True

    def describe_security_groups(self, instance_id: str, region: str = "") -> list[dict]:
        region = region or self._default_region
        from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
        cred = self._get_credential()
        client = cvm_client.CvmClient(cred, region)
        req = cvm_models.DescribeInstancesRequest()
        req.InstanceIds = [instance_id]
        response = client.DescribeInstances(req)
        instances = response.InstanceSet or []
        if not instances:
            raise ValueError(f"CVM 实例 '{instance_id}' 未找到")
        sg_ids = instances[0].SecurityGroupIds or []
        return [{"id": sg_id, "name": sg_id} for sg_id in sg_ids]

    def update_security_group_rule(self, security_group_id: str, port: int, protocol: str = "TCP",
                                   source_cidr: str = "10.0.0.0/8", action: str = "accept", region: str = "") -> bool:
        from providers.tencent.security_group import TencentSecurityGroup
        sg = TencentSecurityGroup(self._secret_id, self._secret_key, region or self._default_region)
        return sg.open_port_for_internal(security_group_id, port, protocol, source_cidr, region)
