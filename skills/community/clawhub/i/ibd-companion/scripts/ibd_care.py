#!/usr/bin/env python3
from __future__ import annotations

import argparse
import calendar
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import ibd_db

CARE_SCHEMA = """
CREATE TABLE IF NOT EXISTS disease_profile (
    id TEXT PRIMARY KEY CHECK (id = 'current'),
    disease_type TEXT NOT NULL DEFAULT 'Crohn',
    earliest_symptom_date TEXT,
    diagnosis_checkup_id TEXT REFERENCES checkups(id),
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS disease_profile_legacy_snapshots (
    id TEXT PRIMARY KEY,
    source_profile_id TEXT NOT NULL,
    source_schema_version INTEGER NOT NULL,
    migrated_at TEXT NOT NULL,
    payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS treatment_plans (
    id TEXT PRIMARY KEY,
    drug_name TEXT NOT NULL,
    dose_note TEXT,
    interval_days INTEGER NOT NULL CHECK (interval_days > 0),
    first_scheduled_at TEXT NOT NULL,
    pre_injection_lab_days INTEGER CHECK (pre_injection_lab_days IS NULL OR pre_injection_lab_days >= 0),
    pre_injection_lab_title TEXT,
    reminder_advance_days INTEGER NOT NULL DEFAULT 1 CHECK (reminder_advance_days >= 0),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0,1)),
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS treatment_plan_occurrences (
    id TEXT PRIMARY KEY,
    treatment_plan_id TEXT NOT NULL REFERENCES treatment_plans(id),
    scheduled_at TEXT NOT NULL,
    injection_id TEXT NOT NULL REFERENCES injections(id),
    created_at TEXT NOT NULL,
    UNIQUE(treatment_plan_id, scheduled_at)
);

CREATE TABLE IF NOT EXISTS checkup_assessments (
    id TEXT PRIMARY KEY,
    checkup_id TEXT NOT NULL REFERENCES checkups(id),
    version_no INTEGER NOT NULL CHECK (version_no > 0),
    supersedes_id TEXT REFERENCES checkup_assessments(id),
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    disease_status TEXT CHECK (disease_status IN ('active','remission','flaring','unknown')),
    affected_locations_json TEXT NOT NULL DEFAULT '[]',
    severity TEXT CHECK (severity IN ('mild','moderate','severe','unknown')),
    original_conclusion TEXT,
    confirmed_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    CHECK (disease_status IS NOT NULL OR affected_locations_json <> '[]' OR severity IS NOT NULL OR original_conclusion IS NOT NULL),
    UNIQUE(checkup_id, version_no)
);

CREATE TABLE IF NOT EXISTS symptom_baselines (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (status IN ('draft','candidate','confirmed','historical')),
    source TEXT NOT NULL CHECK (source IN ('manual','daily_records')),
    stool_total REAL CHECK (stool_total IS NULL OR stool_total >= 0),
    pain_max REAL CHECK (pain_max IS NULL OR pain_max BETWEEN 0 AND 10),
    bloating_score REAL CHECK (bloating_score IS NULL OR bloating_score BETWEEN 0 AND 10),
    blood TEXT CHECK (blood IN ('yes','no','unknown')),
    urgency TEXT CHECK (urgency IN ('yes','no','unknown')),
    night_stool TEXT CHECK (night_stool IN ('yes','no','unknown')),
    source_start_date TEXT,
    source_end_date TEXT,
    evidence_json TEXT,
    confirmed_at TEXT,
    superseded_at TEXT,
    replaces_id TEXT REFERENCES symptom_baselines(id),
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (status <> 'confirmed' OR confirmed_at IS NOT NULL),
    CHECK (source_start_date IS NULL OR source_end_date IS NULL OR source_start_date <= source_end_date)
);

CREATE TABLE IF NOT EXISTS review_episodes (
    id TEXT PRIMARY KEY,
    sequence_no INTEGER CHECK (sequence_no IS NULL OR sequence_no > 0),
    review_type TEXT NOT NULL CHECK (review_type IN ('diagnosis','scheduled','first_year','annual','unscheduled','other')),
    title TEXT NOT NULL,
    original_due_at TEXT NOT NULL,
    current_due_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('pending','partial','completed','delayed','cancelled')),
    delay_reason TEXT,
    notes TEXT,
    legacy_source_checkup_id TEXT UNIQUE REFERENCES checkups(id),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (status <> 'completed' OR completed_at IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS review_components (
    id TEXT PRIMARY KEY,
    review_id TEXT NOT NULL REFERENCES review_episodes(id),
    checkup_id TEXT NOT NULL REFERENCES checkups(id),
    component_role TEXT NOT NULL CHECK (component_role IN (
        'lab','endoscopy','ct','mri','mre','pathology','visit','assessment','diagnostic_workup','other'
    )),
    notes TEXT,
    created_at TEXT NOT NULL,
    UNIQUE(review_id, checkup_id)
);

CREATE TABLE IF NOT EXISTS checkup_reports (
    id TEXT PRIMARY KEY,
    checkup_id TEXT NOT NULL REFERENCES checkups(id),
    report_type TEXT NOT NULL CHECK (report_type IN (
        'lab','endoscopy','ct','mri','mre','pathology','visit','other'
    )),
    version_no INTEGER NOT NULL CHECK (version_no > 0),
    supersedes_id TEXT REFERENCES checkup_reports(id),
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    reported_at TEXT,
    source_organization TEXT,
    findings_text TEXT,
    impression_text TEXT,
    original_text TEXT,
    attachment_ref TEXT,
    created_at TEXT NOT NULL,
    CHECK (
        findings_text IS NOT NULL OR impression_text IS NOT NULL OR
        original_text IS NOT NULL OR attachment_ref IS NOT NULL
    ),
    UNIQUE(checkup_id, report_type, version_no)
);

CREATE TABLE IF NOT EXISTS review_plans (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    review_type TEXT NOT NULL CHECK (review_type IN ('scheduled','first_year','annual','other')),
    interval_months INTEGER NOT NULL CHECK (interval_months > 0),
    first_due_at TEXT NOT NULL,
    last_due_at TEXT,
    reminder_advance_days INTEGER NOT NULL DEFAULT 14 CHECK (reminder_advance_days >= 0),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0,1)),
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (last_due_at IS NULL OR first_due_at <= last_due_at)
);

CREATE TABLE IF NOT EXISTS review_plan_occurrences (
    id TEXT PRIMARY KEY,
    review_plan_id TEXT NOT NULL REFERENCES review_plans(id),
    scheduled_at TEXT NOT NULL,
    review_id TEXT NOT NULL REFERENCES review_episodes(id),
    created_at TEXT NOT NULL,
    UNIQUE(review_plan_id, scheduled_at)
);

CREATE TABLE IF NOT EXISTS review_reminders (
    id TEXT PRIMARY KEY,
    review_id TEXT NOT NULL REFERENCES review_episodes(id),
    remind_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending','sent','completed','cancelled')),
    external_system TEXT,
    external_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_treatment_plan_occurrence ON treatment_plan_occurrences(treatment_plan_id, scheduled_at);
CREATE UNIQUE INDEX IF NOT EXISTS idx_current_checkup_assessment ON checkup_assessments(checkup_id) WHERE is_current=1;
CREATE UNIQUE INDEX IF NOT EXISTS idx_confirmed_symptom_baseline ON symptom_baselines(status) WHERE status='confirmed';
CREATE INDEX IF NOT EXISTS idx_baseline_status_created ON symptom_baselines(status, created_at);
CREATE INDEX IF NOT EXISTS idx_review_due ON review_episodes(status, current_due_at);
CREATE INDEX IF NOT EXISTS idx_review_components_review ON review_components(review_id, component_role);
CREATE INDEX IF NOT EXISTS idx_review_components_checkup ON review_components(checkup_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_current_checkup_report
    ON checkup_reports(checkup_id, report_type) WHERE is_current=1;
CREATE INDEX IF NOT EXISTS idx_review_plan_occurrence
    ON review_plan_occurrences(review_plan_id, scheduled_at);
CREATE UNIQUE INDEX IF NOT EXISTS idx_review_plan_occurrence_review
    ON review_plan_occurrences(review_id);
CREATE INDEX IF NOT EXISTS idx_review_reminder_time
    ON review_reminders(status, remind_at);
"""

PROFILE_V2_COLUMNS = {
    'id', 'disease_type', 'onset_date', 'diagnosis_date', 'primary_location',
    'current_status', 'notes', 'created_at', 'updated_at',
}


def open_care_db(path: Path) -> sqlite3.Connection:
    conn = ibd_db.open_or_init_db(path)
    source_version = conn.execute('PRAGMA user_version').fetchone()[0]
    with conn:
        conn.executescript(CARE_SCHEMA)
    _migrate_v2_profile_if_needed(conn)
    if source_version < 4:
        _migrate_v3_review_hierarchy_if_needed(conn)
    if source_version < 5:
        _migrate_v4_plan_naming_if_needed(conn)
    if source_version < 6:
        _migrate_v5_core_metric_definition_if_needed(conn)
    with conn:
        conn.execute('PRAGMA user_version = 6')
    return conn


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row['name'] for row in conn.execute(f'PRAGMA table_info({table})')}


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone() is not None


def _migrate_v4_plan_naming_if_needed(conn: sqlite3.Connection) -> None:
    has_followups = _table_exists(conn, 'followup_plans')
    has_occurrences = _table_exists(conn, 'plan_occurrences')
    if not has_followups and not has_occurrences:
        return
    followup_count = conn.execute(
        'SELECT COUNT(*) FROM followup_plans'
    ).fetchone()[0] if has_followups else 0
    followup_occurrence_count = conn.execute(
        "SELECT COUNT(*) FROM plan_occurrences WHERE plan_kind='followup'"
    ).fetchone()[0] if has_occurrences else 0
    if followup_count or followup_occurrence_count:
        raise RuntimeError(
            'legacy followup plans require explicit review before V5 migration'
        )
    with conn:
        if has_occurrences:
            conn.execute(
                '''INSERT OR IGNORE INTO treatment_plan_occurrences(
                       id,treatment_plan_id,scheduled_at,injection_id,created_at
                   )
                   SELECT id,plan_id,scheduled_at,injection_id,created_at
                   FROM plan_occurrences
                   WHERE plan_kind='injection' AND injection_id IS NOT NULL'''
            )
            conn.execute('DROP TABLE plan_occurrences')
        if has_followups:
            conn.execute('DROP TABLE followup_plans')


def _migrate_v5_core_metric_definition_if_needed(conn: sqlite3.Connection) -> None:
    """Correct the core antibody definition when doing so preserves all facts.

    Early databases seeded infliximab antibody as a qualitative observation,
    while the tracker now uses the quantitative ng/mL assay.  Do not rewrite a
    database that already contains text-valued historical results: those facts
    need an explicit user decision instead of a type change by migration.
    """
    metric = conn.execute(
        "SELECT value_type,default_unit FROM metric_definitions WHERE code='ifx_antibody'"
    ).fetchone()
    if metric is None or (metric['value_type'] == 'numeric' and metric['default_unit'] == 'ng/mL'):
        return
    text_count, numeric_count = conn.execute(
        '''SELECT
               SUM(CASE WHEN text_value IS NOT NULL THEN 1 ELSE 0 END),
               SUM(CASE WHEN numeric_value IS NOT NULL THEN 1 ELSE 0 END)
           FROM checkup_results WHERE metric_code='ifx_antibody' '''
    ).fetchone()
    if text_count:
        return
    with conn:
        conn.execute(
            "UPDATE metric_definitions SET value_type='numeric',default_unit='ng/mL' "
            "WHERE code='ifx_antibody'",
        )


def _migrate_v2_profile_if_needed(conn: sqlite3.Connection) -> None:
    columns = _table_columns(conn, 'disease_profile')
    if not PROFILE_V2_COLUMNS <= columns:
        return
    rows = [dict(row) for row in conn.execute('SELECT * FROM disease_profile')]
    stamp = ibd_db.now_iso()
    with conn:
        for row in rows:
            conn.execute(
                '''INSERT INTO disease_profile_legacy_snapshots(
                       id,source_profile_id,source_schema_version,migrated_at,payload_json
                   ) VALUES (?,?,?,?,?)''',
                (ibd_db.new_id(), row['id'], 2, stamp, json.dumps(row, ensure_ascii=False, sort_keys=True)),
            )
        conn.execute('ALTER TABLE disease_profile RENAME TO disease_profile_v2_archived')
        conn.execute(
            '''CREATE TABLE disease_profile (
                id TEXT PRIMARY KEY CHECK (id = 'current'),
                disease_type TEXT NOT NULL DEFAULT 'Crohn',
                earliest_symptom_date TEXT,
                diagnosis_checkup_id TEXT REFERENCES checkups(id),
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )'''
        )
        for row in rows:
            conn.execute(
                '''INSERT INTO disease_profile(
                       id,disease_type,earliest_symptom_date,diagnosis_checkup_id,notes,created_at,updated_at
                   ) VALUES (?,?,?,?,?,?,?)''',
                (row['id'], row['disease_type'], row['onset_date'], None, row['notes'], row['created_at'], row['updated_at']),
            )
        conn.execute('DROP TABLE disease_profile_v2_archived')


def _insert_legacy_review(
    conn: sqlite3.Connection, *, checkup: sqlite3.Row, review_type: str,
    component_role: str,
) -> None:
    existing = conn.execute(
        'SELECT id FROM review_episodes WHERE legacy_source_checkup_id=?',
        (checkup['id'],),
    ).fetchone()
    if existing:
        review_id = existing['id']
    else:
        review_id = ibd_db.new_id()
        stamp = ibd_db.now_iso()
        status = checkup['status'] if checkup['status'] in ('pending','completed','delayed','cancelled') else 'pending'
        conn.execute(
            '''INSERT INTO review_episodes(
                   id,sequence_no,review_type,title,original_due_at,current_due_at,
                   completed_at,status,delay_reason,notes,legacy_source_checkup_id,
                   created_at,updated_at
               ) VALUES (?,NULL,?,?,?,?,?,?,?,?,?,?,?)''',
            (review_id, review_type, checkup['title'], checkup['original_due_at'],
             checkup['current_due_at'], checkup['completed_at'], status,
             checkup['delay_reason'], checkup['summary_note'], checkup['id'], stamp, stamp),
        )
    conn.execute(
        '''INSERT OR IGNORE INTO review_components(
               id,review_id,checkup_id,component_role,notes,created_at
           ) VALUES (?,?,?,?,NULL,?)''',
        (ibd_db.new_id(), review_id, checkup['id'], component_role, ibd_db.now_iso()),
    )


def _migrate_v3_review_hierarchy_if_needed(conn: sqlite3.Connection) -> None:
    """Add review parents for explicit legacy diagnosis/review rows without copying tests."""
    profile = conn.execute("SELECT diagnosis_checkup_id FROM disease_profile WHERE id='current'").fetchone()
    diagnosis_id = profile['diagnosis_checkup_id'] if profile else None
    with conn:
        if diagnosis_id:
            diagnosis = conn.execute('SELECT * FROM checkups WHERE id=?', (diagnosis_id,)).fetchone()
            if diagnosis:
                _insert_legacy_review(
                    conn, checkup=diagnosis, review_type='diagnosis',
                    component_role='diagnostic_workup',
                )
        for checkup in conn.execute(
            "SELECT * FROM checkups WHERE title LIKE '%复查%' ORDER BY COALESCE(completed_at,current_due_at),id"
        ):
            if checkup['id'] == diagnosis_id:
                continue
            _insert_legacy_review(
                conn, checkup=checkup, review_type='scheduled',
                component_role='lab' if checkup['kind'] == 'lab' else 'other',
            )


def _date_or_none(value: str | None) -> str | None:
    if value is not None:
        ibd_db.validate_date(value)
    return value


def _timestamp(value: str) -> datetime:
    return ibd_db.parse_iso(value)


def _remind_at(event_at: str, days: int) -> str:
    return (_timestamp(event_at) - timedelta(days=days)).isoformat(timespec='seconds')


def _series(first_at: str, interval_days: int, through: str) -> list[str]:
    start = _timestamp(first_at)
    end = _timestamp(through)
    if end < start:
        return []
    result: list[str] = []
    current = start
    while current <= end:
        result.append(current.isoformat(timespec='seconds'))
        current += timedelta(days=interval_days)
    return result


def _add_months(value: datetime, months: int) -> datetime:
    if months < 0:
        raise ValueError('months must be non-negative')
    absolute = value.year * 12 + (value.month - 1) + months
    year, month_index = divmod(absolute, 12)
    month = month_index + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def _month_series(first_at: str, interval_months: int, through: str, last_at: str | None = None) -> list[str]:
    start = _timestamp(first_at)
    end = _timestamp(through)
    if last_at is not None:
        end = min(end, _timestamp(last_at))
    if end < start:
        return []
    result: list[str] = []
    index = 0
    while True:
        current = _add_months(start, index * interval_months)
        if current > end:
            return result
        result.append(current.isoformat(timespec='seconds'))
        index += 1


def get_profile(conn: sqlite3.Connection) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM disease_profile WHERE id='current'").fetchone()
    return dict(row) if row else None


def _validated_diagnosis_checkup(conn: sqlite3.Connection, identifier: str | None) -> str | None:
    if identifier is None:
        return None
    row = conn.execute('SELECT status FROM checkups WHERE id=?', (identifier,)).fetchone()
    if row is None:
        raise ValueError('diagnosis checkup not found')
    if row['status'] != 'completed':
        raise ValueError('diagnosis checkup must be completed before it can be linked')
    return identifier


def set_profile(
    conn: sqlite3.Connection, *, disease_type: str, earliest_symptom_date: str | None,
    diagnosis_checkup_id: str | None, notes: str | None,
) -> dict[str, Any]:
    _date_or_none(earliest_symptom_date)
    _validated_diagnosis_checkup(conn, diagnosis_checkup_id)
    stamp = ibd_db.now_iso()
    with conn:
        conn.execute(
            '''INSERT INTO disease_profile(
                   id,disease_type,earliest_symptom_date,diagnosis_checkup_id,notes,created_at,updated_at
               ) VALUES ('current',?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET
                   disease_type=excluded.disease_type,
                   earliest_symptom_date=excluded.earliest_symptom_date,
                   diagnosis_checkup_id=excluded.diagnosis_checkup_id,
                   notes=excluded.notes,
                   updated_at=excluded.updated_at''',
            (disease_type, earliest_symptom_date, diagnosis_checkup_id, notes, stamp, stamp),
        )
    return get_profile(conn) or {}


def _upsert_plan(conn: sqlite3.Connection, table: str, identifier: str | None, values: dict[str, Any]) -> dict[str, Any]:
    if table not in ('treatment_plans', 'review_plans'):
        raise ValueError('invalid plan table')
    identifier = identifier or ibd_db.new_id()
    existing = conn.execute(f'SELECT created_at FROM {table} WHERE id=?', (identifier,)).fetchone()
    stamp = ibd_db.now_iso()
    values = {**values, 'id': identifier, 'created_at': existing['created_at'] if existing else stamp, 'updated_at': stamp}
    columns = list(values)
    assignments = ','.join(f'{name}=excluded.{name}' for name in columns if name not in ('id', 'created_at'))
    placeholders = ','.join('?' for _ in columns)
    with conn:
        conn.execute(
            f"INSERT INTO {table}({','.join(columns)}) VALUES ({placeholders}) "
            f"ON CONFLICT(id) DO UPDATE SET {assignments}",
            tuple(values[name] for name in columns),
        )
    row = conn.execute(f'SELECT * FROM {table} WHERE id=?', (identifier,)).fetchone()
    return dict(row)


def set_treatment_plan(
    conn: sqlite3.Connection, *, identifier: str | None, drug_name: str, dose_note: str | None,
    interval_days: int, first_scheduled_at: str, pre_injection_lab_days: int | None,
    pre_injection_lab_title: str | None, reminder_advance_days: int, active: int, notes: str | None,
) -> dict[str, Any]:
    _timestamp(first_scheduled_at)
    if interval_days <= 0 or reminder_advance_days < 0 or (pre_injection_lab_days is not None and pre_injection_lab_days < 0):
        raise ValueError('plan intervals and reminder lead times must be non-negative; interval must be positive')
    return _upsert_plan(conn, 'treatment_plans', identifier, {
        'drug_name': drug_name, 'dose_note': dose_note, 'interval_days': interval_days,
        'first_scheduled_at': first_scheduled_at, 'pre_injection_lab_days': pre_injection_lab_days,
        'pre_injection_lab_title': pre_injection_lab_title, 'reminder_advance_days': reminder_advance_days,
        'active': active, 'notes': notes,
    })


def _has_treatment_occurrence(
    conn: sqlite3.Connection, plan_id: str, scheduled_at: str,
) -> bool:
    return conn.execute(
        '''SELECT 1 FROM treatment_plan_occurrences
           WHERE treatment_plan_id=? AND scheduled_at=?''',
        (plan_id, scheduled_at),
    ).fetchone() is not None


def _add_treatment_occurrence(
    conn: sqlite3.Connection, *, plan_id: str, scheduled_at: str, injection_id: str,
) -> str:
    identifier = ibd_db.new_id()
    with conn:
        conn.execute(
            '''INSERT INTO treatment_plan_occurrences(
                   id,treatment_plan_id,scheduled_at,injection_id,created_at
               ) VALUES (?,?,?,?,?)''',
            (identifier, plan_id, scheduled_at, injection_id, ibd_db.now_iso()),
        )
    return identifier


def generate_injections(conn: sqlite3.Connection, *, plan_id: str, through: str) -> list[dict[str, Any]]:
    _timestamp(through)
    plan = conn.execute('SELECT * FROM treatment_plans WHERE id=? AND active=1', (plan_id,)).fetchone()
    if plan is None:
        raise ValueError('active treatment plan not found')
    generated: list[dict[str, Any]] = []
    for scheduled_at in _series(plan['first_scheduled_at'], plan['interval_days'], through):
        if _has_treatment_occurrence(conn, plan_id, scheduled_at):
            continue
        injection_id = ibd_db.schedule_injection(
            conn, drug_name=plan['drug_name'], scheduled_at=scheduled_at,
            interval_days=plan['interval_days'], dose_note=plan['dose_note'],
            reminder_at=_remind_at(scheduled_at, plan['reminder_advance_days']),
        )
        _add_treatment_occurrence(conn, plan_id=plan_id, scheduled_at=scheduled_at, injection_id=injection_id)
        item: dict[str, Any] = {'scheduled_at': scheduled_at, 'injection_id': injection_id}
        if plan['pre_injection_lab_days'] is not None:
            lab_at = (_timestamp(scheduled_at) - timedelta(days=plan['pre_injection_lab_days'])).isoformat(timespec='seconds')
            checkup_id = ibd_db.schedule_checkup(
                conn, kind='lab', title=plan['pre_injection_lab_title'] or '输注前验血',
                due_at=lab_at, related_injection_id=injection_id, timing='pre_injection',
                reminder_at=_remind_at(lab_at, plan['reminder_advance_days']),
            )
            item['pre_injection_lab'] = {'due_at': lab_at, 'checkup_id': checkup_id}
        generated.append(item)
    return generated


REVIEW_TYPES = ('diagnosis', 'scheduled', 'first_year', 'annual', 'unscheduled', 'other')
REVIEW_COMPONENT_ROLES = (
    'lab', 'endoscopy', 'ct', 'mri', 'mre', 'pathology', 'visit',
    'assessment', 'diagnostic_workup', 'other',
)
REPORT_TYPES = ('lab', 'endoscopy', 'ct', 'mri', 'mre', 'pathology', 'visit', 'other')


def schedule_review(
    conn: sqlite3.Connection, *, title: str, review_type: str, due_at: str,
    sequence_no: int | None = None, notes: str | None = None,
    reminder_at: str | None = None,
) -> dict[str, Any]:
    _timestamp(due_at)
    if reminder_at is not None:
        _timestamp(reminder_at)
    if review_type not in REVIEW_TYPES:
        raise ValueError('invalid review_type')
    if sequence_no is not None and sequence_no <= 0:
        raise ValueError('sequence_no must be positive')
    identifier = ibd_db.new_id()
    stamp = ibd_db.now_iso()
    with conn:
        conn.execute(
            '''INSERT INTO review_episodes(
                   id,sequence_no,review_type,title,original_due_at,current_due_at,
                   status,notes,created_at,updated_at
               ) VALUES (?,?,?,?,?,?,'pending',?,?,?)''',
            (identifier, sequence_no, review_type, title, due_at, due_at, notes, stamp, stamp),
        )
        if reminder_at:
            conn.execute(
                '''INSERT INTO review_reminders(
                       id,review_id,remind_at,status,created_at,updated_at
                   ) VALUES (?,?,?,'pending',?,?)''',
                (ibd_db.new_id(), identifier, reminder_at, stamp, stamp),
            )
    return dict(conn.execute('SELECT * FROM review_episodes WHERE id=?', (identifier,)).fetchone())


def complete_review(
    conn: sqlite3.Connection, *, review_id: str, completed_at: str,
    notes: str | None = None,
) -> dict[str, Any]:
    _timestamp(completed_at)
    stamp = ibd_db.now_iso()
    with conn:
        row = conn.execute('SELECT * FROM review_episodes WHERE id=?', (review_id,)).fetchone()
        if row is None:
            raise ValueError('review not found')
        conn.execute(
            '''UPDATE review_episodes
               SET completed_at=?,status='completed',notes=COALESCE(?,notes),updated_at=?
               WHERE id=?''',
            (completed_at, notes, stamp, review_id),
        )
        conn.execute(
            "UPDATE review_reminders SET status='completed',updated_at=? WHERE review_id=? AND status='pending'",
            (stamp, review_id),
        )
    return dict(conn.execute('SELECT * FROM review_episodes WHERE id=?', (review_id,)).fetchone())


def link_review_component(
    conn: sqlite3.Connection, *, review_id: str, checkup_id: str,
    component_role: str, notes: str | None = None,
) -> dict[str, Any]:
    if component_role not in REVIEW_COMPONENT_ROLES:
        raise ValueError('invalid review component role')
    if conn.execute('SELECT 1 FROM review_episodes WHERE id=?', (review_id,)).fetchone() is None:
        raise ValueError('review not found')
    if conn.execute('SELECT 1 FROM checkups WHERE id=?', (checkup_id,)).fetchone() is None:
        raise ValueError('checkup not found')
    identifier = ibd_db.new_id()
    with conn:
        conn.execute(
            '''INSERT INTO review_components(
                   id,review_id,checkup_id,component_role,notes,created_at
               ) VALUES (?,?,?,?,?,?)
               ON CONFLICT(review_id,checkup_id) DO UPDATE SET
                   component_role=excluded.component_role,
                   notes=excluded.notes''',
            (identifier, review_id, checkup_id, component_role, notes, ibd_db.now_iso()),
        )
    row = conn.execute(
        'SELECT * FROM review_components WHERE review_id=? AND checkup_id=?',
        (review_id, checkup_id),
    ).fetchone()
    return dict(row)


def record_checkup_report(
    conn: sqlite3.Connection, *, checkup_id: str, report_type: str,
    reported_at: str | None, source_organization: str | None,
    findings_text: str | None, impression_text: str | None,
    original_text: str | None, attachment_ref: str | None,
) -> dict[str, Any]:
    if report_type not in REPORT_TYPES:
        raise ValueError('invalid report_type')
    if reported_at is not None:
        _timestamp(reported_at)
    if not any((findings_text, impression_text, original_text, attachment_ref)):
        raise ValueError('a report needs text or an attachment reference')
    checkup = conn.execute('SELECT status FROM checkups WHERE id=?', (checkup_id,)).fetchone()
    if checkup is None:
        raise ValueError('checkup not found')
    if checkup['status'] != 'completed':
        raise ValueError('checkup must be completed before recording a report')
    stamp = ibd_db.now_iso()
    with conn:
        prior = conn.execute(
            '''SELECT * FROM checkup_reports
               WHERE checkup_id=? AND report_type=? AND is_current=1''',
            (checkup_id, report_type),
        ).fetchone()
        version_no = prior['version_no'] + 1 if prior else 1
        if prior:
            conn.execute('UPDATE checkup_reports SET is_current=0 WHERE id=?', (prior['id'],))
        identifier = ibd_db.new_id()
        conn.execute(
            '''INSERT INTO checkup_reports(
                   id,checkup_id,report_type,version_no,supersedes_id,is_current,
                   reported_at,source_organization,findings_text,impression_text,
                   original_text,attachment_ref,created_at
               ) VALUES (?,?,?,?,?,1,?,?,?,?,?,?,?)''',
            (identifier, checkup_id, report_type, version_no, prior['id'] if prior else None,
             reported_at, source_organization, findings_text, impression_text,
             original_text, attachment_ref, stamp),
        )
    return dict(conn.execute('SELECT * FROM checkup_reports WHERE id=?', (identifier,)).fetchone())


def set_review_plan(
    conn: sqlite3.Connection, *, identifier: str | None, title: str,
    review_type: str, interval_months: int, first_due_at: str,
    last_due_at: str | None, reminder_advance_days: int,
    active: int, notes: str | None,
) -> dict[str, Any]:
    _timestamp(first_due_at)
    if last_due_at is not None:
        _timestamp(last_due_at)
    if review_type not in ('scheduled', 'first_year', 'annual', 'other'):
        raise ValueError('invalid review plan type')
    if interval_months <= 0 or reminder_advance_days < 0:
        raise ValueError('review plan intervals and reminder lead times are invalid')
    if last_due_at is not None and _timestamp(last_due_at) < _timestamp(first_due_at):
        raise ValueError('last_due_at cannot precede first_due_at')
    return _upsert_plan(conn, 'review_plans', identifier, {
        'title': title, 'review_type': review_type, 'interval_months': interval_months,
        'first_due_at': first_due_at, 'last_due_at': last_due_at,
        'reminder_advance_days': reminder_advance_days, 'active': active, 'notes': notes,
    })


def _review_matches_due_date(review: sqlite3.Row, due_at: str) -> bool:
    """Match date-only planning anchors without treating different days as one event."""
    due_date = _timestamp(due_at).date()
    return any(
        value is not None and _timestamp(value).date() == due_date
        for value in (review['original_due_at'], review['current_due_at'], review['completed_at'])
    )


def _unlinked_existing_reviews_for_due_date(
    conn: sqlite3.Connection, due_at: str,
) -> list[sqlite3.Row]:
    """Find one historical/hand-entered review that can receive plan provenance."""
    candidates = conn.execute(
        '''SELECT r.* FROM review_episodes r
           WHERE r.status <> 'cancelled'
             AND NOT EXISTS (
                 SELECT 1 FROM review_plan_occurrences o WHERE o.review_id=r.id
             )'''
    )
    return [row for row in candidates if _review_matches_due_date(row, due_at)]


def _add_review_occurrence(
    conn: sqlite3.Connection, *, plan_id: str, scheduled_at: str, review_id: str,
) -> None:
    with conn:
        conn.execute(
            '''INSERT INTO review_plan_occurrences(
                   id,review_plan_id,scheduled_at,review_id,created_at
               ) VALUES (?,?,?,?,?)''',
            (ibd_db.new_id(), plan_id, scheduled_at, review_id, ibd_db.now_iso()),
        )


def generate_reviews(conn: sqlite3.Connection, *, plan_id: str, through: str) -> list[dict[str, Any]]:
    _timestamp(through)
    plan = conn.execute('SELECT * FROM review_plans WHERE id=? AND active=1', (plan_id,)).fetchone()
    if plan is None:
        raise ValueError('active review plan not found')
    generated: list[dict[str, Any]] = []
    for due_at in _month_series(
        plan['first_due_at'], plan['interval_months'], through, plan['last_due_at']
    ):
        if conn.execute(
            'SELECT 1 FROM review_plan_occurrences WHERE review_plan_id=? AND scheduled_at=?',
            (plan_id, due_at),
        ).fetchone():
            continue
        existing = _unlinked_existing_reviews_for_due_date(conn, due_at)
        if len(existing) > 1:
            raise ValueError(
                f'multiple unlinked reviews match planned date {due_at[:10]}; link one explicitly before generation'
            )
        if existing:
            _add_review_occurrence(
                conn, plan_id=plan_id, scheduled_at=due_at, review_id=existing[0]['id'],
            )
            generated.append({
                'due_at': due_at, 'review_id': existing[0]['id'], 'linked_existing': True,
            })
            continue
        review = schedule_review(
            conn, title=plan['title'], review_type=plan['review_type'], due_at=due_at,
            notes=plan['notes'], reminder_at=_remind_at(due_at, plan['reminder_advance_days']),
        )
        _add_review_occurrence(conn, plan_id=plan_id, scheduled_at=due_at, review_id=review['id'])
        generated.append({'due_at': due_at, 'review_id': review['id']})
    return generated


def review_detail(conn: sqlite3.Connection, *, review_id: str) -> dict[str, Any]:
    review = conn.execute('SELECT * FROM review_episodes WHERE id=?', (review_id,)).fetchone()
    if review is None:
        raise ValueError('review not found')
    components = []
    for row in conn.execute(
        '''SELECT rc.*,c.kind,c.title,c.status,c.completed_at,c.related_injection_id,c.timing
           FROM review_components rc JOIN checkups c ON c.id=rc.checkup_id
           WHERE rc.review_id=? ORDER BY COALESCE(c.completed_at,c.current_due_at),rc.created_at''',
        (review_id,),
    ):
        item = dict(row)
        item['results'] = [dict(result) for result in conn.execute(
            '''SELECT r.*,m.display_name,m.value_type
               FROM checkup_results r JOIN metric_definitions m ON m.code=r.metric_code
               WHERE r.checkup_id=? ORDER BY m.display_name''',
            (row['checkup_id'],),
        )]
        item['reports'] = [dict(report) for report in conn.execute(
            '''SELECT * FROM checkup_reports
               WHERE checkup_id=? AND is_current=1 ORDER BY report_type''',
            (row['checkup_id'],),
        )]
        item['assessments'] = [dict(assessment) for assessment in conn.execute(
            '''SELECT * FROM checkup_assessments
               WHERE checkup_id=? AND is_current=1 ORDER BY confirmed_at''',
            (row['checkup_id'],),
        )]
        components.append(item)
    return {'review': dict(review), 'components': components}


def _locations_json(locations: list[str]) -> str:
    clean = [item.strip() for item in locations if item.strip()]
    if len(clean) != len(set(clean)):
        raise ValueError('affected locations must not repeat')
    return json.dumps(clean, ensure_ascii=False)


def record_checkup_assessment(
    conn: sqlite3.Connection, *, checkup_id: str, disease_status: str | None,
    affected_locations: list[str], severity: str | None, original_conclusion: str | None,
    confirmed_at: str,
) -> dict[str, Any]:
    _timestamp(confirmed_at)
    if disease_status not in (None, 'active', 'remission', 'flaring', 'unknown'):
        raise ValueError('invalid disease_status')
    if severity not in (None, 'mild', 'moderate', 'severe', 'unknown'):
        raise ValueError('invalid severity')
    locations_json = _locations_json(affected_locations)
    if disease_status is None and locations_json == '[]' and severity is None and not original_conclusion:
        raise ValueError('an assessment needs at least one confirmed conclusion')
    checkup = conn.execute('SELECT status FROM checkups WHERE id=?', (checkup_id,)).fetchone()
    if checkup is None:
        raise ValueError('checkup not found')
    if checkup['status'] != 'completed':
        raise ValueError('checkup must be completed before recording a confirmed assessment')
    stamp = ibd_db.now_iso()
    with conn:
        prior = conn.execute(
            'SELECT * FROM checkup_assessments WHERE checkup_id=? AND is_current=1', (checkup_id,)
        ).fetchone()
        version_no = (prior['version_no'] + 1) if prior else 1
        if prior:
            conn.execute('UPDATE checkup_assessments SET is_current=0 WHERE id=?', (prior['id'],))
        identifier = ibd_db.new_id()
        conn.execute(
            '''INSERT INTO checkup_assessments(
                   id,checkup_id,version_no,supersedes_id,is_current,disease_status,
                   affected_locations_json,severity,original_conclusion,confirmed_at,created_at
               ) VALUES (?,?,?,?,1,?,?,?,?,?,?)''',
            (identifier, checkup_id, version_no, prior['id'] if prior else None, disease_status,
             locations_json, severity, original_conclusion, confirmed_at, stamp),
        )
    return dict(conn.execute('SELECT * FROM checkup_assessments WHERE id=?', (identifier,)).fetchone())


def create_manual_symptom_baseline(
    conn: sqlite3.Connection, *, stool_total: float | None, pain_max: float | None,
    bloating_score: float | None, blood: str | None, urgency: str | None,
    night_stool: str | None, notes: str | None,
) -> dict[str, Any]:
    return _create_baseline(
        conn, status='draft', source='manual', stool_total=stool_total, pain_max=pain_max,
        bloating_score=bloating_score, blood=blood, urgency=urgency, night_stool=night_stool,
        source_start_date=None, source_end_date=None, evidence=None, notes=notes,
    )


def _create_baseline(
    conn: sqlite3.Connection, *, status: str, source: str, stool_total: float | None,
    pain_max: float | None, bloating_score: float | None, blood: str | None,
    urgency: str | None, night_stool: str | None, source_start_date: str | None,
    source_end_date: str | None, evidence: dict[str, Any] | None, notes: str | None,
) -> dict[str, Any]:
    if status not in ('draft', 'candidate'):
        raise ValueError('new symptom baselines must start as draft or candidate')
    if source not in ('manual', 'daily_records'):
        raise ValueError('invalid baseline source')
    if stool_total is not None and stool_total < 0:
        raise ValueError('stool_total must be non-negative')
    for value, name in ((pain_max, 'pain_max'), (bloating_score, 'bloating_score')):
        if value is not None and not 0 <= value <= 10:
            raise ValueError(f'{name} must be between 0 and 10')
    for value in (blood, urgency, night_stool):
        if value not in (None, 'yes', 'no', 'unknown'):
            raise ValueError('invalid yes/no/unknown baseline field')
    _date_or_none(source_start_date)
    _date_or_none(source_end_date)
    if source_start_date and source_end_date and source_start_date > source_end_date:
        raise ValueError('baseline source range is invalid')
    identifier = ibd_db.new_id()
    stamp = ibd_db.now_iso()
    with conn:
        conn.execute(
            '''INSERT INTO symptom_baselines(
                   id,status,source,stool_total,pain_max,bloating_score,blood,urgency,night_stool,
                   source_start_date,source_end_date,evidence_json,notes,created_at,updated_at
               ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (identifier, status, source, stool_total, pain_max, bloating_score, blood, urgency,
             night_stool, source_start_date, source_end_date,
             json.dumps(evidence, ensure_ascii=False, sort_keys=True) if evidence else None,
             notes, stamp, stamp),
        )
    return dict(conn.execute('SELECT * FROM symptom_baselines WHERE id=?', (identifier,)).fetchone())


def generate_symptom_baseline_candidate(
    conn: sqlite3.Connection, *, start_date: str, end_date: str, notes: str | None = None,
) -> dict[str, Any]:
    ibd_db.validate_date(start_date)
    ibd_db.validate_date(end_date)
    if start_date > end_date:
        raise ValueError('candidate date range is invalid')
    dates = [
        row['log_date'] for row in conn.execute(
            'SELECT DISTINCT log_date FROM symptom_logs WHERE log_date BETWEEN ? AND ? ORDER BY log_date',
            (start_date, end_date),
        )
    ]
    daily = [ibd_db.aggregate_day(conn, value) for value in dates]
    qualifying = [
        item for item in daily
        if item['overall_vs_usual'] == 'usual' or item['back_to_usual'] == 1
    ]
    if len(qualifying) < 7:
        raise ValueError('at least 7 explicitly usual or back-to-usual recorded days are required for a candidate')

    def median_or_none(field: str) -> float | None:
        values = [item[field] for item in qualifying if item[field] is not None]
        return ibd_db._median(values)

    def usual_tri(field: str) -> str | None:
        values = [item[field] for item in qualifying if item[field] is not None]
        if not values:
            return None
        return 'yes' if 'yes' in values else 'no' if 'no' in values else None

    evidence = {
        'method': 'explicitly_recorded_usual_or_back_to_usual_days',
        'source_start_date': start_date,
        'source_end_date': end_date,
        'recorded_days': len(daily),
        'qualifying_days': len(qualifying),
        'qualifying_dates': [item['log_date'] for item in qualifying],
        'not_a_clinical_status_inference': True,
    }
    return _create_baseline(
        conn, status='candidate', source='daily_records',
        stool_total=median_or_none('stool_total'), pain_max=median_or_none('pain_max'),
        bloating_score=median_or_none('bloating_max'), blood=usual_tri('blood_any'), urgency=usual_tri('urgency_any'),
        night_stool=usual_tri('night_stool_any'), source_start_date=start_date,
        source_end_date=end_date, evidence=evidence, notes=notes,
    )


def confirm_symptom_baseline(conn: sqlite3.Connection, *, identifier: str, confirmed_at: str) -> dict[str, Any]:
    _timestamp(confirmed_at)
    stamp = ibd_db.now_iso()
    with conn:
        candidate = conn.execute('SELECT * FROM symptom_baselines WHERE id=?', (identifier,)).fetchone()
        if candidate is None:
            raise ValueError('symptom baseline not found')
        if candidate['status'] not in ('draft', 'candidate'):
            raise ValueError('only a draft or candidate baseline can be confirmed')
        existing = conn.execute("SELECT * FROM symptom_baselines WHERE status='confirmed'").fetchone()
        if existing:
            conn.execute(
                "UPDATE symptom_baselines SET status='historical',superseded_at=?,updated_at=? WHERE id=?",
                (confirmed_at, stamp, existing['id']),
            )
        conn.execute(
            "UPDATE symptom_baselines SET status='confirmed',confirmed_at=?,replaces_id=?,updated_at=? WHERE id=?",
            (confirmed_at, existing['id'] if existing else None, stamp, identifier),
        )
    return dict(conn.execute('SELECT * FROM symptom_baselines WHERE id=?', (identifier,)).fetchone())


def current_summary(conn: sqlite3.Connection) -> dict[str, Any]:
    profile = get_profile(conn)
    diagnosis_record = None
    if profile and profile['diagnosis_checkup_id']:
        row = conn.execute('SELECT * FROM checkups WHERE id=?', (profile['diagnosis_checkup_id'],)).fetchone()
        diagnosis_record = dict(row) if row else None
    latest_assessment = conn.execute(
        '''SELECT a.*,c.kind AS checkup_kind,c.title AS checkup_title,c.completed_at AS checkup_completed_at
           FROM checkup_assessments a JOIN checkups c ON c.id=a.checkup_id
           WHERE a.is_current=1 AND c.status='completed'
           ORDER BY c.completed_at DESC,a.confirmed_at DESC,a.created_at DESC LIMIT 1'''
    ).fetchone()
    baseline = conn.execute(
        "SELECT * FROM symptom_baselines WHERE status='confirmed' ORDER BY confirmed_at DESC LIMIT 1"
    ).fetchone()
    latest_review = conn.execute(
        '''SELECT r.*,COUNT(rc.id) AS component_count
           FROM review_episodes r
           LEFT JOIN review_components rc ON rc.review_id=r.id
           WHERE r.status='completed'
           GROUP BY r.id
           ORDER BY r.completed_at DESC,r.updated_at DESC LIMIT 1'''
    ).fetchone()
    return {
        'disease_profile': profile,
        'diagnosis_checkup': diagnosis_record,
        'latest_confirmed_checkup_assessment': dict(latest_assessment) if latest_assessment else None,
        'active_treatment_plans': [dict(row) for row in conn.execute('SELECT * FROM treatment_plans WHERE active=1 ORDER BY first_scheduled_at')],
        'active_review_plans': [dict(row) for row in conn.execute('SELECT * FROM review_plans WHERE active=1 ORDER BY first_due_at')],
        'latest_completed_review': dict(latest_review) if latest_review else None,
        'active_symptom_baseline': dict(baseline) if baseline else None,
    }


def overview(conn: sqlite3.Connection) -> dict[str, Any]:
    state = current_summary(conn)
    state.update({
        'review_episodes': [dict(row) for row in conn.execute(
            '''SELECT r.*,COUNT(rc.id) AS component_count
               FROM review_episodes r LEFT JOIN review_components rc ON rc.review_id=r.id
               GROUP BY r.id ORDER BY r.current_due_at'''
        )],
        'planned_injections': [dict(row) for row in conn.execute(
            '''SELECT o.treatment_plan_id,o.scheduled_at,o.injection_id,
                      i.status AS injection_status
                 FROM treatment_plan_occurrences o
                 JOIN injections i ON i.id=o.injection_id
                 ORDER BY o.scheduled_at'''
        )],
        'pending_symptom_baselines': [dict(row) for row in conn.execute(
            "SELECT * FROM symptom_baselines WHERE status IN ('draft','candidate') ORDER BY created_at"
        )],
    })
    return state


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Private IBD care-plan and confirmed-context extension')
    parser.add_argument('--db', type=Path, default=ibd_db.DEFAULT_DB)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    sub.add_parser('overview')
    sub.add_parser('current-summary')

    p = sub.add_parser('set-profile')
    p.add_argument('--disease-type', default='Crohn')
    p.add_argument('--earliest-symptom-date')
    p.add_argument('--diagnosis-checkup-id')
    p.add_argument('--notes')

    p = sub.add_parser('set-treatment-plan')
    p.add_argument('--id')
    p.add_argument('--drug', required=True)
    p.add_argument('--dose-note')
    p.add_argument('--interval-days', required=True, type=int)
    p.add_argument('--first-scheduled-at', required=True)
    p.add_argument('--pre-injection-lab-days', type=int)
    p.add_argument('--pre-injection-lab-title')
    p.add_argument('--reminder-advance-days', type=int, default=1)
    p.add_argument('--inactive', action='store_true')
    p.add_argument('--notes')

    p = sub.add_parser('generate-injections')
    p.add_argument('--plan-id', required=True)
    p.add_argument('--through', required=True)
    p = sub.add_parser('schedule-review')
    p.add_argument('--title', required=True)
    p.add_argument('--review-type', required=True, choices=REVIEW_TYPES)
    p.add_argument('--due-at', required=True)
    p.add_argument('--sequence', type=int)
    p.add_argument('--notes')
    p.add_argument('--remind-at')

    p = sub.add_parser('complete-review')
    p.add_argument('--id', required=True)
    p.add_argument('--completed-at', required=True)
    p.add_argument('--notes')

    p = sub.add_parser('link-review-component')
    p.add_argument('--review-id', required=True)
    p.add_argument('--checkup-id', required=True)
    p.add_argument('--role', required=True, choices=REVIEW_COMPONENT_ROLES)
    p.add_argument('--notes')

    p = sub.add_parser('add-checkup-report')
    p.add_argument('--checkup-id', required=True)
    p.add_argument('--report-type', required=True, choices=REPORT_TYPES)
    p.add_argument('--reported-at')
    p.add_argument('--source-organization')
    p.add_argument('--findings')
    p.add_argument('--impression')
    p.add_argument('--original-text')
    p.add_argument('--attachment-ref')

    p = sub.add_parser('review-detail')
    p.add_argument('--id', required=True)

    p = sub.add_parser('set-review-plan')
    p.add_argument('--id')
    p.add_argument('--title', required=True)
    p.add_argument('--review-type', required=True, choices=('scheduled','first_year','annual','other'))
    p.add_argument('--interval-months', required=True, type=int)
    p.add_argument('--first-due-at', required=True)
    p.add_argument('--last-due-at')
    p.add_argument('--reminder-advance-days', type=int, default=14)
    p.add_argument('--inactive', action='store_true')
    p.add_argument('--notes')

    p = sub.add_parser('generate-reviews')
    p.add_argument('--plan-id', required=True)
    p.add_argument('--through', required=True)

    p = sub.add_parser('record-checkup-assessment')
    p.add_argument('--checkup-id', required=True)
    p.add_argument('--disease-status', choices=('active','remission','flaring','unknown'))
    p.add_argument('--affected-location', action='append', default=[])
    p.add_argument('--severity', choices=('mild','moderate','severe','unknown'))
    p.add_argument('--original-conclusion')
    p.add_argument('--confirmed-at', required=True)

    p = sub.add_parser('create-manual-baseline')
    p.add_argument('--stool-total', type=float)
    p.add_argument('--pain-max', type=float)
    p.add_argument('--bloating-score', type=float)
    p.add_argument('--blood', choices=('yes','no','unknown'))
    p.add_argument('--urgency', choices=('yes','no','unknown'))
    p.add_argument('--night-stool', choices=('yes','no','unknown'))
    p.add_argument('--notes')

    p = sub.add_parser('generate-baseline-candidate')
    p.add_argument('--start-date', required=True)
    p.add_argument('--end-date', required=True)
    p.add_argument('--notes')

    p = sub.add_parser('confirm-baseline')
    p.add_argument('--id', required=True)
    p.add_argument('--confirmed-at', required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ibd_db.storage_notice(args.db)
    conn = open_care_db(args.db)
    if args.command == 'init':
        print_json({'database': str(Path(args.db).expanduser()), 'user_version': conn.execute('PRAGMA user_version').fetchone()[0]})
    elif args.command == 'overview':
        print_json(overview(conn))
    elif args.command == 'current-summary':
        print_json(current_summary(conn))
    elif args.command == 'set-profile':
        print_json(set_profile(conn, disease_type=args.disease_type,
                               earliest_symptom_date=args.earliest_symptom_date,
                               diagnosis_checkup_id=args.diagnosis_checkup_id, notes=args.notes))
    elif args.command == 'set-treatment-plan':
        print_json(set_treatment_plan(conn, identifier=args.id, drug_name=args.drug, dose_note=args.dose_note,
                   interval_days=args.interval_days, first_scheduled_at=args.first_scheduled_at,
                   pre_injection_lab_days=args.pre_injection_lab_days,
                   pre_injection_lab_title=args.pre_injection_lab_title,
                   reminder_advance_days=args.reminder_advance_days, active=0 if args.inactive else 1, notes=args.notes))
    elif args.command == 'generate-injections':
        print_json(generate_injections(conn, plan_id=args.plan_id, through=args.through))
    elif args.command == 'schedule-review':
        print_json(schedule_review(
            conn, title=args.title, review_type=args.review_type, due_at=args.due_at,
            sequence_no=args.sequence, notes=args.notes, reminder_at=args.remind_at,
        ))
    elif args.command == 'complete-review':
        print_json(complete_review(
            conn, review_id=args.id, completed_at=args.completed_at, notes=args.notes,
        ))
    elif args.command == 'link-review-component':
        print_json(link_review_component(
            conn, review_id=args.review_id, checkup_id=args.checkup_id,
            component_role=args.role, notes=args.notes,
        ))
    elif args.command == 'add-checkup-report':
        print_json(record_checkup_report(
            conn, checkup_id=args.checkup_id, report_type=args.report_type,
            reported_at=args.reported_at, source_organization=args.source_organization,
            findings_text=args.findings, impression_text=args.impression,
            original_text=args.original_text, attachment_ref=args.attachment_ref,
        ))
    elif args.command == 'review-detail':
        print_json(review_detail(conn, review_id=args.id))
    elif args.command == 'set-review-plan':
        print_json(set_review_plan(
            conn, identifier=args.id, title=args.title, review_type=args.review_type,
            interval_months=args.interval_months, first_due_at=args.first_due_at,
            last_due_at=args.last_due_at, reminder_advance_days=args.reminder_advance_days,
            active=0 if args.inactive else 1, notes=args.notes,
        ))
    elif args.command == 'generate-reviews':
        print_json(generate_reviews(conn, plan_id=args.plan_id, through=args.through))
    elif args.command == 'record-checkup-assessment':
        print_json(record_checkup_assessment(
            conn, checkup_id=args.checkup_id, disease_status=args.disease_status,
            affected_locations=args.affected_location, severity=args.severity,
            original_conclusion=args.original_conclusion, confirmed_at=args.confirmed_at,
        ))
    elif args.command == 'create-manual-baseline':
        print_json(create_manual_symptom_baseline(
            conn, stool_total=args.stool_total, pain_max=args.pain_max,
            bloating_score=args.bloating_score, blood=args.blood, urgency=args.urgency,
            night_stool=args.night_stool, notes=args.notes,
        ))
    elif args.command == 'generate-baseline-candidate':
        print_json(generate_symptom_baseline_candidate(
            conn, start_date=args.start_date, end_date=args.end_date, notes=args.notes,
        ))
    elif args.command == 'confirm-baseline':
        print_json(confirm_symptom_baseline(conn, identifier=args.id, confirmed_at=args.confirmed_at))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, sqlite3.IntegrityError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
