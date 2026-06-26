"""Unified data models and source interface for Multi-Source Feed."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


@dataclass
class FeedItem:
    """One piece of content from any source."""

    source: str  # e.g. "x_feed", "hn", "rss:openai-blog", "github_trending"
    title: str
    url: str
    author: str = ""
    content: str = ""  # body / description
    timestamp: str = ""  # ISO 8601
    tags: list[str] = field(default_factory=list)

    # Source-specific metrics stored as a flat dict.
    # Examples: {"views": 12000, "likes": 300}  (X)
    #           {"points": 450, "num_comments": 120}  (HN)
    #           {"stars_today": 800, "total_stars": 5000}  (GitHub)
    metrics: dict[str, Any] = field(default_factory=dict)

    # Extra fields that don't fit the common schema.
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


class BaseSource(abc.ABC):
    """Abstract interface every source must implement."""

    def __init__(self, name: str, config: dict | None = None):
        self.name = name
        self.config = config or {}

    @abc.abstractmethod
    def fetch(self) -> list[FeedItem]:
        """Fetch items from the source. Must return a list of FeedItem."""
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
