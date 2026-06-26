from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mal_updater.config import MalSecrets, load_config
from mal_updater.db import list_review_queue_entries, list_series_mappings, upsert_series_mapping
from mal_updater.ingestion import ingest_snapshot_payload
from mal_updater.mal_client import MalClient
from mal_updater.mapping import (
    SeriesMappingInput,
    build_search_queries,
    map_series,
    normalize_title,
    should_auto_approve_mapping,
)
from mal_updater.sync_planner import (
    MAPPING_REVIEW_HEURISTICS_REVISION,
    build_dry_run_sync_plan,
    build_mapping_review,
    execute_approved_sync,
    persist_mapping_review_queue,
    persist_sync_review_queue,
)
from tests.test_validation_ingestion import sample_snapshot


class MappingTests(unittest.TestCase):
    def test_normalize_title_strips_dub_and_season_noise(self) -> None:
        self.assertEqual(
            normalize_title("BOFURI: I Don’t Want to Get Hurt, so I’ll Max Out My Defense. Season 2 (English Dub)"),
            "bofuri i don t want to get hurt so i ll max out my defense",
        )

    def test_normalize_title_splits_letter_digit_boundaries(self) -> None:
        self.assertEqual(normalize_title("PERSONA5 the Animation"), "persona 5 the animation")
        self.assertEqual(normalize_title("Ver1.1a"), "ver 1 1 a")

    def test_map_series_does_not_treat_stylized_single_x_as_roman_installment_hint(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 30911,
                                "title": "Tales of Zestiria the Cross",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 34086,
                                "title": "Tales of Zestiria the Cross 2nd Season",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Tales of Zestiria the X",
                        season_title="Tales of Zestiria the X (English Dub)",
                        season_number=1,
                        max_episode_number=16,
                        completed_episode_count=16,
                    ),
                )

        self.assertEqual(result.chosen_candidate.mal_anime_id, 30911)
        self.assertFalse(any(reason.startswith("roman_installment_match=") for reason in result.rationale))
        self.assertFalse(any(reason.startswith("installment_hint_match=roman:") for reason in result.rationale))
        self.assertFalse(any(reason.startswith("roman_installment_match=") for reason in result.candidates[0].match_reasons))

    def test_map_series_flags_exact_title_overflow_as_possible_multi_entry_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 849,
                                "title": "Suzumiya Haruhi no Yuuutsu",
                                "alternative_titles": {"en": "The Melancholy of Haruhi Suzumiya", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 14,
                            }
                        },
                        {
                            "node": {
                                "id": 4382,
                                "title": "Suzumiya Haruhi no Yuuutsu (2009)",
                                "alternative_titles": {"en": "The Melancholy of Haruhi Suzumiya", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 14,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="The Melancholy of Haruhi Suzumiya",
                        season_title="The Melancholy of Haruhi Suzumiya (English Dub)",
                        season_number=1,
                        max_episode_number=28,
                        completed_episode_count=28,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(849, result.chosen_candidate.mal_anime_id)
        self.assertIn("exact_normalized_title", result.rationale)
        self.assertIn("episode_evidence_exceeds_candidate_count=28>14", result.rationale)
        self.assertIn("multi_entry_bundle_suspected=28<=14+14", result.rationale)
        self.assertIsNotNone(result.bundle_companion_candidate)
        self.assertEqual(4382, result.bundle_companion_candidate.mal_anime_id)
        self.assertEqual(1, len(result.bundle_companion_candidates or []))
        self.assertEqual({4382}, {candidate.mal_anime_id for candidate in (result.bundle_companion_candidates or [])})

    def test_map_series_flags_exact_title_overflow_as_bundle_even_when_later_season_companion_scores_low(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 20057,
                                "title": "Space☆Dandy",
                                "alternative_titles": {"en": "Space Dandy", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                        {
                            "node": {
                                "id": 2451,
                                "title": "Space Cobra",
                                "alternative_titles": {"en": "Space Cobra", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 31,
                            }
                        },
                        {
                            "node": {
                                "id": 12431,
                                "title": "Uchuu Kyoudai",
                                "alternative_titles": {"en": "Space Brothers", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 99,
                            }
                        },
                        {
                            "node": {
                                "id": 2452,
                                "title": "Space Adventure Cobra",
                                "alternative_titles": {"en": "Space Adventure Cobra", "synonyms": []},
                                "media_type": "movie",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                        {
                            "node": {
                                "id": 23327,
                                "title": "Space☆Dandy 2nd Season",
                                "alternative_titles": {"en": "Space Dandy 2nd Season", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-space-dandy",
                        title="Space Dandy",
                        season_title="Space Dandy (English Dub)",
                        season_number=1,
                        max_episode_number=21,
                        completed_episode_count=21,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 20057)
        self.assertIn("episode_evidence_exceeds_candidate_count=21>13", result.rationale)
        self.assertIn("multi_entry_bundle_suspected=21<=13+13", result.rationale)
        self.assertIsNotNone(result.bundle_companion_candidate)
        self.assertEqual(23327, result.bundle_companion_candidate.mal_anime_id)
        self.assertEqual({23327}, {candidate.mal_anime_id for candidate in (result.bundle_companion_candidates or [])})
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_flags_exact_title_overflow_as_possible_three_entry_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 1001,
                                "title": "Example Split Show",
                                "alternative_titles": {"en": "Example Split Show", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 1002,
                                "title": "Example Split Show Part 2",
                                "alternative_titles": {"en": "Example Split Show", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 1003,
                                "title": "Example Split Show Part 3",
                                "alternative_titles": {"en": "Example Split Show", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123b",
                        title="Example Split Show",
                        season_title="Example Split Show (English Dub)",
                        season_number=1,
                        max_episode_number=36,
                        completed_episode_count=36,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 1001)
        self.assertIn("episode_evidence_exceeds_candidate_count=36>12", result.rationale)
        self.assertIn("multi_entry_bundle_suspected=36<=12+12+12", result.rationale)
        self.assertIsNotNone(result.bundle_companion_candidate)
        self.assertIn(result.bundle_companion_candidate.mal_anime_id, {1002, 1003})
        self.assertEqual({1002, 1003}, {candidate.mal_anime_id for candidate in (result.bundle_companion_candidates or [])})
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_multi_entry_bundle_prefers_later_seasons_over_higher_scoring_sidecar_noise(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 39468,
                                "title": "Honzuki no Gekokujou: Shisho ni Naru Tame ni wa Shudan wo Erandeiraremasen",
                                "alternative_titles": {"en": "Ascendance of a Bookworm", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 14,
                            }
                        },
                        {
                            "node": {
                                "id": 40841,
                                "title": "Honzuki no Gekokujou: Shisho ni Naru Tame ni wa Shudan wo Erandeiraremasen OVA",
                                "alternative_titles": {"en": "Ascendance of a Bookworm OVA", "synonyms": []},
                                "media_type": "ova",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                        {
                            "node": {
                                "id": 42429,
                                "title": "Honzuki no Gekokujou: Shisho ni Naru Tame ni wa Shudan wo Erandeiraremasen 3rd Season",
                                "alternative_titles": {"en": "Ascendance of a Bookworm Season 3", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 10,
                            }
                        },
                        {
                            "node": {
                                "id": 40815,
                                "title": "Honzuki no Gekokujou: Shisho ni Naru Tame ni wa Shudan wo Erandeiraremasen 2nd Season",
                                "alternative_titles": {"en": "Ascendance of a Bookworm Season 2", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 51616,
                                "title": "Honzuki no Gekokujou: Shisho ni Naru Tame ni wa Shudan wo Erandeiraremasen Recap",
                                "alternative_titles": {"en": "Ascendance of a Bookworm Recap", "synonyms": []},
                                "media_type": "tv_special",
                                "status": "finished_airing",
                                "num_episodes": 2,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-bookworm",
                        title="Ascendance of a Bookworm",
                        season_title="Ascendance of a Bookworm (English Dub)",
                        season_number=1,
                        max_episode_number=32,
                        completed_episode_count=32,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 39468)
        self.assertIn("episode_evidence_exceeds_candidate_count=32>14", result.rationale)
        self.assertIn("multi_entry_bundle_suspected=32<=14+10+12", result.rationale)
        self.assertEqual({42429, 40815}, {candidate.mal_anime_id for candidate in (result.bundle_companion_candidates or [])})
        self.assertNotIn(40841, {candidate.mal_anime_id for candidate in (result.bundle_companion_candidates or [])})
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertGreater(
            next(candidate.score for candidate in result.candidates if candidate.mal_anime_id == 40841),
            next(candidate.score for candidate in result.candidates if candidate.mal_anime_id == 42429),
        )

    def test_map_series_flags_explicit_later_season_overflow_as_possible_multi_entry_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 58572,
                                "title": "Shangri-La Frontier: Kusoge Hunter, Kamige ni Idoman to su 2nd Season",
                                "alternative_titles": {"en": "Shangri-La Frontier Season 2", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 25,
                            }
                        },
                        {
                            "node": {
                                "id": 61338,
                                "title": "Shangri-La Frontier: Kusoge Hunter, Kamige ni Idoman to su 3rd Season",
                                "alternative_titles": {"en": "Shangri-La Frontier Season 3", "synonyms": []},
                                "media_type": "tv",
                                "status": "not_yet_aired",
                                "num_episodes": 25,
                            }
                        },
                        {
                            "node": {
                                "id": 52347,
                                "title": "Shangri-La Frontier: Kusoge Hunter, Kamige ni Idoman to su",
                                "alternative_titles": {"en": "Shangri-La Frontier", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 25,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-shangri-bundle",
                        title="Shangri-La Frontier",
                        season_title="Shangri-La Frontier Season 2 (English Dub)",
                        season_number=2,
                        max_episode_number=49,
                        completed_episode_count=49,
                    ),
                )

        self.assertEqual(result.status, "strong")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 58572)
        self.assertIn("season_number_match=2", result.rationale)
        self.assertIn("episode_evidence_exceeds_candidate_count=49>25", result.rationale)
        self.assertIn("multi_entry_bundle_suspected=49<=25+25", result.rationale)
        self.assertEqual({61338}, {candidate.mal_anime_id for candidate in (result.bundle_companion_candidates or [])})

    def test_map_series_boosts_base_title_match_when_provider_title_only_adds_arc_subtitle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            def fake_search(query: str, limit: int = 5) -> dict:
                if query == "One Piece":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 21,
                                    "title": "One Piece",
                                    "alternative_titles": {},
                                    "media_type": "tv",
                                    "status": "currently_airing",
                                    "num_episodes": 9999,
                                }
                            },
                            {
                                "node": {
                                    "id": 22,
                                    "title": "One Room",
                                    "alternative_titles": {},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 12,
                                }
                            },
                        ]
                    }
                return {"data": []}

            with patch.object(MalClient, "search_anime", side_effect=fake_search):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-arc",
                        title="One Piece: Egghead Arc (English Dub)",
                        max_episode_number=1122,
                        completed_episode_count=1120,
                    ),
                )

        self.assertEqual(result.status, "strong")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 21)
        self.assertIn("exact_base_title_after_subtitle_trim", result.rationale)
        self.assertFalse(should_auto_approve_mapping(result))

    def test_map_series_does_not_trim_installment_subtitle_into_false_base_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 42,
                                "title": "Attack on Titan",
                                "alternative_titles": {},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 25,
                            }
                        }
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-installment",
                        title="Attack on Titan: Season 2",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertNotIn("exact_base_title_after_subtitle_trim", result.rationale)
        self.assertNotEqual(result.status, "exact")

    def test_map_series_falls_back_to_base_title_for_pipe_or_dash_arc_subtitles(self) -> None:
        for title in (
            "One Piece | Egghead Arc (English Dub)",
            "One Piece — Egghead Arc (English Dub)",
            "One Piece – Egghead Arc (English Dub)",
        ):
            with self.subTest(title=title):
                with tempfile.TemporaryDirectory() as td:
                    root = Path(td)
                    (root / ".MAL-Updater" / "config").mkdir(parents=True)
                    config = load_config(root)
                    client = MalClient(
                        config,
                        MalSecrets(
                            client_id="client-id",
                            client_secret=None,
                            access_token="access-token",
                            refresh_token=None,
                            client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                            client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                            access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                            refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                        ),
                    )

                    def fake_search(query: str, limit: int = 5) -> dict:
                        if query == "One Piece":
                            return {
                                "data": [
                                    {
                                        "node": {
                                            "id": 21,
                                            "title": "One Piece",
                                            "alternative_titles": {},
                                            "media_type": "tv",
                                            "status": "currently_airing",
                                            "num_episodes": 9999,
                                        }
                                    }
                                ]
                            }
                        return {"data": []}

                    with patch.object(MalClient, "search_anime", side_effect=fake_search) as search_mock:
                        result = map_series(
                            client,
                            SeriesMappingInput(
                                provider="crunchyroll",
                                provider_series_id="series-arc-delimited",
                                title=title,
                                max_episode_number=1122,
                                completed_episode_count=1120,
                            ),
                        )

                attempted_queries = [call.args[0] for call in search_mock.call_args_list]
                self.assertIn("One Piece", attempted_queries)
                self.assertEqual(result.status, "strong")
                self.assertEqual(result.chosen_candidate.mal_anime_id, 21)
                self.assertIn("exact_base_title_after_subtitle_trim", result.rationale)

    def test_map_series_penalizes_related_non_tv_sidecar_when_provider_has_explicit_season_context(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            def fake_search(query: str, limit: int = 5) -> dict:
                if query == "Million Arthur Season 2 (English Dub)":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 38268,
                                    "title": "Hangyakusei Million Arthur 2nd Season",
                                    "alternative_titles": {},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 13,
                                }
                            }
                        ]
                    }
                if query == "Million Arthur":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 37555,
                                    "title": "Hangyakusei Million Arthur",
                                    "alternative_titles": {},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 10,
                                }
                            }
                        ]
                    }
                return {"data": []}

            def fake_details(anime_id: int, fields: str | None = None) -> dict:
                if anime_id == 38268:
                    return {
                        "id": 38268,
                        "title": "Hangyakusei Million Arthur 2nd Season",
                        "alternative_titles": {},
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 13,
                        "related_anime": [{"node": {"id": 30954}}],
                    }
                if anime_id == 37555:
                    return {
                        "id": 37555,
                        "title": "Hangyakusei Million Arthur",
                        "alternative_titles": {},
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 10,
                        "related_anime": [],
                    }
                if anime_id == 30954:
                    return {
                        "id": 30954,
                        "title": "Jakusansei Million Arthur",
                        "alternative_titles": {},
                        "media_type": "ona",
                        "status": "finished_airing",
                        "num_episodes": 10,
                        "related_anime": [],
                    }
                return {"id": anime_id, "related_anime": []}

            with (
                patch.object(MalClient, "search_anime", side_effect=fake_search),
                patch.object(MalClient, "get_anime_details", side_effect=fake_details),
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-million-arthur",
                        title="Million Arthur",
                        season_title="Million Arthur Season 2 (English Dub)",
                        season_number=2,
                        completed_episode_count=13,
                        max_episode_number=13,
                    ),
                )

        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 38268)
        candidates_by_id = {candidate.mal_anime_id: candidate for candidate in result.candidates}
        self.assertIn(30954, candidates_by_id)
        self.assertIn("ona_penalty_for_explicit_season_context", candidates_by_id[30954].match_reasons)
        self.assertGreater(candidates_by_id[38268].score, candidates_by_id[30954].score)

    def test_build_search_queries_combines_generic_season_title_with_base_title(self) -> None:
        queries = build_search_queries(
            SeriesMappingInput(
                provider="crunchyroll",
                provider_series_id="series-123",
                title="Campfire Cooking in Another World with My Absurd Skill",
                season_title="Season 2",
                season_number=2,
            )
        )

        self.assertEqual(queries[0:2], [
            "Season 2",
            "Campfire Cooking in Another World with My Absurd Skill Season 2",
        ])
        self.assertIn("Campfire Cooking in Another World with My Absurd Skill 2nd Season", queries)
        self.assertIn("Campfire Cooking in Another World with My Absurd Skill 2", queries)
        self.assertIn("Campfire Cooking in Another World with My Absurd Skill II", queries)
        self.assertEqual(queries[-1], "Campfire Cooking in Another World with My Absurd Skill")

    def test_build_search_queries_normalizes_missing_spacing_in_installment_markers(self) -> None:
        queries = build_search_queries(
            SeriesMappingInput(
                provider="crunchyroll",
                provider_series_id="series-123",
                title="The Saint's Magic Power is Omnipotent",
                season_title="The Saint's Magic Power is Omnipotent Season2 (English Dub)",
                season_number=2,
            )
        )

        self.assertEqual(queries[0:2], [
            "The Saint's Magic Power is Omnipotent Season2 (English Dub)",
            "The Saint's Magic Power is Omnipotent Season 2",
        ])
        self.assertIn("The Saint's Magic Power is Omnipotent 2nd Season", queries)
        self.assertIn("The Saint's Magic Power is Omnipotent 2", queries)
        self.assertIn("The Saint's Magic Power is Omnipotent II", queries)
        self.assertEqual(queries[-1], "The Saint's Magic Power is Omnipotent")

    def test_build_search_queries_strips_broadcast_and_uncensored_suffix_noise(self) -> None:
        queries = build_search_queries(
            SeriesMappingInput(
                provider="crunchyroll",
                provider_series_id="series-123",
                title="Harem in the Labyrinth of Another World",
                season_title="Harem in the Labyrinth of Another World - Broadcast Version (Uncensored)",
            )
        )

        self.assertEqual(
            queries[0:2],
            [
                "Harem in the Labyrinth of Another World - Broadcast Version (Uncensored)",
                "Harem in the Labyrinth of Another World",
            ],
        )
        self.assertEqual(queries[-1], "Harem in the Labyrinth of Another World")

    def test_map_series_boosts_parenthetical_english_alias_to_base_title_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 19685,
                                "title": "Kanojo ga Flag wo Oraretara",
                                "alternative_titles": {},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                        {
                            "node": {
                                "id": 24451,
                                "title": "Kanojo ga Flag wo Oraretara: Christmas? Sonna Mono ga Boku ni Tsuuyou Suru to Omou no ka?",
                                "alternative_titles": {},
                                "media_type": "ova",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-parenthetical-alias",
                        title="Kanojo ga Flag wo Oraretara (If Her Flag Breaks)",
                        season_title="Kanojo ga Flag wo Oraretara (If Her Flag Breaks)",
                        max_episode_number=13,
                        completed_episode_count=13,
                    ),
                )

        self.assertEqual(result.status, "strong")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 19685)
        self.assertIn("exact_base_title_after_subtitle_trim", result.rationale)
        self.assertFalse(should_auto_approve_mapping(result))

    def test_map_series_prefers_exact_specific_installment_over_base_title_tie(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            responses = {
                "Restaurant to Another World 2 (English Dub)": {
                    "data": [
                        {
                            "node": {
                                "id": 48804,
                                "title": "Isekai Shokudou 2",
                                "alternative_titles": {"en": "Restaurant to Another World 2"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
                "Restaurant to Another World": {
                    "data": [
                        {
                            "node": {
                                "id": 34012,
                                "title": "Isekai Shokudou",
                                "alternative_titles": {"en": "Restaurant to Another World"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            }

            with patch.object(MalClient, "search_anime", side_effect=lambda query, limit=5: responses.get(query, {"data": []})):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Restaurant to Another World",
                        season_title="Restaurant to Another World 2 (English Dub)",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 48804)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_uses_roman_query_variant_for_later_season_search(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            def fake_search(query: str, limit: int = 5) -> dict:
                if query == "Classroom of the Elite III":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 51180,
                                    "title": "Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e 3rd Season",
                                    "alternative_titles": {"en": "Classroom of the Elite III"},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 13,
                                }
                            },
                            {
                                "node": {
                                    "id": 51096,
                                    "title": "Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e 2nd Season",
                                    "alternative_titles": {"en": "Classroom of the Elite II"},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 13,
                                }
                            },
                        ]
                    }
                return {"data": []}

            with patch.object(MalClient, "search_anime", side_effect=fake_search):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Classroom of the Elite",
                        season_title="Classroom of the Elite Season 3 (English Dub)",
                        season_number=3,
                        max_episode_number=13,
                        completed_episode_count=13,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 51180)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_expands_related_anime_to_recover_hidden_tv_sequel(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            def fake_search(query: str, limit: int = 5) -> dict:
                if query == "My Wife is the Student Council President+! (Uncensored)":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 31980,
                                    "title": "Okusama ga Seitokaichou! Seitokaichou to Ofuro Asobi",
                                    "alternative_titles": {
                                        "synonyms": ["Okusama ga Seitokaichou! OVA"],
                                        "en": "My Wife is the Student Council President OVA",
                                        "ja": "",
                                    },
                                    "media_type": "ova",
                                    "status": "finished_airing",
                                    "num_episodes": 1,
                                }
                            },
                            {
                                "node": {
                                    "id": 5909,
                                    "title": "Seitokai no Ichizon",
                                    "alternative_titles": {},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 12,
                                }
                            },
                        ]
                    }
                return {"data": []}

            def fake_details(anime_id: int, *, fields: str = "") -> dict:
                if anime_id == 31980:
                    return {
                        "id": 31980,
                        "title": "Okusama ga Seitokaichou! Seitokaichou to Ofuro Asobi",
                        "alternative_titles": {
                            "synonyms": ["Okusama ga Seitokaichou! OVA"],
                            "en": "My Wife is the Student Council President OVA",
                            "ja": "",
                        },
                        "media_type": "ova",
                        "status": "finished_airing",
                        "num_episodes": 1,
                        "related_anime": [
                            {
                                "node": {"id": 28819, "title": "Okusama ga Seitokaichou!"},
                                "relation_type": "parent_story",
                                "relation_type_formatted": "Parent story",
                            }
                        ],
                    }
                if anime_id == 28819:
                    return {
                        "id": 28819,
                        "title": "Okusama ga Seitokaichou!",
                        "alternative_titles": {
                            "synonyms": ["Oku-sama ga Seito Kaichou!"],
                            "en": "My Wife is the Student Council President!",
                            "ja": "",
                        },
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 12,
                        "related_anime": [
                            {
                                "node": {"id": 32603, "title": "Okusama ga Seitokaichou!+!"},
                                "relation_type": "sequel",
                                "relation_type_formatted": "Sequel",
                            }
                        ],
                    }
                if anime_id == 32603:
                    return {
                        "id": 32603,
                        "title": "Okusama ga Seitokaichou!+!",
                        "alternative_titles": {
                            "synonyms": [
                                "My Wife is the Student Council President 2nd Season",
                                "Okusama ga Seitokaichou! Plus",
                            ],
                            "en": "My Wife is the Student Council President!+",
                            "ja": "",
                        },
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 12,
                        "related_anime": [],
                    }
                if anime_id == 5909:
                    return {
                        "id": 5909,
                        "title": "Seitokai no Ichizon",
                        "alternative_titles": {},
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 12,
                        "related_anime": [],
                    }
                raise AssertionError(f"unexpected anime details lookup: {anime_id}")

            with patch.object(MalClient, "search_anime", side_effect=fake_search), patch.object(
                MalClient,
                "get_anime_details",
                side_effect=fake_details,
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-related-expansion",
                        title="My Wife is the Student Council President",
                        season_title="My Wife is the Student Council President+! (Uncensored)",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 32603)
        self.assertIn("related_anime_expansion", result.chosen_candidate.match_reasons)
        self.assertIn("installment_hint_match=plus", result.chosen_candidate.match_reasons)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_expands_related_anime_for_suffix_residue_without_installment_context(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            def fake_search(query: str, limit: int = 5) -> dict:
                if query == "Shuffle! (English Dub)":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 1836,
                                    "title": "Shuffle! Memories",
                                    "alternative_titles": {},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 12,
                                }
                            }
                        ]
                    }
                return {"data": []}

            def fake_details(anime_id: int, *, fields: str = "") -> dict:
                if anime_id == 1836:
                    return {
                        "id": 1836,
                        "title": "Shuffle! Memories",
                        "alternative_titles": {},
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 12,
                        "related_anime": [
                            {
                                "node": {"id": 79, "title": "Shuffle!"},
                                "relation_type": "prequel",
                                "relation_type_formatted": "Prequel",
                            }
                        ],
                    }
                if anime_id == 79:
                    return {
                        "id": 79,
                        "title": "Shuffle!",
                        "alternative_titles": {"en": "Shuffle!", "synonyms": [], "ja": ""},
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 24,
                        "related_anime": [],
                    }
                raise AssertionError(f"unexpected anime details lookup: {anime_id}")

            with patch.object(MalClient, "search_anime", side_effect=fake_search), patch.object(
                MalClient,
                "get_anime_details",
                side_effect=fake_details,
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-shuffle",
                        title="Shuffle!",
                        season_title="Shuffle! (English Dub)",
                        season_number=1,
                        max_episode_number=8,
                        completed_episode_count=8,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 79)
        self.assertIn("related_anime_expansion", result.chosen_candidate.match_reasons)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_prioritizes_promising_relation_chains_before_low_value_siblings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            def fake_search(query: str, limit: int = 5) -> dict:
                if query == "Seven Mortal Sins (English Dub)":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 35418,
                                    "title": "Sin: Nanatsu no Taizai Zange-roku Specials",
                                    "alternative_titles": {"en": "Seven Mortal Sins Specials", "synonyms": [], "ja": ""},
                                    "media_type": "special",
                                    "status": "finished_airing",
                                    "num_episodes": 7,
                                }
                            },
                            {
                                "node": {
                                    "id": 23755,
                                    "title": "Nanatsu no Taizai",
                                    "alternative_titles": {"en": "The Seven Deadly Sins", "synonyms": [], "ja": ""},
                                    "media_type": "tv",
                                    "status": "finished_airing",
                                    "num_episodes": 24,
                                }
                            },
                        ]
                    }
                return {"data": []}

            def fake_details(anime_id: int, *, fields: str = "") -> dict:
                if anime_id == 35418:
                    return {
                        "id": 35418,
                        "title": "Sin: Nanatsu no Taizai Zange-roku Specials",
                        "alternative_titles": {"en": "Seven Mortal Sins Specials", "synonyms": [], "ja": ""},
                        "media_type": "special",
                        "status": "finished_airing",
                        "num_episodes": 7,
                        "related_anime": [
                            {
                                "node": {"id": 35417, "title": "Sin: Nanatsu no Taizai Zange-roku"},
                                "relation_type": "prequel",
                                "relation_type_formatted": "Prequel",
                            }
                        ],
                    }
                if anime_id == 35417:
                    return {
                        "id": 35417,
                        "title": "Sin: Nanatsu no Taizai Zange-roku",
                        "alternative_titles": {"en": "", "synonyms": [], "ja": ""},
                        "media_type": "ona",
                        "status": "finished_airing",
                        "num_episodes": 12,
                        "related_anime": [
                            {
                                "node": {"id": 33834, "title": "Sin: Nanatsu no Taizai"},
                                "relation_type": "other",
                                "relation_type_formatted": "Other",
                            }
                        ],
                    }
                if anime_id == 33834:
                    return {
                        "id": 33834,
                        "title": "Sin: Nanatsu no Taizai",
                        "alternative_titles": {"en": "Seven Mortal Sins", "synonyms": [], "ja": ""},
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 12,
                        "related_anime": [],
                    }
                if anime_id == 23755:
                    return {
                        "id": 23755,
                        "title": "Nanatsu no Taizai",
                        "alternative_titles": {"en": "The Seven Deadly Sins", "synonyms": [], "ja": ""},
                        "media_type": "tv",
                        "status": "finished_airing",
                        "num_episodes": 24,
                        "related_anime": [
                            {"node": {"id": 30347, "title": "Nanatsu no Taizai OVA"}},
                            {"node": {"id": 31722, "title": "Nanatsu no Taizai: Seisen no Shirushi"}},
                            {"node": {"id": 36923, "title": "Nanatsu no Taizai: Imashime no Fukkatsu Joshou"}},
                        ],
                    }
                if anime_id in {30347, 31722, 36923}:
                    return {
                        "id": anime_id,
                        "title": f"noise-{anime_id}",
                        "alternative_titles": {},
                        "media_type": "ova",
                        "status": "finished_airing",
                        "num_episodes": 1,
                        "related_anime": [],
                    }
                raise AssertionError(f"unexpected anime details lookup: {anime_id}")

            with patch.object(MalClient, "search_anime", side_effect=fake_search), patch.object(
                MalClient,
                "get_anime_details",
                side_effect=fake_details,
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-seven-mortal-sins",
                        title="Seven Mortal Sins",
                        season_title="Seven Mortal Sins (English Dub)",
                        season_number=1,
                        max_episode_number=7,
                        completed_episode_count=7,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 33834)
        self.assertIn("related_anime_expansion", result.chosen_candidate.match_reasons)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_does_not_expand_relations_for_plain_season_one_tv_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 37555,
                                "title": "Hangyakusei Million Arthur",
                                "alternative_titles": {"en": "Million Arthur", "synonyms": [], "ja": ""},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 10,
                            }
                        }
                    ]
                },
            ), patch.object(MalClient, "get_anime_details", side_effect=AssertionError("relation expansion should not run")):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-million-arthur",
                        title="Million Arthur",
                        season_title="Million Arthur Season 1 (English Dub)",
                        season_number=1,
                        max_episode_number=7,
                        completed_episode_count=7,
                    ),
                )

        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 37555)
        self.assertNotIn("related_anime_expansion", result.chosen_candidate.match_reasons)

    def test_map_series_classifies_exact_match_conservatively(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 42,
                                "title": "Attack on Titan Final Season",
                                "alternative_titles": {"synonyms": ["Attack on Titan Final Season (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 16,
                            }
                        },
                        {"node": {"id": 99, "title": "Random Other Show", "alternative_titles": {}, "media_type": "tv"}},
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Attack on Titan",
                        season_title="Attack on Titan Final Season (English Dub)",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 42)

    def test_map_series_uses_season_and_episode_evidence_to_avoid_wrong_sequel(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 100,
                                "title": "Example Show Season 1",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 200,
                                "title": "Example Show Season 2",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show Season 2",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertIsNotNone(result.chosen_candidate)
        self.assertEqual(result.chosen_candidate.mal_anime_id, 200)
        self.assertTrue(any("season_number_match=2" == reason for reason in result.rationale))

    def test_map_series_penalizes_candidate_with_extra_installment_hint_when_provider_has_none(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 666,
                                "title": "JoJo no Kimyou na Bouken",
                                "alternative_titles": {"en": "JoJo's Bizarre Adventure"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 26,
                            }
                        },
                        {
                            "node": {
                                "id": 20899,
                                "title": "JoJo no Kimyou na Bouken Part 3: Stardust Crusaders",
                                "alternative_titles": {"en": "JoJo's Bizarre Adventure: Stardust Crusaders"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 24,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="JoJo's Bizarre Adventure",
                        season_title="JoJo's Bizarre Adventure",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 666)
        self.assertIn("candidate_extra_installment_hint", result.candidates[1].match_reasons)

    def test_should_auto_approve_exact_unique_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 200,
                                "title": "Example Show Season 2",
                                "alternative_titles": {"synonyms": ["Example Show Season 2 (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 100,
                                "title": "Different Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show Season 2 (English Dub)",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_penalizes_auxiliary_candidates_even_with_exact_title(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 28677,
                                "title": "Yamada-kun to 7-nin no Majo",
                                "alternative_titles": {"en": "Yamada-kun and the Seven Witches"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 20359,
                                "title": "Yamada-kun to 7-nin no Majo PV",
                                "alternative_titles": {"en": "Yamada-kun and the Seven Witches"},
                                "media_type": "special",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Yamada-kun and the Seven Witches",
                        season_title="Yamada-kun and the Seven Witches",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 28677)
        self.assertIn("candidate_auxiliary_content=pv", result.candidates[1].match_reasons)

    def test_map_series_promotes_exact_tv_match_over_near_single_episode_ova_review_noise(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 28677,
                                "title": "Yamada-kun to 7-nin no Majo",
                                "alternative_titles": {"en": "Yamada-kun and the Seven Witches"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 24627,
                                "title": "Yamada-kun to 7-nin no Majo: Mou Hitotsu no Suzaku-sai",
                                "alternative_titles": {"en": "Yamada-kun and the Seven Witches: Another Suzaku Festival"},
                                "media_type": "ova",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-ova-noise",
                        title="Yamada-kun and the Seven Witches",
                        season_title="Yamada-kun and the Seven Witches",
                        completed_episode_count=12,
                        max_episode_number=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 28677)
        self.assertIn("substring_title_match", result.candidates[1].match_reasons)
        self.assertIn("episode_evidence_exceeds_candidate_count=12>1", result.candidates[1].match_reasons)

    def test_map_series_promotes_exact_tv_match_over_near_extra_suffix_franchise_entry_without_episode_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 28677,
                                "title": "Yamada-kun to 7-nin no Majo",
                                "alternative_titles": {"en": "Yamada-kun and the Seven Witches"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": None,
                            }
                        },
                        {
                            "node": {
                                "id": 24627,
                                "title": "Yamada-kun to 7-nin no Majo: Mou Hitotsu no Suzaku-sai",
                                "alternative_titles": {"en": "Yamada-kun and the Seven Witches: Another Suzaku Festival"},
                                "media_type": "ova",
                                "status": "finished_airing",
                                "num_episodes": None,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-ova-suffix-noise",
                        title="Yamada-kun and the Seven Witches",
                        season_title="Yamada-kun and the Seven Witches",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 28677)
        self.assertIn("candidate_extra_title_suffix", result.candidates[1].match_reasons)

    def test_map_series_promotes_exact_base_series_over_sequel_suffix_variant(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 38297,
                                "title": "Maou-sama, Retry!",
                                "alternative_titles": {"en": "Demon Lord, Retry!"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": None,
                            }
                        },
                        {
                            "node": {
                                "id": 56400,
                                "title": "Maou-sama, Retry! R",
                                "alternative_titles": {"en": "Demon Lord, Retry! R"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": None,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-retry-base",
                        title="Demon Lord, Retry! (English Dub)",
                        season_title="Demon Lord, Retry! (English Dub)",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 38297)
        self.assertIn("candidate_extra_title_suffix", result.candidates[1].match_reasons)

    def test_map_series_promotes_exact_base_series_over_non_exact_tv_suffix_variants(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 6213,
                                "title": "Toaru Kagaku no Railgun",
                                "alternative_titles": {"en": "A Certain Scientific Railgun"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 24,
                            }
                        },
                        {
                            "node": {
                                "id": 16049,
                                "title": "Toaru Kagaku no Railgun S",
                                "alternative_titles": {"en": "A Certain Scientific Railgun S"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 24,
                            }
                        },
                        {
                            "node": {
                                "id": 38481,
                                "title": "Toaru Kagaku no Railgun T",
                                "alternative_titles": {"en": "A Certain Scientific Railgun T"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 25,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-railgun-base",
                        title="A Certain Scientific Railgun (English Dub)",
                        season_title="A Certain Scientific Railgun (English Dub)",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 6213)
        self.assertIn("candidate_extra_title_suffix", result.candidates[1].match_reasons)
        self.assertNotIn("exact_normalized_title", result.candidates[1].match_reasons)

    def test_map_series_promotes_exact_tv_match_over_tv_special_when_title_only_differs_by_digit_spacing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 36023,
                                "title": "Persona 5 the Animation",
                                "alternative_titles": {},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": None,
                            }
                        },
                        {
                            "node": {
                                "id": 38431,
                                "title": "Persona 5 the Animation TV Specials",
                                "alternative_titles": {},
                                "media_type": "tv_special",
                                "status": "finished_airing",
                                "num_episodes": None,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-persona5",
                        title="PERSONA5 the Animation",
                        season_title="PERSONA5 the Animation",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 36023)
        self.assertIn("exact_normalized_title", result.chosen_candidate.match_reasons)
        self.assertIn("candidate_extra_title_suffix", result.candidates[1].match_reasons)

    def test_map_series_promotes_exact_tv_match_over_non_exact_ona_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 34257,
                                "title": "Cinderella Girls Gekijou",
                                "alternative_titles": {"en": "The iDOLM@STER CINDERELLA GIRLS Theater"},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                        {
                            "node": {
                                "id": 35346,
                                "title": "Cinderella Girls Gekijou: Kayou Cinderella Theater",
                                "alternative_titles": {},
                                "media_type": "ona",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-cingeki",
                        title="The iDOLM@STER CINDERELLA GIRLS Theater",
                        season_title="THE iDOLM@STER CINDERELLA GIRLS Theater 1st and 2nd Seasons (TV)",
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertTrue(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 34257)
        self.assertEqual(result.candidates[1].media_type, "ona")
        self.assertNotIn("exact_normalized_title", result.candidates[1].match_reasons)

    def test_map_series_does_not_promote_exact_ova_match_over_base_tv_series(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 666,
                                "title": "JoJo no Kimyou na Bouken",
                                "alternative_titles": {"en": "JoJo's Bizarre Adventure"},
                                "media_type": "ova",
                                "status": "finished_airing",
                                "num_episodes": 6,
                            }
                        },
                        {
                            "node": {
                                "id": 14719,
                                "title": "JoJo no Kimyou na Bouken (TV)",
                                "alternative_titles": {},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 26,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-jojo-ova",
                        title="JoJo's Bizarre Adventure",
                        season_title="JoJo's Bizarre Adventure",
                        completed_episode_count=26,
                        max_episode_number=26,
                    ),
                )

        self.assertEqual(result.status, "ambiguous")
        self.assertFalse(should_auto_approve_mapping(result))
        self.assertEqual(result.chosen_candidate.mal_anime_id, 666)

    def test_should_not_auto_approve_when_season_evidence_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 100,
                                "title": "Example Show Season 1",
                                "alternative_titles": {"synonyms": ["Example Show Season 2 (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 200,
                                "title": "Another Different Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show Season 2 (English Dub)",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertFalse(should_auto_approve_mapping(result))

    def test_map_series_combined_generic_season_query_promotes_safe_exact_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            def fake_search(query: str, limit: int = 5) -> dict[str, object]:
                if query == "Campfire Cooking in Another World with My Absurd Skill Season 2":
                    return {
                        "data": [
                            {
                                "node": {
                                    "id": 500,
                                    "title": "Campfire Cooking in Another World with My Absurd Skill Season 2",
                                    "alternative_titles": {"synonyms": []},
                                    "media_type": "tv",
                                    "status": "currently_airing",
                                    "num_episodes": 12,
                                }
                            }
                        ]
                    }
                return {"data": []}

            with patch.object(MalClient, "search_anime", side_effect=fake_search):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Campfire Cooking in Another World with My Absurd Skill",
                        season_title="Season 2",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 500)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_uses_roman_installment_hint_to_break_tie(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 300,
                                "title": "A Certain Magical Index II",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 24,
                            }
                        },
                        {
                            "node": {
                                "id": 400,
                                "title": "A Certain Magical Index III",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 26,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="A Certain Magical Index",
                        season_title="A Certain Magical Index III (English Dub)",
                        season_number=3,
                        max_episode_number=26,
                        completed_episode_count=26,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 400)
        self.assertIn("roman_installment_match=roman:3", result.rationale)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_build_search_queries_combines_generic_cour_title_with_base_title(self) -> None:
        queries = build_search_queries(
            SeriesMappingInput(
                provider="crunchyroll",
                provider_series_id="series-123",
                title="Example Show",
                season_title="2nd Cour",
                season_number=1,
            )
        )

        self.assertEqual(
            queries,
            [
                "2nd Cour",
                "Example Show 2nd Cour",
                "Example Show",
            ],
        )

    def test_map_series_uses_split_installment_match_for_part_vs_cour(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 500,
                                "title": "Example Show Final Season Part 1",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 600,
                                "title": "Example Show The Final Season 2nd Cour",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show Final Season Part 2 (English Dub)",
                        season_number=4,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.chosen_candidate.mal_anime_id, 600)
        self.assertIn("split_installment_match=split:2", result.rationale)

    def test_map_series_softens_aggregate_episode_numbering_when_installment_and_completion_evidence_align(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 700,
                                "title": "Example Show Season 2",
                                "alternative_titles": {"synonyms": ["Example Show Season 2 (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                        {
                            "node": {
                                "id": 600,
                                "title": "Example Show Season 1",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show Season 2 (English Dub)",
                        season_number=2,
                        max_episode_number=25,
                        completed_episode_count=13,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 700)
        self.assertTrue(any(reason == "aggregated_episode_numbering_suspected=25>13" for reason in result.rationale))
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_prefers_part_two_candidate_for_aggregated_second_season(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 59193,
                                "title": "Mushoku Tensei III: Isekai Ittara Honki Dasu",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "currently_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 45576,
                                "title": "Mushoku Tensei: Isekai Ittara Honki Dasu Part 2",
                                "alternative_titles": {"synonyms": ["Mushoku Tensei: Jobless Reincarnation Part 2"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 39535,
                                "title": "Mushoku Tensei: Isekai Ittara Honki Dasu",
                                "alternative_titles": {"synonyms": ["Mushoku Tensei: Jobless Reincarnation"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 11,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Mushoku Tensei: Jobless Reincarnation",
                        season_title="Mushoku Tensei: Jobless Reincarnation Season 2",
                        season_number=2,
                        max_episode_number=24,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 45576)
        self.assertIn("season_to_split_match=part:2,split:2", result.rationale)
        self.assertTrue(any(reason == "aggregated_episode_numbering_suspected=24>12" for reason in result.rationale))
        self.assertNotIn("episode_evidence_exceeds_candidate_count=24>12", result.rationale)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_prefers_split_specific_candidate_over_broader_same_season_tie(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 53200,
                                "title": "Hataraku Maou-sama!! 2nd Season",
                                "alternative_titles": {"synonyms": ["The Devil is a Part-Timer! Season 2 Part 2 (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 48413,
                                "title": "Hataraku Maou-sama!!",
                                "alternative_titles": {"synonyms": ["The Devil is a Part-Timer! Season 2 (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 15809,
                                "title": "Hataraku Maou-sama!",
                                "alternative_titles": {"synonyms": ["The Devil is a Part-Timer! (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-devil-part-timer",
                        title="The Devil is a Part-Timer!",
                        season_title="The Devil is a Part-Timer! Season 2 Part 2 (English Dub)",
                        season_number=2,
                        max_episode_number=13,
                        completed_episode_count=13,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 53200)
        self.assertIn("season_to_split_match=part:2,split:2", result.rationale)
        second = result.candidates[1]
        self.assertEqual(second.mal_anime_id, 48413)
        self.assertIn("season_number_match=2", second.match_reasons)
        self.assertFalse(any(reason.startswith("season_to_split_match=") for reason in second.match_reasons))
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_softens_single_episode_overflow_when_later_season_hint_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 44037,
                                "title": "Shin no Nakama ja Nai to Yuusha no Party wo Oidasareta node, Henkyou de Slow Life suru Koto ni Shimashita",
                                "alternative_titles": {
                                    "en": "Banished from the Hero's Party, I Decided to Live a Quiet Life in the Countryside"
                                },
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                        {
                            "node": {
                                "id": 53488,
                                "title": "Shin no Nakama ja Nai to Yuusha no Party wo Oidasareta node, Henkyou de Slow Life suru Koto ni Shimashita 2nd",
                                "alternative_titles": {
                                    "en": "Banished from the Hero's Party, I Decided to Live a Quiet Life in the Countryside Season 2"
                                },
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Banished from the Hero's Party, I Decided to Live a Quiet Life in the Countryside",
                        season_title="Banished from the Hero's Party, I Decided to Live a Quiet Life in the Countryside Season2 (English Dub)",
                        season_number=2,
                        max_episode_number=13,
                        completed_episode_count=13,
                        max_completed_episode_number=13,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 53488)
        self.assertIn("season_number_match=2", result.rationale)
        self.assertTrue(any(reason == "minor_episode_overflow_suspected=13>12" for reason in result.rationale))
        self.assertNotIn("episode_evidence_exceeds_candidate_count=13>12", result.rationale)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_softens_single_episode_overflow_for_exact_base_title_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 6880,
                                "title": "Deadman Wonderland",
                                "alternative_titles": {"en": "Deadman Wonderland", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 10372,
                                "title": "Deadman Wonderland: Akai Knife Tsukai",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "ova",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Deadman Wonderland",
                        season_title="Deadman Wonderland (English Dub)",
                        season_number=1,
                        max_episode_number=13,
                        completed_episode_count=13,
                        max_completed_episode_number=13,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 6880)
        self.assertIn("exact_normalized_title", result.rationale)
        self.assertIn("minor_episode_overflow_suspected=13>12", result.rationale)
        self.assertNotIn("episode_evidence_exceeds_candidate_count=13>12", result.rationale)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_penalizes_base_installment_candidate_when_provider_explicitly_targets_later_season(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 710,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 711,
                                "title": "Example Show 2nd Season",
                                "alternative_titles": {"en": "Example Show Season 2", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show Season 2 (English Dub)",
                        season_number=2,
                        max_episode_number=12,
                        completed_episode_count=12,
                        max_completed_episode_number=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 711)
        self.assertIn("season_number_match=2", result.rationale)
        weaker = next(candidate for candidate in result.candidates if candidate.mal_anime_id == 710)
        self.assertIn("base_installment_penalty_for_explicit_later_season", weaker.match_reasons)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_penalizes_single_special_when_provider_looks_like_multi_episode_main_series(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 710,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 711,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "special",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show",
                        season_number=1,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.chosen_candidate.mal_anime_id, 710)
        self.assertIn("special_penalty_for_multi_episode_series", result.candidates[1].match_reasons)

    def test_map_series_prefers_title_season_hint_when_provider_metadata_is_noisy(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 700,
                                "title": "Example Show Season 2",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 800,
                                "title": "Example Show Season 3",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Example Show",
                        season_title="Example Show Season 2",
                        season_number=3,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.chosen_candidate.mal_anime_id, 700)
        self.assertIn("provider_season_metadata_conflict=metadata:3;title:2", result.rationale)

    def test_map_series_does_not_penalize_exact_movie_title_inside_collection(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 900,
                                "title": "Dragon Ball Super: Super Hero",
                                "alternative_titles": {"synonyms": ["Dragon Ball Super: Super Hero (English Dub)"]},
                                "media_type": "movie",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        }
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-123",
                        title="Dragon Ball Movies",
                        season_title="Dragon Ball Super: Super Hero (English Dub)",
                        season_number=2115,
                        max_episode_number=1,
                        completed_episode_count=1,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 900)
        self.assertIn("movie_type_allowed_for_exact_title", result.rationale)

    def test_map_series_prefers_tv_bundle_over_exact_movie_and_prologue_sidecars_for_multi_episode_series(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 6922,
                                "title": "Fate/stay night Movie: Unlimited Blade Works",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "movie",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                        {
                            "node": {
                                "id": 22297,
                                "title": "Fate/stay night: Unlimited Blade Works",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 27821,
                                "title": "Fate/stay night: Unlimited Blade Works Prologue",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv_special",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                        {
                            "node": {
                                "id": 28701,
                                "title": "Fate/stay night: Unlimited Blade Works 2nd Season",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 13,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-fate-ubw",
                        title="Fate/stay night [Unlimited Blade Works]",
                        season_title="Fate/stay night [Unlimited Blade Works] (English Dub)",
                        season_number=1,
                        max_episode_number=24,
                        completed_episode_count=24,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(22297, result.chosen_candidate.mal_anime_id)
        self.assertIn("multi_entry_bundle_suspected=24<=12+13", result.rationale)
        self.assertEqual({28701}, {candidate.mal_anime_id for candidate in (result.bundle_companion_candidates or [])})
        self.assertTrue(should_auto_approve_mapping(result))
        movie_candidate = next(candidate for candidate in result.candidates if candidate.mal_anime_id == 6922)
        prologue_candidate = next(candidate for candidate in result.candidates if candidate.mal_anime_id == 27821)
        self.assertIn("single_episode_movie_penalty_for_multi_episode_series", movie_candidate.match_reasons)
        self.assertIn("movie_penalty", movie_candidate.match_reasons)
        self.assertIn("single_episode_tv_special_penalty_for_multi_episode_series", prologue_candidate.match_reasons)
        self.assertLess(movie_candidate.score, result.chosen_candidate.score)
        self.assertLess(prologue_candidate.score, result.chosen_candidate.score)

    def test_map_series_uses_supplemental_title_candidate_for_unsearchable_exact_title(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(MalClient, "search_anime", return_value={"data": []}), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 40708,
                    "title": "Monster Musume no Oishasan",
                    "alternative_titles": {"en": "Monster Girl Doctor", "synonyms": [], "ja": "モンスター娘のお医者さん"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 12,
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-monster-girl-doctor",
                        title="Monster Girl Doctor",
                        season_title="Monster Girl Doctor (English Dub)",
                        season_number=1,
                        max_episode_number=12,
                        completed_episode_count=12,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 40708)
        self.assertIn("supplemental_title_candidate", result.rationale)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_uses_supplemental_bundle_candidates_for_girls_bravo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            details = {
                241: {
                    "id": 241,
                    "title": "Girls Bravo: First Season",
                    "alternative_titles": {"en": "Girls Bravo", "synonyms": [], "ja": "GIRLSブラボー first season"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 11,
                },
                487: {
                    "id": 487,
                    "title": "Girls Bravo: Second Season",
                    "alternative_titles": {"en": "Girls Bravo: Second Season", "synonyms": [], "ja": "GIRLSブラボー second season"},
                    "media_type": "tv",
                    "status": "finished_airing",
                    "num_episodes": 13,
                },
            }

            with patch.object(MalClient, "search_anime", return_value={"data": []}), patch.object(
                MalClient,
                "get_anime_details",
                side_effect=lambda anime_id, fields=None: details[anime_id],
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-girls-bravo",
                        title="Girls Bravo",
                        season_title="Girls Bravo",
                        season_number=1,
                        max_episode_number=24,
                        completed_episode_count=24,
                    ),
                )

        self.assertEqual(result.status, "strong")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 241)
        self.assertEqual([], result.bundle_companion_candidates or [])
        self.assertFalse(should_auto_approve_mapping(result))

    def test_map_series_auto_approves_exact_later_installment_when_base_title_is_aggregated_noise(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 48761,
                                "title": "Saihate no Paladin",
                                "alternative_titles": {"en": "The Faraway Paladin", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 50664,
                                "title": "Saihate no Paladin: Tetsusabi no Yama no Ou",
                                "alternative_titles": {"en": "The Faraway Paladin: The Lord of the Rust Mountains", "synonyms": ["Saihate no Paladin 2nd Season"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-faraway-paladin-rust-mountains",
                        title="The Faraway Paladin",
                        season_title="The Faraway Paladin The Lord Of The Rust Mountains (English Dub)",
                        season_number=2,
                        max_episode_number=13,
                        completed_episode_count=13,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 50664)
        self.assertIn("exact_later_installment_alignment", result.rationale)
        self.assertTrue(should_auto_approve_mapping(result))

    def test_map_series_auto_approves_exact_single_movie_feature(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            client = MalClient(
                config,
                MalSecrets(
                    client_id="client-id",
                    client_secret=None,
                    access_token="access-token",
                    refresh_token=None,
                    client_id_path=root / ".MAL-Updater" / "secrets" / "mal_client_id.txt",
                    client_secret_path=root / ".MAL-Updater" / "secrets" / "mal_client_secret.txt",
                    access_token_path=root / ".MAL-Updater" / "secrets" / "mal_access_token.txt",
                    refresh_token_path=root / ".MAL-Updater" / "secrets" / "mal_refresh_token.txt",
                ),
            )

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 48561,
                                "title": "Jujutsu Kaisen 0 Movie",
                                "alternative_titles": {"en": "Jujutsu Kaisen 0", "synonyms": ["JJK 0"]},
                                "media_type": "movie",
                                "status": "finished_airing",
                                "num_episodes": 1,
                            }
                        },
                        {
                            "node": {
                                "id": 40748,
                                "title": "Jujutsu Kaisen",
                                "alternative_titles": {"en": "Jujutsu Kaisen", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 24,
                            }
                        },
                    ]
                },
            ):
                result = map_series(
                    client,
                    SeriesMappingInput(
                        provider="crunchyroll",
                        provider_series_id="series-jjk-zero",
                        title="JUJUTSU KAISEN 0",
                        season_title="JUJUTSU KAISEN 0",
                        season_number=0,
                        max_episode_number=1,
                        completed_episode_count=1,
                    ),
                )

        self.assertEqual(result.status, "exact")
        self.assertEqual(result.chosen_candidate.mal_anime_id, 48561)
        self.assertTrue(should_auto_approve_mapping(result))


class PersistedMappingTests(unittest.TestCase):
    def test_upsert_and_list_series_mappings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            ingest_snapshot_payload(payload, config)

            created = upsert_series_mapping(
                config.db_path,
                provider="crunchyroll",
                provider_series_id="series-123",
                mal_anime_id=321,
                confidence=0.99,
                mapping_source="user_approved",
                approved_by_user=True,
                notes="looked correct",
            )
            items = list_series_mappings(config.db_path, provider="crunchyroll", approved_only=True)

        self.assertEqual(created.mal_anime_id, 321)
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0].approved_by_user)
        self.assertEqual(items[0].notes, "looked correct")


class DryRunPlannerTests(unittest.TestCase):
    def test_build_dry_run_sync_plan_proposes_forward_only_update(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["series"][0]["title"] = "Example Show"
            payload["series"][0]["season_title"] = "Example Show (English Dub)"
            payload["progress"][0]["episode_number"] = 3
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": ["Example Show (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 1},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(len(proposals), 1)
        proposal = proposals[0]
        self.assertEqual(proposal.decision, "propose_update")
        self.assertEqual(proposal.proposed_my_list_status, {"status": "watching", "num_watched_episodes": 3})
        self.assertEqual(proposal.mapping_source, "auto_exact")
        self.assertTrue(proposal.persisted_mapping_approved)
        self.assertIn("preserve_meaningful_score", proposal.reasons)

    def test_build_dry_run_sync_plan_refuses_to_decrease_existing_progress(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 5},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "skip")
        self.assertTrue(any("refusing_to_decrease_mal_progress" in reason for reason in proposals[0].reasons))

    def test_build_mapping_review_preserves_user_approved_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
            upsert_series_mapping(
                config.db_path,
                provider="crunchyroll",
                provider_series_id="series-123",
                mal_anime_id=777,
                confidence=1.0,
                mapping_source="user_approved",
                approved_by_user=True,
                notes="manual approval",
            )

            with patch.object(MalClient, "search_anime", side_effect=AssertionError("should not search approved mapping")):
                items = build_mapping_review(config, limit=5, mapping_limit=3)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].decision, "preserved")
        self.assertEqual(items[0].suggested_mal_anime_id, 777)
        self.assertEqual(items[0].mapping_status, "approved")

    def test_build_mapping_review_auto_approves_exact_unique_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["series"][0]["title"] = "Example Show"
            payload["series"][0]["season_title"] = "Example Show Season 2 (English Dub)"
            payload["series"][0]["season_number"] = 2
            payload["progress"][0]["episode_number"] = 12
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 222,
                                "title": "Example Show Season 2",
                                "alternative_titles": {"synonyms": ["Example Show Season 2 (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {"node": {"id": 999, "title": "Different Show", "alternative_titles": {}, "media_type": "tv"}},
                    ]
                },
            ):
                items = build_mapping_review(config, limit=5, mapping_limit=3)
                persisted = list_series_mappings(config.db_path, provider="crunchyroll", approved_only=True)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].decision, "auto_approved")
        self.assertEqual(items[0].mapping_status, "approved")
        self.assertTrue(any(reason == "auto_approved_exact_unique_match" for reason in items[0].reasons))
        self.assertEqual(len(persisted), 1)
        self.assertEqual(persisted[0].mal_anime_id, 222)
        self.assertEqual(persisted[0].mapping_source, "auto_exact")

    def test_build_mapping_review_surfaces_bundle_companion_for_multi_entry_residue(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["series"][0]["title"] = "The Melancholy of Haruhi Suzumiya"
            payload["series"][0]["season_title"] = "The Melancholy of Haruhi Suzumiya (English Dub)"
            payload["series"][0]["season_number"] = 1
            progress_template = dict(payload["progress"][0])
            payload["progress"] = []
            for episode_number in range(1, 29):
                item = dict(progress_template)
                item["provider_series_id"] = "series-123"
                item["provider_episode_id"] = f"ep-{episode_number}"
                item["episode_number"] = episode_number
                item["completion_ratio"] = 1.0
                payload["progress"].append(item)
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 849,
                                "title": "Suzumiya Haruhi no Yuuutsu",
                                "alternative_titles": {"en": "The Melancholy of Haruhi Suzumiya", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 14,
                            }
                        },
                        {
                            "node": {
                                "id": 4382,
                                "title": "Suzumiya Haruhi no Yuuutsu (2009)",
                                "alternative_titles": {"en": "The Melancholy of Haruhi Suzumiya", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 14,
                            }
                        },
                    ]
                },
            ):
                items = build_mapping_review(config, limit=5, mapping_limit=5)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].decision, "auto_approved")
        self.assertEqual(MAPPING_REVIEW_HEURISTICS_REVISION, items[0].mapper_revision)
        self.assertEqual(MAPPING_REVIEW_HEURISTICS_REVISION, items[0].as_dict()["mapper_revision"])
        self.assertEqual(849, items[0].suggested_mal_anime_id)
        self.assertIsNotNone(items[0].bundle_companion_candidate)
        self.assertEqual(4382, items[0].bundle_companion_candidate["mal_anime_id"])
        self.assertEqual(items[0].bundle_companion_candidate["num_episodes"], 14)
        self.assertEqual(1, len(items[0].bundle_companion_candidates))
        self.assertEqual({4382}, {candidate["mal_anime_id"] for candidate in items[0].bundle_companion_candidates})
        self.assertIn("auto_approved_exact_unique_match", items[0].reasons)

    def test_build_mapping_review_surfaces_all_bundle_companions_for_three_entry_residue(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["series"][0]["provider_series_id"] = "series-123b"
            payload["series"][0]["title"] = "Example Split Show"
            payload["series"][0]["season_title"] = "Example Split Show (English Dub)"
            payload["series"][0]["season_number"] = 1
            payload["watchlist"][0]["provider_series_id"] = "series-123b"
            progress_template = dict(payload["progress"][0])
            payload["progress"] = []
            for episode_number in range(1, 37):
                item = dict(progress_template)
                item["provider_series_id"] = "series-123b"
                item["provider_episode_id"] = f"ep-{episode_number}"
                item["episode_number"] = episode_number
                item["completion_ratio"] = 1.0
                payload["progress"].append(item)
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 1001,
                                "title": "Example Split Show",
                                "alternative_titles": {"en": "Example Split Show", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 1002,
                                "title": "Example Split Show Part 2",
                                "alternative_titles": {"en": "Example Split Show", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {
                            "node": {
                                "id": 1003,
                                "title": "Example Split Show Part 3",
                                "alternative_titles": {"en": "Example Split Show", "synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                    ]
                },
            ):
                items = build_mapping_review(config, limit=5, mapping_limit=5)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].decision, "auto_approved")
        self.assertEqual({1002, 1003}, {candidate["mal_anime_id"] for candidate in items[0].bundle_companion_candidates})
        self.assertIn(items[0].bundle_companion_candidate["mal_anime_id"], {1002, 1003})
        self.assertIn("auto_approved_exact_unique_match", items[0].reasons)

    def test_build_dry_run_sync_plan_uses_user_approved_mapping_without_search(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 2
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
            upsert_series_mapping(
                config.db_path,
                provider="crunchyroll",
                provider_series_id="series-123",
                mal_anime_id=555,
                confidence=1.0,
                mapping_source="user_approved",
                approved_by_user=True,
                notes=None,
            )

            with patch.object(MalClient, "search_anime", side_effect=AssertionError("should not search approved mapping")), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 555,
                    "title": "Approved Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0].mal_anime_id, 555)
        self.assertTrue(proposals[0].persisted_mapping_approved)
        self.assertEqual(proposals[0].mapping_status, "approved")
        self.assertEqual(proposals[0].decision, "propose_update")

    def test_build_dry_run_sync_plan_auto_approves_exact_unique_match_for_sync(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["series"][0]["title"] = "Example Show"
            payload["series"][0]["season_title"] = "Example Show Season 2 (English Dub)"
            payload["series"][0]["season_number"] = 2
            payload["progress"][0]["episode_number"] = 12
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 333,
                                "title": "Example Show Season 2",
                                "alternative_titles": {"synonyms": ["Example Show Season 2 (English Dub)"]},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        },
                        {"node": {"id": 999, "title": "Different Show", "alternative_titles": {}, "media_type": "tv"}},
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 333,
                    "title": "Example Show Season 2",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)
                persisted = list_series_mappings(config.db_path, provider="crunchyroll", approved_only=True)

        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0].mapping_status, "approved")
        self.assertTrue(proposals[0].persisted_mapping_approved)
        self.assertEqual(proposals[0].mapping_source, "auto_exact")
        self.assertTrue(any(reason == "auto_approved_exact_unique_match" for reason in proposals[0].reasons))
        self.assertEqual(len(persisted), 1)
        self.assertEqual(persisted[0].mal_anime_id, 333)

    def test_build_dry_run_sync_plan_can_require_approved_mappings_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(MalClient, "search_anime", side_effect=AssertionError("approved-only should not live search")):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3, approved_mappings_only=True)

        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0].decision, "review")
        self.assertTrue(any(reason == "approved_mappings_only_enabled" for reason in proposals[0].reasons))

    def test_persist_mapping_review_queue_only_keeps_unresolved_items(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(MalClient, "search_anime", return_value={"data": []}):
                items = build_mapping_review(config, limit=5, mapping_limit=3)
            persist_mapping_review_queue(config, items)
            rows = list_review_queue_entries(config.db_path, status="open", issue_type="mapping_review")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].severity, "error")
        self.assertEqual(rows[0].payload["decision"], "needs_manual_match")

    def test_persist_sync_review_queue_keeps_review_and_skip_rows(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)
            persist_sync_review_queue(config, proposals)
            rows = list_review_queue_entries(config.db_path, status="open", issue_type="sync_review")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].payload["decision"], "skip")

    def test_build_dry_run_sync_plan_fills_missing_finish_date_only_when_completed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 12
            payload["progress"][0]["completion_ratio"] = 0.95
            payload["progress"][0]["last_watched_at"] = "2026-03-14T22:10:00Z"
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12, "finish_date": None},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "propose_update")
        self.assertEqual(
            proposals[0].proposed_my_list_status,
            {"status": "completed", "num_watched_episodes": 12, "finish_date": "2026-03-14"},
        )
        self.assertIn("fill_missing_finish_date", proposals[0].reasons)
        self.assertIn("preserve_meaningful_start_date", proposals[0].reasons)

    def test_build_dry_run_sync_plan_preserves_existing_finish_date(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 12
            payload["progress"][0]["completion_ratio"] = 0.95
            payload["progress"][0]["last_watched_at"] = "2026-03-14T22:10:00Z"
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12, "finish_date": "2025-01-01"},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "skip")
        self.assertTrue(any(reason == "mal_already_matches_or_exceeds_proposal" for reason in proposals[0].reasons))

    def test_build_dry_run_sync_plan_preserves_meaningful_zero_progress_on_plan_to_watch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"] = []
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "plan_to_watch", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "skip")
        self.assertIn("mal_already_matches_or_exceeds_proposal", proposals[0].reasons)

    def test_build_dry_run_sync_plan_overrides_plan_to_watch_when_crunchyroll_has_completed_episode_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 2
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "plan_to_watch", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "propose_update")
        self.assertEqual(proposals[0].proposed_my_list_status, {"status": "watching", "num_watched_episodes": 2})
        self.assertIn("override_plan_to_watch_due_to_provider_watch_evidence", proposals[0].reasons)

    def test_build_dry_run_sync_plan_suppresses_watching_zero_episode_proposals(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["completion_ratio"] = 0.40
            payload["progress"][0]["episode_number"] = 1
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": None,
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "skip")
        self.assertIsNone(proposals[0].proposed_my_list_status)
        self.assertIn("partial_provider_activity_without_completed_episode", proposals[0].reasons)
        self.assertIn("no_actionable_provider_state", proposals[0].reasons)

    def test_build_dry_run_sync_plan_counts_follow_on_near_complete_episode_as_watched(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"] = [
                {
                    **payload["progress"][0],
                    "provider_episode_id": "episode-1",
                    "episode_number": 1,
                    "playback_position_ms": 1300000,
                    "duration_ms": 1440024,
                    "completion_ratio": 0.9027610239707948,
                    "last_watched_at": "2026-03-14T20:00:00Z",
                },
                {
                    **payload["progress"][0],
                    "provider_episode_id": "episode-2",
                    "episode_number": 2,
                    "playback_position_ms": 1440000,
                    "duration_ms": 1440066,
                    "completion_ratio": 0.9999541687672648,
                    "last_watched_at": "2026-03-14T20:30:00Z",
                },
            ]
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "propose_update")
        self.assertEqual(proposals[0].proposed_my_list_status, {"status": "watching", "num_watched_episodes": 2})
        self.assertIn("completion_policy=ratio>=0.95_or_remaining<=120s_or_later_episode_progress_with_ratio>=0.85", proposals[0].reasons)
        self.assertEqual(1, proposals[0].completion_audit["completed_by"]["later_episode_evidence"])
        self.assertEqual(1, proposals[0].completion_audit["completed_by"]["ratio_threshold"])
        self.assertIn("ep1@ratio=0.903", proposals[0].completion_audit["completed_examples"]["later_episode_evidence"][0])

    def test_sync_proposal_as_dict_includes_completion_audit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 12
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        payload_dict = proposals[0].as_dict()
        self.assertIn("completion_audit", payload_dict)
        self.assertEqual(1, payload_dict["completion_audit"]["completed_by"]["ratio_threshold"])
        self.assertEqual([], payload_dict["completion_audit"]["incomplete_examples"])

    def test_build_dry_run_sync_plan_counts_last_episode_within_credits_window_as_completed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 12
            payload["progress"][0]["playback_position_ms"] = 1322000
            payload["progress"][0]["duration_ms"] = 1440024
            payload["progress"][0]["completion_ratio"] = 0.9180402548846408
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 11, "finish_date": None},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "propose_update")
        self.assertEqual(
            proposals[0].proposed_my_list_status,
            {"status": "completed", "num_watched_episodes": 12, "finish_date": "2026-03-14"},
        )

    def test_build_dry_run_sync_plan_leaves_ambiguous_near_complete_episode_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"] = [
                {
                    **payload["progress"][0],
                    "provider_episode_id": "episode-6",
                    "episode_number": 6,
                    "playback_position_ms": 1440000,
                    "duration_ms": 1440066,
                    "completion_ratio": 0.9999541687672648,
                    "last_watched_at": "2026-03-14T19:00:00Z",
                },
                {
                    **payload["progress"][0],
                    "provider_episode_id": "episode-7",
                    "episode_number": 7,
                    "playback_position_ms": 1280000,
                    "duration_ms": 1420046,
                    "completion_ratio": 0.9013792510946829,
                    "last_watched_at": "2026-03-14T20:00:00Z",
                },
            ]
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "propose_update")
        self.assertEqual(proposals[0].proposed_my_list_status, {"status": "watching", "num_watched_episodes": 6})

    def test_build_dry_run_sync_plan_deduplicates_alternate_episode_variants_by_episode_number(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"] = [
                {
                    **payload["progress"][0],
                    "provider_episode_id": "episode-1-dub-a",
                    "episode_number": 1,
                    "playback_position_ms": 1440000,
                    "duration_ms": 1440066,
                    "completion_ratio": 0.9999541687672648,
                    "last_watched_at": "2026-03-14T18:00:00Z",
                },
                {
                    **payload["progress"][0],
                    "provider_episode_id": "episode-1-dub-b",
                    "episode_number": 1,
                    "playback_position_ms": 1440000,
                    "duration_ms": 1440066,
                    "completion_ratio": 0.9999541687672648,
                    "last_watched_at": "2026-03-14T18:05:00Z",
                },
                {
                    **payload["progress"][0],
                    "provider_episode_id": "episode-2-dub-a",
                    "episode_number": 2,
                    "playback_position_ms": 1440000,
                    "duration_ms": 1440066,
                    "completion_ratio": 0.9999541687672648,
                    "last_watched_at": "2026-03-14T18:30:00Z",
                },
            ]
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")

            with patch.object(
                MalClient,
                "search_anime",
                return_value={
                    "data": [
                        {
                            "node": {
                                "id": 123,
                                "title": "Example Show",
                                "alternative_titles": {"synonyms": []},
                                "media_type": "tv",
                                "status": "finished_airing",
                                "num_episodes": 12,
                            }
                        }
                    ]
                },
            ), patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 123,
                    "title": "Example Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 0},
                },
            ):
                proposals = build_dry_run_sync_plan(config, limit=5, mapping_limit=3)

        self.assertEqual(proposals[0].decision, "propose_update")
        self.assertEqual(proposals[0].proposed_my_list_status, {"status": "watching", "num_watched_episodes": 2})

    def test_execute_approved_sync_dry_run_only_targets_approved_safe_updates(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 4
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
            upsert_series_mapping(
                config.db_path,
                provider="crunchyroll",
                provider_series_id="series-123",
                mal_anime_id=888,
                confidence=1.0,
                mapping_source="user_approved",
                approved_by_user=True,
                notes=None,
            )

            with patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 888,
                    "title": "Approved Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 2, "score": 9},
                },
            ), patch.object(MalClient, "update_my_list_status", side_effect=AssertionError("dry-run should not write")):
                results = execute_approved_sync(config, limit=5, dry_run=True)

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].applied)
        self.assertEqual(results[0].proposal_decision, "propose_update")
        self.assertEqual(results[0].requested_status, {"status": "watching", "num_watched_episodes": 4})
        self.assertIn("executor_dry_run", results[0].reasons)

    def test_execute_approved_sync_performs_live_write_when_safe(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 4
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
            upsert_series_mapping(
                config.db_path,
                provider="crunchyroll",
                provider_series_id="series-123",
                mal_anime_id=888,
                confidence=1.0,
                mapping_source="user_approved",
                approved_by_user=True,
                notes=None,
            )

            with patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 888,
                    "title": "Approved Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "watching", "num_episodes_watched": 2, "score": 9},
                },
            ), patch.object(
                MalClient,
                "update_my_list_status",
                return_value={"status": "watching", "num_episodes_watched": 4, "score": 9},
            ) as update_mock:
                results = execute_approved_sync(config, limit=5, dry_run=False)

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].applied)
        update_mock.assert_called_once_with(888, status="watching", num_watched_episodes=4, score=None, start_date=None, finish_date=None)
        self.assertEqual(results[0].response_status["score"], 9)

    def test_execute_approved_sync_includes_missing_finish_date_when_safe(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 12
            payload["progress"][0]["completion_ratio"] = 0.95
            payload["progress"][0]["last_watched_at"] = "2026-03-14T22:10:00Z"
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
            upsert_series_mapping(
                config.db_path,
                provider="crunchyroll",
                provider_series_id="series-123",
                mal_anime_id=888,
                confidence=1.0,
                mapping_source="user_approved",
                approved_by_user=True,
                notes=None,
            )

            with patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 888,
                    "title": "Approved Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12, "finish_date": None, "score": 9},
                },
            ), patch.object(
                MalClient,
                "update_my_list_status",
                return_value={"status": "completed", "num_episodes_watched": 12, "finish_date": "2026-03-14", "score": 9},
            ) as update_mock:
                results = execute_approved_sync(config, limit=5, dry_run=False)

        self.assertTrue(results[0].applied)
        update_mock.assert_called_once_with(
            888,
            status="completed",
            num_watched_episodes=12,
            score=None,
            start_date=None,
            finish_date="2026-03-14",
        )
        self.assertEqual(results[0].requested_status["finish_date"], "2026-03-14")

    def test_execute_approved_sync_skips_non_forward_safe_completed_downgrade(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            payload = sample_snapshot()
            payload["progress"][0]["episode_number"] = 3
            payload["progress"][0]["completion_ratio"] = 0.95
            ingest_snapshot_payload(payload, config)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True, exist_ok=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
            upsert_series_mapping(
                config.db_path,
                provider="crunchyroll",
                provider_series_id="series-123",
                mal_anime_id=888,
                confidence=1.0,
                mapping_source="user_approved",
                approved_by_user=True,
                notes=None,
            )

            with patch.object(
                MalClient,
                "get_anime_details",
                return_value={
                    "id": 888,
                    "title": "Approved Show",
                    "num_episodes": 12,
                    "my_list_status": {"status": "completed", "num_episodes_watched": 12},
                },
            ), patch.object(MalClient, "update_my_list_status", side_effect=AssertionError("unsafe proposal should not write")):
                results = execute_approved_sync(config, limit=5, dry_run=False)

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].applied)
        self.assertEqual(results[0].proposal_decision, "skip")
        self.assertTrue(any("refusing_to_decrease_mal_progress" in reason or "refusing_to_downgrade_completed_mal_entry" in reason for reason in results[0].reasons))


if __name__ == "__main__":
    unittest.main()
