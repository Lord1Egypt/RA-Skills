#!/usr/bin/env python3
"""Retained-access OpenMandate CLI helper for OpenClaw agents.

Stdlib-only (no pip dependencies). Agents call:
    python3 openmandate.py <command> [args]

Requires OPENMANDATE_API_KEY env var. Optionally override
OPENMANDATE_BASE_URL (default: https://api.openmandate.ai).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

VERSION = "0.6.2"
USER_AGENT = f"openmandate-openclaw/{VERSION}"
DEFAULT_BASE_URL = "https://api.openmandate.ai"
API_KEY_ENV = "OPENMANDATE_API_KEY"
BASE_URL_ENV = "OPENMANDATE_BASE_URL"
PRIVATE_DEVELOPMENT_CODE = "SERVICE_PRIVATE_DEVELOPMENT"
PRIVATE_DEVELOPMENT_MESSAGE = (
    "OpenMandate is in private development; new mandates and integrations "
    "are unavailable."
)


# ── Helpers ──────────────────────────────────────────────────────────


def _get_api_key() -> str:
    key = os.environ.get(API_KEY_ENV, "")
    if not key:
        _die(f"Missing {API_KEY_ENV} environment variable.")
    return key


def _get_base_url() -> str:
    return os.environ.get(BASE_URL_ENV, DEFAULT_BASE_URL).rstrip("/")


def _die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def _request(method: str, path: str, params: dict | None = None) -> dict:
    """Make an HTTP request to the OpenMandate API and return parsed JSON."""
    base = _get_base_url()
    url = f"{base}{path}"

    if params:
        query = urllib.parse.urlencode({key: value for key, value in params.items() if value is not None})
        if query:
            url = f"{url}?{query}"

    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {_get_api_key()}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp_body = resp.read().decode("utf-8")
            if not resp_body:
                return {}
            return json.loads(resp_body)
    except urllib.error.HTTPError as exc:
        try:
            err_body = json.loads(exc.read().decode("utf-8"))
            err = err_body.get("error", {})
            code = err.get("code", "UNKNOWN")
            message = err.get("message", exc.reason)
            _die(f"[{exc.code}] {code}: {message}")
        except (json.JSONDecodeError, ValueError):
            _die(f"[{exc.code}] {exc.reason}")
    except urllib.error.URLError as exc:
        _die(f"Connection failed: {exc.reason}")

    return {}  # unreachable, but keeps linters happy


def _print_json(data: dict | list) -> None:
    print(json.dumps(data, indent=2))


# ── Commands ─────────────────────────────────────────────────────────


def cmd_get(args: argparse.Namespace) -> None:
    result = _request("GET", f"/v1/mandates/{args.mandate_id}")
    _print_json(result)


def cmd_list(args: argparse.Namespace) -> None:
    params: dict = {}
    if args.status:
        params["status"] = args.status
    if args.limit:
        params["limit"] = args.limit
    result = _request("GET", "/v1/mandates", params=params)
    _print_json(result)


def cmd_close(args: argparse.Namespace) -> None:
    result = _request("POST", f"/v1/mandates/{args.mandate_id}/close")
    _print_json(result)


def cmd_matches(args: argparse.Namespace) -> None:
    result = _request("GET", "/v1/matches")
    _print_json(result)


def cmd_match(args: argparse.Namespace) -> None:
    result = _request("GET", f"/v1/matches/{args.match_id}")
    _print_json(result)


def cmd_decline(args: argparse.Namespace) -> None:
    result = _request("POST", f"/v1/matches/{args.match_id}/decline")
    _print_json(result)


def cmd_contacts(args: argparse.Namespace) -> None:
    result = _request("GET", "/v1/contacts")
    _print_json(result)


def cmd_delete_contact(args: argparse.Namespace) -> None:
    result = _request("DELETE", f"/v1/contacts/{args.contact_id}")
    _print_json(result)


def cmd_unavailable(args: argparse.Namespace) -> None:
    _die(f"{PRIVATE_DEVELOPMENT_CODE}: {args.command}: {PRIVATE_DEVELOPMENT_MESSAGE}")


# ── Argument Parser ──────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openmandate",
        description="OpenMandate CLI helper for OpenClaw agents.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    # get
    p_get = sub.add_parser("get", help="Get a mandate by ID")
    p_get.add_argument("mandate_id", help="Mandate ID (e.g. mnd_xxx)")
    p_get.set_defaults(func=cmd_get)

    # list
    p_list = sub.add_parser("list", help="List mandates")
    p_list.add_argument("--status", default=None, help="Filter by status (active, intake, matched, closed). Open mandates returned by default.")
    p_list.add_argument("--limit", type=int, default=None, help="Max results")
    p_list.set_defaults(func=cmd_list)

    # close
    p_close = sub.add_parser("close", help="Close a mandate")
    p_close.add_argument("mandate_id", help="Mandate ID")
    p_close.set_defaults(func=cmd_close)

    # matches
    p_matches = sub.add_parser("matches", help="List all matches")
    p_matches.set_defaults(func=cmd_matches)

    # match
    p_match = sub.add_parser("match", help="Get a match by ID")
    p_match.add_argument("match_id", help="Match ID (e.g. m_xxx)")
    p_match.set_defaults(func=cmd_match)

    # decline
    p_decline = sub.add_parser("decline", help="Decline a match")
    p_decline.add_argument("match_id", help="Match ID")
    p_decline.set_defaults(func=cmd_decline)

    # contacts
    p_contacts = sub.add_parser("contacts", help="List verified contacts")
    p_contacts.set_defaults(func=cmd_contacts)

    # delete-contact
    p_del = sub.add_parser("delete-contact", help="Delete a contact")
    p_del.add_argument("contact_id", help="Contact ID (e.g. vc_xxx)")
    p_del.set_defaults(func=cmd_delete_contact)

    unavailable_commands = {
        "create": "new mandate creation",
        "answer": "intake progression",
        "accept": "match acceptance",
        "outcome": "outcome submission",
        "add-contact": "contact creation",
        "verify-contact": "contact verification",
        "update-contact": "contact updates",
        "resend-otp": "verification-code delivery",
    }
    for command, purpose in unavailable_commands.items():
        unavailable = sub.add_parser(
            command,
            help=f"Unavailable during private development: {purpose}",
        )
        unavailable.add_argument("arguments", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
        unavailable.set_defaults(func=cmd_unavailable)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
