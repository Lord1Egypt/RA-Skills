#!/usr/bin/env python3
"""Scope Guard for the GKN-Phantom Penetration Testing Skill.

Validates every target (and optionally every concrete request URL) against the
AgentContext scope. Used at the SCOPE_CHECK state of the skill state machine.

Rules (see references/safety_policy.md §2):
  - domain match: host equals or is a subdomain of a scope.domains entry.
    Entries starting with "*." allow any subdomain; otherwise exact match.
  - ip range match: resolved IP within one of scope.ip_ranges (CIDR).
  - path allowlist: path starts with one of scope.allowed_paths (empty => all).
  - path blocklist: path matches any scope.blocked_paths entry => reject.

Exit codes:
  0  all targets in scope
  1  one or more targets out of scope (offenders printed to stderr)
  2  input error

Usage:
  python scope_guard.py --context ctx.json
  cat ctx.json | python scope_guard.py --context -
  python scope_guard.py --url https://staging.example.test/api/x --context ctx.json
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys
from urllib.parse import urlparse

# Allow `python scope_guard.py` from anywhere: prepend this script's dir so
# `import utils` works.
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, resolve_ips


def _match_domain(host: str, pattern: str) -> bool:
    host = host.lower().rstrip(".")
    pattern = pattern.lower().rstrip(".")
    if pattern.startswith("*."):
        suffix = pattern[2:]
        return host == suffix or host.endswith("." + suffix)
    return host == pattern


def _match_path(path: str, allowed: list[str], blocked: list[str]) -> bool:
    if blocked:
        for b in blocked:
            if path == b or path.startswith(b.rstrip("/") + "/"):
                return False
    if not allowed:
        return True
    for a in allowed:
        if path == a or path.startswith(a.rstrip("/") + "/") or a == "/":
            return True
    return False


# _resolve removed — now uses utils.resolve_ips() (with timeout + cache)
_resolve = resolve_ips


def _ip_in_ranges(ip: str, ranges: list[str]) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for r in ranges:
        try:
            if addr in ipaddress.ip_network(r, strict=False):
                return True
        except ValueError:
            continue
    return False


def check_target(target: str, scope: dict) -> tuple[bool, str]:
    """Return (in_scope, reason). reason is empty when in_scope=True."""
    parsed = urlparse(target if "://" in target else "http://" + target)
    host = parsed.hostname or ""
    path = parsed.path or "/"

    domains = scope.get("domains", [])
    ip_ranges = scope.get("ip_ranges", [])
    allowed_paths = scope.get("allowed_paths", [])
    blocked_paths = scope.get("blocked_paths", [])

    # Domain match
    if domains and not any(_match_domain(host, d) for d in domains):
        return False, f"host '{host}' does not match any scope domain"

    # IP range match (resolve at request time to avoid DNS-rebinding bypass)
    ips = _resolve(host)
    if not ips:
        return False, f"could not resolve host '{host}'"
    if ip_ranges and not any(_ip_in_ranges(ip, ip_ranges) for ip in ips):
        return False, f"host '{host}' ({', '.join(ips)}) not in any scope ip range"

    # Path match
    if not _match_path(path, allowed_paths, blocked_paths):
        return False, f"path '{path}' rejected by allowed/blocked path lists"

    return True, ""


def run(targets: list[str], scope: dict) -> tuple[bool, list[str]]:
    offenders: list[str] = []
    for t in targets:
        ok, reason = check_target(t, scope)
        if not ok:
            offenders.append(f"{t}: {reason}")
    return (len(offenders) == 0), offenders


def _load_context(path: str) -> dict:
    return load_json(path)


def main() -> int:
    ap = argparse.ArgumentParser(description="GKN-Phantom scope guard")
    ap.add_argument("--context", required=True, help="Path to AgentContext JSON, or '-' for stdin")
    ap.add_argument("--url", help="Optional single URL to check instead of ctx.targets")
    args = ap.parse_args()

    try:
        ctx = _load_context(args.context)
    except (OSError, json.JSONDecodeError) as e:
        print(f"scope_guard: input error: {e}", file=sys.stderr)
        return 2

    scope = ctx.get("scope", {})
    if not scope.get("domains") and not scope.get("ip_ranges"):
        print("scope_guard: scope must define domains and/or ip_ranges", file=sys.stderr)
        return 2

    targets = [args.url] if args.url else ctx.get("targets", [])
    if not targets:
        print("scope_guard: no targets to check", file=sys.stderr)
        return 2

    ok, offenders = run(targets, scope)
    if ok:
        print(json.dumps({"ok": True, "checked": len(targets)}))
        return 0
    print(json.dumps({"ok": False, "offenders": offenders}), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
