from pathlib import Path

import pytest

from scripts.context_isolation import (
    build_context_snapshot,
    build_ir_snapshot,
    build_naive_context_snapshot,
    compare_snapshots,
    extract_ir_from_context,
)


ROOT = Path(__file__).resolve().parent.parent

CASE_PATHS = [
    (
        ROOT / "evals" / "cases" / "zh-ai-collaboration" / "report.report.md",
        ROOT / "evals" / "cases" / "zh-ai-collaboration" / "noise-context.md",
    ),
    (
        ROOT / "evals" / "cases" / "en-ops-weekly" / "report.report.md",
        ROOT / "evals" / "cases" / "en-ops-weekly" / "noise-context.md",
    ),
    (
        ROOT / "evals" / "cases" / "zh-quarterly-growth" / "report.report.md",
        ROOT / "evals" / "cases" / "zh-quarterly-growth" / "noise-context.md",
    ),
]


def test_extract_ir_from_noise_context_matches_case_ir():
    for ir_path, context_path in CASE_PATHS:
        expected = ir_path.read_text(encoding="utf-8").strip()
        context = context_path.read_text(encoding="utf-8")
        assert extract_ir_from_context(context).strip() == expected


def test_extract_ir_rejects_missing_ir_block():
    with pytest.raises(ValueError, match="No valid IR block"):
        extract_ir_from_context("User: discuss architecture later\nAssistant: no IR here")


def test_extract_ir_rejects_multiple_ir_blocks():
    context = """---
title: One
---

## A

Text.
<<<END_IR>>>
---
title: Two
---

## B

Text.
<<<END_IR>>>
"""
    with pytest.raises(ValueError, match="Multiple valid IR blocks"):
        extract_ir_from_context(context)


def test_context_snapshot_matches_bare_ir_snapshot():
    for ir_path, context_path in CASE_PATHS:
        bare = build_ir_snapshot(ir_path.read_text(encoding="utf-8"))
        isolated = build_context_snapshot(context_path.read_text(encoding="utf-8"))
        assert compare_snapshots(bare, isolated) == []


def test_naive_context_snapshot_shows_route_drift():
    drift_seen = 0
    for ir_path, context_path in CASE_PATHS:
        bare = build_ir_snapshot(ir_path.read_text(encoding="utf-8"))
        noisy = build_naive_context_snapshot(context_path.read_text(encoding="utf-8"))
        drift_fields = compare_snapshots(
            bare,
            noisy,
            keys=["resolved_theme", "resolved_report_class", "required_refs"],
        )
        if drift_fields:
            drift_seen += 1
    assert drift_seen >= 2, "Expected noisy wrappers to surface route drift in most fixture cases."
