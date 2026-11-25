"""Dependency-free task memory. AI-assisted extraction from the custom A3 task tool."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import uuid


def execute(action, value, directory):
    if action not in ('add','list','done'):
        raise ValueError('action_not_allowed')
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = directory/'tasks.sqlite'
    connection = sqlite3.connect(path, timeout=5)
    path.chmod(0o600)
    try:
        connection.execute('CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL)')
        if action == 'add':
            if not isinstance(value, str) or not value.strip() or len(value) > 250:
                raise ValueError('title_required_max_250_characters')
            if connection.execute('SELECT COUNT(*) FROM tasks').fetchone()[0] >= 500:
                raise ValueError('task_capacity_reached')
            connection.execute('INSERT INTO tasks VALUES (?,?,?,?)',
                               (uuid.uuid4().hex[:12],value.strip(),'open',datetime.now(timezone.utc).isoformat()))
        elif action == 'done':
            if not isinstance(value, str) or not re.fullmatch('[a-f0-9]{12}',value):
                raise ValueError('invalid_task_id')
            if connection.execute('UPDATE tasks SET status=? WHERE id=?',('done',value)).rowcount != 1:
                raise ValueError('task_not_found')
        connection.commit()
        rows = connection.execute('SELECT id,title,status,created FROM tasks ORDER BY created DESC LIMIT 30').fetchall()
        return {'tasks':[dict(zip(('id','title','status','created'),row)) for row in rows],
                'view_limit':30,'scheduled_reminders':False}
    finally:
        connection.close()


if __name__ == '__main__':
    os.umask(0o077)
    try:
        if len(sys.argv) not in (2,3):
            raise ValueError('usage_tasks_py_add_list_done')
        action = sys.argv[1]
        if action == 'list' and len(sys.argv) != 2:
            raise ValueError('list_accepts_no_argument')
        result = execute(action, sys.argv[2] if len(sys.argv)==3 else None,
                         os.environ.get('A3_TASK_MEMORY_DIR',str(Path.home()/'.local/state/a3-task-memory')))
        print(json.dumps({'ok':True,'data':result},ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'ok':False,'error':str(exc) if isinstance(exc,ValueError) else 'task_storage_unavailable'}))
        raise SystemExit(1)
