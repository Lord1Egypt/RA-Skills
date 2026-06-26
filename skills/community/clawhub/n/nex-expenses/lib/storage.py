"""
Nex Expenses - SQLite storage layer
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import stat
import sqlite3
import datetime as dt
from pathlib import Path
from contextlib import contextmanager
from config import (
    DB_PATH,
    DATA_DIR,
    BELGIAN_TAX_CATEGORIES,
    BTW_RATES,
    QUARTERS,
)


def init_db():
    """Create database and tables if they don't exist. Sets secure file permissions."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPTS_DIR = DATA_DIR / "receipts"
    EXPORT_DIR = DATA_DIR / "exports"
    RECEIPTS_DIR.mkdir(exist_ok=True)
    EXPORT_DIR.mkdir(exist_ok=True)

    # Set secure permissions on data directory (Unix-like systems only)
    try:
        os.chmod(str(DATA_DIR), stat.S_IRWXU)
    except (OSError, AttributeError):
        pass  # Windows doesn't support these permission modes

    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS expenses (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                date                TEXT    NOT NULL,
                vendor              TEXT    NOT NULL,
                description         TEXT,
                amount_incl         REAL    NOT NULL,
                amount_excl         REAL    NOT NULL,
                btw_rate            INTEGER,
                btw_amount          REAL,
                tax_category        TEXT    NOT NULL,
                deduction_pct       INTEGER,
                deductible_amount   REAL,
                payment_method      TEXT,
                receipt_path        TEXT,
                receipt_text        TEXT,
                currency            TEXT    DEFAULT 'EUR',
                notes               TEXT,
                tags                TEXT,
                quarterly_period    TEXT,
                year                INTEGER,
                created_at          TEXT    DEFAULT (datetime('now')),
                updated_at          TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS vendors (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                name                TEXT    NOT NULL UNIQUE,
                default_category    TEXT,
                default_btw_rate    INTEGER,
                total_spent         REAL    DEFAULT 0,
                last_used           TEXT,
                created_at          TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS budgets (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                category            TEXT    NOT NULL,
                monthly_limit       REAL    NOT NULL,
                created_at          TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS recurring_expenses (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor              TEXT    NOT NULL,
                description         TEXT,
                amount              REAL    NOT NULL,
                btw_rate            INTEGER,
                tax_category        TEXT    NOT NULL,
                frequency           TEXT    NOT NULL,
                next_date           TEXT    NOT NULL,
                active              INTEGER DEFAULT 1,
                created_at          TEXT    DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_expenses_date
                ON expenses(date);
            CREATE INDEX IF NOT EXISTS idx_expenses_vendor
                ON expenses(vendor);
            CREATE INDEX IF NOT EXISTS idx_expenses_category
                ON expenses(tax_category);
            CREATE INDEX IF NOT EXISTS idx_expenses_quarterly
                ON expenses(quarterly_period);
            CREATE INDEX IF NOT EXISTS idx_expenses_year
                ON expenses(year);
            CREATE INDEX IF NOT EXISTS idx_expenses_tags
                ON expenses(tags);

            CREATE INDEX IF NOT EXISTS idx_vendors_name
                ON vendors(name);

            CREATE UNIQUE INDEX IF NOT EXISTS idx_budgets_category
                ON budgets(category);

            CREATE INDEX IF NOT EXISTS idx_recurring_active
                ON recurring_expenses(active);
        """)
        conn.execute("PRAGMA journal_mode=WAL")
        _init_fts(conn)


def _init_fts(conn):
    """Create FTS5 virtual tables for full-text search if they don't exist."""
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS fts_expenses USING fts5(
            vendor, description, notes, tags,
            content='expenses', content_rowid='id',
            tokenize='porter unicode61'
        )
    """)

    conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS fts_expenses_ai AFTER INSERT ON expenses BEGIN
            INSERT INTO fts_expenses(rowid, vendor, description, notes, tags)
            VALUES (new.id, new.vendor, new.description, new.notes, new.tags);
        END;
        CREATE TRIGGER IF NOT EXISTS fts_expenses_ad AFTER DELETE ON expenses BEGIN
            INSERT INTO fts_expenses(fts_expenses, rowid, vendor, description, notes, tags)
            VALUES ('delete', old.id, old.vendor, old.description, old.notes, old.tags);
        END;
        CREATE TRIGGER IF NOT EXISTS fts_expenses_au AFTER UPDATE ON expenses BEGIN
            INSERT INTO fts_expenses(fts_expenses, rowid, vendor, description, notes, tags)
            VALUES ('delete', old.id, old.vendor, old.description, old.notes, old.tags);
            INSERT INTO fts_expenses(rowid, vendor, description, notes, tags)
            VALUES (new.id, new.vendor, new.description, new.notes, new.tags);
        END;
    """)


def rebuild_fts():
    """Rebuild all FTS indexes from scratch. Call after bulk imports or DB sync."""
    with _connect() as conn:
        _init_fts(conn)
        conn.execute("INSERT INTO fts_expenses(fts_expenses) VALUES ('rebuild')")


@contextmanager
def _connect():
    """Context manager for database connections with Row factory."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _calculate_quarterly_period(date_str):
    """Calculate quarterly period (Q1, Q2, Q3, Q4) from ISO date string."""
    try:
        d = dt.datetime.fromisoformat(date_str)
        month = d.month
        if month <= 3:
            return "Q1"
        elif month <= 6:
            return "Q2"
        elif month <= 9:
            return "Q3"
        else:
            return "Q4"
    except Exception:
        return None


def _calculate_deductible_amount(amount_excl, deduction_pct):
    """Calculate the deductible portion of an expense."""
    if deduction_pct is None:
        return amount_excl
    return round(amount_excl * deduction_pct / 100, 2)


def save_expense(data_dict):
    """
    Save a new expense. Auto-calculates quarterly_period, year, and deductible_amount.
    Updates vendor statistics. Returns expense id.
    """
    with _connect() as conn:
        # Auto-calculate fields
        date_str = data_dict.get("date")
        date_obj = dt.datetime.fromisoformat(date_str) if date_str else dt.datetime.now()
        year = date_obj.year
        quarterly_period = _calculate_quarterly_period(date_str)

        # Get deduction percentage from category
        category = data_dict.get("tax_category")
        deduction_pct = BELGIAN_TAX_CATEGORIES.get(category, {}).get("deduction", 0)

        amount_excl = data_dict.get("amount_excl", 0)
        deductible_amount = _calculate_deductible_amount(amount_excl, deduction_pct)

        # Insert expense
        cursor = conn.execute(
            """INSERT INTO expenses
               (date, vendor, description, amount_incl, amount_excl, btw_rate, btw_amount,
                tax_category, deduction_pct, deductible_amount, payment_method,
                receipt_path, receipt_text, currency, notes, tags, quarterly_period, year)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data_dict.get("date"),
                data_dict.get("vendor"),
                data_dict.get("description"),
                data_dict.get("amount_incl"),
                amount_excl,
                data_dict.get("btw_rate"),
                data_dict.get("btw_amount"),
                category,
                deduction_pct,
                deductible_amount,
                data_dict.get("payment_method"),
                data_dict.get("receipt_path"),
                data_dict.get("receipt_text"),
                data_dict.get("currency", "EUR"),
                data_dict.get("notes"),
                data_dict.get("tags"),
                quarterly_period,
                year,
            ),
        )

        expense_id = cursor.lastrowid

        # Update vendor stats
        vendor_name = data_dict.get("vendor")
        if vendor_name:
            # Insert or update vendor
            conn.execute(
                """INSERT INTO vendors (name, default_category, default_btw_rate, total_spent, last_used)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(name)
                   DO UPDATE SET
                       total_spent = total_spent + ?,
                       last_used = ?""",
                (
                    vendor_name,
                    category,
                    data_dict.get("btw_rate"),
                    data_dict.get("amount_incl", 0),
                    dt.datetime.now().isoformat(),
                    data_dict.get("amount_incl", 0),
                    dt.datetime.now().isoformat(),
                ),
            )

        return expense_id


def get_expense(expense_id):
    """Retrieve a single expense by id. Returns dict or None."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
        return dict(row) if row else None


def list_expenses(since=None, until=None, category=None, vendor=None, quarter=None, year=None, tag=None, limit=100):
    """List expenses with optional filters."""
    with _connect() as conn:
        sql = "SELECT * FROM expenses WHERE 1=1"
        params = []

        if since:
            sql += " AND date >= ?"
            params.append(since)
        if until:
            sql += " AND date < ?"
            params.append(until)
        if category:
            sql += " AND tax_category = ?"
            params.append(category)
        if vendor:
            sql += " AND vendor = ?"
            params.append(vendor)
        if quarter:
            sql += " AND quarterly_period = ?"
            params.append(quarter)
        if year:
            sql += " AND year = ?"
            params.append(year)
        if tag:
            sql += " AND tags LIKE ?"
            params.append(f"%{tag}%")

        sql += " ORDER BY date DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


def update_expense(expense_id, data_dict):
    """Update an existing expense. Auto-recalculates deductible_amount if needed."""
    with _connect() as conn:
        # Prepare fields to update
        updates = []
        params = []

        for key in [
            "date",
            "vendor",
            "description",
            "amount_incl",
            "amount_excl",
            "btw_rate",
            "btw_amount",
            "tax_category",
            "payment_method",
            "receipt_path",
            "receipt_text",
            "currency",
            "notes",
            "tags",
        ]:
            if key in data_dict:
                updates.append(f"{key} = ?")
                params.append(data_dict[key])

        # Recalculate deductible if tax_category or amount_excl changed
        if "tax_category" in data_dict or "amount_excl" in data_dict:
            # Get current values
            row = conn.execute("SELECT tax_category, amount_excl FROM expenses WHERE id = ?", (expense_id,)).fetchone()
            category = data_dict.get("tax_category", row["tax_category"])
            amount_excl = data_dict.get("amount_excl", row["amount_excl"])

            deduction_pct = BELGIAN_TAX_CATEGORIES.get(category, {}).get("deduction", 0)
            deductible_amount = _calculate_deductible_amount(amount_excl, deduction_pct)

            updates.append("deduction_pct = ?")
            params.append(deduction_pct)
            updates.append("deductible_amount = ?")
            params.append(deductible_amount)

        # Recalculate quarterly_period if date changed
        if "date" in data_dict:
            quarterly_period = _calculate_quarterly_period(data_dict["date"])
            year = dt.datetime.fromisoformat(data_dict["date"]).year
            updates.append("quarterly_period = ?")
            params.append(quarterly_period)
            updates.append("year = ?")
            params.append(year)

        if updates:
            updates.append("updated_at = ?")
            params.append(dt.datetime.now().isoformat())
            params.append(expense_id)

            sql = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
            conn.execute(sql, params)


def delete_expense(expense_id):
    """Delete an expense by id."""
    with _connect() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


def search_expenses(query, limit=30):
    """Full-text search across vendor, description, and notes."""
    with _connect() as conn:
        fts_terms = query.strip()

        try:
            rows = conn.execute(
                """SELECT e.* FROM fts_expenses
                   JOIN expenses e ON e.id = fts_expenses.rowid
                   WHERE fts_expenses MATCH ?
                   ORDER BY fts_expenses.rank
                   LIMIT ?""",
                (fts_terms, limit),
            ).fetchall()
            return [dict(r) for r in rows]
        except sqlite3.OperationalError:
            # Fallback to LIKE search
            words = query.split()
            like_clauses = " AND ".join(
                "(vendor LIKE ? OR description LIKE ? OR notes LIKE ?)" for _ in words
            )
            params = []
            for w in words:
                params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])
            params.append(limit)

            sql = f"SELECT * FROM expenses WHERE {like_clauses} ORDER BY date DESC LIMIT ?"
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]


def get_quarterly_summary(year, quarter):
    """Get summary of expenses for a quarter: totals by category, total deductible, BTW reclaimable."""
    with _connect() as conn:
        summary = {
            "year": year,
            "quarter": quarter,
            "by_category": {},
            "total_gross": 0,
            "total_deductible": 0,
            "total_btw_reclaimable": 0,
            "expense_count": 0,
        }

        # Get all expenses for quarter
        rows = conn.execute(
            """SELECT tax_category, amount_incl, deductible_amount, btw_amount
               FROM expenses
               WHERE year = ? AND quarterly_period = ?
               ORDER BY date""",
            (year, quarter),
        ).fetchall()

        for row in rows:
            category = row["tax_category"]
            summary["expense_count"] += 1
            summary["total_gross"] += row["amount_incl"]
            summary["total_deductible"] += row["deductible_amount"] or 0
            summary["total_btw_reclaimable"] += row["btw_amount"] or 0

            if category not in summary["by_category"]:
                summary["by_category"][category] = {
                    "name": BELGIAN_TAX_CATEGORIES.get(category, {}).get("name", category),
                    "count": 0,
                    "total": 0,
                    "deductible": 0,
                }

            summary["by_category"][category]["count"] += 1
            summary["by_category"][category]["total"] += row["amount_incl"]
            summary["by_category"][category]["deductible"] += row["deductible_amount"] or 0

        return summary


def get_yearly_summary(year):
    """Get summary of all expenses for a year."""
    with _connect() as conn:
        summary = {
            "year": year,
            "by_category": {},
            "by_quarter": {},
            "total_gross": 0,
            "total_deductible": 0,
            "total_btw_reclaimable": 0,
            "expense_count": 0,
        }

        rows = conn.execute(
            """SELECT quarterly_period, tax_category, amount_incl, deductible_amount, btw_amount
               FROM expenses
               WHERE year = ?
               ORDER BY date""",
            (year,),
        ).fetchall()

        for row in rows:
            category = row["tax_category"]
            quarter = row["quarterly_period"]

            summary["expense_count"] += 1
            summary["total_gross"] += row["amount_incl"]
            summary["total_deductible"] += row["deductible_amount"] or 0
            summary["total_btw_reclaimable"] += row["btw_amount"] or 0

            # By category
            if category not in summary["by_category"]:
                summary["by_category"][category] = {
                    "name": BELGIAN_TAX_CATEGORIES.get(category, {}).get("name", category),
                    "count": 0,
                    "total": 0,
                    "deductible": 0,
                }

            summary["by_category"][category]["count"] += 1
            summary["by_category"][category]["total"] += row["amount_incl"]
            summary["by_category"][category]["deductible"] += row["deductible_amount"] or 0

            # By quarter
            if quarter not in summary["by_quarter"]:
                summary["by_quarter"][quarter] = {"total": 0, "deductible": 0, "count": 0}

            summary["by_quarter"][quarter]["total"] += row["amount_incl"]
            summary["by_quarter"][quarter]["deductible"] += row["deductible_amount"] or 0
            summary["by_quarter"][quarter]["count"] += 1

        return summary


def get_monthly_summary(year, month):
    """Get summary of expenses for a specific month."""
    with _connect() as conn:
        summary = {
            "year": year,
            "month": month,
            "by_category": {},
            "total_gross": 0,
            "total_deductible": 0,
            "total_btw_reclaimable": 0,
            "expense_count": 0,
        }

        # Construct date range
        if month == 12:
            since = f"{year}-12-01"
            until = f"{year + 1}-01-01"
        else:
            since = f"{year}-{month:02d}-01"
            until = f"{year}-{month + 1:02d}-01"

        rows = conn.execute(
            """SELECT tax_category, amount_incl, deductible_amount, btw_amount
               FROM expenses
               WHERE date >= ? AND date < ?
               ORDER BY date""",
            (since, until),
        ).fetchall()

        for row in rows:
            category = row["tax_category"]
            summary["expense_count"] += 1
            summary["total_gross"] += row["amount_incl"]
            summary["total_deductible"] += row["deductible_amount"] or 0
            summary["total_btw_reclaimable"] += row["btw_amount"] or 0

            if category not in summary["by_category"]:
                summary["by_category"][category] = {
                    "name": BELGIAN_TAX_CATEGORIES.get(category, {}).get("name", category),
                    "count": 0,
                    "total": 0,
                    "deductible": 0,
                }

            summary["by_category"][category]["count"] += 1
            summary["by_category"][category]["total"] += row["amount_incl"]
            summary["by_category"][category]["deductible"] += row["deductible_amount"] or 0

        return summary


def get_category_breakdown(since=None, until=None):
    """Get breakdown of all expenses by category."""
    with _connect() as conn:
        sql = """SELECT tax_category, COUNT(*) as count, SUM(amount_incl) as total,
                        SUM(deductible_amount) as deductible
                 FROM expenses
                 WHERE 1=1"""
        params = []

        if since:
            sql += " AND date >= ?"
            params.append(since)
        if until:
            sql += " AND date < ?"
            params.append(until)

        sql += " GROUP BY tax_category ORDER BY total DESC"

        rows = conn.execute(sql, params).fetchall()
        result = []
        for row in rows:
            category = row["tax_category"]
            result.append(
                {
                    "category": category,
                    "category_name": BELGIAN_TAX_CATEGORIES.get(category, {}).get("name", category),
                    "count": row["count"],
                    "total": row["total"],
                    "deductible": row["deductible"],
                    "deduction_pct": BELGIAN_TAX_CATEGORIES.get(category, {}).get("deduction", 0),
                }
            )
        return result


def get_vendor_stats(limit=20):
    """Get top vendors by total spending."""
    with _connect() as conn:
        rows = conn.execute(
            """SELECT name, total_spent, default_category, default_btw_rate, last_used
               FROM vendors
               ORDER BY total_spent DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def save_vendor(name, default_category=None, default_btw_rate=None):
    """Insert or update a vendor."""
    with _connect() as conn:
        conn.execute(
            """INSERT INTO vendors (name, default_category, default_btw_rate)
               VALUES (?, ?, ?)
               ON CONFLICT(name)
               DO UPDATE SET
                   default_category = COALESCE(?, default_category),
                   default_btw_rate = COALESCE(?, default_btw_rate)""",
            (name, default_category, default_btw_rate, default_category, default_btw_rate),
        )


def get_vendor(name):
    """Get a vendor by name."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM vendors WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None


def export_for_accountant(year, quarter=None):
    """
    Export expenses formatted for accountant with Belgian column headers.
    Returns list of dicts ready for CSV conversion.
    """
    sql = "SELECT * FROM expenses WHERE year = ?"
    params = [year]

    if quarter:
        sql += " AND quarterly_period = ?"
        params.append(quarter)

    sql += " ORDER BY date"

    with _connect() as conn:
        rows = conn.execute(sql, params).fetchall()

    result = []
    for row in rows:
        row_dict = dict(row)
        category = row_dict["tax_category"]
        category_name = BELGIAN_TAX_CATEGORIES.get(category, {}).get("name", category)

        result.append(
            {
                "Datum": row_dict["date"],
                "Leverancier": row_dict["vendor"],
                "Omschrijving": row_dict["description"],
                "Bedrag excl. BTW": row_dict["amount_excl"],
                "BTW %": row_dict["btw_rate"],
                "BTW Bedrag": row_dict["btw_amount"],
                "Bedrag incl. BTW": row_dict["amount_incl"],
                "Belastingcategorie": category_name,
                "Aftrekbaar %": row_dict["deduction_pct"],
                "Aftrekbaar Bedrag": row_dict["deductible_amount"],
                "Betaalmethode": row_dict["payment_method"],
                "Notities": row_dict["notes"],
                "Labels": row_dict["tags"],
            }
        )

    return result


def get_btw_summary(year, quarter=None):
    """
    Get input VAT (BTW) summary for a period, grouped by rate.
    Returns dict with totals by BTW rate for accountant filing.
    """
    sql = "SELECT btw_rate, SUM(btw_amount) as total_btw FROM expenses WHERE year = ?"
    params = [year]

    if quarter:
        sql += " AND quarterly_period = ?"
        params.append(quarter)

    sql += " GROUP BY btw_rate"

    with _connect() as conn:
        rows = conn.execute(sql, params).fetchall()

    result = {
        "year": year,
        "quarter": quarter,
        "by_rate": {},
        "total_reclaimable": 0,
    }

    for row in rows:
        rate = row["btw_rate"]
        total = row["total_btw"]
        result["by_rate"][rate] = {
            "rate_name": BTW_RATES.get(rate, f"{rate}%"),
            "total_btw": total,
        }
        result["total_reclaimable"] += total

    return result
