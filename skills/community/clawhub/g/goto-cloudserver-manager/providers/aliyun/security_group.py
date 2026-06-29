"""阿里云安全组规则管理。"""

from __future__ import annotations

import structlog

logger = structlog.get_logger(__name__)

# 数据库端口白名单（只允许内网 CIDR，绝不对 0.0.0.0/0 开放）
_DB_SAFE_SOURCES = {"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}


class AliyunSecurityGroup:
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

    def list_rules(self, security_group_id: str, region: str = "") -> list[dict]:
        region = region or self._default_region
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.DescribeSecurityGroupAttributeRequest(
            region_id=region,
            security_group_id=security_group_id,
        )
        response = client.describe_security_group_attribute(request)
        rules = []
        for r in (response.body.permissions.permission or []):
            rules.append({
                "direction": r.direction,
                "protocol": r.ip_protocol,
                "port_range": r.port_range,
                "source": r.source_cidr_ip or r.source_group_id or "",
                "policy": r.policy,
                "priority": r.priority,
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
            raise ValueError(
                f"安全策略禁止将端口 {port} 对公网 0.0.0.0/0 开放。"
                "请指定内网 CIDR（如 10.0.0.0/8）。"
            )
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
            priority="1",
        )
        client.authorize_security_group(request)
        logger.info("aliyun_sg_port_opened", sg=security_group_id, port=port, source=source_cidr)
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
        from alibabacloud_ecs20140526 import models as ecs_models
        client = self._get_client(region)
        request = ecs_models.RevokeSecurityGroupRequest(
            region_id=region,
            security_group_id=security_group_id,
            ip_protocol=protocol,
            port_range=f"{port}/{port}",
            source_cidr_ip=source_cidr,
        )
        client.revoke_security_group(request)
        logger.info("aliyun_sg_rule_revoked", sg=security_group_id, port=port)
        return True
