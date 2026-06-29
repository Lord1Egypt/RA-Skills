"""测试各云厂商安全组规则管理：公网开放校验 + 正常请求构造（mock 掉云厂商 SDK）。"""

import sys
import types

import pytest


def _register_fake_module(monkeypatch, name: str, **attrs):
    mod = types.ModuleType(name)
    for k, v in attrs.items():
        setattr(mod, k, v)
    monkeypatch.setitem(sys.modules, name, mod)
    return mod


# ── 阿里云 ───────────────────────────────────────────────────────────────────

from providers.aliyun.security_group import AliyunSecurityGroup


def test_aliyun_rejects_public_cidr():
    sg = AliyunSecurityGroup("ak", "sk")
    with pytest.raises(ValueError, match="公网"):
        sg.open_port_for_internal("sg-1", 1433, source_cidr="0.0.0.0/0")


def test_aliyun_opens_internal_port(monkeypatch):
    from unittest.mock import MagicMock

    fake_client_cls = MagicMock()
    client_instance = fake_client_cls.return_value

    _register_fake_module(monkeypatch, "alibabacloud_ecs20140526")
    _register_fake_module(monkeypatch, "alibabacloud_ecs20140526.client", Client=fake_client_cls)
    _register_fake_module(monkeypatch, "alibabacloud_ecs20140526.models", AuthorizeSecurityGroupRequest=MagicMock())
    _register_fake_module(monkeypatch, "alibabacloud_tea_openapi")
    _register_fake_module(monkeypatch, "alibabacloud_tea_openapi.models", Config=MagicMock())

    sg = AliyunSecurityGroup("ak", "sk")
    result = sg.open_port_for_internal("sg-1", 1433, source_cidr="10.0.0.0/8")

    assert result is True
    client_instance.authorize_security_group.assert_called_once()


# ── 腾讯云 ───────────────────────────────────────────────────────────────────

from providers.tencent.security_group import TencentSecurityGroup


def test_tencent_rejects_public_cidr():
    sg = TencentSecurityGroup("id", "key")
    with pytest.raises(ValueError, match="公网"):
        sg.open_port_for_internal("sg-1", 1433, source_cidr="0.0.0.0/0")


def test_tencent_opens_internal_port(monkeypatch):
    from unittest.mock import MagicMock

    credential_mock = MagicMock()
    vpc_client_factory = MagicMock()
    client_instance = vpc_client_factory.VpcClient.return_value
    models_mock = MagicMock()

    _register_fake_module(monkeypatch, "tencentcloud")
    _register_fake_module(monkeypatch, "tencentcloud.common", credential=credential_mock)
    _register_fake_module(monkeypatch, "tencentcloud.vpc")
    _register_fake_module(
        monkeypatch, "tencentcloud.vpc.v20170312",
        vpc_client=vpc_client_factory, models=models_mock,
    )

    sg = TencentSecurityGroup("id", "key")
    result = sg.open_port_for_internal("sg-1", 1433, source_cidr="10.0.0.0/8")

    assert result is True
    client_instance.CreateSecurityGroupPolicies.assert_called_once()


# ── 华为云 ───────────────────────────────────────────────────────────────────

from providers.huawei.security_group import HuaweiSecurityGroup


def test_huawei_rejects_public_cidr():
    sg = HuaweiSecurityGroup("ak", "sk", "project-1")
    with pytest.raises(ValueError, match="公网"):
        sg.open_port_for_internal("sg-1", 1433, source_cidr="0.0.0.0/0")


def test_huawei_opens_internal_port(monkeypatch):
    from unittest.mock import MagicMock

    basic_credentials_mock = MagicMock()
    vpc_client_cls = MagicMock()
    client_instance = (
        vpc_client_cls.new_builder.return_value
        .with_credentials.return_value
        .with_region.return_value
        .build.return_value
    )
    model_mock = MagicMock()
    vpc_region_mock = MagicMock()

    _register_fake_module(monkeypatch, "huaweicloudsdkcore")
    _register_fake_module(monkeypatch, "huaweicloudsdkcore.auth")
    _register_fake_module(
        monkeypatch, "huaweicloudsdkcore.auth.credentials",
        BasicCredentials=basic_credentials_mock,
    )
    _register_fake_module(monkeypatch, "huaweicloudsdkvpc")
    _register_fake_module(
        monkeypatch, "huaweicloudsdkvpc.v3",
        VpcClient=vpc_client_cls, model=model_mock,
    )
    _register_fake_module(monkeypatch, "huaweicloudsdkvpc.v3.region")
    _register_fake_module(
        monkeypatch, "huaweicloudsdkvpc.v3.region.vpc_region",
        VpcRegion=vpc_region_mock,
    )

    sg = HuaweiSecurityGroup("ak", "sk", "project-1")
    result = sg.open_port_for_internal("sg-1", 1433, source_cidr="10.0.0.0/8")

    assert result is True
    client_instance.create_security_group_rule.assert_called_once()
