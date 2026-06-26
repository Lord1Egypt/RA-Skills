#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path

from paths import detect_runtime, get_state_base_dir


RECOMMENDED = {
    'python_major': 3,
    'python_minor': 10,
    'tested_python': '3.11',
    'tested_node_major': 22,
    'tested_openclaw': '2026.3.11',
}


def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
    except Exception as e:
        return False, str(e)
    text = (proc.stdout or proc.stderr or '').strip()
    return proc.returncode == 0, text


def status(name: str, level: str, detail: str) -> dict:
    return {'name': name, 'level': level, 'detail': detail}


def main() -> int:
    parser = argparse.ArgumentParser(description='Compatibility doctor for openai-auth-switcher-public')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    results: list[dict] = []

    py_ok = sys.version_info >= (RECOMMENDED['python_major'], RECOMMENDED['python_minor'])
    results.append(status(
        'python',
        'OK' if py_ok else 'FAIL',
        f"running={platform.python_version()} recommended>={RECOMMENDED['python_major']}.{RECOMMENDED['python_minor']} tested={RECOMMENDED['tested_python']}"
    ))

    node_ok, node_text = run_cmd(['node', '--version'])
    results.append(status(
        'node',
        'OK' if node_ok else 'WARN',
        node_text or 'node not found; acceptable if web/OAuth helper flows are not used'
    ))

    oc_ok, oc_text = run_cmd(['openclaw', 'status'])
    results.append(status(
        'openclaw-cli',
        'OK' if oc_ok else 'WARN',
        'openclaw status succeeded' if oc_ok else (oc_text or 'openclaw command unavailable')
    ))

    runtime = detect_runtime()
    root_ok = bool(runtime.get('openclaw_root'))
    workspace_ok = bool(runtime.get('workspace'))
    agent_ok = bool(runtime.get('agent_root'))
    auth_ok = bool(runtime.get('auth_profiles_exists'))

    results.append(status('runtime-openclaw-root', 'OK' if root_ok else 'FAIL', str(runtime.get('openclaw_root'))))
    results.append(status('runtime-workspace', 'OK' if workspace_ok else 'FAIL', str(runtime.get('workspace'))))
    results.append(status('runtime-agent-root', 'OK' if agent_ok else 'FAIL', str(runtime.get('agent_root'))))
    results.append(status('auth-profiles', 'OK' if auth_ok else 'FAIL', str(runtime.get('auth_profiles_path'))))

    linux_ok = platform.system().lower() == 'linux'
    results.append(status('os', 'OK' if linux_ok else 'WARN', platform.platform()))

    skill_root = Path(__file__).resolve().parent.parent
    state_base_dir = get_state_base_dir()
    results.append(status('public-state-base-dir', 'OK', str(state_base_dir)))
    dangerous = []
    caches = []
    forbidden_patterns = [
        'auth-profile.json',
        'callback.txt',
        'result.json',
    ]
    for p in skill_root.rglob('*'):
        if not p.is_file():
            continue
        if '__pycache__' in p.parts:
            caches.append(str(p.relative_to(skill_root)))
            continue
        if any(p.name == bad for bad in forbidden_patterns):
            dangerous.append(str(p.relative_to(skill_root)))
    if dangerous:
        results.append(status('public-tree-sanitization', 'FAIL', f'forbidden files present: {dangerous[:10]}'))
    elif caches:
        results.append(status('public-tree-sanitization', 'WARN', f'bytecode cache present but package wrapper excludes it: {caches[:10]}'))
    else:
        results.append(status('public-tree-sanitization', 'OK', 'no obvious forbidden runtime files in public tree'))

    overall_ok = not any(item['level'] == 'FAIL' for item in results)
    payload = {
        'ok': overall_ok,
        'tested_openclaw': RECOMMENDED['tested_openclaw'],
        'results': results,
        'runtime': runtime,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print('openai-auth-switcher-public doctor')
        for item in results:
            print(f"[{item['level']}] {item['name']}: {item['detail']}")
    return 0 if overall_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
