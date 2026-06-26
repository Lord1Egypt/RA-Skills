"""
Nex Vault - SQLite storage layer
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import stat
import sqlite3
import platform
import datetime as dt
import hashlib
from pathlib import Path
from contextlib import contextmanager
from config import DB_PATH, DATA_DIR, VAULT_DIR


@contextmanager
def _connect():
    """Context manager for database connections."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create database and tables if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_DIR.mkdir(parents=True, exist_ok=True)

    if platform.system() != "Windows":
        os.chmod(str(DATA_DIR), stat.S_IRWXU)
        os.chmod(str(VAULT_DIR), stat.S_IRWXU)

    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                doc_type TEXT NOT NULL,
                file_path TEXT,
                file_hash TEXT UNIQUE,
                party_name TEXT,
                party_contact TEXT,
                start_date TEXT,
                end_date TEXT,
                renewal_date TEXT,
                termination_notice_date TEXT,
                termination_notice_days INTEGER,
                auto_renewal BOOLEAN DEFAULT 0,
                renewal_period TEXT,
                monthly_cost REAL DEFAULT 0,
                yearly_cost REAL DEFAULT 0,
                status TEXT DEFAULT 'active',
                tags TEXT,
                notes TEXT,
                raw_text TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_documents_type
                ON documents(doc_type);
            CREATE INDEX IF NOT EXISTS idx_documents_status
                ON documents(status);
            CREATE INDEX IF NOT EXISTS idx_documents_end_date
                ON documents(end_date);
            CREATE INDEX IF NOT EXISTS idx_documents_party
                ON documents(party_name);

            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                alert_date TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                sent BOOLEAN DEFAULT 0,
                sent_at TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_alerts_document
                ON alerts(document_id);
            CREATE INDEX IF NOT EXISTS idx_alerts_date
                ON alerts(alert_date);
            CREATE INDEX IF NOT EXISTS idx_alerts_sent
                ON alerts(sent);

            CREATE TABLE IF NOT EXISTS key_clauses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                clause_type TEXT NOT NULL,
                content TEXT NOT NULL,
                page_number INTEGER,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_clauses_document
                ON key_clauses(document_id);
            CREATE INDEX IF NOT EXISTS idx_clauses_type
                ON key_clauses(clause_type);

            CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
                name,
                party_name,
                notes,
                raw_text,
                content='documents',
                content_rowid='id'
            );

            CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
                INSERT INTO documents_fts(rowid, name, party_name, notes, raw_text)
                VALUES (new.id, new.name, new.party_name, new.notes, new.raw_text);
            END;

            CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
                DELETE FROM documents_fts WHERE rowid = old.id;
            END;

            CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
                DELETE FROM documents_fts WHERE rowid = old.id;
                INSERT INTO documents_fts(rowid, name, party_name, notes, raw_text)
                VALUES (new.id, new.name, new.party_name, new.notes, new.raw_text);
            END;
        """)


def save_document(name, doc_type, file_path=None, party_name=None, party_contact=None,
                  start_date=None, end_date=None, renewal_date=None,
                  termination_notice_date=None, termination_notice_days=None,
                  auto_renewal=False, renewal_period=None,
                  monthly_cost=0, yearly_cost=0, status='active',
                  tags=None, notes=None, raw_text=None):
    """Save a new document or update existing. Returns document ID."""
    file_hash = None
    if file_path:
        file_hash = _compute_file_hash(file_path)

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO documents (
                name, doc_type, file_path, file_hash, party_name, party_contact,
                start_date, end_date, renewal_date, termination_notice_date,
                termination_notice_days, auto_renewal, renewal_period,
                monthly_cost, yearly_cost, status, tags, notes, raw_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, doc_type, file_path, file_hash, party_name, party_contact,
            start_date, end_date, renewal_date, termination_notice_date,
            termination_notice_days, auto_renewal, renewal_period,
            monthly_cost, yearly_cost, status, tags, notes, raw_text
        ))
        return cursor.lastrowid


def get_document(doc_id):
    """Get a document by ID with all details."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            return None

        # Get associated alerts and clauses
        cursor.execute("SELECT * FROM alerts WHERE document_id = ? ORDER BY alert_date", (doc_id,))
        alerts = cursor.fetchall()

        cursor.execute("SELECT * FROM key_clauses WHERE document_id = ? ORDER BY clause_type", (doc_id,))
        clauses = cursor.fetchall()

        return {
            'document': dict(doc),
            'alerts': [dict(a) for a in alerts],
            'clauses': [dict(c) for c in clauses],
        }


def list_documents(doc_type=None, status=None, party_name=None, expiring_days=None):
    """List documents with optional filters."""
    with _connect() as conn:
        query = "SELECT * FROM documents WHERE 1=1"
        params = []

        if doc_type:
            query += " AND doc_type = ?"
            params.append(doc_type.upper())
        if status:
            query += " AND status = ?"
            params.append(status)
        if party_name:
            query += " AND party_name LIKE ?"
            params.append(f"%{party_name}%")
        if expiring_days is not None:
            today = dt.date.today()
            cutoff = today + dt.timedelta(days=expiring_days)
            query += " AND end_date IS NOT NULL AND end_date <= ?"
            params.append(cutoff.isoformat())

        query += " ORDER BY end_date ASC, name ASC"
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def update_document(doc_id, **kwargs):
    """Update a document's metadata."""
    allowed_fields = {
        'name', 'doc_type', 'party_name', 'party_contact',
        'start_date', 'end_date', 'renewal_date',
        'termination_notice_date', 'termination_notice_days',
        'auto_renewal', 'renewal_period',
        'monthly_cost', 'yearly_cost', 'status', 'tags', 'notes', 'raw_text'
    }
    fields_to_update = {k: v for k, v in kwargs.items() if k in allowed_fields}

    if not fields_to_update:
        return False

    fields_to_update['updated_at'] = dt.datetime.now().isoformat()
    set_clause = ', '.join([f"{k} = ?" for k in fields_to_update.keys()])
    values = list(fields_to_update.values()) + [doc_id]

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE documents SET {set_clause} WHERE id = ?", values)
        return cursor.rowcount > 0


def search_documents(query_text):
    """Full-text search across document names, parties, notes, and content."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.id, d.name, d.doc_type, d.status, d.end_date, d.party_name
            FROM documents d
            JOIN documents_fts fts ON d.id = fts.rowid
            WHERE documents_fts MATCH ?
            ORDER BY rank
            LIMIT 50
        """, (query_text,))
        return [dict(row) for row in cursor.fetchall()]


def get_upcoming_alerts(days=90):
    """Get all upcoming alerts within N days."""
    today = dt.date.today()
    cutoff = (today + dt.timedelta(days=days)).isoformat()

    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, d.name, d.end_date, d.party_name
            FROM alerts a
            JOIN documents d ON a.document_id = d.id
            WHERE a.alert_date <= ? AND a.sent = 0
            ORDER BY a.alert_date ASC
        """, (cutoff,))
        return [dict(row) for row in cursor.fetchall()]


def mark_alert_sent(alert_id):
    """Mark an alert as sent."""
    now = dt.datetime.now().isoformat()
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE alerts SET sent = 1, sent_at = ? WHERE id = ?", (now, alert_id))
        return cursor.rowcount > 0


def get_expiring_documents(days=90):
    """Get documents expiring within N days."""
    return list_documents(expiring_days=days)


def get_document_stats():
    """Get vault statistics."""
    with _connect() as conn:
        cursor = conn.cursor()

        # Total documents
        cursor.execute("SELECT COUNT(*) as count FROM documents")
        total_docs = cursor.fetchone()['count']

        # By type
        cursor.execute("""
            SELECT doc_type, COUNT(*) as count FROM documents GROUP BY doc_type
        """)
        by_type = {row['doc_type']: row['count'] for row in cursor.fetchall()}

        # By status
        cursor.execute("""
            SELECT status, COUNT(*) as count FROM documents GROUP BY status
        """)
        by_status = {row['status']: row['count'] for row in cursor.fetchall()}

        # Cost totals
        cursor.execute("""
            SELECT
                SUM(monthly_cost) as total_monthly,
                SUM(yearly_cost) as total_yearly
            FROM documents WHERE status = 'active'
        """)
        costs = cursor.fetchone()
        total_monthly = costs['total_monthly'] or 0
        total_yearly = costs['total_yearly'] or 0

        # Most common parties
        cursor.execute("""
            SELECT party_name, COUNT(*) as count FROM documents
            WHERE party_name IS NOT NULL
            GROUP BY party_name
            ORDER BY count DESC
            LIMIT 10
        """)
        top_parties = [dict(row) for row in cursor.fetchall()]

        return {
            'total_documents': total_docs,
            'by_type': by_type,
            'by_status': by_status,
            'total_monthly_cost': round(total_monthly, 2),
            'total_yearly_cost': round(total_yearly, 2),
            'top_parties': top_parties,
        }


def save_key_clause(document_id, clause_type, content, page_number=None):
    """Save an extracted key clause."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO key_clauses (document_id, clause_type, content, page_number)
            VALUES (?, ?, ?, ?)
        """, (document_id, clause_type, content, page_number))
        return cursor.lastrowid


def get_key_clauses(document_id, clause_type=None):
    """Get key clauses for a document."""
    with _connect() as conn:
        query = "SELECT * FROM key_clauses WHERE document_id = ?"
        params = [document_id]

        if clause_type:
            query += " AND clause_type = ?"
            params.append(clause_type)

        query += " ORDER BY clause_type, page_number"
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def export_documents(format_type='json'):
    """Export all documents."""
    docs = list_documents()

    if format_type == 'json':
        import json
        return json.dumps(docs, indent=2, default=str)
    elif format_type == 'csv':
        import csv
        import io

        if not docs:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=docs[0].keys())
        writer.writeheader()
        writer.writerows(docs)
        return output.getvalue()

    return ""


def _compute_file_hash(file_path):
    """Compute SHA256 hash of a file."""
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def document_exists_by_hash(file_hash):
    """Check if a document with this file hash already exists."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM documents WHERE file_hash = ?", (file_hash,))
        return cursor.fetchone() is not None
