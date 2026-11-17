#!/usr/bin/env python3
"""Tests for quick_combat.py — Quick Combat pipeline + v5.2 severity escalation."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import quick_combat as qc


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_finding(
    probe_path: str,
    body: str,
    ftype: str = "info_leak",
    severity: str = "medium",
    headers: dict | None = None,
) -> dict:
    """Build a quick-probe-shaped finding for escalation tests."""
    return {
        "type": ftype,
        "severity": severity,
        "tier": "low",
        "target": "https://example.com",
        "probe_path": probe_path,
        "probe_name": "unit-test",
        "status": "detected",
        "confidence": 0.7,
        "evidence": {
            "request": f"GET {probe_path} HTTP/1.1",
            "response": body,
            "timestamp": "2026-09-17T00:00:00Z",
            "tool": "quick_probe",
            "status_code": 200,
            "headers": headers or {"content-type": "text/plain"},
        },
        "reproducible": True,
    }


# ---------------------------------------------------------------------------
# escalate_severity — upgrade rules
# ---------------------------------------------------------------------------


def test_escalate_env_secret_to_high():
    """A .env response containing a live DB_PASSWORD must escalate to high."""
    body = "APP_NAME=shop\nDB_PASSWORD=S3cr3t!pass\nDB_HOST=10.0.0.2\n"
    f = make_finding("/.env", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "high"
    assert out["severity_escalated_from"] == "medium"
    assert "credential" in out["escalation_reason"].lower()


def test_escalate_aws_key_to_high():
    """A response containing an AWS access key ID must escalate to high."""
    body = "leaked log line: aws credential detected REDACTED-SECRET for deploy"
    f = make_finding("/debug.log", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "high"
    assert "aws" in out["escalation_reason"].lower()


def test_escalate_quoted_aws_key_to_critical():
    """A quoted JSON secret (access_key: AKIA...) hits the data_exposure
    rule first and escalates straight to critical — same gate as the full
    state machine."""
    body = '{"access_key": "REDACTED-SECRET"}'
    f = make_finding("/config.json", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "critical"
    assert "data_exposure" in out["escalation_reason"]


def test_escalate_private_key_to_high():
    """A response containing a private key block must escalate to high."""
    body = "REDACTED-SECRET\n"
    f = make_finding("/key.pem", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "high"
    assert "private key" in out["escalation_reason"].lower()


def test_escalate_git_config_to_high():
    """A .git/config response must escalate to high (source recovery)."""
    body = "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n"
    f = make_finding("/.git/config", body, ftype="info_leak")
    out = qc.escalate_severity(f)
    assert out["severity"] == "high"
    assert "git" in out["escalation_reason"].lower()


def test_escalate_phpinfo_to_high():
    """A phpinfo page must escalate to high."""
    body = "<title>phpinfo()</title><h1>Configuration</h1>phpinfo()"
    f = make_finding("/phpinfo.php", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "high"


def test_escalate_backup_archive_to_high():
    """A reachable backup archive must escalate to high and record size."""
    f = make_finding(
        "/backup.zip",
        body="PK\x03\x04binary",
        headers={"content-length": "1048576", "content-type": "application/zip"},
    )
    out = qc.escalate_severity(f)
    assert out["severity"] == "high"
    assert "1048576" in out["escalation_reason"]


def test_escalate_pii_to_critical():
    """Response matching data_exposure threshold must escalate to critical."""
    emails = "\n".join(f"user{i}@example.com" for i in range(15))
    body = f"subscriber dump:\n{emails}\n"
    f = make_finding("/logs/users.txt", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "critical"
    assert out["severity_escalated_from"] == "medium"
    assert "data_exposure" in out["escalation_reason"]


def test_escalate_quoted_secret_to_critical():
    """Quoted secret assignment (classify_data_exposure rule) → critical."""
    body = '{"password": "hunter2-super-secret", "user": "admin"}'
    f = make_finding("/config.json", body)
    out = qc.escalate_severity(f)
    # classify_data_exposure scores quoted secrets 3 → critical
    assert out["severity"] in ("critical", "high")
    assert "severity_escalated_from" in out


# ---------------------------------------------------------------------------
# escalate_severity — no false positives / no de-escalation
# ---------------------------------------------------------------------------


def test_no_escalation_on_benign_body():
    """A benign page must NOT be escalated."""
    body = "<html><body>Welcome to the shop. See our <a href='/about'>about</a> page.</body></html>"
    f = make_finding("/index.html", body, ftype="misconfig", severity="low")
    out = qc.escalate_severity(f)
    assert out["severity"] == "low"
    assert "severity_escalated_from" not in out
    assert "escalation_reason" not in out


def test_no_escalation_on_secret_keyword_without_value():
    """Mentions of the word 'password' with no assignment must NOT escalate."""
    body = "<p>Please change your password regularly. Password safety matters.</p>"
    f = make_finding("/docs/security.html", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "medium"
    assert "severity_escalated_from" not in out


def test_no_escalation_on_empty_password_value():
    """An empty secret value (DB_PASSWORD=) must NOT escalate."""
    body = "DB_PASSWORD=\nDB_HOST=localhost\n"
    f = make_finding("/.env", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "medium"


def test_no_escalation_on_git_word_only():
    """Body mentioning 'git' without a [core] config block must NOT escalate."""
    body = "We use git for version control. Read the git docs for details."
    f = make_finding("/readme.html", body)
    out = qc.escalate_severity(f)
    assert out["severity"] == "medium"


def test_no_deescalation_on_high_input():
    """A finding already at high must not be touched by escalation."""
    body = "DB_PASSWORD=real-secret"
    f = make_finding("/.env", body, severity="high")
    out = qc.escalate_severity(f)
    assert out["severity"] == "high"
    assert "severity_escalated_from" not in out


def test_nuclei_finding_untouched():
    """Findings without probe_path (e.g. nuclei output) must pass through."""
    f = {
        "type": "cve-2021-44228",
        "severity": "critical",
        "evidence": {"response": "DB_PASSWORD=whatever"},
    }
    out = qc.escalate_severity(f)
    assert out is f
    assert "severity_escalated_from" not in out


def test_benign_archive_404_not_escalated():
    """Archive path findings with status != detected must not escalate."""
    f = make_finding("/backup.zip", body="", severity="medium")
    f["status"] = "not_found"
    out = qc.escalate_severity(f)
    assert out["severity"] == "medium"


# ---------------------------------------------------------------------------
# QUICK_PROBES integrity
# ---------------------------------------------------------------------------


def test_quick_probes_wellformed():
    """Every built-in probe must declare type, name, paths, and check."""
    assert len(qc.QUICK_PROBES) >= 7
    for probe in qc.QUICK_PROBES:
        assert "type" in probe and "name" in probe
        assert isinstance(probe.get("paths"), list) and probe["paths"]
        assert probe.get("check") in ("header", "pattern", "status", "redirect")


# ---------------------------------------------------------------------------
# v5.3 C1/C2 — local dry-run server (no real network targets)
# ---------------------------------------------------------------------------

import json as _json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class _FakeTargetHandler(BaseHTTPRequestHandler):
    """A controllable fake target exercising every C1/C2 code path."""

    def log_message(self, *args):
        pass

    def _send(self, code: int, body: str, ctype: str = "text/html"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        from urllib.parse import urlsplit, parse_qs

        path = urlsplit(self.path).path
        query = {k: v[0] for k, v in parse_qs(urlsplit(self.path).query).items()}

        if path == "/":
            # v5.4: emulate open-redirect behaviour on the classic params
            for k in ("redirect", "url", "next", "returnUrl"):
                if k in query:
                    self.send_response(302)
                    self.send_header("Location", query[k])
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
            self._send(200, (
                '<a href="/item?id=1">item</a>'
                '<a href="https://evil.example.com/x?a=1">cross</a>'
                '<a href="/list?page=2">list</a>'
                '<a href="/proxy?url=https://internal.example.test/x">proxy</a>'
                '<script src="/app.js"></script>'
                "<script>var u='/item?id=7';</script>"
            ))
        elif path == "/app.js":
            # v5.4: JS bundle with a leaked AWS key + a hidden endpoint
            self._send(200, (
                'var config = {access_key: "REDACTED-SECRET"};\n'
                'fetch("/hidden?id=1");\n'
                'document.write("<b>debug</b>");\n'
            ), ctype="application/javascript")
        elif path == "/hidden":
            # v5.4: hidden endpoint discovered from JS — SQLi behind it
            val = query.get("id", "")
            if "'" in val or '"' in val:
                self._send(200, (
                    "<b>Database error:</b> You have an error in your SQL syntax; "
                    "check the manual that corresponds to your MySQL server version"
                ))
            else:
                self._send(200, "<html>Hidden item</html>")
        elif path == "/proxy":
            # v5.4: SSRF-style parameter sink
            self._send(200, "proxied ok")
        elif path == "/search":
            # v5.4: only reachable via katana crawl — proves C3 chaining
            val = query.get("q", "")
            if "'" in val or '"' in val:
                self._send(200, (
                    "<b>Database error:</b> You have an error in your SQL syntax; "
                    "check the manual that corresponds to your MySQL server version"
                ))
            else:
                self._send(200, "search results")
        elif path == "/item":
            val = query.get("id", "")
            if "'" in val or '"' in val:
                self._send(200, (
                    "<b>Database error:</b> You have an error in your SQL syntax; "
                    "check the manual that corresponds to your MySQL server version"
                ))
            else:
                self._send(200, "<html>Item page</html>")
        elif path == "/list":
            val = query.get("page", "")
            if "{{7*7}}" in val:
                self._send(200, "Result: 49")
            else:
                self._send(200, "Result: page 2 (10 items)")
        elif path == "/actuator/env":
            self._send(200, _json.dumps({
                "activeProfiles": "prod",
                "propertySources": [{"name": "config", "properties": {
                    "spring.datasource.password": {"value": "root123"}}}],
            }), ctype="application/json")
        elif path == "/actuator/configprops":
            self._send(404, "not found")
        elif path == "/actuator/heapdump":
            self._send(200, "\x00\x01\x02heapdump-binary-prefix", ctype="application/octet-stream")
        elif path == "/graphql":
            self._send(200, _json.dumps({"data": {"__schema": {
                "queryType": {"name": "Query"},
                "mutationType": {"name": "Mutation"},
                "types": [{"name": "User", "kind": "OBJECT"}],
            }}}), ctype="application/json")
        elif path == "/v3/api-docs":
            self._send(200, _json.dumps({
                "paths": {"/api/users": {}, "/api/orders": {}},
            }), ctype="application/json")
        else:
            self._send(404, "not found")

    def do_POST(self):
        from urllib.parse import urlsplit

        if urlsplit(self.path).path == "/graphql" or self.path.startswith("/graphql"):
            self.rfile.read(int(self.headers.get("Content-Length", 0)))
            self._send(200, _json.dumps({"data": {"__schema": {
                "queryType": {"name": "Query"},
                "mutationType": {"name": "Mutation"},
                "types": [{"name": "User", "kind": "OBJECT"}],
            }}}), ctype="application/json")
        elif urlsplit(self.path).path.endswith("/jmreport/queryFieldBySql"):
            # v5.4: JeecgBoot one-shot SQLi verifier echo
            self.rfile.read(int(self.headers.get("Content-Length", 0)))
            self._send(200, _json.dumps({
                "success": True, "result": {"records": [["GKNVERIFY"]]},
            }), ctype="application/json")
        else:
            self._send(404, "not found")


def urlsplit_path(p):
    from urllib.parse import urlsplit
    return urlsplit(p).path


@pytest.fixture(scope="module")
def fake_target():
    """Start a local HTTP server on 127.0.0.1 and yield its base URL."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FakeTargetHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


# ---------------------------------------------------------------------------
# C1 — deep-dive adapters
# ---------------------------------------------------------------------------


def test_dd_route_dispatch():
    assert qc._dd_route({"type": "component_exposure",
                         "probe_path": "/actuator/env"}) == "actuator"
    assert qc._dd_route({"type": "component_exposure",
                         "probe_path": "/swagger-ui.html"}) == "swagger"
    assert qc._dd_route({"type": "graphql_introspection",
                         "probe_path": "/graphql"}) == "graphql"
    assert qc._dd_route({"type": "info_leak", "probe_path": "/.env"}) is None


def test_deep_dive_noop_for_unroutable():
    f = make_finding("/.env", "DB_PASSWORD=x")
    out = qc.deep_dive(f)
    assert "deep_dive" not in out


def test_deep_dive_noop_for_not_detected():
    f = make_finding("/actuator/env", "{}", ftype="component_exposure")
    f["status"] = "not_found"
    out = qc.deep_dive(f)
    assert "deep_dive" not in out


def test_deep_dive_actuator_unmasked_secret_critical(fake_target):
    f = make_finding("/actuator/env", "some body", ftype="component_exposure",
                     severity="medium")
    f["target"] = fake_target
    out = qc.deep_dive(f)
    dd = out["deep_dive"]
    assert dd["performed"] is True
    assert dd["adapter"] == "actuator"
    assert out["severity"] == "critical"
    assert out["severity_escalated_from"] == "medium"
    assert "unmasked credentials" in out["escalation_reason"]
    # bounded request budget
    assert len(dd["requests"]) <= qc._DD_MAX_REQUESTS


def test_deep_dive_actuator_heapdump_critical(fake_target):
    """heapdump reachable (env without secrets) must escalate to critical."""
    class Handler(_FakeTargetHandler):
        def do_GET(self):
            from urllib.parse import urlsplit
            if urlsplit(self.path).path == "/actuator/env":
                self._send(200, _json.dumps(
                    {"propertySources": [{"name": "c", "properties": {
                        "spring.datasource.password": {"value": "******"}}}]}),
                    ctype="application/json")
            else:
                _FakeTargetHandler.do_GET(self)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        f = make_finding("/actuator/env", "x", ftype="component_exposure",
                         severity="medium")
        f["target"] = base
        out = qc.deep_dive(f)
        assert out["severity"] == "critical"
        assert "heapdump" in out["escalation_reason"]
    finally:
        server.shutdown()


def test_deep_dive_graphql_mutation_high(fake_target):
    f = make_finding("/graphql", '{"__schema"}', ftype="graphql_introspection",
                     severity="low")
    f["target"] = fake_target
    out = qc.deep_dive(f)
    assert out["deep_dive"]["adapter"] == "graphql"
    assert out["severity"] == "high"
    assert "mutation" in out["escalation_reason"].lower()
    assert "type fields" in out["deep_dive"]["impact"]


def test_deep_dive_swagger_noauth_high(fake_target):
    f = make_finding("/swagger-ui/index.html", "swagger", ftype="component_exposure",
                     severity="medium")
    f["target"] = fake_target
    out = qc.deep_dive(f)
    dd = out["deep_dive"]
    assert dd["adapter"] == "swagger"
    assert out["severity"] == "high"
    assert "no authentication scheme" in out["escalation_reason"]
    assert "2 endpoints" in dd["impact"]


def test_deep_dive_off_target_returns_error_field(monkeypatch):
    """Unreachable target → adapter records error, never raises."""
    monkeypatch.setattr(qc, "_DD_TIMEOUT", 0.5)
    f = make_finding("/actuator/env", "x", ftype="component_exposure")
    f["target"] = "http://127.0.0.1:1"
    out = qc.deep_dive(f)
    assert out["deep_dive"]["performed"] is True  # requests attempted, impact None


# ---------------------------------------------------------------------------
# C2 — parameter discovery + injection probing
# ---------------------------------------------------------------------------


def test_discover_params_same_origin_only(fake_target):
    entries = qc.discover_params(fake_target)
    urls = [e["url"] for e in entries]
    params = {(e["url"], e["param"]) for e in entries}
    # same-origin param URLs discovered
    assert any(p == "id" for _, p in params)
    assert any(p == "page" for _, p in params)
    # cross-origin excluded
    assert all("evil.example.com" not in u for u in urls)


def test_discover_params_unreachable_returns_empty():
    assert qc.discover_params("http://127.0.0.1:1/", timeout=0.5) == []


def test_probe_injection_sqli_error_based(fake_target):
    entries = [{"url": f"{fake_target}/item?id=1", "param": "id", "value": "1"}]
    findings = qc.probe_injection(fake_target, entries)
    assert len(findings) == 1
    f = findings[0]
    assert f["type"] == "sqli"
    assert f["severity"] == "high"
    assert "mysql" in f["detection_signal"].lower()
    assert f["evidence"]["injected_param"] == "id"
    assert f["evidence"]["payload"]


def test_probe_injection_ssti_reflection(fake_target):
    entries = [{"url": f"{fake_target}/list?page=2", "param": "page", "value": "2"}]
    findings = qc.probe_injection(fake_target, entries)
    assert len(findings) == 1
    f = findings[0]
    assert f["type"] == "ssti"
    assert f["severity"] == "high"
    assert "49" in f["detection_signal"]


def test_probe_injection_clean_param_no_finding(monkeypatch):
    """A param that reflects neither DB errors nor 49 must yield nothing."""
    monkeypatch.setattr(qc, "_DD_TIMEOUT", 0.5)
    entries = [{"url": "http://127.0.0.1:1/item?id=1", "param": "id", "value": "1"}]
    assert qc.probe_injection("http://127.0.0.1:1", entries, timeout=0.5) == []


def test_fingerprint_signatures_cover_engines():
    sigs = qc._fingerprint_signatures()
    engines = {e for e, _ in sigs}
    assert {"mysql", "postgresql", "mssql", "oracle", "sqlite"} <= engines
    assert len(sigs) >= 30


# ---------------------------------------------------------------------------
# escalation helper semantics (shared by A and C layers)
# ---------------------------------------------------------------------------


def test_apply_escalation_keeps_first_from():
    f = {"severity": "medium"}
    assert qc._apply_escalation(f, "high", "first") is True
    assert f["severity_escalated_from"] == "medium"
    # second upgrade keeps the ORIGINAL from-value
    assert qc._apply_escalation(f, "critical", "second") is True
    assert f["severity_escalated_from"] == "medium"
    assert f["severity"] == "critical"
    assert f["escalation_reason"] == "second"


def test_apply_escalation_never_deescalates():
    f = {"severity": "critical"}
    assert qc._apply_escalation(f, "high", "down") is False
    assert f["severity"] == "critical"


# ---------------------------------------------------------------------------
# End-to-end pipeline smoke test (Phase 2.5 + 2.6 wiring)
# ---------------------------------------------------------------------------


def test_run_combat_pipeline_deep_smoke(fake_target, tmp_path):
    """Full pipeline against the local fake target with deep layers ON.

    Verifies the Phase 2.5 (deep dive) and Phase 2.6 (param probes)
    wiring: actuator exposure escalates to critical via deep dive,
    GraphQL introspection escalates to high, and param discovery finds
    the SQLi/SSTi endpoints.
    """
    result = qc.run_combat_pipeline(
        targets=[fake_target],
        output_dir=str(tmp_path / "combat"),
        use_nuclei=False,
        quick_probes=True,
        deep=True,
    )
    # actuator env secret → critical
    assert result["by_severity"]["critical"] >= 1
    # graphql schema + sqli/ssti → high
    assert result["by_severity"]["high"] >= 2
    # summary mentions both deep layers
    assert any("Deep dive" in s for s in result["summary"])
    assert any("Param probes" in s for s in result["summary"])
    # artifacts written
    assert os.path.isfile(result["artifacts"]["findings"])
    # every finding carries full evidence
    import json as _j
    findings = _j.load(open(result["artifacts"]["findings"], encoding="utf-8"))
    for f in findings:
        assert f.get("evidence", {}).get("response") is not None
        assert f.get("evidence", {}).get("timestamp")


# ---------------------------------------------------------------------------
# v5.4 — C5: real OOB channel integration
# ---------------------------------------------------------------------------


class _FakeOOBClient:
    """Deterministic in-memory OOB client for pipeline tests."""

    provider = "fake"

    def __init__(self, confirm_all: bool = True):
        self.confirm_all = confirm_all
        self.tags: list[str] = []
        self.closed = False

    def get_domain(self, tag: str = "gkn") -> str:
        self.tags.append(tag)
        return f"{tag}.oob.fake"

    def poll(self, tag: str | None = None, wait: float = 0.0) -> list[dict]:
        if not self.confirm_all:
            return []
        return [{"full-id": f"{t}.oob.fake", "protocol": "dns",
                 "remote-address": "203.0.113.9"} for t in self.tags]

    def close(self) -> None:
        self.closed = True


def test_run_quick_probes_oob_domain_replacement(fake_target):
    """With a real OOB client, redirect probe paths must carry the live
    callback domain instead of the static placeholder."""
    client = _FakeOOBClient(confirm_all=False)
    findings = qc.run_quick_probes([fake_target], oob_client=client)
    redirects = [f for f in findings if f["type"] == "open_redirect"]
    assert redirects, "open redirect finding expected on fake target"
    for f in redirects:
        assert "oob.authorized.test" not in f["probe_path"]
        assert "gkn-redir.oob.fake" in f["probe_path"]


def test_run_quick_probes_placeholder_without_oob(fake_target):
    """Without an OOB client the placeholder domain is used (back-compat)."""
    findings = qc.run_quick_probes([fake_target])
    redirects = [f for f in findings if f["type"] == "open_redirect"]
    assert redirects
    assert all("oob.authorized.test" in f["probe_path"] for f in redirects)


def test_probe_blind_ssrf_fires_tagged_callbacks(fake_target):
    client = _FakeOOBClient(confirm_all=False)
    entries = [{"url": f"{fake_target}/proxy", "param": "url",
                "value": "https://internal.example.test/x"}]
    pending = qc.probe_blind_ssrf(fake_target, entries, client)
    assert len(pending) == 1
    p = pending[0]
    assert p["param"] == "url"
    assert p["tag"] == "gkn-ssrf-url"
    assert p["callback"] == "https://gkn-ssrf-url.oob.fake/probe"


def test_probe_blind_ssrf_ignores_non_ssrf_params(fake_target):
    client = _FakeOOBClient(confirm_all=False)
    entries = [{"url": f"{fake_target}/item", "param": "id", "value": "1"}]
    assert qc.probe_blind_ssrf(fake_target, entries, client) == []


def test_verify_oob_pending_validates(fake_target):
    """A confirmed OOB callback becomes a validated (not 'detected')
    blind-SSRF finding — the whole point of the C5 layer."""
    findings: list[dict] = []
    pending = [{
        "tag": "gkn-ssrf-url", "param": "url",
        "url": f"{fake_target}/proxy?url=https://gkn-ssrf-url.oob.fake/probe",
        "target": fake_target,
        "callback": "https://gkn-ssrf-url.oob.fake/probe",
    }]
    client = _FakeOOBClient(confirm_all=True)
    client.get_domain("gkn-ssrf-url")  # the probe would have registered the tag
    confirmed, _ = qc.verify_oob_pending(findings, pending, client, wait=0.2)
    assert confirmed == 1
    f = findings[0]
    assert f["type"] == "ssrf"
    assert f["status"] == "validated"
    assert f["severity"] == "high"
    assert f["evidence"]["tool"] == "oob_client"
    assert f["verification_method"] == "oob_callback"


def test_verify_oob_pending_no_callback_no_finding():
    findings: list[dict] = []
    pending = [{"tag": "x", "param": "url", "url": "http://t/?url=x",
                "target": "http://t", "callback": "x.oob.fake"}]
    client = _FakeOOBClient(confirm_all=False)
    confirmed, _ = qc.verify_oob_pending(findings, pending, client, wait=0.2)
    assert confirmed == 0
    assert findings == []


def test_pipeline_blind_ssrf_end_to_end(fake_target, tmp_path):
    """Pipeline wiring: discovered 'url' param → OOB probe → validated SSRF."""
    client = _FakeOOBClient(confirm_all=True)
    result = qc.run_combat_pipeline(
        targets=[fake_target],
        output_dir=str(tmp_path / "combat"),
        use_nuclei=False, quick_probes=False, deep=True,
        oob_client=client, use_cn_probes=False, use_memory=False,
    )
    assert any("OOB verification" in s for s in result["summary"])
    import json as _j
    findings = _j.load(open(result["artifacts"]["findings"], encoding="utf-8"))
    ssrf = [f for f in findings if f["type"] == "ssrf"]
    assert ssrf
    assert all(f["status"] == "validated" for f in ssrf)
    assert client.closed is True  # pipeline released the channel


# ---------------------------------------------------------------------------
# v5.4 — C3: katana full-site crawl
# ---------------------------------------------------------------------------


def test_detect_katana_absent_or_present():
    """detect_katana must return a well-formed triple either way."""
    ok, path, version = qc.detect_katana()
    if ok:
        assert path and version
    else:
        assert path is None and version is None


def test_crawl_katana_parses_jsonl(monkeypatch, fake_target):
    from types import SimpleNamespace

    stdout = "\n".join([
        _json.dumps({"request": {"endpoint": f"{fake_target}/search?q=1"}}),
        _json.dumps({"request": {"endpoint": f"{fake_target}/app.js"}}),
        "garbage-not-json",
        _json.dumps({"url": f"{fake_target}/plain"}),
    ])
    monkeypatch.setattr(qc.subprocess, "run",
                        lambda *a, **k: SimpleNamespace(stdout=stdout, stderr=""))
    result = qc.crawl_katana(fake_target, "/fake/katana")
    assert f"{fake_target}/search?q=1" in result["urls"]
    assert f"{fake_target}/plain" in result["urls"]
    assert f"{fake_target}/app.js" in result["js_urls"]
    assert result["count"] == 3


def test_crawl_katana_failure_returns_empty(monkeypatch, fake_target):
    def boom(*a, **k):
        raise RuntimeError("katana exploded")
    monkeypatch.setattr(qc.subprocess, "run", boom)
    result = qc.crawl_katana(fake_target, "/fake/katana", timeout=1)
    assert result["urls"] == [] and result["js_urls"] == []
    assert "error" in result


def test_pipeline_katana_crawl_feeds_injection(fake_target, tmp_path, monkeypatch):
    """Crawled-only URLs (not on the entry page) must reach probe_injection."""
    monkeypatch.setattr(qc, "detect_katana", lambda: (True, "/fake/katana", "1.0"))

    def fake_crawl(t, kpath, depth=3, timeout=120):
        return {"urls": [f"{t}/search?q=1"], "js_urls": [], "count": 1}

    monkeypatch.setattr(qc, "crawl_katana", fake_crawl)
    result = qc.run_combat_pipeline(
        targets=[fake_target],
        output_dir=str(tmp_path / "combat"),
        use_nuclei=False, quick_probes=False, deep=True,
        use_cn_probes=False, use_memory=False, use_js=False,
    )
    assert any("katana" in s for s in result["summary"])
    import json as _j
    findings = _j.load(open(result["artifacts"]["findings"], encoding="utf-8"))
    # /search?q=1 only exists via the crawl → its SQLi proves C3 chaining
    assert any(f["type"] == "sqli" and "/search" in str(f.get("probe_path", ""))
               for f in findings)


# ---------------------------------------------------------------------------
# v5.4 — C4: JS bundle mining
# ---------------------------------------------------------------------------


def test_collect_js_urls_from_entry_page(fake_target):
    urls = qc.collect_js_urls(fake_target)
    assert f"{fake_target}/app.js" in urls


def test_analyze_target_js_findings_and_hidden_endpoints(fake_target):
    findings, entries = qc.analyze_target_js([f"{fake_target}/app.js"], fake_target)
    # leaked AWS key
    secret = [f for f in findings if f["type"] == "js_secret_leak"]
    assert secret
    assert secret[0]["severity"] == "critical"
    # hidden endpoint extracted for injection probing
    assert any(e["url"] == f"{fake_target}/hidden?id=1" and e["param"] == "id"
               for e in entries)


def test_analyze_target_js_unreachable():
    findings, entries = qc.analyze_target_js(["http://127.0.0.1:1/app.js"], "http://127.0.0.1:1")
    assert findings == [] and entries == []


def test_pipeline_js_mining_chains_to_injection(fake_target, tmp_path):
    """JS bundle → hidden endpoint → SQLi finding, plus JS findings saved."""
    result = qc.run_combat_pipeline(
        targets=[fake_target],
        output_dir=str(tmp_path / "combat"),
        use_nuclei=False, quick_probes=False, deep=True,
        use_cn_probes=False, use_memory=False, use_crawl=False,
    )
    assert any("JS analysis" in s for s in result["summary"])
    import json as _j
    findings = _j.load(open(result["artifacts"]["findings"], encoding="utf-8"))
    types = {f["type"] for f in findings}
    assert "js_secret_leak" in types
    # the /hidden endpoint mined from app.js got injection-probed
    assert any(f["type"] == "sqli" and "/hidden" in str(f.get("probe_path", ""))
               for f in findings)


# ---------------------------------------------------------------------------
# v5.4 — CN component probes in the pipeline
# ---------------------------------------------------------------------------


def test_pipeline_cn_probes_layer(fake_target, tmp_path):
    result = qc.run_combat_pipeline(
        targets=[fake_target],
        output_dir=str(tmp_path / "combat"),
        use_nuclei=False, quick_probes=False, deep=True,
        use_cn_probes=True, use_memory=False, use_js=False, use_crawl=False,
    )
    assert any("CN component probes" in s for s in result["summary"])
    import json as _j
    findings = _j.load(open(result["artifacts"]["findings"], encoding="utf-8"))
    names = {str(f.get("probe_name", "")) for f in findings}
    # JeecgBoot one-shot verifier fired against the fake target
    assert any("queryFieldBySql" in n for n in names)
    jeecg = next(f for f in findings if "queryFieldBySql" in str(f.get("probe_name", "")))
    assert jeecg["severity"] == "critical"


# ---------------------------------------------------------------------------
# v5.4 — C6: cross-run combat memory
# ---------------------------------------------------------------------------


def test_pipeline_memory_marks_second_run_as_duplicate(fake_target, tmp_path):
    out = str(tmp_path / "combat")
    common = dict(use_nuclei=False, quick_probes=False, deep=True,
                  use_cn_probes=False, use_js=False, use_crawl=False)
    qc.run_combat_pipeline(targets=[fake_target], output_dir=out, **common)
    second = qc.run_combat_pipeline(targets=[fake_target], output_dir=out, **common)
    import json as _j
    findings = _j.load(open(second["artifacts"]["findings"], encoding="utf-8"))
    marked = [f for f in findings if f.get("duplicate_state")]
    assert marked, "second run must mark known findings"
    assert all("重复" in str(f["probe_name"]) or "已提交" in str(f["probe_name"])
               for f in marked)
    assert second["duplicate_known"] == len(marked)
    assert any("Memory dedup" in s for s in second["summary"])
    # memory file persisted at the output-dir root, referenced by manifest
    assert os.path.isfile(second["artifacts"]["combat_memory"])


def test_pipeline_memory_preserves_submitted_flag(fake_target, tmp_path):
    out = str(tmp_path / "combat")
    common = dict(use_nuclei=False, quick_probes=False, deep=True,
                  use_cn_probes=False, use_js=False, use_crawl=False)
    first = qc.run_combat_pipeline(targets=[fake_target], output_dir=out, **common)
    # user marks a finding as submitted to the SRC platform
    mem_path = first["artifacts"]["combat_memory"]
    with open(mem_path, "r", encoding="utf-8") as fh:
        memory = _json.load(fh)
    for rec in memory["findings"]:
        rec["submitted"] = True
    with open(mem_path, "w", encoding="utf-8") as fh:
        fh.write(_json.dumps(memory, ensure_ascii=False))
    second = qc.run_combat_pipeline(targets=[fake_target], output_dir=out, **common)
    import json as _j
    findings = _j.load(open(second["artifacts"]["findings"], encoding="utf-8"))
    marked = [f for f in findings if f.get("duplicate_state")]
    assert marked
    assert all(f["duplicate_state"] == "submitted" for f in marked)
    assert all("已提交" in str(f["probe_name"]) for f in marked)


def test_pipeline_no_memory_flag(fake_target, tmp_path):
    out = str(tmp_path / "combat")
    qc.run_combat_pipeline(
        targets=[fake_target], output_dir=out,
        use_nuclei=False, quick_probes=False, deep=True,
        use_cn_probes=False, use_js=False, use_crawl=False, use_memory=False,
    )
    assert not os.path.isfile(os.path.join(out, "combat_memory.json"))


# ---------------------------------------------------------------------------
# v5.4 — probe engine extensions (POST / severity / not_patterns)
# ---------------------------------------------------------------------------


def test_run_probe_post_method(fake_target):
    probe = {
        "type": "sqli", "name": "unit post probe",
        "paths": ["/jeecg-boot/jmreport/queryFieldBySql"],
        "method": "POST",
        "post_body": '{"sql": "select \'UNITPOST\'"}',
        "post_content_type": "application/json",
        "check": "pattern", "patterns": ["GKNVERIFY"],  # echoed by fake target
        "severity": "critical",
    }
    findings = qc._run_quick_probe(fake_target, probe)
    assert len(findings) == 1
    f = findings[0]
    assert f["severity"] == "critical"
    assert f["tier"] == "high"
    assert "POST" in f["evidence"]["request"]
    assert "UNITPOST" in f["evidence"]["request"]


def test_run_probe_severity_override(fake_target):
    probe = {
        "type": "component_exposure", "name": "unit severity",
        "paths": ["/actuator/env"],
        "check": "pattern", "patterns": ["activeProfiles"],
        "severity": "high",
    }
    findings = qc._run_quick_probe(fake_target, probe)
    assert findings and findings[0]["severity"] == "high"
    assert findings[0]["tier"] == "high"
