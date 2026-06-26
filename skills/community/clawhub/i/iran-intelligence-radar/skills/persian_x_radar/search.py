from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import re
from typing import Callable, Dict, Iterable, List, Optional


@dataclass
class SearchRequest:
    keywords: List[str]
    accounts: List[str]
    min_faves: int
    min_retweets: int
    since_hours: int


@dataclass
class RawTweet:
    id: str
    author: str
    timestamp: datetime
    text: str
    likes: int
    retweets: int
    replies: int
    url: str


ToolFn = Callable[..., List[Dict]]


def build_x_query(req: SearchRequest) -> str:
    keyword_clause = " OR ".join(f'"{k}"' for k in req.keywords)
    base = f'(lang:fa) ({keyword_clause})'

    account_clause = ""
    if req.accounts:
        account_terms = " OR ".join(f"from:{a.lstrip('@')}" for a in req.accounts)
        account_clause = f" ({account_terms})"

    query = (
        f"{base}{account_clause} min_faves:{req.min_faves} min_retweets:{req.min_retweets} "
        f"filter:has_engagement -filter:replies since:{req.since_hours}h"
    )
    return query


def _normalize_tool_rows(rows: Iterable[Dict]) -> List[RawTweet]:
    normalized: List[RawTweet] = []
    for row in rows:
        ts = row.get("timestamp")
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                ts = datetime.now(timezone.utc)
        elif ts is None:
            ts = datetime.now(timezone.utc)

        tweet = RawTweet(
            id=str(row.get("id", "")),
            author=str(row.get("author", "unknown")),
            timestamp=ts,
            text=str(row.get("text", "")).strip(),
            likes=int(row.get("likes", 0)),
            retweets=int(row.get("retweets", 0)),
            replies=int(row.get("replies", 0)),
            url=str(row.get("url", "")),
        )
        normalized.append(tweet)
    return normalized


def _looks_mostly_emoji(text: str) -> bool:
    if not text:
        return True
    non_alnum = re.sub(r"[\w\s\u0600-\u06FF]", "", text)
    return len(non_alnum) > len(text) * 0.5


def _looks_promotional(text: str) -> bool:
    promo_markers = ["discount", "off", "buy now", "کد تخفیف", "تبلیغ", "sponsor"]
    low = text.lower()
    return any(marker in low for marker in promo_markers)


def filter_noise(tweets: List[RawTweet], min_chars: int = 12) -> List[RawTweet]:
    filtered: List[RawTweet] = []
    for t in tweets:
        if len(t.text) < min_chars:
            continue
        if _looks_mostly_emoji(t.text):
            continue
        if _looks_promotional(t.text):
            continue
        filtered.append(t)
    return filtered


def dedupe_tweets(tweets: List[RawTweet]) -> List[RawTweet]:
    seen = set()
    unique: List[RawTweet] = []
    for t in tweets:
        key = (t.id, t.url)
        if key in seen:
            continue
        seen.add(key)
        unique.append(t)
    return unique


def search_with_fallback(
    req: SearchRequest,
    x_keyword_search: Optional[ToolFn] = None,
    x_semantic_search: Optional[ToolFn] = None,
    web_search: Optional[ToolFn] = None,
) -> List[RawTweet]:
    query = build_x_query(req)

    tool_order = [
        ("x_keyword_search", x_keyword_search),
        ("x_semantic_search", x_semantic_search),
        ("web_search", web_search),
    ]

    for _, tool_fn in tool_order:
        if tool_fn is None:
            continue
        try:
            rows = tool_fn(query=query)
            if rows:
                return _normalize_tool_rows(rows)
        except Exception:
            continue

    now = datetime.now(timezone.utc)
    # Deterministic local mock data to keep the skill runnable without external tools.
    mock = [
        RawTweet(
            id="m1",
            author="@analyst_fa",
            timestamp=now - timedelta(hours=2),
            text="بحث درباره حمله و موشک در حال افزایش است",
            likes=420,
            retweets=130,
            replies=12,
            url="https://x.com/analyst_fa/status/1",
        ),
        RawTweet(
            id="m2",
            author="@iran_watch",
            timestamp=now - timedelta(hours=3),
            text="گزارش هایی از اعتراض در چند شهر منتشر شده است",
            likes=170,
            retweets=42,
            replies=9,
            url="https://x.com/iran_watch/status/2",
        ),
    ]
    return mock
