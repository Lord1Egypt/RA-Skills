"""Isolated regression tests for Python diagnostic privacy and hook dispatch."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from core import openclaw_runtime_probe, openclaw_signal_hook, signal_detect, signal_pipeline
from core.common import session_fingerprint


QUERY_SECRET = "private_query_sentinel_9d3b"
SESSION_SECRET = "private_session_sentinel_a49c"
QUERY = "remember when " + QUERY_SECRET


class PrivacyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hui-yi-privacy-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "memory" / "cold"
        self.root.mkdir(parents=True)
        self.note = self.root / "example.md"
        self.note.write_text("# Example memory\n\n## Session signals\n- current_session_hits: 0\n", encoding="utf-8")
        self.payload = {
            "_meta": {"version": 5},
            "notes": [{"title": "Example memory", "path": "memory/cold/example.md",
                       "summary": QUERY_SECRET, "tags": [QUERY_SECRET]}],
        }
        self.write_tags()

    def write_tags(self):
        (self.root / "tags.json").write_text(json.dumps(self.payload), encoding="utf-8")

    def call(self, main, argv, stdin=""):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr), patch("sys.stdin", io.StringIO(stdin)):
            code = main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def assert_private(self, output):
        self.assertNotIn(QUERY_SECRET.lower(), output.lower())
        self.assertNotIn(SESSION_SECRET.lower(), output.lower())
        self.assertNotIn("overlap_terms", output)

    def test_detector_default_outputs_hide_query_terms(self):
        for extra in ([], ["--json"]):
            code, stdout, stderr = self.call(signal_detect.main,
                ["--memory-root", str(self.root), "--query", QUERY, *extra])
            self.assertEqual(code, 0)
            self.assertIn("Example memory", stdout)
            self.assert_private(stdout + stderr)

    def test_sensitive_detector_output_requires_opt_in(self):
        code, stdout, _ = self.call(signal_detect.main,
            ["--memory-root", str(self.root), "--query", QUERY, "--json", "--include-sensitive"])
        self.assertEqual(code, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["query"], QUERY)
        self.assertIn(QUERY_SECRET, payload["candidates"][0]["overlap_terms"])

    def test_pipeline_default_output_and_persistence_hash_session(self):
        code, stdout, stderr = self.call(signal_pipeline.main,
            ["--memory-root", str(self.root), "--stdin", "--session-key", SESSION_SECRET, "--apply", "--json"], QUERY)
        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["session_hash"], session_fingerprint(SESSION_SECRET))
        self.assertEqual(len(payload["applied"]), 1)
        self.assert_private(stdout + stderr)
        self.assertNotIn(SESSION_SECRET, (self.root / "tags.json").read_text(encoding="utf-8"))

    def test_sensitive_pipeline_never_outputs_raw_session(self):
        code, stdout, _ = self.call(signal_pipeline.main,
            ["--memory-root", str(self.root), "--query", QUERY, "--session-key", SESSION_SECRET,
             "--json", "--include-sensitive"])
        self.assertEqual(code, 0)
        self.assertIn(QUERY_SECRET, stdout)
        self.assertNotIn(SESSION_SECRET, stdout)

    def test_json_apply_errors_have_failing_exit_status(self):
        with patch.object(signal_pipeline, "apply_candidates", return_value=([], [], ["write_failed"])):
            code, stdout, _ = self.call(signal_pipeline.main,
                ["--memory-root", str(self.root), "--query", QUERY, "--session-key", SESSION_SECRET, "--apply", "--json"])
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(stdout)["ok"])
        self.assert_private(stdout)

    def test_hook_allowlist_cannot_forward_sensitive_pipeline_fields(self):
        untrusted = {"ok": True, "query": QUERY, "session_key": SESSION_SECRET,
                     "candidates": [{"title": QUERY_SECRET, "overlap_terms": [QUERY_SECRET]}],
                     "applied": [QUERY_SECRET], "skipped": [SESSION_SECRET], "apply_errors": []}
        with patch.object(openclaw_signal_hook, "run_pipeline", return_value=untrusted):
            result = openclaw_signal_hook.call_signal_pipeline(self.root, QUERY, SESSION_SECRET,
                limit=3, min_relevance=0.3, min_confidence="medium", apply=False)
        self.assertTrue(result["ok"])
        self.assertEqual(result["pipeline"]["candidateCount"], 1)
        self.assert_private(json.dumps(result))

    def test_hook_redacts_exception_text(self):
        with patch.object(openclaw_signal_hook, "run_pipeline", side_effect=ValueError(QUERY + SESSION_SECRET)):
            result = openclaw_signal_hook.call_signal_pipeline(self.root, QUERY, SESSION_SECRET,
                limit=3, min_relevance=0.3, min_confidence="medium", apply=False)
        self.assertFalse(result["ok"])
        self.assert_private(json.dumps(result))

    def test_hook_and_probe_accept_private_stdin_without_subprocess(self):
        args = ["--memory-root", str(self.root), "--stdin", "--channel", "test",
                "--scope-type", "user", "--scope-id", SESSION_SECRET, "--dry-run"]
        for main in (openclaw_signal_hook.main, openclaw_runtime_probe.main):
            with patch("subprocess.run", side_effect=AssertionError("must not launch a process")):
                code, stdout, stderr = self.call(main, args, QUERY)
            self.assertEqual(code, 0, stderr)
            self.assertTrue(json.loads(stdout)["ok"])
            self.assert_private(stdout + stderr)
            self.assertNotIn('"command"', stdout)

    def test_batch_preflight_prevents_partial_activation(self):
        self.payload["notes"].append({"title": "Unsafe memory", "path": "../outside.md", "summary": QUERY_SECRET})
        self.write_tags()
        before = self.note.read_bytes()
        candidates = [{"path": "memory/cold/example.md", "title": "Example memory"},
                      {"path": "../outside.md", "title": "Unsafe memory"}]
        with self.assertRaises(ValueError):
            signal_pipeline.apply_candidates(self.root, candidates, SESSION_SECRET)
        self.assertEqual(self.note.read_bytes(), before)

    def test_missing_query_is_machine_readable_failure(self):
        code, stdout, _ = self.call(signal_pipeline.main, ["--memory-root", str(self.root), "--json"])
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
