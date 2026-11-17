"""Explicit, one-shot paper observation epochs. No exchange receipts or fills.

Closing an epoch with unknown intentions does not settle it or release its
historical reserves. A new epoch is an independent experiment with the same
frozen capital/risk rules, never a continuation of an equity curve.
"""
import hashlib
import json
import os
from pathlib import Path
import time
import uuid


def _exclusive_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2).encode('utf8'))
        f.flush()
        os.fsync(f.fileno())


def prepare_session(root, authorization):
    """Called manually, only after a clean collector stop and human authorization."""
    if authorization != '恢复模拟挂单':
        raise ValueError('Explicit paper-session authorization required')
    root = Path(root)
    raw = (root/'data/live/status.json').read_bytes()
    previous = json.loads(raw)
    if previous.get('status') != 'STOPPED' or previous.get('storage', {}).get('error'):
        raise ValueError('Clean stopped collector required before preparing an epoch')
    if previous['storage']['received'] != previous['storage']['durable']:
        raise ValueError('Archive must be durable before paper-session boundary')
    session_id = 'paper-' + uuid.uuid4().hex
    digest = hashlib.sha256(raw).hexdigest()
    relative = f'data/live/paper_sessions/{session_id}/previous_snapshot.json'
    archive = root/relative
    archive.parent.mkdir(parents=True, exist_ok=False)
    with archive.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    plan = {'version': 1, 'session_id': session_id, 'authorized_host_ms': time.time_ns()//1_000_000,
            'authorization': authorization, 'mode': 'INDEPENDENT_PAPER_OBSERVATION',
            'previous_snapshot': relative, 'previous_sha256': digest,
            'initial_virtual_cash': '60', 'automatic_renewal': False}
    _exclusive_json(archive.parent/'authorization.json', plan)
    target = root/'config/paper_session.json'
    tmp = target.with_suffix('.tmp')
    with tmp.open('wb') as f:
        f.write(json.dumps(plan, ensure_ascii=False, indent=2).encode('utf8'))
        f.flush(); os.fsync(f.fileno())
    tmp.replace(target)
    return plan


def load_session(root, previous_raw):
    """Validate archived evidence and consume a new epoch at most once."""
    root = Path(root).resolve()
    path = root/'config/paper_session.json'
    if not path.exists():
        return None, [], False
    plan = json.loads(path.read_bytes())
    if (plan.get('version') != 1 or plan.get('authorization') != '恢复模拟挂单'
            or plan.get('mode') != 'INDEPENDENT_PAPER_OBSERVATION'
            or plan.get('automatic_renewal') is not False or plan.get('initial_virtual_cash') != '60'):
        raise ValueError('Invalid paper-session authorization')
    archive = (root/plan['previous_snapshot']).resolve()
    archive.relative_to(root/'data/live/paper_sessions')
    raw = archive.read_bytes()
    if hashlib.sha256(raw).hexdigest() != plan['previous_sha256']:
        raise ValueError('Archived paper snapshot hash mismatch')
    old = json.loads(raw)
    prior = old.get('paper', {})
    history = list(prior.get('archived_sessions', []))
    history.append({'id': (prior.get('session') or {}).get('id', 'legacy-paper'),
                    'status': 'CLOSED_UNKNOWN', 'source_run_id': old.get('run_id'),
                    'snapshot_path': plan['previous_snapshot'], 'snapshot_sha256': plan['previous_sha256'],
                    'account': prior.get('account'), 'orders': prior.get('orders', []),
                    'signals_seen_in_last_process': prior.get('signals_seen'),
                    'realized_pnl': None, 'actual_filled_qty': None})
    session = {'id': plan['session_id'], 'started_host_ms': plan['authorized_host_ms'],
               'mode': plan['mode'], 'automatic_renewal': False,
               'note': '独立纸面轮次；旧未知预留保留在历史轮次，不合并收益，不自动续开'}
    previous = json.loads(previous_raw) if previous_raw else {}
    marker = archive.parent/'activated.json'
    if (previous.get('paper', {}).get('session') or {}).get('id') == plan['session_id']:
        if not marker.exists():
            raise ValueError('Missing paper-session activation marker')
        return session, history, False
    if not previous_raw or hashlib.sha256(previous_raw).hexdigest() != plan['previous_sha256']:
        raise ValueError('Paper resume snapshot changed; no reset performed')
    _exclusive_json(marker, {'session_id': plan['session_id'], 'host_ms': time.time_ns()//1_000_000})
    return session, history, True
