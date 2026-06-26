#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_FILE = Path(os.environ.get('MANUS_CONFIG_FILE', str(Path.home() / '.config' / 'manus-openclaw-bridge' / 'manus.env')))
OUT_DIR = SKILL_DIR / 'tmp' / 'manus'
OUT_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_DOWNLOAD_HOSTS = {
    'api.manus.ai',
    'manus.ai',
    'open.manus.im',
    'cdn.manus.ai',
    'files.manus.ai',
}


def load_env() -> None:
    if not CONFIG_FILE.exists():
        return
    for line in CONFIG_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def get_api_base() -> str:
    api_base = os.environ.get('MANUS_API_BASE', '').rstrip('/')
    if not api_base:
        raise SystemExit(f'MANUS_API_BASE is not set. Put it in {CONFIG_FILE}')
    parsed = urlparse(api_base)
    if parsed.scheme.lower() != 'https':
        raise SystemExit('MANUS_API_BASE must use https://')
    host = (parsed.hostname or '').lower()
    if host not in {'api.manus.ai', 'open.manus.im'} and not host.endswith('.manus.ai'):
        raise SystemExit(f'MANUS_API_BASE host is not allowlisted: {host}')
    return api_base


def api_get(task_id: str):
    key = os.environ.get('MANUS_API_KEY')
    if not key:
        raise SystemExit(f'MANUS_API_KEY is not set. Put it in {CONFIG_FILE}')
    api_base = get_api_base()
    req = urllib.request.Request(
        f'{api_base}/v1/tasks/{task_id}',
        headers={'accept': 'application/json', 'API_KEY': key},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8'))


def collect_files(task: dict):
    files = []
    for msg in task.get('output', []) or []:
        for item in msg.get('content', []) or []:
            file_url = item.get('fileUrl') or item.get('file_url')
            if not file_url:
                continue
            files.append(
                {
                    'url': file_url,
                    'name': item.get('fileName') or item.get('file_name') or 'output.bin',
                    'mime': item.get('mimeType') or item.get('mime_type') or '',
                    'type': item.get('type') or '',
                    'role': msg.get('role') or '',
                }
            )
    return files


def safe_name(name: str):
    keep = []
    for ch in name:
        if ch.isalnum() or ch in '._-':
            keep.append(ch)
        else:
            keep.append('_')
    return ''.join(keep) or 'output.bin'


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme.lower() != 'https':
        raise ValueError('refusing non-HTTPS URL')
    host = (parsed.hostname or '').lower()
    if not host:
        raise ValueError('URL is missing a hostname')
    if host not in ALLOWED_DOWNLOAD_HOSTS and not host.endswith('.manus.ai'):
        raise ValueError(f'refusing URL from untrusted host: {host}')


def download(url: str, path: Path):
    validate_url(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'manus-openclaw-bridge/1.0'})
    with urllib.request.urlopen(req, timeout=120) as resp:
        final_url = resp.geturl()
        validate_url(final_url)
        data = resp.read()
    path.write_bytes(data)
    return path


def main():
    load_env()
    if len(sys.argv) < 2:
        raise SystemExit('Usage: manus_wait_and_collect.py <task_id> [timeout_seconds]')
    task_id = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 900
    start = time.time()
    last_status = None

    while True:
        task = api_get(task_id)
        status = task.get('status', 'unknown')
        if status != last_status:
            print(f'[manus] status={status}', file=sys.stderr)
            last_status = status
        if status in ('completed', 'error', 'pending'):
            break
        if time.time() - start > timeout:
            raise SystemExit(f'timeout waiting for task {task_id}, last status={status}')
        time.sleep(5)

    files = collect_files(task)
    downloaded = []
    for index, file_info in enumerate(files, 1):
        name = safe_name(file_info['name'])
        target = OUT_DIR / f'{task_id}_{index}_{name}'
        try:
            download(file_info['url'], target)
            downloaded.append({**file_info, 'saved_path': str(target)})
        except Exception as exc:
            downloaded.append({**file_info, 'download_error': str(exc)})

    result = {
        'task_id': task_id,
        'status': task.get('status'),
        'task_title': (task.get('metadata') or {}).get('task_title') or task.get('task_title'),
        'task_url': (task.get('metadata') or {}).get('task_url') or task.get('task_url'),
        'files': downloaded,
        'raw': task,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
