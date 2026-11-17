#!/usr/bin/env python3
"""Durable Slurm request identities; compatible with Python 3.6."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
import pty
from pathlib import Path
import re
import shlex
import socket
import subprocess
import sys

SITE = '@SITE@'
PREFIX = '@PREFIX@'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def atomic(path, data):
    temporary = path.with_name(path.name + '.tmp.' + str(os.getpid()))
    with temporary.open('w') as stream:
        json.dump(data, stream, sort_keys=True)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    temporary.replace(path)
    fd = os.open(str(path.parent), os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def command(argv):
    return subprocess.check_output(argv, stderr=subprocess.STDOUT,
                                   universal_newlines=True, timeout=30).strip()


def queue():
    rows = command(['squeue', '-h', '-u', os.environ['USER'], '-o', '%i|%T|%j|%N'])
    jobs = []
    for row in rows.splitlines():
        job, phase, name, node = row.split('|', 3)
        if not re.match(r'^[0-9]+$', job):
            raise RuntimeError('Unsupported scheduler job identity: ' + job)
        jobs.append(dict(job_id=job, slurm_state=phase, name=name, node=node))
    return jobs


def reconcile(record, jobs):
    candidates = [job for job in jobs if job['job_id'] == record['job_id']] if record.get('job_id') else [job for job in jobs if job['name'] == record['job_name']]
    if len(candidates) > 1:
        raise RuntimeError('Multiple jobs match request; inspect before continuing')
    if candidates:
        job = candidates[0]
        detail = command(['scontrol', 'show', 'job', job['job_id'], '-o'])
        if ('Comment=' + record['comment']) not in detail.split():
            raise RuntimeError('Slurm request comment mismatch; refusing to adopt job')
        if not re.search(r'\bUserId=' + re.escape(os.environ['USER']) + r'\(', detail):
            raise RuntimeError('Slurm job owner mismatch')
        if record.get('job_id') and record['job_id'] != job['job_id']:
            raise RuntimeError('Request job identity changed')
        record.update(job_id=job['job_id'], slurm_state=job['slurm_state'], node=job['node'],
                      phase='ready' if record.get('ready') else 'allocated' if job['slurm_state'] == 'RUNNING' else 'pending')
    elif record.get('job_id'):
        rows = command(['sacct', '-nXP', '-j', record['job_id'], '-o', 'JobID,State,ExitCode'])
        match = next((r.split('|') for r in rows.splitlines()
                      if r.split('|')[0] == record['job_id']), None)
        if match and match[1].split()[0] in ('COMPLETED', 'CANCELLED', 'FAILED', 'TIMEOUT', 'NODE_FAIL', 'OUT_OF_MEMORY', 'PREEMPTED', 'BOOT_FAIL', 'DEADLINE', 'REVOKED'):
            record.update(phase='terminal', slurm_state=match[1], exit_code=match[2])
        else:
            record.update(phase='unknown', slurm_state=match[1] if match else 'UNKNOWN')
    else:
        record['phase'] = 'submission_unknown'
    record['observed_at'] = now()
    return record


def directory():
    return Path(os.environ.get(PREFIX + '_GPU_STATE_DIR', str(Path.home() / '.local/state' / (SITE + '-gpu')))) / 'allocations'


def request_path(root, request):
    if not re.match(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$', request):
        raise ValueError('Invalid allocation request ID')
    return root / (request + '.json')


def submit(root, args):
    journal = root.parent / 'deployment.json'
    if journal.exists() and json.loads(journal.read_text()).get('phase') in ('installing', 'rolling_back', 'rollback_failed'):
        raise RuntimeError('Incomplete deployment; recover the saved release before requesting a GPU')
    path = request_path(root, args.request)
    spec = dict(field.split('=', 1) for field in args.field)
    identity = dict(spec=spec, argv=args.command, socket=args.socket, target=args.target)
    jobs = queue()  # Failure is unknown, never an empty queue.
    if path.exists():
        record = json.loads(path.read_text())
        if record['identity'] != identity:
            raise RuntimeError('Allocation request ID reused with changed configuration')
        record = reconcile(record, jobs)
        atomic(path, record)
        return record
    for previous in root.glob('*.json'):
        record = reconcile(json.loads(previous.read_text()), jobs)
        atomic(previous, record)
        if record['phase'] != 'terminal':
            raise RuntimeError('Existing allocation request ' + record['request_id'] + ' requires recovery; no submission')
    if jobs:
        raise RuntimeError('Existing jobs found; inspect and reuse with --job; no submission')
    name = spec.get('job_name') or 'hpc-' + SITE + '-' + hashlib.sha256(args.request.encode()).hexdigest()[:20]
    if not re.match(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,100}$', name):
        raise ValueError('Invalid allocation job name')
    comment = 'hpc-core:' + SITE + ':' + hashlib.sha256(args.request.encode()).hexdigest()
    # Check the pane before reserving, so an ordinary busy-pane refusal is safe.
    pane = command(['tmux', '-L', args.socket, 'display-message', '-p', '-t', args.target,
                    '#{pane_current_command}|#{pane_pid}']).split('|')
    if pane[0] != 'bash':
        raise RuntimeError('Allocation pane is busy: ' + pane[0])
    children = subprocess.run(['pgrep', '-P', pane[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if children.returncode == 0:
        raise RuntimeError('Allocation pane has running children')
    if children.returncode != 1:
        raise RuntimeError('Cannot inspect allocation pane children')
    record = dict(schema_version=1, cluster=SITE, request_id=args.request, identity=identity,
                  job_name=name, comment=comment, phase='reserved', created_at=now(), job_id=None,
                  log_path=str(root / (args.request + '.log')))
    atomic(path, record)  # After this point, uncertainty never causes resubmission.
    env = ['/usr/bin/env', 'HPC_ALLOCATION_REQUEST_ID=' + args.request,
           PREFIX + '_GPU_STATE_DIR=' + str(root.parent),
           'HPC_CORE_JOB_NAME=' + name, 'HPC_ALLOCATION_COMMENT=' + comment]
    holder = str(Path(__file__).resolve())
    shell = 'exec ' + ' '.join(shlex.quote(x) for x in env + [holder, 'hold', args.request, '--'] + args.command)
    subprocess.check_call(['tmux', '-L', args.socket, 'send-keys', '-t', args.target, '-l', '--', shell])
    subprocess.check_call(['tmux', '-L', args.socket, 'send-keys', '-t', args.target, 'Enter'])
    record.update(phase='dispatched', observed_at=now())
    atomic(path, record)
    return record


def hold(root, args):
    path = request_path(root, args.request)
    with (root / 'submit.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        record = json.loads(path.read_text())
        if record.get('holder_started_at'):
            raise RuntimeError('Allocation holder already started; refusing another submit')
        record.update(phase='holding', holder_host=socket.gethostname(), holder_pid=os.getpid(), holder_started_at=now())
        atomic(path, record)
    with open(record['log_path'], 'ab', buffering=0) as log:
        # Preserve a controlling terminal for srun --pty and the PSC bridge.
        # Redirecting the delegated process to a log silently disables --pty.
        def read_master(fd):
            data = os.read(fd, 65536)
            log.write(data)
            return data
        status = pty.spawn(args.command, master_read=read_master)
        rc = os.WEXITSTATUS(status) if os.WIFEXITED(status) else 128 + os.WTERMSIG(status)
    with (root / 'submit.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        record = json.loads(path.read_text())
        record.update(holder_exit_code=rc, holder_ended_at=now())
        try:
            record = reconcile(record, queue())
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            record.update(phase='unknown', observation_error=str(error))
        atomic(path, record)
    if os.environ.get('TMUX_PANE') and os.environ.get('HPC_ALLOCATION_KEEP_PANE', '1') == '1':
        # Keep the sole allocation window reusable after Slurm releases it.
        for key in ('HPC_ALLOCATION_REQUEST_ID', 'HPC_ALLOCATION_COMMENT', 'HPC_CORE_JOB_NAME'):
            os.environ.pop(key, None)
        os.execv('/bin/bash', ['/bin/bash', '--noprofile', '--norc'])
    return rc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['submit', 'hold', 'get', 'bind'])
    parser.add_argument('request')
    parser.add_argument('--socket'); parser.add_argument('--target')
    parser.add_argument('--field', action='append', default=[])
    parser.add_argument('--job'); parser.add_argument('--ready', action='store_true')
    args, command_args = parser.parse_known_args()
    args.command = command_args[1:] if command_args[:1] == ['--'] else command_args
    root = directory(); root.mkdir(parents=True, exist_ok=True); os.chmod(str(root), 0o700)
    try:
        if args.mode == 'hold':
            return hold(root, args)
        with (root / 'submit.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if args.mode == 'submit':
                if not args.socket or not args.target or not args.command:
                    raise ValueError('submit requires socket, target and command')
                record = submit(root, args)
            else:
                path = request_path(root, args.request)
                record = json.loads(path.read_text())
                if args.mode == 'bind':
                    if not args.job or args.job != os.environ.get('SLURM_JOB_ID'):
                        raise RuntimeError('bind must run inside the matching allocation')
                    if os.environ.get('HPC_ALLOCATION_COMMENT') != record['comment']:
                        raise RuntimeError('Allocation comment identity mismatch')
                    if record.get('job_id') and record['job_id'] != args.job:
                        raise RuntimeError('Allocation already bound to another job')
                    record.update(job_id=args.job, phase='ready' if args.ready else 'allocated', ready=args.ready)
                else:
                    record = reconcile(record, queue())
                atomic(path, record)
        print(json.dumps(record, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(json.dumps(dict(cluster=SITE, request_id=args.request, phase='unknown', error=str(error))), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
