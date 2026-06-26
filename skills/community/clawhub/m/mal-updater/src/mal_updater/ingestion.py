from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .config import AppConfig
from .db import bootstrap_database, connect
from .validation import validate_snapshot_payload


@dataclass(slots=True)
class IngestionSummary:
    provider: str
    contract_version: str
    series_count: int
    progress_count: int
    watchlist_count: int
    sync_run_id: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "contract_version": self.contract_version,
            "series_count": self.series_count,
            "progress_count": self.progress_count,
            "watchlist_count": self.watchlist_count,
            "sync_run_id": self.sync_run_id,
        }


def ingest_snapshot_payload(payload: Any, config: AppConfig) -> IngestionSummary:
    snapshot = validate_snapshot_payload(payload)
    bootstrap_database(config.db_path)

    provider = snapshot.provider
    contract_version = snapshot.contract_version

    with connect(config.db_path) as conn:
        sync_run_id = _insert_sync_run(conn, provider, contract_version)
        try:
            _upsert_series(conn, provider, snapshot.series)
            _upsert_progress(conn, provider, snapshot.progress)
            _upsert_watchlist(conn, provider, snapshot.watchlist)
            summary = IngestionSummary(
                provider=provider,
                contract_version=contract_version,
                series_count=len(snapshot.series),
                progress_count=len(snapshot.progress),
                watchlist_count=len(snapshot.watchlist),
                sync_run_id=sync_run_id,
            )
            _complete_sync_run(conn, sync_run_id, "completed", summary.as_dict())
            conn.commit()
            return summary
        except Exception as exc:
            _complete_sync_run(conn, sync_run_id, "failed", {"error": str(exc)})
            conn.commit()
            raise


def ingest_snapshot_file(path: Path, config: AppConfig) -> IngestionSummary:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return ingest_snapshot_payload(payload, config)


def _insert_sync_run(conn, provider: str, contract_version: str) -> int:
    cursor = conn.execute(
        """
        INSERT INTO sync_runs(provider, contract_version, mode, status)
        VALUES (?, ?, ?, ?)
        """,
        (provider, contract_version, "ingest_snapshot", "running"),
    )
    return int(cursor.lastrowid)


def _complete_sync_run(conn, sync_run_id: int, status: str, summary: dict[str, Any]) -> None:
    conn.execute(
        """
        UPDATE sync_runs
        SET status = ?, completed_at = CURRENT_TIMESTAMP, summary_json = ?
        WHERE id = ?
        """,
        (status, json.dumps(summary, sort_keys=True), sync_run_id),
    )


def _upsert_series(conn, provider: str, series_entries: list[Any]) -> None:
    for entry in series_entries:
        raw_entry = asdict(entry)
        conn.execute(
            """
            INSERT INTO provider_series (
                provider,
                provider_series_id,
                title,
                season_title,
                season_number,
                raw_json,
                first_seen_at,
                last_seen_at
            ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(provider, provider_series_id) DO UPDATE SET
                title = excluded.title,
                season_title = excluded.season_title,
                season_number = excluded.season_number,
                raw_json = excluded.raw_json,
                last_seen_at = CURRENT_TIMESTAMP
            """,
            (
                provider,
                entry.provider_series_id,
                entry.title,
                entry.season_title,
                entry.season_number,
                json.dumps(raw_entry, sort_keys=True),
            ),
        )


def _upsert_progress(conn, provider: str, progress_entries: list[Any]) -> None:
    for entry in progress_entries:
        raw_entry = asdict(entry)
        conn.execute(
            """
            INSERT INTO provider_episode_progress (
                provider,
                provider_episode_id,
                provider_series_id,
                episode_number,
                episode_title,
                playback_position_ms,
                duration_ms,
                completion_ratio,
                last_watched_at,
                audio_locale,
                subtitle_locale,
                rating,
                raw_json,
                first_seen_at,
                last_seen_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(provider, provider_episode_id) DO UPDATE SET
                provider_series_id = excluded.provider_series_id,
                episode_number = excluded.episode_number,
                episode_title = excluded.episode_title,
                playback_position_ms = excluded.playback_position_ms,
                duration_ms = excluded.duration_ms,
                completion_ratio = excluded.completion_ratio,
                last_watched_at = excluded.last_watched_at,
                audio_locale = excluded.audio_locale,
                subtitle_locale = excluded.subtitle_locale,
                rating = excluded.rating,
                raw_json = excluded.raw_json,
                last_seen_at = CURRENT_TIMESTAMP
            """,
            (
                provider,
                entry.provider_episode_id,
                entry.provider_series_id,
                entry.episode_number,
                entry.episode_title,
                entry.playback_position_ms,
                entry.duration_ms,
                entry.completion_ratio,
                entry.last_watched_at,
                entry.audio_locale,
                entry.subtitle_locale,
                entry.rating,
                json.dumps(raw_entry, sort_keys=True),
            ),
        )


def _upsert_watchlist(conn, provider: str, watchlist_entries: list[Any]) -> None:
    for entry in watchlist_entries:
        raw_entry = asdict(entry)
        conn.execute(
            """
            INSERT INTO provider_watchlist (
                provider,
                provider_series_id,
                added_at,
                status,
                raw_json,
                first_seen_at,
                last_seen_at
            ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(provider, provider_series_id) DO UPDATE SET
                added_at = excluded.added_at,
                status = excluded.status,
                raw_json = excluded.raw_json,
                last_seen_at = CURRENT_TIMESTAMP
            """,
            (
                provider,
                entry.provider_series_id,
                entry.added_at,
                entry.status,
                json.dumps(raw_entry, sort_keys=True),
            ),
        )
