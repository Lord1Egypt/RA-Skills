"""Synthetic matching/ranking regressions; never open the user's memory tree."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from core.common import parse_session_signals, repetition_signal
from core.matching import match_note, note_is_retrievable, tokenize
from core.scoring import resurfacing_priority
from core.signal_detect import detect_match
from scripts import create, review, scheduler, search

CASES = json.loads((Path(__file__).parent / "fixtures" / "recall_matching.json").read_text(encoding="utf-8"))["cases"]


def repeated_note(**values):
    return {"title": "云南旅游攻略", "summary": "整理大理住宿和交通", "importance": "high",
            "session_signals": {"current_session_hits": 100, "recent_session_hits": 100,
                                "cross_session_repeat_count": 100, "consecutive_session_count": 100,
                                "last_activated": date.today().isoformat()}, **values}


class MatchingTests(unittest.TestCase):
    def test_shared_fixture_detection_and_search_agree(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                relevance, meta = detect_match(case["note"], case["query"])
                self.assertEqual((relevance, meta), match_note(case["note"], case["query"]))
                self.assertEqual(meta["match_eligible"], case["eligible"])
                self.assertGreaterEqual(relevance, case.get("min_relevance", 0.0))
                self.assertLessEqual(relevance, case.get("max_relevance", 1.0))
                score, search_meta = search.score_note(case["note"], [case["query"]])
                self.assertEqual(search_meta["match_eligible"], case["eligible"])
                self.assertEqual(score > 0, case["eligible"])

    def test_query_repetition_never_adds_evidence(self):
        for note, query in (({"tags": ["postgres"]}, "postgres"),
                            ({"title": "数据库迁移"}, "数据库迁移")):
            with self.subTest(query=query):
                self.assertEqual(detect_match(note, query), detect_match(note, " ".join([query] * 20)))
                self.assertEqual(search.score_note(note, [query]), search.score_note(note, [query] * 20))
        self.assertEqual(len(tokenize("postgres " * 20)), 1)

    def test_no_term_or_unrelated_note_gets_metadata_only_score(self):
        note = repeated_note(state="hot", strength="strong", confidence="high")
        for query in ("的", "previous memory information", "数据库迁移"):
            with self.subTest(query=query):
                self.assertEqual(search.score_note(note, [query])[0], 0.0)
                self.assertEqual(resurfacing_priority(note, date.today(), query)[0], 0.0)

    def test_retrieval_confidence_is_independent_of_fact_confidence(self):
        note = {"title": "数据库迁移", "confidence": "low"}
        self.assertEqual(detect_match(note, "数据库迁移"), detect_match({**note, "confidence": "high"}, "数据库迁移"))

    def test_partial_coverage_loses_to_specific_match(self):
        note = {"title": "数据库迁移回滚"}
        exact = detect_match(note, "数据库迁移回滚")[0]
        partial = detect_match({"title": "数据库备份"}, "数据库迁移回滚")[0]
        self.assertGreater(exact, partial)
        self.assertLess(partial, 0.60)

    def test_grammatical_characters_do_not_erase_specific_topics(self):
        for topic in ("前端", "后端", "和田", "有道", "比对"):
            with self.subTest(topic=topic):
                score, meta = detect_match({"title": topic}, f"之前{topic}的问题怎么处理的？")
                self.assertGreaterEqual(score, 0.60)
                self.assertTrue(meta["match_eligible"])

    def test_explicit_lifecycle_controls_not_test_title_heuristics(self):
        for extra in ({"is_fixture": True}, {"fixture": True}, {"type": "test_fixture"},
                      {"active": False}, {"status": "retracted"}, {"superseded_by": "replacement"}):
            self.assertFalse(note_is_retrievable({"title": "Meaningful note", **extra}))
        self.assertTrue(note_is_retrievable({"title": "Smoke test deployment workflow"}))

    def test_query_repeat_boost_is_bounded_and_ages_out(self):
        today = date.today()
        note = repeated_note(title="数据库迁移", summary="数据库迁移")
        baseline = {**note, "session_signals": {}}
        fresh, meta = resurfacing_priority(note, today, "数据库迁移")
        base = resurfacing_priority(baseline, today, "数据库迁移")[0]
        self.assertLessEqual(fresh - base, 0.0700001)
        self.assertLessEqual(meta["query_repetition_boost"], 0.07)
        stale = {**note, "session_signals": {**note["session_signals"], "last_activated": "2020-01-01"}}
        self.assertAlmostEqual(resurfacing_priority(stale, today, "数据库迁移")[0], base, places=6)

    def test_current_correction_beats_explicitly_superseded_repeated_fact(self):
        old = repeated_note(title="午餐偏好", summary="午餐偏好米饭", status="superseded", superseded_by="new")
        new = {"title": "午餐偏好", "summary": "午餐偏好面食，不再吃米饭", "status": "active"}
        self.assertEqual(resurfacing_priority(old, date.today(), "午餐偏好")[0], 0.0)
        self.assertGreater(resurfacing_priority(new, date.today(), "午餐偏好")[0], 0.5)

    def test_scheduled_review_still_accepts_repeat_evidence(self):
        score, meta = resurfacing_priority(repeated_note(), date.today(), None)
        self.assertGreater(score, 0.4)
        self.assertEqual(meta["repetition_signal"], 1.0)

    def test_new_note_does_not_invent_conversation_hits(self):
        content = create.build_note_content("Synthetic topic", "experience", "medium", [])
        signals = parse_session_signals(content)
        for key in ("current_session_hits", "recent_session_hits", "cross_session_repeat_count", "consecutive_session_count"):
            self.assertEqual(signals[key], 0)
        self.assertEqual(repetition_signal({"session_signals": signals}), 0.0)
        self.assertIn("- interval_days: 1", content)
        self.assertIn((date.today() + timedelta(days=1)).isoformat(), content)

    def test_full_text_uses_same_chinese_and_latin_rules(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-matching-") as temporary:
            root = Path(temporary)
            (root / "migration.md").write_text("# 数据库迁移与回滚\n迁移失败后回滚到旧数据库\n", encoding="utf-8")
            (root / "deployment.md").write_text("# Partial deployment\n", encoding="utf-8")
            self.assertTrue(search.search_full_text(root, ["之前数据库迁移失败后怎么回滚？"]))
            self.assertEqual(search.search_full_text(root, ["art"]), [])
            self.assertEqual(search.search_full_text(root, ["之前怎么处理的"]), [])

    def test_index_and_full_text_honor_metadata_scope_and_nested_paths(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-search-scope-") as temporary:
            root = Path(temporary)
            entries = [("current", {}), ("second", {}), ("fixture", {"is_fixture": True}),
                       ("old", {"status": "superseded"}), ("unknown", None)]
            records, index_lines = [], []
            for name, flags in entries:
                (root / name).mkdir()
                (root / name / "topic.md").write_text(f"# 数据库迁移 {name}\n数据库迁移回滚\n", encoding="utf-8")
                index_lines.extend([f"- `{name}/topic.md` — 数据库迁移 {name}", "  - tags: 数据库迁移"])
                if flags is not None:
                    records.append({"path": f"memory/cold/{name}/topic.md", "title": f"数据库迁移 {name}", **flags})
            (root / "tags.json").write_text(json.dumps({"notes": records}), encoding="utf-8")
            (root / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
            hits = search.search_full_text(root, ["数据库迁移"])
            self.assertEqual({hit[0] for hit in hits}, {"current/topic.md", "second/topic.md"})
            index_hits = search.search_index(root, ["数据库迁移"])
            self.assertEqual([line for line, _ in index_hits], [1, 2, 3, 4])
            output = io.StringIO()
            with patch("sys.argv", ["search.py", "数据库迁移", str(root), "--full-text"]), contextlib.redirect_stdout(output):
                self.assertEqual(search.main(), 0)
            for marker in ("fixture/topic.md", "old/topic.md", "unknown/topic.md"):
                self.assertNotIn(marker, output.getvalue())

    def test_existing_empty_or_invalid_index_never_falls_back_to_unknown_files(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-search-scope-") as temporary:
            root = Path(temporary)
            (root / "unknown.md").write_text("# 数据库迁移\n", encoding="utf-8")
            (root / "index.md").write_text("- `unknown.md` — 数据库迁移\n", encoding="utf-8")
            for payload in ("not-json", '{"notes": []}'):
                (root / "tags.json").write_text(payload, encoding="utf-8")
                self.assertEqual(search.search_full_text(root, ["数据库迁移"]), [])
                self.assertEqual(search.search_index(root, ["数据库迁移"]), [])

    def test_missing_index_fallback_honors_note_lifecycle_headings(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-search-fallback-") as temporary:
            root = Path(temporary)
            for name, heading in {"active": "", "fixture": "## Memory type\n- test_fixture",
                                  "old": "## Status\n- superseded", "flag": "## Fixture\n- true",
                                  "inactive": "## Active\n- false"}.items():
                (root / f"{name}.md").write_text(f"# 数据库迁移\n{heading}\n", encoding="utf-8")
            (root / "index.md").write_text("- `old.md` — 数据库迁移\n", encoding="utf-8")
            self.assertEqual({hit[0] for hit in search.search_full_text(root, ["数据库迁移"])}, {"active.md"})
            self.assertEqual(search.search_index(root, ["数据库迁移"]), [])

    def run_resurface(self, notes, query, *, write=True):
        with tempfile.TemporaryDirectory(prefix="hui-yi-resurface-") as temporary:
            args = argparse.Namespace(memory_root=temporary, query=query, context_file=None, stdin=False,
                                      min_relevance=0.15, min_priority=0.0, limit=5,
                                      write_signals=write, session_key="synthetic-session")
            output = io.StringIO()
            with patch.object(review, "load_tags", return_value={"notes": notes}), \
                 patch.object(review, "apply_candidates") as apply, contextlib.redirect_stdout(output):
                self.assertEqual(review.cmd_resurface(args), 0)
            return output.getvalue(), apply

    def test_query_gate_does_not_surface_or_reinforce_unrelated_repetition(self):
        output, apply = self.run_resurface([repeated_note()], "数据库迁移")
        self.assertNotIn("云南旅游攻略", output)
        apply.assert_not_called()

    def test_only_relevant_candidates_are_written(self):
        good = {"title": "数据库迁移", "path": "memory/cold/good.md", "summary": "数据库迁移回滚"}
        output, apply = self.run_resurface([repeated_note(), good], "之前数据库迁移怎么回滚？")
        self.assertIn("数据库迁移", output)
        self.assertNotIn("云南旅游攻略", output)
        apply.assert_called_once()
        self.assertEqual([candidate["path"] for candidate in apply.call_args.args[1]], ["memory/cold/good.md"])

    def test_queryless_review_does_not_fabricate_new_recall_signal(self):
        output, apply = self.run_resurface([repeated_note()], None)
        self.assertIn("云南旅游攻略", output)
        apply.assert_not_called()

    def test_all_queryless_review_entrypoints_exclude_inactive_records(self):
        notes = [repeated_note(title="synthetic-inactive", status="superseded", next_review="2020-01-01"),
                 repeated_note(title="synthetic-fixture", is_fixture=True, next_review="2020-01-01")]
        for note in notes:
            score, meta = resurfacing_priority(note, date.today(), None)
            self.assertEqual(score, 0.0)
            self.assertFalse(meta["retrieval_eligible"])
        output, apply = self.run_resurface(notes, None)
        self.assertNotIn("synthetic-", output)
        apply.assert_not_called()
        with tempfile.TemporaryDirectory(prefix="hui-yi-review-scope-") as temporary:
            args = argparse.Namespace(memory_root=temporary, limit=5)
            for command in (review.cmd_due, review.cmd_session):
                output = io.StringIO()
                with patch.object(review, "load_tags", return_value={"notes": notes}), \
                     patch("builtins.input", side_effect=AssertionError("inactive note must not prompt")), \
                     contextlib.redirect_stdout(output):
                    self.assertEqual(command(args), 0)
                self.assertNotIn("synthetic-", output.getvalue())

    def test_scheduler_and_preview_cannot_bypass_lifecycle_or_query_relevance(self):
        good = repeated_note(title="数据库迁移", path="good.md", state="warm")
        bad = repeated_note(title="云南旅游攻略", path="other.md", state="warm")
        inactive = repeated_note(title="synthetic-inactive", path="old.md", state="warm", status="superseded")
        fixture = repeated_note(title="synthetic-fixture", path="fixture.md", state="warm", is_fixture=True)
        config = {"schedules": [{"id": "test", "enabled": True, "require_due": False, "cooldown_hours": 0}]}
        with tempfile.TemporaryDirectory(prefix="hui-yi-scheduler-scope-") as temporary:
            root = Path(temporary)
            with patch.object(scheduler, "load_tags", return_value={"notes": [good, bad, inactive, fixture]}):
                for preview in (False, True):
                    candidates = scheduler.select_candidates(root, config, datetime.now().astimezone(), None, "test", preview)
                    self.assertEqual({item["note"]["path"] for item in candidates}, {"good.md", "other.md"})
                    candidates = scheduler.select_candidates(root, config, datetime.now().astimezone(), "数据库迁移", "test", preview)
                    self.assertEqual([item["note"]["path"] for item in candidates], ["good.md"])


if __name__ == "__main__":
    unittest.main()
