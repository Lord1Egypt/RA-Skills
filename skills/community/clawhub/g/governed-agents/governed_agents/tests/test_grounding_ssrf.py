import os
import socket
from types import SimpleNamespace

import pytest

from governed_agents import grounding_gate


class DummyResp:
    def __init__(self, status=200):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _mock_getaddrinfo(mapping: dict[str, tuple[int, str]]):
    def _impl(host, *_args, **_kwargs):
        family, ip = mapping[host]
        if family == socket.AF_INET6:
            sockaddr = (ip, 0, 0, 0)
        else:
            sockaddr = (ip, 0)
        return [(family, socket.SOCK_STREAM, 6, "", sockaddr)]

    return _impl


def test_ssrf_dns_rebinding_blocked(monkeypatch):
    monkeypatch.setattr(
        grounding_gate.socket,
        "getaddrinfo",
        _mock_getaddrinfo({"evil.attacker.com": (socket.AF_INET, "192.168.1.1")}),
    )
    assert grounding_gate._check_url("http://evil.attacker.com") is False


def test_ssrf_localhost_blocked(monkeypatch):
    monkeypatch.setattr(
        grounding_gate.socket,
        "getaddrinfo",
        _mock_getaddrinfo({"localhost": (socket.AF_INET, "127.0.0.1")}),
    )
    assert grounding_gate._check_url("http://localhost") is False


def test_ssrf_ipv6_loopback_blocked(monkeypatch):
    monkeypatch.setattr(
        grounding_gate.socket,
        "getaddrinfo",
        _mock_getaddrinfo({"localhost": (socket.AF_INET6, "::1")}),
    )
    assert grounding_gate._check_url("http://localhost") is False


def test_ssrf_literal_private_ip_blocked(monkeypatch):
    monkeypatch.setattr(
        grounding_gate.socket,
        "getaddrinfo",
        _mock_getaddrinfo({"192.168.0.1": (socket.AF_INET, "192.168.0.1")}),
    )
    assert grounding_gate._check_url("http://192.168.0.1") is False


def test_ssrf_public_ip_allowed(monkeypatch):
    monkeypatch.setattr(
        grounding_gate.socket,
        "getaddrinfo",
        _mock_getaddrinfo({"github.com": (socket.AF_INET, "140.82.121.4")}),
    )
    monkeypatch.setattr(
        grounding_gate.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: DummyResp(status=200),
    )
    assert grounding_gate._check_url("https://github.com") is True


def test_ssrf_no_network_env_skips(monkeypatch):
    monkeypatch.setenv("GOVERNED_NO_NETWORK", "1")
    monkeypatch.setattr(
        grounding_gate.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("unexpected DNS")),
    )
    assert grounding_gate._check_url("https://example.com") is True
