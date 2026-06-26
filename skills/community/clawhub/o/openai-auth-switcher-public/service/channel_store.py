from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

CURRENT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = CURRENT_DIR.parent / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from auth_file_lib import OPENAI_PROFILE_KEY, get_openai_default_profile, load_auth_profiles_file, load_json_file, save_json_atomic  # noqa: E402
from paths import ensure_skill_dirs, get_profiles_dir, get_state_base_dir  # noqa: E402

JsonDict = Dict[str, Any]
CHANNELS_INDEX = get_state_base_dir() / 'state' / 'channels.json'
CURRENT_CHANNEL = get_state_base_dir() / 'state' / 'current-channel.json'


def _load_json(path: Path, default: JsonDict | List[Any]) -> JsonDict | List[Any]:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def _save_json(path: Path, data: JsonDict | List[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def ensure_channel_state() -> None:
    ensure_skill_dirs()
    if not CHANNELS_INDEX.exists():
        _save_json(CHANNELS_INDEX, {'channels': []})
    if not CURRENT_CHANNEL.exists():
        _save_json(CURRENT_CHANNEL, {'current_slot': None})


def list_channels() -> List[JsonDict]:
    ensure_channel_state()
    current = get_current_channel_slot()
    rows: List[JsonDict] = []
    for slot_dir in sorted(get_profiles_dir().glob('*')):
        if not slot_dir.is_dir():
            continue
        meta_path = slot_dir / 'meta.json'
        auth_path = slot_dir / 'auth-profile.json'
        meta = _load_json(meta_path, {}) if meta_path.exists() else {}
        auth = _load_json(auth_path, {}) if auth_path.exists() else {}
        rows.append({
            'slot': slot_dir.name,
            'display_name': meta.get('display_name') or slot_dir.name,
            'email': meta.get('email') or '',
            'note': meta.get('note') or '',
            'status': meta.get('status') or ('ready' if auth_path.exists() else 'pending_auth'),
            'disabled': bool(meta.get('disabled')),
            'account_id': auth.get('accountId') or meta.get('account_id'),
            'provider': auth.get('provider') or meta.get('provider') or 'openai-codex',
            'has_auth_file': auth_path.exists(),
            'is_current': slot_dir.name == current,
        })
    return rows


def get_current_channel_slot() -> str | None:
    ensure_channel_state()
    data = _load_json(CURRENT_CHANNEL, {'current_slot': None})
    slot = data.get('current_slot')
    return slot if isinstance(slot, str) and slot else None


def set_current_channel_slot(slot: str | None) -> None:
    ensure_channel_state()
    _save_json(CURRENT_CHANNEL, {'current_slot': slot})


def get_live_current_account() -> JsonDict:
    try:
        current = get_openai_default_profile(load_auth_profiles_file())
        return {
            'account_id': current.get('accountId'),
            'provider': current.get('provider') or OPENAI_PROFILE_KEY,
        }
    except Exception:
        return {'account_id': None, 'provider': OPENAI_PROFILE_KEY}


def create_channel(display_name: str, email: str = '', note: str = '') -> JsonDict:
    ensure_channel_state()
    base = 'channel'
    existing = {row['slot'] for row in list_channels()}
    idx = 1
    slot = f'{base}-{idx}'
    while slot in existing:
        idx += 1
        slot = f'{base}-{idx}'
    cmd = [
        'python3', str(SCRIPTS_DIR / 'profile_slot.py'), 'create',
        '--slot', slot,
        '--display-name', display_name.strip() or slot,
    ]
    if email.strip():
        cmd += ['--email', email.strip()]
    if note.strip():
        cmd += ['--note', note.strip()]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout or proc.stderr or 'create channel failed')
    return {'ok': True, 'slot': slot}


def import_channel_auth(slot: str, source: str) -> JsonDict:
    ensure_channel_state()
    slot_dir = get_profiles_dir() / slot
    auth_path = slot_dir / 'auth-profile.json'
    meta_path = slot_dir / 'meta.json'
    if not slot_dir.exists():
        raise RuntimeError(f'channel not found: {slot}')
    src = Path(source).expanduser().resolve()
    if not src.exists():
        raise RuntimeError(f'授权文件不存在: {src}')
    data = load_json_file(src)
    profile = ((data.get('profiles') or {}).get(OPENAI_PROFILE_KEY)) if 'profiles' in data else data
    if not isinstance(profile, dict):
        raise RuntimeError('授权文件格式不正确，缺少 openai-codex:default 或 profile 对象')
    save_json_atomic(auth_path, profile)
    meta = _load_json(meta_path, {}) if meta_path.exists() else {}
    meta['account_id'] = profile.get('accountId')
    meta['provider'] = profile.get('provider') or 'openai-codex'
    meta['status'] = 'ready'
    _save_json(meta_path, meta)
    return {'ok': True, 'slot': slot, 'account_id': profile.get('accountId')}


def export_channel_auth(slot: str) -> JsonDict:
    ensure_channel_state()
    slot_dir = get_profiles_dir() / slot
    auth_path = slot_dir / 'auth-profile.json'
    if not slot_dir.exists() or not auth_path.exists():
        raise RuntimeError('该通道暂无可导出的授权文件')
    return {'ok': True, 'slot': slot, 'path': str(auth_path)}


def activate_channel(slot: str) -> JsonDict:
    ensure_channel_state()
    slot_dir = get_profiles_dir() / slot
    auth_path = slot_dir / 'auth-profile.json'
    if not slot_dir.exists():
        raise RuntimeError(f'channel not found: {slot}')
    if not auth_path.exists():
        set_current_channel_slot(slot)
        return {
            'ok': False,
            'slot': slot,
            'activated': False,
            'message': '该通道已设为当前，但尚未完成授权接入。请先点“开始授权”，完成登录后再点“完成授权”。',
        }
    cmd = ['python3', str(SCRIPTS_DIR / 'switch_experiment.py'), '--target-slot', slot, '--json']
    proc = subprocess.run(cmd, capture_output=True, text=True)
    raw = proc.stdout or proc.stderr or '{}'
    try:
        result = json.loads(raw)
    except Exception:
        raise RuntimeError(raw)
    if proc.returncode == 0 and result.get('ok'):
        set_current_channel_slot(slot)
        return {
            'ok': True,
            'slot': slot,
            'activated': True,
            'message': f'已切换到通道 {slot}，当前 Claw 已接管该账号。',
            'detail': result,
        }
    raise RuntimeError(result.get('error') or raw)
