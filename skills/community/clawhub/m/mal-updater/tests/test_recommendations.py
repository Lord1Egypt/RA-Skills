from __future__ import annotations

import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from mal_updater.cli import main as cli_main
from mal_updater.config import load_config
from mal_updater.db import (
    bootstrap_database,
    connect,
    get_mal_anime_metadata_map,
    replace_mal_anime_relations,
    replace_mal_recommendation_edges,
    upsert_mal_anime_metadata,
    upsert_series_mapping,
)
from mal_updater.recommendation_metadata import refresh_recommendation_metadata
from mal_updater.recommendations import Recommendation, build_recommendations, group_recommendations


class RecommendationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)
        (self.project_root / ".MAL-Updater" / "config").mkdir(parents=True, exist_ok=True)
        self.config = load_config(self.project_root)
        bootstrap_database(self.config.db_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _insert_series(
        self,
        provider_series_id: str,
        *,
        title: str,
        season_title: str | None = None,
        season_number: int | None = None,
        watchlist_status: str | None = None,
    ) -> None:
        with connect(self.config.db_path) as conn:
            conn.execute(
                """
                INSERT INTO provider_series (provider, provider_series_id, title, season_title, season_number, raw_json)
                VALUES ('crunchyroll', ?, ?, ?, ?, '{}')
                """,
                (provider_series_id, title, season_title, season_number),
            )
            if watchlist_status is not None:
                conn.execute(
                    """
                    INSERT INTO provider_watchlist (provider, provider_series_id, status, raw_json)
                    VALUES ('crunchyroll', ?, ?, '{}')
                    """,
                    (provider_series_id, watchlist_status),
                )
            conn.commit()

    def _insert_progress(
        self,
        provider_series_id: str,
        provider_episode_id: str,
        *,
        episode_number: int,
        completion_ratio: float,
        last_watched_at: str,
    ) -> None:
        with connect(self.config.db_path) as conn:
            conn.execute(
                """
                INSERT INTO provider_episode_progress (
                    provider,
                    provider_episode_id,
                    provider_series_id,
                    episode_number,
                    completion_ratio,
                    last_watched_at,
                    raw_json
                ) VALUES ('crunchyroll', ?, ?, ?, ?, ?, '{}')
                """,
                (provider_episode_id, provider_series_id, episode_number, completion_ratio, last_watched_at),
            )
            conn.commit()

    def _map_series(self, provider_series_id: str, mal_anime_id: int) -> None:
        upsert_series_mapping(
            self.config.db_path,
            provider="crunchyroll",
            provider_series_id=provider_series_id,
            mal_anime_id=mal_anime_id,
            confidence=1.0,
            mapping_source="user_approved",
            approved_by_user=True,
            notes=None,
        )

    def _cache_metadata(
        self,
        mal_anime_id: int,
        *,
        title: str,
        mean: float | None = None,
        popularity: int | None = None,
        genres: list[str] | None = None,
        studios: list[str] | None = None,
        source: str | None = None,
    ) -> None:
        raw = {"id": mal_anime_id, "title": title}
        if genres:
            raw["genres"] = [{"name": genre} for genre in genres]
        if studios:
            raw["studios"] = [{"name": studio} for studio in studios]
        if source:
            raw["source"] = source
        upsert_mal_anime_metadata(
            self.config.db_path,
            mal_anime_id=mal_anime_id,
            title=title,
            title_english=None,
            title_japanese=None,
            alternative_titles=[],
            media_type="tv",
            status="finished_airing",
            num_episodes=12,
            mean=mean,
            popularity=popularity,
            start_season=None,
            raw=raw,
        )

    def _cache_relations(self, mal_anime_id: int, relations: list[dict]) -> None:
        replace_mal_anime_relations(self.config.db_path, mal_anime_id=mal_anime_id, relations=relations)

    def _cache_recommendations(self, mal_anime_id: int, edges: list[dict]) -> None:
        replace_mal_recommendation_edges(self.config.db_path, source_mal_anime_id=mal_anime_id, hop_distance=1, edges=edges)

    def test_new_dubbed_episode_recommendation_detects_contiguous_tail_gap(self) -> None:
        self._insert_series(
            "series-1",
            title="Example Show",
            season_title="Example Show Season 2 (English Dub)",
            season_number=2,
            watchlist_status="in_progress",
        )
        self._insert_progress("series-1", "ep-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-10T01:00:00Z")
        self._insert_progress("series-1", "ep-2", episode_number=2, completion_ratio=1.0, last_watched_at="2026-03-10T02:00:00Z")
        self._insert_progress("series-1", "ep-3", episode_number=3, completion_ratio=0.2, last_watched_at="2026-03-11T02:00:00Z")

        results = build_recommendations(self.config, limit=0)

        self.assertEqual(1, len(results))
        item = results[0]
        self.assertEqual("new_dubbed_episode", item.kind)
        self.assertEqual("series-1", item.provider_series_id)
        self.assertEqual(1, item.context["contiguous_tail_gap"])

    def test_new_season_recommendation_detects_completed_predecessor(self) -> None:
        self._insert_series(
            "season-1",
            title="Franchise Show",
            season_title="Franchise Show (English Dub)",
            season_number=1,
            watchlist_status="fully_watched",
        )
        self._insert_progress("season-1", "s1-ep-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_progress("season-1", "s1-ep-2", episode_number=2, completion_ratio=1.0, last_watched_at="2026-03-01T02:00:00Z")

        self._insert_series(
            "season-2",
            title="Franchise Show",
            season_title="Franchise Show Season 2 (English Dub)",
            season_number=2,
            watchlist_status="never_watched",
        )

        results = build_recommendations(self.config, limit=0)

        self.assertEqual(1, len(results))
        item = results[0]
        self.assertEqual("new_season", item.kind)
        self.assertEqual("season-2", item.provider_series_id)
        self.assertEqual("season-1", item.context["predecessor_provider_series_id"])

    def test_relation_backed_new_season_recommendation_detects_title_drift(self) -> None:
        self._insert_series(
            "sg",
            title="Steins;Gate",
            season_title="Steins;Gate (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("sg", "sg-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_progress("sg", "sg-2", episode_number=2, completion_ratio=1.0, last_watched_at="2026-03-01T02:00:00Z")
        self._insert_series(
            "sg0",
            title="Steins;Gate 0",
            season_title="Steins;Gate 0 (English Dub)",
            watchlist_status="never_watched",
        )
        self._map_series("sg", 9253)
        self._map_series("sg0", 30484)
        self._cache_metadata(9253, title="Steins;Gate")
        self._cache_metadata(30484, title="Steins;Gate 0")
        self._cache_relations(
            9253,
            [
                {
                    "related_mal_anime_id": 30484,
                    "relation_type": "sequel",
                    "relation_type_formatted": "Sequel",
                    "related_title": "Steins;Gate 0",
                    "raw": {"relation_type": "sequel", "node": {"id": 30484, "title": "Steins;Gate 0"}},
                }
            ],
        )

        results = build_recommendations(self.config, limit=0)

        items = [item for item in results if item.provider_series_id == "sg0" and item.kind == "new_season"]
        self.assertEqual(1, len(items))
        self.assertTrue(items[0].context["relation_backed"])
        self.assertEqual("sg", items[0].context["predecessor_provider_series_id"])

    def test_new_season_recommendation_detects_roman_numeral_installments(self) -> None:
        self._insert_series(
            "overlord-2",
            title="Overlord",
            season_title="Overlord II (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("overlord-2", "ol2-ep-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_progress("overlord-2", "ol2-ep-2", episode_number=2, completion_ratio=1.0, last_watched_at="2026-03-01T02:00:00Z")

        self._insert_series(
            "overlord-3",
            title="Overlord",
            season_title="Overlord III (English Dub)",
            watchlist_status="never_watched",
        )

        results = build_recommendations(self.config, limit=0)

        roman_items = [item for item in results if item.provider_series_id == "overlord-3"]
        self.assertEqual(1, len(roman_items))
        item = roman_items[0]
        self.assertEqual("new_season", item.kind)
        self.assertEqual("overlord-2", item.context["predecessor_provider_series_id"])
        self.assertEqual(3, item.context["installment_index"])

    def test_new_season_recommendation_detects_ordinal_season_naming(self) -> None:
        self._insert_series(
            "show-1",
            title="Ordinal Show",
            season_title="Ordinal Show (English Dub)",
            season_number=1,
            watchlist_status="fully_watched",
        )
        self._insert_progress("show-1", "show1-ep-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-02T01:00:00Z")
        self._insert_progress("show-1", "show1-ep-2", episode_number=2, completion_ratio=1.0, last_watched_at="2026-03-02T02:00:00Z")

        self._insert_series(
            "show-2",
            title="Ordinal Show",
            season_title="Ordinal Show Second Season (English Dub)",
            watchlist_status="never_watched",
        )

        results = build_recommendations(self.config, limit=0)

        ordinal_items = [item for item in results if item.provider_series_id == "show-2"]
        self.assertEqual(1, len(ordinal_items))
        item = ordinal_items[0]
        self.assertEqual("new_season", item.kind)
        self.assertEqual("show-1", item.context["predecessor_provider_series_id"])
        self.assertEqual(2, item.context["installment_index"])

    def test_new_season_recommendation_detects_part_style_names_only_with_season_context(self) -> None:
        self._insert_series(
            "final-part-1",
            title="Split Show",
            season_title="Split Show Final Season Part 1 (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress(
            "final-part-1",
            "split-ep-1",
            episode_number=1,
            completion_ratio=1.0,
            last_watched_at="2026-03-03T01:00:00Z",
        )
        self._insert_progress(
            "final-part-1",
            "split-ep-2",
            episode_number=2,
            completion_ratio=1.0,
            last_watched_at="2026-03-03T02:00:00Z",
        )

        self._insert_series(
            "final-part-2",
            title="Split Show",
            season_title="Split Show Final Season Part 2 (English Dub)",
            watchlist_status="never_watched",
        )
        self._insert_series(
            "bare-part-2",
            title="Split Show",
            season_title="Split Show Part 2 (English Dub)",
            watchlist_status="never_watched",
        )

        results = build_recommendations(self.config, limit=0)

        final_items = [item for item in results if item.provider_series_id == "final-part-2"]
        self.assertEqual(1, len(final_items))
        item = final_items[0]
        self.assertEqual("new_season", item.kind)
        self.assertEqual("final-part-1", item.context["predecessor_provider_series_id"])
        self.assertEqual(2, item.context["installment_index"])

        bare_items = [item for item in results if item.provider_series_id == "bare-part-2"]
        self.assertEqual([], bare_items)

    def test_part_style_detection_ignores_titles_that_only_contain_season_word(self) -> None:
        self._insert_series(
            "title-season-part-1",
            title="Split Season Show",
            season_title="Split Season Show Final Season Part 1 (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress(
            "title-season-part-1",
            "title-season-ep-1",
            episode_number=1,
            completion_ratio=1.0,
            last_watched_at="2026-03-04T01:00:00Z",
        )
        self._insert_progress(
            "title-season-part-1",
            "title-season-ep-2",
            episode_number=2,
            completion_ratio=1.0,
            last_watched_at="2026-03-04T02:00:00Z",
        )

        self._insert_series(
            "title-season-bare-part-2",
            title="Split Season Show",
            season_title="Split Season Show Part 2 (English Dub)",
            watchlist_status="never_watched",
        )

        results = build_recommendations(self.config, limit=0)

        bare_items = [item for item in results if item.provider_series_id == "title-season-bare-part-2"]
        self.assertEqual([], bare_items)

    def test_suppresses_skipped_episode_artifacts_that_are_not_tail_gaps(self) -> None:
        self._insert_series(
            "series-skip",
            title="Skip Show",
            season_title="Skip Show (English Dub)",
            season_number=1,
            watchlist_status="fully_watched",
        )
        self._insert_progress("series-skip", "ep-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-10T01:00:00Z")
        self._insert_progress("series-skip", "ep-2", episode_number=2, completion_ratio=0.1, last_watched_at="2026-03-10T02:00:00Z")
        self._insert_progress("series-skip", "ep-3", episode_number=3, completion_ratio=1.0, last_watched_at="2026-03-10T03:00:00Z")

        results = build_recommendations(self.config, limit=0)

        self.assertEqual([], [item for item in results if item.provider_series_id == "series-skip"])

    def test_suppresses_fully_watched_series_when_latest_episode_is_effectively_complete(self) -> None:
        self._insert_series(
            "series-complete",
            title="Complete Show",
            season_title="Complete Show (English Dub)",
            season_number=1,
            watchlist_status="fully_watched",
        )
        self._insert_progress("series-complete", "ep-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-10T01:00:00Z")
        self._insert_progress("series-complete", "ep-2", episode_number=2, completion_ratio=0.99995, last_watched_at="2026-03-10T02:00:00Z")

        results = build_recommendations(self.config, limit=0)

        self.assertEqual([], [item for item in results if item.provider_series_id == "series-complete"])

    def test_more_recent_in_progress_tail_gap_ranks_above_stale_one(self) -> None:
        self._insert_series(
            "recent-show",
            title="Recent Show",
            season_title="Recent Show (English Dub)",
            watchlist_status="in_progress",
        )
        self._insert_progress("recent-show", "r1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-14T01:00:00Z")
        self._insert_progress("recent-show", "r2", episode_number=2, completion_ratio=0.2, last_watched_at="2026-03-14T02:00:00Z")

        self._insert_series(
            "stale-show",
            title="Stale Show",
            season_title="Stale Show (English Dub)",
            watchlist_status="in_progress",
        )
        self._insert_progress("stale-show", "s1", episode_number=1, completion_ratio=1.0, last_watched_at="2020-03-10T01:00:00Z")
        self._insert_progress("stale-show", "s2", episode_number=2, completion_ratio=0.2, last_watched_at="2020-03-10T02:00:00Z")

        results = build_recommendations(self.config, limit=0)

        recent = [item for item in results if item.provider_series_id == "recent-show"][0]
        stale = [item for item in results if item.provider_series_id == "stale-show"][0]
        self.assertEqual("new_dubbed_episode", recent.kind)
        self.assertEqual("resume_backlog", stale.kind)
        self.assertGreater(recent.priority, stale.priority)

    def test_discovery_candidate_aggregates_recommendation_support(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_series(
            "seed-b",
            title="Seed B",
            season_title="Seed B (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-b", "seed-b-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-02T01:00:00Z")
        self._map_series("seed-a", 100)
        self._map_series("seed-b", 200)
        self._cache_metadata(100, title="Seed A")
        self._cache_metadata(200, title="Seed B")
        self._cache_metadata(300, title="Discovery Hit")
        self._cache_recommendations(100, [{"target_mal_anime_id": 300, "target_title": "Discovery Hit", "num_recommendations": 20, "raw": {}}])
        self._cache_recommendations(200, [{"target_mal_anime_id": 300, "target_title": "Discovery Hit", "num_recommendations": 15, "raw": {}}])

        results = build_recommendations(self.config, limit=0)

        discovery = [item for item in results if item.kind == "discovery_candidate"]
        self.assertEqual(1, len(discovery))
        item = discovery[0]
        self.assertEqual("mal:300", item.provider_series_id)
        self.assertEqual(2, item.context["supporting_source_count"])
        self.assertEqual(35, item.context["aggregated_recommendation_votes"])

    def test_discovery_candidate_prefers_cached_genre_overlap(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._map_series("seed-a", 100)
        self._cache_metadata(100, title="Seed A", genres=["Sci-Fi", "Thriller"])
        self._cache_metadata(300, title="Genre Match", mean=8.0, popularity=500, genres=["Sci-Fi", "Action"])
        self._cache_metadata(400, title="Genre Miss", mean=8.0, popularity=500, genres=["Romance"])
        self._cache_recommendations(100, [
            {"target_mal_anime_id": 300, "target_title": "Genre Match", "num_recommendations": 20, "raw": {}},
            {"target_mal_anime_id": 400, "target_title": "Genre Miss", "num_recommendations": 20, "raw": {}},
        ])

        results = [item for item in build_recommendations(self.config, limit=0) if item.kind == "discovery_candidate"]

        self.assertEqual(["mal:300", "mal:400"], [item.provider_series_id for item in results])
        self.assertEqual(["Sci-Fi"], results[0].context["shared_genres"])
        self.assertGreater(results[0].context["genre_overlap_score"], 0)
        self.assertIn("shared seed genres: Sci-Fi", results[0].reasons)
        self.assertEqual([], results[1].context["shared_genres"])
        self.assertEqual(0, results[1].context["genre_overlap_score"])
        self.assertGreater(results[0].priority, results[1].priority)

    def test_discovery_candidate_prefers_cached_studio_overlap_when_votes_tie(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._map_series("seed-a", 100)
        self._cache_metadata(100, title="Seed A", studios=["Bones"])
        self._cache_metadata(300, title="Studio Match", mean=8.0, popularity=500, studios=["Bones"])
        self._cache_metadata(400, title="Studio Miss", mean=8.0, popularity=500, studios=["Madhouse"])
        self._cache_recommendations(100, [
            {"target_mal_anime_id": 300, "target_title": "Studio Match", "num_recommendations": 20, "raw": {}},
            {"target_mal_anime_id": 400, "target_title": "Studio Miss", "num_recommendations": 20, "raw": {}},
        ])

        results = [item for item in build_recommendations(self.config, limit=0) if item.kind == "discovery_candidate"]

        self.assertEqual(["mal:300", "mal:400"], [item.provider_series_id for item in results])
        self.assertEqual(["Bones"], results[0].context["shared_studios"])
        self.assertGreater(results[0].context["studio_overlap_score"], 0)
        self.assertIn("shared seed studios: Bones", results[0].reasons)
        self.assertEqual([], results[1].context["shared_studios"])
        self.assertEqual(0, results[1].context["studio_overlap_score"])
        self.assertGreater(results[0].priority, results[1].priority)

    def test_discovery_candidate_prefers_cached_source_overlap_when_votes_tie(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._map_series("seed-a", 100)
        self._cache_metadata(100, title="Seed A", source="light_novel")
        self._cache_metadata(300, title="Source Match", mean=8.0, popularity=500, source="light_novel")
        self._cache_metadata(400, title="Source Miss", mean=8.0, popularity=500, source="manga")
        self._cache_recommendations(100, [
            {"target_mal_anime_id": 300, "target_title": "Source Match", "num_recommendations": 20, "raw": {}},
            {"target_mal_anime_id": 400, "target_title": "Source Miss", "num_recommendations": 20, "raw": {}},
        ])

        results = [item for item in build_recommendations(self.config, limit=0) if item.kind == "discovery_candidate"]

        self.assertEqual(["mal:300", "mal:400"], [item.provider_series_id for item in results])
        self.assertEqual("light_novel", results[0].context["source"])
        self.assertGreater(results[0].context["source_overlap_score"], 0)
        self.assertIn("shared seed source material: light_novel", results[0].reasons)
        self.assertEqual("manga", results[1].context["source"])
        self.assertEqual(0, results[1].context["source_overlap_score"])
        self.assertGreater(results[0].priority, results[1].priority)

    def test_discovery_candidate_skips_direct_franchise_relations_from_seed_titles(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._map_series("seed-a", 100)
        self._cache_metadata(100, title="Seed A")
        self._cache_metadata(300, title="Seed A Sequel")
        self._cache_metadata(400, title="Different Discovery")
        self._cache_relations(
            100,
            [
                {
                    "related_mal_anime_id": 300,
                    "relation_type": "sequel",
                    "relation_type_formatted": "Sequel",
                    "related_title": "Seed A Sequel",
                    "raw": {"relation_type": "sequel", "node": {"id": 300, "title": "Seed A Sequel"}},
                }
            ],
        )
        self._cache_recommendations(100, [
            {"target_mal_anime_id": 300, "target_title": "Seed A Sequel", "num_recommendations": 20, "raw": {}},
            {"target_mal_anime_id": 400, "target_title": "Different Discovery", "num_recommendations": 18, "raw": {}},
        ])

        results = [item for item in build_recommendations(self.config, limit=0) if item.kind == "discovery_candidate"]

        self.assertEqual(["mal:400"], [item.provider_series_id for item in results])

    def test_discovery_candidate_skips_franchise_relations_even_when_edge_comes_from_different_seed(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_series(
            "seed-b",
            title="Seed B",
            season_title="Seed B (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-b", "seed-b-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-02T01:00:00Z")
        self._map_series("seed-a", 100)
        self._map_series("seed-b", 200)
        self._cache_metadata(100, title="Seed A")
        self._cache_metadata(200, title="Seed B")
        self._cache_metadata(300, title="Seed A Sequel")
        self._cache_metadata(400, title="Different Discovery")
        self._cache_relations(
            100,
            [
                {
                    "related_mal_anime_id": 300,
                    "relation_type": "sequel",
                    "relation_type_formatted": "Sequel",
                    "related_title": "Seed A Sequel",
                    "raw": {"relation_type": "sequel", "node": {"id": 300, "title": "Seed A Sequel"}},
                }
            ],
        )
        self._cache_recommendations(200, [
            {"target_mal_anime_id": 300, "target_title": "Seed A Sequel", "num_recommendations": 20, "raw": {}},
            {"target_mal_anime_id": 400, "target_title": "Different Discovery", "num_recommendations": 18, "raw": {}},
        ])

        results = [item for item in build_recommendations(self.config, limit=0) if item.kind == "discovery_candidate"]

        self.assertEqual(["mal:400"], [item.provider_series_id for item in results])

    def test_discovery_candidate_skips_titles_already_present_in_provider_catalog(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_series(
            "already-here",
            title="Already Here",
            season_title="Already Here (English Dub)",
            watchlist_status="available",
        )
        self._map_series("seed-a", 100)
        self._cache_metadata(100, title="Seed A")
        self._cache_metadata(300, title="Already Here")
        self._cache_recommendations(100, [
            {"target_mal_anime_id": 300, "target_title": "Already Here", "num_recommendations": 20, "raw": {}},
        ])

        results = [item for item in build_recommendations(self.config, limit=0) if item.kind == "discovery_candidate"]

        self.assertEqual([], results)

    def test_discovery_target_metadata_refresh_persists_my_list_status_and_suppresses_candidate(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_series(
            "seed-b",
            title="Seed B",
            season_title="Seed B (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-b", "seed-b-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-02T01:00:00Z")
        self._map_series("seed-a", 100)
        self._map_series("seed-b", 200)

        baseline = build_recommendations(self.config, limit=0)
        baseline_discovery = [item for item in baseline if item.kind == "discovery_candidate"]
        self.assertEqual([], baseline_discovery)

        def fake_get_anime_details(anime_id: int, *, fields: str = "") -> dict:
            payloads = {
                100: {
                    "id": 100,
                    "title": "Seed A",
                    "alternative_titles": {},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 12,
                    "mean": 8.1,
                    "popularity": 500,
                    "start_season": {"year": 2020, "season": "winter"},
                    "related_anime": [],
                    "recommendations": [
                        {"node": {"id": 300, "title": "Discovery Hit"}, "num_recommendations": 20},
                    ],
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12},
                },
                200: {
                    "id": 200,
                    "title": "Seed B",
                    "alternative_titles": {},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 13,
                    "mean": 7.9,
                    "popularity": 800,
                    "start_season": {"year": 2021, "season": "spring"},
                    "related_anime": [],
                    "recommendations": [
                        {"node": {"id": 300, "title": "Discovery Hit"}, "num_recommendations": 15},
                    ],
                    "my_list_status": {"status": "completed", "num_episodes_watched": 13},
                },
                300: {
                    "id": 300,
                    "title": "Discovery Hit",
                    "alternative_titles": {"en": "Discovery Hit"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 24,
                    "mean": 8.7,
                    "popularity": 120,
                    "start_season": {"year": 2022, "season": "fall"},
                    "my_list_status": {"status": "watching", "num_episodes_watched": 3},
                },
            }
            return payloads[anime_id]

        with patch("mal_updater.recommendation_metadata.MalClient.get_anime_details", side_effect=fake_get_anime_details) as get_details:
            summary = refresh_recommendation_metadata(
                self.config,
                include_discovery_targets=True,
            )

        self.assertEqual(2, summary.considered)
        self.assertEqual(2, summary.refreshed)
        requested_ids = [call.args[0] for call in get_details.call_args_list]
        self.assertEqual([100, 200, 300], requested_ids)

        metadata_by_id = get_mal_anime_metadata_map(self.config.db_path)
        self.assertEqual("watching", metadata_by_id[300].raw["my_list_status"]["status"])
        self.assertEqual(3, metadata_by_id[300].raw["my_list_status"]["num_episodes_watched"])

        results = build_recommendations(self.config, limit=0)
        discovery = [item for item in results if item.kind == "discovery_candidate" and item.provider_series_id == "mal:300"]
        self.assertEqual([], discovery)

    def test_discovery_target_limit_prefers_higher_aggregate_votes_when_support_count_ties(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_series(
            "seed-b",
            title="Seed B",
            season_title="Seed B (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-b", "seed-b-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-02T01:00:00Z")
        self._map_series("seed-a", 100)
        self._map_series("seed-b", 200)

        def fake_get_anime_details(anime_id: int, *, fields: str = "") -> dict:
            payloads = {
                100: {
                    "id": 100,
                    "title": "Seed A",
                    "alternative_titles": {},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 12,
                    "mean": 8.1,
                    "popularity": 500,
                    "start_season": {"year": 2020, "season": "winter"},
                    "related_anime": [],
                    "recommendations": [
                        {"node": {"id": 300, "title": "Top Hit"}, "num_recommendations": 40},
                        {"node": {"id": 400, "title": "Runner Up"}, "num_recommendations": 30},
                    ],
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12},
                },
                200: {
                    "id": 200,
                    "title": "Seed B",
                    "alternative_titles": {},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 13,
                    "mean": 7.9,
                    "popularity": 800,
                    "start_season": {"year": 2021, "season": "spring"},
                    "related_anime": [],
                    "recommendations": [
                        {"node": {"id": 300, "title": "Top Hit"}, "num_recommendations": 5},
                        {"node": {"id": 400, "title": "Runner Up"}, "num_recommendations": 25},
                    ],
                    "my_list_status": {"status": "completed", "num_episodes_watched": 13},
                },
                300: {
                    "id": 300,
                    "title": "Top Hit",
                    "alternative_titles": {"en": "Top Hit"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 24,
                    "mean": 8.7,
                    "popularity": 120,
                    "start_season": {"year": 2022, "season": "fall"},
                    "my_list_status": {"status": "watching", "num_episodes_watched": 1},
                },
                400: {
                    "id": 400,
                    "title": "Runner Up",
                    "alternative_titles": {"en": "Runner Up"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 12,
                    "mean": 8.0,
                    "popularity": 240,
                    "start_season": {"year": 2021, "season": "summer"},
                    "my_list_status": {"status": "plan_to_watch", "num_episodes_watched": 0},
                },
            }
            return payloads[anime_id]

        with patch("mal_updater.recommendation_metadata.MalClient.get_anime_details", side_effect=fake_get_anime_details) as get_details:
            summary = refresh_recommendation_metadata(
                self.config,
                include_discovery_targets=True,
                discovery_target_limit=1,
            )

        self.assertEqual(2, summary.considered)
        self.assertEqual(2, summary.refreshed)
        requested_ids = [call.args[0] for call in get_details.call_args_list]
        self.assertEqual([100, 200, 400], requested_ids)

        metadata_by_id = get_mal_anime_metadata_map(self.config.db_path)
        self.assertIn(400, metadata_by_id)
        self.assertEqual("plan_to_watch", metadata_by_id[400].raw["my_list_status"]["status"])
        self.assertNotIn(300, metadata_by_id)

    def test_discovery_target_limit_prefers_aggregate_multi_seed_support(self) -> None:
        self._insert_series(
            "seed-a",
            title="Seed A",
            season_title="Seed A (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-a", "seed-a-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-01T01:00:00Z")
        self._insert_series(
            "seed-b",
            title="Seed B",
            season_title="Seed B (English Dub)",
            watchlist_status="fully_watched",
        )
        self._insert_progress("seed-b", "seed-b-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-02T01:00:00Z")
        self._map_series("seed-a", 100)
        self._map_series("seed-b", 200)

        def fake_get_anime_details(anime_id: int, *, fields: str = "") -> dict:
            payloads = {
                100: {
                    "id": 100,
                    "title": "Seed A",
                    "alternative_titles": {},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 12,
                    "mean": 8.1,
                    "popularity": 500,
                    "start_season": {"year": 2020, "season": "winter"},
                    "related_anime": [],
                    "recommendations": [
                        {"node": {"id": 300, "title": "Burst Hit"}, "num_recommendations": 45},
                        {"node": {"id": 400, "title": "Consensus Pick"}, "num_recommendations": 22},
                    ],
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12},
                },
                200: {
                    "id": 200,
                    "title": "Seed B",
                    "alternative_titles": {},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 13,
                    "mean": 7.9,
                    "popularity": 800,
                    "start_season": {"year": 2021, "season": "spring"},
                    "related_anime": [],
                    "recommendations": [
                        {"node": {"id": 400, "title": "Consensus Pick"}, "num_recommendations": 21},
                    ],
                    "my_list_status": {"status": "completed", "num_episodes_watched": 13},
                },
                300: {
                    "id": 300,
                    "title": "Burst Hit",
                    "alternative_titles": {"en": "Burst Hit"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 12,
                    "mean": 8.0,
                    "popularity": 220,
                    "start_season": {"year": 2021, "season": "fall"},
                    "my_list_status": {"status": "plan_to_watch", "num_episodes_watched": 0},
                },
                400: {
                    "id": 400,
                    "title": "Consensus Pick",
                    "alternative_titles": {"en": "Consensus Pick"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 24,
                    "mean": 8.6,
                    "popularity": 140,
                    "start_season": {"year": 2022, "season": "spring"},
                    "my_list_status": {"status": "watching", "num_episodes_watched": 2},
                },
            }
            return payloads[anime_id]

        with patch("mal_updater.recommendation_metadata.MalClient.get_anime_details", side_effect=fake_get_anime_details) as get_details:
            summary = refresh_recommendation_metadata(
                self.config,
                include_discovery_targets=True,
                discovery_target_limit=1,
            )

        self.assertEqual(2, summary.considered)
        self.assertEqual(2, summary.refreshed)
        requested_ids = [call.args[0] for call in get_details.call_args_list]
        self.assertEqual([100, 200, 400], requested_ids)

        metadata_by_id = get_mal_anime_metadata_map(self.config.db_path)
        self.assertIn(400, metadata_by_id)
        self.assertEqual("watching", metadata_by_id[400].raw["my_list_status"]["status"])
        self.assertNotIn(300, metadata_by_id)

    def test_tail_gap_older_than_fresh_window_is_classified_as_resume_backlog(self) -> None:
        self._insert_series(
            "backlog-show",
            title="Backlog Show",
            season_title="Backlog Show (English Dub)",
            season_number=1,
            watchlist_status="in_progress",
        )
        stale = (datetime.now(timezone.utc) - timedelta(days=23)).replace(microsecond=0)
        self._insert_progress("backlog-show", "b1", episode_number=1, completion_ratio=1.0, last_watched_at=stale.isoformat().replace("+00:00", "Z"))
        self._insert_progress(
            "backlog-show",
            "b2",
            episode_number=2,
            completion_ratio=0.2,
            last_watched_at=(stale + timedelta(hours=1)).isoformat().replace("+00:00", "Z"),
        )

        results = build_recommendations(self.config, limit=0)

        self.assertEqual(1, len(results))
        item = results[0]
        self.assertEqual("resume_backlog", item.kind)
        self.assertIn("backlog continuation", " ".join(item.reasons))
        self.assertEqual(1, item.context["contiguous_tail_gap"])

    def test_tail_gap_within_fresh_window_stays_fresh_dubbed_episode(self) -> None:
        self._insert_series(
            "fresh-show",
            title="Fresh Show",
            season_title="Fresh Show (English Dub)",
            season_number=1,
            watchlist_status="in_progress",
        )
        recent = (datetime.now(timezone.utc) - timedelta(days=21)).replace(microsecond=0)
        self._insert_progress("fresh-show", "f1", episode_number=1, completion_ratio=1.0, last_watched_at=recent.isoformat().replace("+00:00", "Z"))
        self._insert_progress(
            "fresh-show",
            "f2",
            episode_number=2,
            completion_ratio=0.2,
            last_watched_at=(recent + timedelta(hours=1)).isoformat().replace("+00:00", "Z"),
        )

        results = build_recommendations(self.config, limit=0)

        self.assertEqual(1, len(results))
        item = results[0]
        self.assertEqual("new_dubbed_episode", item.kind)
        self.assertEqual(1, item.context["contiguous_tail_gap"])

    def test_filters_out_non_english_dub_candidates(self) -> None:
        self._insert_series(
            "series-fr",
            title="Foreign Dub Show",
            season_title="Foreign Dub Show (French Dub)",
            season_number=1,
            watchlist_status="in_progress",
        )
        self._insert_progress("series-fr", "ep-1", episode_number=1, completion_ratio=1.0, last_watched_at="2026-03-10T01:00:00Z")
        self._insert_progress("series-fr", "ep-2", episode_number=2, completion_ratio=0.1, last_watched_at="2026-03-10T02:00:00Z")

        results = build_recommendations(self.config, limit=0)

        self.assertEqual([], results)

    def test_group_recommendations_splits_known_kinds_into_named_sections(self) -> None:
        grouped = group_recommendations(
            [
                Recommendation(
                    kind="resume_backlog",
                    priority=20,
                    provider_series_id="series-backlog",
                    title="Backlog Show",
                    season_title="Backlog Show (English Dub)",
                ),
                Recommendation(
                    kind="new_dubbed_episode",
                    priority=60,
                    provider_series_id="series-fresh",
                    title="Fresh Show",
                    season_title="Fresh Show (English Dub)",
                ),
                Recommendation(
                    kind="new_season",
                    priority=100,
                    provider_series_id="series-next",
                    title="Next Season Show",
                    season_title="Next Season Show Season 2 (English Dub)",
                ),
                Recommendation(
                    kind="discovery_candidate",
                    priority=50,
                    provider_series_id="mal:300",
                    title="Discovery Hit",
                    season_title=None,
                ),
            ]
        )

        self.assertEqual(
            ["continue_next", "fresh_dubbed_episodes", "discovery_candidates", "resume_backlog"],
            [section["key"] for section in grouped],
        )
        self.assertEqual("series-next", grouped[0]["items"][0]["provider_series_id"])
        self.assertEqual("series-fresh", grouped[1]["items"][0]["provider_series_id"])
        self.assertEqual("mal:300", grouped[2]["items"][0]["provider_series_id"])
        self.assertEqual("series-backlog", grouped[3]["items"][0]["provider_series_id"])

    def test_group_recommendations_keeps_unknown_kinds_under_other(self) -> None:
        grouped = group_recommendations(
            [
                Recommendation(
                    kind="mystery_lane",
                    priority=10,
                    provider_series_id="m1",
                    title="Mystery Show",
                    season_title=None,
                )
            ]
        )

        self.assertEqual(1, len(grouped))
        self.assertEqual("other", grouped[0]["key"])
        self.assertEqual(["mystery_lane"], grouped[0]["kinds"])
        self.assertEqual("m1", grouped[0]["items"][0]["provider_series_id"])

    def test_recommend_cli_defaults_to_grouped_output(self) -> None:
        self._insert_series(
            "series-next",
            title="Next Season Show",
            season_title="Next Season Show Season 2 (English Dub)",
            season_number=2,
            watchlist_status="available",
        )
        self._insert_series(
            "series-base",
            title="Next Season Show",
            season_title="Next Season Show (English Dub)",
            season_number=1,
            watchlist_status="fully_watched",
        )
        self._insert_progress(
            "series-base",
            "series-base-1",
            episode_number=1,
            completion_ratio=1.0,
            last_watched_at="2026-03-10T01:00:00Z",
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "recommend",
            "--limit",
            "1",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(["continue_next"], [section["key"] for section in payload])
        self.assertEqual("series-next", payload[0]["items"][0]["provider_series_id"])

    def test_recommend_cli_flat_flag_preserves_legacy_list_output(self) -> None:
        self._insert_series(
            "series-fresh",
            title="Fresh Show",
            season_title="Fresh Show (English Dub)",
            watchlist_status="available",
        )
        self._insert_progress(
            "series-fresh",
            "series-fresh-1",
            episode_number=1,
            completion_ratio=1.0,
            last_watched_at="2026-03-16T01:00:00Z",
        )
        self._insert_progress(
            "series-fresh",
            "series-fresh-2",
            episode_number=2,
            completion_ratio=0.0,
            last_watched_at="2026-03-17T01:00:00Z",
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "recommend",
            "--limit",
            "1",
            "--flat",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertIsInstance(payload, list)
        self.assertEqual("new_dubbed_episode", payload[0]["kind"])
        self.assertEqual("series-fresh", payload[0]["provider_series_id"])


if __name__ == "__main__":
    unittest.main()
