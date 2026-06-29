"""Tests for scripts/srs.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from srs import (  # noqa: E402
    DEFAULT_EASE,
    INTERVALS,
    LEECH_THRESHOLD,
    Row,
    markdown_table,
    next_ease,
    next_interval,
    normalize_topic,
    parse_date,
    parse_table,
    read_rows,
    suggest_difficulty,
    updated_row,
    write_rows,
)


class IntervalTests(unittest.TestCase):
    def test_next_interval_known_streaks(self):
        self.assertEqual(next_interval(1), 1)
        self.assertEqual(next_interval(2), 3)
        self.assertEqual(next_interval(3), 7)
        self.assertEqual(next_interval(4), 14)

    def test_next_interval_streak_5_and_above_defaults_to_30(self):
        self.assertEqual(next_interval(5), 30)
        self.assertEqual(next_interval(10), 30)
        self.assertEqual(next_interval(100), 30)

    def test_intervals_dict_is_readonly_constant(self):
        self.assertEqual(INTERVALS, {1: 1, 2: 3, 3: 7, 4: 14})

    def test_easy_difficulty_multiplies_interval_up(self):
        self.assertEqual(next_interval(1, "easy"), 1)  # int(1 * 1.4) = 1
        self.assertEqual(next_interval(3, "easy"), 9)  # int(7 * 1.4) = 9
        self.assertEqual(next_interval(5, "easy"), 42)  # int(30 * 1.4) = 42

    def test_hard_difficulty_multiplies_interval_down(self):
        self.assertEqual(next_interval(1, "hard"), 1)  # max(1, int(1*0.6)) = 1
        self.assertEqual(next_interval(3, "hard"), 4)  # int(7 * 0.6) = 4
        self.assertEqual(next_interval(5, "hard"), 18)  # int(30 * 0.6) = 18

    def test_medium_difficulty_uses_base_interval(self):
        self.assertEqual(next_interval(1, "medium"), 1)
        self.assertEqual(next_interval(3, "medium"), 7)
        self.assertEqual(next_interval(5, "medium"), 30)


class ParseDateTests(unittest.TestCase):
    def test_valid_iso_date(self):
        import datetime as dt
        self.assertEqual(parse_date("2026-06-07"), dt.date(2026, 6, 7))

    def test_invalid_date_raises_system_exit(self):
        with self.assertRaises(SystemExit):
            parse_date("not-a-date")

    def test_empty_string_raises_system_exit(self):
        with self.assertRaises(SystemExit):
            parse_date("")


class UpdatedRowTests(unittest.TestCase):
    def test_low_score_resets_streak_and_sets_tomorrow(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        old = Row("limits", "2026-06-01", 4, 3, "2026-06-08")
        new = updated_row("limits", 2, today, old)
        self.assertEqual(new.topic, "limits")
        self.assertEqual(new.score, 2)
        self.assertEqual(new.streak, 0)
        self.assertEqual(new.next_review, "2026-06-08")
        self.assertEqual(new.last_review, "2026-06-07")

    def test_high_score_increments_streak(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        old = Row("limits", "2026-06-01", 3, 1, "2026-06-04")
        new = updated_row("limits", 4, today, old)
        self.assertEqual(new.streak, 2)
        self.assertEqual(new.next_review, "2026-06-10")  # today + 3

    def test_new_topic_with_no_old_row(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        new = updated_row("integration", 4, today, None)
        self.assertEqual(new.topic, "integration")
        self.assertEqual(new.streak, 1)
        self.assertEqual(new.next_review, "2026-06-08")  # today + 1

    def test_score_at_boundary_3_is_high_enough(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        old = Row("topic", "2026-06-01", 5, 4, "2026-06-15")  # ease defaults to 2.5
        new = updated_row("topic", 3, today, old)
        self.assertEqual(new.streak, 5)  # 4 + 1
        # score 3 drops ease 2.5 → 2.36; interval int(30 * 1.0 * 2.36/2.5) = 28
        self.assertEqual(new.ease, 2.36)
        self.assertEqual(new.next_review, "2026-07-05")  # today + 28

    def test_difficulty_affects_next_review(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        old_easy = Row("e", "2026-06-01", 4, 3, "2026-06-08", difficulty="easy")
        old_hard = Row("h", "2026-06-01", 4, 3, "2026-06-08", difficulty="hard")
        new_easy = updated_row("e", 5, today, old_easy, difficulty="easy")
        new_hard = updated_row("h", 5, today, old_hard, difficulty="hard")
        self.assertEqual(new_easy.streak, 4)
        self.assertEqual(new_hard.streak, 4)
        # score 5 raises ease 2.5 → 2.6 for both; same streak (4), different
        # difficulty multipliers: int(14*1.4*2.6/2.5)=20 vs int(14*0.6*2.6/2.5)=8
        self.assertEqual(new_easy.next_review, "2026-06-27")  # today + 20
        self.assertEqual(new_hard.next_review, "2026-06-15")  # today + 8

    def test_new_topic_with_difficulty(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        new = updated_row("hard-topic", 4, today, None, difficulty="hard")
        self.assertEqual(new.difficulty, "hard")
        # New topic, streak=1, base interval=1, hard → int(1*0.6) = 1
        self.assertEqual(new.next_review, "2026-06-08")

    def test_updated_row_defaults_to_medium_difficulty(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        new = updated_row("default", 4, today, None)
        self.assertEqual(new.difficulty, "medium")


class MarkdownTableTests(unittest.TestCase):
    def test_empty_rows(self):
        table = markdown_table([])
        self.assertIn("| Topic |", table)
        self.assertIn("|-------|", table)
        # No data rows
        lines = table.strip().split("\n")
        self.assertEqual(len(lines), 2)

    def test_single_row(self):
        row = Row("limits", "2026-06-01", 4, 2, "2026-06-04")
        table = markdown_table([row])
        self.assertIn("| limits |", table)
        self.assertIn("| 2026-06-01 |", table)
        self.assertIn("| 4 |", table)
        self.assertIn("| 2 |", table)
        self.assertIn("| 2026-06-04 |", table)

    def test_multiple_rows(self):
        rows = [
            Row("a", "2026-01-01", 1, 0, "2026-01-02"),
            Row("b", "2026-02-01", 5, 4, "2026-02-15"),
        ]
        table = markdown_table(rows)
        lines = table.strip().split("\n")
        self.assertEqual(len(lines), 4)  # header + separator + 2 data rows
        self.assertIn("| a |", lines[2])
        self.assertIn("| b |", lines[3])

    def test_include_difficulty_column(self):
        row = Row("limits", "2026-06-01", 4, 2, "2026-06-04", difficulty="hard")
        table = markdown_table([row])
        self.assertIn("Difficulty", table)
        self.assertIn("hard", table)
        self.assertIn("困难", table)


class ParseTableTests(unittest.TestCase):
    def test_empty_text(self):
        self.assertEqual(parse_table(""), [])

    def test_parse_header_and_data(self):
        text = """| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| limits | 2026-06-01 | 4 | 2 | 2026-06-04 |
| rolle | 2026-06-05 | 2 | 0 | 2026-06-06 |"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].topic, "limits")
        self.assertEqual(rows[0].score, 4)
        self.assertEqual(rows[0].streak, 2)
        self.assertEqual(rows[1].topic, "rolle")
        self.assertEqual(rows[1].score, 2)

    def test_skips_header_and_separator(self):
        text = """| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| foo | 2026-01-01 | 3 | 1 | 2026-01-04 |"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].topic, "foo")

    def test_non_table_lines_ignored(self):
        text = """Some preamble text
| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| mytopic | 2026-01-01 | 5 | 3 | 2026-01-08 |
Some trailing text"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].topic, "mytopic")

    def test_extra_spaces_in_cells_are_stripped(self):
        text = "|   spaced   |   2026-01-01   |   3   |   1   |   2026-01-04   |"
        rows = parse_table(text)
        full = """| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
|   spaced   |   2026-01-01   |   3   |   1   |   2026-01-04   |"""
        rows = parse_table(full)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].topic, "spaced")

    def test_parse_legacy_5_column_format(self):
        text = """| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| limits | 2026-06-01 | 4 | 2 | 2026-06-04 |"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].difficulty, "medium")

    def test_parse_new_6_column_format(self):
        text = """| Topic | Last Review | Score | Streak | Next Review | Difficulty |
|-------|-------------|-------|--------|-------------|------------|
| limits | 2026-06-01 | 4 | 2 | 2026-06-04 | hard (困难) |"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].difficulty, "hard")

    def test_parse_6_column_strips_chinese_label(self):
        text = """| Topic | Last Review | Score | Streak | Next Review | Difficulty |
|-------|-------------|-------|--------|-------------|------------|
| topic | 2026-06-01 | 5 | 3 | 2026-06-10 | easy (简单) |"""
        rows = parse_table(text)
        self.assertEqual(rows[0].difficulty, "easy")

    def test_parse_mixed_legacy_and_new(self):
        # When round-tripping, the file will be uniform.
        # This test ensures backward compatibility: a file written by old srs.py
        # (5 columns) can be read by the new parse_table.
        text = """| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| legacy | 2026-01-01 | 3 | 1 | 2026-01-04 |"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].topic, "legacy")
        self.assertEqual(rows[0].difficulty, "medium")

    def test_skips_rows_with_non_numeric_score_or_streak(self):
        text = """| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| bad-score | 2026-01-01 | x | 1 | 2026-01-04 |
| bad-streak | 2026-01-01 | 3 | y | 2026-01-04 |
| good | 2026-01-01 | 3 | 1 | 2026-01-04 |"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].topic, "good")

    def test_unknown_difficulty_defaults_to_medium(self):
        text = """| Topic | Last Review | Score | Streak | Next Review | Difficulty |
|-------|-------------|-------|--------|-------------|------------|
| topic | 2026-06-01 | 5 | 3 | 2026-06-10 | impossible |"""
        rows = parse_table(text)
        self.assertEqual(rows[0].difficulty, "medium")

    def test_parse_new_8_column_format(self):
        text = """| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |
|-------|-------------|-------|--------|-------------|------------|------|--------|
| limits | 2026-06-01 | 4 | 2 | 2026-06-04 | hard (困难) | 1.90 | 3 |"""
        rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].difficulty, "hard")
        self.assertEqual(rows[0].ease, 1.90)
        self.assertEqual(rows[0].lapses, 3)

    def test_8_column_defaults_ease_lapses_for_5_and_6_col(self):
        text = """| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| legacy | 2026-01-01 | 3 | 1 | 2026-01-04 |"""
        rows = parse_table(text)
        self.assertEqual(rows[0].ease, DEFAULT_EASE)
        self.assertEqual(rows[0].lapses, 0)

    def test_8_column_clamps_out_of_range_ease(self):
        text = """| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |
|-------|-------------|-------|--------|-------------|------------|------|--------|
| hi | 2026-06-01 | 4 | 2 | 2026-06-04 | medium | 9.9 | 0 |
| lo | 2026-06-01 | 4 | 2 | 2026-06-04 | medium | 0.1 | 0 |"""
        rows = {r.topic: r for r in parse_table(text)}
        self.assertEqual(rows["hi"].ease, 2.7)
        self.assertEqual(rows["lo"].ease, 1.3)

    def test_malformed_row_is_skipped_with_warning(self):
        import io
        import contextlib
        text = """| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |
|-------|-------------|-------|--------|-------------|------------|------|--------|
| good | 2026-01-01 | 3 | 1 | 2026-01-04 | medium | 2.50 | 0 |
| bad | 2026-01-01 | x | 1 | 2026-01-04 | medium | 2.50 | 0 |"""
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = parse_table(text)
        self.assertEqual(len(rows), 1)
        self.assertIn("skipped malformed SRS row", err.getvalue())


class EaseTests(unittest.TestCase):
    def test_score_5_raises_ease(self):
        self.assertEqual(next_ease(2.5, 5), 2.6)

    def test_score_4_keeps_ease(self):
        self.assertEqual(next_ease(2.5, 4), 2.5)

    def test_score_3_lowers_ease(self):
        self.assertEqual(next_ease(2.5, 3), 2.36)

    def test_low_score_drops_ease(self):
        self.assertEqual(next_ease(2.5, 2), 2.3)

    def test_ease_clamped_to_max(self):
        self.assertEqual(next_ease(2.7, 5), 2.7)

    def test_ease_clamped_to_min(self):
        self.assertEqual(next_ease(1.3, 1), 1.3)

    def test_ease_scales_interval(self):
        # Same streak/difficulty, higher ease → longer interval.
        low = next_interval(3, "medium", 1.3)
        high = next_interval(3, "medium", 2.7)
        self.assertLess(low, high)
        self.assertEqual(next_interval(3, "medium", 2.5), 7)  # default ease unchanged


class LapseAndLeechTests(unittest.TestCase):
    def test_low_score_increments_lapses(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        old = Row("t", "2026-06-01", 4, 2, "2026-06-08", lapses=1)
        new = updated_row("t", 2, today, old)
        self.assertEqual(new.lapses, 2)

    def test_high_score_preserves_lapses(self):
        import datetime as dt
        today = dt.date(2026, 6, 7)
        old = Row("t", "2026-06-01", 2, 0, "2026-06-08", lapses=3)
        new = updated_row("t", 4, today, old)
        self.assertEqual(new.lapses, 3)

    def test_is_leech_at_threshold(self):
        row = Row("t", "2026-06-01", 1, 0, "2026-06-02", lapses=LEECH_THRESHOLD)
        self.assertTrue(row.is_leech())
        self.assertFalse(Row("t", "2026-06-01", 1, 0, "2026-06-02", lapses=LEECH_THRESHOLD - 1).is_leech())


class SuggestDifficultyTests(unittest.TestCase):
    def test_suggests_easy_when_strong(self):
        row = Row("t", "2026-06-07", 5, 3, "2026-07-07", difficulty="medium")
        self.assertEqual(suggest_difficulty(row), "easy")

    def test_suggests_hard_when_lapsing(self):
        row = Row("t", "2026-06-07", 2, 0, "2026-06-08", difficulty="medium", lapses=2)
        self.assertEqual(suggest_difficulty(row), "hard")

    def test_no_suggestion_when_steady(self):
        row = Row("t", "2026-06-07", 3, 1, "2026-06-08", difficulty="medium")
        self.assertIsNone(suggest_difficulty(row))


class NormalizeTopicTests(unittest.TestCase):
    def test_collapses_whitespace(self):
        self.assertEqual(normalize_topic("  极限   定义 "), "极限 定义")


class FileReadWriteTests(unittest.TestCase):
    def test_write_and_read_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "srs.md"
            rows = [
                Row("limits", "2026-01-01", 4, 2, "2026-01-04"),
                Row("rolle", "2026-01-02", 2, 0, "2026-01-03"),
            ]
            write_rows(path, rows)
            self.assertTrue(path.exists())
            loaded = read_rows(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0].topic, "limits")
            self.assertEqual(loaded[1].topic, "rolle")

    def test_read_nonexistent_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nonexistent.md"
            rows = read_rows(path)
            self.assertEqual(rows, [])

    def test_write_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sub" / "deep" / "srs.md"
            write_rows(path, [])
            self.assertTrue(path.exists())


class CLIIntegrationTests(unittest.TestCase):
    def _run(self, args: list[str]) -> subprocess.CompletedProcess:
        script = SCRIPT_DIR / "srs.py"
        return subprocess.run(
            [sys.executable, str(script)] + args,
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR),
        )

    def test_init_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(["--workspace", tmp, "init"])
            self.assertEqual(result.returncode, 0, result.stderr)
            path = Path(tmp) / ".oh-my-teacher" / "srs-state.md"
            self.assertTrue(path.exists())

    def test_init_with_slug_and_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(["--workspace", tmp, "init", "--slug", "math", "--active"])
            self.assertEqual(result.returncode, 0, result.stderr)
            active = Path(tmp) / ".oh-my-teacher" / "srs" / "_active"
            self.assertEqual(active.read_text(encoding="utf-8"), "math")

    def test_init_existing_file_fails_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            result = self._run(["--workspace", tmp, "init"])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)

    def test_init_existing_file_with_force_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            result = self._run(["--workspace", tmp, "init", "--force"])
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_set_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init", "--slug", "physics"])
            result = self._run(["--workspace", tmp, "set-active", "physics"])
            self.assertEqual(result.returncode, 0, result.stderr)
            active = Path(tmp) / ".oh-my-teacher" / "srs" / "_active"
            self.assertEqual(active.read_text(encoding="utf-8"), "physics")

    def test_set_active_require_exists_fails_for_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(["--workspace", tmp, "set-active", "ghost", "--require-exists"])
            self.assertNotEqual(result.returncode, 0)

    def test_update_new_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            result = self._run([
                "--workspace", tmp, "update", "limits",
                "--score", "4", "--today", "2026-06-07",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("limits", result.stdout)
            self.assertIn("2026-06-08", result.stdout)  # next review = today + 1

    def test_update_existing_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run([
                "--workspace", tmp, "update", "limits",
                "--score", "4", "--today", "2026-06-01",
            ])
            result = self._run([
                "--workspace", tmp, "update", "limits",
                "--score", "5", "--today", "2026-06-07",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("2026-06-10", result.stdout)  # streak 2 → +3 days

    def test_due_lists_overdue_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            # Topic overdue by 6 days (score 2 → streak=0 → next=2026-06-02)
            self._run([
                "--workspace", tmp, "update", "overdue",
                "--score", "2", "--today", "2026-06-01",
            ])
            # Topic due today (score 4 on 2026-06-06 → streak=1 → next=2026-06-07)
            self._run([
                "--workspace", tmp, "update", "due",
                "--score", "4", "--today", "2026-06-06",
            ])

            result = self._run([
                "--workspace", tmp, "due", "--today", "2026-06-07",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            # overdue should appear before due (more overdue days)
            overdue_idx = result.stdout.index("overdue")
            due_idx = result.stdout.index("due")
            self.assertLess(overdue_idx, due_idx,
                            "overdue (6 days late) should appear before due (on time)")

    def test_due_excludes_future_topics(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            # Topic not due: updated today → next = tomorrow
            self._run([
                "--workspace", tmp, "update", "future",
                "--score", "5", "--today", "2026-06-07",
            ])

            result = self._run([
                "--workspace", tmp, "due", "--today", "2026-06-07",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("future", result.stdout)

    def test_due_tsv_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run([
                "--workspace", tmp, "update", "topic",
                "--score", "4", "--today", "2026-06-01",
            ])
            result = self._run([
                "--workspace", tmp, "due", "--today", "2026-06-07",
                "--format", "tsv",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Difficulty", result.stdout)
            self.assertIn("\t", result.stdout)

    def test_list_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run([
                "--workspace", tmp, "update", "a", "--score", "3", "--today", "2026-01-01",
            ])
            self._run([
                "--workspace", tmp, "update", "b", "--score", "5", "--today", "2026-01-02",
            ])
            result = self._run(["--workspace", tmp, "list"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| a |", result.stdout)
            self.assertIn("| b |", result.stdout)

    def test_update_with_difficulty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            result = self._run([
                "--workspace", tmp, "update", "hard-topic",
                "--score", "4", "--today", "2026-06-07",
                "--difficulty", "hard",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("hard", result.stdout)

    def test_update_invalid_score_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            result = self._run([
                "--workspace", tmp, "update", "topic",
                "--score", "0", "--today", "2026-06-07",
            ])
            self.assertNotEqual(result.returncode, 0)

    def test_update_score_6_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            result = self._run([
                "--workspace", tmp, "update", "topic",
                "--score", "6", "--today", "2026-06-07",
            ])
            self.assertNotEqual(result.returncode, 0)

    def test_rename_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run(["--workspace", tmp, "update", "old-name", "--score", "4", "--today", "2026-06-01"])
            result = self._run(["--workspace", tmp, "rename", "old-name", "new-name"])
            self.assertEqual(result.returncode, 0, result.stderr)
            listed = self._run(["--workspace", tmp, "list"])
            self.assertIn("new-name", listed.stdout)
            self.assertNotIn("old-name", listed.stdout)

    def test_rename_merges_into_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run(["--workspace", tmp, "update", "dup-a", "--score", "2", "--today", "2026-06-01"])
            self._run(["--workspace", tmp, "update", "dup-b", "--score", "2", "--today", "2026-06-02"])
            result = self._run(["--workspace", tmp, "rename", "dup-a", "dup-b"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Merged", result.stderr)
            listed = self._run(["--workspace", tmp, "list"])
            self.assertNotIn("dup-a", listed.stdout)

    def test_remove_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run(["--workspace", tmp, "update", "gone", "--score", "4", "--today", "2026-06-01"])
            result = self._run(["--workspace", tmp, "remove", "gone"])
            self.assertEqual(result.returncode, 0, result.stderr)
            listed = self._run(["--workspace", tmp, "list"])
            self.assertNotIn("gone", listed.stdout)

    def test_remove_missing_topic_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            result = self._run(["--workspace", tmp, "remove", "ghost"])
            self.assertNotEqual(result.returncode, 0)

    def test_fuzzy_duplicate_topic_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run(["--workspace", tmp, "update", "limits-epsilon-delta", "--score", "4", "--today", "2026-06-01"])
            result = self._run(["--workspace", tmp, "update", "limits-epsilon-delt", "--score", "4", "--today", "2026-06-02"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("similar to existing topic", result.stderr)

    def test_leech_warning_after_repeated_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            for day in range(1, LEECH_THRESHOLD + 1):
                result = self._run([
                    "--workspace", tmp, "update", "stuck",
                    "--score", "1", "--today", f"2026-06-0{day}",
                ])
            self.assertIn("Leech", result.stderr)

    def test_difficulty_preserved_across_updates(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(["--workspace", tmp, "init"])
            self._run(["--workspace", tmp, "update", "t", "--score", "4",
                       "--today", "2026-06-01", "--difficulty", "hard"])
            self._run(["--workspace", tmp, "update", "t", "--score", "4", "--today", "2026-06-05"])
            listed = self._run(["--workspace", tmp, "list"])
            self.assertIn("hard", listed.stdout)

    def test_workspace_env_var_used_as_default(self):
        import os
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, OMT_WORKSPACE=tmp)
            script = SCRIPT_DIR / "srs.py"
            subprocess.run([sys.executable, str(script), "init"],
                           capture_output=True, text=True, cwd=str(SCRIPT_DIR), env=env)
            self.assertTrue((Path(tmp) / ".oh-my-teacher" / "srs-state.md").exists())


if __name__ == "__main__":
    unittest.main()
