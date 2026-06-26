#!/usr/bin/env python3
"""Small read-first NextDNS API helper for OpenClaw skills.

Environment:
  NEXTDNS_API_KEY       required, unless --api-key is provided
  NEXTDNS_PROFILE_ID    optional default profile id
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://api.nextdns.io"
ANALYTICS_ENDPOINTS = {
    "status",
    "domains",
    "reasons",
    "ips",
    "devices",
    "protocols",
    "queryTypes",
    "ipVersions",
    "dnssec",
    "encryption",
    "destinations",
}


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2), file=sys.stderr)
    raise SystemExit(code)


def request_json(method: str, path: str, api_key: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    query = ""
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        query = "?" + urllib.parse.urlencode(clean, doseq=True) if clean else ""
    url = f"{BASE_URL}{path}{query}"
    req = urllib.request.Request(url, method=method, headers={
        "X-Api-Key": api_key,
        "Accept": "application/json",
        "User-Agent": "openclaw-nextdns-helper/0.1",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8")
            return {"ok": True, "status": resp.status, "url": url, "response": json.loads(raw) if raw else None}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            body: Any = json.loads(raw)
        except Exception:
            body = raw
        return {"ok": False, "status": e.code, "url": url, "response": body}
    except urllib.error.URLError as e:
        return {"ok": False, "status": None, "url": url, "error": str(e.reason)}


def add_common_query(p: argparse.ArgumentParser) -> None:
    p.add_argument("--from", dest="from_", help="Start date/time, e.g. -24h, -7d, ISO date")
    p.add_argument("--to", help="End date/time, e.g. now or ISO date")
    p.add_argument("--limit", type=int, help="API limit")
    p.add_argument("--cursor", help="Pagination cursor")
    p.add_argument("--device", help="Device id or __UNIDENTIFIED__")


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only NextDNS API helper")
    parser.add_argument("--api-key", default=os.getenv("NEXTDNS_API_KEY"), help="NextDNS API key; defaults to NEXTDNS_API_KEY")
    parser.add_argument("--profile", default=os.getenv("NEXTDNS_PROFILE_ID"), help="NextDNS profile id; defaults to NEXTDNS_PROFILE_ID")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("profiles", help="List profiles available to the API key")
    sub.add_parser("profile", help="Get full profile config; needs --profile")

    a = sub.add_parser("analytics", help="Get an analytics endpoint; needs --profile")
    a.add_argument("endpoint", choices=sorted(ANALYTICS_ENDPOINTS))
    a.add_argument("--series", action="store_true", help="Use ;series time-series endpoint")
    a.add_argument("--status", choices=["default", "blocked", "allowed"], help="For domains endpoint")
    a.add_argument("--root", choices=["true", "false"], help="For domains endpoint")
    a.add_argument("--type", choices=["countries", "gafam"], help="For destinations endpoint")
    a.add_argument("--interval", help="For series, e.g. 1h, 1d, 3600")
    a.add_argument("--alignment", choices=["start", "end", "clock"])
    a.add_argument("--timezone", help="IANA timezone for clock-aligned series")
    a.add_argument("--partials", choices=["none", "start", "end", "all"])
    add_common_query(a)

    l = sub.add_parser("logs", help="Get recent logs; needs --profile")
    l.add_argument("--sort", choices=["asc", "desc"])
    l.add_argument("--status", choices=["default", "error", "blocked", "allowed"])
    l.add_argument("--search", help="Domain/search string")
    l.add_argument("--raw", action="store_true", help="Show all DNS queries, not deduped navigational subset")
    add_common_query(l)

    args = parser.parse_args()
    if not args.api_key:
        die("Missing API key. Set NEXTDNS_API_KEY or pass --api-key.")

    params: dict[str, Any] = {}
    path = ""
    if args.command == "profiles":
        path = "/profiles"
    else:
        if not args.profile:
            die("Missing profile id. Set NEXTDNS_PROFILE_ID or pass --profile.")
        if args.command == "profile":
            path = f"/profiles/{urllib.parse.quote(args.profile)}"
        elif args.command == "analytics":
            endpoint = args.endpoint + (";series" if args.series else "")
            path = f"/profiles/{urllib.parse.quote(args.profile)}/analytics/{endpoint}"
            params = {
                "from": args.from_, "to": args.to, "limit": args.limit, "cursor": args.cursor,
                "device": args.device, "status": args.status, "root": args.root, "type": args.type,
                "interval": args.interval, "alignment": args.alignment, "timezone": args.timezone,
                "partials": args.partials,
            }
        elif args.command == "logs":
            path = f"/profiles/{urllib.parse.quote(args.profile)}/logs"
            params = {
                "from": args.from_, "to": args.to, "limit": args.limit, "cursor": args.cursor,
                "device": args.device, "sort": args.sort, "status": args.status,
                "search": args.search, "raw": "1" if args.raw else None,
            }

    result = request_json("GET", path, args.api_key, params)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
