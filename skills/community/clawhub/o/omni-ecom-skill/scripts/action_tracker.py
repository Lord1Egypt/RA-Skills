#!/usr/bin/env python3
"""Read legacy 1.x action history without granting current write authority."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from artifact_contract import native_action_history_identity,validate_action_history_identity

MUTATING={'create','approve','transition','outcome'}
WARNINGS=['legacy_history_only','cannot_approve_or_execute_current_actions']


def emit(value,stream=sys.stdout):
    print(json.dumps(value,ensure_ascii=False,indent=2),file=stream)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_legacy(path,client_scope):
    if not path.is_file(): raise ValueError('legacy_action_missing')
    value=json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value,dict) or value.get('schema_version')!='1.0':
        raise ValueError('legacy_action_schema_invalid')
    if value.get('client_scope')!=client_scope:
        raise ValueError('legacy_action_client_scope_mismatch')
    if not value.get('action_id') or not value.get('run_id'):
        raise ValueError('legacy_action_identity_missing')
    return value


def read_events(path):
    event_path=path.with_suffix('.events.jsonl')
    if not event_path.is_file(): return []
    rows=[]
    for line in event_path.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip(): continue
        value=json.loads(line)
        if not isinstance(value,dict): raise ValueError('legacy_action_event_invalid')
        rows.append(value)
    return rows


def record(path,client_scope):
    return {'source_file':path.name,'source_sha256':sha(path),
            'action':load_legacy(path,client_scope),'events':read_events(path)}


def view(mode,client_scope,records):
    value=dict(**native_action_history_identity(),client_scope=client_scope,mode=mode,
               count=len(records),records=records,warnings=WARNINGS)
    validate_action_history_identity(value)
    return value


def main():
    parser=argparse.ArgumentParser(description='查看 1.x 行动历史；2.0 当前写入已停用')
    parser.add_argument('command',choices=sorted(MUTATING|{'show','list'}))
    parser.add_argument('--action-file')
    parser.add_argument('--root')
    parser.add_argument('--client-scope')
    parser.add_argument('--status')
    args,_=parser.parse_known_args()
    try:
        if args.command in MUTATING:
            raise ValueError('legacy_action_tracker_write_disabled_use_v2_action_policy_and_gateway')
        if not args.client_scope: raise ValueError('legacy_action_client_scope_required')
        if args.command=='show':
            if not args.action_file: raise ValueError('legacy_action_file_required')
            path=Path(args.action_file).resolve()
            result=view('show',args.client_scope,[record(path,args.client_scope)])
        else:
            if not args.root: raise ValueError('legacy_action_root_required')
            directory=Path(args.root).resolve()/'approvals'; records=[]
            if directory.is_dir():
                for path in sorted(directory.glob('A*.json')):
                    if path.name.endswith('.approval.json'): continue
                    try: item=record(path,args.client_scope)
                    except (OSError,ValueError,json.JSONDecodeError): continue
                    if args.status and item['action'].get('status')!=args.status: continue
                    records.append(item)
            result=view('list',args.client_scope,records)
        emit(result); return 0
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        emit({'status':'FAIL','error':str(exc)},sys.stderr); return 1


if __name__=='__main__': raise SystemExit(main())
