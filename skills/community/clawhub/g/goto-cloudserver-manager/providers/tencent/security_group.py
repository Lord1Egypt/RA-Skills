"""腾讯云安全组规则管理（第三阶段完整实现）。"""

from __future__ import annotations

import json

import structlog

logger = structlog.get_logger(__name__)


class TencentSecurityGroup:
    def __init__(self, secret_id: str, secret_key: str, default_region: str = "ap-guangzhou") -> None:
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._default_region = default_region

    def _get_client(self, region: str):
        from tencentcloud.common import credential
        from tencentcloud.vpc.v20170312 import vpc_client
        cred = credential.Credential(self._secret_id, self._secret_key)
        return vpc_client.VpcClient(cred, region or self._default_region)

    def list_rules(self, security_group_id: str, region: str = "") -> list[dict]:
        region = region or self._default_region
        from tencentcloud.vpc.v20170312 import models as vpc_models
        client = self._get_client(region)
        req = vpc_models.DescribeSecurityGroupPoliciesRequest()
        req.SecurityGroupId = security_group_id
        response = client.DescribeSecurityGroupPolicies(req)
        rules = []
        for p in (response.SecurityGroupPolicySet.Ingress or []):
            rules.append({
                "direction": "ingress",
                "protocol": p.Protocol,
                "port_range": p.Port,
                "source": p.CidrBlock or p.SecurityGroupId or "",
                "policy": p.Action,
                "index": p.PolicyIndex,
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
        """仅允许内网段访问指定端口，拒绝对公网开放数据库端口。"""
        if source_cidr == "0.0.0.0/0":
            raise ValueError(f"安全策略禁止将端口 {port} 对公网开放")
        region = region or self._default_region
        from tencentcloud.vpc.v20170312 import models as vpc_models
        client = self._get_client(region)
        req = vpc_models.CreateSecurityGroupPoliciesRequest()
        params = {
            "SecurityGroupId": security_group_id,
            "SecurityGroupPolicySet": {
                "Ingress": [
                    {
                        "Protocol": protocol,
                        "Port": str(port),
                        "CidrBlock": source_cidr,
                        "Action": "ACCEPT",
                        "PolicyDescription": "goto-cloudserver-manager",
                    }
                ]
            },
        }
        req.from_json_string(json.dumps(params))
        client.CreateSecurityGroupPolicies(req)
        logger.info("tencent_sg_open_port", sg=security_group_id, port=port, source=source_cidr)
        return True

    def revoke_rule(
        self,
        security_group_id: str,
        port: int,
        protocol: str = "TCP",
        source_cidr: str = "10.0.0.0/8",
        region: str = "",
    ) -> bool:
        region = region or self._default_region
        from tencentcloud.vpc.v20170312 import models as vpc_models
        client = self._get_client(region)
        req = vpc_models.DeleteSecurityGroupPoliciesRequest()
        params = {
            "SecurityGroupId": security_group_id,
            "SecurityGroupPolicySet": {
                "Ingress": [
                    {
                        "Protocol": protocol,
                        "Port": str(port),
                        "CidrBlock": source_cidr,
                        "Action": "ACCEPT",
                    }
                ]
            },
        }
        req.from_json_string(json.dumps(params))
        client.DeleteSecurityGroupPolicies(req)
        logger.info("tencent_sg_rule_revoked", sg=security_group_id, port=port)
        return True
