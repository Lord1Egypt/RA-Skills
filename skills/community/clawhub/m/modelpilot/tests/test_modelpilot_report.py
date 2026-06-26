#!/usr/bin/env python3
"""Minimal tests for ModelPilot report logic. These tests do not call Ollama."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "scripts" / "modelpilot_report.py"


def load_report_module():
    spec = importlib.util.spec_from_file_location("modelpilot_report", REPORT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load modelpilot_report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_record(round_number: int, **overrides):
    record = {
        "round": round_number,
        "model": "demo-model:latest",
        "prompt_id": "prompt_001",
        "success": True,
        "format_pass": True,
        "think_leak": False,
        "duration_seconds": 1.0,
        "error": "",
    }
    record.update(overrides)
    return record


def test_one_round_is_candidate_only():
    report = load_report_module()
    decision, reason = report.decision_for_model([fake_record(1)])
    assert decision == "candidate_only"
    assert "Only one" in reason


def test_two_clean_rounds_are_replace_ready():
    report = load_report_module()
    records = [fake_record(1), fake_record(2)]
    decision, reason = report.decision_for_model(records)
    assert decision == "replace_ready"
    assert "Two rounds" in reason


def test_think_leak_is_not_recommended():
    report = load_report_module()
    records = [fake_record(1), fake_record(2, think_leak=True)]
    decision, reason = report.decision_for_model(records)
    assert decision == "not_recommended"
    assert "thinking leakage" in reason


def test_format_failure_is_observe():
    report = load_report_module()
    records = [fake_record(1), fake_record(2, format_pass=False)]
    decision, reason = report.decision_for_model(records)
    assert decision == "observe"
    assert "format" in reason


if __name__ == "__main__":
    test_one_round_is_candidate_only()
    test_two_clean_rounds_are_replace_ready()
    test_think_leak_is_not_recommended()
    test_format_failure_is_observe()
    print("All ModelPilot report tests passed.")

