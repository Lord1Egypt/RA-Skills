"""Reddit source — uses public JSON API (no auth needed)."""

from __future__ import annotations

import re

import requests

from src.models import BaseSource, FeedItem
from src.sources import register


@register("reddit")
class RedditSource(BaseSource):

    DEFAULT_MAX_ITEMS = 15
    DEFAULT_MAX_CONTENT_CHARS = 300

    def fetch(self) -> list[FeedItem]:
        subreddit = self.config.get("subreddit")
        if not subreddit:
            raise ValueError(f"Reddit source {self.name!r} missing 'subreddit'")

        sort = self.config.get("sort", "hot")
        max_items = self.config.get("max_items", self.DEFAULT_MAX_ITEMS)
        max_content = self.config.get("max_content_chars", self.DEFAULT_MAX_CONTENT_CHARS)

        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={max_items + 5}"
        resp = requests.get(
            url,
            headers={"User-Agent": "multi-source-feed:v1.0 (memo pipeline)"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        items: list[FeedItem] = []
        for child in data["data"]["children"]:
            post = child["data"]

            # Skip stickied/pinned posts
            if post.get("stickied"):
                continue

            title = post.get("title", "")
            author = post.get("author", "")
            score = post.get("score", 0)
            num_comments = post.get("num_comments", 0)
            created_utc = post.get("created_utc", 0)

            # Content: selftext for text posts, empty for link posts
            content = post.get("selftext", "")
            content = _strip_markdown(content)[:max_content]

            # URL: external link if it's a link post, otherwise reddit permalink
            post_url = post.get("url", "")
            permalink = f"https://www.reddit.com{post.get('permalink', '')}"
            is_self = post.get("is_self", False)
            item_url = permalink if is_self else post_url

            items.append(
                FeedItem(
                    source=f"reddit:{self.name}",
                    title=title,
                    url=item_url,
                    author=author,
                    content=content,
                    timestamp=str(int(created_utc)),
                    tags=self.config.get("tags", []),
                    metrics={"score": score, "num_comments": num_comments},
                    extra={"subreddit": subreddit, "permalink": permalink},
                )
            )

            if len(items) >= max_items:
                break

        return items


def _strip_markdown(text: str) -> str:
    """Rough markdown removal for brevity."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#*_~`>]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
