#!/usr/bin/env python3
"""Tests for oob_client.py — real out-of-band channel client."""

from __future__ import annotations

import io
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import oob_client as oob_mod
from oob_client import (
    CeyeClient,
    DnslogClient,
    InteractshClient,
    OOBClient,
    get_oob_client,
)


# ---------------------------------------------------------------------------
# Factory — provider resolution and graceful degradation
# ---------------------------------------------------------------------------


def test_factory_none_provider():
    assert get_oob_client(provider="none") is None
    assert get_oob_client(provider="off") is None


def test_factory_auto_without_config(monkeypatch):
    """No interactsh binary, no ceye env → auto returns None."""
    monkeypatch.setattr(oob_mod.shutil, "which", lambda name: None)
    monkeypatch.delenv("GKN_CEYE_IDENTIFIER", raising=False)
    monkeypatch.delenv("GKN_CEYE_TOKEN", raising=False)
    monkeypatch.delenv("GKN_OOB_PROVIDER", raising=False)
    assert get_oob_client(provider="auto") is None


def test_factory_ceye_missing_credentials(monkeypatch):
    monkeypatch.delenv("GKN_CEYE_IDENTIFIER", raising=False)
    monkeypatch.delenv("GKN_CEYE_TOKEN", raising=False)
    assert get_oob_client(provider="ceye") is None


def test_factory_ceye_with_credentials(monkeypatch):
    monkeypatch.delenv("GKN_CEYE_IDENTIFIER", raising=False)
    monkeypatch.delenv("GKN_CEYE_TOKEN", raising=False)
    c = get_oob_client(provider="ceye", ceye_identifier="myid",
                       ceye_token="mytok")
    assert isinstance(c, CeyeClient)
    assert c.get_domain("gkn-ssrf") == "gkn-ssrf.myid.ceye.io"


def test_factory_ceye_via_env(monkeypatch):
    monkeypatch.setenv("GKN_CEYE_IDENTIFIER", "envid")
    monkeypatch.setenv("GKN_CEYE_TOKEN", "envtok")
    c = get_oob_client(provider="ceye")
    assert c.get_domain("t") == "t.envid.ceye.io"


def test_factory_interactsh_missing_binary(monkeypatch):
    monkeypatch.setattr(oob_mod.shutil, "which", lambda name: None)
    assert get_oob_client(provider="interactsh") is None


# ---------------------------------------------------------------------------
# Local fake provider APIs (ceye / dnslog over HTTP)
# ---------------------------------------------------------------------------


class _FakeOOBApiHandler(BaseHTTPRequestHandler):
    """Emulates the ceye.io and dnslog.cn HTTP APIs on one local server."""

    def log_message(self, *args):
        pass

    def _send(self, body: str, ctype: str = "application/json"):
        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        from urllib.parse import urlsplit, parse_qs
        parts = urlsplit(self.path)
        qs = {k: v[0] for k, v in parse_qs(parts.query).items()}

        if parts.path == "/v1/records":  # ceye
            rtype = qs.get("type", "dns")
            records = [
                {"name": "gkn-ssrf-url.myid.ceye.io.", "type": rtype,
                 "time": "2026-09-17 10:00:00"},
                {"name": "gkn-redir.myid.ceye.io.", "type": rtype,
                 "time": "2026-09-17 10:00:01"},
                {"name": "other-tag.myid.ceye.io.", "type": rtype,
                 "time": "2026-09-17 10:00:02"},
            ]
            self._send(json.dumps({"code": 200, "data": records}))
        elif parts.path == "/getdomain.php":  # dnslog
            self._send("abc123.dnslog.cn", ctype="text/plain")
        elif parts.path == "/getrecords.php":  # dnslog
            self._send(json.dumps([
                {"Hostkey": "gkn-x", "Host": "gkn-x.abc123.dnslog.cn",
                 "Type": "A", "Time": "2026-09-17 10:00"},
                {"Hostkey": "zzz", "Host": "zzz.abc123.dnslog.cn",
                 "Type": "A", "Time": "2026-09-17 10:01"},
            ]))
        else:
            self.send_response(404)
            self.end_headers()


@pytest.fixture(scope="module")
def fake_oob_api():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FakeOOBApiHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def test_ceye_client_poll_matching(fake_oob_api):
    c = CeyeClient("myid", "tok", api_base=fake_oob_api, timeout=5)
    # ceye.io exposes both dns and http record types — either is evidence
    hits = c.poll("gkn-ssrf-url", wait=0.5)
    assert hits, "expected at least one tagged interaction"
    assert all("gkn-ssrf-url" in h["name"] for h in hits)
    assert {h["type"] for h in hits} == {"dns", "http"}
    # no match → empty after wait window
    assert c.poll("no-such-tag", wait=0.5) == []
    # tag=None → full record dump (3 records × 2 types)
    everything = c.poll()
    assert len(everything) >= 3
    c.close()


def test_ceye_client_domain_shape():
    c = CeyeClient("myid", "tok")
    assert c.get_domain("gkn") == "gkn.myid.ceye.io"
    assert c.to_dict() == {"provider": "ceye", "identifier": "myid"}
    assert "tok" not in json.dumps(c.to_dict())  # token never serialized


def test_dnslog_client_domain_and_poll(fake_oob_api):
    c = DnslogClient(api_base=fake_oob_api, timeout=5)
    assert c.get_domain("gkn-x") == "gkn-x.abc123.dnslog.cn"
    hits = c.poll("gkn-x", wait=0.5)
    assert len(hits) == 1
    assert "gkn-x" in hits[0]["Host"]
    assert c.poll("missing-tag", wait=0.5) == []
    assert c.to_dict()["provider"] == "dnslog"


def test_dnslog_client_unreachable():
    c = DnslogClient(api_base="http://127.0.0.1:1", timeout=0.5)
    assert c.get_domain("gkn") is None
    assert c.poll("gkn", wait=0.5) == []


# ---------------------------------------------------------------------------
# interactsh subprocess client (mocked Popen)
# ---------------------------------------------------------------------------


class _FakeInteractshProc:
    """Minimal stand-in for the interactsh-client subprocess."""

    def __init__(self, stderr_text: str, stdout_text: str):
        self.stderr = io.StringIO(stderr_text)
        self.stdout = io.StringIO(stdout_text)
        self.terminated = False

    def terminate(self):
        self.terminated = True

    def poll(self):
        return None


def test_interactsh_client_domain_and_poll(monkeypatch):
    correlation = "abc123def456ghi789"
    banner = (
        "interactsh-client v1.2.0\n"
        f"[INF] Using interaction correlation-id: {correlation}\n"
        "[INF] A new correlation ID generated\n"
    )
    interactions = "\n".join([
        json.dumps({"full-id": f"gkn-ssrf-url.{correlation}.oast.fun",
                    "protocol": "http", "remote-address": "1.2.3.4"}),
        json.dumps({"full-id": f"noise.{correlation}.oast.fun",
                    "protocol": "dns"}),
    ]) + "\n"

    holder = {}

    def fake_popen(cmd, **kwargs):
        holder["proc"] = _FakeInteractshProc(banner, interactions)
        return holder["proc"]

    monkeypatch.setattr(oob_mod.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(
        oob_mod.shutil, "which",
        lambda name: "/fake/bin/interactsh-client" if name.startswith("interactsh") else None,
    )

    client = InteractshClient("/fake/bin/interactsh-client", startup_timeout=5)
    # domain: {tag}.{correlation}.{server}
    assert client.get_domain("gkn-ssrf") == f"gkn-ssrf.{correlation}.oast.fun"
    # poll finds the tagged interaction from the stream
    hits = client.poll("gkn-ssrf-url", wait=0.5)
    assert len(hits) == 1
    assert "gkn-ssrf-url" in hits[0]["full-id"]
    assert client.poll("gkn-ssrf-noise", wait=0.3) == []
    client.close()
    assert holder["proc"].terminated
    # serializable state
    assert client.to_dict()["correlation_id"] == correlation


def test_interactsh_client_no_correlation(monkeypatch):
    """A subprocess that never prints a correlation-id → unusable client."""
    def fake_popen(cmd, **kwargs):
        return _FakeInteractshProc("garbage startup noise\n", "")

    monkeypatch.setattr(oob_mod.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(oob_mod.shutil, "which", lambda name: "/fake/interactsh")
    client = InteractshClient("/fake/interactsh", startup_timeout=0.5)
    assert client.get_domain("gkn") is None


def test_interactsh_client_custom_server(monkeypatch):
    """--interactsh-server https://oast.example.com shapes the domain."""
    def fake_popen(cmd, **kwargs):
        return _FakeInteractshProc(
            "[INF] correlation-id: 1234567890abcdef12\n", "")

    monkeypatch.setattr(oob_mod.subprocess, "Popen", fake_popen)
    client = InteractshClient("/fake/interactsh", server="https://oast.example.com")
    assert client.get_domain("t") == "t.1234567890abcdef12.oast.example.com"
    client.close()


def test_interactsh_server_arg_passed(monkeypatch):
    cmd_seen = {}

    def fake_popen(cmd, **kwargs):
        cmd_seen["cmd"] = cmd
        return _FakeInteractshProc("correlation-id: 1234567890abcdef12\n", "")

    monkeypatch.setattr(oob_mod.subprocess, "Popen", fake_popen)
    client = InteractshClient("/fake/interactsh", server="https://oast.example.com")
    assert "-s" in cmd_seen["cmd"]
    assert "https://oast.example.com" in cmd_seen["cmd"]
    assert "-json" in cmd_seen["cmd"]
    client.close()


# ---------------------------------------------------------------------------
# Base contract
# ---------------------------------------------------------------------------


def test_oob_client_base_contract():
    base = OOBClient()
    assert base.poll() == []
    assert base.get_domain() if False else base.to_dict() == {"provider": "base"}
    base.close()  # no-op, never raises
