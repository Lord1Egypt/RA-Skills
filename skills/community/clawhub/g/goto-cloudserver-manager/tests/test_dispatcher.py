"""测试 CloudServerManagerDispatcher 路由分发和策略集成。"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from core.dispatcher import CloudServerManagerDispatcher, ActionResult
from core.policy_engine import PolicyViolationError, ConfirmationRequiredError


MOCK_SERVER_YAML = """
servers:
  - id: mock-win-001
    name: Mock Windows Server
    provider: aliyun
    region: cn-hangzhou
    instance_id: i-mock123
    os_type: windows
    os_version: windows-server-2022
    connection:
      type: cloud_assistant
      fallback: winrm
    environment: test
  - id: mock-linux-001
    name: Mock Linux Server
    provider: aliyun
    region: cn-hangzhou
    instance_id: i-mock456
    os_type: linux
    os_version: ubuntu-22.04
    connection:
      type: cloud_assistant
      fallback: ssh
    environment: test
"""

MOCK_POLICIES_YAML = """
policies:
  default:
    readonly_allowed:
      - check_server_status
    confirmation_required:
      - install_database
    forbidden:
      - drop_table
  test:
    inherits: default
"""

MOCK_PROVIDERS_YAML = """
providers:
  aliyun:
    command_channel: cloud_assistant
    poll_interval_seconds: 5
    max_poll_attempts: 10
    auth:
      access_key_id: fake_ak
      access_key_secret: fake_sk
"""


@pytest.fixture
def dispatcher(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "servers.yaml").write_text(MOCK_SERVER_YAML, encoding="utf-8")
    (config_dir / "policies.yaml").write_text(MOCK_POLICIES_YAML, encoding="utf-8")
    (config_dir / "providers.yaml").write_text(MOCK_PROVIDERS_YAML, encoding="utf-8")

    from core.config_loader import ConfigLoader
    from core.policy_engine import PolicyEngine
    config = ConfigLoader(config_dir=config_dir)
    config.load()
    policy = PolicyEngine(config_dir=config_dir)
    return CloudServerManagerDispatcher(config_loader=config, policy_engine=policy)


def test_forbidden_action_returns_failure(dispatcher):
    result = dispatcher.dispatch("mock-win-001", "drop_table")
    assert result.success is False
    assert "禁止" in result.error


def test_confirmation_required_without_confirmed_returns_failure(dispatcher):
    result = dispatcher.dispatch("mock-win-001", "install_database")
    assert result.success is False
    assert result.data.get("requires_confirmation") is True


def test_confirmation_required_with_confirmed_executes(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")

    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        with patch.object(dispatcher, "_install_database",
                          return_value=ActionResult(success=True, action="install_database", server_id="mock-win-001")):
            result = dispatcher.dispatch("mock-win-001", "install_database", confirmed=True)
    assert result.success is True


def test_unknown_server_raises(dispatcher):
    with pytest.raises(KeyError):
        dispatcher.dispatch("nonexistent-server", "check_server_status")


def test_action_result_bool(dispatcher):
    ok = ActionResult(success=True, action="test", server_id="mock")
    fail = ActionResult(success=False, action="test", server_id="mock")
    assert bool(ok) is True
    assert bool(fail) is False


# ── 新增 action 路由 ─────────────────────────────────────────────────────────

def test_list_instances_uses_provider_not_executor(dispatcher):
    from providers.base import ServerInstance

    mock_provider = MagicMock()
    mock_provider.list_instances.return_value = [
        ServerInstance(instance_id="i-1", name="srv-1", status="running", os_type="windows"),
    ]

    with patch.object(dispatcher, "_get_provider", return_value=mock_provider) as get_provider:
        with patch.object(dispatcher, "_get_executor") as get_executor:
            result = dispatcher.dispatch("mock-win-001", "list_instances", confirmed=True)

    get_provider.assert_called_once()
    get_executor.assert_not_called()
    assert result.success is True
    assert result.data["instances"][0]["instance_id"] == "i-1"


def test_modify_security_group_auto_resolves_sg_id(dispatcher):
    mock_provider = MagicMock()
    mock_provider.describe_security_groups.return_value = [{"id": "sg-1", "name": "default"}]
    mock_provider.update_security_group_rule.return_value = True

    with patch.object(dispatcher, "_get_provider", return_value=mock_provider):
        result = dispatcher.dispatch(
            "mock-win-001", "modify_security_group", params={"port": 1433}, confirmed=True,
        )

    assert result.success is True
    mock_provider.update_security_group_rule.assert_called_once()
    assert mock_provider.update_security_group_rule.call_args.kwargs["security_group_id"] == "sg-1"


def test_modify_security_group_missing_port_fails(dispatcher):
    mock_provider = MagicMock()
    with patch.object(dispatcher, "_get_provider", return_value=mock_provider):
        result = dispatcher.dispatch("mock-win-001", "modify_security_group", params={}, confirmed=True)
    assert result.success is False


def test_reboot_instance(dispatcher):
    mock_provider = MagicMock()
    mock_provider.reboot_instance.return_value = True
    with patch.object(dispatcher, "_get_provider", return_value=mock_provider):
        result = dispatcher.dispatch("mock-win-001", "reboot_instance", confirmed=True)
    assert result.success is True


def test_configure_firewall(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "configure_firewall",
            params={"open_ports": [1433], "source_cidr": "10.0.0.0/8"}, confirmed=True,
        )
    assert result.success is True
    mock_executor.execute.assert_called_once()


def test_configure_firewall_missing_ports_fails(dispatcher):
    mock_executor = MagicMock()
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "configure_firewall", params={}, confirmed=True)
    assert result.success is False


def test_install_monitoring_agent(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "install_monitoring_agent", confirmed=True)
    assert result.success is True


def test_create_user_renders_template(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute_sql.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "create_user",
            params={"database": "gotoplan", "username": "app_user", "password": "Secret123!"},
            confirmed=True,
        )
    assert result.success is True
    db_type, sql = mock_executor.execute_sql.call_args.args
    assert db_type == "sqlserver"
    assert "app_user" in sql


def test_create_user_missing_username_fails(dispatcher):
    mock_executor = MagicMock()
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "create_user", params={"database": "gotoplan"}, confirmed=True)
    assert result.success is False


def test_seed_data_builds_insert(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute_sql.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "seed_data",
            params={"table": "Roles", "rows": [{"Name": "admin"}]},
            confirmed=True,
        )
    assert result.success is True
    db_type, sql = mock_executor.execute_sql.call_args.args
    assert "INSERT INTO" in sql
    assert "Roles" in sql


def test_seed_data_missing_rows_fails(dispatcher):
    mock_executor = MagicMock()
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "seed_data", params={"table": "Roles"}, confirmed=True)
    assert result.success is False


def test_restore_database_requires_source(dispatcher):
    mock_executor = MagicMock()
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "restore_database", params={"name": "gotoplan"}, confirmed=True)
    assert result.success is False
    assert "source" in result.error


def test_restore_database_executes(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "restore_database",
            params={"name": "gotoplan", "source": "C:\\Backup\\gotoplan.bak"},
            confirmed=True,
        )
    assert result.success is True


def test_get_provider_unknown_provider_raises(dispatcher):
    server = dispatcher._config.get_server("mock-win-001")
    server.provider = "unknown_cloud"
    with pytest.raises(ValueError):
        dispatcher._get_provider(server)


# ── 补齐的残留 action（check_network/create_index/configure_winrm/别名）─────────

def test_check_network_routes_to_check_server(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="net ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "check_network", confirmed=True)
    assert result.success is True
    assert result.action == "check_network"


def test_check_database_connections_routes_to_health_check(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute_sql.return_value = MagicMock(exit_code=0, stdout="conns ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "check_database_connections", confirmed=True)
    assert result.success is True


def test_create_index_builds_sql(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute_sql.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "create_index",
            params={"table": "Users", "columns": ["Mobile"]},
            confirmed=True,
        )
    assert result.success is True
    assert "CREATE INDEX" in result.output
    assert "Mobile" in result.output


def test_create_index_missing_columns_fails(dispatcher):
    mock_executor = MagicMock()
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "create_index", params={"table": "Users"}, confirmed=True)
    assert result.success is False


def test_configure_winrm_on_windows(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "configure_winrm", confirmed=True)
    assert result.success is True


def test_modify_firewall_alias_routes_to_configure_firewall(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "modify_firewall", params={"open_ports": [1433]}, confirmed=True,
        )
    assert result.success is True
    assert result.action == "configure_firewall"


def test_install_windows_exporter_alias_routes_to_monitoring_agent(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "install_windows_exporter", confirmed=True)
    assert result.success is True
    assert result.action == "install_monitoring_agent"


# ── SSH/WinRM 直连缺失 IP 时应自动查云厂商 API 补全 ────────────────────────────

def test_winrm_executor_auto_fetches_missing_ip(dispatcher):
    from executor.winrm_executor import WinRMExecutor
    from providers.base import ServerInstance

    mock_executor = MagicMock(spec=WinRMExecutor)
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    mock_provider = MagicMock()
    mock_provider.get_instance.return_value = ServerInstance(
        instance_id="i-mock123", name="mock", status="running", os_type="windows",
        public_ip="9.9.9.9", private_ip="10.0.0.9",
    )

    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        with patch.object(dispatcher, "_get_provider", return_value=mock_provider):
            result = dispatcher.dispatch("mock-win-001", "check_server_status", confirmed=True)

    assert result.success is True
    mock_provider.get_instance.assert_called_once_with("i-mock123", "cn-hangzhou")
    connected_server = mock_executor.connect.call_args.args[0]
    assert connected_server.public_ip == "9.9.9.9"
    assert connected_server.private_ip == "10.0.0.9"


def test_winrm_executor_skips_lookup_when_ip_already_set(dispatcher):
    from executor.winrm_executor import WinRMExecutor

    server = dispatcher._config.get_server("mock-win-001")
    dispatcher._config._servers["mock-win-001"] = server.model_copy(update={"public_ip": "1.1.1.1"})

    mock_executor = MagicMock(spec=WinRMExecutor)
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    mock_provider = MagicMock()

    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        with patch.object(dispatcher, "_get_provider", return_value=mock_provider):
            result = dispatcher.dispatch("mock-win-001", "check_server_status", confirmed=True)

    assert result.success is True
    mock_provider.get_instance.assert_not_called()
    connected_server = mock_executor.connect.call_args.args[0]
    assert connected_server.public_ip == "1.1.1.1"


def test_cloud_assistant_executor_never_triggers_ip_lookup(dispatcher):
    # 普通 MagicMock() 不是 SSHExecutor/WinRMExecutor 实例，模拟 cloud_assistant/TAT 通道
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    mock_provider = MagicMock()

    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        with patch.object(dispatcher, "_get_provider", return_value=mock_provider):
            result = dispatcher.dispatch("mock-win-001", "check_server_status", confirmed=True)

    assert result.success is True
    mock_provider.get_instance.assert_not_called()


# ── 脚本必须先上传到目标机再执行，不能把本机路径拼进远端命令 ──────────────────

def test_check_server_uploads_script_to_windows_temp_before_execute(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-win-001", "check_server_status", confirmed=True)

    assert result.success is True
    mock_executor.upload_file.assert_called_once()
    local_path, remote_path = mock_executor.upload_file.call_args.args
    assert local_path.endswith("check_server.ps1")
    assert remote_path == "C:\\Windows\\Temp\\check_server.ps1"

    cmd = mock_executor.execute.call_args.args[0]
    assert remote_path in cmd
    assert local_path not in cmd


def test_check_server_uploads_script_to_linux_tmp_before_execute(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch("mock-linux-001", "check_server_status", confirmed=True)

    assert result.success is True
    local_path, remote_path = mock_executor.upload_file.call_args.args
    assert local_path.endswith("check_server.sh")
    assert remote_path == "/tmp/check_server.sh"

    cmd = mock_executor.execute.call_args.args[0]
    assert remote_path in cmd
    assert local_path not in cmd


def test_install_database_uploads_script_before_execute(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "install_database", params={"database": "sqlserver"}, confirmed=True,
        )
    assert result.success is True
    remote_path = mock_executor.upload_file.call_args.args[1]
    assert remote_path == "C:\\Windows\\Temp\\install.ps1"
    assert remote_path in mock_executor.execute.call_args.args[0]


def test_backup_database_uploads_script_and_keeps_params_in_command(dispatcher):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = MagicMock(exit_code=0, stdout="ok", stderr="")
    with patch.object(dispatcher, "_get_executor", return_value=mock_executor):
        result = dispatcher.dispatch(
            "mock-win-001", "backup_database",
            params={"name": "gotoplan", "dest": "C:\\Backup"}, confirmed=True,
        )
    assert result.success is True
    remote_path = mock_executor.upload_file.call_args.args[1]
    assert remote_path == "C:\\Windows\\Temp\\backup.ps1"
    cmd = mock_executor.execute.call_args.args[0]
    assert remote_path in cmd
    assert "gotoplan" in cmd
