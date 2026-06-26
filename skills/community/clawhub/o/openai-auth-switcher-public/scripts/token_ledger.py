#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from paths import detect_runtime, get_profiles_dir, get_state_dir, get_sessions_dir
from usage_rollup_lib import summarize_slot_windows

ACTIVE_SLOT_FALLBACK = 'unknown'
LEDGER_VERSION = 8
REPORT_TZ = ZoneInfo('Asia/Shanghai')
JsonDict = Dict[str, Any]


def _parse_iso(ts: str) -> datetime:
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    return datetime.fromisoformat(ts)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _state_path() -> Path:
    return get_state_dir() / 'token-ledger.json'


def _attribution_log_path() -> Path:
    return get_state_dir() / 'token-attribution.jsonl'


def _auth_profiles_runtime_path() -> Path | None:
    runtime = detect_runtime()
    p = runtime.get('auth_profiles_path')
    return Path(p) if p else None


def iter_attribution_rows() -> List[JsonDict]:
    path = _attribution_log_path()
    rows: List[JsonDict] = []
    if not path.exists():
        return rows
    try:
        for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
            try:
                obj = json.loads(line)
            except Exception:
                continue
            key = obj.get('key')
            ts = obj.get('ts')
            slot = obj.get('slot')
            delta = obj.get('delta_tokens')
            if not key or not ts or not slot:
                continue
            try:
                dt = _parse_iso(str(ts))
                delta_int = int(delta or 0)
            except Exception:
                continue
            rows.append({'key': str(key), 'ts': dt, 'slot': str(slot), 'delta_tokens': delta_int})
    except OSError:
        return []
    rows.sort(key=lambda x: (x['ts'], x['key']))
    return rows


def load_slots() -> List[JsonDict]:
    rows = []
    for d in sorted(get_profiles_dir().glob('*')):
        if not d.is_dir():
            continue
        meta = {}
        auth = {}
        mp = d / 'meta.json'
        ap = d / 'auth-profile.json'
        if mp.exists():
            meta = json.loads(mp.read_text(encoding='utf-8'))
        if ap.exists():
            auth = json.loads(ap.read_text(encoding='utf-8'))
        rows.append({'slot': d.name, 'display_name': meta.get('display_name') or d.name, 'account_id': meta.get('account_id') or auth.get('accountId')})
    return rows


def load_switch_events() -> List[JsonDict]:
    path = get_state_dir() / 'experiment-history.jsonl'
    events = []
    if path.exists():
        for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
            try:
                obj = json.loads(line)
            except Exception:
                continue
            ts = obj.get('ts')
            to_account = obj.get('to_account_id') or obj.get('account_id')
            source = obj.get('source') or obj.get('activation_method') or 'switch-history'
            if ts and to_account and obj.get('ok') is True:
                events.append({'ts': _parse_iso(ts), 'account_id': to_account, 'source': source})

    auth_file = _auth_profiles_runtime_path()
    if auth_file and auth_file.exists():
        try:
            data = json.loads(auth_file.read_text(encoding='utf-8'))
            current = (((data.get('profiles') or {}).get('openai-codex:default')) or {}).get('accountId')
            mtime = datetime.fromtimestamp(auth_file.stat().st_mtime, tz=timezone.utc)
            last_event = events[-1] if events else None
            if current and (not last_event or (mtime > last_event['ts'] and current != last_event.get('account_id'))):
                events.append({'ts': mtime, 'account_id': current, 'source': 'auth-file-mtime'})
        except Exception:
            pass

    events.sort(key=lambda x: x['ts'])
    return events


def resolve_current_slot(slots: List[JsonDict]) -> str:
    auth_file = _auth_profiles_runtime_path()
    if not auth_file or not auth_file.exists():
        return ACTIVE_SLOT_FALLBACK
    data = json.loads(auth_file.read_text(encoding='utf-8'))
    current = (((data.get('profiles') or {}).get('openai-codex:default')) or {}).get('accountId')
    for s in slots:
        if s.get('account_id') == current:
            return s['slot']
    return ACTIVE_SLOT_FALLBACK


def account_to_slot_map(slots: List[JsonDict]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for s in slots:
        account_id = s.get('account_id')
        if account_id:
            out[account_id] = s['slot']
    return out


def slot_for_timestamp(ts: datetime, switches: List[JsonDict], current_slot: str, account_slot_map: Dict[str, str]) -> str:
    if not switches:
        return current_slot
    chosen_account = None
    for ev in switches:
        if ev['ts'] <= ts:
            chosen_account = ev['account_id']
        else:
            break
    if chosen_account:
        return account_slot_map.get(chosen_account, ACTIVE_SLOT_FALLBACK)
    return ACTIVE_SLOT_FALLBACK


def make_message_key(session_path: Path, msg_id: str, ts: str) -> str:
    return f'{session_path.name}:{msg_id}:{ts}'


def iter_usage_messages() -> List[JsonDict]:
    rows = []
    sessions_dir = get_sessions_dir()
    if sessions_dir is None or not sessions_dir.exists():
        return rows
    for path in sessions_dir.glob('*.jsonl'):
        session_rows = []
        try:
            for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get('type') != 'message':
                    continue
                msg = obj.get('message') or {}
                if msg.get('role') != 'assistant':
                    continue
                usage = msg.get('usage') or {}
                total = usage.get('totalTokens')
                ts = obj.get('timestamp')
                msg_id = obj.get('id')
                if total is None or ts is None or msg_id is None:
                    continue
                try:
                    dt = _parse_iso(ts)
                except Exception:
                    continue
                session_rows.append({'key': make_message_key(path, str(msg_id), str(ts)), 'ts': dt, 'session': path.name, 'total_tokens': int(total or 0), 'model': msg.get('model'), 'provider': msg.get('provider')})
        except OSError:
            continue

        session_rows.sort(key=lambda x: (x['ts'], x['key']))
        prev_total = None
        for row in session_rows:
            total = row['total_tokens']
            delta = total if prev_total is None else total - prev_total
            if prev_total is not None and delta < 0:
                delta = total
            prev_total = total
            row['delta_tokens'] = int(delta)
            rows.append(row)

    rows.sort(key=lambda x: (x['ts'], x['key']))
    return rows


def default_slot_bucket(slot: str, display_name: str, now: datetime) -> JsonDict:
    return {'slot': slot, 'display_name': display_name, 'source': 'session-usage-incremental', 'today_tokens': 0, 'last_7d_tokens': 0, 'last_30d_tokens': 0, 'lifetime_tokens': 0, 'reset_at': None, 'updated_at': now.isoformat()}


def ensure_slot_buckets(ledger: JsonDict, slots: List[JsonDict], now: datetime) -> None:
    ledger.setdefault('slots', {})
    for s in slots:
        bucket = ledger['slots'].setdefault(s['slot'], default_slot_bucket(s['slot'], s['display_name'], now))
        bucket['display_name'] = s['display_name']
        bucket['source'] = 'session-usage-incremental'
        bucket.setdefault('today_tokens', 0)
        bucket.setdefault('last_7d_tokens', 0)
        bucket.setdefault('last_30d_tokens', 0)
        bucket.setdefault('lifetime_tokens', 0)
        bucket.setdefault('reset_at', None)
        bucket['updated_at'] = now.isoformat()


def fresh_ledger(slots: List[JsonDict], now: datetime, initialized_at: str) -> JsonDict:
    ledger: JsonDict = {
        'version': LEDGER_VERSION,
        'mode': 'timestamp-switch-attribution-v1',
        'slots': {},
        'updated_at': now.isoformat(),
        'initialized_at': initialized_at,
        'last_processed_at': initialized_at,
        'processed_keys': [],
        'attribution': {},
        'note': '本地估算 token 账本：按 usage 时间戳结合切换历史归属到 slot；今日口径按 Asia/Shanghai 自然日统计；非官方账单。',
    }
    ensure_slot_buckets(ledger, slots, now)
    return ledger


def build_ledger() -> JsonDict:
    now = _now()
    slots = load_slots()
    current_slot = resolve_current_slot(slots)
    switches = load_switch_events()
    account_slot_map = account_to_slot_map(slots)
    usage_rows = iter_usage_messages()
    state_path = _state_path()

    existing: JsonDict = {}
    if state_path.exists():
        try:
            existing = json.loads(state_path.read_text(encoding='utf-8'))
        except Exception:
            existing = {}

    if existing.get('version') != LEDGER_VERSION or existing.get('mode') != 'hourly-daily-archive-rollup-v1':
        initialized_at = now.isoformat()
        existing = fresh_ledger(slots, now, initialized_at)

    ledger = existing
    ensure_slot_buckets(ledger, slots, now)
    processed_keys = set(ledger.get('processed_keys') or [])
    attribution = ledger.setdefault('attribution', {})
    new_rows = [row for row in usage_rows if row['key'] not in processed_keys]

    log_path = _attribution_log_path()
    for row in new_rows:
        slot = slot_for_timestamp(row['ts'], switches, current_slot, account_slot_map)
        if slot not in ledger['slots']:
            ledger['slots'][slot] = default_slot_bucket(slot, slot, now)
        attribution[row['key']] = slot
        ledger['slots'][slot]['updated_at'] = now.isoformat()
        processed_keys.add(row['key'])
        ledger['last_processed_at'] = row['ts'].isoformat()
        try:
            with log_path.open('a', encoding='utf-8') as f:
                f.write(json.dumps({'key': row['key'], 'ts': row['ts'].isoformat(), 'delta_tokens': row['delta_tokens'], 'slot': slot, 'source': 'timestamp-switch-attribution-v1', 'processed_at': now.isoformat()}, ensure_ascii=False) + '\n')
        except Exception:
            pass

    rolled = summarize_slot_windows(now)
    rolled_slots = rolled.get('slots') or {}
    for slot_name, slot_data in rolled_slots.items():
        ledger['slots'].setdefault(slot_name, default_slot_bucket(slot_name, slot_data.get('display_name') or slot_name, now))
        ledger['slots'][slot_name].update(slot_data)
    ledger['ok'] = True
    ledger['version'] = LEDGER_VERSION
    ledger['mode'] = 'hourly-daily-archive-rollup-v1'
    ledger['processed_keys'] = sorted(processed_keys)
    ledger['updated_at'] = now.isoformat()
    ledger['note'] = rolled.get('note') or '本地统计改为按小时归档 + 按天归档；非官方账单。'
    runtime = detect_runtime()
    ledger['runtime'] = {'openclaw_root': runtime.get('openclaw_root'), 'workspace': runtime.get('workspace')}
    return ledger


def main() -> int:
    ledger = build_ledger()
    print(json.dumps(ledger, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
