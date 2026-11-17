#!/usr/bin/env python3
"""Tests for utils.py — shared JSON I/O, DNS, fingerprint, and logging."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import utils


# ---------------------------------------------------------------------------
# JSON I/O tests
# ---------------------------------------------------------------------------


def test_load_json_valid(tmp_path):
    """Loading a valid JSON file should return the correct data."""
    data = {"key": "value", "list": [1, 2, 3], "nested": {"a": True}}
    filepath = tmp_path / "test_valid.json"
    filepath.write_text(json.dumps(data), encoding="utf-8")
    loaded = utils.load_json(str(filepath))
    assert loaded == data


def test_load_json_unicode(tmp_path):
    """JSON with non-ASCII (Chinese) characters should survive round-trip."""
    data = {"trigger": "检测", "description": "安全测试"}
    filepath = tmp_path / "test_unicode.json"
    filepath.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    loaded = utils.load_json(str(filepath))
    assert loaded == data


def test_load_json_empty_object(tmp_path):
    """Loading an empty JSON object should work."""
    filepath = tmp_path / "test_empty.json"
    filepath.write_text("{}", encoding="utf-8")
    loaded = utils.load_json(str(filepath))
    assert loaded == {}


def test_load_json_empty_array(tmp_path):
    """Loading an empty JSON array should work."""
    filepath = tmp_path / "test_empty_arr.json"
    filepath.write_text("[]", encoding="utf-8")
    loaded = utils.load_json(str(filepath))
    assert loaded == []


def test_load_json_nonexistent_file():
    """Loading a nonexistent file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        utils.load_json("/nonexistent/path/xyz/file.json")


def test_dump_json_basic():
    """dump_json should produce valid, parseable JSON string."""
    data = {"a": 1, "b": "hello", "c": [True, False, None]}
    result = utils.dump_json(data)
    assert isinstance(result, str)
    # Round-trip
    parsed = json.loads(result)
    assert parsed == data


def test_dump_json_roundtrip_complex():
    """dump_json then load_json from file should preserve complex data."""
    data = {
        "findings": [
            {"id": "f1", "type": "rce", "severity": "critical"},
            {"id": "f2", "type": "xss", "severity": "medium"},
        ],
        "metadata": {"tool": "gkn-phantom", "version": "3.0.0"},
        "tags": ["security", "pentest"],
        "count": 42,
        "active": True,
        "null_val": None,
    }
    dumped = utils.dump_json(data)
    parsed = json.loads(dumped)
    assert parsed == data


def test_dump_json_indent():
    """dump_json with custom indent should produce multi-line output."""
    data = {"x": 1, "y": 2}
    result = utils.dump_json(data, indent=4)
    assert "\n" in result
    assert result.count("\n") >= 3  # at least 3 lines with indent=4


# ---------------------------------------------------------------------------
# Finding fingerprint tests
# ---------------------------------------------------------------------------


def test_finding_fingerprint_stable():
    """Same finding content -> same fingerprint."""
    finding = {
        "type": "sqli",
        "target": "https://example.com/api?id=1",
        "evidence": {
            "request": "GET /api?id=1' OR '1'='1 HTTP/1.1",
            "response": "Error: SQL syntax",
        },
    }
    fp1 = utils.finding_fingerprint(finding)
    fp2 = utils.finding_fingerprint(finding)
    assert fp1 == fp2
    assert len(fp1) == 16  # SHA-256 truncated to 16 hex chars


def test_finding_fingerprint_different_type():
    """Findings with different types -> different fingerprints."""
    f1 = {
        "type": "sqli",
        "target": "https://example.com/api?id=1",
        "evidence": {"request": "GET /test HTTP/1.1"},
    }
    f2 = {
        "type": "xss",
        "target": "https://example.com/api?id=1",
        "evidence": {"request": "GET /test HTTP/1.1"},
    }
    assert utils.finding_fingerprint(f1) != utils.finding_fingerprint(f2)


def test_finding_fingerprint_different_target():
    """Findings with different targets -> different fingerprints."""
    f1 = {
        "type": "sqli",
        "target": "https://example.com/api?id=1",
        "evidence": {"request": "GET /test HTTP/1.1"},
    }
    f2 = {
        "type": "sqli",
        "target": "https://example.com/api?id=2",
        "evidence": {"request": "GET /test HTTP/1.1"},
    }
    assert utils.finding_fingerprint(f1) != utils.finding_fingerprint(f2)


def test_finding_fingerprint_different_request():
    """Findings with different evidence request -> different fingerprints."""
    f1 = {
        "type": "sqli",
        "target": "https://example.com/api",
        "evidence": {"request": "GET /api?id=1' HTTP/1.1"},
    }
    f2 = {
        "type": "sqli",
        "target": "https://example.com/api",
        "evidence": {"request": "POST /api HTTP/1.1"},
    }
    assert utils.finding_fingerprint(f1) != utils.finding_fingerprint(f2)


def test_finding_fingerprint_missing_fields():
    """Fingerprint should work even when fields are missing."""
    finding = {"type": "sqli"}
    fp = utils.finding_fingerprint(finding)
    assert isinstance(fp, str)
    assert len(fp) == 16


def test_finding_fingerprint_empty():
    """Empty finding -> still produces a valid hex fingerprint."""
    finding = {}
    fp = utils.finding_fingerprint(finding)
    assert isinstance(fp, str)
    assert len(fp) == 16
    # Should be all hex characters
    assert all(c in "0123456789abcdef" for c in fp)


# ---------------------------------------------------------------------------
# DNS resolve tests
# ---------------------------------------------------------------------------


def test_resolve_ips_localhost():
    """Resolving localhost should return at least 127.0.0.1."""
    ips = utils.resolve_ips("localhost", timeout=5.0)
    assert len(ips) > 0
    assert "127.0.0.1" in ips


def test_resolve_ips_nonexistent():
    """Resolving a nonexistent domain should return an empty list."""
    ips = utils.resolve_ips(
        "definitely-not-a-real-domain-xyz-12345.invalid",
        timeout=3.0,
    )
    # Should return empty list on resolution failure (may vary by DNS config)
    # Some DNS providers return NXDOMAIN quickly; others may hang.
    # We test that it doesn't raise an exception.
    assert isinstance(ips, list)


def test_resolve_ips_cache():
    """Repeated calls for the same host should use the cache."""
    utils.clear_dns_cache()
    ips1 = utils.resolve_ips("localhost", timeout=5.0)
    ips2 = utils.resolve_ips("localhost", timeout=0.01)  # very short timeout
    # Cache hit means the short timeout doesn't matter
    assert ips1 == ips2


def test_resolve_ips_timeout_does_not_raise():
    """Resolve with a very short timeout should not raise."""
    utils.clear_dns_cache()
    # This may return empty list but should not raise
    ips = utils.resolve_ips("10.255.255.1", timeout=0.5)
    assert isinstance(ips, list)


def test_clear_dns_cache():
    """clear_dns_cache should reset the internal cache."""
    utils.resolve_ips("localhost", timeout=5.0)
    utils.clear_dns_cache()
    # After clearing, the cache should be empty; resolving again should work
    ips = utils.resolve_ips("localhost", timeout=5.0)
    assert len(ips) > 0
    assert "127.0.0.1" in ips


# ---------------------------------------------------------------------------
# Logging tests
# ---------------------------------------------------------------------------


def test_utc_now_iso():
    """utc_now_iso should return a UTC ISO-8601 timestamp ending in Z."""
    ts = utils.utc_now_iso()
    assert isinstance(ts, str)
    assert ts.endswith("Z")
    # Should contain date and time separator
    assert "T" in ts


def test_log_event_structure():
    """log_event should return a dict with ts, state, msg, and any extras."""
    entry = utils.log_event("ACTIVE_TESTING", "Probe sent", tool="curl", target="example.com")
    assert entry["ts"].endswith("Z")
    assert entry["state"] == "ACTIVE_TESTING"
    assert entry["msg"] == "Probe sent"
    assert entry["tool"] == "curl"
    assert entry["target"] == "example.com"


# ---------------------------------------------------------------------------
# Dedup tests
# ---------------------------------------------------------------------------


def test_dedup_against_memory_all_new():
    """When prior is empty, all findings are new."""
    findings = [
        {"type": "sqli", "target": "https://a.com", "evidence": {"request": "GET /a"}},
        {"type": "xss", "target": "https://b.com", "evidence": {"request": "GET /b"}},
    ]
    new, known = utils.dedup_against_memory(findings, [])
    assert len(new) == 2
    assert len(known) == 0


def test_dedup_against_memory_all_known():
    """When findings match prior exactly, all are known."""
    f1 = {"type": "sqli", "target": "https://a.com", "evidence": {"request": "GET /a"}}
    f2 = {"type": "xss", "target": "https://b.com", "evidence": {"request": "GET /b"}}
    findings = [f1, f2]
    new, known = utils.dedup_against_memory(findings, [f1, f2])
    assert len(new) == 0
    assert len(known) == 2
    for k in known:
        assert k["state"] == "known"


def test_dedup_against_memory_mixed():
    """Some findings match prior, some are new."""
    f1 = {"type": "sqli", "target": "https://a.com", "evidence": {"request": "GET /a"}}
    f2 = {"type": "xss", "target": "https://b.com", "evidence": {"request": "GET /b"}}
    f3 = {"type": "rce", "target": "https://c.com", "evidence": {"request": "GET /c"}}
    new, known = utils.dedup_against_memory([f1, f2, f3], [f1])
    assert len(new) == 2
    assert len(known) == 1
    assert known[0]["state"] == "known"
