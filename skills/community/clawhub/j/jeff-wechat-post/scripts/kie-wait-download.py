#!/usr/bin/env python3
import glob
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

CALLBACK_DIR = Path(os.environ.get('KIE_CALLBACK_DIR', '/root/.openclaw/workspace/temp/kie-callback'))


def find_task(task_id: str):
    files = sorted(glob.glob(str(CALLBACK_DIR / '*.summary.json')), key=os.path.getmtime, reverse=True)
    for f in files:
        try:
            obj = json.load(open(f, 'r', encoding='utf-8'))
            data = obj.get('body', {}).get('data', {})
            if data.get('taskId') == task_id:
                return obj
        except Exception:
            continue
    return None


def download_url(url: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, output_path)
        return
    except Exception:
        pass
    subprocess.run(['curl', '-L', url, '-o', str(output_path)], check=True)


def main():
    if len(sys.argv) < 3:
        print('Usage: kie-wait-download.py <task_id> <output_path> [timeout_seconds]', file=sys.stderr)
        sys.exit(2)
    task_id = sys.argv[1]
    output_path = Path(sys.argv[2])
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 180
    deadline = time.time() + timeout

    while time.time() < deadline:
        obj = find_task(task_id)
        if obj:
            data = obj.get('body', {}).get('data', {})
            state = data.get('state')
            if state == 'success':
                result = json.loads(data['resultJson'])
                url = result['resultUrls'][0]
                download_url(url, output_path)
                print(json.dumps({'taskId': task_id, 'state': state, 'url': url, 'output': str(output_path)}))
                return
            if state in ('failed', 'error'):
                print(json.dumps({'taskId': task_id, 'state': state, 'failCode': data.get('failCode'), 'failMsg': data.get('failMsg')}))
                sys.exit(1)
        time.sleep(3)
    print(json.dumps({'taskId': task_id, 'state': 'timeout', 'timeoutSeconds': timeout}))
    sys.exit(1)


if __name__ == '__main__':
    main()
