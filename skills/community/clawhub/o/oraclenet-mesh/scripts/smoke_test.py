#!/usr/bin/env python3
"""Check that the free OracleNet surfaces answer and are shaped as documented.

Every check here is free and read-only: GET on the public discovery files plus
one POST to the free handshake with a harmless intent. No payment is offered,
no 402 is answered, no transaction is opened, and no message is posted.

Usage:
    smoke_test.py                 run the live free checks
    smoke_test.py --offline       run only checks that need no network
    smoke_test.py --json          machine-readable result

Exit codes:
    0   every check passed
    1   at least one check failed
   64   usage error

Python 3.11+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

__version__ = "3.0.0"

BASE = "https://tooloracle.io"
USER_AGENT = f"oraclenet-mesh-skill-smoke/{__version__} (+https://github.com/ToolOracle/oraclenet-mesh-skill)"
DEFAULT_TIMEOUT = 15.0

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 64

# (path, required top-level keys). Required keys are limited to fields that were
# observed live; everything else is treated as optional on purpose.
SURFACES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("/.well-known/agent.json", ("name", "description")),
    ("/.well-known/agent-pulse", ("mesh_state", "timestamp")),
    ("/.well-known/deal-capabilities.json", ("interaction_types",)),
    ("/.well-known/pricing.json", ("tiers",)),
    ("/.well-known/rewards.json", ("reward_categories",)),
    ("/.well-known/verification-policy.json", ("jwks_url",)),
    ("/.well-known/jwks.json", ("keys",)),
    ("/.well-known/do-not-contact.json", ("entries",)),
)

HANDSHAKE_INTENT = "List available capability categories. Discovery only, no payment."

PACKAGE_FILES = (
    "SKILL.md",
    "scripts/route.py",
    "scripts/smoke_test.py",
    "references/route-recipes.md",
    "references/verification.md",
    "references/x402-safety.md",
)


class Results:
    def __init__(self) -> None:
        self.checks: list[dict] = []

    def record(self, name: str, passed: bool, detail: str) -> None:
        self.checks.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    @property
    def failed(self) -> int:
        return sum(1 for c in self.checks if c["status"] == "FAIL")

    @property
    def passed(self) -> int:
        return sum(1 for c in self.checks if c["status"] == "PASS")


def http_json(url: str, timeout: float, payload: dict | None = None) -> tuple[int, object]:
    """Fetch *url* and parse JSON. GET unless *payload* is given."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if data is not None:
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed https base
        return response.status, json.loads(response.read().decode("utf-8"))


def check_surface(results: Results, path: str, required: tuple[str, ...], timeout: float) -> None:
    url = f"{BASE}{path}"
    try:
        status, body = http_json(url, timeout)
    except urllib.error.HTTPError as exc:
        results.record(path, False, f"HTTP {exc.code}")
        return
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        results.record(path, False, f"network error: {exc}")
        return
    except json.JSONDecodeError as exc:
        results.record(path, False, f"invalid JSON: {exc}")
        return

    if status != 200:
        results.record(path, False, f"expected HTTP 200, got {status}")
        return
    if not isinstance(body, dict):
        results.record(path, False, f"expected a JSON object, got {type(body).__name__}")
        return

    missing = [key for key in required if key not in body]
    if missing:
        results.record(path, False, f"missing required key(s): {', '.join(missing)}")
        return

    results.record(path, True, f"HTTP 200, JSON object, {len(body)} top-level keys")


def check_handshake(results: Results, timeout: float) -> None:
    url = f"{BASE}/handshake"
    try:
        status, body = http_json(url, timeout, payload={"intent": HANDSHAKE_INTENT})
    except urllib.error.HTTPError as exc:
        results.record("POST /handshake", False, f"HTTP {exc.code}")
        return
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        results.record("POST /handshake", False, f"network error: {exc}")
        return
    except json.JSONDecodeError as exc:
        results.record("POST /handshake", False, f"invalid JSON: {exc}")
        return

    if status != 200 or not isinstance(body, dict):
        results.record("POST /handshake", False, f"HTTP {status}, unexpected body type")
        return

    if "classification" not in body and "routing" not in body:
        results.record("POST /handshake", False, "neither 'classification' nor 'routing' present")
        return

    routing = body.get("routing") if isinstance(body.get("routing"), dict) else {}
    interfaces = routing.get("interfaces") if isinstance(routing.get("interfaces"), list) else []
    free = sum(1 for i in interfaces if isinstance(i, dict) and i.get("auth") == "none")
    results.record(
        "POST /handshake",
        True,
        f"HTTP 200, {len(interfaces)} interface(s), {free} free",
    )


def check_mcp_entry(results: Results, timeout: float) -> None:
    """GET the MCP entry point. This is a hint document, not a tool call."""
    url = f"{BASE}/quantum/mcp/"
    try:
        status, body = http_json(url, timeout)
    except urllib.error.HTTPError as exc:
        results.record("GET /quantum/mcp/", False, f"HTTP {exc.code}")
        return
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        results.record("GET /quantum/mcp/", False, f"error: {exc}")
        return

    if status != 200 or not isinstance(body, dict):
        results.record("GET /quantum/mcp/", False, f"HTTP {status}")
        return

    results.record("GET /quantum/mcp/", True, f"HTTP 200, protocol={body.get('protocol')!r}")


def check_package_files(results: Results) -> None:
    root = Path(__file__).resolve().parent.parent
    missing = [name for name in PACKAGE_FILES if not (root / name).is_file()]
    if missing:
        results.record("package files", False, f"missing: {', '.join(missing)}")
    else:
        results.record("package files", True, f"all {len(PACKAGE_FILES)} files present")


def check_route_module(results: Results) -> None:
    """Exercise route.py's pure logic without touching the network."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        import route  # noqa: PLC0415 - deliberately late, keeps the module optional
    except Exception as exc:  # pragma: no cover - import failure is the finding
        results.record("route.py import", False, str(exc))
        return

    results.record("route.py import", True, f"version {route.__version__}")

    blocked = route.scan_for_secrets("my api_key = sk-abcdefghijklmnop")
    results.record(
        "route.py secret guard",
        bool(blocked),
        f"blocked patterns: {blocked}" if blocked else "guard did NOT block a credential-like intent",
    )

    clean = route.scan_for_secrets("Find current XRPL liquidity and verify the result")
    results.record(
        "route.py no false positive",
        not clean,
        "ordinary intent passes" if not clean else f"false positive: {clean}",
    )

    fixture = {
        "classification": {"oracle": "XRPLOracle", "confidence": "medium", "source": "static_keyword_match"},
        "classifier_status": "ok",
        "routing": {
            "interfaces": [
                {"protocol": "MCP", "endpoint": "https://example.invalid/mcp/", "auth": "none"},
                {"protocol": "MCP+x402", "endpoint": "https://example.invalid/x402/mcp/", "auth": "x402-payment"},
            ]
        },
    }
    summary = route.summarize(fixture, "https://example.invalid/handshake", "test intent", 200, 12)
    ok = (
        summary["selected_route"] == "XRPLOracle"
        and summary["payment_required"] == "false"
        and summary["free_interface_count"] == 1
        and summary["paid_interface_count"] == 1
        and summary["payment_performed"] is False
    )
    results.record("route.py summarize", ok, "free/paid interfaces classified correctly" if ok else f"unexpected: {summary}")

    paid_only = route.summarize(
        {"routing": {"interfaces": [{"protocol": "MCP+x402", "endpoint": "x", "auth": "x402-payment"}]}},
        "https://example.invalid/handshake", "test", 200, 5,
    )
    ok_paid = paid_only["payment_required"] == "true" and paid_only["free_interface_count"] == 0
    results.record("route.py paid-only route", ok_paid, "paid-only route flagged" if ok_paid else f"unexpected: {paid_only}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="smoke_test.py",
        description="Free, read-only checks of the public OracleNet surfaces. Never pays.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 all passed, 1 at least one failure, 64 usage error.",
    )
    parser.add_argument("--offline", action="store_true", help="run only checks that need no network")
    parser.add_argument("--json", action="store_true", dest="as_json", help="machine-readable output")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help=f"per-request timeout (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--version", action="version", version=f"smoke_test.py {__version__}")
    args = parser.parse_args(argv)

    if args.timeout <= 0:
        print("error: --timeout must be greater than 0", file=sys.stderr)
        return EXIT_USAGE

    results = Results()

    check_package_files(results)
    check_route_module(results)

    if not args.offline:
        for path, required in SURFACES:
            check_surface(results, path, required, args.timeout)
        check_handshake(results, args.timeout)
        check_mcp_entry(results, args.timeout)

    if args.as_json:
        print(json.dumps(
            {
                "mode": "offline" if args.offline else "live",
                "passed": results.passed,
                "failed": results.failed,
                "payment_performed": False,
                "checks": results.checks,
            },
            indent=2,
        ))
    else:
        for check in results.checks:
            print(f"[{check['status']}] {check['check']} — {check['detail']}")
        print()
        mode = "offline" if args.offline else "live"
        print(f"{results.passed} passed, {results.failed} failed ({mode} mode). No payment was performed.")

    return EXIT_OK if results.failed == 0 else EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
