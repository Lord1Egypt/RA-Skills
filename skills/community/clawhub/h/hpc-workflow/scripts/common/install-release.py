#!/usr/bin/env python3
"""Python 3.6 remote installer; PAYLOAD is supplied by the authenticated caller."""
import ast
import base64
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile


def atomic(path, data, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(prefix='.hpc-install-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        os.chmod(temporary, mode); os.replace(temporary, str(path))
        directory = os.open(str(path.parent), os.O_RDONLY)
        try: os.fsync(directory)
        finally: os.close(directory)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)


def write_json(path, data):
    atomic(path, (json.dumps(data, sort_keys=True) + '\n').encode())


def target_for(home, site, name):
    if name.startswith('bin/') and re.fullmatch(r'[A-Za-z0-9._-]+', name[4:]):
        return home / '.local/bin' / name[4:]
    if name.startswith('config/') and re.fullmatch(r'[A-Za-z0-9._-]+', name[7:]):
        return home / ('.config/' + site + '-gpu') / name[7:]
    if name == 'profile.json':
        return home / ('.config/' + site + '-gpu/profile.json')
    raise ValueError('Unsupported release member: ' + name)


def quiescent(home, site):
    queue = subprocess.check_output(['squeue', '-h', '-u', os.environ['USER'], '-o', '%i|%T'],
                                    universal_newlines=True, timeout=30).strip()
    if queue: raise RuntimeError('Live jobs exist; deployment refused: ' + queue)
    for path in (home / ('.local/state/' + site + '-gpu/allocations')).glob('*.json'):
        record = json.loads(path.read_text())
        if path.name == 'hpc-deployment-guard.json' and record.get('deployment_guard') and record.get('cluster') == site:
            journal = home / ('.local/state/' + site + '-gpu/deployment.json')
            if journal.exists() and record.get('backup') == json.loads(journal.read_text()).get('backup'):
                continue
        if record.get('phase') == 'terminal': continue
        if not record.get('job_id'): raise RuntimeError('Unresolved allocation request: ' + str(path))
        rows = subprocess.check_output(['sacct', '-nXP', '-j', record['job_id'], '-o', 'JobID,State'],
                                       universal_newlines=True, timeout=30)
        terminal = next((r.split('|')[1].split()[0] for r in rows.splitlines()
                         if r.split('|')[0] == record['job_id']), 'UNKNOWN')
        if terminal not in ('COMPLETED', 'CANCELLED', 'FAILED', 'TIMEOUT', 'NODE_FAIL',
                            'OUT_OF_MEMORY', 'PREEMPTED', 'BOOT_FAIL', 'DEADLINE', 'REVOKED'):
            raise RuntimeError('Allocation termination is unconfirmed: ' + str(path))


def restore(home, site, backup, journal):
    index = json.loads((backup / 'index.json').read_text())
    if index['site'] != site: raise ValueError('Backup site mismatch')
    # Verify every prior byte before changing any target.
    for name, entry in index['files'].items():
        target_for(home, site, name)
        if entry['exists'] and hashlib.sha256((backup / name).read_bytes()).hexdigest() != entry['sha256']:
            raise RuntimeError('Backup hash mismatch: ' + name)
    write_json(journal, dict(phase='rolling_back', backup=str(backup)))
    for name, entry in index['files'].items():
        target = target_for(home, site, name)
        if entry['exists']: atomic(target, (backup / name).read_bytes(), entry['mode'])
        elif target.exists() or target.is_symlink(): target.unlink()
    write_json(journal, dict(phase='rolled_back', backup=str(backup)))
    remove_guard(home, site)


def remove_guard(home, site):
    guard = home / ('.local/state/' + site + '-gpu/allocations/hpc-deployment-guard.json')
    if guard.exists():
        record = json.loads(guard.read_text())
        if not record.get('deployment_guard') or record.get('cluster') != site:
            raise RuntimeError('Deployment guard identity mismatch')
        guard.unlink()


def install(payload):
    home = Path.home(); site = payload['site']
    if not re.fullmatch(r'[a-z][a-z0-9-]{0,30}', site): raise ValueError('Invalid site')
    state = home / ('.local/state/' + site + '-gpu')
    allocations = state / 'allocations'; allocations.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = (allocations / 'submit.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    quiescent(home, site)
    journal = state / 'deployment.json'
    archive = os.path.expandvars(payload.get('archive', ''))
    if not archive:
        config = home / ('.config/' + site + '-gpu/gpu.env')
        variable = site.upper().replace('-', '_') + '_LOCAL_SNAPSHOT_ARCHIVE'
        command = 'set -e; [[ ! -f "$1" ]] || source "$1"; printf "%s" "${' + variable + ':-${HPC_ARCHIVE:-}}"'
        archive = subprocess.check_output(['bash', '-c', command, 'probe', str(config)],
                                         universal_newlines=True, timeout=30).strip()
    if not archive:
        archive = str(home / (('project/local-workspaces/local-' + os.environ['USER'] + '.tar.zst')
                             if site == 'psc' else '.local/share/' + site + '-local-snapshot/workspace.tar.zst'))
    if Path(archive + '.lock').is_dir(): raise RuntimeError('Legacy snapshot lock exists; inspect before deployment')
    # Create the lock even on an empty archive, so a concurrent writer uses the same inode.
    Path(archive).parent.mkdir(parents=True, exist_ok=True)
    lease = open(archive + '.autosave.core.lock', 'a')
    fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
    prior = json.loads(journal.read_text()) if journal.exists() else {}
    if prior.get('phase') in ('installing', 'rolling_back', 'rollback_failed'):
        restore(home, site, Path(prior['backup']), journal)
    if payload.get('rollback'):
        backup = Path(payload['rollback']).expanduser().resolve()
        allowed = (home / '.local/state/hpc-core-backups').resolve()
        if allowed not in backup.parents: raise ValueError('Rollback target must be a saved release backup')
        restore(home, site, backup, journal)
        print(json.dumps(dict(site=site, action='rolled_back', backup=str(backup))))
        return
    files = {name: base64.b64decode(data) for name, data in payload['files'].items()}
    manifest_name = 'config/core-manifest.json'
    manifest_bytes = (json.dumps(payload['manifest'], sort_keys=True) + '\n').encode()
    if manifest_name in files: raise ValueError('Manifest is managed by the installer')
    stage = Path(tempfile.mkdtemp(prefix='hpc-stage-', dir=str(home)))
    for name, data in files.items():
        target_for(home, site, name)
        if hashlib.sha256(data).hexdigest() != payload['hashes'][name]: raise RuntimeError('Hash mismatch: ' + name)
        temporary = stage / name; temporary.parent.mkdir(parents=True, exist_ok=True); temporary.write_bytes(data)
        if data.startswith(b'#!/usr/bin/env bash') or name.endswith(('.env', '.sh')):
            subprocess.check_call(['bash', '-n', str(temporary)])
        elif data.startswith(b'#!/usr/bin/env python3'): ast.parse(data.decode())
    files[manifest_name] = manifest_bytes
    backup = home / ('.local/state/hpc-core-backups/' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + site)
    backup.mkdir(parents=True, mode=0o700)
    index = dict(site=site, files={})
    for name in files:
        target = target_for(home, site, name)
        if target.is_symlink(): raise RuntimeError('Symlink install target needs explicit inspection: ' + str(target))
        entry = dict(exists=target.exists())
        if entry['exists']:
            data = target.read_bytes(); entry.update(mode=target.stat().st_mode & 0o777, sha256=hashlib.sha256(data).hexdigest())
            atomic(backup / name, data)
        index['files'][name] = entry
    write_json(backup / 'index.json', index)
    write_json(journal, dict(phase='installing', backup=str(backup), core_version=payload['manifest']['core_version']))
    # Older allocation helpers already reject another unresolved reservation.
    # This barrier protects upgrades even before the new journal-aware helper lands.
    guard = allocations / 'hpc-deployment-guard.json'
    if guard.exists() and not json.loads(guard.read_text()).get('deployment_guard'):
        raise RuntimeError('Deployment guard request ID is already in use')
    write_json(guard, dict(schema_version=1, cluster=site, request_id='hpc-deployment-guard',
                          deployment_guard=True, backup=str(backup), phase='reserved', job_id=None,
                          identity={}, job_name='hpc-deployment-guard', comment='hpc-deployment-guard',
                          created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    def interrupted(signum, frame): raise RuntimeError('Deployment interrupted by signal ' + str(signum))
    signal.signal(signal.SIGTERM, interrupted); signal.signal(signal.SIGHUP, interrupted)
    try:
        for name, data in files.items():
            atomic(target_for(home, site, name), data, 0o700 if name.startswith('bin/') else 0o600)
            if hashlib.sha256(target_for(home, site, name).read_bytes()).hexdigest() != hashlib.sha256(data).hexdigest():
                raise RuntimeError('Installed hash mismatch: ' + name)
        write_json(journal, dict(phase='committed', backup=str(backup), core_version=payload['manifest']['core_version']))
        remove_guard(home, site)
    except BaseException:
        try: restore(home, site, backup, journal)
        except BaseException:
            write_json(journal, dict(phase='rollback_failed', backup=str(backup)))
            raise
        raise
    print(json.dumps(dict(site=site, core_version=payload['manifest']['core_version'], verified_files=len(files)-1,
                         backup=str(backup), stage=str(stage), action='committed')))


if __name__ == '__main__':
    install(json.loads(base64.b64decode(PAYLOAD)))
