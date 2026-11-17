#!/usr/bin/env python3
"""Tests for cn_probes.py — domestic OA/component unauthorized-access library."""

from __future__ import annotations

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import cn_probes


# ---------------------------------------------------------------------------
# Data integrity
# ---------------------------------------------------------------------------


def test_cn_probes_wellformed():
    """Every CN probe must declare type, name, paths, and a valid check."""
    assert len(cn_probes.CN_PROBES) >= 25
    for probe in cn_probes.CN_PROBES:
        assert "type" in probe and "name" in probe, probe
        assert isinstance(probe.get("paths"), list) and probe["paths"], probe["name"]
        assert probe.get("check") in ("header", "pattern", "status", "redirect"), probe["name"]
        if probe["check"] == "pattern":
            assert probe.get("patterns"), probe["name"]
        if probe["check"] == "status":
            assert probe.get("status_codes"), probe["name"]


def test_cn_probes_cover_required_components():
    """The user-named components must all be covered."""
    blob = json.dumps(cn_probes.CN_PROBES, ensure_ascii=False)
    for marker in (
        "e-cology", "bsh.servlet.BshServlet",       # 泛微
        "Ssologin",                                 # 泛微 mobile SQLi
        "seeyon", "htmlofficeservlet",              # 致远
        "ispirit", "gateway.php",                   # 通达
        "nc.bs.framework", "uapws",                 # 用友
        "zentao", "getconfig",                      # 禅道
        "queryFieldBySql", "jmreport", "jeecg",     # JeecgBoot
        "druid", "prod-api",                        # 若依
    ):
        assert marker in blob, f"missing component coverage: {marker}"


def test_cn_probes_jeecg_verify_is_post():
    """The JeecgBoot queryFieldBySql verifier must be a POST probe."""
    probe = next(p for p in cn_probes.CN_PROBES
                 if "queryFieldBySql" in str(p.get("paths")))
    assert probe["method"] == "POST"
    assert "GKNVERIFY" in probe["post_body"]
    assert probe["patterns"] == ["GKNVERIFY"]
    assert probe.get("severity") == "critical"


def test_cn_probes_have_severity_overrides():
    """High-value probes must override the default baseline severity."""
    sev = {p["name"]: p.get("severity") for p in cn_probes.CN_PROBES}
    assert sev["Weaver e-cology BeanShell servlet (RCE point)"] == "critical"
    assert sev["Seeyon getSessionList.jsp unauth session disclosure"] == "high"
    assert sev["TongDa OA unauthorized module interfaces"] == "high"


# ---------------------------------------------------------------------------
# Live probing against a fake domestic-OA target
# ---------------------------------------------------------------------------


class _CNFakeHandler(BaseHTTPRequestHandler):
    """A fake target emulating several domestic components at once."""

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
        from urllib.parse import urlsplit
        path = urlsplit(self.path).path
        if path == "/bsh.servlet.BshServlet":
            self._send(200, "BeanShell servlet — bsh.servlet.BshServlet ready")
        elif path == "/weaver/bsh.servlet.BshServlet":
            self._send(200, "BeanShell servlet")
        elif path == "/seeyon/getSessionList.jsp":
            self._send(200, "var sessions = ['sid1', 'sid2']; seeyon session list")
        elif path == "/seeyon/htmlofficeservlet":
            self._send(500, "method not allowed")
        elif path == "/prod-api/druid/index.html":
            self._send(200, "<html><title>Druid Stat Index</title>druid-login</html>")
        elif path == "/ispirit/interface/gateway.php":
            self._send(200, '{"status": 1, "msg": "ok"}')
        elif path == "/mobile/plugin/Ssologin.jsp":
            self._send(200, "<form>Ssologin for ecology v9</form>")
        # soft-404 decoy: 200 but the body is an error page
        elif path == "/K3Cloud/":
            self._send(200, "404 Not Found — page does not exist")
        else:
            self._send(404, "Not Found")

    def do_POST(self):
        from urllib.parse import urlsplit
        path = urlsplit(self.path).path
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if path == "/jeecg-boot/jmreport/queryFieldBySql":
            self._send(200, json.dumps({
                "success": True, "result": {"records": [["GKNVERIFY"]]},
            }), ctype="application/json")
        else:
            self._send(404, "Not Found")


@pytest.fixture(scope="module")
def cn_fake_target():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _CNFakeHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def test_probe_cn_components_hits(cn_fake_target):
    findings = cn_probes.probe_cn_components([cn_fake_target])
    names = {f["probe_name"] for f in findings}
    # BeanShell RCE point (both paths hit → one dedup? no, two paths = two findings)
    assert any("BeanShell" in n for n in names)
    assert any("getSessionList" in n for n in names)
    assert any("Ssologin" in n for n in names)
    # every finding is a full pipeline-shaped dict
    for f in findings:
        assert f["status"] == "detected"
        assert f["target"] == cn_fake_target
        assert f["evidence"]["tool"] == "quick_probe"
        assert f["severity"] in ("critical", "high", "medium", "low")


def test_probe_cn_components_status_codes_and_soft_404(cn_fake_target):
    """Status-only probes must hit reachable interfaces (ispirit gateway)
    but NOT soft-404 pages (K3Cloud decoy returns 200 + '404 Not Found')."""
    findings = cn_probes.probe_cn_components([cn_fake_target])
    names = {f["probe_name"] for f in findings}
    assert any("TongDa OA unauthorized module interfaces" in n for n in names)
    assert not any("K3Cloud" in n for n in names)


def test_probe_cn_components_post_verify(cn_fake_target):
    """The JeecgBoot one-shot SQLi verifier must fire POST and match the
    echoed marker, returning a critical finding."""
    findings = cn_probes.probe_cn_components([cn_fake_target])
    verify = [f for f in findings if "queryFieldBySql" in f["probe_name"]]
    assert len(verify) == 1
    f = verify[0]
    assert f["type"] == "sqli"
    assert f["severity"] == "critical"
    assert f["tier"] == "high"
    assert "POST" in f["evidence"]["request"]
    assert "GKNVERIFY" in f["evidence"]["request"]


def test_probe_cn_components_no_false_positive_on_404(cn_fake_target):
    """A path not emulated by the fake target must produce no finding."""
    findings = cn_probes.probe_cn_components([cn_fake_target])
    names = {f["probe_name"] for f in findings}
    assert not any("uapws" in n for n in names)
    assert not any("Landray" in n for n in names)


def test_probe_cn_components_unreachable_target():
    """An unreachable target yields zero findings, never raises."""
    assert cn_probes.probe_cn_components(["http://127.0.0.1:1"]) == []
