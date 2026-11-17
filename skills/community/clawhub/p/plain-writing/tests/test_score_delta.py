from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "score_delta.py"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import score_delta  # noqa: E402


class ScoreDeltaTests(unittest.TestCase):
    def make_pair(self, before: str, after: str) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        before_path = root / "before.md"
        after_path = root / "after.md"
        before_path.write_text(before, encoding="utf-8")
        after_path.write_text(after, encoding="utf-8")
        return directory, before_path, after_path

    def test_reports_normalized_and_rule_level_deltas(self) -> None:
        directory, before, after = self.make_pair(
            "It is worth noting that this robust tool can leverage data.",
            "This tool uses data.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(before, after, "strict")
        self.assertGreater(report["before"]["findings"], 0)
        self.assertEqual(0, report["after"]["findings"])
        self.assertLess(report["delta"]["findings_per_100_words"], 0)
        self.assertLess(report["delta"]["words_pct"], 0)
        self.assertLess(report["delta"]["rules"]["WRD002"], 0)
        self.assertFalse(report["mechanical_regression"])
        self.assertFalse(report["judges_truth_or_quality"])

    def test_protected_token_loss_is_visible(self) -> None:
        directory, before, after = self.make_pair(
            "Restart worker-17.",
            "Restart the worker.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(
            before, after, "strict", protected_tokens=["worker-17"]
        )
        self.assertEqual(["worker-17"], report["protected_tokens"]["lost"])
        self.assertEqual(0.0, report["protected_tokens"]["retention_pct"])

    def test_protected_token_requires_presence_not_multiplicity(self) -> None:
        directory, before, after = self.make_pair(
            "Use worker-17, then verify worker-17.",
            "Use worker-17, then verify the worker.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(
            before, after, "strict", protected_tokens=["worker-17"]
        )
        self.assertEqual([], report["protected_tokens"]["lost"])
        self.assertEqual(2, report["protected_tokens"]["source_occurrences"])
        self.assertEqual(1, report["protected_tokens"]["retained_occurrences"])
        self.assertEqual(50.0, report["protected_tokens"]["retention_pct"])

    def test_protected_count_can_require_multiplicity(self) -> None:
        directory, before, after = self.make_pair(
            "Use worker-17, then verify worker-17.",
            "Use worker-17, then verify the worker.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(
            before,
            after,
            "strict",
            protected_tokens=["worker-17"],
            protected_count=True,
        )
        self.assertEqual(["worker-17"], report["protected_tokens"]["lost"])
        self.assertTrue(report["protected_tokens"]["requires_source_count"])

    def test_reports_structure_without_failing_compression(self) -> None:
        directory, before, after = self.make_pair(
            "# Why this matters\n\n- First long explanatory item in a padded list.\n"
            "- Second long explanatory item in a padded list.\n",
            "The first and second items matter.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(before, after, "technical")
        self.assertEqual(-1, report["delta"]["structure"]["headings"])
        self.assertEqual(-2, report["delta"]["structure"]["list_items"])
        self.assertIn("not fidelity failures", report["review_required"])
        self.assertFalse(report["structural_expansion"])

    def test_structural_expansion_can_fail_cli(self) -> None:
        directory, before, after = self.make_pair(
            "Alpha and bravo.",
            "# Update\n\n- Alpha\n- Bravo\n",
        )
        self.addCleanup(directory.cleanup)
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--fail-on-structural-expansion",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, process.returncode)
        self.assertIn("Structural expansion:", process.stdout)

    def test_equivalent_section_label_styles_are_normalized(self) -> None:
        directory, before, after = self.make_pair(
            "**Background**\n\nThe worker stopped.",
            "# Background\n\nThe worker stopped.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(before, after, "technical")
        self.assertEqual(0, report["delta"]["structure"]["section_labels"])
        self.assertFalse(report["structural_expansion"])

    def test_plain_colon_label_is_a_section_label(self) -> None:
        counts = score_delta.structure("Background:\n\nThe worker stopped.")
        self.assertEqual(1, counts["plain_labels"])
        self.assertEqual(1, counts["section_labels"])

    def test_scope_strengthening_is_review_only(self) -> None:
        directory, before, after = self.make_pair(
            "Some retries may fail after the timeout.",
            "All retries will fail because the timeout caused the error.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(before, after, "technical")
        self.assertTrue(report["fidelity_signals"])
        messages = " ".join(item["message"] for item in report["fidelity_signals"])
        self.assertIn("some", messages)
        self.assertIn("may", messages)
        self.assertIn("caused", messages)
        self.assertFalse(report["structural_expansion"])

    def test_scope_signal_does_not_join_unrelated_sentences(self) -> None:
        directory, before, after = self.make_pair(
            "The hook may exist in HTTP. Cleanup won't resolve the backlog.",
            "The hook may exist in HTTP. Cleanup will not resolve the backlog.",
        )
        self.addCleanup(directory.cleanup)
        report = score_delta.compare(before, after, "technical")
        self.assertEqual([], report["fidelity_signals"])

    def test_structure_ignores_literal_log_labels(self) -> None:
        counts = score_delta.structure(
            "```text\nError code: schedule_event_false\n# Literal heading\n```"
        )
        self.assertEqual(0, counts["plain_labels"])
        self.assertEqual(0, counts["headings"])

    def test_json_cli_and_regression_exit(self) -> None:
        directory, before, after = self.make_pair(
            "Use the tool.",
            "It is worth noting that this robust tool can leverage data.",
        )
        self.addCleanup(directory.cleanup)
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--mode",
                "strict",
                "--format",
                "json",
                "--fail-on-regression",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, process.returncode)
        report = json.loads(process.stdout)
        self.assertTrue(report["mechanical_regression"])

    def test_missing_input_returns_usage_error(self) -> None:
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "/missing-before", "/missing-after"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, process.returncode)
        self.assertIn("score_delta.py: error:", process.stderr)


if __name__ == "__main__":
    unittest.main()
