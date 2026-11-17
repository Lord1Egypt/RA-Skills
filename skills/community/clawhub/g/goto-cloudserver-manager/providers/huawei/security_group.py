"""华为云安全组规则管理（第四阶段完整实现）。"""

from __future__ import annotations

import structlog

logger = structlog.get_logger(__name__)


class HuaweiSecurityGroup:
    def __init__(self, access_key_id: str, secret_access_key: str,
                 project_id: str, default_region: str = "cn-east-3") -> None:
        self._ak = access_key_id
        self._sk = secret_access_key
        self._project_id = project_id
        self._default_region = default_region

    def _get_client(self, region: str):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkvpc.v3 import VpcClient
        from huaweicloudsdkvpc.v3.region.vpc_region import VpcRegion
        creds = BasicCredentials(self._ak, self._sk, self._project_id)
        return VpcClient.new_builder().with_credentials(creds).with_region(
            VpcRegion.value_of(region or self._default_region)
        ).build()

    def list_rules(self, security_group_id: str, region: str = "") -> list[dict]:
        region = region or self._default_region
        from huaweicloudsdkvpc.v3 import model as vpc_model
        client = self._get_client(region)
        request = vpc_model.ListSecurityGroupRulesRequest(security_group_id=security_group_id)
        response = client.list_security_group_rules(request)
        rules = []
        for r in (response.security_group_rules or []):
            rules.append({
                "id": r.id,
                "direction": r.direction,
                "protocol": r.protocol or "any",
                "port_range": r.multiport or "",
                "source": r.remote_ip_prefix or r.remote_group_id or "",
                "policy": r.action,
            })
        return rules

    def open_port_for_internal(
        self,
        security_group_id: str,
        port: int,
        protocol: str = "TCP",
        source_cidr: str = "10.0.0.0/8",
        region: str = "",
    ) -> bool:
        if source_cidr == "0.0.0.0/0":
            raise ValueError(f"安全策略禁止将端口 {port} 对公网开放")
        region = region or self._default_region
        from huaweicloudsdkvpc.v3 import model as vpc_model
        client = self._get_client(region)
        request = vpc_model.CreateSecurityGroupRuleRequest()
        request.body = vpc_model.CreateSecurityGroupRuleRequestBody(
            security_group_rule=vpc_model.CreateSecurityGroupRuleOption(
                security_group_id=security_group_id,
                direction="ingress",
                ethertype="IPv4",
                protocol=protocol.lower(),
                multiport=str(port),
                remote_ip_prefix=source_cidr,
            )
        )
        client.create_security_group_rule(request)
        logger.info("huawei_sg_open_port", sg=security_group_id, port=port, source=source_cidr)
        return True

    def revoke_rule(self, security_group_rule_id: str, region: str = "") -> bool:
        region = region or self._default_region
        from huaweicloudsdkvpc.v3 import model as vpc_model
        client = self._get_client(region)
        request = vpc_model.DeleteSecurityGroupRuleRequest(security_group_rule_id=security_group_rule_id)
        client.delete_security_group_rule(request)
        logger.info("huawei_sg_rule_revoked", rule_id=security_group_rule_id)
        return True
