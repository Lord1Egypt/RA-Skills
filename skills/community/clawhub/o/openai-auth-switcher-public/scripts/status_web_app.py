#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
SERVICE_DIR = CURRENT_DIR.parent / 'service'
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from paths import get_runtime_dir
from config import load_install_info
from web_process_lib import port_open, systemd_unit_status, wait_for_port


SYSTEMD_PREVIEW_UNIT = 'openai-auth-switcher-web-preview.service'

PID_PATH = get_runtime_dir() / 'web-preview.pid'


def pid_alive(pid: int) -> bool:
    try:
        import os
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def main() -> int:
    install = load_install_info()
    pid = None
    if PID_PATH.exists():
        try:
            pid = int(PID_PATH.read_text(encoding='utf-8').strip())
        except Exception:
            pid = None
    host = install.get('host', '127.0.0.1')
    port = int(install.get('port', 0) or 0)
    port_ready = bool(port and (port_open(host, port) or wait_for_port(host, port, timeout_seconds=2.0, interval_seconds=0.2)))
    service = install.get('service') or {}
    attempted_systemd = service.get('attempted_systemd') or {}
    unit_name = service.get('unit_name') or attempted_systemd.get('unit_name') or SYSTEMD_PREVIEW_UNIT
    live_systemd_status = systemd_unit_status(unit_name)
    live_systemd_known = live_systemd_status.get('enabled_state') not in ('', 'not-found') or bool(live_systemd_status.get('fragment_path'))
    live_systemd_ready = bool(live_systemd_status.get('is_active'))
    if live_systemd_known:
        effective_mode = 'systemd-user'
        effective_ready = bool(live_systemd_ready and port_ready)
    else:
        effective_mode = service.get('mode')
        effective_ready = bool(service.get('ready') or service.get('ok') or port_ready)
    result = {
        'ok': True,
        'pid': pid,
        'pid_alive': bool(pid and pid_alive(pid)),
        'host': host,
        'port': port,
        'port_open': port_ready,
        'service_mode': effective_mode,
        'service_ready': effective_ready,
        'systemd_status': live_systemd_status,
        'install': install,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
