#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from paths import get_runtime_dir

PID_PATH = get_runtime_dir() / 'web-preview.pid'
SYSTEMD_PREVIEW_UNIT = 'openai-auth-switcher-web-preview.service'


def main() -> int:
    result = {
        'ok': True,
        'systemd_stopped': False,
        'background_stopped': False,
        'pid': None,
        'errors': [],
    }

    stop_service = subprocess.run(['systemctl', '--user', 'disable', '--now', SYSTEMD_PREVIEW_UNIT], capture_output=True, text=True)
    if stop_service.returncode == 0:
        result['systemd_stopped'] = True
    elif 'not loaded' not in ((stop_service.stderr or '') + (stop_service.stdout or '')):
        result['errors'].append((stop_service.stderr or stop_service.stdout or '').strip())

    if PID_PATH.exists():
        try:
            pid = int(PID_PATH.read_text(encoding='utf-8').strip())
            result['pid'] = pid
            os.kill(pid, 15)
            result['background_stopped'] = True
        except ProcessLookupError:
            result['background_stopped'] = True
        except Exception as e:
            result['errors'].append(str(e))
        finally:
            PID_PATH.unlink(missing_ok=True)

    if result['errors']:
        result['ok'] = False
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
