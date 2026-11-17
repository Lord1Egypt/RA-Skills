#!/usr/bin/env python3
"""Tests for adaptive_engine.py — retry, mutation, WAF fallback engine."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import adaptive_engine as ae


# ---------------------------------------------------------------------------
# WAF detection tests
# ---------------------------------------------------------------------------


def test_detect_waf_cloudflare():
    """Response with cf-ray header -> detected as cloudflare."""
    result = {
        "status_code": 403,
        "headers": {"cf-ray": "abc123", "server": "cloudflare"},
        "body": "Access denied",
    }
    waf_detected, waf_type = ae.detect_waf(result)
    assert waf_detected is True
    assert waf_type == "cloudflare"


def test_detect_waf_modsecurity():
    """Response with ModSecurity body text -> detected as mod_security."""
    result = {
        "status_code": 403,
        "headers": {"server": "Apache"},
        "body": "This request was blocked by Mod_Security. Not acceptable.",
    }
    waf_detected, waf_type = ae.detect_waf(result)
    assert waf_detected is True
    assert waf_type == "mod_security"


def test_detect_waf_safedog():
    """Response with 安全狗 body text -> detected as safedog."""
    result = {
        "status_code": 403,
        "headers": {"server": "nginx"},
        "body": "Blocked by 安全狗 WAF",
    }
    waf_detected, waf_type = ae.detect_waf(result)
    assert waf_detected is True
    assert waf_type == "safedog"


def test_detect_waf_none_clean_200():
    """A clean 200 response with no WAF signals -> no WAF detected."""
    result = {
        "status_code": 200,
        "headers": {"content-type": "text/html", "server": "nginx"},
        "body": "<html><body>Welcome!</body></html>",
    }
    waf_detected, waf_type = ae.detect_waf(result)
    assert waf_detected is False
    assert waf_type is None


def test_detect_waf_generic_403():
    """A 403 with generic 'forbidden' body text -> detected as generic WAF."""
    result = {
        "status_code": 403,
        "headers": {"server": "Apache"},
        "body": "Forbidden.",
    }
    waf_detected, waf_type = ae.detect_waf(result)
    assert waf_detected is True
    assert waf_type == "generic"


def test_detect_waf_none_404():
    """A 404 response without WAF markers -> no WAF detected."""
    result = {
        "status_code": 404,
        "headers": {"server": "nginx"},
        "body": "Page not found.",
    }
    waf_detected, waf_type = ae.detect_waf(result)
    assert waf_detected is False
    assert waf_type is None


# ---------------------------------------------------------------------------
# Failure classification tests
# ---------------------------------------------------------------------------


def test_classify_failure_transient_timeout():
    """A result with timeout error -> classified as 'transient'."""
    result = {"error": "timeout", "status_code": None}
    classification = ae.classify_failure(result)
    assert classification == "transient"


def test_classify_failure_transient_connection_refused():
    """A result with connection_refused -> classified as 'transient'."""
    result = {"error": "connection_refused", "status_code": None}
    classification = ae.classify_failure(result)
    assert classification == "transient"


def test_classify_failure_transient_connection_reset():
    """A result with connection_reset -> classified as 'transient'."""
    result = {"error": "connection_reset", "status_code": None}
    classification = ae.classify_failure(result)
    assert classification == "transient"


def test_classify_failure_waf_blocked_403():
    """403 with Cloudflare WAF fingerprint -> classified as 'waf_blocked'."""
    result = {
        "status_code": 403,
        "headers": {"cf-ray": "xyz789", "server": "cloudflare"},
        "body": "Attention required — Cloudflare",
    }
    classification = ae.classify_failure(result)
    assert classification == "waf_blocked"


def test_classify_failure_waf_blocked_406():
    """406 status -> classified as 'waf_blocked' (no WAF needed)."""
    result = {
        "status_code": 406,
        "headers": {"server": "nginx"},
        "body": "Not acceptable",
    }
    classification = ae.classify_failure(result)
    assert classification == "waf_blocked"


def test_classify_failure_waf_blocked_429():
    """429 status -> classified as 'waf_blocked'."""
    result = {
        "status_code": 429,
        "headers": {"server": "nginx"},
        "body": "Too many requests",
    }
    classification = ae.classify_failure(result)
    assert classification == "waf_blocked"


def test_classify_failure_auth_required():
    """401 without WAF -> classified as 'auth_required'."""
    result = {
        "status_code": 401,
        "headers": {"www-authenticate": "Basic"},
        "body": "Unauthorized",
    }
    classification = ae.classify_failure(result)
    assert classification == "auth_required"


def test_classify_failure_not_found():
    """404 -> classified as 'not_found'."""
    result = {
        "status_code": 404,
        "headers": {"server": "nginx"},
        "body": "Not found",
    }
    classification = ae.classify_failure(result)
    assert classification == "not_found"


def test_classify_failure_server_error():
    """500 status -> classified as 'server_error'."""
    result = {
        "status_code": 500,
        "headers": {"server": "Apache"},
        "body": "Internal Server Error",
    }
    classification = ae.classify_failure(result)
    assert classification == "server_error"


def test_classify_failure_false_negative():
    """200 but signal not matched -> classified as 'false_negative'."""
    result = {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "body": "<html><body>OK but no signal</body></html>",
    }
    classification = ae.classify_failure(result)
    assert classification == "false_negative"


def test_classify_failure_none_result():
    """Empty/None result -> classified as 'transient'."""
    classification = ae.classify_failure(None)
    assert classification == "transient"


# ---------------------------------------------------------------------------
# Mutation generation tests
# ---------------------------------------------------------------------------


def test_generate_mutations_sqli():
    """SQLi payload should generate valid, unique mutations."""
    original = "' OR 1=1 --"
    mutations = ae.generate_mutations("sqli", original, max_variants=5)
    assert len(mutations) > 0
    assert len(mutations) <= 5
    # All mutations should differ from the original
    for m in mutations:
        assert m != original
    # All mutations should be unique
    assert len(mutations) == len(set(mutations))
    # All mutations should be strings
    for m in mutations:
        assert isinstance(m, str)


def test_generate_mutations_xss():
    """XSS payload should generate valid mutation variants."""
    original = "<script>alert(1)</script>"
    mutations = ae.generate_mutations("xss", original, max_variants=5)
    assert len(mutations) > 0
    assert len(mutations) <= 5
    for m in mutations:
        assert m != original
    assert len(mutations) == len(set(mutations))


def test_generate_mutations_command_injection():
    """Command injection payload should generate mutations."""
    original = ";sleep 3 #"
    mutations = ae.generate_mutations("command_injection", original, max_variants=3)
    assert len(mutations) > 0
    for m in mutations:
        assert m != original


def test_generate_mutations_unknown_type():
    """An unknown vulnerability type should return an empty list."""
    mutations = ae.generate_mutations("nonexistent_type", "test", max_variants=5)
    assert mutations == []


def test_generate_mutations_single_variant():
    """max_variants=1 should return exactly one mutation."""
    original = "' OR 1=1 --"
    mutations = ae.generate_mutations("sqli", original, max_variants=1)
    assert len(mutations) == 1


# ---------------------------------------------------------------------------
# Adaptive plan building tests
# ---------------------------------------------------------------------------


def test_build_adaptive_plan_retry_transient():
    """Transient failure should produce a retry plan with exponential backoff."""
    probe = {"type": "sqli", "target": "https://example.com/api?id=1"}
    result = {"error": "timeout", "status_code": None}
    plan = ae.build_adaptive_plan(
        probe, result, vuln_type="sqli", original_payload="' OR 1=1 --",
        attempt=1, max_retries=3,
    )
    assert plan["action"] == "retry"
    assert plan["failure_type"] == "transient"
    assert len(plan["retry_schedule"]) > 0
    # Schedule should have exponential backoff (500, 1000, 2000)
    delays = [s["delay_ms"] for s in plan["retry_schedule"]]
    for i in range(1, len(delays)):
        assert delays[i] >= delays[i - 1]


def test_build_adaptive_plan_mutate_waf_blocked():
    """WAF block should produce a mutation plan with mutated payloads."""
    probe = {"type": "sqli", "target": "https://example.com/api?id=1"}
    result = {
        "status_code": 403,
        "headers": {"server": "cloudflare", "cf-ray": "abc123"},
        "body": "Attention required — Cloudflare",
    }
    plan = ae.build_adaptive_plan(
        probe, result, vuln_type="sqli", original_payload="' OR 1=1 --",
        attempt=1, max_retries=3,
    )
    assert plan["action"] == "mutate"
    assert plan["waf_detected"] is True
    assert plan["waf_type"] == "cloudflare"
    assert "mutated_payloads" in plan
    assert len(plan["mutated_payloads"]) > 0


def test_build_adaptive_plan_false_negative():
    """200 with no signal -> fallback to alternative probe strategies."""
    probe = {"type": "sqli", "target": "https://example.com/api?id=1"}
    result = {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "body": "<html><body>Results for: 1</body></html>",
    }
    plan = ae.build_adaptive_plan(
        probe, result, vuln_type="sqli", original_payload="' OR 1=1 --",
        attempt=1, max_retries=3,
    )
    assert plan["action"] in ("fallback_signal", "abort")
    if plan["action"] == "fallback_signal":
        assert len(plan["alternative_signals"]) > 0
        assert plan["fallback_strategy"] == "secondary_signal"


def test_build_adaptive_plan_auth_required():
    """401 without WAF -> abort with needs_credentials."""
    probe = {"type": "idor", "target": "https://example.com/api/user/1"}
    result = {
        "status_code": 401,
        "headers": {"www-authenticate": "Bearer"},
        "body": "Unauthorized",
    }
    plan = ae.build_adaptive_plan(
        probe, result, vuln_type="idor", original_payload="id=1",
        attempt=1, max_retries=3,
    )
    assert plan["action"] == "abort"
    assert plan["fallback_strategy"] == "needs_credentials"


def test_build_adaptive_plan_not_found():
    """404 -> abort with endpoint_gone fallback."""
    probe = {"type": "xss", "target": "https://example.com/search?q=test"}
    result = {
        "status_code": 404,
        "headers": {"server": "nginx"},
        "body": "Not found",
    }
    plan = ae.build_adaptive_plan(
        probe, result, vuln_type="xss", original_payload="<script>alert(1)</script>",
        attempt=1, max_retries=3,
    )
    assert plan["action"] == "abort"
    assert plan["fallback_strategy"] == "endpoint_gone"


def test_build_adaptive_plan_server_error_retry():
    """500 on first attempt -> retry once."""
    probe = {"type": "sqli", "target": "https://example.com/api?id=1"}
    result = {
        "status_code": 500,
        "headers": {"server": "Apache"},
        "body": "Internal Server Error",
    }
    plan = ae.build_adaptive_plan(
        probe, result, vuln_type="sqli", original_payload="' OR 1=1 --",
        attempt=1, max_retries=3,
    )
    assert plan["action"] == "retry"
    assert plan["failure_type"] == "server_error"


def test_build_adaptive_plan_server_error_abort():
    """500 on second attempt (attempt >= 2) -> abort."""
    probe = {"type": "sqli", "target": "https://example.com/api?id=1"}
    result = {
        "status_code": 503,
        "headers": {"server": "Apache"},
        "body": "Service Unavailable",
    }
    plan = ae.build_adaptive_plan(
        probe, result, vuln_type="sqli", original_payload="' OR 1=1 --",
        attempt=2, max_retries=3,
    )
    assert plan["action"] == "abort"


# ---------------------------------------------------------------------------
# Retry schedule tests
# ---------------------------------------------------------------------------


def test_build_retry_schedule_default():
    """Default retry schedule: 3 attempts, exponential backoff from 500ms."""
    schedule = ae.build_retry_schedule(3)
    assert len(schedule) == 3
    assert schedule[0]["delay_ms"] == 500
    assert schedule[1]["delay_ms"] == 1000
    assert schedule[2]["delay_ms"] == 2000


def test_build_retry_schedule_capped():
    """Retry schedule should be capped at max_ms (default 8000)."""
    schedule = ae.build_retry_schedule(10, base_ms=1000, max_ms=8000)
    assert len(schedule) == 10
    for s in schedule:
        assert s["delay_ms"] <= 8000
    # The last entries should be capped at 8000
    assert schedule[-1]["delay_ms"] == 8000
