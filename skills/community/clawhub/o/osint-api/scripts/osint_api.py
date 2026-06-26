#!/usr/bin/env python3
"""
OSINT API — Skill Helper Script
Security Manifest:
  - Environment: OSINT_API_KEY (optional, for authenticated endpoints)
  - External: https://osint.ahsan-tariq-ai.xyz/api/v1/*
  - Local: No files read or written
  - Data: No data collection or persistence

Usage:
    python3 osint_api.py reports [--category CATEGORY]
    python3 osint_api.py categories
    python3 osint_api.py recon --domain DOMAIN
    python3 osint_api.py social --username USERNAME
    python3 osint_api.py breach --email EMAIL
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import HTTPError, URLError

BASE_URL = "https://osint.ahsan-tariq-ai.xyz/api/v1"
API_KEY = os.environ.get("OSINT_API_KEY", "")

if not API_KEY:
    print("Error: OSINT_API_KEY environment variable is required.", file=sys.stderr)
    print("Get a key: curl -X POST https://osint.ahsan-tariq-ai.xyz/api/v1/signup -d 'email=you@example.com'", file=sys.stderr)
    sys.exit(1)

def make_request(method, path, data=None):
    """Make an authenticated HTTPS request to the OSINT API."""
    url = f"{BASE_URL}{path}"
    body = None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    if data:
        body = json.dumps(data).encode("utf-8")

    req = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        print(f"Error: HTTP {e.code} — {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Error: Connection failed — {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="OSINT API Helper")
    sub = parser.add_subparsers(dest="command", required=True)

    # reports
    p_reports = sub.add_parser("reports", help="Get intelligence reports")
    p_reports.add_argument("--category", help="Filter by category")

    # categories
    sub.add_parser("categories", help="List available categories")

    # recon
    p_recon = sub.add_parser("recon", help="Domain reconnaissance")
    p_recon.add_argument("--domain", required=True, help="Domain to investigate")

    # social
    p_social = sub.add_parser("social", help="Social media lookup")
    p_social.add_argument("--username", required=True, help="Username to search")

    # breach
    p_breach = sub.add_parser("breach", help="Breach database check")
    p_breach.add_argument("--email", required=True, help="Email to check")

    args = parser.parse_args()

    if args.command == "reports":
        path = "/reports/enriched"
        if args.category:
            path += f"?category={quote(args.category)}"
        result = make_request("GET", path)

    elif args.command == "categories":
        result = make_request("GET", "/reports/categories")

    elif args.command == "recon":
        result = make_request("GET", f"/recon/{quote(args.domain)}")

    elif args.command == "social":
        result = make_request("GET", f"/social/{quote(args.username)}")

    elif args.command == "breach":
        result = make_request("GET", f"/breach/{quote(args.email)}")

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
