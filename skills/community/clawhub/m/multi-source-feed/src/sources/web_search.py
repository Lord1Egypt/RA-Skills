"""Web search source using Tavily API — catches trending topics not in any feed."""

from __future__ import annotations

import os

import requests

from src.models import BaseSource, FeedItem
from src.sources import register


@register("web_search")
class WebSearchSource(BaseSource):

    API_URL = "https://api.tavily.com/search"
    DEFAULT_MAX_RESULTS = 10

    def fetch(self) -> list[FeedItem]:
        api_key = self.config.get("api_key") or os.environ.get("TAVILY_API_KEY", "")
        if not api_key:
            raise ValueError(
                f"Web search source {self.name!r} needs TAVILY_API_KEY "
                "(set in env or source config)"
            )

        query = self.config.get("query", "")
        if not query:
            raise ValueError(f"Web search source {self.name!r} missing 'query' in config")

        max_results = self.config.get("max_results", self.DEFAULT_MAX_RESULTS)
        search_depth = self.config.get("search_depth", "basic")  # "basic" or "advanced"
        topic = self.config.get("topic", "general")  # "general" or "news"

        days = self.config.get("days", 2)  # Only return results from last N days

        payload = {
            "api_key": api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "topic": topic,
            "include_answer": False,
            "days": days,
        }

        resp = requests.post(self.API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        items: list[FeedItem] = []
        for result in data.get("results", []):
            content = result.get("content", "")[:300]  # Truncate like RSS
            items.append(
                FeedItem(
                    source=f"search:{self.name}",
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    author="",
                    content=content,
                    timestamp="",
                    tags=self.config.get("tags", []),
                    metrics={
                        "relevance_score": result.get("score", 0),
                    },
                )
            )

        return items
