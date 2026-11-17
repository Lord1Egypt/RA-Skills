#!/usr/bin/env python3
"""Shared utilities for GKN-Phantom scripts.

This module centralizes the cross-cutting helpers that every script
re-implemented inline:
  - json_io: load/dump JSON with UTF-8 + "-" stdin support
  - DNS resolve with timeout (used by scope_guard)
  - logging: structured record for execution_log entries
  - dedup: stable hash for finding reproducibility checks

Importable: from utils import json_io, resolve_ips, log_event, finding_fingerprint
CLI: none
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import io
import json
import socket
import sys
from typing import Any

# Default DNS timeout in seconds. Conservative: scope_guard runs at the very
# start of every state transition; a hung DNS lookup should never block the
# state machine.
DEFAULT_DNS_TIMEOUT = 3.0


# ---- JSON I/O ---------------------------------------------------------------
def load_json(source: str) -> Any:
    """Load JSON from a file path or stdin ('-'). Always UTF-8.

    On Linux in minimal CI/Docker environments where LANG=C, Python's
    sys.stdin defaults to ASCII. We wrap it with TextIOWrapper to force
    UTF-8 so non-ASCII JSON (Chinese trigger phrases, etc.) survives.
    """
    if source == "-":
        stdin_wrapper = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        return json.load(stdin_wrapper)
    with open(source, "r", encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(obj: Any, indent: int = 2) -> str:
    """Return obj serialized as JSON (UTF-8, ASCII-safe via ensure_ascii=False)."""
    return json.dumps(obj, indent=indent, ensure_ascii=False)


# ---- DNS --------------------------------------------------------------------
def resolve_ips(host: str, timeout: float = DEFAULT_DNS_TIMEOUT) -> list:
    """Resolve host -> list of IPs with a hard timeout. Empty list on failure.

    Caches within a single run (TTL = run lifetime) to prevent DNS-rebinding
    scope bypass between scope check and the actual request.
    """
    if not hasattr(resolve_ips, "_cache"):
        resolve_ips._cache = {}  # type: ignore[attr-defined]
    cache = resolve_ips._cache  # type: ignore[attr-defined]
    if host in cache:
        return cache[host]
    saved = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        try:
            infos = socket.getaddrinfo(host, None)
        except (socket.gaierror, socket.timeout, OSError):
            return []
        ips = sorted({i[4][0] for i in infos})
    finally:
        socket.setdefaulttimeout(saved)
    cache[host] = ips
    return ips


def clear_dns_cache() -> None:
    """Reset the per-run DNS cache. Call between runs to force fresh lookups."""
    if hasattr(resolve_ips, "_cache"):
        resolve_ips._cache = {}  # type: ignore[attr-defined]


# ---- Logging ----------------------------------------------------------------
def utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_event(state: str, msg: str, **extra: Any) -> dict:
    """Build a structured execution_log entry. Caller appends to state.history."""
    entry: dict[str, Any] = {"ts": utc_now_iso(), "state": state, "msg": msg}
    entry.update(extra)
    return entry


# ---- Finding fingerprint (for dedup + memory) ------------------------------
def finding_fingerprint(finding: dict) -> str:
    """Stable short hash over (type, target, evidence.request).

    Two findings are considered the SAME if their fingerprints match. Use this
    to dedup against memory.prior_findings so repeat runs don't re-report
    unchanged issues.
    """
    payload = json.dumps(
        {
            "type": finding.get("type", ""),
            "target": finding.get("target", ""),
            "request": (finding.get("evidence", {}) or {}).get("request", ""),
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def dedup_against_memory(findings: list, prior: list) -> tuple[list, list]:
    """Split findings into (new, already_known) based on fingerprint memory.

    Returns (new_findings, known_findings). `known_findings` retain their
    status from prior memory; the agent logs them as "known, no change".
    """
    prior_map = {finding_fingerprint(f): f for f in prior or []}
    new, known = [], []
    for f in findings or []:
        fp = finding_fingerprint(f)
        if fp in prior_map:
            known.append({**prior_map[fp], "fingerprint": fp, "state": "known"})
        else:
            new.append({**f, "fingerprint": fp})
    return new, known
