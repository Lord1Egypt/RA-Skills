"""测试 ConfigLoader 服务器配置加载和环境变量展开。"""

import os
import pytest
from pathlib import Path
from core.config_loader import ConfigLoader


SAMPLE_SERVERS_YAML = """
servers:
  - id: test-win-001
    name: 测试 Windows 服务器
    provider: aliyun
    region: cn-hangzhou
    instance_id: i-test123
    os_type: windows
    os_version: windows-server-2022
    connection:
      type: cloud_assistant
      fallback: winrm
    role:
      - database
    environment: test

  - id: test-linux-001
    name: 测试 Linux 服务器
    provider: tencent
    region: ap-guangzhou
    instance_id: ins-test456
    os_type: linux
    os_version: ubuntu-22.04
    connection:
      type: tat
      fallback: ssh
    role:
      - app
    environment: prod
"""

SAMPLE_PROVIDERS_YAML = """
providers:
  aliyun:
    name: 阿里云
    auth:
      type: access_key
      access_key_id: test_ak_id
      access_key_secret: test_ak_secret
  tencent:
    name: 腾讯云
    auth:
      type: secret_key
      secret_id: test_secret_id
      secret_key: test_secret_key
"""


@pytest.fixture
def config_loader(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "servers.yaml").write_text(SAMPLE_SERVERS_YAML, encoding="utf-8")
    (config_dir / "providers.yaml").write_text(SAMPLE_PROVIDERS_YAML, encoding="utf-8")
    loader = ConfigLoader(config_dir=config_dir)
    loader.load()
    return loader


def test_loads_windows_server(config_loader):
    server = config_loader.get_server("test-win-001")
    assert server.name == "测试 Windows 服务器"
    assert server.provider == "aliyun"
    assert server.os_type == "windows"


def test_loads_linux_server(config_loader):
    server = config_loader.get_server("test-linux-001")
    assert server.os_type == "linux"
    assert server.environment == "prod"


def test_unknown_server_raises(config_loader):
    with pytest.raises(KeyError):
        config_loader.get_server("nonexistent-server")


def test_list_servers_filter_by_environment(config_loader):
    test_servers = config_loader.list_servers(environment="test")
    assert len(test_servers) == 1
    assert test_servers[0].id == "test-win-001"


def test_list_servers_filter_by_provider(config_loader):
    aliyun_servers = config_loader.list_servers(provider="aliyun")
    assert all(s.provider == "aliyun" for s in aliyun_servers)


def test_get_provider_config(config_loader):
    cfg = config_loader.get_provider_config("aliyun")
    assert cfg["name"] == "阿里云"


def test_server_defaults_to_empty_ip_fields(config_loader):
    server = config_loader.get_server("test-win-001")
    assert server.public_ip == ""
    assert server.private_ip == ""


def test_server_loads_manual_ip_override(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "servers.yaml").write_text(SAMPLE_SERVERS_YAML.replace(
        "environment: test\n",
        "environment: test\n    public_ip: \"1.2.3.4\"\n    private_ip: \"10.0.0.5\"\n",
        1,
    ), encoding="utf-8")
    (config_dir / "providers.yaml").write_text(SAMPLE_PROVIDERS_YAML, encoding="utf-8")
    loader = ConfigLoader(config_dir=config_dir)
    loader.load()
    server = loader.get_server("test-win-001")
    assert server.public_ip == "1.2.3.4"
    assert server.private_ip == "10.0.0.5"


def test_env_var_expansion(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_AK_ID", "actual_key_id")
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "servers.yaml").write_text(SAMPLE_SERVERS_YAML, encoding="utf-8")
    (config_dir / "providers.yaml").write_text("""
providers:
  aliyun:
    auth:
      access_key_id: ${TEST_AK_ID}
""", encoding="utf-8")
    loader = ConfigLoader(config_dir=config_dir)
    loader.load()
    cfg = loader.get_provider_config("aliyun")
    assert cfg["auth"]["access_key_id"] == "actual_key_id"
