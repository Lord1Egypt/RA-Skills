#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from auth_file_lib import (
    OPENAI_PROFILE_KEY,
    backup_auth_profiles_file,
    get_openai_default_profile,
    load_auth_profiles_file,
    replace_openai_default_profile,
    save_auth_profiles_file,
    restore_auth_profiles_file,
)
from lock_lib import LockError, acquire_lock, release_lock
from paths import get_profiles_dir
from probe_lib import probe_auth_structure, probe_gateway_status, probe_openclaw_status, run_command
from state_lib import append_experiment_history, write_last_experiment, write_last_known_good_from_success

JsonDict = Dict[str, Any]


def normalize_target_profile(raw: JsonDict) -> JsonDict:
    if 'profiles' in raw:
        profiles = raw.get('profiles') or {}
        profile = profiles.get(OPENAI_PROFILE_KEY)
        if not isinstance(profile, dict):
            raise ValueError(f'missing {OPENAI_PROFILE_KEY} in target file')
        return profile
    return raw


def resolve_target_profile(args: argparse.Namespace) -> JsonDict:
    if bool(args.target_file) == bool(args.target_slot):
        raise ValueError('must specify exactly one of --target-file / --target-slot')
    if args.target_file:
        raw = json.loads(Path(args.target_file).read_text(encoding='utf-8'))
        return normalize_target_profile(raw)
    slot_path = get_profiles_dir() / args.target_slot / 'auth-profile.json'
    raw = json.loads(slot_path.read_text(encoding='utf-8'))
    return normalize_target_profile(raw)


def restart_gateway_if_needed() -> JsonDict:
    return run_command(['openclaw', 'gateway', 'restart'], timeout=120)


def probe_runtime_state() -> JsonDict:
    gateway = probe_gateway_status()
    status = probe_openclaw_status()
    current = get_openai_default_profile(load_auth_profiles_file())
    return {
        'success': gateway['ok'] and status['ok'],
        'gateway': gateway,
        'status': status,
        'account_id': current.get('accountId'),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Public-track controlled OpenAI auth switch experiment')
    parser.add_argument('--target-file')
    parser.add_argument('--target-slot')
    parser.add_argument('--json', action='store_true', dest='json_output')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--restart-on-fail', dest='restart_on_fail', action='store_true', default=True)
    parser.add_argument('--no-restart-on-fail', dest='restart_on_fail', action='store_false')
    parser.add_argument('--restart-after-write', dest='restart_after_write', action='store_true', default=True)
    parser.add_argument('--no-restart-after-write', dest='restart_after_write', action='store_false')
    return parser.parse_args()


def emit(result: JsonDict) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> int:
    args = parse_args()
    backup_file = None
    try:
        acquire_lock('switch_experiment')
    except LockError as e:
        emit({'ok': False, 'stage': 'acquire_lock', 'error': str(e)})
        return 1

    try:
        current_data = load_auth_profiles_file()
        current_profile = get_openai_default_profile(current_data)
        target_profile = resolve_target_profile(args)
        shape = probe_auth_structure(target_profile)
        if not shape['ok']:
            result = {'ok': False, 'stage': 'validate_target_profile_shape', 'missing': shape['missing']}
            emit(result)
            return 1

        if args.dry_run:
            result = {
                'ok': True,
                'dry_run': True,
                'from_account_id': current_profile.get('accountId'),
                'to_account_id': target_profile.get('accountId'),
                'target_provider': target_profile.get('provider'),
            }
            emit(result)
            return 0

        backup_file = backup_auth_profiles_file()
        updated = replace_openai_default_profile(current_data, target_profile)
        save_auth_profiles_file(updated)

        pre_restart_probe = probe_runtime_state()

        restart_result = {'ok': False, 'stdout': '', 'stderr': ''}
        restart_probe = {'success': False, 'account_id': None}
        if args.restart_after_write:
            restart_result = restart_gateway_if_needed()
            if restart_result.get('ok'):
                restart_probe = probe_runtime_state()

        activated = restart_probe.get('success') and restart_probe.get('account_id') == target_profile.get('accountId')
        if activated:
            result = {
                'ok': True,
                'from_account_id': current_profile.get('accountId'),
                'to_account_id': target_profile.get('accountId'),
                'activation': 'restart-required',
                'backup_file': str(backup_file),
                'validated': True,
                'rolled_back': False,
                'pre_restart_account_id': pre_restart_probe.get('account_id'),
                'post_restart_account_id': restart_probe.get('account_id'),
            }
            append_experiment_history(result)
            write_last_experiment(result)
            write_last_known_good_from_success(backup_file=str(backup_file), account_id=target_profile.get('accountId'))
            emit(result)
            return 0

        restore_auth_profiles_file(backup_file)
        rollback_restart = restart_gateway_if_needed() if args.restart_on_fail else {'ok': False}
        result = {
            'ok': False,
            'stage': 'runtime_probe',
            'error': 'restart probe failed or account_id mismatch',
            'backup_file': str(backup_file),
            'rolled_back': True,
            'restored_account_id': current_profile.get('accountId'),
            'rollback_restart_ok': rollback_restart.get('ok'),
            'pre_restart_account_id': pre_restart_probe.get('account_id'),
            'post_restart_account_id': restart_probe.get('account_id'),
        }
        append_experiment_history(result)
        write_last_experiment(result)
        emit(result)
        return 1
    except Exception as e:
        if backup_file is not None:
            try:
                restore_auth_profiles_file(backup_file)
            except Exception:
                pass
        result = {
            'ok': False,
            'stage': 'exception',
            'error': str(e),
            'backup_file': str(backup_file) if backup_file else None,
            'rolled_back': backup_file is not None,
        }
        append_experiment_history(result)
        write_last_experiment(result)
        emit(result)
        return 1
    finally:
        release_lock()


if __name__ == '__main__':
    sys.exit(main())
