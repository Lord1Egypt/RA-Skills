#!/usr/bin/env python3
"""
Fetch comments from Polymarket Gamma API for a given event.

Retrieves holder comments via the public comments endpoint. Supports
lookup by event slug (auto-resolves to numeric ID) or direct numeric ID.

Usage:
    python fetch_comments.py --slug "will-aliens-be-confirmed"
    python fetch_comments.py --event-id 90177
    python fetch_comments.py --slug "strait-of-hormuz" --limit 30
"""

import argparse
import http.client
import json
import sys
import time
import urllib.request
import urllib.parse

GAMMA_API = "https://gamma-api.polymarket.com"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "polymarket-market-pulse/1.0",
}


def fetch_with_retry(url: str, headers: dict, max_retries: int = 3, backoff: float = 1.0):
    """Fetch a URL with exponential-backoff retry on transient errors."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except (urllib.error.URLError,
                http.client.IncompleteRead,
                http.client.RemoteDisconnected,
                TimeoutError,
                ConnectionResetError) as e:
            if attempt < max_retries - 1:
                wait = backoff * (2 ** attempt)
                print(f"[WARN] Retry {attempt + 1}/{max_retries} for {url[:80]}... ({e})", file=sys.stderr)
                time.sleep(wait)
            else:
                raise


def resolve_event_id(slug: str) -> int:
    """Resolve an event slug to its numeric ID via the Gamma API."""
    url = f"{GAMMA_API}/events?slug={urllib.parse.quote(slug)}&limit=1"
    data = fetch_with_retry(url, HEADERS)
    if not data:
        raise ValueError(f"Event not found for slug: {slug}")
    event = data[0] if isinstance(data, list) else data
    event_id = event.get("id")
    if event_id is None:
        raise ValueError(f"Event has no ID field: {slug}")
    print(f"[INFO] Resolved slug '{slug}' -> event ID {event_id}", file=sys.stderr)
    return int(event_id)


def fetch_comments(event_id: int, limit: int = 20) -> list:
    """Fetch comments for an event from the Gamma API."""
    url = (
        f"{GAMMA_API}/comments"
        f"?parent_entity_type=Event"
        f"&parent_entity_id={event_id}"
        f"&limit={limit}"
        f"&order=createdAt"
        f"&ascending=false"
    )
    print(f"[INFO] Fetching up to {limit} comments for event {event_id}...", file=sys.stderr)
    data = fetch_with_retry(url, HEADERS)

    if isinstance(data, dict) and data.get("type") == "validation error":
        raise ValueError(f"API error: {data.get('error', 'unknown')}")

    if not isinstance(data, list):
        return []

    return data


def format_comment(comment: dict) -> dict:
    """Extract relevant fields from a raw comment."""
    profile = comment.get("profile", {})
    name = profile.get("name") or profile.get("pseudonym") or "Anonymous"
    return {
        "id": comment.get("id"),
        "author": name,
        "body": comment.get("body", ""),
        "created_at": comment.get("createdAt"),
        "is_reply": comment.get("parentCommentID") is not None,
        "reply_to_comment_id": comment.get("parentCommentID"),
        "reaction_count": comment.get("reactionCount", 0),
        "user_address": comment.get("userAddress"),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch Polymarket event comments")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--slug", type=str, help="Event slug (will resolve to numeric ID)")
    group.add_argument("--event-id", type=int, help="Numeric event ID")
    parser.add_argument("--limit", type=int, default=20, help="Max comments to fetch (default: 20)")
    parser.add_argument("--raw", action="store_true", help="Output raw API response without formatting")
    parser.add_argument("--output", type=str, default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    event_id = args.event_id if args.event_id else resolve_event_id(args.slug)

    try:
        raw_comments = fetch_comments(event_id, args.limit)
    except Exception as e:
        print(f"[ERROR] Failed to fetch comments: {e}", file=sys.stderr)
        sys.exit(1)

    if args.raw:
        result = raw_comments
    else:
        result = {
            "event_id": event_id,
            "total_fetched": len(raw_comments),
            "comments": [format_comment(c) for c in raw_comments],
        }

    print(f"[INFO] Fetched {len(raw_comments)} comments for event {event_id}", file=sys.stderr)

    json_str = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
