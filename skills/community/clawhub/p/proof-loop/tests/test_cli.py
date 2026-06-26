from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "scripts" / "init_task.py"
CHECK = ROOT / "scripts" / "check_task.py"
BIN_INIT = ROOT / "bin" / "proof-loop-init"
BIN_CHECK = ROOT / "bin" / "proof-loop-check"


def run(*args: object, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(a) for a in args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


class ProofLoopCliTests(unittest.TestCase):
    def test_init_task_creates_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run("python3", INIT, "demo-task", "--title", "Demo task", "--root", tmp)
            self.assertEqual(result.returncode, 0, result.stdout)
            task_dir = Path(tmp) / ".agent" / "tasks" / "demo-task"
            self.assertTrue((task_dir / "spec.md").exists())
            self.assertTrue((task_dir / "verdict.json").exists())
            self.assertTrue((task_dir / "problems.md").exists())
            self.assertTrue((task_dir / "evidence.md").exists())

    def test_invalid_task_ids_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for task_id in ("bad/slash", ".hidden"):
                result = run("python3", INIT, task_id, "--root", tmp)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Invalid task id", result.stdout)

    def test_unverified_task_fails_done_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            init = run("python3", INIT, "unverified", "--root", tmp)
            self.assertEqual(init.returncode, 0, init.stdout)
            result = run("python3", CHECK, Path(tmp) / ".agent" / "tasks" / "unverified")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PROOF_LOOP_FAIL", result.stdout)
            self.assertIn("UNKNOWN", result.stdout)

    def test_completed_example_passes_done_gate(self) -> None:
        result = run("python3", CHECK, ROOT / "examples" / "example-task" / ".agent" / "tasks" / "ui-language-fix")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PROOF_LOOP_PASS", result.stdout)

    def test_invalid_json_fails_done_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / ".agent" / "tasks" / "bad-json"
            task_dir.mkdir(parents=True)
            (task_dir / "spec.md").write_text("# Task\n", encoding="utf-8")
            (task_dir / "verdict.json").write_text("{bad json", encoding="utf-8")
            (task_dir / "problems.md").write_text("", encoding="utf-8")
            result = run("python3", CHECK, task_dir)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid JSON", result.stdout)

    def test_non_empty_problems_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / ".agent" / "tasks" / "has-problems"
            task_dir.mkdir(parents=True)
            (task_dir / "spec.md").write_text("# Task\n", encoding="utf-8")
            (task_dir / "verdict.json").write_text(
                json.dumps({
                    "task_id": "has-problems",
                    "phase": "verify",
                    "agent": "test",
                    "timestamp": "2026-05-20T00:00:00Z",
                    "overall": "PASS",
                    "criteria": [{"id": "AC1", "status": "PASS", "note": "ok"}],
                }),
                encoding="utf-8",
            )
            (task_dir / "problems.md").write_text("# Still broken\n", encoding="utf-8")
            result = run("python3", CHECK, task_dir)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("problems.md is not empty", result.stdout)

    def test_wrappers_work_from_another_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            external = Path(tmp) / "other-repo"
            external.mkdir()
            init = run(BIN_INIT, "external-task", "--title", "External task", "--root", ".", cwd=external)
            self.assertEqual(init.returncode, 0, init.stdout)
            task_dir = external / ".agent" / "tasks" / "external-task"
            self.assertTrue(task_dir.exists())
            check = run(BIN_CHECK, task_dir, cwd=external)
            self.assertNotEqual(check.returncode, 0)
            self.assertIn("PROOF_LOOP_FAIL", check.stdout)

    def test_unified_cli_status_list_doctor_report_and_validate(self) -> None:
        report_task = ROOT / "examples" / "demo-repo" / ".agent" / "tasks" / "nav-labels-proof"
        doctor = run(ROOT / "bin" / "proof-loop", "doctor")
        self.assertEqual(doctor.returncode, 0, doctor.stdout)
        self.assertIn("PROOF_LOOP_DOCTOR_PASS", doctor.stdout)

        status = run(ROOT / "bin" / "proof-loop", "status", report_task)
        self.assertEqual(status.returncode, 0, status.stdout)
        self.assertIn("overall=PASS", status.stdout)

        listing = run(ROOT / "bin" / "proof-loop", "list", "--root", ROOT / "examples" / "demo-repo")
        self.assertEqual(listing.returncode, 0, listing.stdout)
        self.assertIn("nav-labels-proof", listing.stdout)

        validate = run(ROOT / "bin" / "proof-loop", "validate", report_task, "--require-evidence-json")
        self.assertEqual(validate.returncode, 0, validate.stdout)
        self.assertIn("PROOF_LOOP_SCHEMA_PASS", validate.stdout)

        report = run(ROOT / "bin" / "proof-loop", "report", report_task, "--format", "md")
        self.assertEqual(report.returncode, 0, report.stdout)
        self.assertIn("# Proof Report - nav-labels-proof", report.stdout)
        self.assertIn("| AC1 | PASS |", report.stdout)
        self.assertIn("raw/check-nav-labels.txt", report.stdout)

    def test_install_guides_dry_run_does_not_mutate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run(
                ROOT / "bin" / "proof-loop",
                "install-guides",
                "--root",
                root,
                "--dry-run",
                "--harness",
                "codex",
                "--harness",
                "claude",
                "--harness",
                "opencode",
                "--harness",
                "hermes",
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("DRY_RUN codex", result.stdout)
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertFalse((root / "CLAUDE.md").exists())

    def test_demo_script_runs_fail_fix_pass_flow(self) -> None:
        result = run("python3", ROOT / "examples" / "demo-repo" / "run_demo.py")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("NAV_LABEL_CHECK_FAIL", result.stdout)
        self.assertIn("NAV_LABEL_CHECK_PASS", result.stdout)
        self.assertIn("# Proof Report - nav-labels-proof", result.stdout)


if __name__ == "__main__":
    unittest.main()
