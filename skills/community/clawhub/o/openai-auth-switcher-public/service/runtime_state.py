from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from config import get_runtime_summary, load_install_info
from channel_store import get_current_channel_slot, get_live_current_account, list_channels

import sys
CURRENT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = CURRENT_DIR.parent / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
from web_process_lib import systemd_unit_status  # noqa: E402

SYSTEMD_PREVIEW_UNIT = 'openai-auth-switcher-web-preview.service'

JsonDict = Dict[str, Any]


def build_page_state() -> JsonDict:
    install = load_install_info()
    runtime = get_runtime_summary()
    service = install.get('service') or {}
    attempted_systemd = service.get('attempted_systemd') or {}
    unit_name = service.get('unit_name') or attempted_systemd.get('unit_name') or SYSTEMD_PREVIEW_UNIT
    live_status = systemd_unit_status(unit_name)
    live_systemd_known = live_status.get('enabled_state') not in ('', 'not-found') or bool(live_status.get('fragment_path'))
    live_systemd_ready = bool(live_status.get('is_active'))
    status = live_status if live_status.get('ok') else (service.get('status') or attempted_systemd.get('status') or {})
    effective_mode = 'systemd-user' if live_systemd_known else service.get('mode')
    effective_ready = bool(live_systemd_ready and install.get('port')) if live_systemd_known else bool(install.get('ready') or service.get('ready') or service.get('ok'))
    channels = list_channels()
    current_slot = get_current_channel_slot()
    live_current = get_live_current_account()
    return {
        'ok': True,
        'install': install,
        'runtime': runtime,
        'mode': runtime.get('mode'),
        'auth_ready': runtime.get('auth_ready'),
        'service_mode': effective_mode,
        'service_ready': effective_ready,
        'channels': channels,
        'channel_summary': {
            'count': len(channels),
            'current_slot': current_slot,
            'live_current_account': live_current,
        },
        'service_summary': {
            'mode': effective_mode,
            'ready': effective_ready,
            'unit_name': unit_name,
            'active_state': status.get('active_state'),
            'sub_state': status.get('sub_state'),
            'result': status.get('result'),
            'port': install.get('port'),
            'host': install.get('host'),
            'local_url': install.get('local_url'),
            'log_path': service.get('log_path') or attempted_systemd.get('log_path'),
            'fallback_reason': service.get('fallback_reason'),
        },
        'next_action': 'import_auth_or_complete_first_auth' if not runtime.get('auth_ready') else 'review_runtime_then_switch',
    }


def parse_basic_auth(header_value: str | None) -> tuple[str, str] | None:
    if not header_value or not header_value.startswith('Basic '):
        return None
    import base64
    try:
        raw = base64.b64decode(header_value.split(' ', 1)[1]).decode('utf-8')
    except Exception:
        return None
    if ':' not in raw:
        return None
    user, password = raw.split(':', 1)
    return user, password
