#!/usr/bin/env python3
"""Tests for rules_loader.py — configuration-driven rule engine."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import rules_loader as rl


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_registry():
    """Reset the global registry cache between tests so each test
    gets a fresh load."""
    rl.reset_registry()
    yield
    rl.reset_registry()


@pytest.fixture
def registry():
    """Return a freshly-loaded RuleRegistry."""
    reg = rl.RuleRegistry()
    reg.load_directory()
    return reg


# ---------------------------------------------------------------------------
# load_all_rules
# ---------------------------------------------------------------------------


def test_load_all_rules(registry):
    """Loading all rules from ../rules/ should yield more than 30 rules."""
    count = registry.rule_count
    assert count > 30, f"Expected >30 rules, got {count}"


def test_load_directory_returns_count(registry):
    """load_directory() returns the count of successfully loaded rules."""
    count = registry.rule_count
    assert isinstance(count, int)
    assert count > 0


# ---------------------------------------------------------------------------
# Rules by tier
# ---------------------------------------------------------------------------


def test_rules_by_tier_low(registry):
    """Low tier must have at least one rule."""
    low_rules = registry.get_rules_by_tier("low")
    assert len(low_rules) > 0


def test_rules_by_tier_medium(registry):
    """Medium tier must have at least one rule."""
    medium_rules = registry.get_rules_by_tier("medium")
    assert len(medium_rules) > 0


def test_rules_by_tier_high(registry):
    """High tier must have at least one rule."""
    high_rules = registry.get_rules_by_tier("high")
    assert len(high_rules) > 0


def test_rules_by_tier_critical(registry):
    """Critical tier must have at least one rule."""
    critical_rules = registry.get_rules_by_tier("critical")
    assert len(critical_rules) > 0


def test_rules_by_tier_invalid(registry):
    """Querying a nonexistent tier should return an empty list."""
    invalid = registry.get_rules_by_tier("nonexistent")
    assert invalid == []


# ---------------------------------------------------------------------------
# Rule schema validation
# ---------------------------------------------------------------------------


REQUIRED_FIELDS = [
    "id", "type", "severity", "tier", "risk_level",
    "probe_description", "detection_signal",
]


def test_rule_schema_valid(registry):
    """Every loaded rule must contain all required fields."""
    for rule in registry.get_all_rules():
        for field in REQUIRED_FIELDS:
            value = getattr(rule, field, None)
            assert value is not None and value != "", (
                f"Rule id='{rule.id}' missing required field '{field}'"
            )


def test_valid_severities(registry):
    """Every rule's severity must be in VALID_SEVERITIES."""
    for rule in registry.get_all_rules():
        assert rule.severity in rl.VALID_SEVERITIES, (
            f"Rule id='{rule.id}': invalid severity '{rule.severity}'"
        )


def test_valid_tiers(registry):
    """Every rule's tier must be in VALID_TIERS."""
    for rule in registry.get_all_rules():
        assert rule.tier in rl.VALID_TIERS, (
            f"Rule id='{rule.id}': invalid tier '{rule.tier}'"
        )


def test_valid_risk_levels(registry):
    """Every rule's risk_level must be in VALID_RISK_LEVELS."""
    for rule in registry.get_all_rules():
        assert rule.risk_level in rl.VALID_RISK_LEVELS, (
            f"Rule id='{rule.id}': invalid risk_level '{rule.risk_level}'"
        )


def test_type_non_empty(registry):
    """Every rule's type must be a non-empty string."""
    for rule in registry.get_all_rules():
        assert isinstance(rule.type, str), f"Rule id='{rule.id}': type is not a string"
        assert rule.type != "", f"Rule id='{rule.id}': type is empty"


def test_target_param_hints_is_list(registry):
    """Every rule's target_param_hints must be a list."""
    for rule in registry.get_all_rules():
        assert isinstance(rule.target_param_hints, list), (
            f"Rule id='{rule.id}': target_param_hints is not a list"
        )


def test_boolean_fields_types(registry):
    """Optional boolean fields must be actual booleans if present."""
    bool_fields = [
        "safe_poc", "requires_credentials",
        "requires_human_approval", "blocked_in_safe_mode",
    ]
    for rule in registry.get_all_rules():
        for field in bool_fields:
            value = getattr(rule, field, None)
            if value is not None:
                assert isinstance(value, bool), (
                    f"Rule id='{rule.id}': '{field}' is not a boolean, "
                    f"got {type(value).__name__}"
                )


# ---------------------------------------------------------------------------
# Validate rules (no errors for valid rules)
# ---------------------------------------------------------------------------


def test_validate_rules_no_errors(registry):
    """After loading valid YAML rules, the registry should report zero
    schema errors in the detection rule files.

    Note: mutation_strategies.yaml and waf_signatures.yaml are auxiliary
    config files (not detection rules), so validation errors from those
    files are expected and ignored here.
    """
    errors = registry.errors
    # Filter out errors from non-rule config files
    schema_errors = [
        e for e in errors
        if (
            "Missing required field" in e
            or "must be a" in e
            or "must be one of" in e
        )
        and "mutation_strategies.yaml" not in e
        and "waf_signatures.yaml" not in e
    ]
    assert len(schema_errors) == 0, (
        f"Schema validation errors in detection rule files: {schema_errors}"
    )


def test_validate_single_valid_rule():
    """_validate_rule should return NO errors for a completely valid rule dict."""
    valid_rule = {
        "id": "test-rule-001",
        "type": "sqli",
        "severity": "high",
        "tier": "high",
        "risk_level": "L2",
        "target_param_hints": ["id", "q"],
        "probe_description": "Test SQL injection with error-based payload.",
        "detection_signal": "SQL error in response",
        "safe_poc": True,
        "requires_credentials": False,
        "requires_human_approval": False,
        "blocked_in_safe_mode": False,
    }
    errors = rl._validate_rule(valid_rule, "test.yaml", 1)
    assert errors == [], f"Expected no errors, got: {errors}"


def test_validate_rule_missing_field():
    """_validate_rule should report errors for missing required fields."""
    invalid_rule = {
        "id": "bad-rule",
        "type": "sqli",
        # missing severity, tier, risk_level, etc.
    }
    errors = rl._validate_rule(invalid_rule, "test.yaml", 1)
    assert len(errors) > 0
    assert any("severity" in e.lower() or "tier" in e.lower() for e in errors)


def test_validate_rule_bad_severity():
    """_validate_rule should reject an invalid severity value."""
    bad_rule = {
        "id": "bad-sev",
        "type": "xss",
        "severity": "super_critical",
        "tier": "medium",
        "risk_level": "L2",
        "target_param_hints": ["q"],
        "probe_description": "Test.",
        "detection_signal": "Signal.",
    }
    errors = rl._validate_rule(bad_rule, "test.yaml", 1)
    assert len(errors) > 0
    assert any("severity" in e.lower() for e in errors)


def test_validate_rule_bad_tier():
    """_validate_rule should reject an invalid tier value."""
    bad_rule = {
        "id": "bad-tier",
        "type": "xss",
        "severity": "medium",
        "tier": "extreme",
        "risk_level": "L2",
        "target_param_hints": ["q"],
        "probe_description": "Test.",
        "detection_signal": "Signal.",
    }
    errors = rl._validate_rule(bad_rule, "test.yaml", 1)
    assert len(errors) > 0
    assert any("tier" in e.lower() for e in errors)


def test_validate_rule_bad_risk_level():
    """_validate_rule should reject an invalid risk level value."""
    bad_rule = {
        "id": "bad-rl",
        "type": "xss",
        "severity": "medium",
        "tier": "medium",
        "risk_level": "L99",
        "target_param_hints": ["q"],
        "probe_description": "Test.",
        "detection_signal": "Signal.",
    }
    errors = rl._validate_rule(bad_rule, "test.yaml", 1)
    assert len(errors) > 0
    assert any("risk_level" in e.lower() for e in errors)


def test_validate_rule_bad_target_param_hints():
    """_validate_rule should reject non-list target_param_hints."""
    bad_rule = {
        "id": "bad-hints",
        "type": "xss",
        "severity": "medium",
        "tier": "medium",
        "risk_level": "L2",
        "target_param_hints": "q",
        "probe_description": "Test.",
        "detection_signal": "Signal.",
    }
    errors = rl._validate_rule(bad_rule, "test.yaml", 1)
    assert len(errors) > 0
    assert any("target_param_hints" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# Reload
# ---------------------------------------------------------------------------


def test_reload_rules(registry):
    """reload() should work without errors and return a valid count."""
    count_before = registry.rule_count
    count_after = registry.reload(force=True)
    assert count_after == count_before
    assert count_after > 0


def test_reload_no_directory():
    """reload() on a registry with no directory loaded returns -1."""
    reg = rl.RuleRegistry()
    result = reg.reload()
    assert result == -1


# ---------------------------------------------------------------------------
# Query methods
# ---------------------------------------------------------------------------


def test_get_rules_by_type(registry):
    """get_rules_by_type should return rules matching the vulnerability type."""
    sqli_rules = registry.get_rules_by_type("sqli")
    assert len(sqli_rules) > 0
    for r in sqli_rules:
        assert r.type == "sqli"


def test_get_rules_by_severity(registry):
    """get_rules_by_severity should return rules matching the severity."""
    critical_rules = registry.get_rules_by_severity("critical")
    assert len(critical_rules) > 0
    for r in critical_rules:
        assert r.severity == "critical"


def test_get_rule_by_id(registry):
    """get_rule_by_id should return the rule with the given ID."""
    all_rules = registry.get_all_rules()
    assert len(all_rules) > 0
    first_id = all_rules[0].id
    found = registry.get_rule_by_id(first_id)
    assert found is not None
    assert found.id == first_id


def test_get_rule_by_nonexistent_id(registry):
    """get_rule_by_id with a nonexistent ID should return None."""
    found = registry.get_rule_by_id("nonexistent-rule-id-xyz")
    assert found is None


def test_get_vuln_types(registry):
    """get_vuln_types should return a sorted list of unique types."""
    types = registry.get_vuln_types()
    assert len(types) > 0
    assert types == sorted(types)
    assert "sqli" in types or "rce" in types


def test_get_tiers(registry):
    """get_tiers should return a sorted list of tiers present."""
    tiers = registry.get_tiers()
    assert len(tiers) > 0
    assert tiers == sorted(tiers)


def test_get_stats(registry):
    """get_stats should return a dict with expected keys."""
    stats = registry.get_stats()
    assert "total_rules" in stats
    assert "by_tier" in stats
    assert "by_type" in stats
    assert "by_severity" in stats
    assert stats["total_rules"] > 0


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def test_export_rules(registry):
    """export_rules should return a list of dicts."""
    exported = registry.export_rules(tier="low")
    assert isinstance(exported, list)
    assert len(exported) > 0
    for item in exported:
        assert isinstance(item, dict)
        assert item.get("tier") == "low"


def test_export_as_json(registry):
    """export_as_json should return a valid JSON string."""
    json_str = registry.export_as_json(tier="medium")
    assert isinstance(json_str, str)
    assert len(json_str) > 0
    # Should be valid JSON
    import json
    parsed = json.loads(json_str)
    assert isinstance(parsed, list)


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------


def test_load_rules_convenience():
    """The module-level load_rules() should return a populated registry."""
    rl.reset_registry()
    reg = rl.load_rules()
    assert reg.rule_count > 0
