#!/usr/bin/env python3
"""
X (Twitter) connector — API-only.

Uses X API v2 for posting. Browser-based actions (when API is unavailable)
should be handled by the agent via the browser tool.

Credentials: credentials/x.json or X_USER_ACCESS_TOKEN env var.
Format:
    {"accounts": {"account-key": {"username": "@handle", "user_access_token": "..."}}}

Usage:
  python3 -m act.connectors.x --account <account> --text "hello world"
  python3 -m act.connectors.x --account <account> --text "hello" --image /path/to/image.png
  python3 -m act.connectors.x --account <account> --segments '["tweet 1", "tweet 2"]'
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import stat
import sys
from pathlib import Path
from typing import Any

from .http import http_request

CREDENTIALS_DIR = Path(os.environ.get("CREDENTIALS_DIR", Path.home() / ".hum" / "credentials"))
X_CREDS_PATH = CREDENTIALS_DIR / "x.json"

PLATFORM = "x"


class XConnectorError(RuntimeError):
    pass


# Backward compatibility alias
XPostError = XConnectorError
ConnectorError = XConnectorError


# ── Credentials ─────────────────────────────────────────────────────────────


def load_credentials(account: str | None) -> dict[str, Any]:
    """Load X API credentials for the given account."""
    if not X_CREDS_PATH.exists():
        return {}
    cred_path = X_CREDS_PATH
    mode = cred_path.stat().st_mode
    if mode & (stat.S_IRGRP | stat.S_IROTH):
        print(f"Warning: credential file {cred_path} is readable by group/others. Run: chmod 600 {cred_path}", file=sys.stderr)
    with X_CREDS_PATH.open() as f:
        creds = json.load(f)

    root = creds
    if "accounts" in creds:
        if not account:
            raise ConnectorError("X credentials define multiple accounts. Pass --account.")
        if account not in creds["accounts"]:
            return {}
        creds = creds["accounts"][account]

    token = (
        os.environ.get("X_USER_ACCESS_TOKEN")
        or os.environ.get("TWITTER_USER_ACCESS_TOKEN")
        or creds.get("user_access_token")
    )
    if not token:
        return {}

    return {
        "user_access_token": token,
        "username": creds.get("username", root.get("username", account or "unknown")),
    }


def _api_available(account: str | None) -> bool:
    """Check if X API credentials are available."""
    try:
        creds = load_credentials(account)
        return bool(creds.get("user_access_token"))
    except ConnectorError:
        return False


def _x_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


# ── API posting ─────────────────────────────────────────────────────────────


def _upload_media_api(token: str, image_path: Path) -> str:
    """Upload an image to X via API. Returns media_id."""
    content_type, _ = mimetypes.guess_type(image_path.name)
    if content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise ConnectorError("X API media upload supports jpg, png, or webp.")

    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    payload = {
        "media": encoded,
        "media_category": "tweet_image",
        "media_type": content_type,
        "shared": False,
    }
    _, data, _ = http_request(
        "POST",
        "https://api.x.com/2/media/upload",
        headers=_x_headers(token),
        payload=payload,
        exc_factory=ConnectorError,
    )
    media_id = data.get("data", {}).get("id")
    if not media_id:
        raise ConnectorError(f"X media upload did not return an id: {data}")
    return media_id


def _post_api(
    text: str,
    account: str,
    media_path: Path | None = None,
) -> dict[str, Any]:
    """Post a single tweet via X API v2."""
    creds = load_credentials(account)
    token = creds["user_access_token"]

    payload: dict[str, Any] = {"text": text}
    if media_path:
        media_id = _upload_media_api(token, media_path)
        payload["media"] = {"media_ids": [media_id]}

    _, data, _ = http_request(
        "POST",
        "https://api.x.com/2/tweets",
        headers=_x_headers(token),
        payload=payload,
        exc_factory=ConnectorError,
    )
    tweet_id = data.get("data", {}).get("id")
    if not tweet_id:
        raise ConnectorError(f"X post create failed: {data}")

    return {
        "method": "api",
        "platform": "x",
        "account": creds["username"],
        "tweet_id": tweet_id,
        "url": f"https://x.com/{creds['username']}/status/{tweet_id}",
    }


def _post_thread_api(
    segments: list[str],
    account: str,
    media_path: Path | None = None,
) -> dict[str, Any]:
    """Post a thread via X API v2 (reply chain)."""
    creds = load_credentials(account)
    token = creds["user_access_token"]

    for idx, seg in enumerate(segments, 1):
        if len(seg) > 280:
            raise ConnectorError(f"Segment {idx} exceeds 280 chars ({len(seg)}).")

    media_id = _upload_media_api(token, media_path) if media_path else None
    previous_id = None
    posted_ids: list[str] = []

    for idx, seg in enumerate(segments):
        payload: dict[str, Any] = {"text": seg}
        if idx == 0 and media_id:
            payload["media"] = {"media_ids": [media_id]}
        if previous_id:
            payload["reply"] = {"in_reply_to_tweet_id": previous_id}

        _, data, _ = http_request(
            "POST",
            "https://api.x.com/2/tweets",
            headers=_x_headers(token),
            payload=payload,
            exc_factory=ConnectorError,
        )
        tweet_id = data.get("data", {}).get("id")
        if not tweet_id:
            raise ConnectorError(f"X post create failed at segment {idx + 1}: {data}")
        previous_id = tweet_id
        posted_ids.append(tweet_id)

    first_id = posted_ids[0]
    return {
        "method": "api",
        "platform": "x",
        "account": creds["username"],
        "posted_ids": posted_ids,
        "url": f"https://x.com/{creds['username']}/status/{first_id}",
    }


# ── Public API ──────────────────────────────────────────────────────────────


def post(
    text: str,
    account: str,
    media_path: str | None = None,
) -> dict[str, Any]:
    """Post a single tweet via X API.

    Returns dict with: method, platform, account, url, tweet_id.
    Raises ConnectorError if API credentials are missing or the request fails.
    """
    resolved_media = Path(media_path).resolve() if media_path else None
    if not _api_available(account):
        raise ConnectorError(
            "X API credentials not available. "
            "Add credentials to credentials/x.json or set X_USER_ACCESS_TOKEN."
        )
    return _post_api(text, account, resolved_media)


def post_thread(
    segments: list[str],
    account: str,
    media_path: str | None = None,
) -> dict[str, Any]:
    """Post a thread via X API (reply chain).

    Returns dict with: method, platform, account, url, posted_ids.
    Raises ConnectorError if API credentials are missing or the request fails.
    """
    resolved_media = Path(media_path).resolve() if media_path else None
    if not _api_available(account):
        raise ConnectorError(
            "X API credentials not available. "
            "Add credentials to credentials/x.json or set X_USER_ACCESS_TOKEN."
        )
    return _post_thread_api(segments, account, resolved_media)


# ── Stubs (not yet implemented) ─────────────────────────────────────────────


def comment(
    post_url: str,
    text: str,
    account: str,
) -> dict[str, Any]:
    """Reply to an existing X post. Not yet implemented."""
    raise NotImplementedError("X comment not yet implemented")


def follow(
    handle: str,
    account: str,
) -> dict[str, Any]:
    """Follow an X account. Not yet implemented."""
    raise NotImplementedError("X follow not yet implemented")


def get_stats(
    account: str,
    post_url: str | None = None,
) -> dict[str, Any]:
    """Get engagement stats for an X account or post.

    X API v2 stats (public_metrics, impression_count) require Pro tier ($5k/mo).
    Always falls back to browser-based scraping via the agent's browser session.
    """
    creds = load_credentials(account)
    username = creds.get("username", account) if creds else account
    return {
        "needs_browser": True,
        "platform": "x",
        "account": username,
        "profile_url": f"https://x.com/{username.lstrip('@')}",
    }


def _browser_stats(username: str) -> dict[str, Any]:
    """Scrape X profile stats via HTTP (no browser needed).

    X embeds profile data as JSON in the page HTML. We fetch the page,
    extract the __INITIAL_STATE__ JSON, and parse out the key metrics.
    """
    import re

    url = f"https://x.com/{username.lstrip('@')}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        return {
            "method": "browser",
            "platform": "x",
            "account": username,
            "error": f"Failed to fetch profile: {exc}",
        }

    # Extract __INITIAL_STATE__ JSON from HTML
    match = re.search(
        r'id="__INITIAL_STATE__"\s*>\s*({.*?})\s*</script>',
        html,
        re.DOTALL,
    )
    if not match:
        # Fallback: try to extract individual stats via regex
        return _extract_stats_from_html(html, username)

    try:
        import json as _json

        state = _json.loads(match.group(1))
    except Exception:
        return _extract_stats_from_html(html, username)

    # Navigate to user entity in state
    users = state.get("users", {})
    user = users.get(username.lstrip("@"), {})
    if not user:
        # Try finding by screen_name
        for k, v in users.items():
            if v.get("screen_name", "").lower() == username.lstrip("@").lower():
                user = v
                break

    follower_count = user.get("follower_count", 0) or 0
    following_count = user.get("following_count", 0) or 0
    statuses_count = user.get("statuses_count", 0) or 0

    # Extract latest tweets from timeline
    tweets = []
    timeline = (
        state.get("featureSwitchTimeline", {})
        .get("timeline", {})
        .get("instructions", [{}])
    )
    entries = []
    for instr in timeline:
        for entry in instr.get("addEntries", {}).get("entries", []):
            entries.append(entry)

    for entry in entries[:10]:
        tweet_data = entry.get("content", {}).get("tweet", {})
        if not tweet_data:
            # Variant format
            tweet_data = entry.get("content", {})
        tweet_id = tweet_data.get("id_str", "")
        full_text = tweet_data.get("full_text", "") or tweet_data.get("text", "")
        created_at = tweet_data.get("created_at", "")
        retweet_count = tweet_data.get("retweet_count", 0) or 0
        favorite_count = tweet_data.get("favorite_count", 0) or 0
        reply_count = tweet_data.get("reply_count", 0) or 0
        view_count = tweet_data.get("views", {}).get("count", 0) or 0

        if full_text:
            tweets.append({
                "id": tweet_id,
                "text": full_text[:200],
                "created_at": created_at,
                "retweets": retweet_count,
                "likes": favorite_count,
                "replies": reply_count,
                "views": view_count,
                "url": f"https://x.com/{username.lstrip('@')}/status/{tweet_id}",
            })

    return {
        "method": "browser",
        "platform": "x",
        "account": username,
        "url": url,
        "profile": {
            "followers": follower_count,
            "following": following_count,
            "posts": statuses_count,
        },
        "recent_posts": tweets,
    }


def _extract_stats_from_html(html: str, username: str) -> dict[str, Any]:
    """Fallback: extract stats from HTML when JSON state is unavailable."""
    import re

    followers = 0
    following = 0
    posts = 0

    fmatch = re.search(r'"follower_count"\s*:\s*(\d+)', html)
    if fmatch:
        followers = int(fmatch.group(1))

    fimatch = re.search(r'"following_count"\s*:\s*(\d+)', html)
    if fimatch:
        following = int(fimatch.group(1))

    pmatch = re.search(r'"statuses_count"\s*:\s*(\d+)', html)
    if pmatch:
        posts = int(pmatch.group(1))

    # Try alternate HTML patterns
    if not followers:
        m = re.search(r'([\d,]+)\s+Followers', html)
        if m:
            followers = int(m.group(1).replace(",", ""))

    return {
        "method": "browser",
        "platform": "x",
        "account": username,
        "profile": {
            "followers": followers,
            "following": following,
            "posts": posts,
        },
        "recent_posts": [],
        "note": "Limited data extracted from HTML",
    }


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post to X via API")
    parser.add_argument("--account", required=True, help="Account key from credentials")
    parser.add_argument("--text", help="Tweet text (single post)")
    parser.add_argument("--segments", help="JSON array of thread segments")
    parser.add_argument("--image", default=None, help="Image path to attach")
    args = parser.parse_args()

    try:
        if args.segments:
            segs = json.loads(args.segments)
            result = post_thread(segs, args.account, args.image)
        elif args.text:
            result = post(args.text, args.account, args.image)
        else:
            parser.error("Provide --text or --segments")
        print(json.dumps(result, indent=2))
    except ConnectorError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)
