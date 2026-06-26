#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from auth_file_lib import get_openai_default_profile, load_auth_profiles_file, restore_auth_profiles_file
from lock_lib import LockError, acquire_lock, release_lock
from probe_lib import probe_gateway_status, probe_openclaw_status, run_command
from state_lib import append_experiment_history, load_last_known_good

JsonDict = Dict[str, Any]


def restart_gateway() -> JsonDict:
    return run_command(['openclaw', 'gateway', 'restart'])


def probe_restored_state() -> JsonDict:
    gateway = probe_gateway_status()
    status = probe_openclaw_status()
    current = get_openai_default_profile(load_auth_profiles_file())
    return {
        'success': gateway['ok'] and status['ok'],
        'gateway': gateway,
        'status': status,
        'account_id': current.get('accountId'),
    }


def resolve_backup_source(args: argparse.Namespace) -> Path:
    if bool(args.backup_file) == bool(args.last_known_good):
        raise ValueError('must specify exactly one of --backup-file / --last-known-good')
    if args.backup_file:
        return Path(args.backup_file)
    data = load_last_known_good()
    backup_file = data.get('backup_file')
    if not backup_file:
        raise ValueError('last-known-good missing backup_file')
    return Path(backup_file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--backup-file')
    parser.add_argument('--last-known-good', action='store_true')
    parser.add_argument('--json', action='store_true', dest='json_output')
    parser.add_argument('--restart-gateway', dest='restart_gateway', action='store_true', default=True)
    parser.add_argument('--no-restart-gateway', dest='restart_gateway', action='store_false')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        acquire_lock('rollback_experiment')
    except LockError as e:
        print(json.dumps({'ok': False, 'stage': 'acquire_lock', 'error': str(e)}, ensure_ascii=False, indent=2))
        return 1

    try:
        try:
            backup = resolve_backup_source(args)
        except Exception as e:
            result = {'ok': False, 'stage': 'resolve_backup_source', 'error': str(e)}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1

        try:
            restore_auth_profiles_file(backup)
        except Exception as e:
            result = {'ok': False, 'stage': 'restore_auth_file', 'error': str(e), 'backup_file': str(backup)}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1

        restart_result = restart_gateway() if args.restart_gateway else {'ok': False}
        probe = probe_restored_state()
        result = {
            'ok': probe['success'],
            'restored_from': str(backup),
            'restored_account_id': probe['account_id'],
            'gateway_restarted': restart_result.get('ok', False),
            'validated': probe['success'],
        }
        append_experiment_history({'action': 'rollback', **result})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if probe['success'] else 1
    finally:
        release_lock()


if __name__ == '__main__':
    sys.exit(main())
