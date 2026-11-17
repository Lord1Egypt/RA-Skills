#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""Tests for scripts/validate_run.py (v1.10.2).

Covers GATE 1-6 with synthetic run_dir + results.jsonl fixtures.
Each gate has a positive (passes) and negative (INVALID) case.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate_run.py"


def _run(run_dir: Path, recs: list[dict]) -> subprocess.CompletedProcess:
    jsonl = run_dir / "results.jsonl"
    jsonl.write_text("\n".join(json.dumps(r) for r in recs), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(VALIDATE), str(run_dir), str(jsonl)],
        cwd=str(ROOT), capture_output=True, text=True,
    )


def _make_arm(run_dir: Path, test_id: str, arm: str, files: dict = None) -> Path:
    d = run_dir / f"{test_id}-{arm}"
    d.mkdir(parents=True, exist_ok=True)
    if files is not None:
        for name, content in files.items():
            (d / name).write_text(content, encoding="utf-8")
    else:
        (d / "solution.py").write_text("print('agent worked')\n", encoding="utf-8")
    return d


def test_gate1_zero_api_calls_is_invalid():
    """PASS with api_calls=0 in both arms -> fabricated (no agent ran)."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T1", "control")
        _make_arm(rd, "T1", "treatment")
        rec = {"test_id": "T1", "verdict": "PASS",
               "api_calls_control": 0, "api_calls_treatment": 0}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 1 should flag zero api_calls, got rc=0: {r.stdout}"
        assert "no agent ran" in r.stdout


def test_gate1_real_api_calls_passes():
    """PASS with real api_calls -> valid."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T2", "control")
        _make_arm(rd, "T2", "treatment")
        rec = {"test_id": "T2", "verdict": "PASS",
               "api_calls_control": 11, "api_calls_treatment": 12}
        r = _run(rd, [rec])
        assert r.returncode == 0, f"GATE 1 valid case failed: {r.stdout}"


def test_gate2_empty_arm_is_invalid():
    """Control arm has no model-produced files -> INVALID."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T3", "control", files={})  # empty
        _make_arm(rd, "T3", "treatment")
        rec = {"test_id": "T3", "verdict": "PASS",
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 2 should flag empty arm, got rc=0: {r.stdout}"
        assert "no model-produced files" in r.stdout


def test_gate3_identical_claim_mismatch_is_invalid():
    """Evidence says identical but calc.py differs on disk -> INVALID."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        c = _make_arm(rd, "T4", "control")
        t = _make_arm(rd, "T4", "treatment")
        (c / "calc.py").write_text("x=1\n", encoding="utf-8")
        (t / "calc.py").write_text("x=2\n", encoding="utf-8")  # differs
        rec = {"test_id": "T4", "verdict": "NO-DIFF",
               "evidence": "calc.py is identical between arms",
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 3 should flag mismatch, got rc=0: {r.stdout}"
        assert "sha mismatch" in r.stdout


def test_gate4_contamination_is_invalid():
    """Control arm was given the skill -> contamination, not a control."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T5", "control")
        _make_arm(rd, "T5", "treatment")
        rec = {"test_id": "T5", "verdict": "NO-DIFF",
               "evidence": "both arms were dispatched with skill_view",
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 4 should flag contamination, got rc=0: {r.stdout}"
        assert "contamination" in r.stdout


def test_gate5_fabricated_tool_finding_is_invalid():
    """Evidence claims circular dep found, but madge output says none -> INVALID."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        c = _make_arm(rd, "T6", "control")
        t = _make_arm(rd, "T6", "treatment")
        (t / "madge_output.txt").write_text("No circular dependency found\n", encoding="utf-8")
        rec = {"test_id": "T6", "verdict": "PASS",
               "evidence": "Found 1 circular dependency via madge",
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 5 should flag fabricated finding, got rc=0: {r.stdout}"
        assert "Fabricated" in r.stdout


def test_gate6_cross_run_contamination_is_invalid():
    """Evidence cites a different run dir -> cross-run contamination."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T7", "control")
        _make_arm(rd, "T7", "treatment")
        rec = {"test_id": "T7", "verdict": "PASS",
               "evidence": "see keelwright-qa/1784583906 for details",
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 6 should flag cross-run, got rc=0: {r.stdout}"
        assert "cross-run contamination" in r.stdout


def test_gate7_missing_review_record_is_invalid():
    """requires_review=true but no review_report/review field -> INVALID."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T10", "control")
        _make_arm(rd, "T10", "treatment")
        rec = {"test_id": "T10", "verdict": "PASS",
               "requires_review": True,
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 7 should flag missing review, got rc=0: {r.stdout}"
        assert "Review request not recorded" in r.stdout


def test_gate8_review_missing_diff_attestation_is_invalid():
    """Review mentions tests but does not attest diff/report or red->green -> INVALID."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T11", "control")
        _make_arm(rd, "T11", "treatment")
        rec = {"test_id": "T11", "verdict": "PASS",
               "requires_review": True,
               "review": "I checked the tests and they pass",
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 1, f"GATE 8 should flag weak review, got rc=0: {r.stdout}"
        assert "does not mention diff/report" in r.stdout or "red->green" in r.stdout


def test_gate8_review_complete_passes():
    """Review with diff report + red->green attestation -> valid."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T12", "control")
        _make_arm(rd, "T12", "treatment")
        rec = {"test_id": "T12", "verdict": "PASS",
               "requires_review": True,
               "review": "Review report attached. Diff matches disk. Tests moved from red to green.",
               "api_calls_control": 5, "api_calls_treatment": 5}
        r = _run(rd, [rec])
        assert r.returncode == 0, f"GATE 8 complete review should pass, got rc=1: {r.stdout}"


def test_all_gates_pass_clean_run():
    """A fully clean run with 2 tests passes all gates."""
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td)
        _make_arm(rd, "T8", "control")
        _make_arm(rd, "T8", "treatment")
        _make_arm(rd, "T9", "control")
        _make_arm(rd, "T9", "treatment")
        recs = [
            {"test_id": "T8", "verdict": "PASS",
             "api_calls_control": 11, "api_calls_treatment": 12},
            {"test_id": "T9", "verdict": "NO-DIFF",
             "evidence": "arms differ as expected, no identical claim",
             "api_calls_control": 8, "api_calls_treatment": 9},
        ]
        r = _run(rd, recs)
        assert r.returncode == 0, f"clean run should pass, got rc=1: {r.stdout}"
