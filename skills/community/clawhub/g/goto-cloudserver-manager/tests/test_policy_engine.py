"""测试 PolicyEngine 三级权限控制。"""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from core.policy_engine import PolicyEngine, PolicyViolationError, ConfirmationRequiredError

MOCK_POLICIES = """
policies:
  default:
    readonly_allowed:
      - check_server_status
      - generate_report
    confirmation_required:
      - install_database
      - create_database
    forbidden:
      - drop_table
      - delete_database
  test:
    inherits: default
"""


@pytest.fixture
def engine(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "policies.yaml").write_text(MOCK_POLICIES, encoding="utf-8")
    return PolicyEngine(config_dir=config_dir)


def test_readonly_action_passes(engine):
    engine.check("check_server_status", environment="test")  # 不应抛出异常


def test_readonly_generate_report(engine):
    engine.check("generate_report", environment="default")


def test_confirmation_required_raises(engine):
    with pytest.raises(ConfirmationRequiredError) as exc_info:
        engine.check("install_database", environment="test")
    assert exc_info.value.action == "install_database"


def test_forbidden_action_raises(engine):
    with pytest.raises(PolicyViolationError) as exc_info:
        engine.check("drop_table", environment="test")
    assert "禁止" in str(exc_info.value)


def test_forbidden_delete_database(engine):
    with pytest.raises(PolicyViolationError):
        engine.check("delete_database", environment="default")


def test_unknown_action_requires_confirmation(engine):
    with pytest.raises(ConfirmationRequiredError):
        engine.check("some_unknown_action", environment="test")


def test_is_readonly(engine):
    assert engine.is_readonly("check_server_status") is True
    assert engine.is_readonly("install_database") is False


def test_is_forbidden(engine):
    assert engine.is_forbidden("drop_table") is True
    assert engine.is_forbidden("check_server_status") is False


def test_confirmation_error_carries_plan(engine):
    plan = {"server": "test-001", "params": {"database": "mysql"}}
    with pytest.raises(ConfirmationRequiredError) as exc_info:
        engine.check("install_database", environment="test", plan=plan)
    assert exc_info.value.plan["server"] == "test-001"
