#!/usr/bin/env python3
"""Tests for scripts/self_check.py itself.

A gate that silently stops checking is worse than no gate: RC5 shipped as a hardcoded "1.0.0"
and kept reporting "pinned" after the package moved to 1.1.0, while both install lines in the
docs still named the old release. These tests pin that behaviour down.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import self_check as sc  # noqa: E402

FRONTMATTER = """---
name: packet-audit
description: "Use when documents must pass. Not legal advice, not OCR."
metadata: {{"version": "{version}", "license": "MIT-0", "offline": true}}
---

# Packet Audit

"""


class FloatingPinRule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self._saved = (sc.ROOT, sc.SKILL, sc.checks)
        sc.ROOT, sc.SKILL = self.root, self.root / "SKILL.md"
        sc.checks = []

    def tearDown(self):
        sc.ROOT, sc.SKILL, sc.checks = self._saved

    def write(self, version: str, *documents: tuple[str, str]) -> None:
        (self.root / "SKILL.md").write_text(FRONTMATTER.format(version=version), encoding="utf-8")
        for name, text in documents:
            (self.root / name).write_text(text, encoding="utf-8")

    def rule(self) -> dict:
        sc.rule_no_floating_versions()
        return sc.checks[-1]

    def test_current_pin_passes(self):
        self.write("1.1.1", ("README.md", "npx --yes clawhub@0.23.3 install deepseekoracle/packet-audit@1.1.1\n"))
        result = self.rule()
        self.assertTrue(result["ok"], result["detail"])
        self.assertIn("1.1.1", result["detail"])

    def test_stale_pin_fails_and_names_both_versions(self):
        # the exact regression: docs pinned the previous release
        self.write("1.1.1", ("README.md", "npx --yes clawhub@0.23.3 install deepseekoracle/packet-audit@1.0.0\n"))
        result = self.rule()
        self.assertFalse(result["ok"])
        self.assertIn("1.0.0", result["detail"])
        self.assertIn("1.1.1", result["detail"])

    def test_floating_latest_still_fails(self):
        self.write("1.1.1", ("README.md", "npx --yes clawhub@latest install packet-audit\n"))
        self.assertFalse(self.rule()["ok"])

    def test_changelog_history_mentioning_an_old_pin_is_not_an_offence(self):
        self.write("1.1.1",
                   ("CHANGELOG.md", "## v1.1.0\n\nInstall commands still pinned `packet-audit@1.0.0`.\n"),
                   ("README.md", "npx --yes clawhub@0.23.3 install deepseekoracle/packet-audit@1.1.1\n"))
        result = self.rule()
        self.assertTrue(result["ok"], result["detail"])

    def test_unreadable_version_fails_instead_of_skipping(self):
        (self.root / "SKILL.md").write_text("---\nname: packet-audit\n---\n\n# x\n", encoding="utf-8")
        result = self.rule()
        self.assertFalse(result["ok"])
        self.assertIn("no version", result["detail"])

    def test_version_is_read_from_frontmatter_metadata(self):
        self.write("2.3.4")
        head, _ = sc.frontmatter((self.root / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(head["meta"]["version"], "2.3.4")


class ShippedPackage(unittest.TestCase):
    """The real tree must satisfy the rule it ships."""

    def test_package_passes_its_own_gate(self):
        sc.checks = []
        code = sc.main()
        payload = {"failed": [c["name"] for c in sc.checks if not c["ok"]],
                   "count": len(sc.checks)}
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["count"], 10, payload)

    def test_version_agrees_across_manifest_engine_and_changelog(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        head, _ = sc.frontmatter(text)
        version = head["meta"]["version"]
        engine = (ROOT / "scripts" / "packet_audit.py").read_text(encoding="utf-8")
        self.assertIn(f'TOOL_VERSION = "{version}"', engine)
        self.assertRegex((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
                         rf"^## v{re.escape(version)}\b", )

    def test_every_documented_install_pins_that_version(self):
        version = sc.frontmatter((ROOT / "SKILL.md").read_text(encoding="utf-8"))[0]["meta"]["version"]
        for name in ("SKILL.md", "README.md"):
            doc = (ROOT / name).read_text(encoding="utf-8")
            pins = re.findall(r"packet-audit@([0-9][0-9A-Za-z.\-]*)", doc)
            self.assertTrue(pins, f"{name} has no pinned install line")
            self.assertEqual(set(pins), {version}, name)


if __name__ == "__main__":
    unittest.main()
