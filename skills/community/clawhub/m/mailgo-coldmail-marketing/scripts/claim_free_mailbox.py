#!/usr/bin/env python3
"""
Claim a free pre-warmed mailbox from Mailgo.

Uses only stdlib (urllib) — zero third-party dependencies.

Usage:
    python3 claim_free_mailbox.py
    python3 claim_free_mailbox.py --api-key "your-token-here"
    python3 claim_free_mailbox.py --json

Requires:
    MAILGO_API_KEY environment variable (or --api-key flag)

Output:
    Human-readable summary on stdout (default) or JSON with --json flag.
    Errors on stderr.
"""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

_ssl_ctx = ssl.create_default_context()
# Do NOT disable certificate verification — MITM attacks would allow token theft

BASE = "https://api.leadsnavi.com"
ENDPOINT = "/mcp/mailgo-auth/api/biz/benefits/assign-prewarm"

USER_AGENT = "mailgo-mcp-server/1.0 (https://github.com/netease-im/leadsnavi-mcp-server)"


def claim_free_mailbox(api_key, base_url=None):
    """
    Claim a free pre-warmed mailbox.

    Returns:
        (success: bool, email: str | None, error: str | None)
    """
    url = f"{base_url or BASE}{ENDPOINT}"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }

    # POST with empty body
    data = json.dumps({}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, None, "Authentication failed. Please check your MAILGO_API_KEY."
        if e.code == 405:
            return False, None, (
                f"HTTP 405 Method Not Allowed. "
                f"The API endpoint may have changed. URL: {url}"
            )
        err_body = e.read().decode("utf-8", errors="replace")
        return False, None, f"HTTP {e.code}: {err_body[:500]}"
    except urllib.error.URLError as e:
        return False, None, f"Cannot connect to {url}: {e.reason}"
    except Exception as e:
        return False, None, f"Unexpected error: {e}"

    # Parse response
    if not isinstance(body, dict) or "code" not in body:
        return False, None, f"Invalid API response format: {body}"

    if body["code"] != 0:
        msg = body.get("message", "Unknown error")
        return False, None, f"API error (code {body['code']}): {msg}"

    email = body.get("data")
    if email is None:
        return False, None, "No free mailbox available in the pool. Please contact support."

    if not isinstance(email, str) or "@" not in email:
        return False, None, f"Invalid email format in response: {email}"

    return True, email, None


def main():
    parser = argparse.ArgumentParser(
        description="Claim a free pre-warmed mailbox from Mailgo"
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="MAILGO_API_KEY (OpenAPI Key). Reads from env var if omitted.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Base URL for Mailgo API. Default: https://api.leadsnavi.com",
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output result in JSON format",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("MAILGO_API_KEY")
    if not api_key:
        if args.json_output:
            print(json.dumps({"success": False, "error": "MAILGO_API_KEY not set"}))
        else:
            print(
                "Error: MAILGO_API_KEY is required.\n"
                "Set it via environment variable or use --api-key.",
                file=sys.stderr,
            )
        sys.exit(1)

    if not args.json_output:
        print("Claiming free pre-warmed mailbox...", file=sys.stderr)

    success, email, error = claim_free_mailbox(api_key, args.base_url)

    if args.json_output:
        if success:
            result = {
                "success": True,
                "email": email,
                "info": {
                    "type": "PW_ACCOUNT",
                    "validity_period": "60 days",
                    "status": "DEPLOYED",
                    "sender_score": "90+",
                },
            }
        else:
            result = {"success": False, "error": error}
        print(json.dumps(result, indent=2))
    else:
        if success:
            print(f"Success! Free mailbox claimed: {email}", file=sys.stderr)
            print(f"  Validity: 60 days | Sender Score: 90+", file=sys.stderr)
            print(f"  Ready for cold email campaigns.", file=sys.stderr)
            # Print just the email to stdout for easy scripting
            print(email)
        else:
            print(f"Failed to claim mailbox: {error}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
