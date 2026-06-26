"""
Nex E-Invoice - SQLite storage layer
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import stat
import sqlite3
import datetime as dt
from pathlib import Path
from contextlib import contextmanager
from config import DB_PATH, DATA_DIR, EXPORT_DIR


def init_db():
    """Create database and tables if they don't exist. Sets secure file permissions."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Set secure permissions on data directory (Unix-like systems)
    if os.name != "nt":
        os.chmod(str(DATA_DIR), stat.S_IRWXU)
        os.chmod(str(EXPORT_DIR), stat.S_IRWXU)

    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS invoices (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number      TEXT    NOT NULL UNIQUE,
                issue_date          TEXT    NOT NULL,
                due_date            TEXT    NOT NULL,
                seller_vat          TEXT    NOT NULL,
                seller_name         TEXT    NOT NULL,
                buyer_vat           TEXT    NOT NULL,
                buyer_name          TEXT    NOT NULL,
                buyer_street        TEXT,
                buyer_city          TEXT,
                buyer_postcode      TEXT,
                buyer_country       TEXT    DEFAULT 'BE',
                buyer_email         TEXT,
                buyer_kbo           TEXT,
                buyer_peppol_id     TEXT,
                subtotal_excl       REAL    NOT NULL,
                total_btw           REAL    NOT NULL,
                total_incl          REAL    NOT NULL,
                currency            TEXT    DEFAULT 'EUR',
                payment_terms       INTEGER DEFAULT 30,
                payment_reference   TEXT,
                status              TEXT    DEFAULT 'draft',
                xml_path            TEXT,
                notes               TEXT,
                created_at          TEXT    DEFAULT (datetime('now')),
                updated_at          TEXT    DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_invoices_number
                ON invoices(invoice_number);
            CREATE INDEX IF NOT EXISTS idx_invoices_buyer_vat
                ON invoices(buyer_vat);
            CREATE INDEX IF NOT EXISTS idx_invoices_issue_date
                ON invoices(issue_date);
            CREATE INDEX IF NOT EXISTS idx_invoices_status
                ON invoices(status);
            CREATE INDEX IF NOT EXISTS idx_invoices_created_at
                ON invoices(created_at);

            CREATE TABLE IF NOT EXISTS invoice_lines (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id      INTEGER NOT NULL,
                line_number     INTEGER NOT NULL,
                description     TEXT    NOT NULL,
                quantity        REAL    NOT NULL,
                unit_code       TEXT    DEFAULT 'C62',
                unit_price      REAL    NOT NULL,
                btw_rate        INTEGER NOT NULL,
                btw_amount      REAL    NOT NULL,
                line_total      REAL    NOT NULL,
                created_at      TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_invoice_lines_invoice_id
                ON invoice_lines(invoice_id);

            CREATE TABLE IF NOT EXISTS contacts (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT    NOT NULL,
                vat_number      TEXT    UNIQUE,
                kbo_number      TEXT,
                street          TEXT,
                city            TEXT,
                postcode        TEXT,
                country         TEXT    DEFAULT 'BE',
                email           TEXT,
                phone           TEXT,
                peppol_id       TEXT,
                iban            TEXT,
                bic             TEXT,
                notes           TEXT,
                created_at      TEXT    DEFAULT (datetime('now')),
                updated_at      TEXT    DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_contacts_vat
                ON contacts(vat_number);
            CREATE INDEX IF NOT EXISTS idx_contacts_name
                ON contacts(name);

            CREATE TABLE IF NOT EXISTS sequences (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                prefix          TEXT    NOT NULL,
                current_number  INTEGER DEFAULT 0,
                year            INTEGER NOT NULL,
                UNIQUE (prefix, year)
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS fts_invoices USING fts5(
                invoice_number, buyer_name, buyer_email,
                content='invoices', content_rowid='id',
                tokenize='porter unicode61'
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS fts_lines USING fts5(
                description, content='invoice_lines',
                content_rowid='id', tokenize='porter unicode61'
            );
        """)
        conn.execute("PRAGMA journal_mode=WAL")
        _init_fts_triggers(conn)


def _init_fts_triggers(conn):
    """Create FTS triggers to keep search indexes in sync."""
    conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS fts_invoices_ai AFTER INSERT ON invoices BEGIN
            INSERT INTO fts_invoices(rowid, invoice_number, buyer_name, buyer_email)
            VALUES (new.id, new.invoice_number, new.buyer_name, new.buyer_email);
        END;

        CREATE TRIGGER IF NOT EXISTS fts_invoices_ad AFTER DELETE ON invoices BEGIN
            INSERT INTO fts_invoices(fts_invoices, rowid, invoice_number, buyer_name, buyer_email)
            VALUES ('delete', old.id, old.invoice_number, old.buyer_name, old.buyer_email);
        END;

        CREATE TRIGGER IF NOT EXISTS fts_invoices_au AFTER UPDATE ON invoices BEGIN
            INSERT INTO fts_invoices(fts_invoices, rowid, invoice_number, buyer_name, buyer_email)
            VALUES ('delete', old.id, old.invoice_number, old.buyer_name, old.buyer_email);
            INSERT INTO fts_invoices(rowid, invoice_number, buyer_name, buyer_email)
            VALUES (new.id, new.invoice_number, new.buyer_name, new.buyer_email);
        END;

        CREATE TRIGGER IF NOT EXISTS fts_lines_ai AFTER INSERT ON invoice_lines BEGIN
            INSERT INTO fts_lines(rowid, description)
            VALUES (new.id, new.description);
        END;

        CREATE TRIGGER IF NOT EXISTS fts_lines_ad AFTER DELETE ON invoice_lines BEGIN
            INSERT INTO fts_lines(fts_lines, rowid, description)
            VALUES ('delete', old.id, old.description);
        END;

        CREATE TRIGGER IF NOT EXISTS fts_lines_au AFTER UPDATE ON invoice_lines BEGIN
            INSERT INTO fts_lines(fts_lines, rowid, description)
            VALUES ('delete', old.id, old.description);
            INSERT INTO fts_lines(rowid, description)
            VALUES (new.id, new.description);
        END;
    """)


@contextmanager
def _connect():
    """Context manager for database connections with row factory."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def next_invoice_number(prefix=None):
    """Generate next sequential invoice number (e.g., INV-2026-0001). Auto-resets yearly."""
    if prefix is None:
        from config import INVOICE_PREFIX
        prefix = INVOICE_PREFIX

    now = dt.datetime.now()
    year = now.year

    with _connect() as conn:
        row = conn.execute(
            "SELECT current_number FROM sequences WHERE prefix = ? AND year = ?",
            (prefix, year),
        ).fetchone()

        if row:
            current = row["current_number"] + 1
            conn.execute(
                "UPDATE sequences SET current_number = ? WHERE prefix = ? AND year = ?",
                (current, prefix, year),
            )
        else:
            current = 1
            conn.execute(
                "INSERT INTO sequences (prefix, current_number, year) VALUES (?, ?, ?)",
                (prefix, current, year),
            )

    return f"{prefix}-{year}-{current:04d}"


def save_invoice(data):
    """Insert invoice with line items. Returns invoice_id."""
    with _connect() as conn:
        # Insert invoice header
        invoice_data = {k: v for k, v in data.items() if k != "lines"}
        cols = ", ".join(invoice_data.keys())
        placeholders = ", ".join("?" * len(invoice_data))

        cursor = conn.execute(
            f"INSERT INTO invoices ({cols}) VALUES ({placeholders})",
            tuple(invoice_data.values()),
        )
        invoice_id = cursor.lastrowid

        # Insert line items
        if data.get("lines"):
            for line_idx, line in enumerate(data["lines"], start=1):
                line["invoice_id"] = invoice_id
                line["line_number"] = line_idx
                line_cols = ", ".join(line.keys())
                line_placeholders = ", ".join("?" * len(line))
                conn.execute(
                    f"INSERT INTO invoice_lines ({line_cols}) VALUES ({line_placeholders})",
                    tuple(line.values()),
                )

        return invoice_id


def get_invoice(invoice_number):
    """Fetch invoice header and all line items by invoice number."""
    with _connect() as conn:
        invoice_row = conn.execute(
            "SELECT * FROM invoices WHERE invoice_number = ?", (invoice_number,)
        ).fetchone()

        if not invoice_row:
            return None

        invoice = dict(invoice_row)

        lines_rows = conn.execute(
            "SELECT * FROM invoice_lines WHERE invoice_id = ? ORDER BY line_number",
            (invoice["id"],),
        ).fetchall()

        invoice["lines"] = [dict(r) for r in lines_rows]
        return invoice


def list_invoices(status=None, since=None, until=None, buyer=None, limit=50):
    """List invoices with optional filters. Returns list of invoice summaries."""
    with _connect() as conn:
        sql = "SELECT * FROM invoices WHERE 1=1"
        params = []

        if status:
            sql += " AND status = ?"
            params.append(status)
        if since:
            sql += " AND issue_date >= ?"
            params.append(since)
        if until:
            sql += " AND issue_date < ?"
            params.append(until)
        if buyer:
            sql += " AND (buyer_name LIKE ? OR buyer_vat LIKE ?)"
            buyer_pattern = f"%{buyer}%"
            params.extend([buyer_pattern, buyer_pattern])

        sql += " ORDER BY issue_date DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


def update_invoice_status(invoice_number, status):
    """Update invoice status (draft/sent/paid/cancelled) and updated_at timestamp."""
    with _connect() as conn:
        conn.execute(
            "UPDATE invoices SET status = ?, updated_at = datetime('now') WHERE invoice_number = ?",
            (status, invoice_number),
        )


def save_contact(data):
    """Upsert contact by vat_number. Returns contact_id."""
    with _connect() as conn:
        vat_number = data.get("vat_number")

        if vat_number:
            # Check if exists
            existing = conn.execute(
                "SELECT id FROM contacts WHERE vat_number = ?", (vat_number,)
            ).fetchone()

            if existing:
                # Update
                contact_id = existing["id"]
                updates = []
                params = []
                for k, v in data.items():
                    if k != "id":
                        updates.append(f"{k} = ?")
                        params.append(v)
                params.append(contact_id)
                if updates:
                    sql = f"UPDATE contacts SET {', '.join(updates)}, updated_at = datetime('now') WHERE id = ?"
                    conn.execute(sql, params)
            else:
                # Insert
                cols = ", ".join(data.keys())
                placeholders = ", ".join("?" * len(data))
                cursor = conn.execute(
                    f"INSERT INTO contacts ({cols}) VALUES ({placeholders})",
                    tuple(data.values()),
                )
                contact_id = cursor.lastrowid
        else:
            # Insert without vat_number
            cols = ", ".join(data.keys())
            placeholders = ", ".join("?" * len(data))
            cursor = conn.execute(
                f"INSERT INTO contacts ({cols}) VALUES ({placeholders})",
                tuple(data.values()),
            )
            contact_id = cursor.lastrowid

        return contact_id


def get_contact(vat_number):
    """Lookup contact by VAT number."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM contacts WHERE vat_number = ?", (vat_number,)
        ).fetchone()
        return dict(row) if row else None


def list_contacts(search=None, limit=50):
    """List all contacts with optional name/email search."""
    with _connect() as conn:
        sql = "SELECT * FROM contacts WHERE 1=1"
        params = []

        if search:
            sql += " AND (name LIKE ? OR email LIKE ? OR vat_number LIKE ?)"
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern, search_pattern])

        sql += " ORDER BY name LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


def get_invoice_stats(year=None):
    """Get invoice statistics: total invoiced, total BTW, count by status."""
    if year is None:
        year = dt.datetime.now().year

    with _connect() as conn:
        year_start = f"{year}-01-01"
        year_end = f"{year + 1}-01-01"

        # Total by status
        status_rows = conn.execute(
            """SELECT status, COUNT(*) as count, SUM(total_incl) as total
               FROM invoices
               WHERE issue_date >= ? AND issue_date < ?
               GROUP BY status""",
            (year_start, year_end),
        ).fetchall()

        stats = {
            "year": year,
            "by_status": {},
            "total_invoiced": 0.0,
            "total_btw": 0.0,
            "invoice_count": 0,
        }

        for row in status_rows:
            status = row["status"]
            count = row["count"]
            total = row["total"] or 0.0
            stats["by_status"][status] = {"count": count, "total": total}
            stats["total_invoiced"] += total

        # Total BTW
        btw_row = conn.execute(
            """SELECT SUM(total_btw) as total_btw, COUNT(*) as invoice_count
               FROM invoices
               WHERE issue_date >= ? AND issue_date < ?""",
            (year_start, year_end),
        ).fetchone()

        if btw_row:
            stats["total_btw"] = btw_row["total_btw"] or 0.0
            stats["invoice_count"] = btw_row["invoice_count"] or 0

        return stats


def search_invoices(query, limit=30):
    """Full-text search across invoice numbers, buyer names, line descriptions."""
    with _connect() as conn:
        fts_terms = query.strip()

        # Search invoices
        sql_invoices = """
            SELECT i.id, i.invoice_number, i.buyer_name, i.buyer_vat,
                   i.issue_date, i.total_incl, i.status,
                   fts_invoices.rank as fts_rank
            FROM fts_invoices
            JOIN invoices i ON i.id = fts_invoices.rowid
            WHERE fts_invoices MATCH ?
            ORDER BY fts_invoices.rank
            LIMIT ?
        """

        try:
            invoice_rows = conn.execute(sql_invoices, (fts_terms, limit)).fetchall()
            results = [dict(r) for r in invoice_rows]

            # Also search line descriptions
            sql_lines = """
                SELECT DISTINCT i.id, i.invoice_number, i.buyer_name,
                       i.issue_date, i.total_incl, i.status,
                       GROUP_CONCAT(l.description, ' | ') as matched_lines
                FROM fts_lines
                JOIN invoice_lines l ON l.id = fts_lines.rowid
                JOIN invoices i ON i.id = l.invoice_id
                WHERE fts_lines MATCH ?
                GROUP BY i.id
                LIMIT ?
            """

            line_rows = conn.execute(sql_lines, (fts_terms, limit)).fetchall()

            # Deduplicate and merge results
            result_dict = {r["id"]: r for r in results}
            for row in line_rows:
                row_dict = dict(row)
                if row_dict["id"] not in result_dict:
                    result_dict[row_dict["id"]] = row_dict
                else:
                    # Merge line matches
                    if "matched_lines" in row_dict:
                        result_dict[row_dict["id"]]["matched_lines"] = row_dict[
                            "matched_lines"
                        ]

            return list(result_dict.values())[:limit]

        except sqlite3.OperationalError:
            # FTS not populated, fallback to LIKE
            return _fallback_search_invoices(query, limit)


def _fallback_search_invoices(query, limit=30):
    """Fallback LIKE-based search when FTS not available."""
    with _connect() as conn:
        words = query.split()
        like_clauses = " OR ".join(
            "(i.invoice_number LIKE ? OR i.buyer_name LIKE ? OR l.description LIKE ?)"
            for _ in words
        )
        params = []
        for w in words:
            pattern = f"%{w}%"
            params.extend([pattern, pattern, pattern])

        sql = f"""
            SELECT DISTINCT i.id, i.invoice_number, i.buyer_name, i.buyer_vat,
                   i.issue_date, i.total_incl, i.status
            FROM invoices i
            LEFT JOIN invoice_lines l ON i.id = l.invoice_id
            WHERE {like_clauses}
            ORDER BY i.issue_date DESC
            LIMIT ?
        """
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
