from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SeriesRef:
    provider_series_id: str
    title: str
    season_title: str | None = None
    season_number: int | None = None


@dataclass(slots=True)
class EpisodeProgress:
    provider_episode_id: str
    provider_series_id: str
    episode_number: int | None
    episode_title: str | None
    playback_position_ms: int | None
    duration_ms: int | None
    completion_ratio: float | None
    last_watched_at: str | None
    audio_locale: str | None = None
    subtitle_locale: str | None = None
    rating: str | None = None


@dataclass(slots=True)
class WatchlistEntry:
    provider_series_id: str
    added_at: str | None
    status: str | None = None
    list_id: str | None = None
    list_name: str | None = None
    list_kind: str | None = None


@dataclass(slots=True)
class ProviderSnapshot:
    contract_version: str
    generated_at: str
    provider: str
    account_id_hint: str | None
    series: list[SeriesRef] = field(default_factory=list)
    progress: list[EpisodeProgress] = field(default_factory=list)
    watchlist: list[WatchlistEntry] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)
