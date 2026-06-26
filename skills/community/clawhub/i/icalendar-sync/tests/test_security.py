#!/usr/bin/env python3
"""
Security-focused tests for iCalendar Sync.
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from unittest.mock import patch
from keyring.errors import KeyringError
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from icalendar_sync.calendar import CalendarManager, cmd_setup, validate_secret_value, build_manager


@pytest.fixture(autouse=True)
def isolate_config_path(tmp_path, monkeypatch):
    """Prevent tests from using user-level config credentials."""
    monkeypatch.setenv("ICALENDAR_SYNC_CONFIG", str(tmp_path / "test-icalendar-sync.yaml"))


def test_validate_secret_value_rejects_control_chars():
    assert validate_secret_value("xxxx-xxxx-xxxx-xxxx")
    assert not validate_secret_value("xxxx-xxxx\n-xxxx-xxxx")
    assert not validate_secret_value("xxxx-xxxx\r-xxxx-xxxx")
    assert not validate_secret_value("xxxx-\x00xxx-xxxx-xxxx")


def test_setup_non_interactive_requires_env_vars():
    args = argparse.Namespace(username=None, non_interactive=True, storage="keyring", config=None)

    with patch.dict(os.environ, {}, clear=True):
        with patch("icalendar_sync.calendar.keyring.set_password") as mock_set_password:
            cmd_setup(args)
            mock_set_password.assert_not_called()


def test_setup_non_interactive_saves_to_keyring():
    args = argparse.Namespace(username=None, non_interactive=True, storage="keyring", config=None)

    with patch.dict(
        os.environ,
        {"ICLOUD_USERNAME": "test@icloud.com", "ICLOUD_APP_PASSWORD": "xxxx-xxxx-xxxx-xxxx"},
        clear=True,
    ):
        with patch("icalendar_sync.calendar.keyring.set_password") as mock_set_password:
            cmd_setup(args)
            mock_set_password.assert_called_once_with(
                "openclaw-icalendar",
                "test@icloud.com",
                "xxxx-xxxx-xxxx-xxxx",
            )


def test_setup_keyring_error_does_not_write_plaintext_file():
    args = argparse.Namespace(username=None, non_interactive=True, storage="keyring", config=None)

    with patch.dict(
        os.environ,
        {"ICLOUD_USERNAME": "test@icloud.com", "ICLOUD_APP_PASSWORD": "xxxx-xxxx-xxxx-xxxx"},
        clear=True,
    ):
        with patch(
            "icalendar_sync.calendar.keyring.set_password",
            side_effect=KeyringError("keyring unavailable"),
        ):
            with patch("builtins.open") as mock_open:
                cmd_setup(args)
                mock_open.assert_not_called()


def test_setup_non_interactive_saves_to_config_file(tmp_path):
    config_path = tmp_path / "credentials.yaml"
    args = argparse.Namespace(
        username=None,
        non_interactive=True,
        storage="file",
        config=str(config_path),
    )

    with patch.dict(
        os.environ,
        {"ICLOUD_USERNAME": "test@icloud.com", "ICLOUD_APP_PASSWORD": "xxxx-xxxx-xxxx-xxxx"},
        clear=True,
    ):
        with patch("icalendar_sync.calendar.keyring.set_password") as mock_set_password:
            cmd_setup(args)
            mock_set_password.assert_not_called()

    assert config_path.exists()
    text = config_path.read_text(encoding="utf-8")
    assert "test@icloud.com" in text
    assert "app_password" in text


def test_manager_reads_credentials_from_config_file(tmp_path):
    config_path = tmp_path / "credentials.yaml"
    config_path.write_text(
        "username: cfg@icloud.com\napp_password: xxxx-xxxx-xxxx-xxxx\n",
        encoding="utf-8",
    )

    with patch.dict(os.environ, {}, clear=True):
        with patch("icalendar_sync.calendar.keyring.get_password", return_value=None):
            manager = CalendarManager(config_path=str(config_path))
            assert manager.username == "cfg@icloud.com"
            assert manager.password == "xxxx-xxxx-xxxx-xxxx"


def test_manager_file_credential_source_skips_keyring(tmp_path):
    config_path = tmp_path / "credentials.yaml"
    config_path.write_text(
        "username: cfg@icloud.com\napp_password: xxxx-xxxx-xxxx-xxxx\n",
        encoding="utf-8",
    )

    with patch.dict(os.environ, {}, clear=True):
        with patch("icalendar_sync.calendar.keyring.get_password") as mock_get_password:
            manager = CalendarManager(config_path=str(config_path), credential_source="file")
            assert manager.username == "cfg@icloud.com"
            assert manager.password == "xxxx-xxxx-xxxx-xxxx"
            mock_get_password.assert_not_called()


def test_build_manager_uses_file_source_when_config_explicit():
    args = argparse.Namespace(
        provider="caldav",
        storage=None,
        config="/tmp/credentials.yaml",
        user_agent=None,
        debug_http=False,
        ignore_keyring=False,
    )
    with patch("icalendar_sync.calendar.CalendarManager") as mock_manager_cls:
        build_manager(args)
        assert mock_manager_cls.call_args.kwargs["credential_source"] == "file"


def test_build_manager_auto_uses_caldav_on_macos():
    args = argparse.Namespace(
        provider="auto",
        storage=None,
        config=None,
        user_agent=None,
        debug_http=False,
        ignore_keyring=False,
    )
    with patch("icalendar_sync.calendar.sys.platform", "darwin"):
        with patch("icalendar_sync.calendar.CalendarManager") as mock_manager_cls:
            build_manager(args)
            mock_manager_cls.assert_called_once()


def test_build_manager_respects_explicit_storage_over_config():
    args = argparse.Namespace(
        provider="caldav",
        storage="env",
        config="/tmp/credentials.yaml",
        user_agent=None,
        debug_http=False,
        ignore_keyring=False,
    )
    with patch("icalendar_sync.calendar.CalendarManager") as mock_manager_cls:
        build_manager(args)
        assert mock_manager_cls.call_args.kwargs["credential_source"] == "env"


def test_update_validation_rejects_invalid_time_range():
    manager = CalendarManager()
    start = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    end = datetime(2026, 1, 1, 11, 0, tzinfo=timezone.utc)
    event = {"DTSTART": start, "DTEND": end}

    assert manager._validate_event_time_range(event) is False
