"""Anthropic News source — scrapes anthropic.com/news (no public RSS available)."""

from __future__ import annotations

import re as _re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from src.models import BaseSource, FeedItem
from src.sources import register

BASE_URL = "https://www.anthropic.com"
NEWS_URL = f"{BASE_URL}/news"

# Only surface product/announcement news; skip pure research papers and policy
ALLOWED_SUBJECTS = {"product", "announcements", "announcement"}

_KNOWN_SUBJECTS = {
    "product", "announcements", "announcement", "research",
    "policy", "safety", "interpretability", "news",
}

_DATE_PATTERN = _re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}\b",
    _re.IGNORECASE,
)

DEFAULT_MAX_AGE_DAYS = 7

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


@register("anthropic_news")
class AnthropicNewsSource(BaseSource):

    def fetch(self) -> list[FeedItem]:
        max_items = self.config.get("max_items", 10)
        max_age_days = self.config.get("max_age_days", DEFAULT_MAX_AGE_DAYS)
        tags = self.config.get("tags", [])
        cutoff = datetime.now() - timedelta(days=max_age_days)

        try:
            resp = requests.get(NEWS_URL, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"   ⚠️ AnthropicNews fetch failed: {e}")
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        items: list[FeedItem] = []
        skipped_old = 0

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if not href.startswith("/news/"):
                continue

            texts = [t.strip() for t in a_tag.stripped_strings]
            subject = _find_subject(texts)

            if subject and subject.lower() not in ALLOWED_SUBJECTS:
                continue

            title = _find_title(texts)
            if not title:
                continue

            date_str = _find_date(texts)

            # Skip items older than max_age_days
            if date_str and _is_too_old(date_str, cutoff):
                skipped_old += 1
                continue

            items.append(
                FeedItem(
                    source=f"rss:{self.name}",
                    title=title,
                    url=f"{BASE_URL}{href}",
                    author="Anthropic",
                    content="",
                    timestamp=date_str,
                    tags=tags,
                    metrics={},
                )
            )

            if len(items) >= max_items:
                break

        if skipped_old:
            print(f"   🕐 AnthropicNews: skipped {skipped_old} items older than {max_age_days}d")

        return items


def _find_subject(texts: list[str]) -> str:
    for t in texts:
        if t.lower() in _KNOWN_SUBJECTS:
            return t
    return ""


def _find_date(texts: list[str]) -> str:
    for t in texts:
        if _DATE_PATTERN.search(t):
            return t
    return ""


def _find_title(texts: list[str]) -> str:
    candidates = [t for t in texts if len(t) > 15 and t.lower() not in _KNOWN_SUBJECTS]
    return max(candidates, key=len) if candidates else ""


def _is_too_old(date_str: str, cutoff: datetime) -> bool:
    """Return True if the date string is before cutoff."""
    try:
        dt = datetime.strptime(date_str, "%b %d, %Y")
        return dt < cutoff
    except ValueError:
        return False  # Can't parse → keep it
