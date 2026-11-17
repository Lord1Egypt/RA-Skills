"""Unit tests for the random study-practice plan generator."""
import datetime as _dt
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
SCRIPT = SCRIPTS_DIR / "generate_study_plan.py"

_spec = importlib.util.spec_from_file_location("generate_study_plan", SCRIPT)
gsp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gsp)


class PlanShapeTests(unittest.TestCase):
    def setUp(self):
        self.pool = gsp.load_topics()

    def test_default_plan_shape(self):
        plan = gsp.build_plan(seed=1, days=7, slots_per_day=3,
                              topics_pool=self.pool, session_minutes=45,
                              start_date="2026-10-24")
        self.assertEqual(len(plan), 7)
        for day in plan:
            self.assertEqual(len(day["slots"]), 3)
            for slot in day["slots"]:
                self.assertIn("topic", slot)
                self.assertTrue(slot["topic"])
                self.assertTrue(slot["practice"])
                self.assertIsInstance(slot["minutes"], int)

    def test_dates_increment_from_start(self):
        plan = gsp.build_plan(seed=3, days=3, slots_per_day=1,
                              topics_pool=self.pool, session_minutes=45,
                              start_date="2026-01-01")
        self.assertEqual([d["date"] for d in plan],
                         ["2026-01-01", "2026-01-02", "2026-01-03"])

    def test_custom_days_and_slots(self):
        plan = gsp.build_plan(seed=9, days=2, slots_per_day=2,
                              topics_pool=self.pool, session_minutes=30,
                              start_date="2026-01-01")
        self.assertEqual(len(plan), 2)
        self.assertEqual([len(d["slots"]) for d in plan], [2, 2])


class ConstraintTests(unittest.TestCase):
    def setUp(self):
        self.pool = gsp.load_topics()

    def test_topic_no_repeat_until_pool_exhausted(self):
        plan = gsp.build_plan(seed=42, days=7, slots_per_day=3,
                              topics_pool=self.pool, session_minutes=45,
                              start_date="2026-01-01")
        topics = [s["topic"] for day in plan for s in day["slots"]]
        head = topics[:len(self.pool)]
        self.assertEqual(len(set(head)), len(self.pool),
                         "主题在池未用尽前不应重复")

    def test_slots_do_not_overlap_within_a_day(self):
        plan = gsp.build_plan(seed=7, days=5, slots_per_day=7,
                              topics_pool=self.pool, session_minutes=110,
                              start_date="2026-01-01")
        for day in plan:
            intervals = []
            for s in day["slots"]:
                hh, mm = (int(x) for x in s["start"].split(":"))
                start = hh * 60 + mm
                intervals.append((start, start + s["minutes"]))
            for (a0, a1), (b0, b1) in zip(intervals, intervals[1:]):
                self.assertLessEqual(a1, b0, f"时段冲突: {a0}-{a1} 与 {b0}-{b1}")

    def test_durations_within_bounded_interval(self):
        base = 45
        plan = gsp.build_plan(seed=11, days=7, slots_per_day=3,
                              topics_pool=self.pool, session_minutes=base,
                              start_date="2026-01-01")
        for day in plan:
            for s in day["slots"]:
                self.assertGreaterEqual(s["minutes"], gsp.MIN_MINUTES)
                self.assertLessEqual(s["minutes"], base + gsp.SESSION_JITTER_MINUTES)
                self.assertGreaterEqual(s["minutes"], base - gsp.SESSION_JITTER_MINUTES)


class ReproducibilityTests(unittest.TestCase):
    def setUp(self):
        self.pool = gsp.load_topics()

    def test_same_seed_is_reproducible(self):
        kwargs = dict(days=7, slots_per_day=3, topics_pool=self.pool,
                      session_minutes=45, start_date="2026-10-24")
        p1 = gsp.build_plan(seed=20240501, **kwargs)
        p2 = gsp.build_plan(seed=20240501, **kwargs)
        self.assertEqual(gsp.render_markdown(p1, 20240501),
                         gsp.render_markdown(p2, 20240501))
        self.assertEqual(gsp.render_json(p1, 20240501),
                         gsp.render_json(p2, 20240501))
        self.assertEqual(gsp.render_text(p1, 20240501),
                         gsp.render_text(p2, 20240501))

    def test_different_seed_differs(self):
        kwargs = dict(days=7, slots_per_day=3, topics_pool=self.pool,
                      session_minutes=45, start_date="2026-10-24")
        p1 = gsp.build_plan(seed=1, **kwargs)
        p2 = gsp.build_plan(seed=2, **kwargs)
        self.assertNotEqual(gsp.render_markdown(p1, 1), gsp.render_markdown(p2, 2))


class TopicOverrideTests(unittest.TestCase):
    def test_topics_as_names(self):
        pool = gsp.load_topics("英语,算法,写作")
        self.assertEqual([t["topic"] for t in pool], ["英语", "算法", "写作"])
        for entry in pool:
            self.assertTrue(entry["practices"])

    def test_topics_as_json_file(self):
        tmp = SKILL_DIR / "tests" / "_tmp_topics.json"
        tmp.write_text(json.dumps({"topics": [{"topic": "自定主题",
                                               "practices": ["练习 A"]}]}),
                       encoding="utf-8")
        try:
            pool = gsp.load_topics(str(tmp))
            self.assertEqual(pool[0]["topic"], "自定主题")
            self.assertEqual(pool[0]["practices"], ["练习 A"])
        finally:
            tmp.unlink(missing_ok=True)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.pool = gsp.load_topics()
        self.plan = gsp.build_plan(seed=5, days=2, slots_per_day=3,
                                   topics_pool=self.pool, session_minutes=45,
                                   start_date="2026-10-24")

    def test_markdown_has_table_header_and_rows(self):
        md = gsp.render_markdown(self.plan, seed=5)
        self.assertIn("| 日期 | 时段 | 学习主题 | 实践内容 | 时长(分钟) |", md)
        self.assertIn("|------|------|----------|----------|------------|", md)
        self.assertEqual(md.count("\n| "), 6 + 1)  # 6 rows + header

    def test_json_render_roundtrip(self):
        payload = json.loads(gsp.render_json(self.plan, seed=5))
        self.assertEqual(payload["seed"], 5)
        self.assertEqual(len(payload["plan"]), 2)


class CliTests(unittest.TestCase):
    def test_help(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        for flag in ("--days", "--slots-per-day", "--topics",
                     "--session-minutes", "--seed"):
            self.assertIn(flag, proc.stdout)

    def test_cli_markdown_default(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--seed", "20240501",
             "--start-date", "2026-10-24"],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("| 日期 | 时段 | 学习主题 | 实践内容 | 时长(分钟) |",
                      proc.stdout)
        self.assertIn("2026-10-24", proc.stdout)

    def test_cli_text_and_json(self):
        for fmt in ("text", "json"):
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--seed", "42", "--days", "2",
                 "--slots-per-day", "2", "--format", fmt,
                 "--start-date", "2026-01-01"],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            if fmt == "json":
                json.loads(proc.stdout)

    def test_cli_invalid_days(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--seed", "1", "--days", "0",
             "--start-date", "2026-01-01"],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)

    def test_cli_output_file(self):
        out = SKILL_DIR / "tests" / "_tmp_output.md"
        try:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--seed", "1", "--days", "1",
                 "--output", str(out), "--start-date", "2026-01-01"],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(out.exists())
            self.assertIn("学习实践表", out.read_text(encoding="utf-8"))
        finally:
            out.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()