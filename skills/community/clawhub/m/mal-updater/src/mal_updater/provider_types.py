from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .config import AppConfig
from .contracts import ProviderSnapshot


@dataclass(slots=True)
class ProviderCapabilities:
    history: bool = False
    continue_watching: bool = False
    watchlists: bool = False
    favourites: bool = False
    rich_progress: bool = False
    incremental_boundaries: bool = False
    token_refresh: bool = False


@dataclass(slots=True)
class ProviderFetchResult:
    snapshot: ProviderSnapshot
    metadata: dict[str, Any] = field(default_factory=dict)


class ProviderModule(Protocol):
    slug: str
    display_name: str
    capabilities: ProviderCapabilities

    def fetch_snapshot(
        self,
        config: AppConfig,
        *,
        profile: str = "default",
        full_refresh: bool = False,
    ) -> ProviderFetchResult:
        ...

    def write_snapshot_file(self, path: Path, snapshot: ProviderSnapshot) -> Path:
        ...
