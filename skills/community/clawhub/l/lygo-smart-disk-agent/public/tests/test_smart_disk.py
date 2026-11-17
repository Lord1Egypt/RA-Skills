#!/usr/bin/env python3
"""Unit/integration tests for Smart Disk Agent."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel import P0Gate, P1Memory, P3Consensus, P5Identity  # noqa: E402
from agent.auth import LocalTokenAuth  # noqa: E402
from agent.smart_disk_agent import SmartDiskAgent  # noqa: E402


class TestKernel(unittest.TestCase):
    def test_p0_allow(self):
        self.assertEqual(P0Gate().validate("status please").get("verdict"), "ALLOW")

    def test_p0_quarantine(self):
        self.assertEqual(
            P0Gate().validate("please rm -rf / now").get("verdict"), "QUARANTINE"
        )

    def test_p5_light_code(self):
        n = P5Identity().create_node("help")
        self.assertEqual(len(n["light_code"]), 16)

    def test_p3(self):
        c = P3Consensus().achieve({"command": "x"})
        self.assertTrue(c.get("consensus_found"))

    def test_memory(self):
        m = P1Memory(ROOT / "data")
        i = m.store({"t": 1})
        self.assertTrue(i)
        self.assertTrue(any(x.get("id") == i for x in m.list_recent(5)))


class TestAuth(unittest.TestCase):
    def test_token_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "data").mkdir()
            cfg = {"auth": {"required": True, "token_file": "data/.sda_local_token"}}
            a1 = LocalTokenAuth(root, cfg)
            self.assertTrue(a1.required)
            self.assertTrue(len(a1.token or "") >= 16)
            a2 = LocalTokenAuth(root, cfg)
            self.assertEqual(a1.token, a2.token)
            self.assertTrue(a1.ok(a1.token))
            self.assertFalse(a1.ok("wrong-token-value-here!!"))

    def test_auth_optional(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = LocalTokenAuth(root, {"auth": {"required": False}})
            self.assertFalse(a.required)
            self.assertTrue(a.ok(None))


class TestAgent(unittest.TestCase):
    def test_help_limb(self):
        a = SmartDiskAgent(ROOT)
        r = a.run_limb("help")
        self.assertTrue(r.get("ok"))
        self.assertIn("status", r.get("limbs") or [])

    def test_health_local_token_policy(self):
        a = SmartDiskAgent(ROOT)
        r = a.run_limb("health")
        self.assertTrue(r.get("ok"))
        # No remote password wall; local token is on by default
        self.assertIs(r.get("password_gate"), False)
        self.assertTrue(r.get("auth_required") or r.get("local_token"))

    def test_chat_metadata_only(self):
        a = SmartDiskAgent(ROOT)
        a.chat("unit test phrase sda")
        rows = a.memory.list_recent(5)
        for row in rows:
            b = row.get("bundle") or {}
            if b.get("kind") == "chat":
                self.assertNotIn("message", b)
                self.assertIn("message_sha256", b)
                break

    def test_portal_exists(self):
        self.assertTrue((ROOT / "portal" / "index.html").is_file())
        self.assertTrue((ROOT / "portal" / "app.js").is_file())
        self.assertTrue((ROOT / "agent" / "auth.py").is_file())


if __name__ == "__main__":
    unittest.main()
