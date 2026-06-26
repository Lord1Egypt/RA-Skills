from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from pathlib import Path as _Path
import sys

CURRENT_DIR = _Path(__file__).resolve().parent
SCRIPTS_DIR = CURRENT_DIR.parent / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from paths import ensure_skill_dirs, get_runtime_dir, detect_runtime, get_state_base_dir  # noqa: E402

JsonDict = Dict[str, Any]
INSTALL_INFO_PATH = get_runtime_dir() / 'install-info.json'


def load_install_info() -> JsonDict:
    if not INSTALL_INFO_PATH.exists():
        return {}
    try:
        return json.loads(INSTALL_INFO_PATH.read_text(encoding='utf-8'))
    except Exception:
        return {}


def save_install_info(data: JsonDict) -> None:
    ensure_skill_dirs()
    INSTALL_INFO_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def build_web_url(host: str, port: int) -> str:
    return f'http://{host}:{port}'


def get_server_ip() -> str:
    return os.environ.get('OPENAI_AUTH_SWITCHER_SERVER_IP', '<server-ip>')


def build_ssh_tunnel_command(port: int, user: str = 'root') -> str:
    return f'ssh -L {port}:127.0.0.1:{port} {user}@{get_server_ip()}'


def get_runtime_summary() -> JsonDict:
    runtime = detect_runtime()
    auth_exists = bool(runtime.get('auth_profiles_exists'))
    return {
        'runtime': runtime,
        'state_base_dir': str(get_state_base_dir()),
        'mode': 'managed' if auth_exists else 'onboarding',
        'auth_ready': auth_exists,
    }
