from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict, List

from paths import get_sessions_dir

SESSION_ERROR_KEYWORDS = [
    'auth',
    'provider',
    'unauthorized',
    'rate limit',
    'unknown model',
    'failover',
]

JsonDict = Dict[str, Any]


def run_command(command: list[str], timeout: int | None = None) -> JsonDict:
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return {
            'ok': proc.returncode == 0,
            'exit_code': proc.returncode,
            'stdout': proc.stdout,
            'stderr': proc.stderr,
        }
    except subprocess.TimeoutExpired as e:
        return {
            'ok': False,
            'exit_code': None,
            'stdout': e.stdout or '',
            'stderr': (e.stderr or '') + f'\nTIMEOUT after {timeout}s',
        }


def probe_gateway_status() -> JsonDict:
    return run_command(['openclaw', 'gateway', 'status'])


def probe_openclaw_status() -> JsonDict:
    return run_command(['openclaw', 'status'])


def probe_auth_structure(profile: JsonDict) -> JsonDict:
    required = ['type', 'provider', 'access', 'refresh', 'expires']
    missing = [key for key in required if key not in profile]
    return {'ok': not missing, 'missing': missing}


def find_recent_session_files(limit: int = 3) -> List[Path]:
    sessions_dir = get_sessions_dir()
    if sessions_dir is None or not sessions_dir.exists():
        return []
    files = sorted(sessions_dir.glob('*.jsonl'), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:limit]


def scan_session_errors(files: List[Path]) -> List[JsonDict]:
    results: List[JsonDict] = []
    for path in files:
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        lines = text.splitlines()[-300:]
        for line in lines:
            low = line.lower()
            if any(keyword in low for keyword in SESSION_ERROR_KEYWORDS):
                results.append({'file': str(path), 'line': line[:500]})
    return results


def probe_runtime_summary(session_limit: int = 3) -> JsonDict:
    return {
        'gateway': probe_gateway_status(),
        'status': probe_openclaw_status(),
        'recent_errors': scan_session_errors(find_recent_session_files(session_limit)),
    }
