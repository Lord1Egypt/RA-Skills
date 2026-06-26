#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

GALIM_SCRIPT = Path('/root/.openclaw/workspace/skills/webtop-galim/scripts/galim_fetch_tasks.py')
SA_FILE = Path(os.getenv('GOOGLE_SA_FILE', '/root/.openclaw/workspace/.secrets/google-sa.json'))
DEFAULT_CALENDAR_ID = os.getenv('OFEK_GALIM_CALENDAR_ID', 'primary')
TZ = 'Asia/Jerusalem'
DATE_FMT = '%d/%m/%y | %H:%M'
BASE = 'https://www.googleapis.com/calendar/v3'


def run_galim_json(days: int):
    proc = subprocess.run(
        [sys.executable, str(GALIM_SCRIPT), '--json', '--hide-overdue', '--due-within-days', str(days)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def parse_due(due_at: str):
    return datetime.strptime(due_at, DATE_FMT)


def get_session():
    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=['https://www.googleapis.com/auth/calendar']
    )
    return AuthorizedSession(creds)


def gget(session, path, params=None):
    url = f'{BASE}{path}'
    if params:
        url += '?' + urlencode(params, doseq=True)
    r = session.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


def gpost(session, path, body):
    r = session.post(f'{BASE}{path}', json=body, timeout=60)
    r.raise_for_status()
    return r.json()


def list_existing(session, calendar_id, time_min, time_max):
    items = []
    page_token = None
    while True:
        params = {
            'timeMin': time_min,
            'timeMax': time_max,
            'singleEvents': 'true',
            'maxResults': 250,
            'privateExtendedProperty': 'source=webtop-galim',
        }
        if page_token:
            params['pageToken'] = page_token
        resp = gget(session, f'/calendars/{calendar_id}/events', params=params)
        items.extend(resp.get('items', []))
        page_token = resp.get('nextPageToken')
        if not page_token:
            break
    return items


def build_key(child_name, title, due_at):
    return f'{child_name}|{title}|{due_at}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--calendar-id', default=DEFAULT_CALENDAR_ID)
    ap.add_argument('--days', type=int, default=30)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    galim = run_galim_json(args.days)
    session = get_session()
    now = datetime.utcnow().isoformat() + 'Z'
    future = (datetime.utcnow() + timedelta(days=args.days + 2)).isoformat() + 'Z'
    existing = list_existing(session, args.calendar_id, now, future)
    existing_keys = {
        ((e.get('extendedProperties') or {}).get('private') or {}).get('ofekGalimKey')
        for e in existing
    }

    created = []
    skipped = []
    for child in galim:
        if not child.get('success'):
            continue
        for task in child.get('tasks', []):
            due = parse_due(task['due_at'])
            key = build_key(child['child_name'], task['title'], task['due_at'])
            if key in existing_keys:
                skipped.append(key)
                continue
            end = due + timedelta(hours=1)
            body = {
                'summary': f"[גלים] {child['child_name']} - {task['title']}",
                'description': (
                    f"ילד/ה: {child['child_name']}\n"
                    f"מקצוע: {task['subject']}\n"
                    f"סוג: {task['task_type']}\n"
                    f"מקור: גלים\n"
                    f"מועד הגשה: {task['due_at']}"
                ),
                'start': {'dateTime': due.isoformat(), 'timeZone': TZ},
                'end': {'dateTime': end.isoformat(), 'timeZone': TZ},
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 180},
                    ],
                },
                'extendedProperties': {
                    'private': {
                        'source': 'webtop-galim',
                        'ofekGalimKey': key,
                        'childName': child['child_name'],
                    }
                },
            }
            if args.dry_run:
                created.append({'summary': body['summary'], 'due': task['due_at']})
            else:
                event = gpost(session, f'/calendars/{args.calendar_id}/events', body)
                created.append({'summary': body['summary'], 'id': event.get('id'), 'due': task['due_at']})

    print(json.dumps({'created': created, 'skipped': len(skipped), 'calendarId': args.calendar_id}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
