#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

BASE = Path('/root/.openclaw/workspace/skills/webtop-galim/scripts')
GALIM = BASE / 'galim_fetch_tasks.py'
OFEK = BASE / 'fetch_tasks.py'
WEBTOP = BASE / 'webtop_fetch_summary.py'


def run_json(script: Path, extra_args=None):
    cmd = [sys.executable, str(script), '--json']
    if extra_args:
        cmd.extend(extra_args)
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=240,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f'failed: {script.name}')
    return json.loads(proc.stdout)


def format_unified(galim_data, ofek_data=None, webtop_data=None, limit=5):
    lines = ['📚 *דוח משימות מאוחד - גלים / אופק / וובטופ*', '']

    by_child = {}

    for item in galim_data or []:
        by_child.setdefault(item['child_name'], {})['galim'] = item

    for item in ofek_data or []:
        by_child.setdefault(item['child_name'], {})['ofek'] = item

    for child_name in sorted(by_child.keys()):
        lines.append(f'👤 *{child_name}*')
        child = by_child[child_name]

        galim = child.get('galim')
        if galim:
            if galim.get('success'):
                lines.append(f"גלים: {galim.get('task_count', 0)} משימות")
                for task in (galim.get('tasks') or [])[:limit]:
                    lines.append(f"- {task['title']}")
                    lines.append(f"  {task['subject']} | {task['task_type']} | {task['due_at']}")
                extra = max(0, len(galim.get('tasks') or []) - limit)
                if extra:
                    lines.append(f'  ... ועוד {extra} משימות בגלים')
            else:
                lines.append(f"גלים: שגיאה - {galim.get('error', 'לא ידוע')}")
        else:
            lines.append('גלים: אין נתונים')

        ofek = child.get('ofek')
        if ofek:
            if ofek.get('error'):
                lines.append(f"אופק: שגיאה - {ofek['error']}")
            else:
                lines.append(
                    'אופק: '
                    f"פתוחות {ofek.get('open_count', '?')}, "
                    f"לתיקון {ofek.get('fix_count', '?')}, "
                    f"ממתינות {ofek.get('waiting_count', '?')}, "
                    f"נבדקו {ofek.get('checked_count', '?')}"
                )
        else:
            lines.append('אופק: עדיין לא מוגדר / לא נבדק')

        lines.append('')

    if webtop_data:
        lines.append('📝 *וובטופ*')
        if webtop_data.get('success'):
            raw = (webtop_data.get('raw_text') or '').strip()
            if raw:
                lines.append(raw)
            else:
                lines.append('אין פלט מוובטופ')
        else:
            lines.append(f"שגיאה בוובטופ: {webtop_data.get('error') or 'לא ידוע'}")
        lines.append('')

    return '\n'.join(lines).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=5)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--hide-overdue', action='store_true')
    ap.add_argument('--due-within-days', type=int)
    args = ap.parse_args()

    extra_args = []
    if args.hide_overdue:
        extra_args.append('--hide-overdue')
    if args.due_within_days is not None:
        extra_args.extend(['--due-within-days', str(args.due_within_days)])

    galim_data = run_json(GALIM, extra_args=extra_args)

    ofek_data = None
    if os.getenv('OFEK_KIDS_JSON'):
        try:
            ofek_data = run_json(OFEK)
        except Exception as e:
            ofek_data = [{
                'child_name': 'כללי',
                'error': str(e),
                'open_count': None,
                'fix_count': None,
                'waiting_count': None,
                'checked_count': None,
            }]

    webtop_data = None
    try:
        webtop_data = run_json(WEBTOP)
    except Exception as e:
        webtop_data = {'success': False, 'error': str(e), 'raw_text': ''}

    if args.json:
        print(json.dumps({'galim': galim_data, 'ofek': ofek_data, 'webtop': webtop_data}, ensure_ascii=False, indent=2))
    else:
        print(format_unified(galim_data, ofek_data=ofek_data, webtop_data=webtop_data, limit=args.limit))


if __name__ == '__main__':
    main()
