from __future__ import annotations
"""Bird X search client for hum feed scraping.

Uses a vendored subset of @steipete/bird v0.8.0 (MIT License) to search X
via Twitter's GraphQL API. Requires AUTH_TOKEN and CT0 from an active X
browser session.

Credentials are loaded in priority order:
  1. HUM_X_AUTH_TOKEN / HUM_X_CT0 environment variables
  2. ~/.hum/credentials/x.json → "auth_token" / "ct0" keys
  3. AUTH_TOKEN / CT0 environment variables (shared with last30days)
"""

import json
import os
import shutil
import signal
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

_BIRD_SEARCH_MJS = Path(__file__).parent / "vendor" / "bird-search" / "bird-search.mjs"
_BIRD_DETAIL_MJS = Path(__file__).parent / "vendor" / "bird-search" / "bird-tweet-detail.mjs"
_BIRD_FOLLOW_MJS = Path(__file__).parent / "vendor" / "bird-search" / "bird-follow.mjs"

_credentials: dict[str, str] = {}


def set_credentials(auth_token: str | None, ct0: str | None) -> None:
    """Inject AUTH_TOKEN/CT0 so Node subprocesses can use them."""
    if auth_token:
        _credentials["AUTH_TOKEN"] = auth_token
    if ct0:
        _credentials["CT0"] = ct0


def _has_credentials() -> bool:
    creds = _subprocess_env()
    return bool(creds.get("AUTH_TOKEN") and creds.get("CT0"))


def _subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(_credentials)
    return env


def is_available() -> bool:
    """Return True if bird-search.mjs exists, Node is in PATH, and credentials are set."""
    if not _BIRD_SEARCH_MJS.exists():
        return False
    if not shutil.which("node"):
        return False
    return _has_credentials()


def _run_detail(tweet_id: str, timeout: int = 20) -> dict[str, Any]:
    """Run bird-tweet-detail.mjs for a single tweet and return parsed JSON."""
    if not _BIRD_DETAIL_MJS.exists() or not shutil.which("node"):
        return {"error": "bird-tweet-detail.mjs not found or node not in PATH"}
    cmd = ["node", str(_BIRD_DETAIL_MJS), tweet_id]
    preexec = os.setsid if hasattr(os, "setsid") else None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=preexec,
            env=_subprocess_env(),
        )
        try:
            stdout, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except (ProcessLookupError, PermissionError, OSError):
                proc.kill()
            proc.wait(timeout=5)
            return {"error": f"timed out after {timeout}s"}
        output = (stdout or "").strip()
        return json.loads(output) if output else {"error": "empty response"}
    except json.JSONDecodeError as e:
        return {"error": f"invalid JSON: {e}"}
    except Exception as e:
        return {"error": str(e)}


def follow_accounts(handles: list[str], timeout: int = 30) -> list[dict]:
    """Follow X accounts by handle via CreateFriendship GraphQL.

    Args:
        handles: List of X handles (with or without @)
        timeout: Seconds before giving up per request

    Returns:
        List of dicts with keys: handle, success, userId (if resolved), error (if failed)
    """
    if not _BIRD_FOLLOW_MJS.exists() or not shutil.which("node"):
        return [{"handle": h, "success": False, "error": "bird-follow.mjs not found or node not in PATH"} for h in handles]

    cmd = ["node", str(_BIRD_FOLLOW_MJS)] + handles
    preexec = os.setsid if hasattr(os, "setsid") else None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=preexec,
            env=_subprocess_env(),
        )
        try:
            stdout, _ = proc.communicate(timeout=timeout * len(handles))
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except (ProcessLookupError, PermissionError, OSError):
                proc.kill()
            proc.wait(timeout=5)
            return [{"handle": h, "success": False, "error": "timed out"} for h in handles]
        output = (stdout or "").strip()
        data = json.loads(output) if output else {}
        return data.get("results", [])
    except json.JSONDecodeError as e:
        return [{"handle": h, "success": False, "error": f"invalid JSON: {e}"} for h in handles]
    except Exception as e:
        return [{"handle": h, "success": False, "error": str(e)} for h in handles]


def fetch_article(tweet_id: str, timeout: int = 20) -> dict | None:
    """Fetch a tweet's full article body via TweetResultByRestId GraphQL.

    Args:
        tweet_id: Tweet ID (the tweet that links to or is the article)
        timeout: Seconds before giving up

    Returns:
        Dict with keys: title, body, summary — or None if not an article / fetch failed.
    """
    result = _run_detail(tweet_id, timeout=timeout)
    if result.get("error") or not result.get("success"):
        return None
    tweet = result.get("tweet") or {}
    return tweet.get("article")  # {title, body, summary} or None


def _run(query: str, count: int, timeout: int) -> dict[str, Any]:
    """Run bird-search.mjs and return parsed JSON response."""
    cmd = ["node", str(_BIRD_SEARCH_MJS), query, "--count", str(count), "--json"]
    preexec = os.setsid if hasattr(os, "setsid") else None

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=preexec,
            env=_subprocess_env(),
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except (ProcessLookupError, PermissionError, OSError):
                proc.kill()
            proc.wait(timeout=5)
            return {"error": f"timed out after {timeout}s", "items": []}

        if proc.returncode != 0:
            return {"error": (stderr or "").strip() or "bird search failed", "items": []}

        output = (stdout or "").strip()
        return json.loads(output) if output else {"items": []}

    except json.JSONDecodeError as e:
        return {"error": f"invalid JSON: {e}", "items": []}
    except Exception as e:
        return {"error": str(e), "items": []}


_THREAD_PATTERNS = (
    "🧵",
    "1/",
    "1.",
    "thread:",
    "a thread",
    "short thread",
    "long thread",
)


def _is_thread_start(text: str) -> bool:
    """Heuristic: return True if this tweet looks like the start of a thread."""
    lower = text.lower().strip()
    # Ends with truncation marker — more content in thread
    if text.rstrip().endswith("…") or text.rstrip().endswith("..."):
        return True
    # Starts or ends with common thread signals
    for pat in _THREAD_PATTERNS:
        if lower.startswith(pat) or lower.endswith(pat):
            return True
    return False


def _normalize(raw_items: list[dict], handle: str = "") -> list[dict]:
    """Convert raw Bird tweet objects to hum feed item format."""
    items = []
    for tweet in raw_items:
        if not isinstance(tweet, dict):
            continue

        # URL
        url = tweet.get("permanent_url") or tweet.get("url", "")
        if not url and tweet.get("id"):
            author = tweet.get("author", {}) or tweet.get("user", {})
            screen_name = author.get("username") or author.get("screen_name", "")
            if screen_name:
                url = f"https://x.com/{screen_name}/status/{tweet['id']}"
        if not url:
            continue

        # Date
        date = None
        created_at = tweet.get("createdAt") or tweet.get("created_at", "")
        if created_at:
            try:
                if len(created_at) > 10 and created_at[10] == "T":
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                else:
                    dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                date = dt.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                pass

        # Author
        author = tweet.get("author", {}) or tweet.get("user", {})
        author_handle = (
            author.get("username") or author.get("screen_name", "") or handle
        ).lstrip("@")

        # Skip replies to other people's tweets
        tweet_id = str(tweet.get("id") or tweet.get("id_str") or "")
        in_reply_to = str(tweet.get("inReplyToStatusId") or tweet.get("in_reply_to_status_id") or "")
        conversation_id = str(tweet.get("conversationId") or tweet.get("conversation_id") or "")
        if in_reply_to and conversation_id and conversation_id != tweet_id:
            continue

        content = str(tweet.get("text") or tweet.get("full_text") or "").strip()

        # Detect article tweets via card name or explicit article URL in content
        card = tweet.get("card") or tweet.get("cardByUrl") or {}
        card_name = str(card.get("name") or card.get("card_name") or "")
        is_article = "article" in card_name.lower() or "x.com/i/articles" in content

        is_thread = _is_thread_start(content)

        if is_thread:
            post_type = "thread"
        elif is_article:
            post_type = "article"
        else:
            post_type = "tweet"

        item = {
            "source": "x",
            "author": f"@{author_handle}",
            "content": content,
            "post_type": post_type,
            "url": url,
            "timestamp": date,
            "likes": _int(tweet.get("likeCount") or tweet.get("like_count") or tweet.get("favorite_count")) or 0,
            "retweets": _int(tweet.get("retweetCount") or tweet.get("retweet_count")) or 0,
            "replies": _int(tweet.get("replyCount") or tweet.get("reply_count")) or 0,
            "views": _int(tweet.get("viewCount") or tweet.get("view_count")) or 0,
            "media": [],
        }
        if tweet_id:
            item["tweet_id"] = tweet_id
        items.append(item)
    return items


def _int(val: Any) -> int | None:
    if val is None:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def fetch_thread(tweet_id: str, handle: str, count: int = 50, timeout: int = 30) -> list[dict]:
    """Fetch all tweets in a thread by querying conversation_id via Bird.

    Args:
        tweet_id: ID of the first tweet in the thread
        handle: Author handle (without @) — used to filter to only their replies
        count: Max tweets to fetch (default 50)
        timeout: Seconds before giving up

    Returns:
        List of normalized hum feed items in chronological order, or empty list on failure.
    """
    handle = handle.lstrip("@")
    query = f"conversation_id:{tweet_id} from:{handle}"
    response = _run(query, count, timeout)

    if isinstance(response, dict) and response.get("error"):
        return []

    raw = response if isinstance(response, list) else response.get("items", response.get("tweets", []))
    tweets = _normalize(raw if isinstance(raw, list) else [], handle=handle)
    # Sort chronologically (oldest first) so we can stitch in order
    tweets.sort(key=lambda t: t.get("timestamp") or "")
    return tweets


def fetch_thread_as_item(tweet_id: str, handle: str, seed_item: dict, timeout: int = 30) -> dict:
    """Fetch a full thread and return a single merged feed item.

    Stitches all thread tweets into one item with combined text and summed stats.
    Falls back to the seed_item unchanged if thread fetch fails.

    Args:
        tweet_id: ID of the first tweet in the thread
        handle: Author handle (without @)
        seed_item: The original feed item for the thread-start tweet
        timeout: Seconds before giving up

    Returns:
        A single merged feed item representing the full thread.
    """
    tweets = fetch_thread(tweet_id, handle, timeout=timeout)
    if not tweets:
        return seed_item

    full_content = "\n\n".join(t["content"] for t in tweets if t.get("content"))

    return {
        **seed_item,
        "content": full_content,
        "post_type": "thread",
        "tweet_count": len(tweets),
        "likes": sum(t.get("likes") or 0 for t in tweets),
        "retweets": sum(t.get("retweets") or 0 for t in tweets),
        "replies": sum(t.get("replies") or 0 for t in tweets),
        "views": sum(t.get("views") or 0 for t in tweets),
    }


def fetch_profile(handle: str, since: str | None = None, count: int = 20, timeout: int = 30) -> list[dict]:
    """Fetch recent posts from an X profile via Bird.

    Args:
        handle: X handle (without @)
        since: ISO 8601 date string (YYYY-MM-DD) — only fetch tweets after this date
        count: Max number of tweets to fetch
        timeout: Seconds before giving up

    Returns:
        List of normalized hum feed items, or empty list on failure.
    """
    handle = handle.lstrip("@")
    query = f"from:{handle}"
    if since:
        date = since[:10]  # trim to YYYY-MM-DD
        query += f" since:{date}"

    response = _run(query, count, timeout)

    if isinstance(response, dict) and response.get("error"):
        return []

    raw = response if isinstance(response, list) else response.get("items", response.get("tweets", []))
    return _normalize(raw if isinstance(raw, list) else [], handle=handle)


def fetch_home_feed(since: str | None = None, count: int = 100, timeout: int = 90) -> list[dict]:
    """Fetch tweets from followed accounts via Bird (X search with filter:follows).

    Uses the X search operator 'filter:follows' to restrict results to accounts
    the authenticated session follows — effectively the home timeline without
    any browser automation.

    Args:
        since: ISO 8601 date string (YYYY-MM-DD) — only fetch tweets after this date
        count: Max number of tweets to fetch (default 40, ~5 scrolls worth)
        timeout: Seconds before giving up

    Returns:
        List of normalized hum feed items, or empty list on failure/no credentials.
    """
    query = "filter:follows"
    if since:
        query += f" since:{since[:10]}"

    response = _run(query, count, timeout)

    if isinstance(response, dict) and response.get("error"):
        return []

    raw = response if isinstance(response, list) else response.get("items", response.get("tweets", []))
    return _normalize(raw if isinstance(raw, list) else [], handle="")
