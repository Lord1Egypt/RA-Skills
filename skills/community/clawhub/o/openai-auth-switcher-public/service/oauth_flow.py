from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
SCRIPTS_DIR = BASE_DIR / 'scripts'
STATE_DIR = BASE_DIR / 'skill-data' / 'state'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from channel_store import set_current_channel_slot  # noqa: E402

JsonDict = Dict[str, Any]


STATUS_LABELS = {
    'starting': '正在生成授权链接',
    'waiting_callback': '等待用户完成授权',
    'processing': '正在处理回调',
    'completed': '已完成授权',
    'failed': '授权失败',
    'superseded': '已被新的授权任务替代',
}


def oauth_status_label(status: str | None) -> str:
    return STATUS_LABELS.get(status or '', status or '未知状态')


def ensure_state_dir() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / 'oauth-sessions').mkdir(parents=True, exist_ok=True)


def read_json_file(path: Path) -> JsonDict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def write_json_file(path: Path, data: JsonDict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def oauth_session_dir(session_id: str) -> Path:
    return STATE_DIR / 'oauth-sessions' / session_id


def read_oauth_sessions(limit: int = 20) -> List[JsonDict]:
    ensure_state_dir()
    rows: List[JsonDict] = []
    for d in sorted((STATE_DIR / 'oauth-sessions').glob('*')):
        if not d.is_dir():
            continue
        item = read_json_file(d / 'session.json')
        if item:
            rows.append(item)
    return rows[-limit:]


def start_oauth_session(slot: str, display_name: str | None = None) -> JsonDict:
    ensure_state_dir()
    for existing in read_oauth_sessions():
        if existing.get('slot') == slot and existing.get('status') in ('starting', 'waiting_callback', 'processing'):
            existing['status'] = 'superseded'
            write_json_file(oauth_session_dir(existing['sessionId']) / 'session.json', existing)
    session_id = uuid.uuid4().hex[:16]
    session_dir = oauth_session_dir(session_id)
    session_dir.mkdir(parents=True, exist_ok=True)
    write_json_file(session_dir / 'session.json', {
        'sessionId': session_id,
        'slot': slot,
        'displayName': display_name or slot,
        'status': 'starting',
    })
    env = os.environ.copy()
    env['PATH'] = '/root/.local/share/pnpm:/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin:' + env.get('PATH', '')
    subprocess.Popen(
        ['node', str((Path('/root/.openclaw/workspace/skills/openai-auth-switcher/scripts/oauth_web_login.mjs'))), str(STATE_DIR), session_id, slot, display_name or slot],
        cwd=str(BASE_DIR),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(30):
        sess = read_json_file(session_dir / 'session.json')
        if sess.get('authUrl') or sess.get('status') == 'failed':
            return {'ok': True, 'session': sess}
        time.sleep(0.2)
    return {'ok': True, 'session': read_json_file(session_dir / 'session.json')}


def parse_callback_url(callback_url: str) -> JsonDict:
    parsed = urlparse(callback_url)
    query = parse_qs(parsed.query)
    code = (query.get('code') or [''])[0]
    state = (query.get('state') or [''])[0]
    return {
        'host': parsed.netloc,
        'path': parsed.path,
        'has_code': bool(code),
        'has_state': bool(state),
        'code_preview': (code[:12] + '...') if code else None,
        'state_preview': (state[:12] + '...') if state else None,
    }


def submit_oauth_callback(session_id: str, callback_url: str) -> JsonDict:
    session_dir = oauth_session_dir(session_id)
    if not session_dir.exists():
        return {'ok': False, 'error': f'session not found: {session_id}'}
    (session_dir / 'callback.txt').write_text(callback_url.strip() + '\n', encoding='utf-8')
    session = {}
    for _ in range(40):
        session = read_json_file(session_dir / 'session.json')
        if session.get('status') in ('completed', 'failed'):
            break
        time.sleep(0.5)
    if session.get('status') == 'completed':
        slot = (session.get('slot') or '').strip()
        if slot:
            set_current_channel_slot(slot)
        return {
            'ok': True,
            'status': 'completed',
            'sessionId': session_id,
            'slot': slot,
            'account_id': session.get('account_id'),
            'message': '授权完成，账号已接入。现在可以直接设为当前。',
            'parsed': parse_callback_url(callback_url),
        }
    if session.get('status') == 'failed':
        return {
            'ok': False,
            'status': 'failed',
            'sessionId': session_id,
            'error': session.get('error') or '授权失败',
            'parsed': parse_callback_url(callback_url),
        }
    return {
        'ok': True,
        'status': 'processing',
        'sessionId': session_id,
        'message': '回调已提交，后台仍在处理，请稍后刷新。',
        'parsed': parse_callback_url(callback_url),
    }
