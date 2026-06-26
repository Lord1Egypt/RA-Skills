"""Hacker News source — fetches front-page stories via Algolia API."""

from __future__ import annotations

import requests

from src.models import BaseSource, FeedItem
from src.sources import register


@register("hn")
class HNSource(BaseSource):

    DEFAULT_HITS = 30
    DEFAULT_MIN_SCORE = 10
    API_URL = "https://hn.algolia.com/api/v1/search"

    def fetch(self) -> list[FeedItem]:
        hits_per_page = self.config.get("hits_per_page", self.DEFAULT_HITS)
        min_score = self.config.get("min_score", self.DEFAULT_MIN_SCORE)

        resp = requests.get(
            self.API_URL,
            params={"tags": "front_page", "hitsPerPage": hits_per_page},
            timeout=15,
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", [])

        items: list[FeedItem] = []
        for h in hits:
            points = h.get("points") or 0
            if points < min_score:
                continue

            items.append(
                FeedItem(
                    source=f"hn:{self.name}",
                    title=h.get("title", ""),
                    url=h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID', '')}",
                    author=h.get("author", ""),
                    content="",  # HN front-page items rarely have body text
                    timestamp=h.get("created_at", ""),
                    tags=self.config.get("tags", []),
                    metrics={
                        "points": points,
                        "num_comments": h.get("num_comments") or 0,
                    },
                    extra={"hn_id": h.get("objectID", "")},
                )
            )

        return items
