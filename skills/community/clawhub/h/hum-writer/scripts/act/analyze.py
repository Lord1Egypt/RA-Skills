#!/usr/bin/env python3
"""
analyze.py — Gather insights and analytics about your social accounts.

Pulls engagement stats, follower growth, top-performing posts, and
audience patterns across platforms.

Usage (CLI):
    python3 scripts/act/analyze.py --platform x --account <account>
    python3 scripts/act/analyze.py --platform linkedin --account <account>
    python3 scripts/act/analyze.py --platform all --account <account>

Usage (library):
    from act.analyze import analyze_account, analyze_post
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from act.connectors import load as load_connector


def analyze_account(
    platform: str,
    account: str,
) -> dict[str, Any]:
    """Gather account-level insights for a platform.

    Returns dict with engagement metrics, follower stats, and recent post performance.
    For X and LinkedIn (which require JS rendering), returns a result with
    needs_browser=True and browser instructions for the agent to execute.
    """
    connector = load_connector(platform)
    result = connector.get_stats(account)

    if isinstance(result, dict) and result.get("needs_browser"):
        platform_name = result["platform"]
        profile_url = result["profile_url"]
        instructions = _get_browser_instructions(platform_name, profile_url)
        return {
            "needs_browser": True,
            "platform": platform_name,
            "account": account,
            "profile_url": profile_url,
            "instructions": instructions,
        }

    return result


def _get_browser_instructions(platform: str, profile_url: str) -> dict:
    """Return browser scraping instructions for a given platform."""
    if platform == "x":
        return {
            "action": "scrape_x_profile",
            "url": profile_url,
            "steps": [
                f"Navigate to {profile_url}",
                "Wait for the page to fully load (2-3 seconds)",
                "Extract from the profile header:",
                "  - Follower count",
                "  - Following count",
                "  - Post count",
                "  - Profile description/bio",
                "Scroll down and extract up to 10 recent posts, for each:",
                "  - Post text (first 200 chars)",
                "  - Posted date/relative time",
                "  - Like count",
                "  - Repost count",
                "  - Reply count",
                "  - View count (if shown)",
                "  - Post URL",
            ],
            "output_schema": {
                "profile": {
                    "followers": "integer",
                    "following": "integer",
                    "posts": "integer",
                    "bio": "string",
                },
                "recent_posts": [
                    {
                        "type": "original | repost",
                        "original_author": "string (only if repost, e.g. '@jackzhang')",
                        "text": "string (first 200 chars)",
                        "date": "string (relative date)",
                        "likes": "integer",
                        "retweets": "integer",
                        "replies": "integer",
                        "views": "integer (if available)",
                        "url": "string",
                    }
                ],
            },
        }
    elif platform == "linkedin":
        return {
            "action": "scrape_linkedin_profile",
            "url": profile_url,
            "steps": [
                f"Navigate to {profile_url}",
                "Wait for the page to fully load (3-4 seconds)",
                "Extract the following data from the profile:",
                "  - Profile views (number)",
                "  - Post impressions in past 7 days (number)",
                "  - Search appearances (number)",
                "  - Follower count",
                "  - Connection count",
                "Scroll down and extract up to 10 recent posts, for each:",
                "  - Post type: 'original' or 'repost'",
                "  - If repost: original author's name (e.g. 'Jack Zhang')",
                "  - Post text (first 150 chars, or description for link/video posts)",
                "  - Reaction count",
                "  - Comment count",
                "  - Repost count",
                "  - Date posted",
            ],
            "output_schema": {
                "profile_views": "integer",
                "post_impressions_7d": "integer",
                "search_appearances": "integer",
                "followers": "integer",
                "connections": "integer",
                "recent_posts": [
                    {
                        "type": "original | repost",
                        "original_author": "string (only if repost, e.g. '@jackzhang')",
                        "text": "string (first 150 chars)",
                        "reactions": "integer",
                        "comments": "integer",
                        "reposts": "integer",
                        "date": "string",
                    }
                ],
            },
        }
    return {}


def analyze_post(
    platform: str,
    account: str,
    post_url: str,
) -> dict[str, Any]:
    """Gather detailed analytics for a specific post.

    Returns dict with impressions, engagement rate, comments, shares.
    """
    connector = load_connector(platform)
    return connector.get_stats(account, post_url)


def analyze_all(account: str) -> dict[str, Any]:
    """Gather insights across all platforms."""
    results = {}
    for platform in ["x", "linkedin"]:
        try:
            results[platform] = analyze_account(platform, account)
        except NotImplementedError:
            results[platform] = {"status": "not_implemented"}
        except Exception as e:
            print(f"[analyze] Unexpected error on {platform}: {e}", file=sys.stderr)
            results[platform] = {"status": "error", "message": str(e)}
    return results


# ── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Gather account insights and analytics")
    parser.add_argument("--platform", required=True, choices=["x", "linkedin", "all"])
    parser.add_argument("--account", required=True, help="Account key from credentials")
    parser.add_argument("--post-url", help="Specific post URL to analyze")
    args = parser.parse_args()

    try:
        if args.platform == "all":
            result = analyze_all(args.account)
        elif args.post_url:
            result = analyze_post(args.platform, args.account, args.post_url)
        else:
            result = analyze_account(args.platform, args.account)
        print(json.dumps(result, indent=2))
    except NotImplementedError as e:
        print(f"NOT IMPLEMENTED: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[analyze] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
