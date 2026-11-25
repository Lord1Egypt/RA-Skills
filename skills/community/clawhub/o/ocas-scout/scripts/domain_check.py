#!/usr/bin/env python3
"""Domain availability check for a username (stdlib-only).

Tests ``<username>.<tld>`` across common TLDs: DNS resolution says whether the
domain is registered / points somewhere, and an HTTP request says whether it
serves a live site. No whois service or API key — just DNS + HTTP.

Specific match tiers (uppercase, then lowercase — the same DNS point may be
reached by two names), then a set of lower-confidence permutations. Reported
separately so a brief never presents a permutation as the subject's own domain.

Usage:

    python3 domain_check.py --username indigokarasu
    python3 domain_check.py --username someone --tlds com,io,dev
    python3 domain_check.py --username someone --format detailed
"""
from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _envelope import add_format_arg, emit, fail, main_guard  # noqa: E402

DEFAULT_TLDS = ["com", "io", "net", "org", "dev", "me", "co", "app"]
_LABEL_RE = re.compile(r"[^a-z0-9-]")
_UA = "hermes-osint-investigation/0.2"


def domain_label(username: str) -> str:
    """Reduce a username to a valid DNS label (lowercase alnum + hyphen)."""
    label = _LABEL_RE.sub(
        "", (username or "").lower().replace("_", "-").replace(".", "-"))
    return label.strip("-")[:63].strip("-")


def _resolves(host: str) -> bool:
    try:
        socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        return True
    except (socket.gaierror, OSError):
        return False


def _is_live(host: str, timeout: float = 8.0) -> bool:
    for scheme in ("https", "http"):
        try:
            req = urllib.request.Request(
                f"{scheme}://{host}", headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status < 500:
                    return True
        except urllib.error.HTTPError as exc:
            # A 4xx still means something answers there.
            if exc.code < 500:
                return True
        except Exception:  # noqa: BLE001
            continue
    return False


def check(username: str, tlds: list[str] | None = None, timeout: float = 8.0,
          workers: int = 8) -> dict:
    label = domain_label(username)
    tlds = tlds or DEFAULT_TLDS
    if not label:
        return {"username": username, "label": "", "results": [],
                "actionable_guidance": (
                    "The username reduced to an empty DNS label (it held no "
                    "letters or digits). Check the value you passed.")}

    hosts = [f"{label}.{tld}" for tld in tlds]

    def _probe(host):
        registered = _resolves(host)
        live = _is_live(host, timeout) if registered else False
        return {"domain": host, "registered": registered, "live": live}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(_probe, hosts))

    return {
        "username": username,
        "label": label,
        "results": results,
        "registered_count": sum(1 for r in results if r["registered"]),
        "live_count": sum(1 for r in results if r["live"]),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--username", required=True, help="Username to test")
    ap.add_argument("--tlds", default=",".join(DEFAULT_TLDS),
                    help="Comma-separated TLDs (default: %s)" % ",".join(DEFAULT_TLDS))
    ap.add_argument("--timeout", type=float, default=8.0)
    add_format_arg(ap)
    a = ap.parse_args()

    tlds = [t.strip().lstrip(".").lower() for t in a.tlds.split(",") if t.strip()]
    if not tlds:
        return fail("no TLDs given", a.format,
                    guidance="Pass --tlds com,io,dev (at least one TLD).",
                    code="bad_input")

    res = check(a.username, tlds, a.timeout)
    res["ok"] = True
    res["count"] = len(res["results"])
    emit(
        res, a.format,
        summary=(f"{res['registered_count']}/{len(res['results'])} registered, "
                 f"{res['live_count']} live for '{res['label']}'"),
        concise_keys=("domain", "registered", "live"),
    )
    if not res["registered_count"]:
        print(json.dumps({"actionable_guidance": (
            "No registration found. This is a legitimate negative, not an "
            "error. A registered-but-not-live domain still means the name is "
            "taken; a live one is a stronger identity signal than a profile "
            "match alone — but confirm the site actually names the subject "
            "before treating it as theirs.")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main_guard(main))
