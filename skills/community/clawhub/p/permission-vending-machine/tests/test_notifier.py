"""Tests for notifier.py."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from pvm.channels.base import NotificationResult
from pvm.notifier import Notifier


@pytest.fixture
def config_file(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text("""
vault:
  db_path: "./grants.db"
  default_ttl_minutes: 30
  max_ttl_minutes: 480
channels:
  sendblue:
    enabled: true
    api_key: "fake-key"
    from_number: "+17870000000"
    approver_numbers:
      - "+1234567890"
  discord:
    enabled: true
    webhook_url: "https://discord.com/api/webhooks/fake"
  email:
    enabled: false
  telegram:
    enabled: false
  slack:
    enabled: false
""")
    return str(cfg)


class TestNotifierInit:
    def test_loads_enabled_channels(self, config_file):
        notifier = Notifier(config_file)
        assert "sendblue" in notifier.enabled_channels
        assert "discord" in notifier.enabled_channels

    def test_skips_disabled_channels(self, config_file):
        notifier = Notifier(config_file)
        assert "email" not in notifier.enabled_channels
        assert "telegram" not in notifier.enabled_channels
        assert "slack" not in notifier.enabled_channels

    def test_missing_config_raises(self):
        with pytest.raises(FileNotFoundError):
            Notifier("/nonexistent/config.yaml")


class TestNotifierMulticast:
    @patch("pvm.notifier.SendblueChannel")
    @patch("pvm.notifier.DiscordChannel")
    def test_notifies_all_enabled_channels(self, mock_discord, mock_sendblue, config_file):
        mock_sendblue_instance = MagicMock()
        mock_sendblue_instance.send.return_value = NotificationResult(
            channel="sendblue", success=True, message="test"
        )
        mock_sendblue.return_value = mock_sendblue_instance

        mock_discord_instance = MagicMock()
        mock_discord_instance.send.return_value = NotificationResult(
            channel="discord", success=True, message="test"
        )
        mock_discord.return_value = mock_discord_instance

        notifier = Notifier(config_file)
        results = notifier.notify_approvers(
            message="please approve",
            approval_token="tok_123",
            agent_id="coder",
            scope="/tmp/test",
            reason="testing",
            ttl_minutes=5,
        )

        assert mock_sendblue_instance.send.called
        assert mock_discord_instance.send.called
        assert len(results) == 2
        assert results["sendblue"].success is True
        assert results["discord"].success is True

    @patch("pvm.notifier.SendblueChannel")
    @patch("pvm.notifier.DiscordChannel")
    def test_partial_failure_continues(self, mock_discord, mock_sendblue, config_file):
        # First sendblue succeeds, second (discord) fails
        mock_sb = MagicMock()
        mock_sb.send.return_value = NotificationResult(
            channel="sendblue", success=True, message="ok"
        )
        mock_sendblue.return_value = mock_sb

        mock_dc = MagicMock()
        mock_dc.send.side_effect = Exception("network error")
        mock_discord.return_value = mock_dc

        notifier = Notifier(config_file)
        results = notifier.notify_approvers(
            message="test",
            approval_token="tok_123",
        )

        assert "sendblue" in results
        assert results["sendblue"].success is True
        assert "discord" in results
        assert results["discord"].success is False
        assert "network error" in results["discord"].error


class TestNotifierEnvSubstitution:
    def test_substitutes_env_vars(self, tmp_path, monkeypatch):
        monkeypatch.setenv("TEST_API_KEY", "secret123")
        cfg = tmp_path / "config.yaml"
        cfg.write_text("""
vault:
  db_path: "./grants.db"
channels:
  sendblue:
    enabled: true
    api_key: "${TEST_API_KEY}"
    from_number: "+17870000000"
    approver_numbers:
      - "+1234567890"
  discord:
    enabled: false
  email:
    enabled: false
  telegram:
    enabled: false
  slack:
    enabled: false
""")
        notifier = Notifier(str(cfg))
        # Would need mock to verify the actual key, but at least it loads
        assert "sendblue" in notifier.enabled_channels

    def test_missing_env_var_empty(self, tmp_path, monkeypatch):
        monkeypatch.delenv("NONEXISTENT_VAR", raising=False)
        cfg = tmp_path / "config.yaml"
        cfg.write_text("""
vault:
  db_path: "./grants.db"
channels:
  sendblue:
    enabled: true
    api_key: "${NONEXISTENT_VAR}"
    from_number: "+17870000000"
    approver_numbers:
      - "+1234567890"
  discord:
    enabled: false
  email:
    enabled: false
  telegram:
    enabled: false
  slack:
    enabled: false
""")
        # Should load with empty string key, not crash
        notifier = Notifier(str(cfg))
        assert "sendblue" in notifier.enabled_channels
