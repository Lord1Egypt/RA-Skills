#!/usr/bin/env python3
"""Durable, scoped run journal. Recorded host IDs are claims, not host verification.

SQLite is authoritative; JSONL export is a derived replay view. A hash chain
detects accidental edits but is not a signature against a privileged writer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from artifact_contract import (validate_audit_identity, validate_operational_identity,
                               validate_receipt_identity, validate_runtime_event_identity)


STAGES = ('intake', 'inventory', 'analysis', 'adjudication', 'draft', 'review', 'complete')
ROLES = ('data-analyst', 'platform-ops', 'content-live-growth', 'ad-profit-optimizer', 'delivery-review')
SENSITIVE = re.compile(r'(password|secret_value|access_token|refresh_token|authorization|cookie|api_key)', re.I)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(encoded(value).encode('utf-8')).hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def check_payload(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if SENSITIVE.search(key):
                raise ValueError('credential_field_not_allowed')
            check_payload(child)
    elif isinstance(value, list):
        for child in value:
            check_payload(child)


class Journal:
    def __init__(self, db_path, read_only=False, existing_only=False):
        use_uri = read_only or existing_only
        location = (Path(db_path).resolve().as_uri() + ('?mode=ro' if read_only else '?mode=rw')
                    if use_uri else str(db_path))
        self.db = sqlite3.connect(location, uri=use_uri, timeout=20, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        if read_only or existing_only:
            return
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY, client_scope TEXT NOT NULL,
            team_version TEXT NOT NULL, task_type TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS events (
            run_id TEXT NOT NULL REFERENCES runs(run_id), seq INTEGER NOT NULL,
            event_key TEXT NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL,
            created_at TEXT NOT NULL, previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL,
            PRIMARY KEY(run_id,seq), UNIQUE(run_id,event_key));
          CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events
            BEGIN SELECT RAISE(ABORT,'append_only'); END;
          CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events
            BEGIN SELECT RAISE(ABORT,'append_only'); END;
        ''')

    def close(self):
        self.db.close()

    def create(self, run_id, client_scope, version, task_type):
        if not all(isinstance(v, str) and v.strip() for v in (run_id, client_scope, version, task_type)):
            raise ValueError('run_identity_missing')
        identity = (run_id, client_scope, version, task_type)
        with self.transaction():
            old = self.db.execute('SELECT * FROM runs WHERE run_id=?', (run_id,)).fetchone()
            if old and tuple(old) != identity:
                raise ValueError('run_identity_conflict')
            self.db.execute('INSERT OR IGNORE INTO runs VALUES (?,?,?,?)', identity)

    def transaction(self):
        from contextlib import contextmanager
        @contextmanager
        def scope():
            self.db.execute('BEGIN IMMEDIATE')
            try:
                yield
                self.db.execute('COMMIT')
            except BaseException:
                self.db.execute('ROLLBACK')
                raise
        return scope()

    def events(self, run_id, client_scope):
        identity = self.db.execute('SELECT * FROM runs WHERE run_id=?', (run_id,)).fetchone()
        if not identity or identity['client_scope'] != client_scope:
            raise ValueError('run_scope_mismatch')
        rows = [dict(row) for row in self.db.execute('SELECT * FROM events WHERE run_id=? ORDER BY seq', (run_id,))]
        previous = ''
        for seq, row in enumerate(rows, 1):
            actual = row.pop('event_hash')
            if row['seq'] != seq or row['previous_hash'] != previous or digest(row) != actual:
                raise ValueError('audit_chain_invalid')
            row['event_hash'] = actual
            row['payload'] = json.loads(row['body'])
            previous = actual
        return rows

    def append(self, run_id, client_scope, event_key, kind, payload):
        if not event_key or not isinstance(payload, dict):
            raise ValueError('event_invalid')
        check_payload(payload)
        with self.transaction():
            return self.append_locked(run_id,client_scope,event_key,kind,payload)

    def append_locked(self,run_id,client_scope,event_key,kind,payload):
        """Internal append for a caller already holding an immediate transaction."""
        if not self.db.in_transaction:
            raise ValueError('audit_transaction_required')
        check_payload(payload)
        body=encoded(payload)
        rows = self.events(run_id, client_scope)
        run = self.db.execute('SELECT team_version FROM runs WHERE run_id=?', (run_id,)).fetchone()
        operational_kind = ('platform_read' if kind == 'platform_read_observed' else
            'policy_decision' if kind == 'action_policy_decision' else
            'connector_call' if kind in
            ('action_call_reserved','action_call_returned','action_call_uncertain','action_call_aborted') else
            'readback' if kind == 'action_call_readback' else
            'outcome' if kind == 'action_call_outcome' else None)
        if operational_kind:
            validate_operational_identity(payload, operational_kind, run['team_version'])
        audit_kind = ('model_observation' if kind == 'model_observation' else
            'human_feedback' if kind == 'human_correction' else
            'quality_observation' if kind == 'quality_observation' else
            'monitor_policy' if kind == 'monitor_policy' else
            'monitor_comparison' if kind == 'monitor_comparison' else None)
        if audit_kind:
            validate_audit_identity(payload, audit_kind, run['team_version'])
        if kind.startswith('member_') or kind.startswith('challenge_'):
            validate_runtime_event_identity(payload, kind, run['team_version'])
        if kind == 'delivery_completed':
            validate_receipt_identity(payload, 'completion_event', run['team_version'])
        if kind == 'intake_blocked':
            validate_receipt_identity(payload, 'intake_blocked_event', run['team_version'])
        old = next((r for r in rows if r['event_key'] == event_key), None)
        if old:
            if old['kind'] != kind or old['body'] != body:
                raise ValueError('idempotency_key_conflict')
            return old['event_hash']
        self.validate_event(rows, kind, payload)
        row = dict(run_id=run_id, seq=len(rows)+1, event_key=event_key,
                   kind=kind, body=body, created_at=utc_now(),
                   previous_hash=rows[-1]['event_hash'] if rows else '')
        event_hash = digest(row)
        self.db.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?)', (*row.values(), event_hash))
        return event_hash

    @staticmethod
    def validate_event(rows, kind, p):
        if kind == 'phase':
            previous = [r['payload']['phase'] for r in rows if r['kind'] == 'phase']
            current = previous[-1] if previous else 'intake'
            # Formal completion is deliberately owned by completion_gate, never a phase label.
            target = p.get('phase')
            if target not in STAGES[:-1] or STAGES.index(target) != STAGES.index(current)+1:
                raise ValueError('phase_transition_invalid')
        elif kind in ('member_started', 'member_returned', 'member_failed', 'member_rejected'):
            if p.get('role') not in ROLES or not all(p.get(k) for k in ('host', 'agent_task_id', 'attempt_id')):
                raise ValueError('member_identity_missing')
            identity = tuple(p[k] for k in ('role','host','agent_task_id','attempt_id'))
            matching = [r for r in rows if r['kind'].startswith('member_') and
                        tuple(r['payload'].get(k) for k in ('role','host','agent_task_id','attempt_id')) == identity]
            if kind == 'member_started':
                if matching:
                    raise ValueError('attempt_already_started')
                starts=[r['payload'] for r in rows if r['kind']=='member_started']
                if any(r['kind']=='member_returned' and r['payload']['role']==p['role'] for r in rows):
                    raise ValueError('member_already_returned')
                if any(x['role']!=p['role'] and x['host']==p['host'] and
                       x['agent_task_id']==p['agent_task_id'] for x in starts):
                    raise ValueError('task_reused_across_roles')
                if any(x['role']==p['role'] and x['attempt_id']==p['attempt_id'] for x in starts):
                    raise ValueError('attempt_task_id_conflict')
                failures=[r for r in rows if r['kind'] in ('member_failed','member_rejected') and
                          r['payload']['role']==p['role']]
                if len(failures)>=2:
                    raise ValueError('member_retry_exhausted')
                terminal={(r['payload']['role'],r['payload']['attempt_id']) for r in rows
                          if r['kind'] in ('member_returned','member_failed','member_rejected')}
                if any(x['role']==p['role'] and (x['role'],x['attempt_id']) not in terminal for x in starts):
                    raise ValueError('role_still_waiting')
            else:
                if not matching or matching[-1]['kind'] != 'member_started':
                    raise ValueError('member_not_waiting')
                if kind == 'member_returned' and not re.fullmatch('[0-9a-f]{64}', str(p.get('handoff_sha256',''))):
                    raise ValueError('handoff_hash_missing')
                if kind == 'member_rejected' and (not p.get('reason') or p.get('host_state')!='completed'):
                    raise ValueError('rejected_return_observation_missing')
        elif kind in ('challenge_started','challenge_returned','challenge_failed','challenge_rejected'):
            if p.get('role') not in ROLES[:-1] or not all(p.get(k) for k in ('round_id','host','agent_task_id','observation_file','observation_sha256')):
                raise ValueError('challenge_identity_missing')
            matching=[r for r in rows if r['kind'].startswith('challenge_') and
                      r['payload'].get('round_id')==p['round_id'] and r['payload'].get('role')==p['role']]
            if kind=='challenge_started':
                if matching: raise ValueError('challenge_round_already_started')
                if not all(p.get(k) for k in ('request_file','request_sha256','identity','inputs','conflict_ids')):
                    raise ValueError('challenge_request_missing')
            else:
                if len(matching)!=1 or matching[0]['kind']!='challenge_started':
                    raise ValueError('challenge_not_waiting')
                if any(matching[0]['payload'][k]!=p[k] for k in ('host','agent_task_id')):
                    raise ValueError('challenge_task_changed')
                if kind=='challenge_returned' and not all(p.get(k) for k in ('response_file','response_sha256')):
                    raise ValueError('challenge_response_missing')
                if kind=='challenge_rejected' and (p.get('host_state')!='completed' or not p.get('reason')):
                    raise ValueError('challenge_rejection_invalid')
        elif kind == 'model_observation':
            if not p.get('model_alias') or not p.get('task_class'):
                raise ValueError('model_identity_missing')
            for field in ('latency_ms','cost'):
                value = p.get(field)
                if value is not None and (isinstance(value, bool) or not isinstance(value, (int,float)) or not math.isfinite(value) or value < 0):
                    raise ValueError('model_measurement_invalid')
        elif kind == 'delivery_completed':
            if not (p.get('receipt_file') and re.fullmatch('[0-9a-f]{64}',str(p.get('receipt_sha256',''))) and
                    re.fullmatch(r'R[1-9][0-9]*',str(p.get('report_revision','')))):
                raise ValueError('completion_event_invalid')
            latest={}
            for row in rows:
                if row['kind'].startswith('member_'):
                    latest[row['payload']['role']]=row['kind']
            if not latest or 'member_started' in latest.values():
                raise ValueError('completion_members_waiting')
            challenges={}
            for row in rows:
                if row['kind'].startswith('challenge_'):
                    challenges[(row['payload']['round_id'],row['payload']['role'])]=row['kind']
            if 'challenge_started' in challenges.values(): raise ValueError('completion_challenges_waiting')
        elif kind == 'intake_blocked':
            if rows or p.get('reason_code')!='no_supported_files' or p.get('report_generated') is not False or not (
                p.get('receipt_file') and re.fullmatch('[0-9a-f]{64}',str(p.get('receipt_sha256','')))):
                raise ValueError('intake_blocked_event_invalid')
        elif kind == 'quality_observation':
            if (type(p.get('has_conflict')) is not bool or type(p.get('conflict_count')) is not int or
                p['conflict_count']<0 or p['has_conflict']!=(p['conflict_count']>0) or
                not isinstance(p.get('inputs'),dict) or not p['inputs'] or not p.get('report_revision')):
                raise ValueError('quality_observation_invalid')
        elif kind == 'platform_read_observed':
            hashes=('request_sha256','descriptor_sha256','connector_response_sha256','data_sha256','connector_source_fingerprint')
            if (not all(isinstance(p.get(k),str) and p[k] for k in
                        ('read_id','request_id','client_scope','platform','account_id','store_id','resource','platform_id')) or
                not all(re.fullmatch('[0-9a-f]{64}',str(p.get(k,''))) for k in hashes) or
                type(p.get('simulated')) is not bool or type(p.get('platform_connection_verified')) is not bool or
                p.get('independently_authenticated') is not False or p.get('formal_acceptance_completed') is not False or
                p.get('evidence_kind') not in ('synthetic_mock_read','native_platform_api_observation') or
                p.get('status') not in ('synthetic_read_verified','native_api_observation_recorded')):
                raise ValueError('platform_read_observation_invalid')
            if p.get('data_sha256') != digest(p.get('data')):
                raise ValueError('platform_read_data_fingerprint_invalid')
            if ((p['simulated'] and (p['platform_connection_verified'] or
                 p['evidence_kind']!='synthetic_mock_read' or p['status']!='synthetic_read_verified')) or
                (not p['simulated'] and (not p['platform_connection_verified'] or
                 p['evidence_kind']!='native_platform_api_observation' or
                 p['status']!='native_api_observation_recorded'))):
                raise ValueError('platform_read_evidence_boundary_invalid')
        elif kind == 'action_policy_decision':
            if (p.get('decision') not in ('denied','requires_approval','assisted_plan_only','eligible_for_execution') or
                not p.get('action_id') or not re.fullmatch('[0-9a-f]{64}',str(p.get('request_sha256',''))) or
                not p.get('reason') or p.get('executed') is not False):
                raise ValueError('action_policy_decision_invalid')
        elif kind.startswith('action_call_'):
            if not all(isinstance(p.get(k),str) and p[k] for k in
                       ('call_key','connector_call_id','action_id','approval_id')):
                raise ValueError('action_call_identity_missing')
            matching=[r for r in rows if r['kind'].startswith('action_call_') and
                      r['payload'].get('call_key')==p['call_key']]
            if kind=='action_call_reserved':
                if (matching or not all(re.fullmatch('[0-9a-f]{64}',str(p.get(k,''))) for k in
                    ('call_key','request_sha256','policy_sha256','approval_sha256','descriptor_sha256',
                     'expected_sha256','before_sha256')) or type(p.get('simulated')) is not bool or
                    p.get('resubmission_allowed') is not False):
                    raise ValueError('action_call_reservation_invalid')
                decisions=[r['payload'] for r in rows if r['kind']=='action_policy_decision' and
                           r['payload'].get('action_id')==p['action_id']]
                if not decisions or decisions[-1]['decision']!='eligible_for_execution' or any(
                    decisions[-1].get(k)!=p.get(k) for k in ('approval_id','request_sha256','bindings')):
                    raise ValueError('action_call_policy_binding_missing')
            else:
                if not matching or matching[0]['kind']!='action_call_reserved' or any(
                    matching[0]['payload'].get(k)!=p[k] for k in ('connector_call_id','action_id','approval_id')):
                    raise ValueError('action_call_not_reserved')
                terminals=[r for r in matching if r['kind'] in
                           ('action_call_returned','action_call_uncertain','action_call_aborted')]
                if kind in ('action_call_returned','action_call_uncertain','action_call_aborted'):
                    if terminals:
                        raise ValueError('action_call_already_observed')
                    if kind=='action_call_returned' and not re.fullmatch('[0-9a-f]{64}',str(p.get('response_sha256',''))):
                        raise ValueError('action_call_response_missing')
                    if kind!='action_call_returned' and not p.get('reason'):
                        raise ValueError('action_call_reason_missing')
                elif kind=='action_call_readback':
                    if not p.get('readback_id') or type(p.get('matched')) is not bool or type(p.get('read_succeeded')) is not bool:
                        raise ValueError('action_readback_invalid')
                    if (p['matched'] and not p['read_succeeded']) or (p['read_succeeded'] and
                        not re.fullmatch('[0-9a-f]{64}',str(p.get('actual_sha256','')))):
                        raise ValueError('action_readback_evidence_missing')
                elif kind=='action_call_outcome':
                    reads=[r for r in matching if r['kind']=='action_call_readback' and
                           r['payload'].get('readback_id')==p.get('readback_id')]
                    if not reads or p.get('outcome') not in ('verified','blocked') or p.get('resubmission_allowed') is not False:
                        raise ValueError('action_outcome_readback_missing')
                    if p.get('simulated') is not matching[0]['payload']['simulated']:
                        raise ValueError('action_outcome_evidence_type_changed')
                    if p['outcome']=='verified' and (not terminals or terminals[0]['kind']!='action_call_returned' or
                                                    not reads[-1]['payload']['matched']):
                        raise ValueError('action_outcome_not_verified')
                else:
                    raise ValueError('action_call_kind_unknown')
        elif kind == 'monitor_policy':
            if not p.get('policy_id') or not p.get('revision') or not re.fullmatch('[0-9a-f]{64}',str(p.get('sha256',''))):
                raise ValueError('monitor_policy_invalid')
        elif kind == 'monitor_comparison':
            if not p.get('output') or not re.fullmatch('[0-9a-f]{64}',str(p.get('sha256',''))) or p.get('automatic_changes') is not False:
                raise ValueError('monitor_comparison_invalid')
        elif kind in ('gate_blocked', 'human_correction', 'connector_observation'):
            if not p.get('reason'):
                raise ValueError('observation_reason_missing')
        else:
            raise ValueError('event_kind_unknown')

    def status(self, run_id, client_scope):
        rows = self.events(run_id, client_scope)
        members = {}
        for r in rows:
            if r['kind'].startswith('member_'):
                p = r['payload']
                members[(p['role'],p['host'],p['agent_task_id'],p['attempt_id'])] = r
        challenges={}
        for r in rows:
            if r['kind'].startswith('challenge_'):
                p=r['payload']; challenges[(p['round_id'],p['role'])]=r
        calls={}
        for r in rows:
            if r['kind'].startswith('action_call_'):
                p=r['payload']
                call=calls.setdefault(p['call_key'],{})
                call.update({k:p[k] for k in ('action_id','approval_id','connector_call_id','readback_id',
                                              'outcome','reason','simulated') if k in p})
                call['state']=r['kind']
                call['resubmission_allowed']=False
        intake=next((r for r in rows if r['kind']=='intake_blocked'),None)
        platform_reads=[r['payload'] for r in rows if r['kind']=='platform_read_observed']
        return dict(run_id=run_id, client_scope=client_scope,
                    phase=next((r['payload']['phase'] for r in reversed(rows) if r['kind']=='phase'), 'intake'),
                    waiting=[r['payload'] for r in members.values() if r['kind']=='member_started'],
                    challenges_waiting=[r['payload'] for r in challenges.values() if r['kind']=='challenge_started'],
                    members=[dict(state=r['kind'], **r['payload']) for r in members.values()],
                    action_calls=list(calls.values()),
                    platform_reads=platform_reads,
                    terminal_outcome='intake_blocked_no_report' if intake else None,
                    events=len(rows), last_event_hash=rows[-1]['event_hash'] if rows else '',
                    runtime_proof='recorded_host_observations_not_independent_verification')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db', required=True)
    ap.add_argument('--run-id', required=True)
    ap.add_argument('--client-scope', required=True)
    sub = ap.add_subparsers(dest='command', required=True)
    create = sub.add_parser('create')
    create.add_argument('--team-version', required=True)
    create.add_argument('--task-type', required=True)
    record = sub.add_parser('record')
    record.add_argument('--event-key', required=True)
    record.add_argument('--kind', required=True)
    record.add_argument('--payload', required=True, help='JSON file; never include credentials')
    sub.add_parser('status')
    sub.add_parser('replay')
    args = ap.parse_args()
    journal = Journal(args.db)
    try:
        if args.command == 'create':
            journal.create(args.run_id, args.client_scope, args.team_version, args.task_type)
        elif args.command == 'record':
            if args.kind in ('delivery_completed','intake_blocked'):
                raise ValueError('terminal_outcome_owned_by_gate')
            if args.kind.startswith('challenge_'):
                raise ValueError('challenge_owned_by_runtime')
            if args.kind.startswith('action_call_'):
                raise ValueError('action_call_owned_by_gateway')
            journal.append(args.run_id, args.client_scope, args.event_key, args.kind,
                           json.loads(Path(args.payload).read_text(encoding='utf-8-sig')))
        if args.command == 'replay':
            for row in journal.events(args.run_id, args.client_scope):
                print(encoded(row))
        else:
            print(encoded(journal.status(args.run_id, args.client_scope)))
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(encoded(dict(status='journal_blocked', reason=str(exc))))
        return 2
    finally:
        journal.close()


if __name__ == '__main__':
    raise SystemExit(main())
