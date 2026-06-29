#!/usr/bin/env python3
"""Fetch the OpenRouter /api/v1/models listing and save it to disk.

The endpoint is public — no API key is required. If a key is supplied
(via --api-key or env OPENROUTER_API_KEY) it is used for higher rate
limits and to attribute requests to your account.

Usage:
    python3 fetch_models.py [--api-key KEY] [--out PATH]

Default output path is alongside this script: models_raw.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://openrouter.ai/api/v1/models"
DEFAULT_OUT = Path(__file__).resolve().parent / "models_raw.json"


def fetch(api_key: str | None) -> dict:
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(API_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} from {API_URL}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: cannot reach {API_URL} — {e.reason}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError:
        print(f"ERROR: request to {API_URL} timed out", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in response — {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENROUTER_API_KEY"),
        help="Optional. OpenRouter API key, or set OPENROUTER_API_KEY. "
             "Endpoint is public; key only affects rate limits / attribution.",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    data = fetch(args.api_key)
    models = data.get("data", [])
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Fetched {len(models)} models -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
