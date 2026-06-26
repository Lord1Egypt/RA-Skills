"""
Nex MeetCost - SQLite storage layer
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
    DATA_DIR, DB_PATH, EXPORT_DIR,
    DEFAULT_RATES, CURRENCY_SYMBOL,
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
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                meeting_type TEXT DEFAULT 'other',
                meeting_date TEXT,
                duration_minutes REAL NOT NULL,
                attendees TEXT,
                total_cost REAL,
                notes TEXT,
                recurring INTEGER DEFAULT 0,
                recurrence_weekly INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS attendees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                role TEXT DEFAULT 'other',
                hourly_rate REAL,
                FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings(meeting_date);
            CREATE INDEX IF NOT EXISTS idx_meetings_type ON meetings(meeting_type);
            CREATE INDEX IF NOT EXISTS idx_attendees_meeting ON attendees(meeting_id);
        """)


def calculate_cost(duration_minutes, attendee_list):
    total = 0.0
    details = []
    for a in attendee_list:
        rate = a.get('rate') if a.get('rate') is not None else DEFAULT_RATES.get(a.get('role', 'other'), 85.0)
        cost = (duration_minutes / 60.0) * rate
        details.append({
            'name': a['name'],
            'role': a.get('role', 'other'),
            'rate': rate,
            'cost': round(cost, 2),
        })
        total += cost
    return round(total, 2), details


def save_meeting(title, duration_minutes, attendee_list, meeting_type="other",
                 meeting_date=None, notes=None, recurring=False, recurrence_weekly=0):
    if not meeting_date:
        meeting_date = dt.date.today().isoformat()

    total_cost, details = calculate_cost(duration_minutes, attendee_list)

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO meetings (title, meeting_type, meeting_date, duration_minutes,
                                  attendees, total_cost, notes, recurring, recurrence_weekly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, meeting_type, meeting_date, duration_minutes,
              json.dumps(attendee_list), total_cost, notes,
              1 if recurring else 0, recurrence_weekly))
        meeting_id = cursor.lastrowid

        for d in details:
            cursor.execute("""
                INSERT INTO attendees (meeting_id, name, role, hourly_rate)
                VALUES (?, ?, ?, ?)
            """, (meeting_id, d['name'], d['role'], d['rate']))

        return meeting_id, total_cost, details


def get_meeting(meeting_id):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meetings WHERE id = ?", (meeting_id,))
        row = cursor.fetchone()
        if not row:
            return None

        meeting = dict(row)
        cursor.execute("SELECT * FROM attendees WHERE meeting_id = ?", (meeting_id,))
        meeting['attendee_details'] = [dict(a) for a in cursor.fetchall()]
        return meeting


def list_meetings(meeting_type=None, date_from=None, date_to=None, limit=50):
    with _connect() as conn:
        query = "SELECT * FROM meetings WHERE 1=1"
        params = []

        if meeting_type:
            query += " AND meeting_type = ?"
            params.append(meeting_type)
        if date_from:
            query += " AND meeting_date >= ?"
            params.append(date_from)
        if date_to:
            query += " AND meeting_date <= ?"
            params.append(date_to)

        query += " ORDER BY meeting_date DESC, created_at DESC LIMIT ?"
        params.append(limit)

        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def get_stats(date_from=None, date_to=None):
    with _connect() as conn:
        cursor = conn.cursor()

        where = "WHERE 1=1"
        params = []
        if date_from:
            where += " AND meeting_date >= ?"
            params.append(date_from)
        if date_to:
            where += " AND meeting_date <= ?"
            params.append(date_to)

        cursor.execute(f"SELECT COUNT(*) as c FROM meetings {where}", params)
        total = cursor.fetchone()['c']

        cursor.execute(f"SELECT COALESCE(SUM(total_cost), 0) as t FROM meetings {where}", params)
        total_cost = cursor.fetchone()['t']

        cursor.execute(f"SELECT COALESCE(SUM(duration_minutes), 0) as t FROM meetings {where}", params)
        total_minutes = cursor.fetchone()['t']

        cursor.execute(f"""
            SELECT meeting_type, COUNT(*) as c, COALESCE(SUM(total_cost), 0) as cost,
                   COALESCE(SUM(duration_minutes), 0) as mins
            FROM meetings {where}
            GROUP BY meeting_type ORDER BY cost DESC
        """, params)
        by_type = {row['meeting_type']: {
            'count': row['c'], 'cost': round(row['cost'], 2), 'minutes': row['mins']
        } for row in cursor.fetchall()}

        # Recurring cost projection (monthly)
        cursor.execute("""
            SELECT COALESCE(SUM(total_cost * recurrence_weekly * 4.33), 0) as monthly
            FROM meetings WHERE recurring = 1
        """)
        monthly_recurring = round(cursor.fetchone()['monthly'], 2)

        cursor.execute(f"""
            SELECT strftime('%Y-%m', meeting_date) as month,
                   COUNT(*) as c, COALESCE(SUM(total_cost), 0) as cost
            FROM meetings {where} AND meeting_date IS NOT NULL
            GROUP BY month ORDER BY month DESC LIMIT 12
        """, params)
        by_month = {row['month']: {
            'count': row['c'], 'cost': round(row['cost'], 2)
        } for row in cursor.fetchall()}

        return {
            'total_meetings': total,
            'total_cost': round(total_cost, 2),
            'total_minutes': total_minutes,
            'total_hours': round(total_minutes / 60.0, 2),
            'avg_cost': round(total_cost / total, 2) if total > 0 else 0,
            'monthly_recurring': monthly_recurring,
            'by_type': by_type,
            'by_month': by_month,
        }


def export_meetings(format_type='json', **filters):
    meetings = list_meetings(limit=10000, **filters)
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
