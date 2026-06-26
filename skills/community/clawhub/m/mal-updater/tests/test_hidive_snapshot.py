from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mal_updater.config import load_config
from mal_updater.hidive_auth import HidiveSession, HidiveStatePaths, HidiveTokenSet
from mal_updater.hidive_snapshot import fetch_snapshot


class HidiveSnapshotTests(unittest.TestCase):
    def _build_session(self, root: Path) -> HidiveSession:
        config = load_config(root)
        state_paths = HidiveStatePaths(
            root=root / ".MAL-Updater" / "state" / "hidive" / "default",
            access_token_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "authorisation_token.txt",
            refresh_token_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "refresh_token.txt",
            session_state_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "session.json",
            sync_boundary_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "sync_boundary.json",
        )
        return HidiveSession(
            config=config,
            profile="default",
            state_paths=state_paths,
            token=HidiveTokenSet(authorisation_token="access-token", refresh_token="refresh-token", account_id="acct-123"),
        )

    def test_fetch_snapshot_combines_history_and_continue_watching(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)
            session.state_paths.root.mkdir(parents=True, exist_ok=True)

            history_payload = {
                "vods": [
                    {
                        "id": 1001,
                        "title": "Episode 12",
                        "duration": 1440,
                        "watchedAt": 1770504571302,
                        "externalAssetId": "EPSX0000000000117504",
                        "rating": "TV-14",
                        "episodeInformation": {
                            "seasonNumber": 1,
                            "episodeNumber": 12,
                            "season": 32844,
                            "seasonTitle": "Season 1",
                            "seriesInformation": {
                                "id": 3560,
                                "title": "Dusk Beyond the End of the World",
                            },
                        },
                    }
                ],
                "page": 1,
                "totalPages": 1,
            }
            home_payload = {
                "buckets": [
                    {
                        "name": "CONTINUE WATCHING",
                        "bucketId": 25401,
                        "type": "VOD_VIDEO",
                        "contentList": [
                            {
                                "id": 2002,
                                "title": "Episode 3",
                                "duration": 1500,
                                "watchedAt": 1770600000000,
                                "externalAssetId": "EPSX0000000000999999",
                                "watchProgress": 600,
                                "rating": "TV-14",
                                "episodeInformation": {
                                    "seasonNumber": 2,
                                    "episodeNumber": 3,
                                    "seasonTitle": "Season 2",
                                    "seriesInformation": {
                                        "id": 4000,
                                        "title": "Example Continue Show",
                                    },
                                },
                            }
                        ],
                    }
                ]
            }
            favourites_payload = {
                "events": [
                    {
                        "id": 5005,
                        "title": "Favorite Show",
                        "publishedDate": 1770700000000,
                    }
                ],
                "page": 1,
                "totalPages": 1,
            }

            with patch("mal_updater.hidive_snapshot.start_hidive_session", return_value=session), patch.object(
                HidiveSession,
                "json_get",
                side_effect=[history_payload, home_payload, favourites_payload],
            ):
                result = fetch_snapshot(load_config(root))

        self.assertEqual(result.snapshot.provider, "hidive")
        self.assertEqual(3, len(result.snapshot.series))
        self.assertEqual(2, len(result.snapshot.progress))
        progress_by_episode = {item.provider_episode_id: item for item in result.snapshot.progress}
        self.assertEqual(1001, int(progress_by_episode["1001"].provider_episode_id))
        self.assertEqual(1.0, progress_by_episode["1001"].completion_ratio)
        self.assertEqual(600000, progress_by_episode["2002"].playback_position_ms)
        self.assertEqual(0.4, progress_by_episode["2002"].completion_ratio)
        self.assertEqual(1, len(result.snapshot.watchlist))
        self.assertEqual('5005', result.snapshot.watchlist[0].provider_series_id)
        self.assertEqual('Favorites', result.snapshot.watchlist[0].list_name)
        self.assertEqual({"history": True, "continue_watching": True, "watchlists": True}, result.snapshot.raw["supports"])
        self.assertFalse(result.snapshot.raw["sync_boundary_present"])
        self.assertEqual("incremental", result.snapshot.raw["sync_boundary_mode"])
        self.assertEqual(str(session.state_paths.sync_boundary_path), result.snapshot.raw["sync_boundary_path"])

    def test_fetch_snapshot_stops_early_when_incremental_boundary_matches(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)
            session.state_paths.root.mkdir(parents=True, exist_ok=True)
            session.state_paths.sync_boundary_path.write_text(
                '{\n'
                '  "schema_version": 1,\n'
                '  "generated_at": "2026-03-20T00:00:00Z",\n'
                '  "account_id_hint": "acct-123",\n'
                '  "history": {"first_seen": ["3560|1001|1770504571302"]},\n'
                '  "continue_watching": {"first_seen": ["4000|2002|1770600000000|600"]},\n'
                '  "favourites": {"first_seen": ["5005|Favorite Show"]}\n'
                '}\n',
                encoding="utf-8",
            )
            history_payload = {
                "vods": [
                    {
                        "id": 1001,
                        "title": "Episode 12",
                        "duration": 1440,
                        "watchedAt": 1770504571302,
                        "episodeInformation": {
                            "seasonNumber": 1,
                            "episodeNumber": 12,
                            "seasonTitle": "Season 1",
                            "seriesInformation": {"id": 3560, "title": "Dusk Beyond the End of the World"},
                        },
                    }
                ],
                "page": 1,
                "totalPages": 9,
            }
            home_payload = {
                "buckets": [
                    {
                        "name": "CONTINUE WATCHING",
                        "contentList": [
                            {
                                "id": 2002,
                                "title": "Episode 3",
                                "duration": 1500,
                                "watchedAt": 1770600000000,
                                "watchProgress": 600,
                                "episodeInformation": {
                                    "seasonNumber": 2,
                                    "episodeNumber": 3,
                                    "seasonTitle": "Season 2",
                                    "seriesInformation": {"id": 4000, "title": "Example Continue Show"},
                                },
                            }
                        ],
                    }
                ]
            }
            favourites_payload = {"events": [{"id": 5005, "title": "Favorite Show"}], "page": 1, "totalPages": 99}
            with patch("mal_updater.hidive_snapshot.start_hidive_session", return_value=session), patch.object(
                HidiveSession,
                "json_get",
                side_effect=[history_payload, home_payload, favourites_payload],
            ):
                result = fetch_snapshot(load_config(root))

        self.assertTrue(result.snapshot.raw["history_stopped_early"])
        self.assertTrue(result.snapshot.raw["continue_stopped_early"])
        self.assertTrue(result.snapshot.raw["favourite_stopped_early"])
        self.assertTrue(result.snapshot.raw["sync_boundary_present"])


if __name__ == "__main__":
    unittest.main()
