#!/usr/bin/env python3
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DATE = datetime.now().strftime('%Y-%m-%d')
RETRY_SCRIPT = ROOT / 'scripts' / 'send_telegram_retry.sh'
TARGET = os.environ.get('TELEGRAM_TARGET', 'telegram:<target-chat-id>')
DEADLINE_SECONDS = int(os.environ.get('HTML_RETRY_WINDOW_SECONDS', str(30 * 60)))
SLEEP_BETWEEN_ROUNDS = int(os.environ.get('HTML_RETRY_INTERVAL_SECONDS', '20'))

HTML_PARTS = [
    ROOT / 'output' / 'readable' / f'paper_report_readable_{DATE}.part1.html',
    ROOT / 'output' / 'readable' / f'paper_report_readable_{DATE}.part2.html',
]
HTML_MESSAGES = [
    'Readable HTML report part 1.',
    'Readable HTML report part 2.',
]
TELEGRAM_JSON = ROOT / 'output' / 'telegram' / f'telegram_messages_{DATE}.json'


def send(target, message, media=None):
    cmd = [str(RETRY_SCRIPT), target, message]
    if media:
        cmd.append(str(media))
    return subprocess.run(cmd, text=True, capture_output=True)


def send_messages_fallback():
    data = json.loads(TELEGRAM_JSON.read_text())
    results = []
    for idx, msg in enumerate(data.get('messages', []), start=1):
        proc = send(TARGET, msg)
        results.append({'index': idx, 'ok': proc.returncode == 0, 'stdout': proc.stdout, 'stderr': proc.stderr})
        if proc.returncode != 0:
            return {'ok': False, 'mode': 'telegram-messages', 'results': results}
    return {'ok': True, 'mode': 'telegram-messages', 'results': results}


def main():
    start = time.time()
    success = [False, False]
    rounds = []

    while time.time() - start < DEADLINE_SECONDS:
        round_result = {'at': time.time(), 'parts': []}
        for idx, part in enumerate(HTML_PARTS):
            if success[idx]:
                round_result['parts'].append({'index': idx + 1, 'skipped': True})
                continue
            proc = send(TARGET, HTML_MESSAGES[idx], part)
            ok = proc.returncode == 0
            success[idx] = ok or success[idx]
            round_result['parts'].append({'index': idx + 1, 'ok': ok, 'stdout': proc.stdout, 'stderr': proc.stderr})
        rounds.append(round_result)
        if all(success):
            print(json.dumps({'ok': True, 'mode': 'html', 'rounds': rounds}, ensure_ascii=False, indent=2))
            return
        time.sleep(SLEEP_BETWEEN_ROUNDS)

    fallback = send_messages_fallback()
    print(json.dumps({'ok': fallback.get('ok', False), 'mode': 'fallback-after-html-timeout', 'htmlRounds': rounds, 'fallback': fallback}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if fallback.get('ok', False) else 1)


if __name__ == '__main__':
    main()
