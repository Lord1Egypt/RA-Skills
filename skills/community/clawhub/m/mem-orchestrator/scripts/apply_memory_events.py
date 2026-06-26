#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from lib_memory import yaml, dump_yaml_fallback, load_yaml_file

ROOT = os.environ.get('MEMORY_ROOT', os.path.join(os.getcwd(), 'memory'))
SESSION_PATH = os.path.join(ROOT, 'session-state.yaml')
DAILY_DIR = os.path.join(ROOT, 'daily')
OBJECTS_DIR = os.path.join(ROOT, 'objects')
PREFERENCES_DIR = os.path.join(OBJECTS_DIR, 'preferences')
DECISIONS_DIR = os.path.join(OBJECTS_DIR, 'decisions')


def ensure_dirs():
    os.makedirs(ROOT, exist_ok=True)
    os.makedirs(DAILY_DIR, exist_ok=True)
    os.makedirs(PREFERENCES_DIR, exist_ok=True)
    os.makedirs(DECISIONS_DIR, exist_ok=True)


def load_session():
    if not os.path.exists(SESSION_PATH):
        return {'session_id': 'auto', 'active_domains': [], 'active_objects': [], 'current_goal': '', 'recent_constraints': [], 'last_updated': ''}
    return load_yaml_file(SESSION_PATH) or {'session_id': 'auto', 'active_domains': [], 'active_objects': [], 'current_goal': '', 'recent_constraints': [], 'last_updated': ''}


def save_session(data):
    with open(SESSION_PATH, 'w', encoding='utf-8') as f:
        if yaml is None:
            f.write(dump_yaml_fallback(data))
        else:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def append_daily(events):
    day = datetime.now().astimezone().strftime('%Y-%m-%d')
    path = os.path.join(DAILY_DIR, f'{day}.md')
    with open(path, 'a', encoding='utf-8') as f:
        if os.path.getsize(path) == 0:
            f.write(f'# {day}\n\n')
        for ev in events:
            f.write('## Event\n')
            f.write(f"- 时间：{ev.get('timestamp','')}\n")
            f.write(f"- 类型：{ev.get('event_type','')}\n")
            f.write(f"- 主题：{', '.join(ev.get('domains', []))}\n")
            f.write(f"- 内容：{ev.get('text','')}\n\n")


def upsert_object(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        if yaml is None:
            f.write(dump_yaml_fallback(data))
        else:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def slugify(text):
    cleaned = ''.join(ch.lower() if ch.isalnum() else '-' for ch in text)
    while '--' in cleaned:
        cleaned = cleaned.replace('--', '-')
    return cleaned.strip('-') or 'memory-item'


def materialize_durable_objects(events):
    now = datetime.now().astimezone().isoformat(timespec='seconds')
    day = datetime.now().date().isoformat()
    created = []
    for ev in events:
        text = ev.get('text', '').strip()
        if not text:
            continue
        if ev.get('event_type') == 'preference_update':
            slug = slugify(text[:40])
            path = os.path.join(PREFERENCES_DIR, f'{slug}.yaml')
            if not os.path.exists(path):
                blob = {
                    'id': f'preference/{slug}',
                    'type': 'preference',
                    'domain': (ev.get('domains') or ['meta'])[0],
                    'title': text[:24],
                    'summary': text,
                    'why_it_matters': 'Auto-captured from user preference update during conversation.',
                    'tags': ['auto-captured'],
                    'status': 'discussed',
                    'confidence': 'medium',
                    'last_discussed': day,
                    'relations': {},
                    'user_takeaways': [text],
                    'created_at': now,
                    'updated_at': now,
                }
                upsert_object(path, blob)
                created.append(path)
        elif ev.get('event_type') == 'decision_made':
            slug = slugify(text[:40])
            path = os.path.join(DECISIONS_DIR, f'{slug}.yaml')
            if not os.path.exists(path):
                blob = {
                    'id': f'decision/{slug}',
                    'type': 'decision',
                    'domain': (ev.get('domains') or ['meta'])[0],
                    'title': text[:24],
                    'summary': text,
                    'why_it_matters': 'Auto-captured from an explicit decision in conversation.',
                    'tags': ['auto-captured'],
                    'status': 'discussed',
                    'confidence': 'medium',
                    'last_discussed': day,
                    'relations': {},
                    'user_takeaways': [text],
                    'created_at': now,
                    'updated_at': now,
                }
                upsert_object(path, blob)
                created.append(path)
    return created


def main():
    ensure_dirs()
    payload = json.load(sys.stdin)
    events = payload.get('events', [])
    session = load_session()
    active = set(session.get('active_domains', []) or [])
    for ev in events:
        for d in ev.get('domains', []):
            active.add(d)
    session['active_domains'] = sorted(active)
    session['last_updated'] = datetime.now().astimezone().isoformat(timespec='seconds')
    save_session(session)
    append_daily(events)
    created = materialize_durable_objects(events)
    print(json.dumps({'ok': True, 'applied': len(events), 'session_path': SESSION_PATH, 'created_objects': created}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
