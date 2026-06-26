"""
Nex Decision Journal - SQLite storage layer
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
    STATUS_PENDING, STATUS_REVIEWED, STATUS_ABANDONED,
    ACCURACY_OPTIONS,
)


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------
@contextmanager
def _connect():
    """Context manager for database connections."""
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


# ---------------------------------------------------------------------------
# Schema initialization
# ---------------------------------------------------------------------------
def init_db():
    """Create database and tables if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    if platform.system() != "Windows":
        try:
            os.chmod(str(DATA_DIR), stat.S_IRWXU)
        except OSError:
            pass

    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                context TEXT,
                options TEXT,
                chosen_option TEXT,
                reasoning TEXT,
                prediction TEXT,
                confidence INTEGER DEFAULT 5,
                category TEXT DEFAULT 'other',
                tags TEXT,
                stakes TEXT DEFAULT 'medium',
                reversible INTEGER DEFAULT 1,
                follow_up_date TEXT,
                status TEXT DEFAULT 'pending',
                outcome TEXT,
                outcome_date TEXT,
                outcome_notes TEXT,
                prediction_accuracy TEXT,
                lessons_learned TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_decisions_status
                ON decisions(status);
            CREATE INDEX IF NOT EXISTS idx_decisions_category
                ON decisions(category);
            CREATE INDEX IF NOT EXISTS idx_decisions_follow_up
                ON decisions(follow_up_date);
            CREATE INDEX IF NOT EXISTS idx_decisions_created
                ON decisions(created_at);
            CREATE INDEX IF NOT EXISTS idx_decisions_confidence
                ON decisions(confidence);

            CREATE VIRTUAL TABLE IF NOT EXISTS decisions_fts USING fts5(
                title,
                context,
                options,
                reasoning,
                prediction,
                outcome,
                lessons_learned
            );
        """)


# ---------------------------------------------------------------------------
# FTS sync helper
# ---------------------------------------------------------------------------
def _sync_fts(conn, row_id, title, context, options, reasoning,
              prediction, outcome, lessons_learned):
    """Upsert a decision into the FTS index."""
    conn.execute("DELETE FROM decisions_fts WHERE rowid = ?", (row_id,))
    conn.execute("""
        INSERT INTO decisions_fts(rowid, title, context, options, reasoning,
                                  prediction, outcome, lessons_learned)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (row_id,
          title or '', context or '', options or '', reasoning or '',
          prediction or '', outcome or '', lessons_learned or ''))


def _sync_fts_from_row(conn, row_id):
    """Rebuild FTS entry from current row data."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, context, options, reasoning, prediction, outcome, lessons_learned
        FROM decisions WHERE id = ?
    """, (row_id,))
    row = cursor.fetchone()
    if row:
        _sync_fts(conn, row_id, row['title'], row['context'], row['options'],
                  row['reasoning'], row['prediction'], row['outcome'],
                  row['lessons_learned'])


# ---------------------------------------------------------------------------
# CRUD: Create
# ---------------------------------------------------------------------------
def save_decision(title, context=None, options=None, chosen_option=None,
                  reasoning=None, prediction=None, confidence=5,
                  category="other", tags=None, stakes="medium",
                  reversible=True, follow_up_date=None):
    """Save a new decision. Returns decision ID."""
    options_json = None
    if options:
        if isinstance(options, list):
            options_json = json.dumps(options)
        else:
            options_json = options

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO decisions (
                title, context, options, chosen_option, reasoning,
                prediction, confidence, category, tags, stakes,
                reversible, follow_up_date, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, context, options_json, chosen_option, reasoning,
            prediction, confidence, category, tags, stakes,
            1 if reversible else 0, follow_up_date, STATUS_PENDING
        ))
        row_id = cursor.lastrowid
        _sync_fts(conn, row_id, title, context, options_json,
                  reasoning, prediction, None, None)
        return row_id


# ---------------------------------------------------------------------------
# CRUD: Read
# ---------------------------------------------------------------------------
def get_decision(decision_id):
    """Get a decision by ID."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def list_decisions(status=None, category=None, tags=None, limit=50, offset=0):
    """List decisions with optional filters."""
    with _connect() as conn:
        query = "SELECT * FROM decisions WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)
        if category:
            query += " AND category = ?"
            params.append(category)
        if tags:
            query += " AND tags LIKE ?"
            params.append(f"%{tags}%")

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def get_pending_reviews():
    """Get decisions where follow_up_date has passed and no outcome recorded."""
    today = dt.date.today().isoformat()
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM decisions
            WHERE status = ?
              AND follow_up_date IS NOT NULL
              AND follow_up_date <= ?
            ORDER BY follow_up_date ASC
        """, (STATUS_PENDING, today))
        return [dict(row) for row in cursor.fetchall()]


def get_decisions_by_date_range(start_date, end_date):
    """Get decisions created within a date range."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM decisions
            WHERE date(created_at) >= ? AND date(created_at) <= ?
            ORDER BY created_at DESC
        """, (start_date, end_date))
        return [dict(row) for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# CRUD: Update
# ---------------------------------------------------------------------------
def update_decision(decision_id, **kwargs):
    """Update a decision's fields."""
    allowed_fields = {
        'title', 'context', 'options', 'chosen_option', 'reasoning',
        'prediction', 'confidence', 'category', 'tags', 'stakes',
        'reversible', 'follow_up_date', 'status',
        'outcome', 'outcome_date', 'outcome_notes',
        'prediction_accuracy', 'lessons_learned',
    }
    fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
    if not fields:
        return False

    fields['updated_at'] = dt.datetime.now().isoformat()
    set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values()) + [decision_id]

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE decisions SET {set_clause} WHERE id = ?", values)
        if cursor.rowcount > 0:
            _sync_fts_from_row(conn, decision_id)
            return True
        return False


def record_outcome(decision_id, outcome, prediction_accuracy,
                   outcome_notes=None, lessons_learned=None):
    """Record the outcome of a decision."""
    if prediction_accuracy not in ACCURACY_OPTIONS:
        raise ValueError(f"prediction_accuracy must be one of: {ACCURACY_OPTIONS}")

    return update_decision(
        decision_id,
        outcome=outcome,
        outcome_date=dt.date.today().isoformat(),
        outcome_notes=outcome_notes,
        prediction_accuracy=prediction_accuracy,
        lessons_learned=lessons_learned,
        status=STATUS_REVIEWED,
    )


def abandon_decision(decision_id, reason=None):
    """Mark a decision as abandoned."""
    return update_decision(
        decision_id,
        status=STATUS_ABANDONED,
        outcome_notes=reason or "Decision abandoned",
    )


# ---------------------------------------------------------------------------
# CRUD: Delete
# ---------------------------------------------------------------------------
def delete_decision(decision_id):
    """Permanently delete a decision."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM decisions_fts WHERE rowid = ?", (decision_id,))
        cursor.execute("DELETE FROM decisions WHERE id = ?", (decision_id,))
        return cursor.rowcount > 0


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
def search_decisions(query_text):
    """Full-text search across all decision fields."""
    with _connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT d.*
                FROM decisions_fts fts
                JOIN decisions d ON d.id = fts.rowid
                WHERE decisions_fts MATCH ?
                ORDER BY fts.rank
                LIMIT 50
            """, (query_text,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            like_q = f"%{query_text}%"
            cursor.execute("""
                SELECT * FROM decisions
                WHERE title LIKE ? OR context LIKE ? OR reasoning LIKE ?
                   OR prediction LIKE ? OR outcome LIKE ? OR lessons_learned LIKE ?
                ORDER BY created_at DESC
                LIMIT 50
            """, (like_q, like_q, like_q, like_q, like_q, like_q))
            return [dict(row) for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
def get_stats():
    """Get decision journal statistics."""
    with _connect() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM decisions")
        total = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM decisions WHERE status = ?", (STATUS_PENDING,))
        pending = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM decisions WHERE status = ?", (STATUS_REVIEWED,))
        reviewed = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM decisions WHERE status = ?", (STATUS_ABANDONED,))
        abandoned = cursor.fetchone()['count']

        cursor.execute("""
            SELECT prediction_accuracy, COUNT(*) as count
            FROM decisions
            WHERE status = ? AND prediction_accuracy IS NOT NULL
            GROUP BY prediction_accuracy
        """, (STATUS_REVIEWED,))
        accuracy_rows = cursor.fetchall()
        accuracy = {row['prediction_accuracy']: row['count'] for row in accuracy_rows}

        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM decisions
            GROUP BY category
            ORDER BY count DESC
        """)
        by_category = {row['category']: row['count'] for row in cursor.fetchall()}

        cursor.execute("SELECT AVG(confidence) as avg_conf FROM decisions WHERE confidence IS NOT NULL")
        avg_confidence_row = cursor.fetchone()
        avg_confidence = round(avg_confidence_row['avg_conf'], 1) if avg_confidence_row['avg_conf'] else 0

        confidence_by_accuracy = {}
        for acc in ACCURACY_OPTIONS:
            cursor.execute("""
                SELECT AVG(confidence) as avg_conf
                FROM decisions
                WHERE prediction_accuracy = ? AND confidence IS NOT NULL
            """, (acc,))
            row = cursor.fetchone()
            if row['avg_conf'] is not None:
                confidence_by_accuracy[acc] = round(row['avg_conf'], 1)

        cursor.execute("""
            SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count
            FROM decisions
            WHERE created_at >= date('now', '-12 months')
            GROUP BY month
            ORDER BY month
        """)
        by_month = {row['month']: row['count'] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT stakes, COUNT(*) as count
            FROM decisions
            GROUP BY stakes
            ORDER BY count DESC
        """)
        by_stakes = {row['stakes']: row['count'] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT COUNT(*) as count FROM decisions
            WHERE confidence >= 8 AND prediction_accuracy = 'wrong'
        """)
        overconfident = cursor.fetchone()['count']

        cursor.execute("""
            SELECT COUNT(*) as count FROM decisions
            WHERE confidence <= 3 AND prediction_accuracy = 'correct'
        """)
        underconfident = cursor.fetchone()['count']

        today = dt.date.today().isoformat()
        cursor.execute("""
            SELECT COUNT(*) as count FROM decisions
            WHERE status = ? AND follow_up_date IS NOT NULL AND follow_up_date <= ?
        """, (STATUS_PENDING, today))
        pending_reviews = cursor.fetchone()['count']

        return {
            'total': total,
            'pending': pending,
            'reviewed': reviewed,
            'abandoned': abandoned,
            'accuracy': accuracy,
            'by_category': by_category,
            'avg_confidence': avg_confidence,
            'confidence_by_accuracy': confidence_by_accuracy,
            'by_month': by_month,
            'by_stakes': by_stakes,
            'overconfident_wrong': overconfident,
            'underconfident_correct': underconfident,
            'pending_reviews': pending_reviews,
        }


def get_all_tags():
    """Get all unique tags used across decisions."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tags FROM decisions WHERE tags IS NOT NULL AND tags != ''")
        all_tags = set()
        for row in cursor.fetchall():
            for tag in row['tags'].split(','):
                tag = tag.strip()
                if tag:
                    all_tags.add(tag)
        return sorted(all_tags)


# ---------------------------------------------------------------------------
# Reflection queries
# ---------------------------------------------------------------------------
def get_lessons():
    """Get all decisions with recorded lessons learned."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM decisions
            WHERE lessons_learned IS NOT NULL AND lessons_learned != ''
            ORDER BY outcome_date DESC
        """)
        return [dict(row) for row in cursor.fetchall()]


def get_overconfident_decisions():
    """Decisions where confidence was high but prediction was wrong."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM decisions
            WHERE confidence >= 7 AND prediction_accuracy = 'wrong'
            ORDER BY confidence DESC
        """)
        return [dict(row) for row in cursor.fetchall()]


def get_underconfident_decisions():
    """Decisions where confidence was low but prediction was correct."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM decisions
            WHERE confidence <= 4 AND prediction_accuracy = 'correct'
            ORDER BY confidence ASC
        """)
        return [dict(row) for row in cursor.fetchall()]


def get_accuracy_by_category():
    """Get prediction accuracy breakdown per category."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                category,
                COUNT(*) as total,
                SUM(CASE WHEN prediction_accuracy = 'correct' THEN 1 ELSE 0 END) as correct,
                SUM(CASE WHEN prediction_accuracy = 'partially_correct' THEN 1 ELSE 0 END) as partial,
                SUM(CASE WHEN prediction_accuracy = 'wrong' THEN 1 ELSE 0 END) as wrong
            FROM decisions
            WHERE status = 'reviewed' AND prediction_accuracy IS NOT NULL
            GROUP BY category
            ORDER BY total DESC
        """)
        return [dict(row) for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
def export_decisions(format_type='json', status=None):
    """Export decisions to JSON or CSV."""
    decisions = list_decisions(status=status, limit=10000)

    if format_type == 'json':
        return json.dumps(decisions, indent=2, default=str)
    elif format_type == 'csv':
        import csv
        import io

        if not decisions:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=decisions[0].keys())
        writer.writeheader()
        writer.writerows(decisions)
        return output.getvalue()

    return ""
