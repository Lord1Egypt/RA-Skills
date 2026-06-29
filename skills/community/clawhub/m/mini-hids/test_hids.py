#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mini-HIDS unit tests.
"""

import os
import sqlite3
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch

from hids_common import (
    FirewallManager,
    delete_blacklist_entry,
    execute_ban,
    execute_unban,
    extract_client_ip,
    init_db,
    list_blacklist_rows,
    load_config,
    parse_alert_line,
    purge_expired_blacklist_entries,
    scan_web_roots,
    upsert_blacklist_entry,
    validate_ban_request,
    validate_ip,
)


def suspicious_php_fixture():
    """Build a detector fixture without shipping a complete executable sample."""
    return "".join([
        "<?php echo ",
        "sh",
        "ell_",
        "exec",
        "($_",
        "GET",
        "['cmd']); ?>",
    ])


class TestValidateIP(unittest.TestCase):
    def test_valid_ipv4(self):
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("10.0.0.1"))
        self.assertTrue(validate_ip("8.8.8.8"))

    def test_valid_ipv6(self):
        self.assertTrue(validate_ip("::1"))
        self.assertTrue(validate_ip("fe80::1"))
        self.assertTrue(validate_ip("2001:db8::1"))

    def test_invalid_ip(self):
        self.assertFalse(validate_ip("not-an-ip"))
        self.assertFalse(validate_ip("256.256.256.256"))
        self.assertFalse(validate_ip(""))
        self.assertFalse(validate_ip("192.168.1"))


class TestConfigLoading(unittest.TestCase):
    def test_load_config_defaults(self):
        with patch("hids_common.BASE_DIR", tempfile.gettempdir()):
            config = load_config()
            self.assertIn("LOG_PATHS", config)
            self.assertIn("BAN_TIME", config)
            self.assertIn("TRUSTED_IPS", config)
            self.assertEqual(config["BAN_TIME"], 3600)

    def test_config_path_resolution(self):
        with patch("hids_common.BASE_DIR", tempfile.gettempdir()):
            config = load_config()
            self.assertTrue(os.path.isabs(config["BLACKLIST_DB"]))
            self.assertTrue(os.path.isabs(config["ALERT_LOG"]))
            self.assertTrue(os.path.isabs(config["PID_FILE"]))


class TestAccessLogParsing(unittest.TestCase):
    def test_common_access_log_ip(self):
        line = '203.0.113.10 - - [18/Jun/2025:10:23:45 +0000] "GET / HTTP/1.1" 200 12'
        self.assertEqual(extract_client_ip(line), "203.0.113.10")

    def test_access_log_with_username(self):
        line = '203.0.113.11 user auth [18/Jun/2025:10:23:45 +0000] "GET / HTTP/1.1" 200 12'
        self.assertEqual(extract_client_ip(line), "203.0.113.11")

    def test_invalid_access_log_ip(self):
        line = 'not-an-ip - - [18/Jun/2025:10:23:45 +0000] "GET / HTTP/1.1" 200 12'
        self.assertIsNone(extract_client_ip(line))


class TestSQLiteOperations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "blacklist.db")
        init_db(self.db_path)

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except PermissionError:
            pass

    def test_init_db_creates_table(self):
        with sqlite3.connect(self.db_path) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            table_names = [t[0] for t in tables]
            self.assertIn("blacklist", table_names)

    def test_upsert_and_list(self):
        upsert_blacklist_entry(self.db_path, "192.168.1.100", int(time.time()) + 3600, "test ban")
        rows = list_blacklist_rows(self.db_path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "192.168.1.100")
        self.assertEqual(rows[0][2], "test ban")

    def test_delete_entry(self):
        upsert_blacklist_entry(self.db_path, "192.168.1.100", int(time.time()) + 3600, "test")
        delete_blacklist_entry(self.db_path, "192.168.1.100")
        rows = list_blacklist_rows(self.db_path)
        self.assertEqual(len(rows), 0)

    def test_purge_expired(self):
        past_time = int(time.time()) - 100
        future_time = int(time.time()) + 3600
        upsert_blacklist_entry(self.db_path, "10.0.0.1", past_time, "expired")
        upsert_blacklist_entry(self.db_path, "10.0.0.2", future_time, "active")

        purged = purge_expired_blacklist_entries(self.db_path)
        self.assertEqual(purged, 1)

        rows = list_blacklist_rows(self.db_path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "10.0.0.2")


class TestValidateBanRequest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "blacklist.db")
        init_db(self.db_path)

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except PermissionError:
            pass

    def test_invalid_ip(self):
        result = validate_ban_request("invalid", [], self.db_path)
        self.assertIsNotNone(result)
        self.assertFalse(result["success"])

    def test_trusted_ip(self):
        result = validate_ban_request("192.168.1.1", ["192.168.1.1"], self.db_path)
        self.assertIsNotNone(result)
        self.assertFalse(result["success"])

    def test_already_banned(self):
        future_time = int(time.time()) + 3600
        upsert_blacklist_entry(self.db_path, "10.0.0.1", future_time, "test")
        result = validate_ban_request("10.0.0.1", [], self.db_path)
        self.assertIsNotNone(result)
        self.assertTrue(result["success"])

    def test_valid_request(self):
        result = validate_ban_request("10.0.0.1", [], self.db_path)
        self.assertIsNone(result)


class TestExecuteBanUnban(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "blacklist.db")
        init_db(self.db_path)
        self.mock_firewall = MagicMock()

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except PermissionError:
            pass

    def test_execute_ban_success(self):
        expiry_time = execute_ban("10.0.0.1", "test", 3600, self.mock_firewall, self.db_path)
        self.assertGreater(expiry_time, int(time.time()))
        self.mock_firewall.ban_ip.assert_called_once_with("10.0.0.1", 3600)
        rows = list_blacklist_rows(self.db_path)
        self.assertEqual(len(rows), 1)

    def test_execute_ban_failure_rollback(self):
        self.mock_firewall.ban_ip.side_effect = RuntimeError("firewall error")
        with self.assertRaises(RuntimeError):
            execute_ban("10.0.0.1", "test", 3600, self.mock_firewall, self.db_path)
        self.mock_firewall.unban_ip.assert_called_once_with("10.0.0.1")

    def test_execute_unban_success(self):
        future_time = int(time.time()) + 3600
        upsert_blacklist_entry(self.db_path, "10.0.0.1", future_time, "test")
        result = execute_unban("10.0.0.1", self.mock_firewall, self.db_path)
        self.assertTrue(result)
        self.mock_firewall.unban_ip.assert_called_once_with("10.0.0.1")
        rows = list_blacklist_rows(self.db_path)
        self.assertEqual(len(rows), 0)

    def test_execute_unban_not_in_blacklist(self):
        result = execute_unban("10.0.0.1", self.mock_firewall, self.db_path)
        self.assertFalse(result)


class TestWebshellScan(unittest.TestCase):
    def test_scan_web_roots_finds_suspicious_file(self):
        with tempfile.TemporaryDirectory() as web_root:
            fixture_path = os.path.join(web_root, "sample.php")
            with open(fixture_path, "w", encoding="utf-8") as fixture_file:
                fixture_file.write(suspicious_php_fixture())

            result = scan_web_roots([web_root])

        self.assertEqual(result["scanned_files"], 1)
        self.assertEqual(result["suspicious_count"], 1)
        self.assertEqual(result["suspicious_files"][0]["file"], fixture_path)

    def test_incremental_scan_skips_unchanged_file(self):
        with tempfile.TemporaryDirectory() as web_root:
            fixture_path = os.path.join(web_root, "sample.php")
            with open(fixture_path, "w", encoding="utf-8") as fixture_file:
                fixture_file.write(suspicious_php_fixture())

            state = {}
            first_result = scan_web_roots([web_root], state)
            second_result = scan_web_roots([web_root], state)

        self.assertEqual(first_result["modified_files"], 1)
        self.assertEqual(second_result["modified_files"], 0)
        self.assertEqual(second_result["suspicious_count"], 0)


class TestDaemonDetection(unittest.TestCase):
    def test_detect_web_attack_uses_access_log_ip(self):
        import mini_hids

        line = '203.0.113.20 user auth [18/Jun/2025:10:23:45 +0000] "GET /?q=<script> HTTP/1.1" 200 12'
        with patch.object(mini_hids, "ban_ip") as mock_ban:
            with patch.object(mini_hids, "log_alert"):
                with patch.dict(mini_hids.CONFIG, {"MAX_FAILURES": 1, "WINDOW_SECONDS": 300}):
                    with mini_hids.state_lock:
                        mini_hids.blacklist.clear()
                        mini_hids.ip_failures.clear()
                    mini_hids.detect_web_attack(line)

        mock_ban.assert_called_once_with("203.0.113.20", "Web攻击")


class TestMCPServerValidation(unittest.TestCase):
    def test_get_alerts_rejects_invalid_lines(self):
        import mcp_server

        result = mcp_server._handle_tool_call("mini_hids_get_alerts", {"lines": "10"})

        self.assertTrue(result["isError"])
        self.assertFalse(result["structuredContent"]["success"])

    def test_ban_ip_requires_reason(self):
        import mcp_server

        result = mcp_server._handle_tool_call("mini_hids_ban_ip", {"ip": "192.0.2.10"})

        self.assertTrue(result["isError"])
        self.assertFalse(result["structuredContent"]["success"])


class TestParseAlertLine(unittest.TestCase):
    def test_ssh_brute_force(self):
        line = "[2025-06-18 10:23:45] [SSH暴力破解] 检测到来自 192.168.1.100 的登录失败，已达到阈值"
        result = parse_alert_line(line)
        self.assertEqual(result["type"], "ssh_brute_force")
        self.assertEqual(result["ip"], "192.168.1.100")
        self.assertEqual(result["timestamp"], "2025-06-18 10:23:45")

    def test_web_attack(self):
        line = "[2025-06-18 10:23:45] [Web攻击] 检测到来自 10.0.0.1 的可能攻击: <script>，已达到阈值"
        result = parse_alert_line(line)
        self.assertEqual(result["type"], "web_attack")
        self.assertEqual(result["ip"], "10.0.0.1")

    def test_webshell(self):
        line = "[2025-06-18 10:23:45] [Webshell] 检测到可疑文件: /var/www/html/sample.php"
        result = parse_alert_line(line)
        self.assertEqual(result["type"], "webshell")

    def test_ban(self):
        line = "[2025-06-18 10:23:45] [封禁] IP 192.168.1.100 因 SSH暴力破解 被封禁"
        result = parse_alert_line(line)
        self.assertEqual(result["type"], "ban")
        self.assertEqual(result["ip"], "192.168.1.100")

    def test_system_event(self):
        line = "[2025-06-18 10:23:45] [监控启动] 开始监控 /var/log/auth.log"
        result = parse_alert_line(line)
        self.assertEqual(result["type"], "system")

    def test_error_event(self):
        line = "[2025-06-18 10:23:45] [错误] 执行封禁失败 10.0.0.1: permission denied"
        result = parse_alert_line(line)
        self.assertEqual(result["type"], "error")

    def test_raw_line(self):
        line = "unformatted log line"
        result = parse_alert_line(line)
        self.assertEqual(result["raw"], "unformatted log line")


if __name__ == "__main__":
    unittest.main()
