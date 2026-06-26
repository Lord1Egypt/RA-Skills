#!/usr/bin/env python3
"""
Contract tests for the Exchange module in NextLink.
These tests validate the current public structure and utility behavior,
not legacy import paths or obsolete API assumptions.
"""

import os
import sys
import subprocess
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCHANGE_MODULE_DIR = os.path.join(PROJECT_ROOT, "modules", "exchange")
sys.path.insert(0, EXCHANGE_MODULE_DIR)


class TestUtils(unittest.TestCase):
    """Tests for currently supported utility helpers."""

    def test_out_function_exists(self):
        from utils import out

        self.assertTrue(callable(out))

    def test_die_function_exists(self):
        from utils import die

        self.assertTrue(callable(die))

    def test_parse_datetime_iso(self):
        from utils import parse_datetime

        result = parse_datetime("2024-01-15T10:30:00")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 15)

    def test_parse_datetime_date(self):
        from utils import parse_datetime

        result = parse_datetime("2024-01-15")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 15)


class TestConfirmOrDie(unittest.TestCase):
    """Tests for the confirm_or_die safety helper."""

    def test_auto_approve_per_command_bypasses(self):
        """When auto_approved=True kwarg is passed, confirm_or_die returns immediately."""
        from utils import confirm_or_die

        # Should not raise or exit when auto_approved is True
        confirm_or_die("Delete everything", auto_approved=True)

    @patch("sys.stdin")
    def test_non_tty_exits_with_json_error(self, mock_stdin):
        """When stdin is not a TTY and no auto-approve, exits with code 2."""
        from utils import confirm_or_die

        mock_stdin.isatty.return_value = False

        with self.assertRaises(SystemExit) as cm:
            confirm_or_die("Delete file.txt")

        self.assertEqual(cm.exception.code, 2)

    @patch("sys.stdin")
    @patch("builtins.input", return_value="y")
    def test_tty_yes_allows(self, mock_input, mock_stdin):
        """When stdin is TTY and user types 'y', returns without error."""
        from utils import confirm_or_die

        mock_stdin.isatty.return_value = True

        # Should return normally
        confirm_or_die("Delete file.txt")

    @patch("sys.stdin")
    @patch("builtins.input", return_value="n")
    def test_tty_no_aborts(self, mock_input, mock_stdin):
        """When stdin is TTY and user types 'n', exits with code 2."""
        from utils import confirm_or_die

        mock_stdin.isatty.return_value = True

        with self.assertRaises(SystemExit) as cm:
            confirm_or_die("Delete file.txt")

        self.assertEqual(cm.exception.code, 2)

    @patch("sys.stdin")
    @patch("builtins.input", return_value="")
    def test_tty_empty_defaults_no(self, mock_input, mock_stdin):
        """When stdin is TTY and user presses Enter (empty), aborts."""
        from utils import confirm_or_die

        mock_stdin.isatty.return_value = True

        with self.assertRaises(SystemExit) as cm:
            confirm_or_die("Delete file.txt")

        self.assertEqual(cm.exception.code, 2)

    @patch("sys.stdin")
    @patch("builtins.input", side_effect=EOFError)
    def test_tty_eof_aborts(self, mock_input, mock_stdin):
        """When stdin is TTY and EOF is received, exits with code 2."""
        from utils import confirm_or_die

        mock_stdin.isatty.return_value = True

        with self.assertRaises(SystemExit) as cm:
            confirm_or_die("Delete file.txt")

        self.assertEqual(cm.exception.code, 2)

    def test_parse_datetime_none(self):
        from utils import parse_datetime

        self.assertIsNone(parse_datetime(None))

    def test_parse_datetime_invalid_returns_none(self):
        from utils import parse_datetime

        self.assertIsNone(parse_datetime("+1d"))

    def test_parse_recipients_single(self):
        from utils import parse_recipients

        self.assertEqual(parse_recipients("user@example.com"), ["user@example.com"])

    def test_parse_recipients_comma_separated(self):
        from utils import parse_recipients

        self.assertEqual(
            parse_recipients("user1@example.com, user2@example.com"),
            ["user1@example.com", "user2@example.com"],
        )

    def test_parse_recipients_semicolon_is_not_split(self):
        from utils import parse_recipients

        self.assertEqual(
            parse_recipients("user1@example.com; user2@example.com"),
            ["user1@example.com; user2@example.com"],
        )

    def test_format_datetime_uses_isoformat(self):
        from utils import format_datetime

        result = format_datetime(datetime(2024, 1, 15, 10, 30))
        self.assertEqual(result, "2024-01-15T10:30:00")

    def test_format_datetime_none(self):
        from utils import format_datetime

        self.assertIsNone(format_datetime(None))

    def test_mask_email(self):
        from utils import mask_email

        self.assertEqual(mask_email("user@example.com"), "u***@example.com")

    def test_mask_email_invalid_input_returns_mask(self):
        from utils import mask_email

        self.assertEqual(mask_email(""), "***")
        self.assertEqual(mask_email("not-an-email"), "***")

    def test_parse_recipients_none_returns_empty_list(self):
        from utils import parse_recipients

        self.assertEqual(parse_recipients(None), [])

    def test_die_accepts_dict_message(self):
        from utils import die

        with self.assertRaises(SystemExit) as exc:
            die({"ok": False, "error": "boom"})
        self.assertEqual(exc.exception.code, 1)

    def test_task_to_dict_returns_empty_without_exchangelib_task(self):
        from utils import task_to_dict

        self.assertEqual(task_to_dict(None), {})


class TestLogger(unittest.TestCase):
    """Tests for logger helpers."""

    def test_get_logger_returns_logger_instance(self):
        from logger import get_logger

        logger = get_logger()
        self.assertIsNotNone(logger)


class TestConfig(unittest.TestCase):
    """Tests for current config loading entrypoints."""

    @patch.dict(
        os.environ,
        {
            "EXCHANGE_SERVER": "https://test.com/EWS",
            "EXCHANGE_USERNAME": "testuser",
            "EXCHANGE_PASSWORD": "testpass",
            "EXCHANGE_EMAIL": "test@test.com",
        },
        clear=False,
    )
    def test_get_config_from_env(self):
        from config import get_config

        config = get_config()
        self.assertEqual(config["server"], "https://test.com/EWS")
        self.assertEqual(config["username"], "testuser")
        self.assertEqual(config["password"], "testpass")
        self.assertEqual(config["email"], "test@test.com")

    def test_get_connection_config_exists(self):
        from config import get_connection_config

        self.assertTrue(callable(get_connection_config))


class TestMail(unittest.TestCase):
    """Tests for mail module structure."""

    def test_mail_functions_exist(self):
        from mail import cmd_connect, cmd_read, cmd_get, cmd_send, cmd_mark_all_read

        for fn in [cmd_connect, cmd_read, cmd_get, cmd_send, cmd_mark_all_read]:
            self.assertTrue(callable(fn))

    def test_add_parser_exists(self):
        from mail import add_parser

        self.assertTrue(callable(add_parser))

    def test_get_folder_standard_aliases(self):
        from mail import get_folder

        mock_account = MagicMock()
        mock_account.inbox = "inbox_folder"
        mock_account.trash = "trash_folder"
        mock_account.sent = "sent_folder"
        mock_account.drafts = "drafts_folder"
        mock_account.junk = "junk_folder"
        mock_account.outbox = "outbox_folder"
        mock_account.root.walk = MagicMock(return_value=[])

        self.assertEqual(get_folder(mock_account, "inbox"), "inbox_folder")
        self.assertEqual(get_folder(mock_account, "INBOX"), "inbox_folder")
        self.assertEqual(get_folder(mock_account, "trash"), "trash_folder")
        self.assertEqual(get_folder(mock_account, "deleted"), "trash_folder")
        self.assertEqual(get_folder(mock_account, "spam"), "junk_folder")


class TestCalendar(unittest.TestCase):
    """Tests for calendar module structure."""

    def test_calendar_functions_exist(self):
        from cal import cmd_connect, cmd_list, cmd_today, cmd_create

        for fn in [cmd_connect, cmd_list, cmd_today, cmd_create]:
            self.assertTrue(callable(fn))

    def test_add_parser_exists(self):
        from cal import add_parser

        self.assertTrue(callable(add_parser))


class TestTasks(unittest.TestCase):
    """Tests for tasks module structure."""

    def test_tasks_functions_exist(self):
        from tasks import cmd_connect, cmd_list, cmd_create, cmd_complete, cmd_trash

        for fn in [cmd_connect, cmd_list, cmd_create, cmd_complete, cmd_trash]:
            self.assertTrue(callable(fn))

    def test_add_parser_exists(self):
        from tasks import add_parser

        self.assertTrue(callable(add_parser))


class TestCLI(unittest.TestCase):
    """Tests for CLI entrypoint behavior."""

    def test_cli_imports(self):
        from cli import main

        self.assertTrue(callable(main))

    def test_cli_help_output_mentions_modules(self):
        result = subprocess.run(
            [sys.executable, "-m", "modules.exchange.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("nexlink", result.stdout)
        self.assertIn("mail", result.stdout)
        self.assertIn("calendar", result.stdout)
        self.assertIn("tasks", result.stdout)
        self.assertIn("--json", result.stdout)

    def test_cli_help_json_flag_listed_in_subcommands(self):
        """Each module subcommand help should mention --json."""
        for subcmd in ["mail connect", "calendar today", "tasks list", "sync status"]:
            result = subprocess.run(
                [sys.executable, "-m", "modules.exchange.cli"] + subcmd.split() + ["--help"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
            )
            self.assertEqual(result.returncode, 0, f"{subcmd} --help failed")
            self.assertIn("--json", result.stdout, f"{subcmd} --help should list --json")


class TestAnalytics(unittest.TestCase):
    """Tests for analytics module structure."""

    def test_analytics_source_contains_expected_commands(self):
        analytics_path = os.path.join(EXCHANGE_MODULE_DIR, "analytics.py")
        content = open(analytics_path, "r", encoding="utf-8").read()

        for symbol in [
            "def cmd_stats",
            "def cmd_top_senders",
            "def cmd_folders",
            "def cmd_heatmap",
            "def get_email_stats",
            "def add_parser",
        ]:
            self.assertIn(symbol, content)


class TestSync(unittest.TestCase):
    """Tests for sync module structure."""

    def test_sync_functions_exist(self):
        from sync import cmd_sync, cmd_reminders, cmd_status

        for fn in [cmd_sync, cmd_reminders, cmd_status]:
            self.assertTrue(callable(fn))

    def test_add_parser_exists(self):
        from sync import add_parser

        self.assertTrue(callable(add_parser))


if __name__ == "__main__":
    unittest.main()
