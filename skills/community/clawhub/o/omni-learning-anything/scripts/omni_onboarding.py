"""Private, idempotent first-use observations. No credentials or free-form logs."""
import math
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import omni_core as c

EVENTS = ('started', 'user_action', 'authorization_started', 'authorization_finished',
          'intent_ready', 'plan_ready', 'first_lesson_ready', 'blocked', 'resumed')
STAGES = ('intent', 'requirements', 'dependencies', 'authorization', 'destination',
          'render', 'inspection', 'publish', 'scheduler')


def validate_usage(usage):
    allowed = {'source', 'input_tokens', 'output_tokens', 'cost', 'currency'}
    if not isinstance(usage, dict) or set(usage)-allowed or usage.get('source') != 'host_meter' or not set(usage)-{'source'}:
        raise ValueError('Usage accepts only actual host_meter input_tokens/output_tokens/cost/currency; never credentials.')
    for key in ('input_tokens', 'output_tokens'):
        if key in usage and (type(usage[key]) is not int or usage[key] < 0):
            raise ValueError('Metered tokens must be nonnegative integers.')
    if 'cost' in usage or 'currency' in usage:
        cost = usage.get('cost'); currency = usage.get('currency')
        if type(cost) not in (int, float) or not math.isfinite(cost) or cost < 0 or not isinstance(currency, str) or not re.fullmatch('[A-Z]{3}', currency):
            raise ValueError('Metered cost requires a finite nonnegative value and a three-letter currency.')


def ledger_path(root):
    path = Path(root).resolve()/'onboarding/events.json'
    if path.parent.is_symlink() or path.is_symlink():
        raise ValueError('Onboarding ledger must stay inside the course archive without symlinks.')
    return path


def load(root):
    path = ledger_path(root)
    if not path.exists():
        return []
    data = c.read(path)
    if not isinstance(data, dict) or data.get('schema') != 1 or not isinstance(data.get('events'), list):
        raise ValueError('Invalid onboarding ledger; preserve it for recovery.')
    return data['events']


def auth_start(events):
    pending = None
    for item in events:
        if item['event'] == 'authorization_started':
            pending = datetime.fromisoformat(item['at'])
        elif item['event'] == 'authorization_finished':
            pending = None
    return pending


def record(root, event, event_id, *, stage=None, user_actions=None, usage=None, now=None):
    if event not in EVENTS or not isinstance(event_id, str) or not re.fullmatch('[A-Za-z][A-Za-z0-9_.-]{0,63}', event_id):
        raise ValueError('Choose a documented event and a stable non-secret event ID.')
    if stage is not None and stage not in STAGES or event == 'blocked' and stage is None:
        raise ValueError('Choose a documented stage; blocked requires a stage.')
    if event == 'user_action':
        if type(user_actions) is not int or user_actions < 1:
            raise ValueError('A recorded user action needs a positive observed count.')
    elif user_actions is not None:
        raise ValueError('Only user_action events accept user_actions.')
    if usage is not None:
        validate_usage(usage)
    payload = {'id': event_id, 'event': event}
    if stage is not None: payload['stage'] = stage
    if user_actions is not None: payload['user_actions'] = user_actions
    if usage is not None: payload['usage'] = usage
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('Observation time needs a timezone.')
    root = Path(root); root.mkdir(mode=0o700, parents=True, exist_ok=True)
    with c.lock(root):
        events = load(root)
        for item in events:
            if item['id'] == event_id:
                if {k: v for k, v in item.items() if k != 'at'} != payload:
                    raise ValueError('Event ID already records a different observation; existing data preserved.')
                return {'recorded': False, 'event_id': event_id}
        if not events and event != 'started' or events and event == 'started':
            raise ValueError('Start once with a started event; reuse the same ledger after interruption.')
        if events and now < datetime.fromisoformat(events[-1]['at']):
            raise ValueError('Observation clock moved backwards; correct the clock before recording.')
        pending = auth_start(events)
        if event == 'authorization_started' and pending or event == 'authorization_finished' and not pending:
            raise ValueError('Authorization attempts must have paired started/finished observations.')
        events.append(dict(payload, at=now.astimezone(timezone.utc).isoformat()))
        path = ledger_path(root); path.parent.mkdir(mode=0o700, exist_ok=True)
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as temp:
                temp_path = Path(temp.name)
                json.dump({'schema': 1, 'events': events}, temp, ensure_ascii=False, indent=2)
                temp.write('\n')
            os.replace(temp_path, path)
        finally:
            if temp_path and temp_path.exists(): temp_path.unlink()
    return {'recorded': True, 'event_id': event_id}


def status(root, *, now=None):
    events = load(root); now = now or datetime.now(timezone.utc)
    started = datetime.fromisoformat(events[0]['at']) if events else None
    milestones = {}; waiting = 0; pending = None
    for item in events:
        at = datetime.fromisoformat(item['at']); kind = item['event']
        if kind in ('intent_ready', 'plan_ready', 'first_lesson_ready') and kind not in milestones:
            milestones[kind] = (at-started).total_seconds()
        if kind == 'authorization_started': pending = at
        if kind == 'authorization_finished':
            waiting += (at-pending).total_seconds(); pending = None
    if pending:
        waiting += max(0, (now-pending).total_seconds())
    return {'events': len(events), 'started_at': started.isoformat() if started else None,
            'elapsed_seconds': max(0, (now-started).total_seconds()) if started else None,
            'milestones_seconds': milestones, 'authorization_wait_seconds': waiting,
            'authorization_in_progress': pending is not None,
            'recorded_user_actions': sum(x.get('user_actions', 0) for x in events),
            'usage_reports': [{'event_id': x['id'], 'usage': x['usage']} for x in events if 'usage' in x],
            'total_cost': None,
            'note': 'Only recorded interactions and host-meter observations; completeness and total cost are unknown. No learning outcome or authorization success is inferred.'}
