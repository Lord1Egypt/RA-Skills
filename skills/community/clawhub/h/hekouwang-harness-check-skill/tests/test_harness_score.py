from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import harness_score  # noqa: E402


class HarnessScoreTests(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str, executable: bool = False) -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if executable:
            path.chmod(path.stat().st_mode | 0o111)
        return path

    def strong_fixture(self, root: Path) -> None:
        self.write(root, "README.md", "# Harness\nSee the Skill route and human review boundary.\n")
        self.write(root, "LICENSE", "MIT\n")
        self.write(root, "CHANGELOG.md", "# Changelog\n")
        self.write(root, "CONTRIBUTING.md", "# Contributing\n")
        self.write(root, "AGENTS.md", "Route to the Skill and references. Real host smoke test is separate.\n")
        self.write(root, ".harness/scripts/verify.sh", """#!/usr/bin/env bash
set -euo pipefail
case "$1" in
  --working-tree|--staged|--ci) echo '728 项检查通过' ;;
  *) exit 2 ;;
esac
""", executable=True)
        self.write(root, ".harness/scripts/harness-check.sh", "#!/usr/bin/env bash\nexit 0\n", executable=True)
        self.write(root, ".harness/scripts/episode.py", "# checkpoint recovery atomic lock resume\n")
        self.write(root, ".harness/scripts/observe-checks.sh", "# redact telemetry trend event\n")
        self.write(root, ".harness/scripts/sync-agent-adapters.sh", "# drift lifecycle --check\n")
        self.write(root, ".harness/hooks/safety-gate.py", "# fail-closed allow ask deny approval\n")
        self.write(root, ".harness/contracts/task-contract.json", json.dumps({
            "sha256": "abc", "evidence": [], "Evaluator": "independent", "humanEvidence": {
                "reviewer": "test", "decision": "pass"
            }
        }))
        self.write(root, ".harness/contracts/component-registry.json", "component registry workflow profile runtime contract\n")
        self.write(root, ".harness/tests/test-negative.py", "# negative invalid deny blocked\nassert True\n")
        self.write(root, ".harness/tests/fixtures/positive.json", "{}\n")
        self.write(root, ".harness/tests/fixtures/negative.json", "{}\n")
        self.write(root, "docs/host-smoke.md", "smoke pass decision=pass\n")
        self.write(root, ".github/workflows/quality.yml", """name: quality
jobs:
  check:
    steps:
      - run: bash .harness/scripts/verify.sh --ci
      - run: bash .harness/scripts/harness-check.sh --ci
""")
        self.write(root, ".claude/settings.json", "{}\n")
        self.write(root, ".cursor/hooks.json", "{}\n")
        self.write(root, ".codebuddy/settings.json", "{}\n")
        self.write(root, ".codex/hooks.json", "{}\n")

    def test_strong_repo_scores_evidence_not_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.strong_fixture(root)
            report = harness_score.scan(root, ["working-tree", "ci"])

            self.assertGreaterEqual(report["score"]["value"], 80)
            self.assertFalse(report["score"]["caps"])
            self.assertEqual(report["score"]["decision"], "CONDITIONAL")
            self.assertEqual(report["executions"][0]["exitCode"], 0)
            self.assertEqual(report["executions"][0]["governanceCounts"], [728])
            self.assertEqual(report["executions"][0]["failureLabels"], [])
            self.assertGreater(report["counts"]["runtimeSignals"], 0)

    def test_weak_repo_is_hard_capped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "README.md", "A beautiful Harness Skill with great governance.\n")
            report = harness_score.scan(root)
            cap_ids = {item["id"] for item in report["score"]["caps"]}

            self.assertIn("no_verification_entrypoint", cap_ids)
            self.assertIn("no_ci_parity", cap_ids)
            self.assertIn("no_safety_enforcement", cap_ids)
            self.assertIn("no_negative_regression", cap_ids)
            self.assertIn("no_evidence_contract", cap_ids)
            self.assertLessEqual(report["score"]["value"], 35)
            self.assertEqual(report["score"]["decision"], "BLOCKED")

    def test_markdown_and_schema_fields_are_stable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.strong_fixture(root)
            report = harness_score.scan(root)
            rendered = harness_score.markdown(report)

            self.assertIn("# Harness Scorecard", rendered)
            self.assertIn("## Dimension score", rendered)
            for key in ("schemaVersion", "target", "score", "dimensions", "findings", "hosts", "executions"):
                self.assertIn(key, report)

    def test_domain_profile_is_separate_and_keeps_confidence_honest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "AGENTS.md", "已发布、来源、渠道、视觉验收、外部副作用、预检。\n")
            self.write(root, "README.md", "content agent workflow\n")
            report = harness_score.scan(root, profile="content-agent")

            self.assertIsNotNone(report["profile"])
            self.assertEqual(report["profile"]["id"], "content-agent")
            self.assertLess(report["profile"]["score"]["confidence"], 85)
            self.assertEqual(report["profile"]["score"]["decision"], "CONDITIONAL")

    def test_package_script_is_a_portable_verification_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "package.json", json.dumps({"scripts": {"check:ci": "echo ok"}}))
            self.write(root, ".github/workflows/ci.yml", "run: pnpm run check:ci\n")
            report = harness_score.scan(root)

            self.assertIn("package.json:scripts.check:ci", report["verification"]["entrypoints"])
            self.assertNotIn("no_verification_entrypoint", {item["id"] for item in report["score"]["caps"]})

    def test_machine_path_detector_distinguishes_portable_and_local_docs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.strong_fixture(root)
            portable = harness_score.scan(root)
            portable_dimension = next(item for item in portable["dimensions"] if item["id"] == "docs_portability")
            portable_titles = {item["title"] for item in portable_dimension["signals"]}
            self.assertIn("未发现机器专属路径", portable_titles)

            self.write(root, "README.md", "Local-only example: /" + "Users/example/project\n")
            local = harness_score.scan(root)
            local_dimension = next(item for item in local["dimensions"] if item["id"] == "docs_portability")
            local_titles = {item["title"] for item in local_dimension["signals"]}
            self.assertIn("发现机器专属路径", local_titles)

    def test_live_terminal_mode_keeps_progress_and_colored_verdict_separate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.strong_fixture(root)
            trace = io.StringIO()
            with contextlib.redirect_stderr(trace):
                report = harness_score.scan(root, ["ci"], live=True, color="never")
            rendered = harness_score.terminal_report(report, colors=False)

            self.assertTrue("RUN ci" in trace.getvalue() or "PREPARE ci" in trace.getvalue())
            self.assertIn("ci · exit 0", rendered)
            self.assertIn("SCORE", rendered)
            self.assertIn("configured ≠ triggered", rendered)


if __name__ == "__main__":
    unittest.main()
