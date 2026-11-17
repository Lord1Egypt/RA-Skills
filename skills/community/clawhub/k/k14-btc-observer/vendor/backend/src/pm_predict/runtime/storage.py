"""A separate SQLite WAL writer process; never called from strategy functions."""
import json
from contextlib import closing
from pathlib import Path
import queue
import sqlite3
import time
import orjson


def encode(x):
    return orjson.dumps(x, default=str).decode()


def writer_main(inbox, acknowledgments, db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=FULL')
    conn.executescript('''CREATE TABLE IF NOT EXISTS runs(
      id TEXT PRIMARY KEY, scenario TEXT, title TEXT, created_ms INTEGER, status TEXT, snapshot TEXT);
      CREATE TABLE IF NOT EXISTS events(
      run_id TEXT, sequence INTEGER, payload TEXT NOT NULL, duplicate INTEGER,
      PRIMARY KEY(run_id,sequence));''')
    conn.execute("UPDATE runs SET status='interrupted' WHERE status IN ('running','paused')")
    conn.commit()
    saved = 0
    while True:
        message = inbox.get()
        if message is None:
            conn.commit(); conn.close(); return
        batch = [message]
        stopping = False
        while len(batch) < 64:
            try:
                item = inbox.get_nowait()
                if item is None:
                    stopping = True; break
                batch.append(item)
            except queue.Empty:
                break
        for item in batch:
            if item['kind'] == 'run_started':
                conn.execute('INSERT INTO runs VALUES(?,?,?,?,?,?)', (item['run_id'],item['scenario'],item['title'],item['created_ms'],'running','{}'))
            elif item['kind'] == 'event':
                conn.execute('INSERT INTO events VALUES(?,?,?,?)', (item['run_id'], item['sequence'], encode(item['payload']), int(item['duplicate'])))
                saved += 1
            elif item['kind'] == 'snapshot':
                p = item['payload']
                if p['run_id']:
                    conn.execute('UPDATE runs SET status=?,snapshot=? WHERE id=?', (p['status'],encode(p),p['run_id']))
            elif item['kind'] == 'runtime_error':
                conn.execute('UPDATE runs SET status=? WHERE id=?', ('error',item['run_id']))
        conn.commit()
        try:
            acknowledgments.put_nowait({'persisted_events': saved, 'last_commit_ms': int(time.time()*1000)})
        except queue.Full:
            pass  # Only redundant writer telemetry, never ledger events.
        if stopping:
            conn.close(); return


def history(db_path):
    if not Path(db_path).exists():
        return []
    with closing(sqlite3.connect(f'file:{Path(db_path).as_posix()}?mode=ro', uri=True)) as c:
        c.row_factory = sqlite3.Row
        return [dict(r) for r in c.execute('SELECT id,scenario,title,created_ms,status FROM runs ORDER BY created_ms DESC LIMIT 50')]


def load_run(db_path, run_id):
    with closing(sqlite3.connect(f'file:{Path(db_path).as_posix()}?mode=ro', uri=True)) as c:
        r = c.execute('SELECT snapshot,status FROM runs WHERE id=?', (run_id,)).fetchone()
        if r is None:
            return None
        value = json.loads(r[0])
        value['status'] = r[1]
        return value

