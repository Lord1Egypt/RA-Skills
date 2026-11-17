#!/usr/bin/env python3
"""Send one free OracleNet handshake and report the recommended route.

This script does exactly one thing: it POSTs a natural-language intent to the
free OracleNet handshake endpoint and prints a structured summary of the route
that came back.

It deliberately does NOT:
  * send any credential, API key, or payment header
  * follow up by calling the recommended endpoint
  * retry, poll, or fan out to other services

Exit codes:
    0   success
    1   network error (DNS, connection, timeout, TLS)
    2   invalid or unexpected response (bad HTTP status, non-JSON, wrong shape)
   64   usage error (bad arguments, or an intent that looks like it holds a secret)

Python 3.11+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request

__version__ = "3.0.0"

DEFAULT_ENDPOINT = "https://tooloracle.io/handshake"
DEFAULT_TIMEOUT = 15.0
USER_AGENT = f"oraclenet-mesh-skill/{__version__} (+https://github.com/ToolOracle/oraclenet-mesh-skill)"
MAX_INTENT_CHARS = 2000
MAX_RESPONSE_BYTES = 1_000_000

EXIT_OK = 0
EXIT_NETWORK = 1
EXIT_BAD_RESPONSE = 2
EXIT_USAGE = 64

# The intent string is a routing hint, never a payload. These patterns catch the
# most common ways a credential ends up pasted into one by accident.
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("PEM private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("API token prefix", re.compile(r"\b(?:sk-|ghp_|gho_|github_pat_|clh_|xoxb-|xoxp-|AKIA)[A-Za-z0-9_\-]{10,}")),
    ("hex private key or hash", re.compile(r"\b(?:0x)?[0-9a-fA-F]{64}\b")),
    ("bearer credential", re.compile(r"(?i)\b(?:authorization|bearer|x-api-key|api[_-]?key|secret|passphrase)\b\s*[:=]\s*\S+")),
    ("mnemonic seed phrase", re.compile(r"(?i)\b(?:seed|mnemonic|recovery)\s+phrase\b")),
)


class HandshakeError(Exception):
    """Raised when the endpoint answered, but not in a usable way."""


def scan_for_secrets(intent: str) -> list[str]:
    """Return the names of secret patterns found in *intent* (empty if clean)."""
    return [label for label, pattern in SECRET_PATTERNS if pattern.search(intent)]


def post_handshake(endpoint: str, intent: str, timeout: float) -> tuple[int, dict]:
    """POST the intent and return (http_status, parsed_json).

    Raises urllib.error.URLError / OSError on transport failure and
    HandshakeError when the response is not usable JSON.
    """
    body = json.dumps({"intent": intent}).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed https endpoint
        status = response.status
        raw = response.read(MAX_RESPONSE_BYTES + 1)

    if len(raw) > MAX_RESPONSE_BYTES:
        raise HandshakeError(f"response larger than {MAX_RESPONSE_BYTES} bytes")

    if status != 200:
        raise HandshakeError(f"expected HTTP 200, got HTTP {status}")

    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HandshakeError(f"response was not valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise HandshakeError(f"expected a JSON object, got {type(payload).__name__}")

    return status, payload


def summarize(payload: dict, endpoint: str, intent: str, status: int, elapsed_ms: int) -> dict:
    """Reduce a handshake response to the fields an agent needs to decide."""
    classification = payload.get("classification")
    classification = classification if isinstance(classification, dict) else {}

    routing = payload.get("routing")
    routing = routing if isinstance(routing, dict) else {}

    raw_interfaces = routing.get("interfaces")
    raw_interfaces = raw_interfaces if isinstance(raw_interfaces, list) else []

    interfaces = []
    for item in raw_interfaces:
        if not isinstance(item, dict):
            continue
        auth = item.get("auth")
        interfaces.append(
            {
                "protocol": item.get("protocol"),
                "endpoint": item.get("endpoint"),
                "auth": auth,
                # A route is free to try only when it explicitly says so.
                "free_to_try": auth == "none",
            }
        )

    free = [i for i in interfaces if i["free_to_try"]]
    paid = [i for i in interfaces if i["auth"] == "x402-payment"]

    if not interfaces:
        payment_required = "unknown"
    elif free:
        payment_required = "false"
    elif paid:
        payment_required = "true"
    else:
        payment_required = "unknown"

    notes = [
        "The handshake returns no price and no signature status. "
        "Read the per-tool MCP card, the 402 challenge, and the JWKS for those.",
    ]
    if not interfaces:
        notes.append("No routing interfaces were returned — do not call anything.")
    elif not free:
        notes.append("No free interface was offered. A paid call needs explicit authorisation.")
    if classification.get("confidence") == "low":
        notes.append("Classifier confidence is low — consider rephrasing the intent.")

    return {
        "ok": True,
        "intent": intent,
        "endpoint": endpoint,
        "http_status": status,
        "elapsed_ms": elapsed_ms,
        "selected_route": classification.get("oracle"),
        "confidence": classification.get("confidence"),
        "match_source": classification.get("source"),
        "classifier_status": payload.get("classifier_status"),
        "interfaces": interfaces,
        "free_interface_count": len(free),
        "paid_interface_count": len(paid),
        "payment_required": payment_required,
        "payment_performed": False,
        "links": payload.get("links") if isinstance(payload.get("links"), dict) else {},
        "next_steps": payload.get("next_steps") if isinstance(payload.get("next_steps"), list) else [],
        "notes": notes,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="route.py",
        description=(
            "Send one free OracleNet handshake and print the recommended route. "
            "Never sends credentials and never makes a payment."
        ),
        epilog=(
            "Exit codes: 0 success, 1 network error, 2 invalid response, 64 usage error.\n"
            'Example: route.py "Find current XRPL liquidity and verify the result"'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("intent", nargs="*", help="natural-language description of what you need")
    parser.add_argument("--raw", action="store_true", help="print the unmodified handshake response")
    parser.add_argument(
        "--timeout", type=float, default=DEFAULT_TIMEOUT,
        help=f"request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--endpoint", default=DEFAULT_ENDPOINT,
        help=f"handshake endpoint (default: {DEFAULT_ENDPOINT})",
    )
    parser.add_argument("--version", action="version", version=f"route.py {__version__}")
    return parser


def fail(message: str, code: int) -> int:
    print(json.dumps({"ok": False, "error": message}, indent=2))
    print(f"error: {message}", file=sys.stderr)
    return code


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    intent = " ".join(args.intent).strip()
    if not intent:
        parser.print_usage(sys.stderr)
        return fail("no intent given — pass one sentence describing what you need", EXIT_USAGE)

    if len(intent) > MAX_INTENT_CHARS:
        return fail(f"intent longer than {MAX_INTENT_CHARS} characters", EXIT_USAGE)

    found = scan_for_secrets(intent)
    if found:
        return fail(
            "refusing to send: the intent looks like it contains a credential "
            f"({', '.join(found)}). The intent is a routing hint, not a payload.",
            EXIT_USAGE,
        )

    if args.timeout <= 0:
        return fail("--timeout must be greater than 0", EXIT_USAGE)

    if not args.endpoint.startswith(("http://", "https://")):
        return fail("--endpoint must be an http(s) URL", EXIT_USAGE)

    started = time.monotonic()
    try:
        status, payload = post_handshake(args.endpoint, intent, args.timeout)
    except urllib.error.HTTPError as exc:
        return fail(f"handshake returned HTTP {exc.code}", EXIT_BAD_RESPONSE)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return fail(f"network error contacting {args.endpoint}: {exc}", EXIT_NETWORK)
    except HandshakeError as exc:
        return fail(str(exc), EXIT_BAD_RESPONSE)

    elapsed_ms = int((time.monotonic() - started) * 1000)

    if args.raw:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return EXIT_OK

    print(json.dumps(summarize(payload, args.endpoint, intent, status, elapsed_ms), indent=2, ensure_ascii=False))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
