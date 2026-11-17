#!/usr/bin/env python3
"""Shared pytest fixtures for the GKN-Phantom v3.0 test suite.

Provides sample data (findings, assets, attack paths) and a temporary
report output directory for use by all test modules.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def sample_findings() -> list[dict[str, Any]]:
    """Return 4 sample findings — one per severity tier — in the
    GKN-Phantom Finding schema format (status=validated)."""
    return [
        {
            "id": "finding-001",
            "type": "rce",
            "severity": "critical",
            "tier": "critical",
            "target": "https://example.com/api/exec",
            "status": "validated",
            "confidence": 0.92,
            "evidence": {
                "request": "POST /api/exec HTTP/1.1\nHost: example.com\n\ncmd=;sleep 5 #",
                "response": "HTTP/1.1 200 OK\n\ntime_delta=5.1s",
                "timestamp": "2025-01-15T10:30:00Z",
                "tool": "manual_probe",
            },
            "reproducible": True,
            "safe_poc": False,
            "risk_level": "L4",
            "requires_human_approval": True,
            "blocked_in_safe_mode": True,
            "detection_signal": "Time-based command execution confirmed",
            "remediation": "Sanitize all user input passed to system calls; use parameterized APIs.",
            "fingerprint": "a1b2c3d4e5f60001",
        },
        {
            "id": "finding-002",
            "type": "sqli",
            "severity": "high",
            "tier": "high",
            "target": "https://example.com/api/users?id=1",
            "status": "validated",
            "confidence": 0.85,
            "evidence": {
                "request": "GET /api/users?id=1' OR '1'='1 HTTP/1.1\nHost: example.com",
                "response": 'HTTP/1.1 200 OK\n\n[{"id":1,"name":"admin"},{"id":2,"name":"user"}]',
                "timestamp": "2025-01-15T10:31:00Z",
                "tool": "manual_probe",
            },
            "reproducible": True,
            "safe_poc": True,
            "risk_level": "L2",
            "requires_human_approval": False,
            "blocked_in_safe_mode": False,
            "detection_signal": "SQL error signature in response",
            "remediation": "Use parameterized queries or prepared statements.",
            "fingerprint": "a1b2c3d4e5f60002",
        },
        {
            "id": "finding-003",
            "type": "xss",
            "severity": "medium",
            "tier": "medium",
            "target": "https://example.com/search?q=test",
            "status": "validated",
            "confidence": 0.78,
            "evidence": {
                "request": "GET /search?q=<script>alert(1)</script> HTTP/1.1\nHost: example.com",
                "response": 'HTTP/1.1 200 OK\n\nResults for: <script>alert(1)</script>',
                "timestamp": "2025-01-15T10:32:00Z",
                "tool": "manual_probe",
            },
            "reproducible": True,
            "safe_poc": True,
            "risk_level": "L2",
            "requires_human_approval": False,
            "blocked_in_safe_mode": False,
            "detection_signal": "Marker reflected unescaped",
            "remediation": "HTML-encode user input before rendering in responses.",
            "fingerprint": "a1b2c3d4e5f60003",
        },
        {
            "id": "finding-004",
            "type": "misconfig",
            "severity": "low",
            "tier": "low",
            "target": "https://example.com/",
            "status": "validated",
            "confidence": 0.95,
            "evidence": {
                "request": "GET / HTTP/1.1\nHost: example.com",
                "response": 'HTTP/1.1 200 OK\nServer: Apache/2.4.7\nX-Powered-By: PHP/5.5.9',
                "timestamp": "2025-01-15T10:33:00Z",
                "tool": "header_inspect",
            },
            "reproducible": True,
            "safe_poc": True,
            "risk_level": "L1",
            "requires_human_approval": False,
            "blocked_in_safe_mode": False,
            "detection_signal": "Security headers missing; version headers present",
            "remediation": "Remove version banners; add HSTS, CSP, X-Frame-Options headers.",
            "fingerprint": "a1b2c3d4e5f60004",
        },
    ]


@pytest.fixture
def sample_assets() -> dict[str, Any]:
    """Return a sample assets dictionary with domains, IPs, endpoints,
    SSL report, and technology stack."""
    return {
        "domains": [
            "example.com",
            "api.example.com",
            "admin.example.com",
        ],
        "ips": [
            "93.184.216.34",
            "93.184.216.35",
        ],
        "endpoints": [
            {"url": "https://example.com/", "method": "GET", "params": []},
            {"url": "https://example.com/api/users", "method": "GET", "params": ["id"]},
            {"url": "https://example.com/api/login", "method": "POST", "params": ["username", "password"]},
            {"url": "https://example.com/search", "method": "GET", "params": ["q"]},
            {"url": "https://example.com/upload", "method": "POST", "params": ["file"]},
        ],
        "ssl_report": {
            "example.com": {
                "tls_versions": ["TLS 1.2", "TLS 1.3"],
                "cert_valid": True,
                "cert_expiry": "2026-06-15",
                "issuer": "Let's Encrypt",
            }
        },
        "tech_stack": {
            "web_server": "nginx/1.24.0",
            "backend": "Python/Flask",
            "database": "PostgreSQL 15",
            "cdn": "None",
        },
    }


@pytest.fixture
def sample_attack_paths() -> list[dict[str, Any]]:
    """Return 2 sample attack paths demonstrating exploitation chains."""
    return [
        {
            "id": "path-001",
            "name": "SQLi → Data Exfiltration",
            "severity": "critical",
            "steps": [
                {
                    "step": 1,
                    "action": "Identify injectable parameter 'id' on /api/users",
                    "finding_id": "finding-002",
                },
                {
                    "step": 2,
                    "action": "Extract database schema via UNION SELECT",
                    "finding_id": None,
                },
                {
                    "step": 3,
                    "action": "Dump user credentials (emails + password hashes)",
                    "finding_id": None,
                },
            ],
            "impact": "Full user database compromise — 10k+ records exposed.",
        },
        {
            "id": "path-002",
            "name": "XSS → Session Hijacking → Account Takeover",
            "severity": "high",
            "steps": [
                {
                    "step": 1,
                    "action": "Inject stored XSS payload via /search reflected param",
                    "finding_id": "finding-003",
                },
                {
                    "step": 2,
                    "action": "Victim admin triggers payload → session cookie exfiltrated",
                    "finding_id": None,
                },
            ],
            "impact": "Admin session hijacked; full admin panel access gained.",
        },
    ]


@pytest.fixture
def tmp_report_dir(tmp_path: Path) -> Path:
    """Create and return a temporary directory for report output."""
    report_dir = tmp_path / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir
