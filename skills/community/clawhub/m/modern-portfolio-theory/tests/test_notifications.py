"""Tests for notifications.py — file output, email dispatch, HTML templates."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mpt_portfolio.config import (
    Config,
    EmailConfig,
    NotificationEventsConfig,
    PortfolioConfig,
    RebalancingConfig,
)
from mpt_portfolio.notifications import (
    _build_backtest_complete_email,
    _build_performance_report_email,
    _build_portfolio_created_email,
    _build_rebalance_reminder_email,
    notify_file,
    send_notification,
    notify_portfolio_created,
    notify_backtest_complete,
    notify_rebalance_reminder,
    notify_performance_report,
)


@pytest.fixture
def config_file_only() -> Config:
    return Config(
        portfolio=PortfolioConfig(name="test"),
        notifications=NotificationEventsConfig(method="file"),
        email=EmailConfig(enabled=False),
    )


@pytest.fixture
def config_email_enabled() -> Config:
    return Config(
        portfolio=PortfolioConfig(name="test"),
        notifications=NotificationEventsConfig(method="both"),
        email=EmailConfig(
            enabled=True,
            smtp_host="smtp.test.com",
            smtp_port=587,
            smtp_use_tls=True,
            smtp_user="user@test.com",
            smtp_password="pass",
            sender="sender@test.com",
            recipients=["r@test.com"],
        ),
    )


@pytest.fixture
def sample_quantities() -> dict:
    return {
        "XLK": {"weight": 0.35, "price": 200.0, "exact_shares": 175.0, "whole_shares": 175},
        "GLD": {"weight": 0.25, "price": 180.0, "exact_shares": 138.89, "whole_shares": 138},
    }


class TestNotifyFile:
    def test_creates_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "mpt_portfolio.notifications.get_portfolio_reports_dir",
            lambda name: tmp_path,
        )
        path = notify_file("test", "Test Subject", "Test body")
        assert path.exists()
        content = path.read_text()
        assert "Subject: Test Subject" in content
        assert "Test body" in content


class TestSendNotification:
    def test_file_method_no_email(self, config_file_only, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "mpt_portfolio.notifications.get_portfolio_reports_dir",
            lambda name: tmp_path,
        )
        with patch("mpt_portfolio.notifications.notify_email") as mock_email:
            send_notification("test", config_file_only, "Subj", "<html/>", "plain", None)
            mock_email.assert_not_called()
        assert any(f.name.startswith("notification_") for f in tmp_path.iterdir())

    def test_email_disabled_skips(self, tmp_path, monkeypatch):
        config = Config(
            portfolio=PortfolioConfig(name="test"),
            notifications=NotificationEventsConfig(method="email"),
            email=EmailConfig(enabled=False),
        )
        monkeypatch.setattr(
            "mpt_portfolio.notifications.get_portfolio_reports_dir",
            lambda name: tmp_path,
        )
        with patch("mpt_portfolio.notifications.notify_email") as mock_email:
            send_notification("test", config, "Subj", "<html/>", "plain", None)
            mock_email.assert_not_called()

    @patch("mpt_portfolio.notifications.notify_email", return_value=True)
    def test_both_method(self, mock_email, config_email_enabled, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "mpt_portfolio.notifications.get_portfolio_reports_dir",
            lambda name: tmp_path,
        )
        send_notification("test", config_email_enabled, "Sub", "<h>", "p", None)
        mock_email.assert_called_once()
        assert any(f.name.startswith("notification_") for f in tmp_path.iterdir())


class TestEventToggles:
    def test_portfolio_created_disabled(self, config_file_only):
        config_file_only.notifications.portfolio_created = False
        with patch("mpt_portfolio.notifications.send_notification") as mock:
            notify_portfolio_created(
                "test", config_file_only, "max_sharpe", {}, 0.1, 0.15, 0.8, 0.04, 100000, {},
            )
            mock.assert_not_called()

    def test_backtest_disabled(self, config_file_only):
        config_file_only.notifications.backtest_complete = False
        with patch("mpt_portfolio.notifications.send_notification") as mock:
            notify_backtest_complete("test", config_file_only, "monthly", "reason", {})
            mock.assert_not_called()

    def test_rebalance_disabled(self, config_file_only):
        config_file_only.notifications.rebalance_reminder = False
        with patch("mpt_portfolio.notifications.send_notification") as mock:
            notify_rebalance_reminder("test", config_file_only, True, "drift", 0.08, "XLK", [], 10.0)
            mock.assert_not_called()

    def test_performance_disabled(self, config_file_only):
        config_file_only.notifications.performance_report = False
        with patch("mpt_portfolio.notifications.send_notification") as mock:
            notify_performance_report(
                "test", config_file_only, 110000, 0.10, 0.08, 0.9, 0.095, -0.12, 0.14, 180, 3,
            )
            mock.assert_not_called()


class TestHTMLTemplates:
    def test_portfolio_created_content(self, sample_quantities):
        html, plain = _build_portfolio_created_email(
            "my_port", "max_sharpe", {}, 0.12, 0.15, 0.85, 0.04, 100000, sample_quantities,
        )
        assert "my_port" in html
        assert "max_sharpe" in html
        assert "12.00%" in html
        assert "0.850" in html
        assert "XLK" in html
        assert "my_port" in plain
        assert "XLK" in plain

    def test_backtest_complete_content(self):
        strategies = {
            "monthly": {"total_return": 0.45, "cagr": 0.08, "sharpe": 0.9,
                        "max_drawdown": -0.18, "turnover": 1.2, "costs": 150.0},
            "quarterly": {"total_return": 0.40, "cagr": 0.07, "sharpe": 0.8,
                          "max_drawdown": -0.20, "turnover": 0.8, "costs": 100.0},
        }
        html, plain = _build_backtest_complete_email(
            "my_port", "monthly", "Best risk-adjusted", strategies,
        )
        assert "monthly" in html
        assert "quarterly" in html
        assert "Best risk-adjusted" in html
        assert "monthly" in plain

    def test_rebalance_needed_content(self):
        order = MagicMock()
        order.action = "BUY"
        order.ticker = "XLK"
        order.shares_rounded = 10
        order.dollar_amount = 2000.0
        order.current_weight = 0.30
        order.target_weight = 0.35
        html, plain = _build_rebalance_reminder_email(
            "my_port", True, "Drift exceeded threshold",
            0.08, "XLK", [order], 25.0,
        )
        assert "Rebalance Needed" in html
        assert "XLK" in html
        assert "BUY" in html
        assert "REBALANCE NEEDED" in plain

    def test_rebalance_not_needed(self):
        html, plain = _build_rebalance_reminder_email(
            "my_port", False, "Within threshold", 0.02, "GLD", [], 0.0,
        )
        assert "No Rebalance Needed" in html
        assert "No rebalance needed" in plain

    def test_performance_report_content(self):
        html, plain = _build_performance_report_email(
            "my_port", 125000, 0.25, 0.18, 0.95, 0.22, -0.10, 0.14, 365, 4,
        )
        assert "$125,000.00" in html
        assert "25.00%" in html
        assert "0.950" in html
        assert "$125,000.00" in plain
