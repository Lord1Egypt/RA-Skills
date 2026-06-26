"""Product Hunt source — GraphQL API, sorted by votes."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import requests

from src.models import BaseSource, FeedItem
from src.sources import register


_GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"

_QUERY = """
query($first: Int!, $postedAfter: DateTime) {
  posts(first: $first, order: VOTES, postedAfter: $postedAfter) {
    edges {
      node {
        name
        tagline
        votesCount
        url
        website
        createdAt
        topics {
          edges {
            node {
              name
            }
          }
        }
        makers {
          name
          username
        }
      }
    }
  }
}
"""


@register("producthunt")
class ProductHuntSource(BaseSource):

    DEFAULT_MAX_ITEMS = 15

    def fetch(self) -> list[FeedItem]:
        token = os.environ.get("PRODUCTHUNT_API_TOKEN", "")
        if not token:
            raise RuntimeError("PRODUCTHUNT_API_TOKEN not set in .env")

        max_items = self.config.get("max_items", self.DEFAULT_MAX_ITEMS)
        lookback_days = self.config.get("posted_after_days", 2)

        variables = {"first": max_items}
        posted_after = (
            datetime.now(timezone.utc) - timedelta(days=lookback_days)
        ).strftime("%Y-%m-%dT00:00:00Z")
        variables["postedAfter"] = posted_after

        resp = requests.post(
            _GRAPHQL_URL,
            json={"query": _QUERY, "variables": variables},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        if "errors" in data:
            raise RuntimeError(f"PH API error: {data['errors']}")

        items: list[FeedItem] = []
        for edge in data["data"]["posts"]["edges"]:
            node = edge["node"]

            # Clean UTM params from URL
            url = node.get("url", "")
            if "?" in url:
                url = url.split("?")[0]

            topics = [
                t["node"]["name"]
                for t in node.get("topics", {}).get("edges", [])
            ]
            makers = node.get("makers") or []
            author = makers[0]["username"] if makers else ""

            items.append(
                FeedItem(
                    source=f"ph:{self.name}",
                    title=node["name"],
                    url=url,
                    author=author,
                    content=node.get("tagline", ""),
                    timestamp=node.get("createdAt", ""),
                    tags=self.config.get("tags", []) + topics,
                    metrics={"votes": node.get("votesCount", 0)},
                )
            )

        return items
