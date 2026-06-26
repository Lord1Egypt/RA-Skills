#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests"
# ]
# ///

"""
Perform web search using the /web-search API.

Usage:
    python perform_web_search.py --query "your query" [--summary true] [--freshness noLimit] [--count 10] [--api-key KEY]
"""

import argparse
import json
import os
import sys
from typing import Optional

import requests

API_URL = "https://ai.gitee.com/v1/web-search"


def str_to_bool(value: str) -> bool:
    """Parse CLI booleans."""
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("Expected one of: true, false, 1, 0, yes, no")


def get_api_key(provided_key: Optional[str]) -> Optional[str]:
    """Get API key from argument or environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GITEEAI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Perform web search using the /web-search API"
    )
    parser.add_argument(
        "--query", "-q",
        required=True,
        help="Search keywords or natural language query"
    )
    parser.add_argument(
        "--summary",
        type=str_to_bool,
        default=True,
        help="Whether to include summary in the results (true/false). Default: true"
    )
    parser.add_argument(
        "--freshness",
        default="noLimit",
        choices=["noLimit", "oneDay", "oneWeek", "oneMonth", "oneYear"],
        help="Time filter for the search results"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of results to return. Default: 10"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gitee AI API key for Authorization: Bearer <token>"
    )

    args = parser.parse_args()

    if args.count < 1 or args.count > 50:
        print("Error: --count must be between 1 and 50.", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GITEEAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    payload = {
        "query": args.query,
        "summary": args.summary,
        "freshness": args.freshness,
        "count": args.count,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print("Performing web search...")
    print(f"URL: {API_URL}")
    print(f"Query: {args.query}")
    print(f"Summary: {args.summary}")
    print(f"Freshness: {args.freshness}")
    print(f"Count: {args.count}")

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
    except requests.HTTPError as exc:
        body = ""
        if exc.response is not None:
            try:
                body = exc.response.text
            except Exception:
                body = ""
        print(f"Error performing web search: HTTP error: {exc}", file=sys.stderr)
        if body:
            print(body, file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as exc:
        print(f"Error performing web search: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"Error parsing JSON response: {exc}", file=sys.stderr)
        sys.exit(1)

    print("\nSEARCH_RESULTS_JSON:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
