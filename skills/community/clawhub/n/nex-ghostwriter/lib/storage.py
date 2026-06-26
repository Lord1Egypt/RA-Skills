"""
Nex Ghostwriter - SQLite storage layer
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import stat
import json
import sqlite3
import platform
import datetime as dt
from pathlib import Path
from contextlib import contextmanager

from lib.config import (
    DATA_DIR, DB_PATH, EXPORT_DIR, TEMPLATES_DIR,
    STATUS_DRAFT, STATUS_SENT, STATUS_SKIPPED,
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
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    if platform.system() != "Windows":
        try:
            os.chmod(str(DATA_DIR), stat.S_IRWXU)
        except OSError:
            pass

    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                meeting_type TEXT DEFAULT 'other',
                meeting_date TEXT,
                attendees TEXT,
                client_name TEXT,
                client_email TEXT,
                notes TEXT,
                action_items TEXT,
                next_steps TEXT,
                deadline TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER NOT NULL,
                subject TEXT,
                body TEXT NOT NULL,
                tone TEXT DEFAULT 'professional',
                status TEXT DEFAULT 'draft',
                sent_at TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                company TEXT,
                role TEXT,
                preferred_greeting TEXT,
                notes TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings(meeting_date);
            CREATE INDEX IF NOT EXISTS idx_meetings_client ON meetings(client_name);
            CREATE INDEX IF NOT EXISTS idx_meetings_type ON meetings(meeting_type);
            CREATE INDEX IF NOT EXISTS idx_drafts_meeting ON drafts(meeting_id);
            CREATE INDEX IF NOT EXISTS idx_drafts_status ON drafts(status);
            CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);

            CREATE VIRTUAL TABLE IF NOT EXISTS meetings_fts USING fts5(
                title, notes, action_items, next_steps, client_name, attendees
            );
        """)


# --- FTS sync ---

def _sync_fts(conn, row_id, title, notes, action_items, next_steps, client_name, attendees):
    conn.execute("DELETE FROM meetings_fts WHERE rowid = ?", (row_id,))
    conn.execute("""
        INSERT INTO meetings_fts(rowid, title, notes, action_items, next_steps, client_name, attendees)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (row_id, title or '', notes or '', action_items or '',
          next_steps or '', client_name or '', attendees or ''))


def _sync_fts_from_row(conn, row_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, notes, action_items, next_steps, client_name, attendees
        FROM meetings WHERE id = ?
    """, (row_id,))
    row = cursor.fetchone()
    if row:
        _sync_fts(conn, row_id, row['title'], row['notes'], row['action_items'],
                  row['next_steps'], row['client_name'], row['attendees'])


# --- Meetings CRUD ---

def save_meeting(title, meeting_type="other", meeting_date=None, attendees=None,
                 client_name=None, client_email=None, notes=None,
                 action_items=None, next_steps=None, deadline=None):
    if not meeting_date:
        meeting_date = dt.date.today().isoformat()

    action_items_json = None
    if action_items:
        if isinstance(action_items, list):
            action_items_json = json.dumps(action_items)
        else:
            action_items_json = action_items

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO meetings (title, meeting_type, meeting_date, attendees,
                                  client_name, client_email, notes, action_items,
                                  next_steps, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, meeting_type, meeting_date, attendees, client_name,
              client_email, notes, action_items_json, next_steps, deadline))
        row_id = cursor.lastrowid
        _sync_fts(conn, row_id, title, notes, action_items_json,
                  next_steps, client_name, attendees)
        return row_id


def get_meeting(meeting_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meetings WHERE id = ?", (meeting_id,))
        row = cursor.fetchone()
        if not row:
            return None

        meeting = dict(row)
        cursor.execute("SELECT * FROM drafts WHERE meeting_id = ? ORDER BY created_at DESC", (meeting_id,))
        meeting['drafts'] = [dict(d) for d in cursor.fetchall()]
        return meeting


def list_meetings(meeting_type=None, client_name=None, limit=50):
    with _connect() as conn:
        query = "SELECT * FROM meetings WHERE 1=1"
        params = []

        if meeting_type:
            query += " AND meeting_type = ?"
            params.append(meeting_type)
        if client_name:
            query += " AND client_name LIKE ?"
            params.append(f"%{client_name}%")

        query += " ORDER BY meeting_date DESC, created_at DESC LIMIT ?"
        params.append(limit)

        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def update_meeting(meeting_id, **kwargs):
    allowed = {
        'title', 'meeting_type', 'meeting_date', 'attendees',
        'client_name', 'client_email', 'notes', 'action_items',
        'next_steps', 'deadline',
    }
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return False

    fields['updated_at'] = dt.datetime.now().isoformat()
    set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values()) + [meeting_id]

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE meetings SET {set_clause} WHERE id = ?", values)
        if cursor.rowcount > 0:
            _sync_fts_from_row(conn, meeting_id)
            return True
        return False


def search_meetings(query_text):
    with _connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.*
                FROM meetings_fts fts
                JOIN meetings m ON m.id = fts.rowid
                WHERE meetings_fts MATCH ?
                ORDER BY fts.rank
                LIMIT 50
            """, (query_text,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            like_q = f"%{query_text}%"
            cursor.execute("""
                SELECT * FROM meetings
                WHERE title LIKE ? OR notes LIKE ? OR client_name LIKE ?
                   OR action_items LIKE ? OR next_steps LIKE ?
                ORDER BY meeting_date DESC LIMIT 50
            """, (like_q, like_q, like_q, like_q, like_q))
            return [dict(row) for row in cursor.fetchall()]


# --- Drafts CRUD ---

def save_draft(meeting_id, subject, body, tone="professional"):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO drafts (meeting_id, subject, body, tone, status)
            VALUES (?, ?, ?, ?, ?)
        """, (meeting_id, subject, body, tone, STATUS_DRAFT))
        return cursor.lastrowid


def get_draft(draft_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.*, m.title as meeting_title, m.client_name, m.client_email
            FROM drafts d
            JOIN meetings m ON d.meeting_id = m.id
            WHERE d.id = ?
        """, (draft_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def mark_draft_sent(draft_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE drafts SET status = ?, sent_at = datetime('now') WHERE id = ?
        """, (STATUS_SENT, draft_id))
        return cursor.rowcount > 0


def mark_draft_skipped(draft_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE drafts SET status = ? WHERE id = ?
        """, (STATUS_SKIPPED, draft_id))
        return cursor.rowcount > 0


def list_drafts(status=None, limit=50):
    with _connect() as conn:
        query = """
            SELECT d.*, m.title as meeting_title, m.client_name
            FROM drafts d
            JOIN meetings m ON d.meeting_id = m.id
            WHERE 1=1
        """
        params = []
        if status:
            query += " AND d.status = ?"
            params.append(status)

        query += " ORDER BY d.created_at DESC LIMIT ?"
        params.append(limit)

        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


# --- Contacts CRUD ---

def save_contact(name, email=None, company=None, role=None,
                 preferred_greeting=None, notes=None):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contacts (name, email, company, role, preferred_greeting, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, company, role, preferred_greeting, notes))
        return cursor.lastrowid


def get_contact(contact_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def find_contact_by_name(name):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", (f"%{name}%",))
        results = cursor.fetchall()
        return [dict(r) for r in results]


def list_contacts(limit=100):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY name ASC LIMIT ?", (limit,))
        return [dict(row) for row in cursor.fetchall()]


def update_contact(contact_id, **kwargs):
    allowed = {'name', 'email', 'company', 'role', 'preferred_greeting', 'notes'}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return False

    set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values()) + [contact_id]

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE contacts SET {set_clause} WHERE id = ?", values)
        return cursor.rowcount > 0


# --- Stats ---

def get_stats():
    with _connect() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as c FROM meetings")
        total_meetings = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) as c FROM drafts")
        total_drafts = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) as c FROM drafts WHERE status = ?", (STATUS_SENT,))
        sent = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) as c FROM drafts WHERE status = ?", (STATUS_DRAFT,))
        pending = cursor.fetchone()['c']

        cursor.execute("SELECT COUNT(*) as c FROM contacts")
        total_contacts = cursor.fetchone()['c']

        cursor.execute("""
            SELECT meeting_type, COUNT(*) as c FROM meetings
            GROUP BY meeting_type ORDER BY c DESC
        """)
        by_type = {row['meeting_type']: row['c'] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT client_name, COUNT(*) as c FROM meetings
            WHERE client_name IS NOT NULL AND client_name != ''
            GROUP BY client_name ORDER BY c DESC LIMIT 10
        """)
        top_clients = {row['client_name']: row['c'] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT strftime('%Y-%m', meeting_date) as month, COUNT(*) as c
            FROM meetings WHERE meeting_date IS NOT NULL
            GROUP BY month ORDER BY month DESC LIMIT 12
        """)
        by_month = {row['month']: row['c'] for row in cursor.fetchall()}

        return {
            'total_meetings': total_meetings,
            'total_drafts': total_drafts,
            'drafts_sent': sent,
            'drafts_pending': pending,
            'total_contacts': total_contacts,
            'by_type': by_type,
            'top_clients': top_clients,
            'by_month': by_month,
        }


# --- Export ---

def export_meetings(format_type='json'):
    meetings = list_meetings(limit=10000)
    if format_type == 'json':
        return json.dumps(meetings, indent=2, default=str)
    elif format_type == 'csv':
        import csv
        import io
        if not meetings:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=meetings[0].keys())
        writer.writeheader()
        writer.writerows(meetings)
        return output.getvalue()
    return ""
