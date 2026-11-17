from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "memory_review.py"
SPEC = importlib.util.spec_from_file_location("memory_review", MODULE_PATH)
assert SPEC and SPEC.loader
memory_review = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = memory_review
SPEC.loader.exec_module(memory_review)


class MemoryReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, value: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        return path

    def test_state_detects_new_and_changed_old_diaries(self) -> None:
        day1 = self.write("memory/daily/2026-07/2026-07-29.md", "day one\n")
        day2 = self.write("memory/daily/2026-07/2026-07-30.md", "day two\n")
        self.write(
            "data/exec-logs/memory-review/2026-07-31.md",
            json.dumps({"lastScanned": {"date": "2026-07-29", "md5": memory_review.md5(day1)}}),
        )
        state = self.root / "data/exec-logs/memory-review/state.json"
        first = memory_review.build_scan(self.root, state, lookback=5)
        self.assertEqual([item["path"] for item in first["changed_sources"]], [
            "memory/daily/2026-07/2026-07-30.md"
        ])
        memory_review.atomic_json(state, first["state_after"])
        self.assertEqual(memory_review.build_scan(self.root, state, 5)["changed_sources"], [])

        day1.write_text("day one amended\n")
        changed = memory_review.build_scan(self.root, state, 5)["changed_sources"]
        self.assertEqual(changed[0]["reason"], "changed")
        self.assertEqual(changed[0]["path"], "memory/daily/2026-07/2026-07-29.md")
        self.assertEqual(day2.read_text(), "day two\n")

    def test_review_report_is_not_a_daily_source(self) -> None:
        self.write("memory/daily/2026-07/2026-07-30.md", "daily\n")
        self.write("memory/daily/2026-07/2026-07-30-memory-review.md", "report\n")
        files = memory_review.daily_files(self.root)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0][0], "2026-07-30")

    def test_candidate_search_prefers_existing_topic(self) -> None:
        self.write(
            "memory/knowledge/fw-provider-registry-lazy-loading.md",
            "# Provider Registry Lazy Loading\n\nAvoid eager provider loading.\n",
        )
        self.write("memory/knowledge/fw-unrelated.md", "# Email Routing\n\nMX records.\n")
        rows = memory_review.candidate_rows(self.root, "provider registry lazy loading", 5)
        self.assertEqual(rows[0]["path"], "memory/knowledge/fw-provider-registry-lazy-loading.md")

    def test_validate_plan_accepts_update_first(self) -> None:
        self.write("memory/daily/2026-07/2026-07-30.md", "daily\n")
        self.write("memory/knowledge/fw-existing.md", "# Existing\n")
        plan = {
            "schema_version": 2,
            "source_files": ["memory/daily/2026-07/2026-07-30.md"],
            "decisions": [
                {
                    "signal": "same topic gained evidence",
                    "action": "update_existing",
                    "destination": "memory/knowledge/fw-existing.md",
                    "source_refs": ["memory/daily/2026-07/2026-07-30.md"],
                    "candidates_checked": ["memory/knowledge/fw-existing.md"],
                    "reason": "existing document owns the topic",
                }
            ],
        }
        self.assertEqual(memory_review.validate_decision_plan(self.root, plan), [])

    def test_validate_plan_rejects_unsearched_or_dated_creation(self) -> None:
        self.write("memory/daily/2026-07/2026-07-30.md", "daily\n")
        plan = {
            "schema_version": 2,
            "source_files": ["memory/daily/2026-07/2026-07-30.md"],
            "decisions": [
                {
                    "signal": "new topic",
                    "action": "create_new",
                    "destination": "memory/knowledge/fw-new-topic-2026-07.md",
                    "source_refs": ["memory/daily/2026-07/2026-07-30.md"],
                    "candidates_checked": [],
                    "reason": "new",
                }
            ],
        }
        errors = memory_review.validate_decision_plan(self.root, plan)
        self.assertTrue(any("date-free" in error for error in errors))
        self.assertTrue(any("searches_performed" in error for error in errors))

    def test_validate_plan_allows_creation_after_empty_search(self) -> None:
        self.write("memory/daily/2026-07/2026-07-30.md", "daily\n")
        plan = {
            "schema_version": 2,
            "source_files": ["memory/daily/2026-07/2026-07-30.md"],
            "decisions": [
                {
                    "signal": "independent new topic",
                    "action": "create_new",
                    "destination": "memory/knowledge/fw-independent-topic.md",
                    "source_refs": ["memory/daily/2026-07/2026-07-30.md"],
                    "candidates_checked": [],
                    "searches_performed": ["rg: independent topic", "memory_search: independent topic"],
                    "reason": "no existing document matched",
                }
            ],
        }
        self.assertEqual(memory_review.validate_decision_plan(self.root, plan), [])


if __name__ == "__main__":
    unittest.main()
