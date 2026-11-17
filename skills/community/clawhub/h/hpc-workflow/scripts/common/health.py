#!/usr/bin/env python3
"""Observe compute-local backup health without sending signals or changing data."""
import argparse
import datetime
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

SITE = '@SITE@'
PREFIX = '@PREFIX@'
ADAPTER = '@ADAPTER@'


def read_record(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None


def observe(archive, job, interval=300):
    archive = Path(archive)
    archive_name = str(archive)
    pid_path = Path((archive_name[:-8] if archive_name.endswith('.tar.zst') else archive_name) + '.autosave.pid')
    record = read_record(Path(str(archive) + '.health.json'))
    result = dict(archive=str(archive), backup_state='missing' if not archive.exists() else 'present',
                  autosave_state='stopped', last_success_at=None, last_failure=None,
                  consecutive_failures=0, integrity='not_checked', freshness='unknown')
    live_identity = None
    if pid_path.exists():
        fields = pid_path.read_text().strip().split('\t')
        result['autosave_state'] = 'unknown'
        if len(fields) == 3 and fields[0].isdigit() and fields[1] == socket.gethostname():
            process = Path('/proc') / fields[0] / 'stat'
            try:
                # Process names can contain spaces: parse after the final ')'.
                stat = process.read_text().rsplit(')', 1)[1].split()
                if stat[19] == fields[2] and stat[0] != 'Z':
                    live_identity = ':'.join((fields[1], fields[0], fields[2]))
                    result['autosave_state'] = 'alive'
                else:
                    result['autosave_state'] = 'stale'
            except FileNotFoundError:
                result['autosave_state'] = 'stale'
    if record:
        for key in ('last_success_at', 'last_failure', 'consecutive_failures', 'last_verified_at'):
            result[key] = record.get(key, result.get(key))
        result['last_operation'] = record.get('operation')
        result['last_operation_exit_code'] = record.get('exit_code')
        same_writer = record.get('last_success_job') == job and record.get('last_success_autosave_id') == live_identity
        result['current_writer_has_saved'] = bool(live_identity and same_writer)
        if record.get('last_success_at'):
            stamp = datetime.datetime.strptime(record['last_success_at'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc)
            age = (datetime.datetime.now(datetime.timezone.utc) - stamp).total_seconds()
            result.update(last_success_age_seconds=max(0, int(age)),
                          freshness='fresh' if age <= max(120, interval * 2) and age >= -60 else 'stale')
    result['healthy'] = bool(result['backup_state'] == 'present' and result['autosave_state'] == 'alive'
                             and result.get('current_writer_has_saved') and result['freshness'] == 'fresh'
                             and result['consecutive_failures'] == 0)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--job', required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    try:
        if args.job != os.environ.get('SLURM_JOB_ID'):
            raise ValueError('Health probe is outside the requested allocation')
        default = Path.home() / '.local/share' / (SITE + '-local-snapshot') / 'workspace.tar.zst'
        if ADAPTER == 'psc':
            default = Path.home() / 'project/local-workspaces' / ('local-' + os.environ['USER'] + '.tar.zst')
        archive = os.environ.get(PREFIX + '_LOCAL_SNAPSHOT_ARCHIVE', str(default))
        result = observe(archive, args.job, int(os.environ.get(PREFIX + '_GPU_AUTOSAVE_INTERVAL', '300')))
        base = os.environ.get(PREFIX + '_LOCAL_BASE') if ADAPTER == 'msi' else os.environ.get('LOCAL')
        result.update(cluster=SITE, job_id=args.job, host=socket.gethostname(), observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      compute_storage=dict(path=base, writable=bool(base and os.path.isdir(base) and os.access(base, os.W_OK))))
        result['healthy'] = result['healthy'] and result['compute_storage']['writable']
        if args.verify:
            helper = str(Path(os.environ.get('HPC_CORE_BIN', str(Path.home() / '.local/bin'))) / (SITE + '-local-snapshot'))
            process = subprocess.Popen([helper, 'verify', archive], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, start_new_session=True)
            try:
                output, _ = process.communicate(timeout=int(os.environ.get('HPC_HEALTH_VERIFY_SECONDS', '300')))
                result['integrity'] = 'verified' if process.returncode == 0 and 'SNAPSHOT_VERIFIED' in output else 'failed'
                result['integrity_output'] = output[-2000:]
            except subprocess.TimeoutExpired:
                import signal
                os.killpg(process.pid, signal.SIGKILL); process.communicate()
                result['integrity'] = 'unknown'
                result['integrity_output'] = 'Verification timeout'
            result['healthy'] = result['healthy'] and result['integrity'] == 'verified'
        print('HPC_HEALTH_JSON=' + json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print('HPC_HEALTH_JSON=' + json.dumps(dict(cluster=SITE, job_id=args.job, healthy=False, error=str(error))))
        return 1


if __name__ == '__main__':
    sys.exit(main())
