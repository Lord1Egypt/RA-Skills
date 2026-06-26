"""
Nex Timetrack - SQLite storage layer
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import stat
import json
import math
import sqlite3
import platform
import datetime as dt
from pathlib import Path
from contextlib import contextmanager

from lib.config import (
    DATA_DIR, DB_PATH, EXPORT_DIR,
    BILLABLE, NON_BILLABLE, DEFAULT_RATE,
    ROUND_TO_MINUTES, CURRENCY_SYMBOL,
)


@contextmanager
def _connect():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    if platform.system() != "Windows":
        try:
            os.chmod(str(DATA_DIR), stat.S_IRWXU)
        except OSError:
            pass

    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                rate REAL,
                contact_email TEXT,
                notes TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                client_id INTEGER,
                rate REAL,
                budget_hours REAL,
                notes TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                client_id INTEGER,
                description TEXT NOT NULL,
                category TEXT DEFAULT 'other',
                started_at TEXT,
                ended_at TEXT,
                duration_minutes REAL,
                billable INTEGER DEFAULT 1,
                rate REAL,
                tags TEXT,
                notes TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
                FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS active_timer (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                description TEXT NOT NULL,
                project_id INTEGER,
                client_id INTEGER,
                category TEXT DEFAULT 'other',
                billable INTEGER DEFAULT 1,
                tags TEXT,
                started_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_entries_project ON entries(project_id);
            CREATE INDEX IF NOT EXISTS idx_entries_client ON entries(client_id);
            CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(started_at);
            CREATE INDEX IF NOT EXISTS idx_entries_billable ON entries(billable);
            CREATE INDEX IF NOT EXISTS idx_entries_category ON entries(category);
            CREATE INDEX IF NOT EXISTS idx_projects_client ON projects(client_id);
            CREATE INDEX IF NOT EXISTS idx_projects_active ON projects(active);

            CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(
                description, notes, tags
            );
        """)


# --- FTS sync ---

def _sync_fts(conn, row_id, description, notes, tags):
    conn.execute("DELETE FROM entries_fts WHERE rowid = ?", (row_id,))
    conn.execute("""
        INSERT INTO entries_fts(rowid, description, notes, tags)
        VALUES (?, ?, ?, ?)
    """, (row_id, description or '', notes or '', tags or ''))


def _sync_fts_from_row(conn, row_id):
    cursor = conn.cursor()
    cursor.execute("SELECT description, notes, tags FROM entries WHERE id = ?", (row_id,))
    row = cursor.fetchone()
    if row:
        _sync_fts(conn, row_id, row['description'], row['notes'], row['tags'])


# --- Timer ---

def start_timer(description, project_id=None, client_id=None, category="other",
                billable=True, tags=None):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_timer WHERE id = 1")
        existing = cursor.fetchone()
        if existing:
            return None, dict(existing)

        now = dt.datetime.now().isoformat()
        cursor.execute("""
            INSERT OR REPLACE INTO active_timer (id, description, project_id, client_id,
                                                  category, billable, tags, started_at)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        """, (description, project_id, client_id, category, 1 if billable else 0,
              tags, now))
        return now, None


def stop_timer(notes=None):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_timer WHERE id = 1")
        timer = cursor.fetchone()
        if not timer:
            return None

        timer = dict(timer)
        now = dt.datetime.now()
        started = dt.datetime.fromisoformat(timer['started_at'])
        duration = (now - started).total_seconds() / 60.0

        cursor.execute("""
            INSERT INTO entries (project_id, client_id, description, category,
                                started_at, ended_at, duration_minutes, billable,
                                rate, tags, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timer['project_id'], timer['client_id'], timer['description'],
              timer['category'], timer['started_at'], now.isoformat(),
              round(duration, 1), timer['billable'],
              _resolve_rate(conn, timer['project_id'], timer['client_id']),
              timer['tags'], notes))

        entry_id = cursor.lastrowid
        _sync_fts(conn, entry_id, timer['description'], notes, timer['tags'])
        cursor.execute("DELETE FROM active_timer WHERE id = 1")

        return {
            'entry_id': entry_id,
            'description': timer['description'],
            'started_at': timer['started_at'],
            'ended_at': now.isoformat(),
            'duration_minutes': round(duration, 1),
        }


def get_active_timer():
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_timer WHERE id = 1")
        row = cursor.fetchone()
        if not row:
            return None
        timer = dict(row)
        now = dt.datetime.now()
        started = dt.datetime.fromisoformat(timer['started_at'])
        timer['elapsed_minutes'] = round((now - started).total_seconds() / 60.0, 1)
        return timer


def cancel_timer():
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_timer WHERE id = 1")
        timer = cursor.fetchone()
        if not timer:
            return None
        timer = dict(timer)
        cursor.execute("DELETE FROM active_timer WHERE id = 1")
        return timer


# --- Entries CRUD ---

def save_entry(description, duration_minutes, project_id=None, client_id=None,
               category="other", billable=True, tags=None, notes=None,
               entry_date=None, rate=None):
    if not entry_date:
        entry_date = dt.date.today().isoformat()

    started_at = f"{entry_date}T09:00:00"

    with _connect() as conn:
        if rate is None:
            rate = _resolve_rate(conn, project_id, client_id)

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entries (project_id, client_id, description, category,
                                started_at, duration_minutes, billable, rate, tags, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (project_id, client_id, description, category, started_at,
              duration_minutes, 1 if billable else 0, rate, tags, notes))
        row_id = cursor.lastrowid
        _sync_fts(conn, row_id, description, notes, tags)
        return row_id


def get_entry(entry_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.*, p.name as project_name, c.name as client_name
            FROM entries e
            LEFT JOIN projects p ON e.project_id = p.id
            LEFT JOIN clients c ON e.client_id = c.id
            WHERE e.id = ?
        """, (entry_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def list_entries(project_id=None, client_id=None, category=None,
                 billable=None, date_from=None, date_to=None, limit=50):
    with _connect() as conn:
        query = """
            SELECT e.*, p.name as project_name, c.name as client_name
            FROM entries e
            LEFT JOIN projects p ON e.project_id = p.id
            LEFT JOIN clients c ON e.client_id = c.id
            WHERE 1=1
        """
        params = []

        if project_id:
            query += " AND e.project_id = ?"
            params.append(project_id)
        if client_id:
            query += " AND e.client_id = ?"
            params.append(client_id)
        if category:
            query += " AND e.category = ?"
            params.append(category)
        if billable is not None:
            query += " AND e.billable = ?"
            params.append(1 if billable else 0)
        if date_from:
            query += " AND e.started_at >= ?"
            params.append(date_from)
        if date_to:
            query += " AND e.started_at <= ?"
            params.append(date_to + "T23:59:59")

        query += " ORDER BY e.started_at DESC LIMIT ?"
        params.append(limit)

        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def update_entry(entry_id, **kwargs):
    allowed = {
        'description', 'category', 'duration_minutes', 'billable',
        'rate', 'tags', 'notes', 'project_id', 'client_id',
    }
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return False

    if 'billable' in fields:
        fields['billable'] = 1 if fields['billable'] else 0

    fields['updated_at'] = dt.datetime.now().isoformat()
    set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values()) + [entry_id]

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE entries SET {set_clause} WHERE id = ?", values)
        if cursor.rowcount > 0:
            _sync_fts_from_row(conn, entry_id)
            return True
        return False


def delete_entry(entry_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entries_fts WHERE rowid = ?", (entry_id,))
        cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        return cursor.rowcount > 0


def search_entries(query_text):
    with _connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT e.*, p.name as project_name, c.name as client_name
                FROM entries_fts fts
                JOIN entries e ON e.id = fts.rowid
                LEFT JOIN projects p ON e.project_id = p.id
                LEFT JOIN clients c ON e.client_id = c.id
                WHERE entries_fts MATCH ?
                ORDER BY fts.rank
                LIMIT 50
            """, (query_text,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            like_q = f"%{query_text}%"
            cursor.execute("""
                SELECT e.*, p.name as project_name, c.name as client_name
                FROM entries e
                LEFT JOIN projects p ON e.project_id = p.id
                LEFT JOIN clients c ON e.client_id = c.id
                WHERE e.description LIKE ? OR e.notes LIKE ? OR e.tags LIKE ?
                ORDER BY e.started_at DESC LIMIT 50
            """, (like_q, like_q, like_q))
            return [dict(row) for row in cursor.fetchall()]


# --- Clients ---

def save_client(name, rate=None, contact_email=None, notes=None):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clients (name, rate, contact_email, notes)
            VALUES (?, ?, ?, ?)
        """, (name, rate, contact_email, notes))
        return cursor.lastrowid


def get_client(client_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def find_client_by_name(name):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE name LIKE ?", (f"%{name}%",))
        results = cursor.fetchall()
        return [dict(r) for r in results]


def list_clients():
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ORDER BY name ASC")
        return [dict(row) for row in cursor.fetchall()]


# --- Projects ---

def save_project(name, client_id=None, rate=None, budget_hours=None, notes=None):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (name, client_id, rate, budget_hours, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (name, client_id, rate, budget_hours, notes))
        return cursor.lastrowid


def get_project(project_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, c.name as client_name
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.id
            WHERE p.id = ?
        """, (project_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def find_project_by_name(name):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, c.name as client_name
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.id
            WHERE p.name LIKE ?
        """, (f"%{name}%",))
        return [dict(r) for r in cursor.fetchall()]


def list_projects(active_only=True):
    with _connect() as conn:
        query = """
            SELECT p.*, c.name as client_name
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.id
        """
        if active_only:
            query += " WHERE p.active = 1"
        query += " ORDER BY p.name ASC"

        cursor = conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]


# --- Rate resolution ---

def _resolve_rate(conn, project_id=None, client_id=None):
    if project_id:
        cursor = conn.cursor()
        cursor.execute("SELECT rate, client_id FROM projects WHERE id = ?", (project_id,))
        proj = cursor.fetchone()
        if proj and proj['rate']:
            return proj['rate']
        if proj and proj['client_id']:
            client_id = proj['client_id']

    if client_id:
        cursor = conn.cursor()
        cursor.execute("SELECT rate FROM clients WHERE id = ?", (client_id,))
        cl = cursor.fetchone()
        if cl and cl['rate']:
            return cl['rate']

    return DEFAULT_RATE


# --- Reporting ---

def _round_up(minutes):
    if ROUND_TO_MINUTES <= 0:
        return minutes
    return math.ceil(minutes / ROUND_TO_MINUTES) * ROUND_TO_MINUTES


def get_summary(client_id=None, project_id=None, date_from=None, date_to=None,
                billable_only=False, round_up=False):
    entries = list_entries(
        client_id=client_id,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
        billable=True if billable_only else None,
        limit=10000,
    )

    total_minutes = 0
    billable_minutes = 0
    total_amount = 0.0
    by_client = {}
    by_project = {}
    by_category = {}
    by_date = {}

    for e in entries:
        mins = e['duration_minutes'] or 0
        if round_up:
            mins = _round_up(mins)

        total_minutes += mins

        if e['billable']:
            billable_minutes += mins
            rate = e['rate'] or DEFAULT_RATE
            total_amount += (mins / 60.0) * rate

        client = e['client_name'] or "No client"
        by_client.setdefault(client, {'minutes': 0, 'amount': 0.0})
        by_client[client]['minutes'] += mins
        if e['billable']:
            by_client[client]['amount'] += (mins / 60.0) * (e['rate'] or DEFAULT_RATE)

        project = e['project_name'] or "No project"
        by_project.setdefault(project, {'minutes': 0, 'amount': 0.0})
        by_project[project]['minutes'] += mins
        if e['billable']:
            by_project[project]['amount'] += (mins / 60.0) * (e['rate'] or DEFAULT_RATE)

        cat = e['category'] or "other"
        by_category.setdefault(cat, 0)
        by_category[cat] += mins

        date_key = e['started_at'][:10] if e['started_at'] else "unknown"
        by_date.setdefault(date_key, 0)
        by_date[date_key] += mins

    return {
        'total_entries': len(entries),
        'total_minutes': total_minutes,
        'total_hours': round(total_minutes / 60.0, 2),
        'billable_minutes': billable_minutes,
        'billable_hours': round(billable_minutes / 60.0, 2),
        'total_amount': round(total_amount, 2),
        'by_client': by_client,
        'by_project': by_project,
        'by_category': by_category,
        'by_date': dict(sorted(by_date.items())),
    }


def get_stats():
    with _connect() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as c FROM entries")
        total_entries = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) as c FROM clients")
        total_clients = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) as c FROM projects WHERE active = 1")
        total_projects = cursor.fetchone()['c']

        cursor.execute("SELECT COALESCE(SUM(duration_minutes), 0) as t FROM entries")
        total_minutes = cursor.fetchone()['t']

        cursor.execute("SELECT COALESCE(SUM(duration_minutes), 0) as t FROM entries WHERE billable = 1")
        billable_minutes = cursor.fetchone()['t']

        cursor.execute("""
            SELECT COALESCE(SUM(duration_minutes / 60.0 * COALESCE(rate, ?)), 0) as t
            FROM entries WHERE billable = 1
        """, (DEFAULT_RATE,))
        total_revenue = cursor.fetchone()['t']

        cursor.execute("""
            SELECT category, COALESCE(SUM(duration_minutes), 0) as t
            FROM entries GROUP BY category ORDER BY t DESC
        """)
        by_category = {row['category']: row['t'] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT c.name, COALESCE(SUM(e.duration_minutes), 0) as t
            FROM entries e
            JOIN clients c ON e.client_id = c.id
            GROUP BY c.name ORDER BY t DESC LIMIT 10
        """)
        top_clients = {row['name']: row['t'] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT strftime('%Y-%m', started_at) as month, COALESCE(SUM(duration_minutes), 0) as t
            FROM entries WHERE started_at IS NOT NULL
            GROUP BY month ORDER BY month DESC LIMIT 12
        """)
        by_month = {row['month']: row['t'] for row in cursor.fetchall()}

        return {
            'total_entries': total_entries,
            'total_clients': total_clients,
            'total_projects': total_projects,
            'total_minutes': total_minutes,
            'total_hours': round(total_minutes / 60.0, 2),
            'billable_minutes': billable_minutes,
            'billable_hours': round(billable_minutes / 60.0, 2),
            'total_revenue': round(total_revenue, 2),
            'by_category': by_category,
            'top_clients': top_clients,
            'by_month': by_month,
        }


# --- Export ---

def export_entries(format_type='json', **filters):
    entries = list_entries(limit=10000, **filters)
    if format_type == 'json':
        return json.dumps(entries, indent=2, default=str)
    elif format_type == 'csv':
        import csv
        import io
        if not entries:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=entries[0].keys())
        writer.writeheader()
        writer.writerows(entries)
        return output.getvalue()
    return ""
