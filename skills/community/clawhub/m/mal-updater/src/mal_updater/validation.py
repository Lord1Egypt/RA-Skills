from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import EpisodeProgress, ProviderSnapshot, SeriesRef, WatchlistEntry


class SnapshotValidationError(ValueError):
    pass


ISO_SUFFIX = "Z"


def _is_iso_datetime(value: str) -> bool:
    if not isinstance(value, str) or "T" not in value:
        return False
    return value.endswith(ISO_SUFFIX) or "+" in value[10:]


def _expect_type(value: Any, expected: type | tuple[type, ...], field: str) -> None:
    if not isinstance(value, expected):
        if isinstance(expected, tuple):
            names = ", ".join(t.__name__ for t in expected)
        else:
            names = expected.__name__
        raise SnapshotValidationError(f"{field} must be {names}")


def _expect_optional_type(value: Any, expected: type | tuple[type, ...], field: str) -> None:
    if value is not None:
        _expect_type(value, expected, field)


def _expect_non_negative_int(value: Any, field: str) -> None:
    _expect_optional_type(value, int, field)
    if isinstance(value, int) and value < 0:
        raise SnapshotValidationError(f"{field} must be >= 0")


def _expect_ratio(value: Any, field: str) -> None:
    if value is None:
        return
    _expect_type(value, (int, float), field)
    numeric = float(value)
    if numeric < 0 or numeric > 1:
        raise SnapshotValidationError(f"{field} must be between 0 and 1")


def _validate_series_item(item: Any, index: int) -> SeriesRef:
    field = f"series[{index}]"
    _expect_type(item, dict, field)
    provider_series_id = item.get("provider_series_id")
    title = item.get("title")
    season_title = item.get("season_title")
    season_number = item.get("season_number")

    _expect_type(provider_series_id, str, f"{field}.provider_series_id")
    _expect_type(title, str, f"{field}.title")
    _expect_optional_type(season_title, str, f"{field}.season_title")
    _expect_optional_type(season_number, int, f"{field}.season_number")

    allowed = {"provider_series_id", "title", "season_title", "season_number"}
    extras = sorted(set(item) - allowed)
    if extras:
        raise SnapshotValidationError(f"{field} contains unexpected keys: {', '.join(extras)}")

    return SeriesRef(
        provider_series_id=provider_series_id,
        title=title,
        season_title=season_title,
        season_number=season_number,
    )


def _validate_progress_item(item: Any, index: int) -> EpisodeProgress:
    field = f"progress[{index}]"
    _expect_type(item, dict, field)

    required = {
        "provider_episode_id",
        "provider_series_id",
        "episode_number",
        "episode_title",
        "playback_position_ms",
        "duration_ms",
        "completion_ratio",
        "last_watched_at",
        "audio_locale",
        "subtitle_locale",
        "rating",
    }
    missing = sorted(required - set(item))
    if missing:
        raise SnapshotValidationError(f"{field} is missing keys: {', '.join(missing)}")
    extras = sorted(set(item) - required)
    if extras:
        raise SnapshotValidationError(f"{field} contains unexpected keys: {', '.join(extras)}")

    _expect_type(item["provider_episode_id"], str, f"{field}.provider_episode_id")
    _expect_type(item["provider_series_id"], str, f"{field}.provider_series_id")
    _expect_optional_type(item["episode_number"], int, f"{field}.episode_number")
    _expect_optional_type(item["episode_title"], str, f"{field}.episode_title")
    _expect_non_negative_int(item["playback_position_ms"], f"{field}.playback_position_ms")
    _expect_non_negative_int(item["duration_ms"], f"{field}.duration_ms")
    _expect_ratio(item["completion_ratio"], f"{field}.completion_ratio")
    _expect_optional_type(item["audio_locale"], str, f"{field}.audio_locale")
    _expect_optional_type(item["subtitle_locale"], str, f"{field}.subtitle_locale")
    _expect_optional_type(item["rating"], str, f"{field}.rating")
    last_watched_at = item["last_watched_at"]
    if last_watched_at is not None and not _is_iso_datetime(last_watched_at):
        raise SnapshotValidationError(f"{field}.last_watched_at must be an ISO-8601 datetime string")

    return EpisodeProgress(
        provider_episode_id=item["provider_episode_id"],
        provider_series_id=item["provider_series_id"],
        episode_number=item["episode_number"],
        episode_title=item["episode_title"],
        playback_position_ms=item["playback_position_ms"],
        duration_ms=item["duration_ms"],
        completion_ratio=float(item["completion_ratio"]) if item["completion_ratio"] is not None else None,
        last_watched_at=last_watched_at,
        audio_locale=item["audio_locale"],
        subtitle_locale=item["subtitle_locale"],
        rating=item["rating"],
    )


def _validate_watchlist_item(item: Any, index: int) -> WatchlistEntry:
    field = f"watchlist[{index}]"
    _expect_type(item, dict, field)
    required = {"provider_series_id", "added_at", "status"}
    allowed = required | {"list_id", "list_name", "list_kind"}
    missing = sorted(required - set(item))
    if missing:
        raise SnapshotValidationError(f"{field} is missing keys: {', '.join(missing)}")
    extras = sorted(set(item) - allowed)
    if extras:
        raise SnapshotValidationError(f"{field} contains unexpected keys: {', '.join(extras)}")

    provider_series_id = item["provider_series_id"]
    added_at = item["added_at"]
    status = item["status"]
    list_id = item.get("list_id")
    list_name = item.get("list_name")
    list_kind = item.get("list_kind")
    _expect_type(provider_series_id, str, f"{field}.provider_series_id")
    _expect_optional_type(added_at, str, f"{field}.added_at")
    if added_at is not None and not _is_iso_datetime(added_at):
        raise SnapshotValidationError(f"{field}.added_at must be an ISO-8601 datetime string")
    _expect_optional_type(status, str, f"{field}.status")
    _expect_optional_type(list_id, str, f"{field}.list_id")
    _expect_optional_type(list_name, str, f"{field}.list_name")
    _expect_optional_type(list_kind, str, f"{field}.list_kind")

    return WatchlistEntry(
        provider_series_id=provider_series_id,
        added_at=added_at,
        status=status,
        list_id=list_id,
        list_name=list_name,
        list_kind=list_kind,
    )


def validate_snapshot_payload(payload: Any) -> ProviderSnapshot:
    _expect_type(payload, dict, "snapshot")

    required = {
        "contract_version",
        "generated_at",
        "provider",
        "series",
        "progress",
        "watchlist",
        "raw",
    }
    missing = sorted(required - set(payload))
    if missing:
        raise SnapshotValidationError(f"snapshot is missing keys: {', '.join(missing)}")

    allowed = required | {"account_id_hint"}
    extras = sorted(set(payload) - allowed)
    if extras:
        raise SnapshotValidationError(f"snapshot contains unexpected keys: {', '.join(extras)}")

    contract_version = payload["contract_version"]
    generated_at = payload["generated_at"]
    provider = payload["provider"]
    account_id_hint = payload.get("account_id_hint")
    series = payload["series"]
    progress = payload["progress"]
    watchlist = payload["watchlist"]
    raw = payload["raw"]

    _expect_type(contract_version, str, "snapshot.contract_version")
    if contract_version != "1.0":
        raise SnapshotValidationError("snapshot.contract_version must be '1.0'")
    _expect_type(generated_at, str, "snapshot.generated_at")
    if not _is_iso_datetime(generated_at):
        raise SnapshotValidationError("snapshot.generated_at must be an ISO-8601 datetime string")
    _expect_type(provider, str, "snapshot.provider")
    if not provider.strip():
        raise SnapshotValidationError("snapshot.provider must be a non-empty string")
    _expect_optional_type(account_id_hint, str, "snapshot.account_id_hint")
    _expect_type(series, list, "snapshot.series")
    _expect_type(progress, list, "snapshot.progress")
    _expect_type(watchlist, list, "snapshot.watchlist")
    _expect_type(raw, dict, "snapshot.raw")

    validated_series = [_validate_series_item(item, index) for index, item in enumerate(series)]
    validated_progress = [_validate_progress_item(item, index) for index, item in enumerate(progress)]
    validated_watchlist = [_validate_watchlist_item(item, index) for index, item in enumerate(watchlist)]

    known_series_ids: set[str] = set()
    for index, item in enumerate(validated_series):
        if item.provider_series_id in known_series_ids:
            raise SnapshotValidationError(
                f"series[{index}].provider_series_id duplicates an earlier series id: {item.provider_series_id}"
            )
        known_series_ids.add(item.provider_series_id)

    seen_episode_ids: set[str] = set()
    for index, item in enumerate(validated_progress):
        if item.provider_episode_id in seen_episode_ids:
            raise SnapshotValidationError(
                f"progress[{index}].provider_episode_id duplicates an earlier episode id: {item.provider_episode_id}"
            )
        seen_episode_ids.add(item.provider_episode_id)
        if item.provider_series_id not in known_series_ids:
            raise SnapshotValidationError(
                f"progress[{index}].provider_series_id references unknown series id: {item.provider_series_id}"
            )

    seen_watchlist_series_ids: set[str] = set()
    for index, item in enumerate(validated_watchlist):
        if item.provider_series_id in seen_watchlist_series_ids:
            raise SnapshotValidationError(
                f"watchlist[{index}].provider_series_id duplicates an earlier watchlist entry: {item.provider_series_id}"
            )
        seen_watchlist_series_ids.add(item.provider_series_id)
        if item.provider_series_id not in known_series_ids:
            raise SnapshotValidationError(
                f"watchlist[{index}].provider_series_id references unknown series id: {item.provider_series_id}"
            )

    return ProviderSnapshot(
        contract_version=contract_version,
        generated_at=generated_at,
        provider=provider,
        account_id_hint=account_id_hint,
        series=validated_series,
        progress=validated_progress,
        watchlist=validated_watchlist,
        raw=raw,
    )


def validate_snapshot_json_text(text: str) -> ProviderSnapshot:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SnapshotValidationError(f"invalid JSON: {exc}") from exc
    return validate_snapshot_payload(payload)


def validate_snapshot_file(path: Path) -> ProviderSnapshot:
    return validate_snapshot_json_text(path.read_text(encoding="utf-8"))
