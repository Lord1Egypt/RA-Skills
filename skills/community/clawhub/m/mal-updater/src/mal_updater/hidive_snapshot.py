from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import AppConfig
from .contracts import EpisodeProgress, ProviderSnapshot, SeriesRef, WatchlistEntry
from .hidive_auth import HidiveAuthError, HidiveSession, HidiveStatePaths, start_hidive_session


class HidiveSnapshotError(RuntimeError):
    pass


SYNC_BOUNDARY_SCHEMA_VERSION = 1
HISTORY_BOUNDARY_MARKER_LIMIT = 25
CONTINUE_BOUNDARY_MARKER_LIMIT = 25
FAVOURITE_BOUNDARY_MARKER_LIMIT = 25


@dataclass(slots=True)
class _SyncBoundary:
    generated_at: str | None
    account_id_hint: str | None
    history_markers: list[str]
    continue_markers: list[str]
    favourite_markers: list[str]


@dataclass(slots=True)
class HidiveFetchResult:
    snapshot: ProviderSnapshot
    history_count: int
    continue_count: int
    favourite_count: int


def _now_string() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _iso_from_epoch_ms(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _safe_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def _history_item_fingerprint(item: dict[str, Any]) -> str | None:
    episode_information = item.get("episodeInformation") or {}
    series_information = episode_information.get("seriesInformation") or {}
    provider_series_id = series_information.get("id")
    provider_episode_id = item.get("id") or item.get("externalAssetId")
    watched_at = item.get("watchedAt")
    if provider_series_id is None or provider_episode_id is None:
        return None
    return "|".join([str(provider_series_id), str(provider_episode_id), str(watched_at or "")])


def _continue_item_fingerprint(item: dict[str, Any]) -> str | None:
    episode_information = item.get("episodeInformation") or {}
    series_information = episode_information.get("seriesInformation") or {}
    provider_series_id = series_information.get("id")
    provider_episode_id = item.get("id") or item.get("externalAssetId")
    watched_at = item.get("watchedAt")
    watch_progress = item.get("watchProgress")
    if provider_series_id is None or provider_episode_id is None:
        return None
    return "|".join([str(provider_series_id), str(provider_episode_id), str(watched_at or ""), str(watch_progress or "")])


def _favourite_item_fingerprint(item: dict[str, Any]) -> str | None:
    provider_series_id = item.get("id")
    title = item.get("title")
    if provider_series_id is None or title is None:
        return None
    return "|".join([str(provider_series_id), str(title)])


def _load_sync_boundary(state_paths: HidiveStatePaths) -> _SyncBoundary | None:
    path = state_paths.sync_boundary_path
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    if int(payload.get("schema_version") or 0) != SYNC_BOUNDARY_SCHEMA_VERSION:
        return None
    history = payload.get("history") if isinstance(payload.get("history"), dict) else {}
    continue_watching = payload.get("continue_watching") if isinstance(payload.get("continue_watching"), dict) else {}
    favourites = payload.get("favourites") if isinstance(payload.get("favourites"), dict) else {}
    return _SyncBoundary(
        generated_at=str(payload.get("generated_at")) if payload.get("generated_at") else None,
        account_id_hint=str(payload.get("account_id_hint")) if payload.get("account_id_hint") else None,
        history_markers=[str(item) for item in history.get("first_seen", []) if item],
        continue_markers=[str(item) for item in continue_watching.get("first_seen", []) if item],
        favourite_markers=[str(item) for item in favourites.get("first_seen", []) if item],
    )


def _write_sync_boundary(
    *,
    state_paths: HidiveStatePaths,
    generated_at: str,
    account_id_hint: str | None,
    history_items: list[dict[str, Any]],
    continue_items: list[dict[str, Any]],
    favourite_items: list[dict[str, Any]],
) -> None:
    state_paths.root.mkdir(parents=True, exist_ok=True)
    history_markers = []
    for item in history_items:
        fp = _history_item_fingerprint(item)
        if fp and fp not in history_markers:
            history_markers.append(fp)
        if len(history_markers) >= HISTORY_BOUNDARY_MARKER_LIMIT:
            break
    continue_markers = []
    for item in continue_items:
        fp = _continue_item_fingerprint(item)
        if fp and fp not in continue_markers:
            continue_markers.append(fp)
        if len(continue_markers) >= CONTINUE_BOUNDARY_MARKER_LIMIT:
            break
    favourite_markers = []
    for item in favourite_items:
        fp = _favourite_item_fingerprint(item)
        if fp and fp not in favourite_markers:
            favourite_markers.append(fp)
        if len(favourite_markers) >= FAVOURITE_BOUNDARY_MARKER_LIMIT:
            break
    payload = {
        "schema_version": SYNC_BOUNDARY_SCHEMA_VERSION,
        "generated_at": generated_at,
        "account_id_hint": account_id_hint,
        "history": {"marker_limit": HISTORY_BOUNDARY_MARKER_LIMIT, "retained_count": len(history_markers), "first_seen": history_markers},
        "continue_watching": {"marker_limit": CONTINUE_BOUNDARY_MARKER_LIMIT, "retained_count": len(continue_markers), "first_seen": continue_markers},
        "favourites": {"marker_limit": FAVOURITE_BOUNDARY_MARKER_LIMIT, "retained_count": len(favourite_markers), "first_seen": favourite_markers},
    }
    state_paths.sync_boundary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    state_paths.sync_boundary_path.chmod(0o600)


def _normalize_hidive_watch_progress(raw_progress: Any, duration_seconds: int | None) -> tuple[int | None, float | None]:
    numeric = _safe_float(raw_progress)
    if numeric is None:
        return None, None
    if 0.0 <= numeric <= 1.0:
        playback_ratio = numeric
        playback_seconds = int((duration_seconds or 0) * playback_ratio) if duration_seconds is not None else None
        return playback_seconds, playback_ratio
    if duration_seconds is not None and duration_seconds > 0:
        playback_seconds = int(max(0.0, numeric))
        playback_ratio = min(1.0, max(0.0, playback_seconds / duration_seconds))
        return playback_seconds, playback_ratio
    return int(max(0.0, numeric)), None


def _extract_series_ref_from_episode_info(item: dict[str, Any]) -> SeriesRef | None:
    episode_information = item.get("episodeInformation") or {}
    series_information = episode_information.get("seriesInformation") or {}
    provider_series_id = series_information.get("id")
    title = series_information.get("title")
    if provider_series_id is None or not title:
        return None
    return SeriesRef(
        provider_series_id=str(provider_series_id),
        title=str(title),
        season_title=(str(episode_information.get("seasonTitle")) if episode_information.get("seasonTitle") is not None else None),
        season_number=_safe_int(episode_information.get("seasonNumber")),
    )


def _history_item_to_progress(item: dict[str, Any]) -> EpisodeProgress | None:
    episode_information = item.get("episodeInformation") or {}
    series_information = episode_information.get("seriesInformation") or {}
    provider_episode_id = item.get("id") or item.get("externalAssetId")
    provider_series_id = series_information.get("id")
    if provider_episode_id is None or provider_series_id is None:
        return None
    duration_seconds = _safe_int(item.get("duration"))
    duration_ms = duration_seconds * 1000 if duration_seconds is not None else None
    return EpisodeProgress(
        provider_episode_id=str(provider_episode_id),
        provider_series_id=str(provider_series_id),
        episode_number=_safe_int(episode_information.get("episodeNumber")),
        episode_title=str(item.get("title")) if item.get("title") is not None else None,
        playback_position_ms=duration_ms,
        duration_ms=duration_ms,
        completion_ratio=1.0 if duration_ms else None,
        last_watched_at=_iso_from_epoch_ms(item.get("watchedAt")),
        audio_locale=None,
        subtitle_locale=None,
        rating=str(item.get("rating")) if item.get("rating") is not None else None,
    )


def _continue_item_to_progress(item: dict[str, Any]) -> EpisodeProgress | None:
    episode_information = item.get("episodeInformation") or {}
    series_ref = _extract_series_ref_from_episode_info(item)
    if series_ref is None:
        return None
    provider_episode_id = item.get("id") or item.get("externalAssetId")
    if provider_episode_id is None:
        return None
    duration_seconds = _safe_int(item.get("duration"))
    duration_ms = duration_seconds * 1000 if duration_seconds is not None else None
    playback_seconds, watch_progress = _normalize_hidive_watch_progress(item.get("watchProgress"), duration_seconds)
    playback_position_ms = playback_seconds * 1000 if playback_seconds is not None else None
    return EpisodeProgress(
        provider_episode_id=str(provider_episode_id),
        provider_series_id=series_ref.provider_series_id,
        episode_number=_safe_int(episode_information.get("episodeNumber")),
        episode_title=str(item.get("title")) if item.get("title") is not None else None,
        playback_position_ms=playback_position_ms,
        duration_ms=duration_ms,
        completion_ratio=watch_progress,
        last_watched_at=_iso_from_epoch_ms(item.get("watchedAt")),
        audio_locale=None,
        subtitle_locale=None,
        rating=str(item.get("rating")) if item.get("rating") is not None else None,
    )


def _fetch_history_items(session: HidiveSession, *, history_markers: set[str] | None = None) -> tuple[list[dict[str, Any]], int, bool]:
    page = 1
    size = 100
    items: list[dict[str, Any]] = []
    pages_fetched = 0
    stopped_early = False
    while True:
        payload = session.json_get("/customer/history/vod", params={"size": size, "page": page})
        pages_fetched += 1
        if not isinstance(payload, dict):
            raise HidiveSnapshotError("HIDIVE history payload was not a JSON object")
        vods = payload.get("vods")
        if not isinstance(vods, list):
            raise HidiveSnapshotError("HIDIVE history payload did not include a vods list")
        batch = [item for item in vods if isinstance(item, dict)]
        items.extend(batch)
        if history_markers and any((_history_item_fingerprint(item) in history_markers) for item in batch):
            stopped_early = True
            break
        total_pages = _safe_int(payload.get("totalPages")) or 1
        if page >= total_pages or not vods:
            break
        page += 1
    return items, pages_fetched, stopped_early


def _fetch_continue_items(session: HidiveSession, *, continue_markers: set[str] | None = None) -> tuple[list[dict[str, Any]], bool]:
    payload = session.json_get("/content/home", params={"size": 100, "page": 1})
    if not isinstance(payload, dict):
        raise HidiveSnapshotError("HIDIVE home payload was not a JSON object")
    buckets = payload.get("buckets")
    if not isinstance(buckets, list):
        raise HidiveSnapshotError("HIDIVE home payload did not include a buckets list")
    for bucket in buckets:
        if not isinstance(bucket, dict):
            continue
        if str(bucket.get("name") or "").strip().upper() != "CONTINUE WATCHING":
            continue
        content_list = bucket.get("contentList")
        if isinstance(content_list, list):
            items = [item for item in content_list if isinstance(item, dict)]
            stopped_early = bool(continue_markers and any((_continue_item_fingerprint(item) in continue_markers) for item in items))
            return items, stopped_early
        return [], False
    return [], False


def _fetch_favourite_items(session: HidiveSession, *, favourite_markers: set[str] | None = None) -> tuple[list[dict[str, Any]], int, bool]:
    page = 1
    size = 100
    items: list[dict[str, Any]] = []
    pages_fetched = 0
    stopped_early = False
    while True:
        payload = session.json_get("/favourite/vods", params={"size": size, "page": page})
        pages_fetched += 1
        if not isinstance(payload, dict):
            raise HidiveSnapshotError("HIDIVE favourites payload was not a JSON object")
        # HIDIVE currently returns favourites under `events`
        events = payload.get("events") or payload.get("vods") or []
        if not isinstance(events, list):
            raise HidiveSnapshotError("HIDIVE favourites payload did not include an events/vods list")
        batch = [item for item in events if isinstance(item, dict)]
        items.extend(batch)
        if favourite_markers and any((_favourite_item_fingerprint(item) in favourite_markers) for item in batch):
            stopped_early = True
            break
        total_pages = _safe_int(payload.get("totalPages")) or 1
        if page >= total_pages or not events:
            break
        page += 1
    return items, pages_fetched, stopped_early


def _favourite_item_to_series(item: dict[str, Any]) -> SeriesRef | None:
    provider_series_id = item.get('id')
    title = item.get('title')
    if provider_series_id is None or not title:
        return None
    return SeriesRef(
        provider_series_id=str(provider_series_id),
        title=str(title),
        season_title=None,
        season_number=None,
    )


def _favourite_item_to_watchlist(item: dict[str, Any]) -> WatchlistEntry | None:
    provider_series_id = item.get('id')
    if provider_series_id is None:
        return None
    return WatchlistEntry(
        provider_series_id=str(provider_series_id),
        added_at=_iso_from_epoch_ms(item.get('watchedAt') or item.get('publishedDate')),
        status='favorite',
        list_id='favorites',
        list_name='Favorites',
        list_kind='system',
    )


def _dedupe_series(entries: list[SeriesRef]) -> list[SeriesRef]:
    by_id: dict[str, SeriesRef] = {}
    for entry in entries:
        by_id.setdefault(entry.provider_series_id, entry)
    return list(by_id.values())


def _dedupe_progress(entries: list[EpisodeProgress]) -> list[EpisodeProgress]:
    by_id: dict[str, EpisodeProgress] = {}
    for entry in entries:
        previous = by_id.get(entry.provider_episode_id)
        if previous is None:
            by_id[entry.provider_episode_id] = entry
            continue
        if (entry.last_watched_at or "") >= (previous.last_watched_at or ""):
            by_id[entry.provider_episode_id] = entry
    return list(by_id.values())


def fetch_snapshot(
    config: AppConfig,
    *,
    profile: str = "default",
    timeout_seconds: float | None = None,
    use_incremental_boundary: bool = True,
) -> HidiveFetchResult:
    try:
        session = start_hidive_session(config, profile=profile, timeout_seconds=timeout_seconds)
        boundary = _load_sync_boundary(session.state_paths) if use_incremental_boundary else None
        if boundary and boundary.account_id_hint and session.token.account_id and boundary.account_id_hint != session.token.account_id:
            boundary = None
        history_items, history_pages_fetched, history_stopped_early = _fetch_history_items(
            session,
            history_markers=set(boundary.history_markers) if boundary else None,
        )
        continue_items, continue_stopped_early = _fetch_continue_items(
            session,
            continue_markers=set(boundary.continue_markers) if boundary else None,
        )
        favourite_items, favourite_pages_fetched, favourite_stopped_early = _fetch_favourite_items(
            session,
            favourite_markers=set(boundary.favourite_markers) if boundary else None,
        )
    except HidiveAuthError as exc:
        raise
    except Exception as exc:
        raise HidiveSnapshotError(str(exc)) from exc

    history_series = [series for item in history_items if (series := _extract_series_ref_from_episode_info(item)) is not None]
    continue_series = [series for item in continue_items if (series := _extract_series_ref_from_episode_info(item)) is not None]
    favourite_series = [series for item in favourite_items if (series := _favourite_item_to_series(item)) is not None]
    history_progress = [progress for item in history_items if (progress := _history_item_to_progress(item)) is not None]
    continue_progress = [progress for item in continue_items if (progress := _continue_item_to_progress(item)) is not None]
    watchlist_entries = [entry for item in favourite_items if (entry := _favourite_item_to_watchlist(item)) is not None]

    generated_at = _now_string()
    snapshot = ProviderSnapshot(
        contract_version=config.contract_version,
        generated_at=generated_at,
        provider="hidive",
        account_id_hint=session.token.account_id,
        series=_dedupe_series([*history_series, *continue_series, *favourite_series]),
        progress=_dedupe_progress([*history_progress, *continue_progress]),
        watchlist=watchlist_entries,
        raw={
            "history_count": len(history_items),
            "history_pages_fetched": history_pages_fetched,
            "history_stopped_early": history_stopped_early,
            "continue_count": len(continue_items),
            "continue_stopped_early": continue_stopped_early,
            "favourite_count": len(favourite_items),
            "favourite_pages_fetched": favourite_pages_fetched,
            "favourite_stopped_early": favourite_stopped_early,
            "sync_boundary_present": boundary is not None,
            "sync_boundary_mode": "incremental" if use_incremental_boundary else "full_refresh",
            "sync_boundary_schema_version": SYNC_BOUNDARY_SCHEMA_VERSION,
            "sync_boundary_path": str(session.state_paths.sync_boundary_path),
            "supports": {
                "history": True,
                "continue_watching": True,
                "watchlists": True,
            },
        },
    )
    _write_sync_boundary(
        state_paths=session.state_paths,
        generated_at=generated_at,
        account_id_hint=session.token.account_id,
        history_items=history_items,
        continue_items=continue_items,
        favourite_items=favourite_items,
    )
    return HidiveFetchResult(
        snapshot=snapshot,
        history_count=len(history_items),
        continue_count=len(continue_items),
        favourite_count=len(favourite_items),
    )


def snapshot_to_dict(snapshot: ProviderSnapshot) -> dict[str, Any]:
    return {
        "contract_version": snapshot.contract_version,
        "generated_at": snapshot.generated_at,
        "provider": snapshot.provider,
        "account_id_hint": snapshot.account_id_hint,
        "series": [asdict(item) for item in snapshot.series],
        "progress": [asdict(item) for item in snapshot.progress],
        "watchlist": [asdict(item) for item in snapshot.watchlist],
        "raw": snapshot.raw,
    }


def write_snapshot_file(path: Path, snapshot: ProviderSnapshot) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot_to_dict(snapshot), indent=2) + "\n", encoding="utf-8")
    return path
