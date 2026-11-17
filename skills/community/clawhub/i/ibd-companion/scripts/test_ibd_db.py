#!/usr/bin/env python3
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ibd_care
import ibd_db


class IbdDbTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "ibd.sqlite3"
        self.conn = ibd_db.init_db(self.path)

    def tearDown(self) -> None:
        self.conn.close()
        self.tmp.cleanup()

    def test_default_path_respects_openclaw_state_dir_and_override(self) -> None:
        state = str(Path(self.tmp.name) / "state")
        self.assertEqual(
            ibd_db.resolve_default_db({"OPENCLAW_STATE_DIR": state}),
            Path(state) / "private" / "ibd" / "ibd.sqlite3",
        )
        override = str(Path(self.tmp.name) / "custom.sqlite3")
        self.assertEqual(
            ibd_db.resolve_default_db(
                {"OPENCLAW_STATE_DIR": state, "IBD_DB_PATH": override}
            ),
            Path(override),
        )

    def test_open_or_init_db_lazily_initializes_private_database(self) -> None:
        path = Path(self.tmp.name) / "nested" / "ibd.sqlite3"
        conn = ibd_db.open_or_init_db(path)
        try:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 1)
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM metric_definitions").fetchone()[0], 6
            )
            metrics = [tuple(row) for row in conn.execute(
                "SELECT code,value_type,default_unit FROM metric_definitions ORDER BY code"
            )]
            self.assertEqual(metrics, [
                ('alb', 'numeric', 'g/L'), ('crp', 'numeric', 'mg/L'),
                ('esr', 'numeric', 'mm/h'), ('hgb', 'numeric', 'g/L'),
                ('plt', 'numeric', '10^9/L'), ('wbc', 'numeric', '10^9/L'),
            ])
        finally:
            conn.close()
        self.assertTrue(path.exists())
        if os.name != "nt":
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)

    def test_base_init_never_downgrades_a_care_database(self) -> None:
        care_path = Path(self.tmp.name) / "care.sqlite3"
        care = ibd_care.open_care_db(care_path)
        try:
            ibd_care.set_profile(
                care,
                disease_type="Crohn",
                earliest_symptom_date="2020-01-01",
                diagnosis_checkup_id=None,
                notes="keep this profile",
            )
            self.assertEqual(care.execute("PRAGMA user_version").fetchone()[0], 6)
        finally:
            care.close()

        base = ibd_db.init_db(care_path)
        try:
            self.assertEqual(base.execute("PRAGMA user_version").fetchone()[0], 6)
            profile = base.execute(
                "SELECT disease_type,notes FROM disease_profile WHERE id='current'"
            ).fetchone()
            self.assertEqual(tuple(profile), ("Crohn", "keep this profile"))
        finally:
            base.close()

    def test_period_analysis_baseline_lags_metrics_and_injections(self) -> None:
        start = date.fromisoformat("2026-07-01")
        milk_days = {0, 4, 8}
        for offset in range(12):
            current = start + timedelta(days=offset)
            stool = 5 if offset in {1, 5, 9} else 2
            overall = "usual"
            if offset in {10, 11}:
                overall = "slightly_worse"
            ibd_db.record_symptom(
                self.conn,
                raw_text="analysis fixture",
                observed_at=f"{current.isoformat()}T20:00:00+08:00",
                stool_count=stool,
                stool_count_mode="day_total",
                pain_score=3 if stool == 5 else 1,
                overall_vs_usual=overall,
            )
            if offset in milk_days:
                ibd_db.record_factor(
                    self.conn, label="牛奶", log_date=current.isoformat()
                )

        first_checkup = ibd_db.schedule_checkup(
            self.conn,
            kind="lab",
            title="CRP 1",
            due_at="2026-07-01T09:00:00+08:00",
        )
        ibd_db.complete_checkup(
            self.conn, first_checkup, "2026-07-01T09:00:00+08:00"
        )
        ibd_db.add_result(
            self.conn,
            checkup_id=first_checkup,
            metric_code="crp",
            numeric_value=1,
            unit="mg/L",
        )
        second_checkup = ibd_db.schedule_checkup(
            self.conn,
            kind="lab",
            title="CRP 2",
            due_at="2026-07-12T09:00:00+08:00",
        )
        ibd_db.complete_checkup(
            self.conn, second_checkup, "2026-07-12T09:00:00+08:00"
        )
        ibd_db.add_result(
            self.conn,
            checkup_id=second_checkup,
            metric_code="crp",
            numeric_value=3,
            unit="mg/L",
        )

        injection_id = ibd_db.schedule_injection(
            self.conn,
            drug_name="test biologic",
            scheduled_at="2026-07-02T09:00:00+08:00",
        )
        ibd_db.reschedule_injection(
            self.conn,
            injection_id,
            "2026-07-03T09:00:00+08:00",
            "test",
        )
        ibd_db.complete_injection(
            self.conn, injection_id, "2026-07-04T09:00:00+08:00"
        )

        summary = ibd_db.period_summary(
            self.conn, end_date="2026-07-12", days=12, analysis=True
        )
        analysis = summary["analysis"]
        self.assertEqual(analysis["coverage"]["recorded_day_ratio"], 1.0)
        self.assertEqual(
            analysis["worsening_pattern"]["classification"],
            "multi_day_recorded_worsening",
        )
        self.assertEqual(
            analysis["worsening_pattern"]["max_consecutive_worse_days"], 2
        )
        usual_evidence = analysis["recorded_usual_day_evidence"]
        self.assertEqual(usual_evidence["stool_total_median_descriptive"], 2.0)
        self.assertFalse(usual_evidence["is_confirmed_baseline"])
        milk = analysis["factor_associations"][0]
        self.assertEqual(milk["canonical_name"], "牛奶")
        lag_one = next(item for item in milk["lags"] if item["lag_days"] == 1)
        self.assertEqual(lag_one["stool_total"]["exposed_days_with_data"], 3)
        self.assertEqual(lag_one["stool_total"]["comparison_days_with_data"], 3)
        self.assertEqual(lag_one["stool_total"]["median_difference"], 3.0)
        self.assertEqual(lag_one["stool_total"]["evidence"], "exploratory")
        crp = analysis["metric_trends"][0]
        self.assertEqual(crp["absolute_change"], 2.0)
        self.assertEqual(crp["percent_change"], 200.0)
        injection = analysis["injection_summary"]
        self.assertEqual(injection["rescheduled_count"], 1)
        self.assertEqual(injection["completed_timing"][0]["days_from_original_schedule"], 2.0)
        self.assertEqual(injection["completed_timing"][0]["days_from_current_schedule"], 1.0)

    def test_period_summary_without_analysis_keeps_basic_shape(self) -> None:
        summary = ibd_db.period_summary(
            self.conn, end_date="2026-07-31", days=7
        )
        self.assertNotIn("analysis", summary)

    def test_exact_nine_tables_and_seed_metrics(self) -> None:
        tables = {
            row["name"]
            for row in self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        self.assertEqual(
            tables,
            {
                "symptom_logs", "factor_terms", "factor_logs", "injections",
                "checkups", "metric_definitions", "checkup_results", "reminders", "settings",
            },
        )
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM metric_definitions").fetchone()[0], 6)
        metrics = [tuple(row) for row in self.conn.execute(
            "SELECT code,value_type,default_unit FROM metric_definitions ORDER BY code"
        )]
        self.assertEqual(metrics, [
            ('alb', 'numeric', 'g/L'), ('crp', 'numeric', 'mg/L'),
            ('esr', 'numeric', 'mm/h'), ('hgb', 'numeric', 'g/L'),
            ('plt', 'numeric', '10^9/L'), ('wbc', 'numeric', '10^9/L'),
        ])

    def test_latest_day_total_calibrates_then_later_increments_only(self) -> None:
        d = "2026-07-31"
        ibd_db.record_symptom(self.conn, raw_text="今天已经两次", observed_at=f"{d}T09:00:00+08:00", recorded_at=f"{d}T09:01:00+08:00", stool_count=2, stool_count_mode="day_total")
        ibd_db.record_symptom(self.conn, raw_text="刚又一次", observed_at=f"{d}T14:00:00+08:00", recorded_at=f"{d}T14:01:00+08:00", stool_count=1, stool_count_mode="increment")
        ibd_db.record_symptom(self.conn, raw_text="今天一共四次", observed_at=f"{d}T20:00:00+08:00", recorded_at=f"{d}T20:01:00+08:00", stool_count=4, stool_count_mode="day_total")
        ibd_db.record_symptom(self.conn, raw_text="后来又两次", observed_at=f"{d}T21:00:00+08:00", recorded_at=f"{d}T21:01:00+08:00", stool_count=2, stool_count_mode="increment")
        self.assertEqual(ibd_db.aggregate_day(self.conn, d)["stool_total"], 6)

    def test_daily_aggregate_includes_stool_state_bloating_and_temperature(self) -> None:
        d = "2026-07-31"
        ibd_db.record_symptom(
            self.conn, raw_text="上午偏稀", observed_at=f"{d}T09:00:00+08:00",
            stool_state="loose", bloating_score=1, temperature_c=36.7,
        )
        ibd_db.record_symptom(
            self.conn, raw_text="晚上成型但腹胀明显", observed_at=f"{d}T20:00:00+08:00",
            stool_state="formed", bloating_score=3, temperature_c=37.2,
        )
        daily = ibd_db.aggregate_day(self.conn, d)
        self.assertEqual(daily["stool_state_latest"], "formed")
        self.assertEqual((daily["bloating_max"], daily["bloating_latest"]), (3, 3))
        self.assertEqual((daily["temperature_max_c"], daily["temperature_latest_c"]), (37.2, 37.2))

    def test_effective_time_not_insertion_order(self) -> None:
        d = "2026-07-31"
        ibd_db.record_symptom(self.conn, raw_text="晚间又两次", observed_at=f"{d}T21:00:00+08:00", recorded_at=f"{d}T21:05:00+08:00", stool_count=2, stool_count_mode="increment")
        ibd_db.record_symptom(self.conn, raw_text="补记八点时一共四次", observed_at=f"{d}T20:00:00+08:00", recorded_at=f"{d}T22:00:00+08:00", stool_count=4, stool_count_mode="day_total")
        self.assertEqual(ibd_db.aggregate_day(self.conn, d)["stool_total"], 6)

    def test_no_day_total_sums_increments(self) -> None:
        d = "2026-07-31"
        for hour, count in ((9, 1), (14, 2)):
            ibd_db.record_symptom(self.conn, raw_text="新增", observed_at=f"{d}T{hour:02d}:00:00+08:00", stool_count=count, stool_count_mode="increment")
        self.assertEqual(ibd_db.aggregate_day(self.conn, d)["stool_total"], 3)

    def test_superseded_row_excluded(self) -> None:
        d = "2026-07-31"
        old = ibd_db.record_symptom(self.conn, raw_text="刚又两次", observed_at=f"{d}T14:00:00+08:00", stool_count=2, stool_count_mode="increment")
        ibd_db.record_symptom(self.conn, raw_text="说错了，是一次", observed_at=f"{d}T14:00:00+08:00", stool_count=1, stool_count_mode="increment", supersedes_id=old)
        self.assertEqual(ibd_db.aggregate_day(self.conn, d)["stool_total"], 1)

    def test_back_to_usual_requires_explicit_language(self) -> None:
        self.assertIsNone(ibd_db.classify_back_to_usual("现在好一点了"))
        self.assertIsNone(ibd_db.classify_back_to_usual("腹痛缓解很多"))
        self.assertEqual(ibd_db.classify_back_to_usual("已经恢复到和平时一样了"), 1)
        self.assertEqual(ibd_db.classify_back_to_usual("还没有完全恢复"), 0)
        self.assertIsNone(ibd_db.classify_back_to_usual("今天腹痛两分"))

    def test_factor_alias_resolves_to_canonical_term(self) -> None:
        row = ibd_db.resolve_factor(self.conn, "微辣")
        self.assertEqual(row["canonical_name"], "辣食")
        factor_id = ibd_db.record_factor(self.conn, label="微辣", log_date="2026-07-31")
        stored = self.conn.execute(
            "SELECT t.canonical_name,f.raw_label FROM factor_logs f JOIN factor_terms t ON t.id=f.factor_id WHERE f.id=?",
            (factor_id,),
        ).fetchone()
        self.assertEqual(dict(stored), {"canonical_name": "辣食", "raw_label": "微辣"})
        self.assertNotEqual(ibd_db.resolve_factor(self.conn, "牛奶")["id"], ibd_db.resolve_factor(self.conn, "酸奶")["id"])

    def test_injection_reschedule_preserves_original_and_reminder_history(self) -> None:
        injection_id = ibd_db.schedule_injection(
            self.conn, drug_name="类克", scheduled_at="2026-09-17T09:00:00+08:00",
            reminder_at="2026-09-16T09:00:00+08:00",
        )
        ibd_db.reschedule_injection(
            self.conn, injection_id, "2026-09-20T09:00:00+08:00", "医院调整",
            "2026-09-19T09:00:00+08:00",
        )
        row = self.conn.execute("SELECT * FROM injections WHERE id=?", (injection_id,)).fetchone()
        self.assertEqual(row["original_scheduled_at"], "2026-09-17T09:00:00+08:00")
        self.assertEqual(row["current_scheduled_at"], "2026-09-20T09:00:00+08:00")
        reminders = list(self.conn.execute("SELECT status,remind_at FROM reminders WHERE injection_id=? ORDER BY created_at,id", (injection_id,)))
        self.assertEqual(sorted(row["status"] for row in reminders), ["cancelled", "pending"])
        ibd_db.add_reminder(self.conn, injection_id=injection_id, reminder_kind="advance", remind_at="2026-09-13T09:00:00+08:00")
        ibd_db.add_reminder(self.conn, injection_id=injection_id, reminder_kind="due_day", remind_at="2026-09-20T08:00:00+08:00")
        kinds = {row["reminder_kind"] for row in self.conn.execute("SELECT reminder_kind FROM reminders WHERE injection_id=?", (injection_id,))}
        self.assertEqual(kinds, {"primary", "advance", "due_day"})

    def test_complete_missing_injection_raises_after_prior_writes(self) -> None:
        ibd_db.schedule_injection(
            self.conn, drug_name="类克", scheduled_at="2026-09-17T09:00:00+08:00"
        )
        with self.assertRaisesRegex(ValueError, "injection not found"):
            ibd_db.complete_injection(
                self.conn, "missing-id", "2026-09-17T09:00:00+08:00"
            )

    def test_reminder_requires_exactly_one_target(self) -> None:
        stamp = ibd_db.now_iso()
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO reminders(id,reminder_kind,remind_at,status,created_at,updated_at) VALUES (?,'primary',?,'pending',?,?)",
                (ibd_db.new_id(), stamp, stamp, stamp),
            )

    def test_checkup_reschedule_and_report_specific_ranges(self) -> None:
        checkup_id = ibd_db.schedule_checkup(
            self.conn, kind="lab", title="输注前复查", due_at="2026-09-15T09:00:00+08:00"
        )
        ibd_db.reschedule_checkup(self.conn, checkup_id, "2026-09-16T09:00:00+08:00", "医院调整")
        row = self.conn.execute("SELECT * FROM checkups WHERE id=?", (checkup_id,)).fetchone()
        self.assertEqual(row["original_due_at"], "2026-09-15T09:00:00+08:00")
        self.assertEqual(row["current_due_at"], "2026-09-16T09:00:00+08:00")
        ibd_db.complete_checkup(self.conn, checkup_id, "2026-09-16T09:00:00+08:00")
        ibd_db.add_result(
            self.conn, checkup_id=checkup_id, metric_code="hgb", numeric_value=127,
            unit="g/L", reference_low=130, reference_high=175, abnormal_flag="low",
        )
        hgb = self.conn.execute("SELECT * FROM checkup_results WHERE checkup_id=? AND metric_code='hgb'", (checkup_id,)).fetchone()
        self.assertEqual((hgb["reference_low"], hgb["reference_high"], hgb["abnormal_flag"]), (130, 175, "low"))
        ibd_db.add_result(
            self.conn, checkup_id=checkup_id, metric_code="crp", numeric_value=0.5, unit="mg/L"
        )
        crp = self.conn.execute("SELECT * FROM checkup_results WHERE checkup_id=? AND metric_code='crp'", (checkup_id,)).fetchone()
        self.assertIsNone(crp["reference_low"])
        self.assertIsNone(crp["reference_high"])
        self.assertIsNone(crp["abnormal_flag"])

    def test_custom_metric_definition_can_be_added_and_deactivated(self) -> None:
        metric = ibd_db.add_metric_definition(
            self.conn, code="infliximab_level", display_name="英夫利西单抗浓度",
            value_type="numeric", default_unit="μg/mL",
        )
        self.assertEqual(metric["code"], "infliximab_level")
        checkup_id = ibd_db.schedule_checkup(
            self.conn, kind="lab", title="药物浓度", due_at="2026-09-15T09:00:00+08:00"
        )
        ibd_db.complete_checkup(self.conn, checkup_id, "2026-09-15T09:00:00+08:00")
        ibd_db.add_result(
            self.conn, checkup_id=checkup_id, metric_code="infliximab_level", numeric_value=3.2,
            unit="μg/mL",
        )
        result = self.conn.execute("SELECT * FROM checkup_results WHERE checkup_id=?", (checkup_id,)).fetchone()
        self.assertEqual(result["numeric_value"], 3.2)
        self.assertIsNone(result["text_value"])
        inactive = ibd_db.deactivate_metric_definition(self.conn, code="infliximab_level")
        self.assertEqual(inactive["active"], 0)
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM checkup_results WHERE metric_code='infliximab_level'"
            ).fetchone()[0], 1,
        )
        with self.assertRaisesRegex(ValueError, "unknown metric"):
            ibd_db.add_result(
                self.conn, checkup_id=checkup_id, metric_code="infliximab_level",
                numeric_value=4.0, unit="μg/mL",
            )

    def test_custom_metric_definition_rejects_unsafe_or_duplicate_codes(self) -> None:
        with self.assertRaisesRegex(ValueError, "snake_case"):
            ibd_db.add_metric_definition(
                self.conn, code="CRP", display_name="C反应蛋白副本", value_type="numeric",
            )
        with self.assertRaisesRegex(ValueError, "already exists"):
            ibd_db.add_metric_definition(
                self.conn, code="crp", display_name="另一个 CRP", value_type="numeric",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
