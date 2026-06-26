#!/usr/bin/env python3
"""
OpenTable search URL builder.

This script DOES NOT fetch OpenTable and DOES NOT open a browser.
It builds the exact search URL the user would have typed and prints
a single-line JSON object for the skill's next step.

The skill then hands that URL to `openclaw browser open` (the native
OpenClaw browser plugin) with the `--browser-profile attached` target,
so navigation happens inside OpenClaw's managed Chromium where Akamai
detection is bypassed and the user can see results in their attached
browser session.

Why this is split from the browser-open step:
- URL construction is deterministic and zero-network, so it stays in
  Python — reliable, testable, schema-pinned.
- Browser automation uses OpenClaw's own CLI, which already knows about
  profiles, SSRF policy, and approvals. Wrapping it in subprocess from
  a script would just reinvent the wheel badly.

Usage:
    python3 search.py \\
        --location "New York" \\
        --date-time 2026-04-12T19:00 \\
        --party 2 \\
        --query italian
"""
from __future__ import annotations

import argparse
import json
import sys
from urllib.parse import quote


SEARCH_BASE = "https://www.opentable.com/s"


def build_search_url(location: str, date_time: str, party: int, query: str) -> str:
    term = f"{query} {location}".strip() if query else location
    params = {
        "term":     term,
        "dateTime": date_time,
        "covers":   str(party),
        "metroId":  "0",
    }
    qs = "&".join(f"{k}={quote(v)}" for k, v in params.items())
    return f"{SEARCH_BASE}?{qs}"


def main() -> int:
    p = argparse.ArgumentParser(description="OpenTable search URL builder")
    p.add_argument("--location",  required=True, help="City / neighborhood / ZIP")
    p.add_argument("--date-time", required=True, help="YYYY-MM-DDTHH:MM (local)")
    p.add_argument("--party",     type=int, required=True)
    p.add_argument("--query",     default="",   help="Optional cuisine / keyword")
    args = p.parse_args()

    url = build_search_url(args.location, args.date_time, args.party, args.query)

    payload = {
        "search_url":   url,
        "next_step":    "openclaw browser --browser-profile attached open <search_url>",
        "instructions": (
            "Hand this URL to `openclaw browser open` on the attached profile. "
            "Then either ask the user which restaurant they want, or run "
            "`openclaw browser snapshot --efficient` to see the results directly."
        ),
    }
    print(json.dumps(payload, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
