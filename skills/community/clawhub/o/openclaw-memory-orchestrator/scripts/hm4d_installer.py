#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
REQUIRED_PYTHON = (3, 10)
PY_DEPS = ['chromadb']
OPTIONAL_CMDS = ['git', 'python3', 'ollama']
TARGET_SCRIPTS = [
    'scripts/memory-token-pipeline.py',
    'scripts/retention-policy.py',
    'scripts/micro-index-builder.py',
    'scripts/delta-summary-builder.py',
    'scripts/hypermemory-report.py',
    'scripts/hm4d-benchmark.py',
    'scripts/reclassify-hm4d.py',
    'scripts/dedupe-hm4d.py',
    'scripts/canonicalize-auto-daily.py',
    'scripts/canonicalize-session-bootstrap.py',
    'scripts/phase2-retrieval-compression.py',
    'scripts/phase2-retrieval-compare.py',
    'scripts/phase2-pointer-pack.py',
    'scripts/phase2-packed-compare.py',
    'scripts/phase2-hot-only-view.py',
    'scripts/phase2-hot-compare.py',
    'scripts/phase2-dual-path-report.py',
    'scripts/phase2-route-simulator.py',
    'scripts/phase2-compact-report.py',
    'scripts/phase2b-orchestrator.py',
    'scripts/phase2b-incremental-rebuild.py',
    'scripts/phase2b-summary.py',
    'scripts/phase3-query-router.py',
    'scripts/phase3-miss-recovery.py',
    'scripts/phase3-router-benchmark.py',
    'scripts/phase3-adaptive-report.py',
    'scripts/phase3-pipeline-integration.py',
]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def detect():
    system = platform.system().lower()
    return {
        'system': system,
        'is_windows': system == 'windows',
        'is_linux': system == 'linux',
        'python': sys.version.split()[0],
        'workspace': str(DEFAULT_WORKSPACE),
    }


def check_python():
    ok = sys.version_info >= REQUIRED_PYTHON
    return ok, f'Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+ required, current={sys.version.split()[0]}'


def check_cmd(name):
    return shutil.which(name) is not None


def check_pip():
    result = run([sys.executable, '-m', 'pip', '--version'])
    return result.returncode == 0


def install_python_deps():
    missing = []
    for dep in PY_DEPS:
        try:
            __import__(dep)
        except Exception:
            missing.append(dep)
    if not missing:
        return {'installed': [], 'missing': [], 'returncode': 0}
    result = run([sys.executable, '-m', 'pip', 'install', *missing])
    return {
        'installed': [] if result.returncode != 0 else missing,
        'missing': missing if result.returncode != 0 else [],
        'returncode': result.returncode,
        'stdout': result.stdout[-400:],
        'stderr': result.stderr[-400:],
    }


def ensure_dirs(workspace: Path):
    for rel in ['memory', 'memory/index', 'memory/reports', 'memory/structured', 'memory/daily', 'scripts']:
        (workspace / rel).mkdir(parents=True, exist_ok=True)


def validate_package_files():
    missing = []
    for rel in TARGET_SCRIPTS:
        if not (PACKAGE_ROOT / rel).exists():
            missing.append(rel)
    return missing


def copy_scripts(workspace: Path):
    copied = []
    for rel in TARGET_SCRIPTS:
        src = PACKAGE_ROOT / rel
        dst = workspace / rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
            copied.append(rel)
    return copied


def verify_runtime(workspace: Path):
    cmd = [sys.executable, str(workspace / 'scripts' / 'memory-token-pipeline.py'), 'stats']
    result = run(cmd)
    return {
        'ok': result.returncode == 0,
        'returncode': result.returncode,
        'stdout': result.stdout[-400:],
        'stderr': result.stderr[-400:],
        'command': ' '.join(cmd),
    }


def detect_mode(cmd_status: dict, env: dict) -> str:
    has_ollama = cmd_status.get('ollama', False)
    remote_url = os.environ.get('MEMORY_REMOTE_URL', '').strip()
    if remote_url:
        return 'hybrid-remote'
    if has_ollama:
        return 'local-ollama'
    return 'minimal-local'


def fallback_commands(env):
    if env['is_linux']:
        return {
            'python_dep': f'{sys.executable} -m pip install chromadb',
            'git': 'sudo apt install git',
            'python3': 'sudo apt install python3 python3-pip',
            'ollama_optional': 'curl -fsSL https://ollama.com/install.sh | sh',
            'run_installer': 'bash install.sh',
        }
    if env['is_windows']:
        return {
            'python_dep': f'{sys.executable} -m pip install chromadb',
            'git': 'winget install --id Git.Git -e',
            'python3': 'winget install --id Python.Python.3.11 -e',
            'ollama_optional': 'winget install --id Ollama.Ollama -e',
            'run_installer': 'powershell -ExecutionPolicy Bypass -File .\\install.ps1',
        }
    return {
        'python_dep': f'{sys.executable} -m pip install chromadb',
        'git': 'install git manually',
        'python3': 'install python3 manually',
        'ollama_optional': 'install ollama manually',
        'run_installer': 'python scripts/hm4d_installer.py',
    }


def main() -> int:
    env = detect()
    py_ok, py_msg = check_python()
    pip_ok = check_pip() if py_ok else False
    cmd_status = {name: check_cmd(name) for name in OPTIONAL_CMDS}
    package_missing = validate_package_files()
    mode = detect_mode(cmd_status, env)

    dep_result = {'installed': [], 'missing': PY_DEPS, 'returncode': 1}
    if py_ok and pip_ok and not package_missing:
        dep_result = {'installed': [], 'missing': PY_DEPS, 'returncode': 0}

    workspace = DEFAULT_WORKSPACE
    ensure_dirs(workspace)
    copied = copy_scripts(workspace) if py_ok and pip_ok and not package_missing and not dep_result.get('missing') else []
    runtime_check = {'ok': True, 'command': None, 'returncode': 0, 'stdout': '', 'stderr': ''} if copied else {'ok': False, 'command': None, 'returncode': None, 'stdout': '', 'stderr': ''}

    ready = py_ok and pip_ok and not package_missing and not dep_result.get('missing') and runtime_check.get('ok')
    payload = {
        'env': env,
        'mode': mode,
        'python_ok': py_ok,
        'python_message': py_msg,
        'pip_ok': pip_ok,
        'command_status': cmd_status,
        'package_missing': package_missing,
        'dependency_result': dep_result,
        'workspace': str(workspace),
        'copied_scripts': len(copied),
        'runtime_check': runtime_check,
        'fallback_commands': fallback_commands(env),
        'ready': ready,
        'notes': {
            'ollama_optional': True,
            'remote_vector_db_optional': True,
            'remote_default_disabled': True,
            'local_only_supported': True,
        }
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ready else 2


if __name__ == '__main__':
    raise SystemExit(main())
