"""Domain models used by the recommender."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def _json_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return [str(value).strip()]


@dataclass
class MemberProfile:
    record_id: str
    display_name: str
    team_name: str = ""
    primary_direction: str = ""
    secondary_directions: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    excluded_topics: list[str] = field(default_factory=list)
    feishu_user_id: str = ""
    source: str = "manual"
    confidence: float = 1.0
    version: int = 1
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemberProfile":
        return cls(
            record_id=str(data.get("record_id") or data.get("member_id") or data.get("id") or data.get("name") or "").strip(),
            display_name=str(data.get("display_name") or data.get("name") or data.get("record_id") or data.get("member_id") or "").strip(),
            team_name=str(data.get("team_name") or "").strip(),
            primary_direction=str(data.get("primary_direction") or "").strip(),
            secondary_directions=_json_list(data.get("secondary_directions")),
            keywords=_json_list(data.get("keywords")),
            excluded_topics=_json_list(data.get("excluded_topics")),
            feishu_user_id=str(data.get("feishu_user_id") or "").strip(),
            source=str(data.get("source") or "manual").strip(),
            confidence=float(data.get("confidence") or 1.0),
            version=int(data.get("version") or 1),
            updated_at=str(data.get("updated_at") or datetime.now(timezone.utc).isoformat()),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Paper:
    paper_id: str
    title: str
    abstract: str
    authors: list[str]
    published_at: str
    source: str
    url: str
    tags: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Paper":
        return cls(
            paper_id=str(data["paper_id"]),
            title=str(data.get("title") or "").strip(),
            abstract=str(data.get("abstract") or "").strip(),
            authors=_json_list(data.get("authors")),
            published_at=str(data.get("published_at") or datetime.now(timezone.utc).isoformat()),
            source=str(data.get("source") or "unknown").strip(),
            url=str(data.get("url") or "").strip(),
            tags=_json_list(data.get("tags")),
            raw=dict(data.get("raw") or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Recommendation:
    record_id: str
    paper_id: str
    score: float
    rank: int
    reason: str
    channel: str = "personal_dm"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
