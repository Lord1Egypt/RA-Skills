"""Smoke tests for ocas-sift scripts.

Run: python3 -m unittest discover -s tests
These verify the contract SKILL.md promises: every script exposes a working
--help that exits 0 without optional dependencies installed, and the wayback
fallback's pure-stdlib helpers behave correctly offline.
"""
import importlib.util
import os
import subprocess
import sys
import unittest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(SKILL_DIR, "scripts")


def _load(name):
    path = os.path.join(SCRIPTS, name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None, path
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestHelpGuards(unittest.TestCase):
    """Every script must print usage and exit 0 on --help (D9 contract)."""

    def test_wayback_help(self):
        p = subprocess.run([sys.executable, "wayback_fallback.py", "--help"],
                           cwd=SCRIPTS, capture_output=True, timeout=30)
        self.assertEqual(p.returncode, 0)
        self.assertIn(b"usage", p.stdout.lower())

    def test_webwright_help(self):
        p = subprocess.run([sys.executable, "webwright_runner.py", "--help"],
                           cwd=SCRIPTS, capture_output=True, timeout=30)
        self.assertEqual(p.returncode, 0)
        self.assertIn(b"usage", p.stdout.lower())

    def test_update_sh_help(self):
        p = subprocess.run(["bash", "update.sh", "--help"],
                           cwd=SCRIPTS, capture_output=True, timeout=30)
        self.assertEqual(p.returncode, 0)
        self.assertIn(b"Usage:", p.stdout)

    def test_update_sh_rejects_unknown_flag(self):
        p = subprocess.run(["bash", "update.sh", "--bogus"],
                           cwd=SCRIPTS, capture_output=True, timeout=60)
        self.assertNotEqual(p.returncode, 0)

    def test_csapi_quota_help(self):
        p = subprocess.run([sys.executable, "csapi_quota.py"],
                           cwd=SCRIPTS, capture_output=True, timeout=30)
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"Google Custom Search API quota tracker", p.stdout)


class TestCSAPIQuotaHelpers(unittest.TestCase):
    def test_csapi_quota_functions(self):
        csapi = _load("csapi_quota")
        targets = csapi._get_targets("owner")
        self.assertEqual(targets, ["owner"])
        targets_all = csapi._get_targets(None)
        self.assertEqual(targets_all, ["owner", "indigo"])

        # Test state check_and_reset
        state = {"owner": {"month": "2000-01", "count": 50}}
        state, modified = csapi.check_and_reset(state, "owner")
        self.assertTrue(modified)
        self.assertEqual(state["owner"]["count"], 0)
        self.assertEqual(len(state["owner"]["history"]), 1)
        self.assertEqual(state["owner"]["history"][0]["queries"], 50)


class TestWebwrightHelpers(unittest.TestCase):
    def test_next_run_id(self):
        import tempfile
        from pathlib import Path
        webwright = _load("webwright_runner")
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = Path(tmpdir)
            self.assertEqual(webwright.next_run_id(ws), 1)

            final_runs = ws / "final_runs"
            final_runs.mkdir()
            (final_runs / "run_1").mkdir()
            (final_runs / "run_2").mkdir()
            (final_runs / "run_10").mkdir()
            # Ensure multi-digit run numbers are parsed as max integer rather than lexicographically
            self.assertEqual(webwright.next_run_id(ws), 11)

    def test_verify_run(self):
        import tempfile
        from pathlib import Path
        webwright = _load("webwright_runner")
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = Path(tmpdir)
            run_dir = ws / "final_runs" / "run_1"
            run_dir.mkdir(parents=True)
            screenshots_dir = run_dir / "screenshots"
            screenshots_dir.mkdir()

            (run_dir / "final_script_log.txt").write_text("Completed CP1 action\n")
            (screenshots_dir / "step2_cp2.png").write_text("")

            res = webwright.verify_run(ws, run_dir, ["Action 1", "Action 2", "Action 3"])
            self.assertEqual(len(res["passed"]), 2)
            self.assertEqual(len(res["failed"]), 1)
            self.assertIn("CP1: Action 1", res["passed"])
            self.assertIn("CP2: Action 2", res["passed"])
            self.assertIn("CP3: Action 3", res["failed"])


class TestWaybackHelpers(unittest.TestCase):
    def test_decode_body_gzip(self):
        import gzip as _gzip
        wb = _load("wayback_fallback")
        raw = _gzip.compress(b"<html>hello</html>")
        self.assertEqual(wb._decode_body(raw, "gzip"), b"<html>hello</html>")

    def test_decode_body_deflate(self):
        import zlib
        wb = _load("wayback_fallback")
        for variant in (zlib.compress(b"data"),
                        zlib.compress(b"data")[2:-4]):  # raw deflate stream
            self.assertEqual(wb._decode_body(variant, "deflate"), b"data")

    def test_hard_block_detection_signals_present(self):
        wb = _load("wayback_fallback")
        # The module must define its hard-block markers; empty would mean the
        # fallback fires on soft failures, its documented anti-pattern.
        self.assertTrue(len(wb._BLOCK_PATTERNS) > 0)


if __name__ == "__main__":
    unittest.main()
