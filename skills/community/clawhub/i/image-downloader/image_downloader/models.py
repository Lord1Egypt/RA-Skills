from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ImageCandidate:
    source: str
    keyword: str
    image_url: str
    page_url: str | None = None
    thumbnail_url: str | None = None
    title: str | None = None
    width: int | None = None
    height: int | None = None
    content_type: str | None = None
    source_rank: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
