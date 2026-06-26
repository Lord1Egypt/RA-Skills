from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RepoSpec:
    owner: str
    repo: str

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.repo}"

    @property
    def state_key(self) -> str:
        return f"{self.owner}__{self.repo}"

    @property
    def api_url(self) -> str:
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/releases"


@dataclass
class ReleaseItem:
    tag_name: str
    name: str | None
    published_at: str | None
    html_url: str
    body: str
    draft: bool
    prerelease: bool
    release_id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StateData:
    repo: str
    processed_tags: list[str] = field(default_factory=list)
    latest_processed_release_id: int | None = None
    latest_processed_published_at: str | None = None
    last_checked_at: str | None = None
    last_success_at: str | None = None
    initialized_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReleaseSummary:
    markdown: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
