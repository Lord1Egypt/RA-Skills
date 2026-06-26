"""Shared data models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any


CN_TZ = timezone(timedelta(hours=8))


def now_shanghai_iso() -> str:
    return datetime.now(CN_TZ).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class TrendItem:
    platform: str
    region: str
    title_original: str
    summary_zh: str
    raw_url: str
    source_type: str
    source_engine: str
    trust_level: str
    content_type: str
    published_at: str
    fetched_at: str
    rank: int | None = None
    keyword: str | None = None
    title_zh: str | None = None
    meta_json: str | None = None

    def dedup_key(self) -> str:
        return f"{self.platform}:{self.region}:{self.raw_url}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class QueryRequest:
    user_id: str
    region: str
    platforms: list[str]
    keyword: str
    time_range: str = "7d"
    limit: int = 10
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QueryResult:
    items: list[TrendItem]
    errors: dict[str, str]
    async_refetch_started: bool = False

    @property
    def status(self) -> str:
        if self.items and self.errors:
            return "partial"
        if self.errors and not self.items:
            return "failed"
        return "success"
