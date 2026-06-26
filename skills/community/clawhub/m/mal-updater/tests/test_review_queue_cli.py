from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from mal_updater.cli import main as cli_main
from mal_updater.config import ensure_directories, load_config
from mal_updater.db import (
    bootstrap_database,
    connect,
    list_review_queue_entries,
    replace_review_queue_entries,
    update_review_queue_entry_statuses,
)
from mal_updater.ingestion import ingest_snapshot_payload
from tests.test_validation_ingestion import sample_snapshot


class ReviewQueueCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.project_root = Path(self.temp_dir.name)
        (self.project_root / ".MAL-Updater" / "config").mkdir(parents=True)
        self.config = load_config(self.project_root)
        ensure_directories(self.config)
        bootstrap_database(self.config.db_path)

    def test_list_review_queue_summary_reports_decisions_and_top_reasons(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "error",
                    "payload": {
                        "decision": "needs_manual_match",
                        "reasons": ["ambiguous_candidates", "same_franchise_tie"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-2",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "reasons": ["ambiguous_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(2, payload["count"])
        self.assertEqual({"mapping_review": 2}, payload["by_issue_type"])
        self.assertEqual({"error": 1, "warning": 1}, payload["by_severity"])
        self.assertEqual({"needs_manual_match": 1, "review": 1}, payload["by_decision"])
        self.assertEqual("series-1", payload["decision_examples"]["needs_manual_match"][0]["provider_series_id"])
        self.assertEqual(
            ["list-review-queue", "--decision", "needs_manual_match"],
            payload["decision_drilldowns"]["needs_manual_match"],
        )
        self.assertEqual(
            ["resolve-review-queue", "--decision", "needs_manual_match", "--limit", "20"],
            payload["decision_resolutions"]["needs_manual_match"],
        )
        self.assertEqual("ambiguous_candidates", payload["top_reasons"][0]["reason"])
        self.assertEqual(2, payload["top_reasons"][0]["count"])
        self.assertEqual("series-2", payload["top_reasons"][0]["examples"][0]["provider_series_id"])
        self.assertEqual("series-1", payload["top_reasons"][0]["examples"][1]["provider_series_id"])
        self.assertEqual(
            ["list-review-queue", "--reason", "ambiguous_candidates"],
            payload["top_reasons"][0]["drilldown_args"],
        )
        self.assertEqual(
            ["resolve-review-queue", "--reason", "ambiguous_candidates", "--limit", "20"],
            payload["top_reasons"][0]["resolve_args"],
        )

    def test_list_review_queue_summary_honors_issue_type_filter(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "error",
                    "payload": {"decision": "needs_manual_match", "reasons": ["mapping_reason"]},
                }
            ],
        )
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-2",
                    "severity": "warning",
                    "payload": {"decision": "skip", "reasons": ["sync_reason"]},
                }
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
            "--issue-type",
            "sync_review",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("sync_review", payload["issue_type_filter"])
        self.assertEqual(1, payload["count"])
        self.assertEqual({"sync_review": 1}, payload["by_issue_type"])
        self.assertEqual({"skip": 1}, payload["by_decision"])
        self.assertEqual(
            ["list-review-queue", "--issue-type", "sync_review", "--decision", "skip"],
            payload["decision_drilldowns"]["skip"],
        )
        self.assertEqual("sync_reason", payload["top_reasons"][0]["reason"])
        self.assertEqual(
            ["list-review-queue", "--issue-type", "sync_review", "--reason", "sync_reason"],
            payload["top_reasons"][0]["drilldown_args"],
        )

    def test_list_review_queue_limit_caps_non_summary_output(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "error",
                    "payload": {"decision": "needs_manual_match", "reasons": ["reason-a"]},
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-2",
                    "severity": "warning",
                    "payload": {"decision": "review", "reasons": ["reason-b"]},
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--limit",
            "1",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, len(payload))
        self.assertEqual("series-2", payload[0]["provider_series_id"])

    def test_list_review_queue_can_filter_by_provider_series_id(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "error",
                    "payload": {"decision": "needs_manual_match", "reasons": ["reason-a"]},
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-2",
                    "severity": "warning",
                    "payload": {"decision": "review", "reasons": ["reason-b"]},
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--provider-series-id",
            "series-1",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, len(payload))
        self.assertEqual("series-1", payload[0]["provider_series_id"])

    def test_list_review_queue_summary_uses_reopen_actions_for_resolved_status(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["same_franchise_tie"]},
                }
            ],
        )
        update_review_queue_entry_statuses(
            self.config.db_path,
            entry_ids=[item.id for item in list_review_queue_entries(self.config.db_path, status="open")],
            status="resolved",
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
            "--status",
            "resolved",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("reopen", payload["decision_actions"]["needs_manual_match"]["action"])
        self.assertEqual(
            ["reopen-review-queue", "--decision", "needs_manual_match"],
            payload["decision_actions"]["needs_manual_match"]["action_args"],
        )
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli reopen-review-queue --decision needs_manual_match",
            payload["decision_actions"]["needs_manual_match"]["action_command"],
        )
        self.assertEqual(
            ["reopen-review-queue", "--reason", "same_franchise_tie"],
            payload["top_reasons"][0]["reopen_args"],
        )
        self.assertNotIn("resolve_args", payload["top_reasons"][0])

    def test_resolved_summary_reopen_command_is_executable(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["same_franchise_tie"]},
                }
            ],
        )
        update_review_queue_entry_statuses(
            self.config.db_path,
            entry_ids=[item.id for item in list_review_queue_entries(self.config.db_path, status="open")],
            status="resolved",
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
            "--status",
            "resolved",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        reopen_args = payload["decision_actions"]["needs_manual_match"]["action_args"]

        argv = ["mal-updater", "--project-root", str(self.project_root), *reopen_args]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        reopen_payload = json.loads(stdout.getvalue())
        self.assertEqual("resolved", reopen_payload["status_from"])
        self.assertEqual("open", reopen_payload["status_to"])
        self.assertEqual(1, reopen_payload["updated"])

    def test_list_review_queue_summary_examples_include_title_when_available(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-2",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "crunchyroll_title": "Title From Sync Proposal",
                        "reasons": ["sync_reason"],
                    },
                }
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("Title From Sync Proposal", payload["decision_examples"]["skip"][0]["title"])
        self.assertEqual("Title From Sync Proposal", payload["top_reasons"][0]["examples"][0]["title"])

    def test_list_review_queue_summary_falls_back_to_provider_series_title(self) -> None:
        with connect(self.config.db_path) as conn:
            conn.execute(
                """
                INSERT INTO provider_series(provider, provider_series_id, title, season_title, raw_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "crunchyroll",
                    "series-3",
                    "Base Title",
                    "Season Title From Provider",
                    "{}",
                ),
            )
            conn.commit()

        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-3",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "reasons": ["missing_payload_title"],
                    },
                }
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("Season Title From Provider", payload["decision_examples"]["review"][0]["title"])
        self.assertEqual("Season Title From Provider", payload["top_reasons"][0]["examples"][0]["title"])

    def test_list_review_queue_summary_clusters_related_titles_into_franchise_buckets(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-10",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-11",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["same_franchise_tie"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("example show", payload["top_title_clusters"][0]["cluster"])
        self.assertEqual(2, payload["top_title_clusters"][0]["count"])
        self.assertEqual(
            ["list-review-queue", "--title-cluster", "example show"],
            payload["top_title_clusters"][0]["drilldown_args"],
        )
        self.assertEqual(
            ["resolve-review-queue", "--title-cluster", "example show", "--limit", "20"],
            payload["top_title_clusters"][0]["resolve_args"],
        )
        example_titles = {item["title"] for item in payload["top_title_clusters"][0]["examples"]}
        self.assertEqual({"Example Show Season 2", "Example Show Season 3"}, example_titles)

    def test_list_review_queue_summary_groups_repeated_fix_strategies(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-20",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Show A",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-21",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Show B",
                        "reasons": ["ambiguous_candidates", "same_franchise_tie"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(
            "needs_manual_match | ambiguous_candidates | same_franchise_tie",
            payload["top_fix_strategies"][0]["strategy"],
        )
        self.assertEqual(2, payload["top_fix_strategies"][0]["count"])
        self.assertEqual(
            [
                "list-review-queue",
                "--fix-strategy",
                "needs_manual_match | ambiguous_candidates | same_franchise_tie",
            ],
            payload["top_fix_strategies"][0]["drilldown_args"],
        )
        self.assertEqual(
            [
                "resolve-review-queue",
                "--fix-strategy",
                "needs_manual_match | ambiguous_candidates | same_franchise_tie",
                "--limit",
                "20",
            ],
            payload["top_fix_strategies"][0]["resolve_args"],
        )

    def test_list_review_queue_summary_groups_reason_families_and_strategy_families(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-22",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "crunchyroll_title": "Show A Season 1",
                        "reasons": [
                            "top_score=0.880",
                            "margin=0.070",
                            "episode_evidence_exceeds_candidate_count=24>12",
                            "multi_entry_bundle_suspected=24<=12+12",
                            "exact_normalized_title",
                        ],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-23",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "crunchyroll_title": "Show A Season 2",
                        "reasons": [
                            "top_score=0.880",
                            "margin=0.150",
                            "episode_evidence_exceeds_candidate_count=16>12",
                            "multi_entry_bundle_suspected=16<=12+13",
                            "exact_normalized_title",
                        ],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("top_score", payload["top_reason_families"][0]["reason_family"])
        self.assertEqual(2, payload["top_reason_families"][0]["count"])
        self.assertEqual(
            {
                "series-22",
                "series-23",
            },
            set(payload["top_reason_families"][0]["refresh_provider_series_ids"]),
        )
        self.assertEqual(
            "needs_review | episode_evidence_exceeds_candidate_count | exact_normalized_title | margin | multi_entry_bundle_suspected | top_score",
            payload["top_fix_strategy_families"][0]["strategy_family"],
        )
        self.assertEqual(2, payload["top_fix_strategy_families"][0]["count"])
        self.assertEqual(
            "show a || needs_review | episode_evidence_exceeds_candidate_count | exact_normalized_title | margin | multi_entry_bundle_suspected | top_score",
            payload["top_cluster_strategy_families"][0]["cluster_strategy_family"],
        )
        self.assertEqual(
            ["list-review-queue", "--reason-family", "top_score"],
            payload["top_reason_families"][0]["drilldown_args"],
        )
        self.assertEqual(
            [
                "list-review-queue",
                "--fix-strategy-family",
                "needs_review | episode_evidence_exceeds_candidate_count | exact_normalized_title | margin | multi_entry_bundle_suspected | top_score",
            ],
            payload["top_fix_strategy_families"][0]["drilldown_args"],
        )
        self.assertEqual(
            [
                "list-review-queue",
                "--cluster-strategy-family",
                "show a || needs_review | episode_evidence_exceeds_candidate_count | exact_normalized_title | margin | multi_entry_bundle_suspected | top_score",
            ],
            payload["top_cluster_strategy_families"][0]["drilldown_args"],
        )

    def test_list_review_queue_reason_family_filter_returns_matching_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-24",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "crunchyroll_title": "Show A Season 1",
                        "reasons": ["top_score=0.880", "margin=0.070"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-25",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "crunchyroll_title": "Show A Season 2",
                        "reasons": ["top_score=0.910", "margin=0.150"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-26",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "crunchyroll_title": "Show B",
                        "reasons": ["substring_title_match"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--reason-family",
            "top_score",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(2, len(payload))
        self.assertEqual({"series-24", "series-25"}, {item["provider_series_id"] for item in payload})

    def test_list_review_queue_title_cluster_filter_returns_only_matching_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-30",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-31",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["same_franchise_tie"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--title-cluster",
            "example show",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, len(payload))
        self.assertEqual("series-30", payload[0]["provider_series_id"])

    def test_list_review_queue_summary_fix_strategy_filter_scopes_summary(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-40",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Show A",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-41",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Show B",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
            "--fix-strategy",
            "needs_manual_match | ambiguous_candidates | same_franchise_tie",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, payload["count"])
        self.assertEqual(
            "needs_manual_match | ambiguous_candidates | same_franchise_tie",
            payload["fix_strategy_filter"],
        )
        self.assertEqual({"needs_manual_match": 1}, payload["by_decision"])
        self.assertEqual("series-40", payload["decision_examples"]["needs_manual_match"][0]["provider_series_id"])

    def test_list_review_queue_summary_groups_repeated_cluster_strategies(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-50",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-51",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["ambiguous_candidates", "same_franchise_tie"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(
            "example show || needs_manual_match | ambiguous_candidates | same_franchise_tie",
            payload["top_cluster_strategies"][0]["cluster_strategy"],
        )
        self.assertEqual("example show", payload["top_cluster_strategies"][0]["cluster"])
        self.assertIn(
            payload["top_cluster_strategies"][0]["label"],
            {"Example Show Season 2", "Example Show Season 3"},
        )
        self.assertEqual(2, payload["top_cluster_strategies"][0]["count"])
        self.assertEqual(
            [
                "list-review-queue",
                "--cluster-strategy",
                "example show || needs_manual_match | ambiguous_candidates | same_franchise_tie",
            ],
            payload["top_cluster_strategies"][0]["drilldown_args"],
        )
        self.assertEqual(
            [
                "resolve-review-queue",
                "--cluster-strategy",
                "example show || needs_manual_match | ambiguous_candidates | same_franchise_tie",
                "--limit",
                "20",
            ],
            payload["top_cluster_strategies"][0]["resolve_args"],
        )
        self.assertEqual(
            ["series-50", "series-51"],
            sorted(payload["top_cluster_strategies"][0]["refresh_provider_series_ids"]),
        )
        self.assertEqual(
            [
                "refresh-mapping-review-queue",
                "--provider-series-id",
                "series-50",
                "--provider-series-id",
                "series-51",
            ],
            payload["top_cluster_strategies"][0]["refresh_args"],
        )

    def test_list_review_queue_cluster_strategy_filter_returns_only_matching_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-60",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-61",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-62",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--cluster-strategy",
            "example show || needs_manual_match | ambiguous_candidates | same_franchise_tie",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, len(payload))
        self.assertEqual("series-60", payload[0]["provider_series_id"])

    def test_list_review_queue_decision_filter_returns_only_matching_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-70",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Show A",
                        "reasons": ["same_franchise_tie"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-71",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Show B",
                        "reasons": ["same_franchise_tie"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--decision",
            "needs_manual_match",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, len(payload))
        self.assertEqual("series-70", payload[0]["provider_series_id"])

    def test_list_review_queue_summary_reason_filter_scopes_summary(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-80",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Show A",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-81",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Show B",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
            "--reason",
            "same_franchise_tie",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, payload["count"])
        self.assertEqual("same_franchise_tie", payload["reason_filter"])
        self.assertEqual({"needs_manual_match": 1}, payload["by_decision"])
        self.assertEqual("series-80", payload["decision_examples"]["needs_manual_match"][0]["provider_series_id"])

    def test_list_review_queue_summary_drilldowns_preserve_active_filters(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-82",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-83",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-84",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
            "--reason",
            "same_franchise_tie",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(
            ["list-review-queue", "--title-cluster", "example show", "--reason", "same_franchise_tie"],
            payload["top_title_clusters"][0]["drilldown_args"],
        )
        self.assertEqual(
            [
                "list-review-queue",
                "--fix-strategy",
                "needs_manual_match | ambiguous_candidates | same_franchise_tie",
                "--reason",
                "same_franchise_tie",
            ],
            payload["top_fix_strategies"][0]["drilldown_args"],
        )

    def test_review_queue_next_picks_top_cluster_strategy_bucket(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-90",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-91",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["ambiguous_candidates", "same_franchise_tie"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-92",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-next",
            "--issue-type",
            "mapping_review",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(3, payload["count"])
        self.assertEqual("auto", payload["bucket_preference"])
        self.assertEqual("cluster-strategy-family", payload["selected"]["bucket_type"])
        self.assertEqual(
            "example show || needs_manual_match | ambiguous_candidates | same_franchise_tie",
            payload["selected"]["bucket_key"],
        )
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --issue-type mapping_review --cluster-strategy-family "
            '"example show || needs_manual_match | ambiguous_candidates | same_franchise_tie"',
            payload["selected"]["drilldown_command"],
        )
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli resolve-review-queue --issue-type mapping_review --cluster-strategy-family "
            '"example show || needs_manual_match | ambiguous_candidates | same_franchise_tie" --limit 20',
            payload["selected"]["resolve_command"],
        )
        self.assertEqual(
            ["series-90", "series-91"],
            sorted(payload["selected"]["refresh_provider_series_ids"]),
        )
        refresh_command = payload["selected"]["refresh_command"]
        self.assertIn("PYTHONPATH=src python3 -m mal_updater.cli refresh-mapping-review-queue", refresh_command)
        self.assertIn("--provider-series-id series-90", refresh_command)
        self.assertIn("--provider-series-id series-91", refresh_command)

    def test_review_queue_next_prefers_family_bucket_when_it_batches_more_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-90b",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise=tv", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-91b",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["same_franchise=ova", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-92b",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-next",
            "--issue-type",
            "mapping_review",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("cluster-strategy-family", payload["selected"]["bucket_type"])
        self.assertEqual(
            "example show || needs_manual_match | ambiguous_candidates | same_franchise",
            payload["selected"]["bucket_key"],
        )
        self.assertEqual(
            ["series-90b", "series-91b"],
            sorted(payload["selected"]["refresh_provider_series_ids"]),
        )

    def test_review_queue_next_preserves_existing_scope_filters(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-94",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-95",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-96",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["same_franchise_tie"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-next",
            "--issue-type",
            "mapping_review",
            "--reason",
            "same_franchise_tie",
            "--bucket",
            "title-cluster",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("same_franchise_tie", payload["reason_filter"])
        self.assertEqual("title-cluster", payload["selected"]["bucket_type"])
        self.assertEqual("example show", payload["selected"]["bucket_key"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --issue-type mapping_review --title-cluster \"example show\" --reason same_franchise_tie",
            payload["selected"]["drilldown_command"],
        )

    def test_review_queue_next_can_fall_back_to_reason_bucket(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-93",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason"],
                    },
                }
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-next",
            "--issue-type",
            "sync_review",
            "--bucket",
            "reason",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("reason", payload["selected"]["bucket_type"])
        self.assertEqual("sync_reason", payload["selected"]["bucket_key"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --issue-type sync_review --reason sync_reason",
            payload["selected"]["drilldown_command"],
        )

    def test_review_queue_next_returns_null_selection_when_queue_empty(self) -> None:
        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-next",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(0, payload["count"])
        self.assertIsNone(payload["selected"])

    def test_list_review_queue_summary_drilldowns_preserve_non_default_status(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-97",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason"],
                    },
                }
            ],
        )
        with connect(self.config.db_path) as conn:
            conn.execute("UPDATE review_queue SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP WHERE provider_series_id = ?", ("series-97",))
            conn.commit()

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "list-review-queue",
            "--summary",
            "--status",
            "resolved",
            "--issue-type",
            "sync_review",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("resolved", payload["status"])
        self.assertEqual(
            ["list-review-queue", "--status", "resolved", "--issue-type", "sync_review", "--decision", "skip"],
            payload["decision_drilldowns"]["skip"],
        )
        self.assertEqual(
            ["list-review-queue", "--status", "resolved", "--issue-type", "sync_review", "--reason", "sync_reason"],
            payload["top_reasons"][0]["drilldown_args"],
        )

    def test_review_queue_next_preserves_non_default_status_in_selected_command(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-98",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason"],
                    },
                }
            ],
        )
        with connect(self.config.db_path) as conn:
            conn.execute("UPDATE review_queue SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP WHERE provider_series_id = ?", ("series-98",))
            conn.commit()

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-next",
            "--status",
            "resolved",
            "--issue-type",
            "sync_review",
            "--bucket",
            "reason",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("resolved", payload["status"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --status resolved --issue-type sync_review --reason sync_reason",
            payload["selected"]["drilldown_command"],
        )
        self.assertEqual("reopen", payload["selected"]["action"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli reopen-review-queue --issue-type sync_review --reason sync_reason",
            payload["selected"]["action_command"],
        )

    def test_review_queue_worklist_emits_ranked_drilldowns(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-100",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-101",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["ambiguous_candidates", "same_franchise_tie"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-102",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-worklist",
            "--issue-type",
            "mapping_review",
            "--limit",
            "3",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(3, payload["count"])
        self.assertEqual(3, len(payload["selected"]))
        self.assertEqual("cluster-strategy-family", payload["selected"][0]["bucket_type"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --issue-type mapping_review --cluster-strategy-family "
            '"example show || needs_manual_match | ambiguous_candidates | same_franchise_tie"',
            payload["selected"][0]["drilldown_command"],
        )
        self.assertEqual("cluster-strategy-family", payload["selected"][1]["bucket_type"])
        self.assertIn(payload["selected"][2]["bucket_type"], {"cluster-strategy", "fix-strategy-family"})

    def test_review_queue_worklist_preserves_active_filters_and_status(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-103",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason", "retry_later"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-104",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason"],
                    },
                },
            ],
        )
        with connect(self.config.db_path) as conn:
            conn.execute(
                "UPDATE review_queue SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP WHERE issue_type = ?",
                ("sync_review",),
            )
            conn.commit()

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-worklist",
            "--status",
            "resolved",
            "--issue-type",
            "sync_review",
            "--reason",
            "sync_reason",
            "--limit",
            "2",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("resolved", payload["status"])
        self.assertEqual("sync_reason", payload["reason_filter"])
        self.assertEqual(2, len(payload["selected"]))
        self.assertEqual("fix-strategy-family", payload["selected"][0]["bucket_type"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --status resolved --issue-type sync_review --reason sync_reason --fix-strategy-family "
            '"skip | sync_reason"',
            payload["selected"][0]["drilldown_command"],
        )
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli reopen-review-queue --issue-type sync_review --reason sync_reason --fix-strategy-family "
            '"skip | sync_reason"',
            payload["selected"][0]["reopen_command"],
        )
        self.assertNotIn("refresh_command", payload["selected"][0])
        self.assertIn("--status resolved", payload["selected"][1]["drilldown_command"])
        self.assertIn("--issue-type sync_review", payload["selected"][1]["drilldown_command"])
        self.assertIn("--reason sync_reason", payload["selected"][1]["drilldown_command"])

    def test_review_queue_apply_worklist_resolves_ranked_open_buckets(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-105",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-106",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 3",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-107",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-apply-worklist",
            "--issue-type",
            "mapping_review",
            "--limit",
            "2",
            "--per-bucket-limit",
            "1",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("open", payload["status_from"])
        self.assertEqual("resolved", payload["status_to"])
        self.assertEqual(2, payload["selected_bucket_count"])
        self.assertEqual(2, payload["updated"])
        self.assertEqual(2, len(payload["selected_entry_ids"]))
        self.assertEqual("cluster-strategy-family", payload["selected_buckets"][0]["bucket_type"])
        self.assertEqual(2, payload["selected_buckets"][0]["matched_rows"])
        self.assertEqual(1, payload["selected_buckets"][0]["selected_rows"])
        self.assertEqual(1, payload["selected_buckets"][0]["new_rows"])
        self.assertEqual(1, payload["selected_buckets"][1]["new_rows"])
        resolved_ids = {item.id for item in list_review_queue_entries(self.config.db_path, status="resolved")}
        self.assertEqual(set(payload["selected_entry_ids"]), resolved_ids)

    def test_review_queue_apply_worklist_reopens_ranked_resolved_buckets(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-108",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-109",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["retry_later"],
                    },
                },
            ],
        )
        update_review_queue_entry_statuses(
            self.config.db_path,
            entry_ids=[item.id for item in list_review_queue_entries(self.config.db_path, status="open")],
            status="resolved",
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-apply-worklist",
            "--status",
            "resolved",
            "--issue-type",
            "sync_review",
            "--limit",
            "1",
            "--per-bucket-limit",
            "0",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("resolved", payload["status_from"])
        self.assertEqual("open", payload["status_to"])
        self.assertEqual(1, payload["selected_bucket_count"])
        self.assertEqual(1, payload["updated"])
        self.assertEqual("reopen", payload["selected_buckets"][0]["action"])
        reopened_ids = {item.id for item in list_review_queue_entries(self.config.db_path, status="open", issue_type="sync_review")}
        self.assertEqual(set(payload["selected_entry_ids"]), reopened_ids)
        self.assertEqual(1, len(reopened_ids))

    def test_review_queue_refresh_worklist_recomputes_ranked_mapping_buckets(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-201",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-202",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        fake_refresh_payload = {
            "provider_series_ids": ["series-201", "series-202"],
            "items": [{"provider_series_id": "series-201"}, {"provider_series_id": "series-202"}],
            "review_queue": {"resolved": 2, "inserted": 1},
        }
        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-refresh-worklist",
            "--issue-type",
            "mapping_review",
            "--limit",
            "2",
            "--per-bucket-limit",
            "0",
        ]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=io.StringIO) as stdout,
            patch("mal_updater.cli._refresh_mapping_review_queue_for_provider_series_ids", return_value=fake_refresh_payload) as refresh_mock,
        ):
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("mapping_review", payload["issue_type_filter"])
        self.assertEqual(2, payload["selected_bucket_count"])
        self.assertEqual({"series-201", "series-202"}, set(payload["selected_provider_series_ids"]))
        self.assertEqual(fake_refresh_payload, payload["refresh"])
        refresh_mock.assert_called_once()
        _, called_ids, called_mapping_limit = refresh_mock.call_args.args
        self.assertEqual(set(payload["selected_provider_series_ids"]), set(called_ids))
        self.assertEqual(5, called_mapping_limit)

    def test_review_queue_refresh_worklist_rejects_non_mapping_issue_type(self) -> None:
        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "review-queue-refresh-worklist",
            "--issue-type",
            "sync_review",
        ]
        with patch("sys.argv", argv), patch("sys.stderr", new_callable=io.StringIO) as stderr:
            exit_code = cli_main()

        self.assertEqual(2, exit_code)
        self.assertIn("currently supports only mapping_review", stderr.getvalue())

    def test_resolve_review_queue_marks_filtered_open_rows_resolved(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-110",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 2",
                        "reasons": ["same_franchise_tie", "ambiguous_candidates"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-111",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "resolve-review-queue",
            "--issue-type",
            "mapping_review",
            "--reason",
            "same_franchise_tie",
            "--limit",
            "1",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, payload["matched"])
        self.assertEqual(1, payload["updated"])
        self.assertEqual("same_franchise_tie", payload["reason_filter"])
        self.assertEqual("series-110", payload["selected"][0]["provider_series_id"])

        open_rows = list_review_queue_entries(self.config.db_path, status="open", issue_type="mapping_review")
        resolved_rows = list_review_queue_entries(self.config.db_path, status="resolved", issue_type="mapping_review")
        self.assertEqual(["series-111"], [item.provider_series_id for item in open_rows])
        self.assertEqual(["series-110"], [item.provider_series_id for item in resolved_rows])

    def test_resolve_review_queue_can_resolve_all_matching_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-112",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-113",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason", "retry_later"],
                    },
                },
            ],
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "resolve-review-queue",
            "--issue-type",
            "sync_review",
            "--decision",
            "skip",
            "--limit",
            "0",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(2, payload["matched"])
        self.assertEqual(2, payload["updated"])
        self.assertEqual(2, len(payload["selected"]))
        self.assertEqual([], list_review_queue_entries(self.config.db_path, status="open", issue_type="sync_review"))
        resolved_rows = list_review_queue_entries(self.config.db_path, status="resolved", issue_type="sync_review")
        self.assertEqual(["series-113", "series-112"], [item.provider_series_id for item in resolved_rows])

    def test_reopen_review_queue_reopens_filtered_resolved_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-114",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "crunchyroll_title": "Example Show Season 4",
                        "reasons": ["same_franchise_tie"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-115",
                    "severity": "warning",
                    "payload": {
                        "decision": "review",
                        "crunchyroll_title": "Different Show",
                        "reasons": ["weak_candidates"],
                    },
                },
            ],
        )
        update_review_queue_entry_statuses(
            self.config.db_path,
            entry_ids=[item.id for item in list_review_queue_entries(self.config.db_path, status="open", issue_type="mapping_review")],
            status="resolved",
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "reopen-review-queue",
            "--issue-type",
            "mapping_review",
            "--title-cluster",
            "Example Show",
            "--limit",
            "1",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("resolved", payload["status_from"])
        self.assertEqual("open", payload["status_to"])
        self.assertEqual(1, payload["matched"])
        self.assertEqual(1, payload["updated"])
        self.assertEqual("example show", payload["title_cluster_filter"])
        self.assertEqual("series-114", payload["selected"][0]["provider_series_id"])

        open_rows = list_review_queue_entries(self.config.db_path, status="open", issue_type="mapping_review")
        resolved_rows = list_review_queue_entries(self.config.db_path, status="resolved", issue_type="mapping_review")
        self.assertEqual(["series-114"], [item.provider_series_id for item in open_rows])
        self.assertEqual(["series-115"], [item.provider_series_id for item in resolved_rows])

    def test_reopen_review_queue_can_reopen_all_matching_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-116",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-117",
                    "severity": "warning",
                    "payload": {
                        "decision": "skip",
                        "reasons": ["sync_reason", "retry_later"],
                    },
                },
            ],
        )
        update_review_queue_entry_statuses(
            self.config.db_path,
            entry_ids=[item.id for item in list_review_queue_entries(self.config.db_path, status="open", issue_type="sync_review")],
            status="resolved",
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "reopen-review-queue",
            "--issue-type",
            "sync_review",
            "--decision",
            "skip",
            "--limit",
            "0",
        ]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(2, payload["matched"])
        self.assertEqual(2, payload["updated"])
        self.assertEqual(2, len(payload["selected"]))
        self.assertEqual([], list_review_queue_entries(self.config.db_path, status="resolved", issue_type="sync_review"))
        open_rows = list_review_queue_entries(self.config.db_path, status="open", issue_type="sync_review")
        self.assertEqual(["series-117", "series-116"], [item.provider_series_id for item in open_rows])

    def test_refresh_mapping_review_queue_requires_provider_series_id_or_all_open(self) -> None:
        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "refresh-mapping-review-queue",
        ]
        with patch("sys.argv", argv), patch("sys.stderr", new_callable=io.StringIO) as stderr:
            exit_code = cli_main()

        self.assertEqual(2, exit_code)
        self.assertIn(
            "--provider-series-id is required at least once (or use --all-open or a queue-slice filter)",
            stderr.getvalue(),
        )

    def test_refresh_mapping_review_queue_replaces_only_targeted_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-target",
                    "severity": "warning",
                    "payload": {"decision": "needs_review", "reasons": ["stale_reason"]},
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-other",
                    "severity": "warning",
                    "payload": {"decision": "needs_review", "reasons": ["keep_reason"]},
                },
            ],
        )

        refreshed_item = SimpleNamespace(
            provider="crunchyroll",
            provider_series_id="series-target",
            decision="needs_review",
            as_dict=lambda: {
                "provider": "crunchyroll",
                "provider_series_id": "series-target",
                "decision": "needs_review",
                "reasons": ["fresh_reason"],
            },
        )
        auto_approved_item = SimpleNamespace(
            provider="crunchyroll",
            provider_series_id="series-cleared",
            decision="auto_approved",
            as_dict=lambda: {
                "provider": "crunchyroll",
                "provider_series_id": "series-cleared",
                "decision": "auto_approved",
                "reasons": ["auto_approved_exact_unique_match"],
            },
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "refresh-mapping-review-queue",
            "--provider-series-id",
            "series-target",
            "--provider-series-id",
            "series-cleared",
        ]
        with patch("mal_updater.cli.build_mapping_review", return_value=[refreshed_item, auto_approved_item]), patch(
            "sys.argv", argv
        ), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(["series-cleared", "series-target"], payload["provider_series_ids"])
        self.assertEqual({"resolved": 1, "inserted": 1}, payload["review_queue"])

        open_rows = list_review_queue_entries(self.config.db_path, status="open", issue_type="mapping_review")
        self.assertEqual(["series-target", "series-other"], [item.provider_series_id for item in open_rows])
        target_row = next(item for item in open_rows if item.provider_series_id == "series-target")
        self.assertEqual(["fresh_reason"], target_row.payload["reasons"])
        self.assertEqual([], [item.provider_series_id for item in open_rows if item.provider_series_id == "series-cleared"])

    def test_refresh_mapping_review_queue_can_target_all_open_rows(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-open-a",
                    "severity": "warning",
                    "payload": {"decision": "needs_review", "reasons": ["stale_a"]},
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-open-b",
                    "severity": "warning",
                    "payload": {"decision": "needs_review", "reasons": ["stale_b"]},
                },
            ],
        )
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-sync",
                    "severity": "warning",
                    "payload": {"decision": "skip", "reasons": ["sync_reason"]},
                }
            ],
        )

        refreshed_a = SimpleNamespace(
            provider="crunchyroll",
            provider_series_id="series-open-a",
            decision="needs_review",
            as_dict=lambda: {
                "provider": "crunchyroll",
                "provider_series_id": "series-open-a",
                "decision": "needs_review",
                "reasons": ["fresh_a"],
            },
        )
        refreshed_b = SimpleNamespace(
            provider="crunchyroll",
            provider_series_id="series-open-b",
            decision="needs_manual_match",
            as_dict=lambda: {
                "provider": "crunchyroll",
                "provider_series_id": "series-open-b",
                "decision": "needs_manual_match",
                "reasons": ["fresh_b"],
            },
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "refresh-mapping-review-queue",
            "--all-open",
        ]
        with patch("mal_updater.cli.build_mapping_review", return_value=[refreshed_a, refreshed_b]) as build_review, patch(
            "sys.argv", argv
        ), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(["series-open-a", "series-open-b"], payload["provider_series_ids"])
        self.assertEqual({"resolved": 2, "inserted": 2}, payload["review_queue"])
        self.assertEqual(
            ["series-open-a", "series-open-b"],
            sorted(build_review.call_args.kwargs["provider_series_ids"]),
        )

        open_mapping_rows = list_review_queue_entries(self.config.db_path, status="open", issue_type="mapping_review")
        mapping_payloads = {item.provider_series_id: item.payload["reasons"] for item in open_mapping_rows}
        self.assertEqual(["series-open-a", "series-open-b"], sorted(mapping_payloads))
        self.assertEqual(["fresh_a"], mapping_payloads["series-open-a"])
        self.assertEqual(["fresh_b"], mapping_payloads["series-open-b"])
        open_sync_rows = list_review_queue_entries(self.config.db_path, status="open", issue_type="sync_review")
        self.assertEqual(["series-sync"], [item.provider_series_id for item in open_sync_rows])

    def test_refresh_mapping_review_queue_can_target_reason_family_slice(self) -> None:
        ingest_snapshot_payload(sample_snapshot(), self.config)
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-reason-a",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "reasons": ["top_score=0.880", "margin=0.100", "exact_normalized_title"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-reason-b",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "reasons": ["top_score=0.910", "margin=0.030", "substring_title_match"],
                    },
                },
            ],
        )

        refreshed = SimpleNamespace(
            provider="crunchyroll",
            provider_series_id="series-reason-a",
            decision="needs_review",
            as_dict=lambda: {
                "provider": "crunchyroll",
                "provider_series_id": "series-reason-a",
                "decision": "needs_review",
                "reasons": ["fresh_reason_family"],
            },
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "refresh-mapping-review-queue",
            "--reason-family",
            "exact_normalized_title",
        ]
        with patch("mal_updater.cli.build_mapping_review", return_value=[refreshed]) as build_review, patch(
            "sys.argv", argv
        ), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(["series-reason-a"], payload["provider_series_ids"])
        self.assertEqual(["series-reason-a"], sorted(build_review.call_args.kwargs["provider_series_ids"]))

        open_rows = list_review_queue_entries(self.config.db_path, status="open", issue_type="mapping_review")
        reasons_by_series = {item.provider_series_id: item.payload["reasons"] for item in open_rows}
        self.assertEqual(["fresh_reason_family"], reasons_by_series["series-reason-a"])
        self.assertEqual(["top_score=0.910", "margin=0.030", "substring_title_match"], reasons_by_series["series-reason-b"])

    def test_refresh_mapping_review_queue_can_union_explicit_ids_with_filtered_slice(self) -> None:
        ingest_snapshot_payload(sample_snapshot(), self.config)
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-union-explicit",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_manual_match",
                        "reasons": ["manual_reason"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-union-filter",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "reasons": ["top_score=0.880", "margin=0.070", "exact_normalized_title"],
                    },
                },
            ],
        )

        refreshed_explicit = SimpleNamespace(
            provider="crunchyroll",
            provider_series_id="series-union-explicit",
            decision="needs_manual_match",
            as_dict=lambda: {
                "provider": "crunchyroll",
                "provider_series_id": "series-union-explicit",
                "decision": "needs_manual_match",
                "reasons": ["fresh_manual"],
            },
        )
        refreshed_filter = SimpleNamespace(
            provider="crunchyroll",
            provider_series_id="series-union-filter",
            decision="needs_review",
            as_dict=lambda: {
                "provider": "crunchyroll",
                "provider_series_id": "series-union-filter",
                "decision": "needs_review",
                "reasons": ["fresh_filtered"],
            },
        )

        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "refresh-mapping-review-queue",
            "--provider-series-id",
            "series-union-explicit",
            "--reason-family",
            "exact_normalized_title",
        ]
        with patch("mal_updater.cli.build_mapping_review", return_value=[refreshed_explicit, refreshed_filter]) as build_review, patch(
            "sys.argv", argv
        ), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = cli_main()

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(["series-union-explicit", "series-union-filter"], payload["provider_series_ids"])
        self.assertEqual(
            ["series-union-explicit", "series-union-filter"],
            sorted(build_review.call_args.kwargs["provider_series_ids"]),
        )


if __name__ == "__main__":
    unittest.main()
