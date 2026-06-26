"""
Nex CRM - Storage and Database Layer
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import datetime as dt
import sqlite3
import json
from pathlib import Path

from config import DB_PATH, DATA_DIR, PIPELINE_STAGES, ACTIVITY_TYPES, LEAD_SOURCES

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


def db_conn():
    """Get a database connection."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema."""
    conn = db_conn()
    cur = conn.cursor()

    # Prospects table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prospects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL UNIQUE,
            contact_name TEXT,
            email TEXT,
            phone TEXT,
            source TEXT DEFAULT 'other',
            priority TEXT DEFAULT 'cold',
            value INTEGER DEFAULT 0,
            stage TEXT DEFAULT 'lead',
            notes TEXT,
            created_at TEXT,
            updated_at TEXT,
            last_contact TEXT,
            next_follow_up TEXT,
            industry TEXT,
            tags TEXT,
            metadata TEXT
        )
    """)

    # Activities table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id INTEGER NOT NULL,
            type TEXT,
            summary TEXT,
            timestamp TEXT,
            channel TEXT DEFAULT 'note',
            direction TEXT DEFAULT 'outbound',
            details TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        )
    """)

    # Follow-ups table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS follow_ups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id INTEGER NOT NULL,
            date TEXT,
            message TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        )
    """)

    # Reminders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id INTEGER NOT NULL,
            date TEXT,
            message TEXT,
            reminded INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        )
    """)

    # Interactions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id INTEGER NOT NULL,
            channel TEXT,
            message TEXT,
            direction TEXT,
            timestamp TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        )
    """)

    # Create indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_prospects_company ON prospects(company)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_prospects_stage ON prospects(stage)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_prospects_priority ON prospects(priority)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_activities_prospect ON activities(prospect_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_follow_ups_prospect ON follow_ups(prospect_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reminders_prospect ON reminders(prospect_id)")

    conn.commit()
    conn.close()


def add_prospect(data):
    """Add a new prospect."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO prospects (
            company, contact_name, email, phone, source, priority, value,
            stage, notes, created_at, updated_at, industry, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("company"),
        data.get("contact_name"),
        data.get("email"),
        data.get("phone"),
        data.get("source", "other"),
        data.get("priority", "cold"),
        data.get("value", 0),
        data.get("stage", "lead"),
        data.get("notes", ""),
        now,
        now,
        data.get("industry"),
        json.dumps(data.get("tags", []))
    ))

    prospect_id = cur.lastrowid
    conn.commit()
    conn.close()

    return prospect_id


def get_prospect(prospect_id):
    """Get a prospect by ID."""
    conn = db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM prospects WHERE id = ?
    """, (prospect_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    prospect = dict(row)
    if prospect.get("tags"):
        prospect["tags"] = json.loads(prospect["tags"])
    return prospect


def list_prospects(filters=None):
    """List prospects with optional filters."""
    conn = db_conn()
    cur = conn.cursor()

    filters = filters or {}
    query = "SELECT * FROM prospects WHERE 1=1"
    params = []

    if "stage" in filters:
        query += " AND stage = ?"
        params.append(filters["stage"])

    if "priority" in filters:
        query += " AND priority = ?"
        params.append(filters["priority"])

    if "source" in filters:
        query += " AND source = ?"
        params.append(filters["source"])

    if filters.get("stale"):
        # Stale: no contact in 14+ days
        cutoff = (dt.datetime.now() - dt.timedelta(days=14)).isoformat()
        query += " AND (last_contact IS NULL OR last_contact < ?)"
        params.append(cutoff)
        query += " AND stage NOT IN ('won', 'lost', 'churned')"

    query += " ORDER BY created_at DESC"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    prospects = []
    for row in rows:
        prospect = dict(row)
        if prospect.get("tags"):
            prospect["tags"] = json.loads(prospect["tags"])
        prospects.append(prospect)

    return prospects


def update_prospect_stage(prospect_id, stage, reason=""):
    """Update prospect stage."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    cur.execute("""
        UPDATE prospects
        SET stage = ?, updated_at = ?, last_contact = ?
        WHERE id = ?
    """, (stage, now, now, prospect_id))

    # If moving to won/lost, log activity
    if stage in ["won", "lost"]:
        summary = f"Deal {stage.upper()}"
        if reason:
            summary += f": {reason}"
        log_activity(prospect_id, {"type": "note", "summary": summary})

    conn.commit()
    conn.close()


def log_activity(prospect_id, data):
    """Log an activity for a prospect."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO activities (prospect_id, type, summary, timestamp, channel, direction)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        prospect_id,
        data.get("type", "note"),
        data.get("summary", ""),
        now,
        data.get("channel", "note"),
        data.get("direction", "outbound")
    ))

    # Update prospect's last_contact
    cur.execute("""
        UPDATE prospects SET last_contact = ? WHERE id = ?
    """, (now, prospect_id))

    conn.commit()
    conn.close()


def get_activities(prospect_id, limit=10):
    """Get activities for a prospect."""
    conn = db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM activities WHERE prospect_id = ?
        ORDER BY timestamp DESC LIMIT ?
    """, (prospect_id, limit))

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_follow_ups(days_ahead=None):
    """Get follow-ups due."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    query = """
        SELECT f.*, p.company, p.stage
        FROM follow_ups f
        JOIN prospects p ON f.prospect_id = p.id
        WHERE f.completed = 0 AND f.date <= ?
        ORDER BY f.date ASC
    """

    cur.execute(query, (now,))
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def set_follow_up(prospect_id, date, message=""):
    """Set a follow-up date."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO follow_ups (prospect_id, date, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (prospect_id, date, message, now))

    # Update prospect's next_follow_up
    cur.execute("""
        UPDATE prospects SET next_follow_up = ? WHERE id = ?
    """, (date, prospect_id))

    conn.commit()
    conn.close()


def search_prospects(query):
    """Search prospects by text."""
    conn = db_conn()
    cur = conn.cursor()

    search_pattern = f"%{query}%"
    cur.execute("""
        SELECT * FROM prospects
        WHERE company LIKE ? OR contact_name LIKE ? OR email LIKE ? OR notes LIKE ?
        ORDER BY company ASC
    """, (search_pattern, search_pattern, search_pattern, search_pattern))

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_pipeline_stats():
    """Get pipeline statistics by stage."""
    conn = db_conn()
    cur = conn.cursor()

    stats = {}
    for stage in PIPELINE_STAGES:
        cur.execute("""
            SELECT COUNT(*) as count, COALESCE(SUM(value), 0) as value
            FROM prospects WHERE stage = ?
        """, (stage,))
        row = cur.fetchone()
        stats[stage] = {"count": row[0], "value": row[1]}

    conn.close()
    return stats


def get_stale_prospects(days=14):
    """Get prospects with no contact for N days."""
    conn = db_conn()
    cur = conn.cursor()

    cutoff = (dt.datetime.now() - dt.timedelta(days=days)).isoformat()
    cur.execute("""
        SELECT * FROM prospects
        WHERE (last_contact IS NULL OR last_contact < ?)
        AND stage NOT IN ('won', 'lost', 'churned')
        ORDER BY last_contact ASC
    """, (cutoff,))

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def export_prospects(format="json"):
    """Export all prospects."""
    prospects = list_prospects({})
    return prospects


def interact_with_prospect(prospect_id, channel, message, direction="outbound"):
    """Store an interaction/conversation."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO interactions (prospect_id, channel, message, direction, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (prospect_id, channel, message, direction, now))

    # Log as activity too
    activity_type = "call" if channel == "call" else "email" if channel == "email" else "note"
    cur.execute("""
        INSERT INTO activities (prospect_id, type, summary, timestamp, channel, direction)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (prospect_id, activity_type, message[:100], now, channel, direction))

    # Update last_contact
    cur.execute("""
        UPDATE prospects SET last_contact = ? WHERE id = ?
    """, (now, prospect_id))

    conn.commit()
    conn.close()


def set_reminder(prospect_id, date, message=""):
    """Set a reminder."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO reminders (prospect_id, date, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (prospect_id, date, message, now))

    conn.commit()
    conn.close()


def get_reminders():
    """Get reminders."""
    conn = db_conn()
    cur = conn.cursor()

    now = dt.datetime.now().isoformat()
    cur.execute("""
        SELECT r.*, p.company
        FROM reminders r
        JOIN prospects p ON r.prospect_id = p.id
        WHERE r.reminded = 0 AND r.date <= ?
        ORDER BY r.date ASC
    """, (now,))

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]
