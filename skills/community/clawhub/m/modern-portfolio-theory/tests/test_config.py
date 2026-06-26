"""Tests for config.py — validation and loading."""

import pytest
import yaml
from pathlib import Path

from mpt_portfolio.config import (
    Config,
    ConfigValidationError,
    EmailConfig,
    NotificationEventsConfig,
    load_default_config,
    validate_config,
    save_portfolio_config,
    create_portfolio_from_config,
)


class TestValidateConfig:
    def test_default_valid(self):
        raw = load_default_config()
        config = validate_config(raw)
        assert isinstance(config, Config)
        assert len(config.portfolio.assets) == 14

    def test_empty_assets_fails(self):
        raw = load_default_config()
        raw["portfolio"]["assets"] = []
        with pytest.raises(ConfigValidationError, match="non-empty"):
            validate_config(raw)

    def test_negative_investment_fails(self):
        raw = load_default_config()
        raw["portfolio"]["initial_investment"] = -1000
        with pytest.raises(ConfigValidationError, match="positive"):
            validate_config(raw)

    def test_invalid_method_fails(self):
        raw = load_default_config()
        raw["optimization"]["method"] = "invalid"
        with pytest.raises(ConfigValidationError):
            validate_config(raw)

    def test_invalid_price_type_fails(self):
        raw = load_default_config()
        raw["data"]["price_type"] = "invalid"
        with pytest.raises(ConfigValidationError, match="price_type"):
            validate_config(raw)

    def test_max_weight_out_of_range(self):
        raw = load_default_config()
        raw["optimization"]["constraints"]["max_weight"] = 1.5
        with pytest.raises(ConfigValidationError, match="max_weight"):
            validate_config(raw)

    def test_invalid_rebalancing_strategy(self):
        raw = load_default_config()
        raw["backtest"]["rebalancing_strategies"] = ["invalid"]
        with pytest.raises(ConfigValidationError):
            validate_config(raw)


class TestSaveAndLoad:
    def test_round_trip(self, sample_config, tmp_path, monkeypatch):
        monkeypatch.setattr("mpt_portfolio.config.get_portfolios_dir", lambda: tmp_path)
        portfolio_dir = tmp_path / "test"
        portfolio_dir.mkdir()
        path = save_portfolio_config("test", sample_config)
        assert path.exists()
        with open(path) as f:
            raw = yaml.safe_load(f)
        assert raw["portfolio"]["name"] == "test_portfolio"
        assert raw["data"]["price_type"] == "adjusted"


class TestMonitoringConfig:
    def test_default_frequency_is_none(self):
        raw = load_default_config()
        config = validate_config(raw)
        assert config.monitoring.frequency == "none"

    def test_valid_frequencies(self):
        for freq in ("weekly", "monthly", "none"):
            raw = load_default_config()
            raw.setdefault("monitoring", {})["frequency"] = freq
            config = validate_config(raw)
            assert config.monitoring.frequency == freq

    def test_invalid_frequency_fails(self):
        raw = load_default_config()
        raw["monitoring"] = {"frequency": "daily"}
        with pytest.raises(ConfigValidationError, match="monitoring.frequency"):
            validate_config(raw)

    def test_round_trip(self, sample_config, tmp_path, monkeypatch):
        monkeypatch.setattr("mpt_portfolio.config.get_portfolios_dir", lambda: tmp_path)
        sample_config.monitoring.frequency = "weekly"
        portfolio_dir = tmp_path / "test_monitor"
        portfolio_dir.mkdir()
        path = save_portfolio_config("test_monitor", sample_config)
        with open(path) as f:
            raw = yaml.safe_load(f)
        assert raw["monitoring"]["frequency"] == "weekly"


class TestEmailConfig:
    def test_defaults_disabled(self):
        raw = load_default_config()
        config = validate_config(raw)
        assert config.email.enabled is False
        assert config.email.smtp_host is None
        assert config.email.recipients == []

    def test_explicit_email_config(self):
        raw = load_default_config()
        raw["email"] = {
            "enabled": True,
            "smtp_host": "smtp.example.com",
            "smtp_port": 587,
            "smtp_use_tls": True,
            "smtp_user": "user@example.com",
            "smtp_password": "secret",
            "sender": "sender@example.com",
            "recipients": ["a@example.com", "b@example.com"],
        }
        config = validate_config(raw)
        assert config.email.enabled is True
        assert config.email.smtp_host == "smtp.example.com"
        assert config.email.recipients == ["a@example.com", "b@example.com"]

    def test_round_trip(self, sample_config, tmp_path, monkeypatch):
        monkeypatch.setattr("mpt_portfolio.config.get_portfolios_dir", lambda: tmp_path)
        sample_config.email = EmailConfig(
            enabled=True, smtp_host="smtp.test.com", smtp_port=465,
            smtp_use_tls=True, smtp_user="u", smtp_password="p",
            sender="s@test.com", recipients=["r@test.com"],
        )
        portfolio_dir = tmp_path / "test_email"
        portfolio_dir.mkdir()
        path = save_portfolio_config("test_email", sample_config)
        with open(path) as f:
            raw = yaml.safe_load(f)
        assert raw["email"]["enabled"] is True
        assert raw["email"]["smtp_host"] == "smtp.test.com"
        assert raw["email"]["recipients"] == ["r@test.com"]

    def test_email_saved_when_disabled(self, sample_config, tmp_path, monkeypatch):
        monkeypatch.setattr("mpt_portfolio.config.get_portfolios_dir", lambda: tmp_path)
        portfolio_dir = tmp_path / "test_no_email"
        portfolio_dir.mkdir()
        path = save_portfolio_config("test_no_email", sample_config)
        with open(path) as f:
            raw = yaml.safe_load(f)
        assert raw["email"]["enabled"] is False
        assert raw["email"]["smtp_host"] is None


class TestNotificationEventsConfig:
    def test_defaults(self):
        raw = load_default_config()
        config = validate_config(raw)
        assert config.notifications.method == "file"
        assert config.notifications.portfolio_created is True
        assert config.notifications.backtest_complete is True
        assert config.notifications.rebalance_reminder is True
        assert config.notifications.performance_report is True

    def test_invalid_method_fails(self):
        raw = load_default_config()
        raw["notifications"] = {"method": "invalid"}
        with pytest.raises(ConfigValidationError, match="notifications.method"):
            validate_config(raw)

    def test_custom_toggles(self):
        raw = load_default_config()
        raw["notifications"] = {
            "method": "both",
            "portfolio_created": False,
            "performance_report": False,
        }
        config = validate_config(raw)
        assert config.notifications.method == "both"
        assert config.notifications.portfolio_created is False
        assert config.notifications.backtest_complete is True
        assert config.notifications.performance_report is False


class TestBackwardCompatMigration:
    def test_old_notification_email_migrated(self):
        raw = load_default_config()
        raw["rebalancing"] = {
            "strategy": "monthly",
            "notification": {
                "method": "both",
                "email": {
                    "smtp_server": "smtp.old.com",
                    "smtp_port": 587,
                    "username": "old_user",
                    "password": "old_pass",
                    "from_addr": "old@sender.com",
                    "to_addr": "old@recipient.com",
                },
            },
        }
        config = validate_config(raw)
        assert config.email.enabled is True
        assert config.email.smtp_host == "smtp.old.com"
        assert config.email.smtp_user == "old_user"
        assert config.email.smtp_password == "old_pass"
        assert config.email.sender == "old@sender.com"
        assert config.email.recipients == ["old@recipient.com"]
        assert config.notifications.method == "both"

    def test_old_format_does_not_override_new(self):
        raw = load_default_config()
        raw["email"] = {
            "enabled": True,
            "smtp_host": "smtp.new.com",
            "sender": "new@sender.com",
            "recipients": ["new@r.com"],
        }
        raw["rebalancing"] = {
            "strategy": "monthly",
            "notification": {
                "method": "email",
                "email": {"smtp_server": "smtp.old.com"},
            },
        }
        config = validate_config(raw)
        assert config.email.smtp_host == "smtp.new.com"


class TestCreatePortfolio:
    def test_creates_directory(self, sample_config, tmp_path, monkeypatch):
        monkeypatch.setattr("mpt_portfolio.config.get_portfolios_dir", lambda: tmp_path)
        sample_config.portfolio.name = "new_port"
        path = create_portfolio_from_config(sample_config)
        assert path.exists()
        assert (path / "config.yaml").exists()
        assert (path / "reports").is_dir()

    def test_duplicate_fails(self, sample_config, tmp_path, monkeypatch):
        monkeypatch.setattr("mpt_portfolio.config.get_portfolios_dir", lambda: tmp_path)
        sample_config.portfolio.name = "dup"
        create_portfolio_from_config(sample_config)
        with pytest.raises(FileExistsError):
            create_portfolio_from_config(sample_config)
