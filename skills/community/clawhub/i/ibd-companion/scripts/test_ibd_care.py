#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ibd_care
import ibd_db


class IbdCareTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'ibd.sqlite3'
        self.conn = ibd_care.open_care_db(self.path)

    def tearDown(self) -> None:
        self.conn.close()
        self.tmp.cleanup()

    def test_existing_v1_database_migrates_additively(self) -> None:
        path = Path(self.tmp.name) / 'v1.sqlite3'
        old = ibd_db.init_db(path)
        old.close()
        conn = ibd_care.open_care_db(path)
        try:
            tables = {row['name'] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
            self.assertTrue({
                'disease_profile', 'disease_profile_legacy_snapshots', 'treatment_plans',
                'treatment_plan_occurrences', 'checkup_assessments', 'symptom_baselines',
                'review_episodes', 'review_components', 'checkup_reports', 'review_plans',
                'review_plan_occurrences', 'review_reminders',
            } <= tables)
            self.assertEqual(conn.execute('PRAGMA user_version').fetchone()[0], 6)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM metric_definitions').fetchone()[0], 6)
        finally:
            conn.close()

    def test_v2_profile_is_archived_before_it_is_rebuilt(self) -> None:
        path = Path(self.tmp.name) / 'v2.sqlite3'
        old = ibd_db.init_db(path)
        old.executescript('''
            CREATE TABLE disease_profile (
                id TEXT PRIMARY KEY CHECK (id = 'current'),
                disease_type TEXT NOT NULL DEFAULT 'Crohn', onset_date TEXT, diagnosis_date TEXT,
                primary_location TEXT, current_status TEXT, notes TEXT,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
        ''')
        old.execute(
            "INSERT INTO disease_profile VALUES ('current','Crohn','2020-01-01','2020-06-01','回盲部','remission','legacy note','2020-06-01T00:00:00+08:00','2020-06-01T00:00:00+08:00')"
        )
        old.execute('PRAGMA user_version = 2')
        old.commit()
        old.close()

        conn = ibd_care.open_care_db(path)
        try:
            columns = {row['name'] for row in conn.execute('PRAGMA table_info(disease_profile)')}
            self.assertEqual(columns, {
                'id', 'disease_type', 'earliest_symptom_date', 'diagnosis_checkup_id',
                'notes', 'created_at', 'updated_at',
            })
            profile = ibd_care.get_profile(conn)
            self.assertEqual(profile['earliest_symptom_date'], '2020-01-01')
            self.assertIsNone(profile['diagnosis_checkup_id'])
            self.assertEqual(profile['notes'], 'legacy note')
            legacy = conn.execute('SELECT * FROM disease_profile_legacy_snapshots').fetchone()
            payload = json.loads(legacy['payload_json'])
            self.assertEqual(payload['diagnosis_date'], '2020-06-01')
            self.assertEqual(payload['primary_location'], '回盲部')
            self.assertEqual(payload['current_status'], 'remission')
        finally:
            conn.close()

    def test_profile_links_only_a_completed_diagnosis_checkup(self) -> None:
        checkup = ibd_db.schedule_checkup(
            self.conn, kind='visit', title='确诊记录', due_at='2020-06-01T09:00:00+08:00'
        )
        with self.assertRaisesRegex(ValueError, 'must be completed'):
            ibd_care.set_profile(
                self.conn, disease_type='Crohn', earliest_symptom_date='2020-01-01',
                diagnosis_checkup_id=checkup, notes='long-lived note',
            )
        ibd_db.complete_checkup(self.conn, checkup, '2020-06-01T09:00:00+08:00')
        profile = ibd_care.set_profile(
            self.conn, disease_type='Crohn', earliest_symptom_date='2020-01-01',
            diagnosis_checkup_id=checkup, notes='long-lived note',
        )
        self.assertEqual(profile['diagnosis_checkup_id'], checkup)
        self.assertNotIn('current_status', profile)
        self.assertNotIn('primary_location', profile)

    def test_confirmed_checkup_assessments_are_versioned_and_drive_current_summary(self) -> None:
        earlier = ibd_db.schedule_checkup(self.conn, kind='other', title='肠镜', due_at='2026-01-01T09:00:00+08:00')
        later = ibd_db.schedule_checkup(self.conn, kind='visit', title='门诊复查', due_at='2026-02-01T09:00:00+08:00')
        for identifier, when in ((earlier, '2026-01-01T09:00:00+08:00'), (later, '2026-02-01T09:00:00+08:00')):
            ibd_db.complete_checkup(self.conn, identifier, when)
        first = ibd_care.record_checkup_assessment(
            self.conn, checkup_id=earlier, disease_status='active', affected_locations=['回肠'],
            severity='moderate', original_conclusion='医生确认活动', confirmed_at='2026-01-02T09:00:00+08:00',
        )
        revision = ibd_care.record_checkup_assessment(
            self.conn, checkup_id=earlier, disease_status='remission', affected_locations=['回肠'],
            severity='mild', original_conclusion='更正后的明确结论', confirmed_at='2026-01-03T09:00:00+08:00',
        )
        ibd_care.record_checkup_assessment(
            self.conn, checkup_id=later, disease_status='remission', affected_locations=[],
            severity=None, original_conclusion='门诊确认缓解', confirmed_at='2026-02-02T09:00:00+08:00',
        )
        self.assertEqual(revision['supersedes_id'], first['id'])
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM checkup_assessments WHERE checkup_id=?', (earlier,)).fetchone()[0], 2)
        summary = ibd_care.current_summary(self.conn)
        self.assertEqual(summary['latest_confirmed_checkup_assessment']['checkup_id'], later)
        self.assertEqual(summary['latest_confirmed_checkup_assessment']['disease_status'], 'remission')

    def test_metrics_do_not_create_a_formal_assessment(self) -> None:
        checkup = ibd_db.schedule_checkup(self.conn, kind='lab', title='验血', due_at='2026-01-01T09:00:00+08:00')
        ibd_db.complete_checkup(self.conn, checkup, '2026-01-01T09:00:00+08:00')
        ibd_db.add_result(self.conn, checkup_id=checkup, metric_code='crp', numeric_value=9.0, unit='mg/L')
        self.assertIsNone(ibd_care.current_summary(self.conn)['latest_confirmed_checkup_assessment'])

    def test_baseline_is_explicitly_confirmed_and_old_baseline_becomes_history(self) -> None:
        for day in range(1, 8):
            ibd_db.record_symptom(
                self.conn, raw_text='用户明确说和平时一样',
                observed_at=f'2026-07-{day:02d}T20:00:00+08:00', stool_count=2,
                stool_count_mode='day_total', pain_score=1, bloating_score=2,
                overall_vs_usual='usual',
            )
        candidate = ibd_care.generate_symptom_baseline_candidate(
            self.conn, start_date='2026-07-01', end_date='2026-07-07', notes='candidate evidence'
        )
        self.assertEqual(candidate['status'], 'candidate')
        self.assertEqual(json.loads(candidate['evidence_json'])['qualifying_days'], 7)
        self.assertEqual(candidate['bloating_score'], 2)
        self.assertIsNone(ibd_care.current_summary(self.conn)['active_symptom_baseline'])
        confirmed = ibd_care.confirm_symptom_baseline(
            self.conn, identifier=candidate['id'], confirmed_at='2026-07-08T09:00:00+08:00'
        )
        self.assertEqual(confirmed['status'], 'confirmed')
        draft = ibd_care.create_manual_symptom_baseline(
            self.conn, stool_total=3, pain_max=0, bloating_score=None, blood='no',
            urgency='no', night_stool='no', notes='user-entered revision',
        )
        self.assertEqual(draft['status'], 'draft')
        replacement = ibd_care.confirm_symptom_baseline(
            self.conn, identifier=draft['id'], confirmed_at='2026-08-01T09:00:00+08:00'
        )
        self.assertEqual(replacement['replaces_id'], candidate['id'])
        old = self.conn.execute('SELECT status FROM symptom_baselines WHERE id=?', (candidate['id'],)).fetchone()
        self.assertEqual(old['status'], 'historical')
        self.assertEqual(ibd_care.current_summary(self.conn)['active_symptom_baseline']['id'], draft['id'])

    def test_injection_generation_is_idempotent_and_links_pre_lab(self) -> None:
        plan = ibd_care.set_treatment_plan(
            self.conn, identifier=None, drug_name='英夫利西单抗', dose_note='test only',
            interval_days=56, first_scheduled_at='2026-09-17T09:00:00+08:00',
            pre_injection_lab_days=2, pre_injection_lab_title='输注前验血',
            reminder_advance_days=1, active=1, notes=None,
        )
        first = ibd_care.generate_injections(self.conn, plan_id=plan['id'], through='2027-01-20T09:00:00+08:00')
        second = ibd_care.generate_injections(self.conn, plan_id=plan['id'], through='2027-01-20T09:00:00+08:00')
        self.assertEqual(len(first), 3)
        self.assertEqual(second, [])
        injections = list(self.conn.execute('SELECT * FROM injections ORDER BY current_scheduled_at'))
        labs = list(self.conn.execute("SELECT * FROM checkups WHERE timing='pre_injection' ORDER BY current_due_at"))
        self.assertEqual(len(injections), 3)
        self.assertEqual(len(labs), 3)
        self.assertEqual(labs[0]['related_injection_id'], injections[0]['id'])
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM treatment_plan_occurrences').fetchone()[0], 3)

    def test_v4_empty_followup_layer_is_retired_without_duplicate_plan_tables(self) -> None:
        path = Path(self.tmp.name) / 'v4.sqlite3'
        old = ibd_db.init_db(path)
        old.executescript('''
            CREATE TABLE followup_plans (
                id TEXT PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL,
                interval_days INTEGER NOT NULL, first_due_at TEXT NOT NULL,
                reminder_advance_days INTEGER NOT NULL, active INTEGER NOT NULL,
                notes TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE plan_occurrences (
                id TEXT PRIMARY KEY, plan_kind TEXT NOT NULL, plan_id TEXT NOT NULL,
                scheduled_at TEXT NOT NULL, injection_id TEXT, checkup_id TEXT,
                created_at TEXT NOT NULL
            );
        ''')
        old.execute('PRAGMA user_version = 4')
        old.commit()
        old.close()
        conn = ibd_care.open_care_db(path)
        try:
            tables = {
                row['name'] for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            self.assertNotIn('followup_plans', tables)
            self.assertNotIn('plan_occurrences', tables)
            self.assertIn('treatment_plan_occurrences', tables)
            self.assertEqual(conn.execute('PRAGMA user_version').fetchone()[0], 6)
        finally:
            conn.close()

    def test_one_lab_can_belong_to_an_injection_and_a_review_without_copying_results(self) -> None:
        injection = ibd_db.schedule_injection(
            self.conn, drug_name='英夫利西单抗', scheduled_at='2026-01-06T09:00:00+08:00',
            interval_days=56,
        )
        lab = ibd_db.schedule_checkup(
            self.conn, kind='lab', title='第五针及第一次复查抽血',
            due_at='2026-01-06T09:00:00+08:00', related_injection_id=injection,
            timing='pre_injection',
        )
        ibd_db.complete_checkup(self.conn, lab, '2026-01-06T09:00:00+08:00')
        ibd_db.add_result(
            self.conn, checkup_id=lab, metric_code='crp', numeric_value=2.0, unit='mg/L',
        )
        review = ibd_care.schedule_review(
            self.conn, title='第一次大复查', review_type='first_year',
            due_at='2026-01-06T09:00:00+08:00', sequence_no=1,
        )
        ibd_care.link_review_component(
            self.conn, review_id=review['id'], checkup_id=lab, component_role='lab',
        )
        detail = ibd_care.review_detail(self.conn, review_id=review['id'])
        self.assertEqual(detail['components'][0]['related_injection_id'], injection)
        self.assertEqual(detail['components'][0]['results'][0]['metric_code'], 'crp')
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM checkup_results WHERE checkup_id=?', (lab,)).fetchone()[0], 1)

    def test_review_contains_multiple_checkups_and_reports_are_versioned(self) -> None:
        review = ibd_care.schedule_review(
            self.conn, title='年度大复查', review_type='annual',
            due_at='2026-07-01T09:00:00+08:00', sequence_no=3,
        )
        lab = ibd_db.schedule_checkup(
            self.conn, kind='lab', title='年度复查抽血', due_at='2026-07-01T09:00:00+08:00',
            timing='routine',
        )
        endoscopy = ibd_db.schedule_checkup(
            self.conn, kind='other', title='年度复查肠镜', due_at='2026-07-02T09:00:00+08:00',
            timing='routine',
        )
        for identifier, when in (
            (lab, '2026-07-01T09:00:00+08:00'),
            (endoscopy, '2026-07-02T09:00:00+08:00'),
        ):
            ibd_db.complete_checkup(self.conn, identifier, when)
        ibd_care.link_review_component(
            self.conn, review_id=review['id'], checkup_id=lab, component_role='lab',
        )
        ibd_care.link_review_component(
            self.conn, review_id=review['id'], checkup_id=endoscopy, component_role='endoscopy',
        )
        first = ibd_care.record_checkup_report(
            self.conn, checkup_id=endoscopy, report_type='endoscopy',
            reported_at='2026-07-02T12:00:00+08:00', source_organization=None,
            findings_text='原始所见', impression_text='原始结论', original_text=None,
            attachment_ref=None,
        )
        revision = ibd_care.record_checkup_report(
            self.conn, checkup_id=endoscopy, report_type='endoscopy',
            reported_at='2026-07-03T12:00:00+08:00', source_organization=None,
            findings_text='更正所见', impression_text='更正结论', original_text=None,
            attachment_ref=None,
        )
        self.assertEqual(revision['supersedes_id'], first['id'])
        detail = ibd_care.review_detail(self.conn, review_id=review['id'])
        self.assertEqual({item['component_role'] for item in detail['components']}, {'lab', 'endoscopy'})
        current_reports = [report for item in detail['components'] for report in item['reports']]
        self.assertEqual(len(current_reports), 1)
        self.assertEqual(current_reports[0]['version_no'], 2)

    def test_review_plan_uses_calendar_months_and_is_idempotent(self) -> None:
        plan = ibd_care.set_review_plan(
            self.conn, identifier=None, title='第一年半年复查', review_type='first_year',
            interval_months=6, first_due_at='2026-08-31T09:00:00+08:00',
            last_due_at='2027-08-31T09:00:00+08:00', reminder_advance_days=14,
            active=1, notes=None,
        )
        first = ibd_care.generate_reviews(
            self.conn, plan_id=plan['id'], through='2028-12-31T09:00:00+08:00',
        )
        second = ibd_care.generate_reviews(
            self.conn, plan_id=plan['id'], through='2028-12-31T09:00:00+08:00',
        )
        self.assertEqual([item['due_at'][:10] for item in first], ['2026-08-31', '2027-02-28', '2027-08-31'])
        self.assertEqual(second, [])
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM review_reminders').fetchone()[0], 3)
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM review_plans').fetchone()[0], 1)
        self.assertEqual(
            ibd_care.current_summary(self.conn)['active_review_plans'][0]['id'],
            plan['id'],
        )

    def test_review_plan_links_one_existing_review_on_the_anchor_date(self) -> None:
        plan = ibd_care.set_review_plan(
            self.conn, identifier=None, title='年度大复查', review_type='annual',
            interval_months=12, first_due_at='2026-08-03T00:00:00+08:00',
            last_due_at=None, reminder_advance_days=30, active=1, notes=None,
        )
        existing = ibd_care.schedule_review(
            self.conn, title='住院复查', review_type='scheduled',
            due_at='2026-07-30T00:00:00+08:00',
        )
        ibd_care.complete_review(
            self.conn, review_id=existing['id'], completed_at='2026-08-03T00:00:00+08:00',
        )
        generated = ibd_care.generate_reviews(
            self.conn, plan_id=plan['id'], through='2026-08-03T23:59:59+08:00',
        )
        self.assertEqual(generated, [{
            'due_at': '2026-08-03T00:00:00+08:00',
            'review_id': existing['id'],
            'linked_existing': True,
        }])
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM review_episodes').fetchone()[0], 1)
        occurrence = self.conn.execute(
            'SELECT review_id FROM review_plan_occurrences WHERE review_plan_id=?', (plan['id'],)
        ).fetchone()
        self.assertEqual(occurrence['review_id'], existing['id'])

    def test_review_plan_stops_when_due_date_matches_multiple_unlinked_reviews(self) -> None:
        plan = ibd_care.set_review_plan(
            self.conn, identifier=None, title='年度大复查', review_type='annual',
            interval_months=12, first_due_at='2026-08-03T00:00:00+08:00',
            last_due_at=None, reminder_advance_days=30, active=1, notes=None,
        )
        for title in ('复查 A', '复查 B'):
            ibd_care.schedule_review(
                self.conn, title=title, review_type='scheduled',
                due_at='2026-08-03T00:00:00+08:00',
            )
        with self.assertRaisesRegex(ValueError, 'multiple unlinked reviews'):
            ibd_care.generate_reviews(
                self.conn, plan_id=plan['id'], through='2026-08-03T23:59:59+08:00',
            )
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM review_plan_occurrences').fetchone()[0], 0)

    def test_v5_antibody_definition_upgrades_only_without_text_results(self) -> None:
        self.conn.execute(
            "INSERT INTO metric_definitions(code,display_name,value_type,default_unit) "
            "VALUES ('ifx_antibody','英夫利西单抗抗体','qualitative',NULL)"
        )
        self.conn.execute('PRAGMA user_version = 5')
        self.conn.commit()
        self.conn.close()
        self.conn = ibd_care.open_care_db(self.path)
        antibody = self.conn.execute(
            "SELECT value_type,default_unit FROM metric_definitions WHERE code='ifx_antibody'"
        ).fetchone()
        self.assertEqual((antibody['value_type'], antibody['default_unit']), ('numeric', 'ng/mL'))

    def test_explicit_legacy_review_rows_gain_parents_idempotently(self) -> None:
        diagnosis = ibd_db.schedule_checkup(
            self.conn, kind='other', title='确诊住院', due_at='2024-07-13T09:00:00+08:00',
        )
        combined = ibd_db.schedule_checkup(
            self.conn, kind='lab', title='第五针及第一次复查',
            due_at='2025-01-06T09:00:00+08:00',
        )
        for identifier, when in (
            (diagnosis, '2024-07-13T09:00:00+08:00'),
            (combined, '2025-01-06T09:00:00+08:00'),
        ):
            ibd_db.complete_checkup(self.conn, identifier, when)
        ibd_care.set_profile(
            self.conn, disease_type='Crohn', earliest_symptom_date=None,
            diagnosis_checkup_id=diagnosis, notes=None,
        )
        self.conn.execute('PRAGMA user_version = 3')
        self.conn.commit()
        self.conn.close()
        self.conn = ibd_care.open_care_db(self.path)
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM review_episodes').fetchone()[0], 2)
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM review_components').fetchone()[0], 2)
        self.conn.close()
        self.conn = ibd_care.open_care_db(self.path)
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM review_episodes').fetchone()[0], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
