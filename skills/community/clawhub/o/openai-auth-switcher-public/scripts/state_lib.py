from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from paths import ensure_skill_dirs, get_state_dir

JsonDict = Dict[str, Any]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _history_path() -> Path:
    return get_state_dir() / 'experiment-history.jsonl'


def _last_experiment_path() -> Path:
    return get_state_dir() / 'last-experiment.json'


def _last_known_good_path() -> Path:
    return get_state_dir() / 'last-known-good.json'


def normalize_history_event(event: JsonDict) -> JsonDict:
    item = dict(event or {})
    if 'ts' not in item:
        item['ts'] = _now_iso()
    if 'event_type' not in item:
        item['event_type'] = 'account-activation' if item.get('ok') is True else 'account-event'
    if 'activation_method' not in item:
        if item.get('source') == 'oauth-completed':
            item['activation_method'] = 'oauth'
        elif item.get('activation') == 'restart-required':
            item['activation_method'] = 'switch-restart'
        else:
            item['activation_method'] = item.get('source') or 'unknown'
    if 'account_id' not in item:
        item['account_id'] = item.get('to_account_id') or item.get('from_account_id')
    if 'from_slot' not in item:
        item['from_slot'] = item.get('slot') if item.get('ok') is not True else item.get('from_slot')
    if 'to_slot' not in item:
        item['to_slot'] = item.get('slot') or item.get('target_slot')
    if 'account_slot' not in item:
        item['account_slot'] = item.get('to_slot') or item.get('slot')
    return item


def append_experiment_history(event: JsonDict) -> None:
    ensure_skill_dirs()
    item = normalize_history_event(event)
    with _history_path().open('a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def write_last_experiment(data: JsonDict) -> None:
    ensure_skill_dirs()
    if 'updated_at' not in data:
        data['updated_at'] = _now_iso()
    _last_experiment_path().write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_last_known_good(data: JsonDict) -> None:
    ensure_skill_dirs()
    if 'updated_at' not in data:
        data['updated_at'] = _now_iso()
    _last_known_good_path().write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_last_known_good() -> JsonDict:
    path = _last_known_good_path()
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))


def write_last_known_good_from_success(*, backup_file: str, account_id: str | None, profile_key: str = 'openai-codex:default') -> None:
    write_last_known_good({
        'backup_file': backup_file,
        'account_id': account_id,
        'profile_key': profile_key,
    })
