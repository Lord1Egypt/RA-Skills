from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mal_updater.config import load_config
from mal_updater.ingestion import ingest_snapshot_payload
from mal_updater.validation import SnapshotValidationError, validate_snapshot_payload


def sample_snapshot() -> dict:
    return {
        "contract_version": "1.0",
        "generated_at": "2026-03-14T21:00:00Z",
        "provider": "crunchyroll",
        "account_id_hint": None,
        "series": [
            {
                "provider_series_id": "series-123",
                "title": "Example Show",
                "season_title": "Example Show Season 1",
                "season_number": 1,
            }
        ],
        "progress": [
            {
                "provider_episode_id": "episode-456",
                "provider_series_id": "series-123",
                "episode_number": 3,
                "episode_title": "Example Episode",
                "playback_position_ms": 1300000,
                "duration_ms": 1440000,
                "completion_ratio": 0.95,
                "last_watched_at": "2026-03-14T20:55:00Z",
                "audio_locale": "en-US",
                "subtitle_locale": None,
                "rating": None,
            }
        ],
        "watchlist": [
            {
                "provider_series_id": "series-123",
                "added_at": "2026-03-10T12:00:00Z",
                "status": "watching",
                "list_id": "favorites",
                "list_name": "Favorites",
                "list_kind": "system",
            }
        ],
        "raw": {},
    }


class ValidationTests(unittest.TestCase):
    def test_validate_snapshot_payload_returns_dataclass_model(self) -> None:
        snapshot = validate_snapshot_payload(sample_snapshot())
        self.assertEqual(snapshot.provider, "crunchyroll")
        self.assertEqual(snapshot.contract_version, "1.0")
        self.assertEqual(snapshot.series[0].provider_series_id, "series-123")
        self.assertEqual(snapshot.progress[0].completion_ratio, 0.95)
        self.assertEqual(snapshot.watchlist[0].status, "watching")
        self.assertEqual(snapshot.watchlist[0].list_id, "favorites")
        self.assertEqual(snapshot.watchlist[0].list_kind, "system")

    def test_validate_snapshot_payload_rejects_invalid_ratio(self) -> None:
        payload = sample_snapshot()
        payload["progress"][0]["completion_ratio"] = 1.5
        with self.assertRaises(SnapshotValidationError):
            validate_snapshot_payload(payload)

    def test_validate_snapshot_payload_rejects_progress_unknown_series(self) -> None:
        payload = sample_snapshot()
        payload["progress"][0]["provider_series_id"] = "series-missing"
        with self.assertRaises(SnapshotValidationError):
            validate_snapshot_payload(payload)

    def test_validate_snapshot_payload_rejects_duplicate_episode_ids(self) -> None:
        payload = sample_snapshot()
        payload["progress"].append({**payload["progress"][0]})
        with self.assertRaises(SnapshotValidationError):
            validate_snapshot_payload(payload)

    def test_validate_snapshot_payload_rejects_duplicate_watchlist_ids(self) -> None:
        payload = sample_snapshot()
        payload["watchlist"].append({**payload["watchlist"][0]})
        with self.assertRaises(SnapshotValidationError):
            validate_snapshot_payload(payload)


class IngestionTests(unittest.TestCase):
    def test_ingest_snapshot_payload_writes_rows_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)

            summary = ingest_snapshot_payload(sample_snapshot(), config)

            self.assertEqual(summary.provider, "crunchyroll")
            self.assertEqual(summary.series_count, 1)
            self.assertEqual(summary.progress_count, 1)
            self.assertEqual(summary.watchlist_count, 1)
            self.assertIsNotNone(summary.sync_run_id)

            import sqlite3

            conn = sqlite3.connect(config.db_path)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM provider_series").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM provider_episode_progress").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM provider_watchlist").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM sync_runs WHERE status = 'completed'").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
