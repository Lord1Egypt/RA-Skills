from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from paths import detect_runtime, get_profiles_dir, get_state_dir

JsonDict = Dict[str, Any]
STATE_DIR = get_state_dir()
PROFILES_DIR = get_profiles_dir()
REPORT_TZ = ZoneInfo('Asia/Shanghai')
HOURLY_ARCHIVE_PATH = STATE_DIR / 'hourly-archive.json'
DAILY_ARCHIVE_PATH = STATE_DIR / 'daily-archive.json'
LEDGER_STATE_PATH = STATE_DIR / 'token-ledger.json'


def _parse_iso(ts: str) -> datetime:
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    return datetime.fromisoformat(ts)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def load_slots() -> List[JsonDict]:
    rows = []
    for d in sorted(PROFILES_DIR.glob('*')):
        if not d.is_dir():
            continue
        meta = {}
        auth = {}
        mp = d / 'meta.json'
        ap = d / 'auth-profile.json'
        if mp.exists():
            try:
                meta = json.loads(mp.read_text(encoding='utf-8'))
            except Exception:
                meta = {}
        if ap.exists():
            try:
                auth = json.loads(ap.read_text(encoding='utf-8'))
            except Exception:
                auth = {}
        rows.append({
            'slot': d.name,
            'display_name': meta.get('display_name') or d.name,
            'account_id': meta.get('account_id') or auth.get('accountId'),
        })
    return rows


def iter_attribution_rows() -> List[JsonDict]:
    path = STATE_DIR / 'token-attribution.jsonl'
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


def floor_hour(dt: datetime) -> datetime:
    return dt.astimezone(REPORT_TZ).replace(minute=0, second=0, microsecond=0)


def floor_day(dt: datetime) -> datetime:
    return dt.astimezone(REPORT_TZ).replace(hour=0, minute=0, second=0, microsecond=0)


def _read_json(path: Path) -> JsonDict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _write_json(path: Path, data: JsonDict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_reset_map() -> Dict[str, str | None]:
    data = _read_json(LEDGER_STATE_PATH)
    slots = (data.get('slots') or {}) if isinstance(data, dict) else {}
    return {str(slot): (bucket.get('reset_at') if isinstance(bucket, dict) else None) for slot, bucket in slots.items()}


def load_hourly_archive() -> JsonDict:
    data = _read_json(HOURLY_ARCHIVE_PATH)
    data.setdefault('ok', True)
    data.setdefault('timezone', 'Asia/Shanghai')
    data.setdefault('buckets', {})
    data.setdefault('updated_at', None)
    return data


def save_hourly_archive(data: JsonDict) -> None:
    data['updated_at'] = _now().isoformat()
    _write_json(HOURLY_ARCHIVE_PATH, data)


def load_daily_archive() -> JsonDict:
    data = _read_json(DAILY_ARCHIVE_PATH)
    data.setdefault('ok', True)
    data.setdefault('timezone', 'Asia/Shanghai')
    data.setdefault('days', {})
    data.setdefault('updated_at', None)
    return data


def save_daily_archive(data: JsonDict) -> None:
    data['updated_at'] = _now().isoformat()
    _write_json(DAILY_ARCHIVE_PATH, data)


def list_completed_hour_rows(now: datetime | None = None) -> List[JsonDict]:
    ref = now or _now()
    current_hour = floor_hour(ref)
    rows: List[JsonDict] = []
    for row in iter_attribution_rows():
        hour = floor_hour(row['ts'])
        if hour >= current_hour:
            continue
        item = dict(row)
        item['hour_key'] = hour.isoformat()
        item['day_key'] = hour.date().isoformat()
        rows.append(item)
    return rows


def aggregate_hour_rows(rows: List[JsonDict]) -> Dict[str, JsonDict]:
    slot_display = {s['slot']: s.get('display_name') or s['slot'] for s in load_slots()}
    agg: Dict[str, JsonDict] = {}
    for row in rows:
        slot = str(row['slot'])
        hour_key = str(row['hour_key'])
        key = f'{slot}::{hour_key}'
        item = agg.setdefault(key, {
            'slot': slot,
            'display_name': slot_display.get(slot, slot),
            'hour_key': hour_key,
            'day_key': str(row['day_key']),
            'tokens': 0,
            'message_count': 0,
            'source': 'token-attribution-hourly-rollup',
        })
        item['tokens'] += int(row.get('delta_tokens') or 0)
        item['message_count'] += 1
    return agg


def archive_completed_hours(now: datetime | None = None) -> JsonDict:
    ref = now or _now()
    archive = load_hourly_archive()
    buckets = archive.setdefault('buckets', {})
    aggregated = aggregate_hour_rows(list_completed_hour_rows(ref))
    for key, item in aggregated.items():
        buckets[key] = item
    archive['mode'] = 'hourly-archive-by-slot'
    archive['note'] = '每小时归档前一个整点小时的各账号消耗；查询优先使用归档数据。'
    archive['last_archived_hour'] = (floor_hour(ref) - timedelta(hours=1)).isoformat()
    save_hourly_archive(archive)
    return archive


def archive_completed_days(now: datetime | None = None) -> JsonDict:
    ref = now or _now()
    today_key = floor_day(ref).date().isoformat()
    hourly = load_hourly_archive()
    daily = load_daily_archive()
    days = daily.setdefault('days', {})
    tmp: Dict[str, JsonDict] = {}
    for item in (hourly.get('buckets') or {}).values():
        if not isinstance(item, dict):
            continue
        day_key = str(item.get('day_key') or '')
        if not day_key or day_key >= today_key:
            continue
        slot = str(item.get('slot') or '')
        if not slot:
            continue
        key = f'{slot}::{day_key}'
        bucket = tmp.setdefault(key, {
            'slot': slot,
            'display_name': item.get('display_name') or slot,
            'day_key': day_key,
            'tokens': 0,
            'message_count': 0,
            'source': 'hourly-archive-daily-rollup',
        })
        bucket['tokens'] += int(item.get('tokens') or 0)
        bucket['message_count'] += int(item.get('message_count') or 0)
    for key, item in tmp.items():
        days[key] = item
    daily['mode'] = 'daily-archive-by-slot'
    daily['note'] = '每天归档前一天各账号总消耗；7天/30天查询直接聚合日归档与当日小时归档。'
    daily['last_archived_day'] = (floor_day(ref) - timedelta(days=1)).date().isoformat()
    save_daily_archive(daily)
    return daily


def aggregate_live_current_hour(now: datetime | None = None) -> Dict[str, JsonDict]:
    ref = now or _now()
    current_hour = floor_hour(ref)
    slot_display = {s['slot']: s.get('display_name') or s['slot'] for s in load_slots()}
    agg: Dict[str, JsonDict] = {}
    for row in iter_attribution_rows():
        hour = floor_hour(row['ts'])
        if hour != current_hour:
            continue
        slot = str(row['slot'])
        item = agg.setdefault(slot, {
            'slot': slot,
            'display_name': slot_display.get(slot, slot),
            'hour_key': current_hour.isoformat(),
            'day_key': current_hour.date().isoformat(),
            'tokens': 0,
            'message_count': 0,
            'source': 'token-attribution-live-current-hour',
        })
        item['tokens'] += int(row.get('delta_tokens') or 0)
        item['message_count'] += 1
    return agg


def _within_reset(ts: datetime, reset_at: str | None) -> bool:
    if not reset_at:
        return True
    try:
        return ts >= _parse_iso(str(reset_at))
    except Exception:
        return True


def summarize_slot_windows(now: datetime | None = None) -> JsonDict:
    ref = now or _now()
    archive_completed_hours(ref)
    archive_completed_days(ref)
    slots = load_slots()
    slot_display = {s['slot']: s.get('display_name') or s['slot'] for s in slots}
    reset_map = load_reset_map()
    hourly = load_hourly_archive()
    daily = load_daily_archive()
    live_current = aggregate_live_current_hour(ref)
    today_key = floor_day(ref).date().isoformat()
    cutoff_7 = floor_day(ref - timedelta(days=6)).date().isoformat()
    cutoff_30 = floor_day(ref - timedelta(days=29)).date().isoformat()

    result_slots: Dict[str, JsonDict] = {}
    for slot in sorted(slot_display.keys() | live_current.keys()):
        result_slots[slot] = {
            'slot': slot,
            'display_name': slot_display.get(slot, slot),
            'source': 'hourly+daily-archive-rollup',
            'today_tokens': 0,
            'last_7d_tokens': 0,
            'last_30d_tokens': 0,
            'lifetime_tokens': 0,
            'reset_at': reset_map.get(slot),
            'updated_at': ref.isoformat(),
        }

    for item in (hourly.get('buckets') or {}).values():
        if not isinstance(item, dict):
            continue
        slot = str(item.get('slot') or '')
        hour_key = str(item.get('hour_key') or '')
        if not slot or slot not in result_slots or not hour_key:
            continue
        hour_dt = _parse_iso(hour_key)
        if not _within_reset(hour_dt, result_slots[slot].get('reset_at')):
            continue
        tokens = int(item.get('tokens') or 0)
        day_key = str(item.get('day_key') or '')
        if day_key == today_key:
            result_slots[slot]['today_tokens'] += tokens
            result_slots[slot]['lifetime_tokens'] += tokens

    for slot, item in live_current.items():
        if slot not in result_slots:
            result_slots[slot] = {
                'slot': slot,
                'display_name': item.get('display_name') or slot,
                'source': 'hourly+daily-archive-rollup',
                'today_tokens': 0,
                'last_7d_tokens': 0,
                'last_30d_tokens': 0,
                'lifetime_tokens': 0,
                'reset_at': reset_map.get(slot),
                'updated_at': ref.isoformat(),
            }
        hour_dt = _parse_iso(str(item['hour_key']))
        if not _within_reset(hour_dt, result_slots[slot].get('reset_at')):
            continue
        tokens = int(item.get('tokens') or 0)
        result_slots[slot]['today_tokens'] += tokens
        result_slots[slot]['lifetime_tokens'] += tokens

    for item in (daily.get('days') or {}).values():
        if not isinstance(item, dict):
            continue
        slot = str(item.get('slot') or '')
        day_key = str(item.get('day_key') or '')
        if not slot or slot not in result_slots or not day_key:
            continue
        day_dt = datetime.fromisoformat(f'{day_key}T00:00:00+08:00').astimezone(timezone.utc)
        if not _within_reset(day_dt, result_slots[slot].get('reset_at')):
            continue
        tokens = int(item.get('tokens') or 0)
        if cutoff_7 <= day_key < today_key:
            result_slots[slot]['last_7d_tokens'] += tokens
        if cutoff_30 <= day_key < today_key:
            result_slots[slot]['last_30d_tokens'] += tokens
        result_slots[slot]['lifetime_tokens'] += tokens

    for slot, bucket in result_slots.items():
        bucket['last_7d_tokens'] += int(bucket.get('today_tokens') or 0)
        bucket['last_30d_tokens'] += int(bucket.get('today_tokens') or 0)

    return {
        'ok': True,
        'mode': 'hourly-daily-archive-rollup-v1',
        'timezone': 'Asia/Shanghai',
        'slots': result_slots,
        'updated_at': ref.isoformat(),
        'note': '本地统计按小时归档 + 按天归档；7天/30天查询聚合归档数据与当日小时数据。非官方账单。',
    }


def build_hourly_usage_payload(now: datetime | None = None) -> JsonDict:
    ref = now or _now()
    archive_completed_hours(ref)
    archive_completed_days(ref)
    hourly = load_hourly_archive()
    daily = load_daily_archive()
    live_current = aggregate_live_current_hour(ref)
    display_names = {s['slot']: s.get('display_name') or s['slot'] for s in load_slots()}

    hourly_by_slot: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    hourly_total: Dict[str, int] = defaultdict(int)
    daily_by_slot: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    daily_total: Dict[str, int] = defaultdict(int)

    for item in (hourly.get('buckets') or {}).values():
        if not isinstance(item, dict):
            continue
        slot = str(item.get('slot') or '')
        hour_key = str(item.get('hour_key') or '')
        day_key = str(item.get('day_key') or '')
        tokens = int(item.get('tokens') or 0)
        if slot and hour_key:
            hourly_by_slot[slot][hour_key] += tokens
            hourly_total[hour_key] += tokens
        if slot and day_key:
            daily_by_slot[slot][day_key] += tokens
            daily_total[day_key] += tokens

    for slot, item in live_current.items():
        hour_key = str(item.get('hour_key') or '')
        day_key = str(item.get('day_key') or '')
        tokens = int(item.get('tokens') or 0)
        if hour_key:
            hourly_by_slot[slot][hour_key] += tokens
            hourly_total[hour_key] += tokens
        if day_key:
            daily_by_slot[slot][day_key] += tokens
            daily_total[day_key] += tokens

    hours = sorted(hourly_total.keys())
    days = sorted(daily_total.keys())
    slots_payload = {}
    for slot_name in sorted(set(list(display_names.keys()) + list(hourly_by_slot.keys()) + list(daily_by_slot.keys()))):
        slots_payload[slot_name] = {
            'slot': slot_name,
            'display_name': display_names.get(slot_name, slot_name),
            'hourly_series': [{'bucket': hour, 'tokens': int(hourly_by_slot.get(slot_name, {}).get(hour, 0))} for hour in hours],
            'daily_series': [{'bucket': day, 'tokens': int(daily_by_slot.get(slot_name, {}).get(day, 0))} for day in days],
        }

    runtime = detect_runtime()
    return {
        'ok': True,
        'mode': 'hourly-daily-archive-rollup-v1',
        'timezone': 'Asia/Shanghai',
        'runtime': {
            'openclaw_root': runtime.get('openclaw_root'),
            'workspace': runtime.get('workspace'),
        },
        'hourly': {'buckets': hours, 'global_series': [{'bucket': hour, 'tokens': int(hourly_total.get(hour, 0))} for hour in hours]},
        'daily': {'buckets': days, 'global_series': [{'bucket': day, 'tokens': int(daily_total.get(day, 0))} for day in days]},
        'slots': slots_payload,
        'updated_at': ref.isoformat(),
        'note': '小时图使用小时归档 + 当前小时实时增量；天图使用日归档 + 当天小时汇总。北京时间。',
    }
