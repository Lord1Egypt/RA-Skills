#!/usr/bin/env python3
"""
engage.py — Engagement orchestrator for follows, comments, replies, and insights.

Provides a unified interface for platform engagement actions, delegating
to the appropriate connector via connectors.load().

Usage (CLI):
    python3 -m act.engage --platform x --action follow --handles "@user1,@user2" --account myaccount
    python3 -m act.engage --platform linkedin --action comment --post-url URL --text "reply" --account myaccount
    python3 -m act.engage --platform x --action insights --account myaccount

Usage (library):
    from act.engage import follow_accounts, post_comment, gather_insights
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from act.connectors import load as load_connector


# ── Follow ──────────────────────────────────────────────────────────────────


def parse_handles_from_file(path: str) -> list[tuple[str, str]]:
    """Parse handles from a markdown list file.

    Expected format:  - @handle — Description
    Lines with [SKIP] are excluded.
    """
    handles = []
    with open(path) as f:
        for line in f:
            m = re.match(r"\s*[-*]\s+(@\w+)\s*[—–-]?\s*(.*)", line.strip())
            if m and "[SKIP]" not in line:
                handles.append((m.group(1), m.group(2).strip()))
    return handles


def follow_accounts(
    platform: str,
    handles: list[str],
    account: str,
) -> list[dict[str, Any]]:
    """Follow a list of accounts on the given platform.

    Returns list of results, one per handle.
    """
    connector = load_connector(platform)
    results = []
    for handle in handles:
        try:
            result = connector.follow(handle, account)
            results.append(result)
        except NotImplementedError:
            results.append({
                "handle": handle,
                "status": "not_implemented",
                "message": f"{platform} follow not yet implemented via API",
            })
        except Exception as e:
            print(f"[engage] Unexpected error following {handle}: {e}", file=sys.stderr)
            results.append({
                "handle": handle,
                "status": "error",
                "message": str(e),
            })
    return results


# ── Comments / Replies ──────────────────────────────────────────────────────


def post_comment(
    platform: str,
    post_url: str,
    text: str,
    account: str,
) -> dict[str, Any]:
    """Post a comment/reply on an existing post."""
    connector = load_connector(platform)
    return connector.comment(post_url, text, account)


# ── Insights / Stats ───────────────────────────────────────────────────────


def gather_insights(
    platform: str,
    account: str,
    post_url: str | None = None,
) -> dict[str, Any]:
    """Gather engagement stats for an account or specific post."""
    connector = load_connector(platform)
    return connector.get_stats(account, post_url)


# ── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Platform engagement actions")
    parser.add_argument("--platform", required=True, choices=["x", "linkedin"])
    parser.add_argument("--account", required=True, help="Account key from credentials")
    parser.add_argument("--action", required=True, choices=["follow", "comment", "insights"])

    # Follow args
    parser.add_argument("--handles", help="Comma-separated handles (for follow)")
    parser.add_argument("--handles-file", help="Markdown file with handles (for follow)")

    # Comment args
    parser.add_argument("--post-url", help="URL of post to comment on")
    parser.add_argument("--text", help="Comment/reply text")

    args = parser.parse_args()

    try:
        if args.action == "follow":
            if args.handles_file:
                parsed = parse_handles_from_file(args.handles_file)
                handles = [h for h, _ in parsed]
            elif args.handles:
                handles = [h.strip() for h in args.handles.split(",")]
            else:
                parser.error("--handles or --handles-file required for follow action")
            results = follow_accounts(args.platform, handles, args.account)
            print(json.dumps(results, indent=2))

        elif args.action == "comment":
            if not args.post_url or not args.text:
                parser.error("--post-url and --text required for comment action")
            result = post_comment(args.platform, args.post_url, args.text, args.account)
            print(json.dumps(result, indent=2))

        elif args.action == "insights":
            result = gather_insights(args.platform, args.account, args.post_url)
            print(json.dumps(result, indent=2))

    except NotImplementedError as e:
        print(f"NOT IMPLEMENTED: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[engage] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
