"""X/Twitter source — runs scrape_feed.py then reads its output.

The scraper uses Playwright with a real browser (headless=False, proven reliable,
do NOT change to headless). This adapter triggers it automatically during fetch.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.models import BaseSource, FeedItem
from src.sources import register


@register("x_feed")
class XFeedSource(BaseSource):

    def _run_scraper(self, raw_path: Path) -> bool:
        """Run scrape_feed.py to refresh feed_raw.json. Returns True on success."""
        scraper = Path(__file__).resolve().parents[2] / "scrape_feed.py"
        if not scraper.exists():
            print(f"   ⚠️ Scraper not found: {scraper}")
            return False

        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            print(f"   🕷️ Running X scraper (attempt {attempt}/{max_attempts})...")
            try:
                result = subprocess.run(
                    [sys.executable, str(scraper)],
                    cwd=str(scraper.parent),
                    capture_output=True,
                    text=True,
                    timeout=660,
                )
                if result.returncode == 0:
                    print("   ✅ X scraper finished")
                    return True
                print(f"   ⚠️ Scraper exited with code {result.returncode}")
                if result.stderr:
                    print(f"   stderr: {result.stderr[:300]}")
            except subprocess.TimeoutExpired:
                print(f"   ⚠️ Scraper timed out (attempt {attempt})")
            except Exception as e:
                print(f"   ⚠️ Scraper error (attempt {attempt}): {e}")

        print("   ❌ X scraper failed after all attempts")
        return False

    def fetch(self) -> list[FeedItem]:
        raw_path = Path(self.config.get("raw_json_path", "feed_raw.json"))

        # Always re-scrape to get fresh data; return empty on failure (critical source)
        if not self._run_scraper(raw_path):
            return []
        if not raw_path.exists():
            print(f"   ⚠️ X feed file not found: {raw_path}")
            return []

        with open(raw_path, encoding="utf-8") as f:
            data = json.load(f)

        items: list[FeedItem] = []

        # Convert posts
        for post in data.get("posts", []):
            text = post.get("text", "")
            if not text:
                continue

            items.append(
                FeedItem(
                    source=f"x:{self.name}",
                    title=text[:120],
                    url=post.get("url", ""),
                    author=post.get("author_handle", ""),
                    content=text,
                    timestamp=post.get("timestamp", ""),
                    tags=self.config.get("tags", []),
                    metrics={
                        "views": post.get("views", 0),
                        "likes": post.get("likes", 0),
                        "reposts": post.get("reposts", 0),
                        "replies": post.get("replies", 0),
                        "bookmarks": post.get("bookmarks", 0),
                    },
                    extra={
                        "author_name": post.get("author_name", ""),
                        "is_retweet": post.get("is_retweet", False),
                        "retweeted_by": post.get("retweeted_by", ""),
                        "has_media": post.get("has_media", False),
                        "external_links": post.get("external_links", []),
                        "quoted_tweet": post.get("quoted_tweet", ""),
                        "tab_source": post.get("source", ""),
                    },
                )
            )

        # Convert trending topics
        for t in data.get("trending", []):
            topic = t.get("topic", "")
            if not topic:
                continue
            items.append(
                FeedItem(
                    source=f"x:{self.name}:trending",
                    title=topic,
                    url="",
                    author="",
                    content="",
                    timestamp=data.get("scraped_at", ""),
                    tags=["trending"] + self.config.get("tags", []),
                    metrics={},
                    extra={
                        "category": t.get("category", ""),
                        "post_count": t.get("post_count", ""),
                    },
                )
            )

        return items
