#!/usr/bin/env python3
"""Tests for report_generator.py — report assembly, risk scoring, SARIF output."""

from __future__ import annotations

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import report_generator as rg


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_finding(
    fid="f-001",
    vtype="rce",
    severity="critical",
    status="validated",
    target="https://example.com/api/exec",
    **kwargs,
):
    """Build a minimal validated finding dict for tests."""
    f = {
        "id": fid,
        "type": vtype,
        "severity": severity,
        "tier": severity,
        "target": target,
        "status": status,
        "confidence": 0.9,
        "evidence": {
            "request": f"GET {target} HTTP/1.1",
            "response": "HTTP/1.1 200 OK\n\nresult",
            "timestamp": "2025-01-15T10:00:00Z",
            "tool": "test",
        },
        "reproducible": True,
        "safe_poc": True,
        "risk_level": "L2",
        "requires_human_approval": False,
        "blocked_in_safe_mode": False,
        "detection_signal": "Test signal",
        "remediation": "Apply appropriate fix.",
    }
    f.update(kwargs)
    return f


# ---------------------------------------------------------------------------
# Risk score tests
# ---------------------------------------------------------------------------


def test_risk_score_single_critical():
    """A single critical finding -> risk score 25."""
    findings = [_make_finding("f-001", "rce", "critical")]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 25


def test_risk_score_single_high():
    """A single high finding -> risk score 15."""
    findings = [_make_finding("f-002", "sqli", "high")]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 15


def test_risk_score_single_medium():
    """A single medium finding -> risk score 8."""
    findings = [_make_finding("f-003", "xss", "medium")]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 8


def test_risk_score_single_low():
    """A single low finding -> risk score 3."""
    findings = [_make_finding("f-004", "misconfig", "low")]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 3


def test_risk_score_mixed():
    """Mixed severities: critical(25) + high(15) + medium(8) + low(3) = 51."""
    findings = [
        _make_finding("f-001", "rce", "critical"),
        _make_finding("f-002", "sqli", "high"),
        _make_finding("f-003", "xss", "medium"),
        _make_finding("f-004", "misconfig", "low"),
    ]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 51


def test_risk_score_severity_points_mapping():
    """Verify the severity-to-points mapping constants."""
    assert rg.SEVERITY_POINTS == {"critical": 25, "high": 15, "medium": 8, "low": 3}


def test_risk_score_max_100():
    """Score must be capped at 100 even with many critical findings."""
    findings = [
        _make_finding(f"f-{i:03d}", "rce", "critical")
        for i in range(1, 10)
    ]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 100


def test_risk_score_blocked_l4():
    """blocked_l4 flag adds 5 bonus points."""
    findings = [_make_finding("f-001", "rce", "critical")]
    report_no_l4 = rg.build_report(findings, {}, [], [], blocked_l4=False)
    report_l4 = rg.build_report(findings, {}, [], [], blocked_l4=True)
    assert report_l4["risk_score"] == report_no_l4["risk_score"] + 5


def test_risk_score_ignores_non_validated():
    """Only validated findings count toward the risk score."""
    findings = [
        _make_finding("f-001", "rce", "critical", status="validated"),
        _make_finding("f-002", "rce", "critical", status="false_positive"),
        _make_finding("f-003", "rce", "critical", status="detected"),
        _make_finding("f-004", "rce", "critical", status="candidate"),
    ]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 25  # only one validated


def test_risk_score_no_validated():
    """Zero validated findings -> risk score 0."""
    findings = [
        _make_finding("f-001", "rce", "critical", status="false_positive"),
    ]
    report = rg.build_report(findings, {}, [], [])
    assert report["risk_score"] == 0


# ---------------------------------------------------------------------------
# SARIF output tests
# ---------------------------------------------------------------------------


def test_sarif_output_structure():
    """SARIF output must have version, runs, and results fields."""
    findings = [
        _make_finding("f-001", "rce", "critical"),
        _make_finding("f-002", "sqli", "high"),
    ]
    report = rg.build_report(findings, {}, [], [])
    sarif = report["sarif"]

    assert "version" in sarif
    assert sarif["version"] == "2.1.0"
    assert "$schema" in sarif
    assert "runs" in sarif
    assert len(sarif["runs"]) == 1
    assert "results" in sarif["runs"][0]
    assert len(sarif["runs"][0]["results"]) == 2


def test_sarif_only_includes_validated():
    """SARIF results should only include validated findings."""
    findings = [
        _make_finding("f-001", "rce", "critical", status="validated"),
        _make_finding("f-002", "sqli", "high", status="false_positive"),
        _make_finding("f-003", "xss", "medium", status="detected"),
    ]
    report = rg.build_report(findings, {}, [], [])
    sarif = report["sarif"]
    assert len(sarif["runs"][0]["results"]) == 1


def test_sarif_result_has_required_fields():
    """Each SARIF result must have ruleId, level, message, locations, partialFingerprints, properties."""
    findings = [_make_finding("f-001", "rce", "critical")]
    report = rg.build_report(findings, {}, [], [])
    result = report["sarif"]["runs"][0]["results"][0]

    assert "ruleId" in result
    assert "level" in result
    assert "message" in result
    assert "locations" in result
    assert "partialFingerprints" in result
    assert "gkn-phantom/v1" in result["partialFingerprints"]
    assert "properties" in result
    assert result["properties"]["tier"] == "critical"
    assert result["properties"]["severity"] == "critical"


def test_sarif_level_mapping():
    """SARIF level should map correctly: critical/high=error, medium=warning, low=note."""
    findings = [
        _make_finding("f-001", "rce", "critical"),
        _make_finding("f-002", "sqli", "high"),
        _make_finding("f-003", "xss", "medium"),
        _make_finding("f-004", "misconfig", "low"),
    ]
    report = rg.build_report(findings, {}, [], [])
    results = report["sarif"]["runs"][0]["results"]
    levels = {r["properties"]["severity"]: r["level"] for r in results}

    assert levels["critical"] == "error"
    assert levels["high"] == "error"
    assert levels["medium"] == "warning"
    assert levels["low"] == "note"


def test_sarif_empty_when_no_validated():
    """SARIF results should be empty when no findings are validated."""
    findings = [_make_finding("f-001", "rce", "critical", status="false_positive")]
    report = rg.build_report(findings, {}, [], [])
    assert len(report["sarif"]["runs"][0]["results"]) == 0


# ---------------------------------------------------------------------------
# Summary tests
# ---------------------------------------------------------------------------


def test_summary_contains_counts():
    """Summary must mention finding counts and risk score."""
    findings = [
        _make_finding("f-001", "rce", "critical"),
        _make_finding("f-002", "sqli", "high", status="false_positive"),
        _make_finding("f-003", "xss", "medium"),
    ]
    report = rg.build_report(findings, {}, [], [])
    summary = report["summary"]

    # critical(25) + medium(8) = 33
    assert "33/100" in summary
    assert "2 validated" in summary
    assert "1 false positive" in summary


def test_summary_no_validated():
    """Summary should say 'No validated findings' when none exist."""
    findings = [_make_finding("f-001", "rce", "critical", status="false_positive")]
    report = rg.build_report(findings, {}, [], [])
    assert "No validated findings" in report["summary"]


def test_summary_blocked_l4_note():
    """Summary should mention L4 blocking when blocked_l4 is True."""
    findings = [_make_finding("f-001", "rce", "critical")]
    report = rg.build_report(findings, {}, [], [], blocked_l4=True)
    assert "L4" in report["summary"]


# ---------------------------------------------------------------------------
# Report structure tests
# ---------------------------------------------------------------------------


def test_report_has_all_sections():
    """Full report must contain all expected top-level keys."""
    findings = [_make_finding("f-001", "rce", "critical")]
    assets = {"domains": ["example.com"]}
    paths = [{"id": "p-001", "name": "Test path"}]
    log = [{"ts": "2025-01-15T10:00:00Z", "state": "INIT", "msg": "Start"}]

    report = rg.build_report(findings, assets, paths, log)

    expected_keys = {
        "summary", "risk_score", "assets", "findings",
        "attack_paths", "recommendations", "sarif", "execution_log",
    }
    for key in expected_keys:
        assert key in report, f"Missing key '{key}' in report"


def test_report_findings_only_safe_poc():
    """Report findings should only include those with safe_poc=True."""
    findings = [
        _make_finding("f-001", "rce", "critical", safe_poc=True),
        _make_finding("f-002", "sqli", "high", safe_poc=False),
        _make_finding("f-003", "xss", "medium", safe_poc=True),
    ]
    report = rg.build_report(findings, {}, [], [])
    report_findings = report["findings"]
    # safe_poc=False findings should NOT be in the report output
    for f in report_findings:
        assert f.get("safe_poc") is True


def test_recommendations_deduplicated():
    """Recommendations should not repeat for the same vulnerability type."""
    findings = [
        _make_finding("f-001", "rce", "critical"),
        _make_finding("f-002", "rce", "critical", target="https://other.com/rce"),
        _make_finding("f-003", "sqli", "high"),
    ]
    report = rg.build_report(findings, {}, [], [])
    recs = report["recommendations"]
    # rce should appear once
    rce_recs = [r for r in recs if "[rce]" in r]
    assert len(rce_recs) == 1


def test_build_report_does_not_modify_input():
    """build_report should not mutate its input lists."""
    findings = [
        _make_finding("f-001", "rce", "critical"),
        _make_finding("f-002", "sqli", "high"),
    ]
    original_len = len(findings)
    original_type = findings[0]["type"]
    _ = rg.build_report(findings, {}, [], [])
    assert len(findings) == original_len
    assert findings[0]["type"] == original_type
