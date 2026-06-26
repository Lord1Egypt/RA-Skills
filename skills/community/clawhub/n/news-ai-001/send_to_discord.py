#!/usr/bin/env python3
"""
send_to_discord.py
------------------
Send a daily news digest embed to a Discord channel via webhook.

Usage:
    python3 send_to_discord.py \\
        --webhook  "https://discord.com/api/webhooks/..." \\
        --date     "Monday, March 6, 2026" \\
        --topics   "AI & Tech" \\
        --stories  '[{"headline":"...","summary":"...","url":"..."}]'

    # Alternatively, load stories from a temp file:
    python3 send_to_discord.py \\
        --webhook "..." --date "..." --topics "..." \\
        --stories-file /tmp/stories.json
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error


# Discord embed colour (blurple)
EMBED_COLOR = 0x5865F2


def build_payload(stories: list, date_str: str, topics: str) -> dict:
    """Construct the Discord webhook JSON payload."""
    fields = []
    for i, story in enumerate(stories[:5], start=1):
        headline = (story.get("headline") or "")[:80]
        summary  = (story.get("summary")  or "")[:250]
        url      = (story.get("url")      or "").strip()

        value = summary if summary else "No summary available."
        if url:
            value += f"\n[Read more]({url})"

        fields.append({
            "name":   f"{i}. {headline}",
            "value":  value,
            "inline": False,
        })

    embed = {
        "title":       f"📰 Daily News Digest — {date_str}",
        "description": f"Today's top stories in **{topics}**",
        "color":       EMBED_COLOR,
        "fields":      fields,
        "footer": {
            "text": "OpenClaw Daily News • Powered by Claude"
        },
    }

    return {
        "username": "Daily News",
        "embeds":   [embed],
    }


def post_to_discord(webhook_url: str, payload: dict, retries: int = 2) -> int:
    """POST the payload to the Discord webhook, retrying on 429 (rate limit)."""
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    for attempt in range(1, retries + 2):
        try:
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                print(f"✅ Sent successfully! HTTP {status}")
                return status
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            if e.code == 429 and attempt <= retries:
                retry_after = 2
                try:
                    retry_after = json.loads(body).get("retry_after", 2)
                except Exception:
                    pass
                print(f"⏳ Rate limited (429). Retrying in {retry_after}s…", file=sys.stderr)
                time.sleep(retry_after)
                continue
            print(f"❌ Discord error {e.code}: {e.reason}", file=sys.stderr)
            print(f"   Response: {body}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"❌ Network error: {e.reason}", file=sys.stderr)
            sys.exit(1)

    print("❌ Failed after retries.", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Post a news digest to Discord.")
    parser.add_argument("--webhook",      required=True, help="Discord webhook URL")
    parser.add_argument("--date",         default="Today", help="Human-readable date string")
    parser.add_argument("--topics",       default="AI & Tech", help="News topics label")
    parser.add_argument("--stories",      help="JSON array of story objects (inline)")
    parser.add_argument("--stories-file", help="Path to a JSON file containing story array")
    args = parser.parse_args()

    # Load stories from inline arg or file
    if args.stories_file:
        with open(args.stories_file, "r", encoding="utf-8") as f:
            stories = json.load(f)
    elif args.stories:
        stories = json.loads(args.stories)
    else:
        print("❌ Provide --stories or --stories-file", file=sys.stderr)
        sys.exit(1)

    if not isinstance(stories, list) or len(stories) == 0:
        print("❌ Stories must be a non-empty JSON array.", file=sys.stderr)
        sys.exit(1)

    payload = build_payload(stories, args.date, args.topics)
    post_to_discord(args.webhook, payload)


if __name__ == "__main__":
    main()
