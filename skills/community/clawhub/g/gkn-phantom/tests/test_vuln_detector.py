#!/usr/bin/env python3
"""Tests for vuln_detector.py — severity-tiered detection engine."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import vuln_detector as vd


# ---------------------------------------------------------------------------
# build_plan tests
# ---------------------------------------------------------------------------


def test_build_plan_all_tiers(sample_assets):
    """Building a plan with all tiers should produce a non-empty plan."""
    plan = vd.build_plan(
        sample_assets,
        tiers=["low", "medium", "high", "critical"],
        safe_mode=False,
        include_l4=True,
    )
    assert len(plan) > 0
    # Every entry should have the required fields from candidate_finding()
    for item in plan:
        assert "type" in item
        assert "severity" in item
        assert "tier" in item
        assert "target" in item
        assert item["status"] == "detected"


def test_build_plan_safe_mode(sample_assets):
    """When safe_mode is True, L4/blocked_in_safe_mode rules must be excluded."""
    plan = vd.build_plan(
        sample_assets,
        tiers=["low", "medium", "high", "critical"],
        safe_mode=True,
        include_l4=False,
    )
    # No rule with blocked_in_safe_mode=True should appear
    for item in plan:
        assert item.get("blocked_in_safe_mode") is not True

    # Every L4 rule is also blocked_in_safe_mode — double-check consistency
    l4_rules = [
        r
        for tier_rules in vd.TIER_RULES.values()
        for r in tier_rules
        if r.risk_level == "L4"
    ]
    for rule in l4_rules:
        assert rule.blocked_in_safe_mode is True


def test_build_plan_include_l4(sample_assets):
    """When safe_mode is False and include_l4 is True, L4 rules appear."""
    plan_without_l4 = vd.build_plan(
        sample_assets,
        tiers=["low", "medium", "high", "critical"],
        safe_mode=False,
        include_l4=False,
    )
    plan_with_l4 = vd.build_plan(
        sample_assets,
        tiers=["low", "medium", "high", "critical"],
        safe_mode=False,
        include_l4=True,
    )
    # Plan with L4 should have strictly more entries (or at least not fewer)
    assert len(plan_with_l4) >= len(plan_without_l4)

    # At least one L4 entry should be present in the L4-included plan
    l4_types = {"rce", "ssrf", "http_smuggling"}
    l4_entries = [
        item for item in plan_with_l4 if item.get("type") in l4_types
    ]
    assert len(l4_entries) > 0


# ---------------------------------------------------------------------------
# classify_data_exposure tests
# ---------------------------------------------------------------------------


def test_classify_data_exposure_triggered():
    """A body containing 10+ emails should score >= 3 (triggered)."""
    emails = "\n".join(
        f"user{i}@example.com" for i in range(1, 13)
    )
    body = f"Leaked user data:\n{emails}\nEnd of data."
    triggered, score = vd.classify_data_exposure(body)
    assert triggered is True
    assert score >= 3


def test_classify_data_exposure_not_triggered():
    """A clean body with no PII should score < 3 (not triggered)."""
    body = "<html><body><h1>Welcome</h1><p>This is a normal page.</p></body></html>"
    triggered, score = vd.classify_data_exposure(body)
    assert triggered is False
    assert score < 3


def test_classify_data_exposure_phones_detected():
    """5+ phone numbers should be detected and contribute to the score."""
    phones = "\n".join(
        f"({area}) 555-{n:04d}" for area, n in [(212, 1234), (310, 5678),
                                                  (415, 9012), (650, 3456),
                                                  (408, 7890)]
    )
    body = f"Phone directory:\n{phones}"
    triggered, score = vd.classify_data_exposure(body)
    # Phones alone contribute 2 points (not enough to trigger alone, need >=3)
    assert score >= 2


def test_classify_data_exposure_ssn_trigger():
    """SSN patterns should trigger data exposure."""
    body = "Employee SSN list: 123-45-6789, 987-65-4321, 111-22-3333"
    triggered, score = vd.classify_data_exposure(body)
    assert triggered is True
    assert score >= 3


def test_classify_data_exposure_secret_keys_trigger():
    """Hardcoded secret keys / passwords should trigger data exposure."""
    body = '''
    {
        "password": "SuperSecret123!",
        "api_key": "sk-abcdef1234567890",
        "token": "eyJhbGciOiJIUzI1NiJ9.abc.def"
    }
    '''
    triggered, score = vd.classify_data_exposure(body)
    assert triggered is True
    assert score >= 3


# ---------------------------------------------------------------------------
# SEVERITY_BY_TYPE consistency
# ---------------------------------------------------------------------------

VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def test_severity_by_type_consistency():
    """Every vulnerability type must map to a valid severity."""
    for vuln_type, severity in vd.SEVERITY_BY_TYPE.items():
        assert severity in VALID_SEVERITIES, (
            f"Type '{vuln_type}' maps to invalid severity '{severity}'"
        )


def test_all_tiers_have_rules():
    """Every tier (low/medium/high/critical) must have at least one rule."""
    for tier in vd.TIER_ORDER:
        rules = vd.TIER_RULES.get(tier, [])
        assert len(rules) > 0, f"Tier '{tier}' has no rules"


def test_candidate_finding_fields():
    """candidate_finding() must produce a dict with all expected keys."""
    rule = vd.LOW_RULES[0]
    finding = vd.candidate_finding(rule, "https://example.com/", "GET /test")
    expected_keys = {
        "id", "type", "severity", "tier", "target", "status", "confidence",
        "evidence", "reproducible", "safe_poc", "risk_level",
        "requires_human_approval", "blocked_in_safe_mode", "detection_signal",
    }
    for key in expected_keys:
        assert key in finding, f"Missing key '{key}' in candidate finding"
    assert finding["status"] == "detected"
