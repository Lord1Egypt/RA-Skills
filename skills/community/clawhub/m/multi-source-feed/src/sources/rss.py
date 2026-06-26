"""Generic RSS/Atom source — one class handles any feed URL."""

from __future__ import annotations

import re
import time
from calendar import timegm
from datetime import datetime, timedelta

import feedparser

from src.models import BaseSource, FeedItem
from src.sources import register

DEFAULT_MAX_AGE_DAYS = 7


@register("rss")
class RSSSource(BaseSource):

    DEFAULT_MAX_ITEMS = 20
    DEFAULT_MAX_CONTENT_CHARS = 300  # Only need summary, not full articles

    def fetch(self) -> list[FeedItem]:
        url = self.config.get("url")
        if not url:
            raise ValueError(f"RSS source {self.name!r} missing 'url' in config")

        max_items = self.config.get("max_items", self.DEFAULT_MAX_ITEMS)
        max_content = self.config.get("max_content_chars", self.DEFAULT_MAX_CONTENT_CHARS)
        max_age_days = self.config.get("max_age_days", DEFAULT_MAX_AGE_DAYS)
        cutoff_ts = time.time() - max_age_days * 86400

        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            raise RuntimeError(
                f"RSS parse failed for {self.name!r}: {feed.bozo_exception}"
            )

        items: list[FeedItem] = []
        skipped_old = 0
        for entry in feed.entries:
            # Prefer 'published_parsed' over 'updated_parsed' for date filtering
            time_struct = entry.get("published_parsed") or entry.get("updated_parsed")
            if time_struct:
                entry_ts = timegm(time_struct)
                if entry_ts < cutoff_ts:
                    skipped_old += 1
                    continue

            # Prefer 'published' over 'updated' for timestamp.
            ts = entry.get("published", entry.get("updated", ""))

            # Prefer summary (short) over full content (can be huge HTML).
            content = ""
            if entry.get("summary"):
                content = entry.summary
            elif entry.get("content"):
                content = entry.content[0].get("value", "")

            # Strip HTML tags and truncate to save tokens.
            content = _strip_html(content)[:max_content]

            # Author
            author = entry.get("author", "")

            # Categories / tags from feed
            feed_tags = [t.get("term", "") for t in entry.get("tags", []) if t.get("term")]

            items.append(
                FeedItem(
                    source=f"rss:{self.name}",
                    title=entry.get("title", ""),
                    url=entry.get("link", ""),
                    author=author,
                    content=content,
                    timestamp=ts,
                    tags=self.config.get("tags", []) + feed_tags,
                    metrics={},
                )
            )

            if len(items) >= max_items:
                break

        if skipped_old:
            print(f"   🕐 {self.name}: skipped {skipped_old} items older than {max_age_days}d")

        return items


def _strip_html(text: str) -> str:
    """Remove HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
