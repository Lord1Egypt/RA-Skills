#!/usr/bin/env python3
import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from playwright.sync_api import sync_playwright

LOGIN_URL = "https://userdata.galim.org.il/login_idm?request_uri=https%3A%2F%2Fpro.galim.org.il%2F%3Flang%3Dhe"
TASKS_URL = "https://lms.galim.org.il/personal?lang=he"
DEFAULT_ENV_PATH = Path('/root/.openclaw/workspace/.env/webtop-galim.env')
LEGACY_ENV_PATH = Path('/root/.openclaw/workspace/.env/galim.env')
DATE_RE = re.compile(r'^\d{2}/\d{2}/\d{2} \| \d{2}:\d{2}$')
DATE_FMT = '%d/%m/%y | %H:%M'


@dataclass
class GalimTask:
    assigned_at: str
    title: str
    task_type: str
    subject: str
    due_at: str
    overdue: bool = False


@dataclass
class GalimChildResult:
    child_name: str
    success: bool
    task_count: int = 0
    tasks: List[GalimTask] = None
    error: Optional[str] = None


def load_env(path: Path) -> dict:
    env = {}
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def choose_env_path() -> Path:
    override = Path(__import__('os').environ['WEBTOP_GALIM_ENV']) if 'WEBTOP_GALIM_ENV' in __import__('os').environ else None
    if override and override.exists():
        return override
    if DEFAULT_ENV_PATH.exists():
        env = load_env(DEFAULT_ENV_PATH)
        if any(env.get(k) for k in ('GALIM_USERNAME_CHILD1', 'GALIM_USERNAME_CHILD2')):
            return DEFAULT_ENV_PATH
    return LEGACY_ENV_PATH


def load_creds() -> List[tuple]:
    env = load_env(choose_env_path())

    if env.get('GALIM_USERNAME_CHILD1') and env.get('GALIM_PASSWORD_CHILD1'):
        return [
            (env.get('GALIM_NAME_CHILD1', 'Child 1').strip('"'), env['GALIM_USERNAME_CHILD1'], env['GALIM_PASSWORD_CHILD1']),
            (env.get('GALIM_NAME_CHILD2', 'Child 2').strip('"'), env['GALIM_USERNAME_CHILD2'], env['GALIM_PASSWORD_CHILD2']),
        ]

    if env.get('GALIM_USERNAME_YUVAL') and env.get('GALIM_PASSWORD_YUVAL'):
        return [
            (env.get('GALIM_NAME_YUVAL', 'Child 1').strip('"'), env['GALIM_USERNAME_YUVAL'], env['GALIM_PASSWORD_YUVAL']),
            (env.get('GALIM_NAME_SHIRA', 'Child 2').strip('"'), env['GALIM_USERNAME_SHIRA'], env['GALIM_PASSWORD_SHIRA']),
        ]

    raise RuntimeError('Missing Galim credentials in webtop-galim.env or legacy galim.env')


def parse_dt(s: str) -> Optional[datetime]:
    try:
        return datetime.strptime(s, DATE_FMT)
    except Exception:
        return None


def parse_tasks_from_text(text: str) -> List[GalimTask]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    try:
        start = lines.index('תאריך הגשה') + 1
    except ValueError:
        return []

    tasks = []
    i = start
    while i + 4 < len(lines):
        if not DATE_RE.match(lines[i]):
            i += 1
            continue
        assigned_at = lines[i]
        title = lines[i + 1]
        task_type = lines[i + 2]
        subject = lines[i + 3]
        due_at = lines[i + 4]
        if not DATE_RE.match(due_at):
            i += 1
            continue
        due_dt = parse_dt(due_at)
        tasks.append(GalimTask(
            assigned_at=assigned_at,
            title=title,
            task_type=task_type,
            subject=subject,
            due_at=due_at,
            overdue=bool(due_dt and due_dt < datetime.utcnow()),
        ))
        i += 5
    return tasks


def filter_tasks(tasks: List[GalimTask], hide_overdue: bool = False, due_within_days: Optional[int] = None) -> List[GalimTask]:
    now = datetime.utcnow()
    out = []
    for task in tasks:
        due_dt = parse_dt(task.due_at)
        if hide_overdue and task.overdue:
            continue
        if due_within_days is not None and due_dt is not None:
            if due_dt > now + timedelta(days=due_within_days):
                continue
        out.append(task)
    return out


def fetch_for_child(name: str, username: str, password: str, hide_overdue: bool = False, due_within_days: Optional[int] = None) -> GalimChildResult:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(LOGIN_URL, wait_until='networkidle', timeout=60000)
            page.locator('#userName').fill(username)
            page.locator('#password').evaluate("el => el.removeAttribute('readonly')")
            page.locator('#password').fill(password)
            page.get_by_role('button', name='כניסה', exact=True).click()
            page.wait_for_timeout(8000)
            page.goto(TASKS_URL, wait_until='networkidle', timeout=60000)
            text = page.locator('body').inner_text(timeout=30000)
            tasks = parse_tasks_from_text(text)
            tasks = filter_tasks(tasks, hide_overdue=hide_overdue, due_within_days=due_within_days)
            return GalimChildResult(child_name=name, success=True, task_count=len(tasks), tasks=tasks)
        except Exception as e:
            return GalimChildResult(child_name=name, success=False, error=str(e), tasks=[])
        finally:
            browser.close()


def format_hebrew(results: List[GalimChildResult], limit: int = 5) -> str:
    lines = ['📚 *משימות גלים*', '']
    for res in results:
        lines.append(f"👤 *{res.child_name}*")
        if not res.success:
            lines.append(f"❌ שגיאה: {res.error}")
            lines.append('')
            continue
        lines.append(f"סה״כ משימות רלוונטיות: {res.task_count}")
        if not res.tasks:
            lines.append('אין משימות רלוונטיות כרגע ✅')
            lines.append('')
            continue
        for task in res.tasks[:limit]:
            overdue = ' ⚠️ באיחור' if task.overdue else ''
            lines.append(f"- {task.title}{overdue}")
            lines.append(f"  {task.subject} | {task.task_type}")
            lines.append(f"  להגשה: {task.due_at}")
        if len(res.tasks) > limit:
            lines.append(f"  ... ועוד {len(res.tasks) - limit} משימות")
        lines.append('')
    return '\n'.join(lines).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--limit', type=int, default=5)
    ap.add_argument('--hide-overdue', action='store_true')
    ap.add_argument('--due-within-days', type=int)
    args = ap.parse_args()

    results = [
        fetch_for_child(name, username, password, hide_overdue=args.hide_overdue, due_within_days=args.due_within_days)
        for name, username, password in load_creds()
    ]
    if args.json:
        print(json.dumps([asdict(r) for r in results], ensure_ascii=False, indent=2))
    else:
        print(format_hebrew(results, limit=args.limit))


if __name__ == '__main__':
    main()
