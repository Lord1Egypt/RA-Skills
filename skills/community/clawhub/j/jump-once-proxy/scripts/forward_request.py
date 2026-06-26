#!/usr/bin/env python3
"""JumpOnce proxy helper — structured HTTP forwarding via JumpOnce API.

Usage:
    python forward_request.py --url <target_url> [--method GET] [--body '{}'] [--headers '{}'] [--timeout 30]

Requires JUMPONCE_API_KEY env var or --api-key flag.
"""

import argparse
import json
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="JumpOnce HTTP proxy request")
    parser.add_argument("--url", required=True, help="Target URL to forward to")
    parser.add_argument("--method", default="GET", help="HTTP method (default: GET)")
    parser.add_argument("--body", default=None, help="Request body (string)")
    parser.add_argument("--headers", default="{}", help="JSON dict of headers")
    parser.add_argument("--params", default="{}", help="JSON dict of query params")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds (max 120)")
    parser.add_argument("--api-key", default=None, help="API key (or set JUMPONCE_API_KEY)")
    parser.add_argument("--raw", action="store_true", help="Use raw passthrough endpoint")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("JUMPONCE_API_KEY")
    if not api_key:
        print("Error: JUMPONCE_API_KEY env var or --api-key required", file=sys.stderr)
        sys.exit(1)

    try:
        import requests
    except ImportError:
        print("Error: 'requests' package required. Install with: pip install requests", file=sys.stderr)
        sys.exit(1)

    base_url = "http://api.jumptox.top"
    endpoint = "/api/v1/http/raw" if args.raw else "/api/v1/http/request"

    payload = {
        "url": args.url,
        "method": args.method.upper(),
        "headers": json.loads(args.headers),
        "params": json.loads(args.params),
        "timeout": min(args.timeout, 120),
        "followRedirects": True,
        "verifySSL": True,
    }
    if args.body is not None:
        payload["body"] = args.body

    resp = requests.post(
        f"{base_url}{endpoint}",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=payload["timeout"] + 10,
    )

    if args.raw:
        sys.stdout.buffer.write(resp.content)
    else:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
