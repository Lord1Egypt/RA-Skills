#!/usr/bin/env python3
"""money_tracker helper backed by SQLite."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from contextlib import closing
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

MIN_PYTHON = (3, 9)
DEFAULT_DB_ENV = "MONEY_TRACKER_DB"
LEGACY_DB_ENV = "LOCAL_BOOKKEEPING_DB"
DEFAULT_DB_DIR = ".money_tracker"
LEGACY_DB_DIR = ".local-bookkeeping"
DEFAULT_DB_NAME = "bookkeeping.db"
DEFAULT_UNCATEGORIZED = "\u672a\u5206\u7c7b"
DEFAULT_UNSPECIFIED_ACCOUNT = "\u672a\u6307\u5b9a\u8d26\u6237"
DEFAULT_CURRENCY = "CNY"
ACCOUNT_NAME_ALIASES = {
    "alipay": "\u652f\u4ed8\u5b9d",
    "\u652f\u4ed8\u5b9d": "\u652f\u4ed8\u5b9d",
    "wechat": "\u5fae\u4fe1",
    "weixin": "\u5fae\u4fe1",
    "\u5fae\u4fe1": "\u5fae\u4fe1",
    "bank_card": "\u94f6\u884c\u5361",
    "bankcard": "\u94f6\u884c\u5361",
    "\u94f6\u884c\u5361": "\u94f6\u884c\u5361",
    "credit_card": "\u4fe1\u7528\u5361",
    "creditcard": "\u4fe1\u7528\u5361",
    "\u4fe1\u7528\u5361": "\u4fe1\u7528\u5361",
    "cash": "\u73b0\u91d1",
    "\u73b0\u91d1": "\u73b0\u91d1",
}
CURRENCY_ALIASES = {
    "cny": "CNY",
    "rmb": "CNY",
    "\u4eba\u6c11\u5e01": "CNY",
    "\u5143": "CNY",
    "usd": "USD",
    "\u7f8e\u5143": "USD",
    "\u7f8e\u91d1": "USD",
    "eur": "EUR",
    "\u6b27\u5143": "EUR",
}
DEFAULT_ACCOUNT_SPECS = [
    ("\u652f\u4ed8\u5b9d", "CNY"),
    ("\u5fae\u4fe1", "CNY"),
    ("\u94f6\u884c\u5361", "CNY"),
    ("\u94f6\u884c\u5361", "USD"),
    ("\u94f6\u884c\u5361", "EUR"),
]
DEFAULT_ACCOUNT_CURRENCY_BY_NAME = {
    "\u652f\u4ed8\u5b9d": "CNY",
    "\u5fae\u4fe1": "CNY",
    "\u94f6\u884c\u5361": "CNY",
    "\u4fe1\u7528\u5361": "CNY",
    "\u73b0\u91d1": "CNY",
}
RECURRING_FREQUENCIES = {"weekly", "monthly", "yearly"}


def fail(message, exit_code=1, **extra):
    payload = {"ok": False, "error": message}
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_db_path(raw_path):
    candidate = raw_path or os.environ.get(DEFAULT_DB_ENV) or os.environ.get(LEGACY_DB_ENV)
    if candidate:
        return Path(candidate).expanduser().resolve()
    default_path = (Path.home() / DEFAULT_DB_DIR / DEFAULT_DB_NAME).resolve()
    legacy_path = (Path.home() / LEGACY_DB_DIR / DEFAULT_DB_NAME).resolve()
    if default_path.exists() or not legacy_path.exists():
        return default_path
    return legacy_path


def connect_db(db_path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    ensure_schema(conn)
    return conn


def ensure_schema(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            currency TEXT NOT NULL DEFAULT 'CNY',
            is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE (name, currency)
        );

        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_type TEXT NOT NULL CHECK (entry_type IN ('expense', 'income')),
            amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
            currency TEXT NOT NULL DEFAULT 'CNY',
            category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
            category_name_snapshot TEXT NOT NULL,
            account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL,
            account_name_snapshot TEXT NOT NULL DEFAULT '未指定账户',
            description TEXT NOT NULL,
            note TEXT,
            occurred_on TEXT NOT NULL,
            source_text TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS recurring_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_type TEXT NOT NULL CHECK (entry_type IN ('expense', 'income')),
            amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
            currency TEXT NOT NULL DEFAULT 'CNY',
            category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
            category_name_snapshot TEXT NOT NULL,
            account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL,
            account_name_snapshot TEXT NOT NULL DEFAULT '未指定账户',
            description TEXT NOT NULL,
            note TEXT,
            frequency TEXT NOT NULL CHECK (frequency IN ('weekly', 'monthly', 'yearly')),
            interval_count INTEGER NOT NULL DEFAULT 1 CHECK (interval_count > 0),
            next_due_on TEXT NOT NULL,
            source_text TEXT,
            is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_entries_occurred_on ON entries (occurred_on);
        CREATE INDEX IF NOT EXISTS idx_entries_type_date ON entries (entry_type, occurred_on);
        CREATE INDEX IF NOT EXISTS idx_entries_category_snapshot ON entries (category_name_snapshot);
        CREATE INDEX IF NOT EXISTS idx_entries_account_snapshot ON entries (account_name_snapshot);
        CREATE INDEX IF NOT EXISTS idx_entries_currency ON entries (currency);
        CREATE INDEX IF NOT EXISTS idx_recurring_next_due_on ON recurring_transactions (next_due_on);
        CREATE INDEX IF NOT EXISTS idx_recurring_is_active ON recurring_transactions (is_active);
        CREATE INDEX IF NOT EXISTS idx_recurring_category_snapshot ON recurring_transactions (category_name_snapshot);
        CREATE INDEX IF NOT EXISTS idx_recurring_account_snapshot ON recurring_transactions (account_name_snapshot);
        CREATE INDEX IF NOT EXISTS idx_recurring_currency ON recurring_transactions (currency);
        """
    )
    migrate_accounts_table(conn)
    ensure_column_exists(
        conn,
        "entries",
        "account_id",
        "INTEGER REFERENCES accounts(id) ON DELETE SET NULL",
    )
    ensure_column_exists(
        conn,
        "entries",
        "account_name_snapshot",
        "TEXT NOT NULL DEFAULT '未指定账户'",
    )
    ensure_column_exists(
        conn,
        "recurring_transactions",
        "account_id",
        "INTEGER REFERENCES accounts(id) ON DELETE SET NULL",
    )
    ensure_column_exists(
        conn,
        "recurring_transactions",
        "account_name_snapshot",
        "TEXT NOT NULL DEFAULT '未指定账户'",
    )
    ensure_default_accounts(conn)
    sync_account_snapshots(conn)
    conn.commit()


def table_columns(conn, table_name):
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()}


def table_sql(conn, table_name):
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row["sql"] if row else None


def ensure_column_exists(conn, table_name, column_name, column_definition):
    if column_name in table_columns(conn, table_name):
        return
    conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")


def migrate_accounts_table(conn):
    columns = table_columns(conn, "accounts")
    schema_sql = table_sql(conn, "accounts") or ""
    compact_sql = "".join(schema_sql.lower().split())
    requires_migration = "currency" not in columns or "unique(name,currency)" not in compact_sql
    if not requires_migration:
        return

    legacy_rows = conn.execute("SELECT * FROM accounts ORDER BY sort_order ASC, id ASC").fetchall()
    now = utc_now()
    normalized_rows = []
    for row in legacy_rows:
        name = normalize_account_base_name(row["name"], allow_default=False)
        currency = (
            normalize_currency(row["currency"], default=None, allow_none=True)
            if "currency" in columns
            else None
        )
        if currency is None:
            currency = DEFAULT_ACCOUNT_CURRENCY_BY_NAME.get(name, DEFAULT_CURRENCY)
        normalized_rows.append(
            {
                "id": row["id"],
                "name": name,
                "currency": currency,
                "is_active": row["is_active"],
                "sort_order": row["sort_order"],
                "created_at": row["created_at"] or now,
                "updated_at": row["updated_at"] or now,
            }
        )

    conn.commit()
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("ALTER TABLE accounts RENAME TO accounts_legacy")
    conn.execute(
        """
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            currency TEXT NOT NULL DEFAULT 'CNY',
            is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE (name, currency)
        )
        """
    )
    for row in normalized_rows:
        conn.execute(
            """
            INSERT INTO accounts (id, name, currency, is_active, sort_order, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["name"],
                row["currency"],
                row["is_active"],
                row["sort_order"],
                row["created_at"],
                row["updated_at"],
            ),
        )
    conn.execute("DROP TABLE accounts_legacy")
    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON")


def ensure_default_accounts(conn):
    existing_count = conn.execute("SELECT COUNT(*) AS count FROM accounts").fetchone()["count"]
    if existing_count:
        return
    now = utc_now()
    for index, (name, currency) in enumerate(DEFAULT_ACCOUNT_SPECS):
        conn.execute(
            """
            INSERT INTO accounts (name, currency, is_active, sort_order, created_at, updated_at)
            VALUES (?, ?, 1, ?, ?, ?)
            """,
            (name, currency, index, now, now),
        )


def sync_account_snapshots(conn):
    accounts = conn.execute("SELECT id, name, currency FROM accounts").fetchall()
    for row in accounts:
        label = build_account_label(row["name"], row["currency"])
        conn.execute("UPDATE entries SET account_name_snapshot = ? WHERE account_id = ?", (label, row["id"]))
        conn.execute(
            "UPDATE recurring_transactions SET account_name_snapshot = ? WHERE account_id = ?",
            (label, row["id"]),
        )


def get_db_counts(conn):
    category_count = conn.execute("SELECT COUNT(*) AS count FROM categories WHERE is_active = 1").fetchone()["count"]
    account_count = conn.execute("SELECT COUNT(*) AS count FROM accounts WHERE is_active = 1").fetchone()["count"]
    entry_count = conn.execute("SELECT COUNT(*) AS count FROM entries").fetchone()["count"]
    recurring_count = conn.execute("SELECT COUNT(*) AS count FROM recurring_transactions WHERE is_active = 1").fetchone()[
        "count"
    ]
    return {
        "active_category_count": category_count,
        "active_account_count": account_count,
        "entry_count": entry_count,
        "active_recurring_transaction_count": recurring_count,
    }


def normalize_names(names):
    cleaned = []
    seen = set()
    for raw_name in names:
        name = raw_name.strip()
        if not name:
            continue
        if name not in seen:
            cleaned.append(name)
            seen.add(name)
    if not cleaned:
        fail("At least one non-empty category name is required.")
    return cleaned


def normalize_currency(raw_currency, default=DEFAULT_CURRENCY, allow_none=False):
    if raw_currency is None:
        if allow_none:
            return None
        return default
    candidate = raw_currency.strip()
    if not candidate:
        if allow_none:
            return None
        return default
    normalized_key = candidate.lower().replace("-", "").replace("_", "").replace(" ", "")
    alias = CURRENCY_ALIASES.get(normalized_key)
    if alias:
        return alias
    if candidate.isalpha() and 3 <= len(candidate) <= 10:
        return candidate.upper()
    fail("Invalid currency.", provided_currency=raw_currency)


def build_account_label(account_name, currency):
    if account_name == DEFAULT_UNSPECIFIED_ACCOUNT or not currency:
        return account_name
    return f"{account_name} ({currency})"


def normalize_account_base_name(raw_name, allow_default=True):
    if raw_name is None:
        return DEFAULT_UNSPECIFIED_ACCOUNT if allow_default else fail("Account name is required.")
    candidate = raw_name.strip()
    if not candidate:
        return DEFAULT_UNSPECIFIED_ACCOUNT if allow_default else fail("Account name is required.")
    if allow_default and candidate == DEFAULT_UNSPECIFIED_ACCOUNT:
        return DEFAULT_UNSPECIFIED_ACCOUNT
    normalized_key = candidate.lower().replace("-", "_").replace(" ", "_")
    canonical = ACCOUNT_NAME_ALIASES.get(normalized_key)
    if canonical:
        return canonical
    return candidate


def split_account_spec(raw_account):
    candidate = raw_account.strip()
    for separator in (":", "@"):
        if separator in candidate:
            name_part, currency_part = candidate.rsplit(separator, 1)
            return name_part.strip(), currency_part.strip()
    return candidate, None


def parse_account_spec(raw_account, default_currency=None, allow_default=True):
    if raw_account is None:
        if allow_default:
            return {
                "name": DEFAULT_UNSPECIFIED_ACCOUNT,
                "currency": None,
                "label": DEFAULT_UNSPECIFIED_ACCOUNT,
                "raw": None,
            }
        fail("Account name is required.")

    candidate = raw_account.strip()
    if not candidate:
        if allow_default:
            return {
                "name": DEFAULT_UNSPECIFIED_ACCOUNT,
                "currency": None,
                "label": DEFAULT_UNSPECIFIED_ACCOUNT,
                "raw": raw_account,
            }
        fail("Account name is required.")

    if allow_default and candidate == DEFAULT_UNSPECIFIED_ACCOUNT:
        return {
            "name": DEFAULT_UNSPECIFIED_ACCOUNT,
            "currency": None,
            "label": DEFAULT_UNSPECIFIED_ACCOUNT,
            "raw": raw_account,
        }

    name_part, currency_part = split_account_spec(candidate)
    account_name = normalize_account_base_name(name_part, allow_default=False)
    currency = normalize_currency(currency_part, default=None, allow_none=True)
    if currency is None and default_currency is not None:
        currency = normalize_currency(default_currency, default=None, allow_none=False)
    if currency is None:
        currency = DEFAULT_ACCOUNT_CURRENCY_BY_NAME.get(account_name)
    return {
        "name": account_name,
        "currency": currency,
        "label": build_account_label(account_name, currency) if currency else account_name,
        "raw": raw_account,
    }


def normalize_account_specs(names):
    cleaned = []
    seen = set()
    for raw_name in names:
        spec = parse_account_spec(raw_name, allow_default=False)
        if spec["currency"] is None:
            fail(
                "Account currency is required. Use a wallet name with a currency, for example 支付宝:CNY or 银行卡:USD.",
                provided_account=raw_name,
            )
        key = (spec["name"], spec["currency"])
        if key not in seen:
            cleaned.append(spec)
            seen.add(key)
    if not cleaned:
        fail("At least one account name is required.")
    return cleaned


def parse_positive_int(raw_value, field_name):
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        fail(f"Invalid {field_name}.", provided=raw_value)
    if value <= 0:
        fail(f"{field_name.replace('_', ' ').capitalize()} must be greater than zero.", provided=raw_value)
    return value


def parse_amount_to_cents(raw_amount):
    try:
        amount = Decimal(str(raw_amount))
    except InvalidOperation:
        fail("Invalid amount.", provided=raw_amount)
    if amount <= 0:
        fail("Amount must be greater than zero.", provided=raw_amount)
    normalized = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int((normalized * 100).to_integral_value(rounding=ROUND_HALF_UP))


def cents_to_amount(cents):
    return format((Decimal(cents) / Decimal(100)).quantize(Decimal("0.01")), "f")


def parse_iso_date(raw_date):
    try:
        return date.fromisoformat(raw_date)
    except ValueError:
        fail("Invalid date. Expected YYYY-MM-DD.", provided=raw_date)


def normalize_month(raw_month):
    if not raw_month:
        today = date.today()
        return f"{today.year:04d}-{today.month:02d}"
    parts = raw_month.split("-")
    if len(parts) != 2:
        fail("Invalid month. Expected YYYY-MM.", provided=raw_month)
    try:
        year = int(parts[0])
        month = int(parts[1])
    except ValueError:
        fail("Invalid month. Expected YYYY-MM.", provided=raw_month)
    if year < 1 or not 1 <= month <= 12:
        fail("Invalid month. Expected YYYY-MM.", provided=raw_month)
    return f"{year:04d}-{month:02d}"


def normalize_year(raw_year):
    if not raw_year:
        return f"{date.today().year:04d}"
    try:
        year = int(raw_year)
    except ValueError:
        fail("Invalid year. Expected YYYY.", provided=raw_year)
    if year < 1:
        fail("Invalid year. Expected YYYY.", provided=raw_year)
    return f"{year:04d}"


def normalize_week(raw_week):
    if not raw_week:
        today = date.today()
        iso_year, iso_week, _ = today.isocalendar()
        return f"{iso_year:04d}-W{iso_week:02d}"
    if "-W" not in raw_week:
        fail("Invalid week. Expected YYYY-Www.", provided=raw_week)
    year_part, week_part = raw_week.split("-W", 1)
    try:
        year = int(year_part)
        week = int(week_part)
        date.fromisocalendar(year, week, 1)
    except ValueError:
        fail("Invalid week. Expected YYYY-Www.", provided=raw_week)
    return f"{year:04d}-W{week:02d}"


def day_bounds(date_value):
    normalized = parse_iso_date(date_value).isoformat() if date_value else date.today().isoformat()
    start = date.fromisoformat(normalized)
    end = start + timedelta(days=1)
    return normalized, start.isoformat(), end.isoformat()


def month_bounds(month_value):
    normalized = normalize_month(month_value)
    year, month = (int(part) for part in normalized.split("-"))
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    return normalized, start.isoformat(), end.isoformat()


def week_bounds(week_value=None, date_value=None):
    if week_value and date_value:
        fail("Provide only one of --week or --date when selecting a week.", week=week_value, date=date_value)
    if week_value:
        normalized = normalize_week(week_value)
        year_part, week_part = normalized.split("-W", 1)
        start = date.fromisocalendar(int(year_part), int(week_part), 1)
    else:
        reference = parse_iso_date(date_value) if date_value else date.today()
        iso_year, iso_week, _ = reference.isocalendar()
        normalized = f"{iso_year:04d}-W{iso_week:02d}"
        start = reference - timedelta(days=reference.weekday())
    end = start + timedelta(days=7)
    return normalized, start.isoformat(), end.isoformat()


def year_bounds(year_value):
    normalized = normalize_year(year_value)
    year = int(normalized)
    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    return normalized, start.isoformat(), end.isoformat()


def select_transaction_period(args):
    if args.date:
        period_type = "date"
        period_value, start_date, end_date = day_bounds(args.date)
    elif args.week:
        period_type = "week"
        period_value, start_date, end_date = week_bounds(week_value=args.week)
    elif args.year:
        period_type = "year"
        period_value, start_date, end_date = year_bounds(args.year)
    else:
        period_type = "month"
        period_value, start_date, end_date = month_bounds(args.month)
    return period_type, period_value, start_date, end_date


def build_period_metadata(period_type, period_value):
    return {
        "period_type": period_type,
        "period_value": period_value,
        period_type: period_value,
    }


def list_categories_rows(conn, include_inactive=False):
    if include_inactive:
        query = """
            SELECT id, name, is_active, sort_order, created_at, updated_at
            FROM categories
            ORDER BY sort_order ASC, id ASC
        """
        return conn.execute(query).fetchall()
    query = """
        SELECT id, name, is_active, sort_order, created_at, updated_at
        FROM categories
        WHERE is_active = 1
        ORDER BY sort_order ASC, id ASC
    """
    return conn.execute(query).fetchall()


def active_category_names(conn):
    return [row["name"] for row in list_categories_rows(conn, include_inactive=False)]


def list_accounts_rows(conn, include_inactive=False):
    if include_inactive:
        query = """
            SELECT id, name, currency, is_active, sort_order, created_at, updated_at
            FROM accounts
            ORDER BY sort_order ASC, name ASC, currency ASC, id ASC
        """
        return conn.execute(query).fetchall()
    query = """
        SELECT id, name, currency, is_active, sort_order, created_at, updated_at
        FROM accounts
        WHERE is_active = 1
        ORDER BY sort_order ASC, name ASC, currency ASC, id ASC
    """
    return conn.execute(query).fetchall()


def active_account_labels(conn):
    return [build_account_label(row["name"], row["currency"]) for row in list_accounts_rows(conn, include_inactive=False)]


def resolve_category(conn, category_name):
    snapshot = category_name.strip() if category_name and category_name.strip() else DEFAULT_UNCATEGORIZED
    row = conn.execute(
        """
        SELECT id, name
        FROM categories
        WHERE name = ? AND is_active = 1
        """,
        (snapshot,),
    ).fetchone()
    if row:
        return row["id"], row["name"], True
    return None, snapshot, False


def fetch_accounts_by_name(conn, account_name, include_inactive=False):
    query = """
        SELECT id, name, currency, is_active, sort_order, created_at, updated_at
        FROM accounts
        WHERE name = ?
    """
    params = [account_name]
    if not include_inactive:
        query += " AND is_active = 1"
    query += " ORDER BY sort_order ASC, currency ASC, id ASC"
    return conn.execute(query, params).fetchall()


def fetch_account(conn, account_name, currency, include_inactive=False):
    query = """
        SELECT id, name, currency, is_active, sort_order, created_at, updated_at
        FROM accounts
        WHERE name = ? AND currency = ?
    """
    params = [account_name, currency]
    if not include_inactive:
        query += " AND is_active = 1"
    return conn.execute(query, params).fetchone()


def fetch_account_by_id(conn, account_id, include_inactive=True):
    query = """
        SELECT id, name, currency, is_active, sort_order, created_at, updated_at
        FROM accounts
        WHERE id = ?
    """
    params = [account_id]
    if not include_inactive:
        query += " AND is_active = 1"
    return conn.execute(query, params).fetchone()


def resolve_existing_account_row(conn, raw_account):
    if raw_account is None:
        fail("Account name is required.")
    candidate = raw_account.strip()
    if not candidate:
        fail("Account name is required.")

    name_part, currency_part = split_account_spec(candidate)
    account_name = normalize_account_base_name(name_part, allow_default=False)
    if currency_part:
        currency = normalize_currency(currency_part, default=None, allow_none=False)
        row = fetch_account(conn, account_name, currency, include_inactive=True)
        if row is None:
            fail("Account not found.", account=build_account_label(account_name, currency))
        return row

    rows = fetch_accounts_by_name(conn, account_name, include_inactive=True)
    if len(rows) == 1:
        return rows[0]
    if len(rows) > 1:
        fail(
            "Account is ambiguous. Specify the currency, for example 银行卡:USD.",
            provided_account=raw_account,
            matching_accounts=[serialize_account_row(row) for row in rows],
        )
    fail("Account not found.", account=account_name)


def resolve_account(conn, raw_account, explicit_currency=None, allow_default=True):
    spec = parse_account_spec(raw_account, default_currency=explicit_currency, allow_default=allow_default)
    if spec["name"] == DEFAULT_UNSPECIFIED_ACCOUNT:
        return {
            "id": None,
            "name": DEFAULT_UNSPECIFIED_ACCOUNT,
            "currency": None,
            "label": DEFAULT_UNSPECIFIED_ACCOUNT,
            "matched": False,
            "is_active": False,
        }

    if spec["currency"] is not None:
        row = fetch_account(conn, spec["name"], spec["currency"], include_inactive=False)
        if row:
            return {
                "id": row["id"],
                "name": row["name"],
                "currency": row["currency"],
                "label": build_account_label(row["name"], row["currency"]),
                "matched": True,
                "is_active": bool(row["is_active"]),
            }
        return {
            "id": None,
            "name": spec["name"],
            "currency": spec["currency"],
            "label": build_account_label(spec["name"], spec["currency"]),
            "matched": False,
            "is_active": False,
        }

    rows = fetch_accounts_by_name(conn, spec["name"], include_inactive=False)
    if len(rows) == 1:
        row = rows[0]
        return {
            "id": row["id"],
            "name": row["name"],
            "currency": row["currency"],
            "label": build_account_label(row["name"], row["currency"]),
            "matched": True,
            "is_active": bool(row["is_active"]),
        }
    if len(rows) > 1:
        fail(
            "Account is ambiguous. Specify the currency, for example 银行卡:USD.",
            provided_account=raw_account,
            matching_accounts=[serialize_account_row(row) for row in rows],
        )
    return {
        "id": None,
        "name": spec["name"],
        "currency": None,
        "label": spec["name"],
        "matched": False,
        "is_active": False,
    }


def serialize_category_row(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "is_active": bool(row["is_active"]),
        "sort_order": row["sort_order"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def serialize_account_row(row):
    label = build_account_label(row["name"], row["currency"])
    payload = {
        "id": row["id"],
        "name": row["name"],
        "currency": row["currency"],
        "label": label,
        "is_active": bool(row["is_active"]),
        "sort_order": row["sort_order"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
    row_keys = set(row.keys())
    if "income_total_cents" in row_keys:
        payload["income_total"] = cents_to_amount(row["income_total_cents"])
        payload["income_total_cents"] = row["income_total_cents"]
    if "expense_total_cents" in row_keys:
        payload["expense_total"] = cents_to_amount(row["expense_total_cents"])
        payload["expense_total_cents"] = row["expense_total_cents"]
    if "balance_cents" in row_keys:
        payload["balance"] = cents_to_amount(row["balance_cents"])
        payload["balance_cents"] = row["balance_cents"]
    if "entry_count" in row_keys:
        payload["entry_count"] = row["entry_count"]
    return payload


def serialize_entry_row(row):
    return {
        "id": row["id"],
        "type": row["entry_type"],
        "amount": cents_to_amount(row["amount_cents"]),
        "amount_cents": row["amount_cents"],
        "currency": row["currency"],
        "category": row["category_name_snapshot"],
        "account": row["account_name_snapshot"],
        "description": row["description"],
        "note": row["note"],
        "occurred_on": row["occurred_on"],
        "source_text": row["source_text"],
        "created_at": row["created_at"],
    }


def serialize_recurring_row(row):
    return {
        "id": row["id"],
        "type": row["entry_type"],
        "amount": cents_to_amount(row["amount_cents"]),
        "amount_cents": row["amount_cents"],
        "currency": row["currency"],
        "category": row["category_name_snapshot"],
        "account": row["account_name_snapshot"],
        "description": row["description"],
        "note": row["note"],
        "frequency": row["frequency"],
        "interval_count": row["interval_count"],
        "next_due_on": row["next_due_on"],
        "source_text": row["source_text"],
        "is_active": bool(row["is_active"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def fetch_entry_by_id(conn, entry_id):
    return conn.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()


def fetch_latest_entry(conn):
    return conn.execute("SELECT * FROM entries ORDER BY id DESC LIMIT 1").fetchone()


def fetch_category_by_name(conn, category_name):
    return conn.execute(
        """
        SELECT id, name, is_active, sort_order, created_at, updated_at
        FROM categories
        WHERE name = ?
        """,
        (category_name,),
    ).fetchone()


def current_account_context_from_row(conn, row):
    if row["account_id"] is None:
        if row["account_name_snapshot"] == DEFAULT_UNSPECIFIED_ACCOUNT:
            return {
                "id": None,
                "name": DEFAULT_UNSPECIFIED_ACCOUNT,
                "currency": None,
                "label": DEFAULT_UNSPECIFIED_ACCOUNT,
                "matched": False,
                "is_active": False,
            }
        return {
            "id": None,
            "name": row["account_name_snapshot"],
            "currency": normalize_currency(row["currency"], default=None, allow_none=True),
            "label": row["account_name_snapshot"],
            "matched": False,
            "is_active": False,
        }
    account_row = fetch_account_by_id(conn, row["account_id"], include_inactive=True)
    if account_row is None:
        return {
            "id": row["account_id"],
            "name": row["account_name_snapshot"],
            "currency": normalize_currency(row["currency"], default=None, allow_none=True),
            "label": row["account_name_snapshot"],
            "matched": False,
            "is_active": False,
        }
    return {
        "id": account_row["id"],
        "name": account_row["name"],
        "currency": account_row["currency"],
        "label": build_account_label(account_row["name"], account_row["currency"]),
        "matched": bool(account_row["is_active"]),
        "is_active": bool(account_row["is_active"]),
    }


def fetch_recurring_by_id(conn, recurring_id):
    return conn.execute("SELECT * FROM recurring_transactions WHERE id = ?", (recurring_id,)).fetchone()


def resolve_transaction_currency(raw_currency, account_context):
    requested_currency = normalize_currency(raw_currency, default=None, allow_none=True)
    if account_context["name"] == DEFAULT_UNSPECIFIED_ACCOUNT:
        return requested_currency or DEFAULT_CURRENCY
    if account_context["currency"] is not None:
        if requested_currency and requested_currency != account_context["currency"]:
            fail(
                "Currency does not match the selected account.",
                provided_currency=requested_currency,
                account=account_context["label"],
                account_currency=account_context["currency"],
            )
        return account_context["currency"]
    if requested_currency:
        return requested_currency
    fail(
        "Account currency is required. Use a wallet name with a currency, for example Wise:USD, or pass --currency USD.",
        provided_account=account_context["name"],
    )


def resolve_account_context(conn, raw_account, raw_currency=None, allow_default=True):
    if raw_account is None:
        return resolve_account(conn, raw_account, explicit_currency=None, allow_default=allow_default)
    candidate = raw_account.strip()
    if not candidate:
        return resolve_account(conn, raw_account, explicit_currency=None, allow_default=allow_default)
    if allow_default and candidate == DEFAULT_UNSPECIFIED_ACCOUNT:
        return resolve_account(conn, raw_account, explicit_currency=None, allow_default=allow_default)

    name_part, currency_part = split_account_spec(candidate)
    if currency_part:
        return resolve_account(conn, raw_account, explicit_currency=None, allow_default=allow_default)

    normalized_name = normalize_account_base_name(name_part, allow_default=False)
    same_name_rows = fetch_accounts_by_name(conn, normalized_name, include_inactive=False)
    explicit_currency = raw_currency if len(same_name_rows) != 1 else None
    return resolve_account(conn, raw_account, explicit_currency=explicit_currency, allow_default=allow_default)


def resolve_account_context_for_write(conn, raw_account, raw_currency, strict_account):
    account_context = resolve_account_context(conn, raw_account, raw_currency=raw_currency, allow_default=True)
    active_accounts = active_account_labels(conn)
    if strict_account and not account_context["matched"]:
        fail(
            "Account does not match an active predefined account.",
            provided_account=account_context["label"],
            active_accounts=active_accounts,
            default_accounts=[build_account_label(name, currency) for name, currency in DEFAULT_ACCOUNT_SPECS],
        )
    currency = resolve_transaction_currency(raw_currency, account_context)
    if account_context["name"] != DEFAULT_UNSPECIFIED_ACCOUNT and account_context["currency"] is None:
        account_context["currency"] = currency
        account_context["label"] = build_account_label(account_context["name"], currency)
    return account_context, currency, active_accounts


def summarize_totals_by_currency(rows):
    payload = []
    for row in rows:
        payload.append(
            {
                "currency": row["currency"],
                "balance": cents_to_amount(row["balance_cents"]),
                "balance_cents": row["balance_cents"],
                "income_total": cents_to_amount(row["income_total_cents"]),
                "income_total_cents": row["income_total_cents"],
                "expense_total": cents_to_amount(row["expense_total_cents"]),
                "expense_total_cents": row["expense_total_cents"],
                "account_count": row["account_count"],
            }
        )
    return payload


def get_breakdown(conn, start_date, end_date, entry_type, snapshot_column, label_key):
    rows = conn.execute(
        f"""
        SELECT
            {snapshot_column} AS label,
            SUM(amount_cents) AS total_cents,
            COUNT(*) AS entry_count
        FROM entries
        WHERE occurred_on >= ? AND occurred_on < ? AND entry_type = ?
        GROUP BY {snapshot_column}
        ORDER BY total_cents DESC, {snapshot_column} ASC
        """,
        (start_date, end_date, entry_type),
    ).fetchall()
    breakdown = []
    for row in rows:
        breakdown.append(
            {
                label_key: row["label"],
                "total": cents_to_amount(row["total_cents"]),
                "total_cents": row["total_cents"],
                "entry_count": row["entry_count"],
            }
        )
    return breakdown


def collect_report_payload(conn, start_date, end_date):
    totals = {"expense": {"total_cents": 0, "entry_count": 0}, "income": {"total_cents": 0, "entry_count": 0}}
    for row in conn.execute(
        """
        SELECT entry_type, COALESCE(SUM(amount_cents), 0) AS total_cents, COUNT(*) AS entry_count
        FROM entries
        WHERE occurred_on >= ? AND occurred_on < ?
        GROUP BY entry_type
        """,
        (start_date, end_date),
    ):
        totals[row["entry_type"]] = {
            "total_cents": row["total_cents"],
            "entry_count": row["entry_count"],
        }

    expense_breakdown = get_breakdown(conn, start_date, end_date, "expense", "category_name_snapshot", "category")
    income_breakdown = get_breakdown(conn, start_date, end_date, "income", "category_name_snapshot", "category")
    expense_account_breakdown = get_breakdown(conn, start_date, end_date, "expense", "account_name_snapshot", "account")
    income_account_breakdown = get_breakdown(conn, start_date, end_date, "income", "account_name_snapshot", "account")

    expense_total_cents = totals["expense"]["total_cents"]
    income_total_cents = totals["income"]["total_cents"]
    net_total_cents = income_total_cents - expense_total_cents

    return {
        "expense_total": cents_to_amount(expense_total_cents),
        "expense_total_cents": expense_total_cents,
        "income_total": cents_to_amount(income_total_cents),
        "income_total_cents": income_total_cents,
        "net_total": cents_to_amount(net_total_cents),
        "net_total_cents": net_total_cents,
        "entry_count": totals["expense"]["entry_count"] + totals["income"]["entry_count"],
        "expense_entry_count": totals["expense"]["entry_count"],
        "income_entry_count": totals["income"]["entry_count"],
        "expense_by_category": expense_breakdown,
        "income_by_category": income_breakdown,
        "expense_by_account": expense_account_breakdown,
        "income_by_account": income_account_breakdown,
        "top_expense_category": expense_breakdown[0] if expense_breakdown else None,
        "top_income_category": income_breakdown[0] if income_breakdown else None,
        "top_expense_account": expense_account_breakdown[0] if expense_account_breakdown else None,
        "top_income_account": income_account_breakdown[0] if income_account_breakdown else None,
    }


def emit_period_report(command, db_path, period_type, period_value, start_date, end_date):
    with closing(connect_db(db_path)) as conn:
        report_payload = collect_report_payload(conn, start_date, end_date)
    emit(
        {
            "ok": True,
            "command": command,
            "db_path": str(db_path),
            **build_period_metadata(period_type, period_value),
            "start_date": start_date,
            "end_date_exclusive": end_date,
            **report_payload,
        }
    )


def cmd_list_categories(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        categories = [serialize_category_row(row) for row in list_categories_rows(conn, args.all)]
    emit(
        {
            "ok": True,
            "command": "list-categories",
            "db_path": str(db_path),
            "categories": categories,
            "active_category_names": [item["name"] for item in categories if item["is_active"]],
        }
    )


def cmd_list_accounts(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        accounts = [serialize_account_row(row) for row in list_accounts_rows(conn, args.all)]
    emit(
        {
            "ok": True,
            "command": "list-accounts",
            "db_path": str(db_path),
            "accounts": accounts,
            "active_account_labels": [item["label"] for item in accounts if item["is_active"]],
            "default_accounts": [
                {"name": name, "currency": currency, "label": build_account_label(name, currency)}
                for name, currency in DEFAULT_ACCOUNT_SPECS
            ],
        }
    )


def list_account_balance_rows(conn, include_inactive=False, currency_filter=None):
    params = []
    query = """
        SELECT
            a.id,
            a.name,
            a.currency,
            a.is_active,
            a.sort_order,
            a.created_at,
            a.updated_at,
            COALESCE(SUM(CASE WHEN e.entry_type = 'income' THEN e.amount_cents ELSE 0 END), 0) AS income_total_cents,
            COALESCE(SUM(CASE WHEN e.entry_type = 'expense' THEN e.amount_cents ELSE 0 END), 0) AS expense_total_cents,
            COUNT(e.id) AS entry_count
        FROM accounts a
        LEFT JOIN entries e ON e.account_id = a.id
    """
    filters = []
    if not include_inactive:
        filters.append("a.is_active = 1")
    if currency_filter:
        filters.append("a.currency = ?")
        params.append(currency_filter)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += """
        GROUP BY a.id, a.name, a.currency, a.is_active, a.sort_order, a.created_at, a.updated_at
        ORDER BY a.sort_order ASC, a.name ASC, a.currency ASC, a.id ASC
    """
    rows = []
    for row in conn.execute(query, params).fetchall():
        row_payload = dict(row)
        row_payload["balance_cents"] = row_payload["income_total_cents"] - row_payload["expense_total_cents"]
        rows.append(row_payload)
    return rows


def cmd_account_balances(args):
    db_path = resolve_db_path(args.db)
    currency_filter = normalize_currency(args.currency, default=None, allow_none=True) if args.currency else None
    with closing(connect_db(db_path)) as conn:
        rows = list_account_balance_rows(conn, include_inactive=args.all, currency_filter=currency_filter)

    accounts = []
    totals_by_currency = {}
    for row in rows:
        account_payload = serialize_account_row(row)
        accounts.append(account_payload)
        currency_totals = totals_by_currency.setdefault(
            row["currency"],
            {
                "currency": row["currency"],
                "balance_cents": 0,
                "income_total_cents": 0,
                "expense_total_cents": 0,
                "account_count": 0,
            },
        )
        currency_totals["balance_cents"] += row["balance_cents"]
        currency_totals["income_total_cents"] += row["income_total_cents"]
        currency_totals["expense_total_cents"] += row["expense_total_cents"]
        currency_totals["account_count"] += 1

    totals_payload = summarize_totals_by_currency(
        [totals_by_currency[currency] for currency in sorted(totals_by_currency.keys())]
    )
    emit(
        {
            "ok": True,
            "command": "account-balances",
            "db_path": str(db_path),
            "include_inactive": bool(args.all),
            "currency_filter": currency_filter,
            "accounts": accounts,
            "totals_by_currency": totals_payload,
        }
    )


def cmd_init_db(args):
    db_path = resolve_db_path(args.db)
    existed_before = db_path.exists()
    with closing(connect_db(db_path)) as conn:
        counts = get_db_counts(conn)
    emit(
        {
            "ok": True,
            "command": "init-db",
            "db_path": str(db_path),
            "db_exists": db_path.exists(),
            "db_existed_before": existed_before,
            "db_parent": str(db_path.parent),
            **counts,
        }
    )


def cmd_set_categories(args):
    names = normalize_names(args.names)
    db_path = resolve_db_path(args.db)
    now = utc_now()
    with closing(connect_db(db_path)) as conn:
        if args.replace:
            conn.execute("UPDATE categories SET is_active = 0, updated_at = ? WHERE is_active = 1", (now,))
            base_order = 0
        else:
            base_order = (
                conn.execute("SELECT COALESCE(MAX(sort_order), -1) AS max_sort_order FROM categories").fetchone()[
                    "max_sort_order"
                ]
                + 1
            )
        for index, name in enumerate(names):
            conn.execute(
                """
                INSERT INTO categories (name, is_active, sort_order, created_at, updated_at)
                VALUES (?, 1, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    is_active = 1,
                    sort_order = excluded.sort_order,
                    updated_at = excluded.updated_at
                """,
                (name, base_order + index, now, now),
            )
        conn.commit()
        categories = [serialize_category_row(row) for row in list_categories_rows(conn, include_inactive=False)]
    emit(
        {
            "ok": True,
            "command": "set-categories",
            "db_path": str(db_path),
            "replace": bool(args.replace),
            "categories": categories,
        }
    )


def cmd_set_accounts(args):
    specs = normalize_account_specs(args.names)
    db_path = resolve_db_path(args.db)
    now = utc_now()
    with closing(connect_db(db_path)) as conn:
        if args.replace:
            conn.execute("UPDATE accounts SET is_active = 0, updated_at = ? WHERE is_active = 1", (now,))
            base_order = 0
        else:
            base_order = (
                conn.execute("SELECT COALESCE(MAX(sort_order), -1) AS max_sort_order FROM accounts").fetchone()[
                    "max_sort_order"
                ]
                + 1
            )
        for index, spec in enumerate(specs):
            conn.execute(
                """
                INSERT INTO accounts (name, currency, is_active, sort_order, created_at, updated_at)
                VALUES (?, ?, 1, ?, ?, ?)
                ON CONFLICT(name, currency) DO UPDATE SET
                    is_active = 1,
                    sort_order = excluded.sort_order,
                    updated_at = excluded.updated_at
                """,
                (spec["name"], spec["currency"], base_order + index, now, now),
            )
        conn.commit()
        accounts = [serialize_account_row(row) for row in list_accounts_rows(conn, include_inactive=False)]
    emit(
        {
            "ok": True,
            "command": "set-accounts",
            "db_path": str(db_path),
            "replace": bool(args.replace),
            "accounts": accounts,
            "active_account_labels": [item["label"] for item in accounts],
            "default_accounts": [
                {"name": name, "currency": currency, "label": build_account_label(name, currency)}
                for name, currency in DEFAULT_ACCOUNT_SPECS
            ],
        }
    )


def cmd_record(args):
    db_path = resolve_db_path(args.db)
    amount_cents = parse_amount_to_cents(args.amount)
    occurred_on = parse_iso_date(args.date).isoformat()
    entry_type = args.type
    description = args.description.strip()
    if not description:
        fail("Description is required.")
    note = args.note.strip() if args.note else None
    source_text = args.source_text.strip() if args.source_text else None

    with closing(connect_db(db_path)) as conn:
        category_id, category_snapshot, matched = resolve_category(conn, args.category)
        active_names = active_category_names(conn)
        if args.strict_category and not matched:
            fail(
                "Category does not match an active predefined category.",
                provided_category=category_snapshot,
                active_categories=active_names,
            )
        account_context, currency, active_accounts = resolve_account_context_for_write(
            conn, args.account, args.currency, args.strict_account
        )
        created_at = utc_now()
        cursor = conn.execute(
            """
            INSERT INTO entries (
                entry_type,
                amount_cents,
                currency,
                category_id,
                category_name_snapshot,
                account_id,
                account_name_snapshot,
                description,
                note,
                occurred_on,
                source_text,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry_type,
                amount_cents,
                currency,
                category_id,
                category_snapshot,
                account_context["id"],
                account_context["label"],
                description,
                note,
                occurred_on,
                source_text,
                created_at,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM entries WHERE id = ?", (cursor.lastrowid,)).fetchone()

    payload = serialize_entry_row(row)
    payload["category_matched_active_category"] = matched
    payload["account_matched_active_account"] = account_context["matched"]
    emit(
        {
            "ok": True,
            "command": "record",
            "db_path": str(db_path),
            "active_accounts": active_accounts,
            "entry": payload,
        }
    )


def cmd_list_transactions(args):
    db_path = resolve_db_path(args.db)
    period_type, period_value, start_date, end_date = select_transaction_period(args)
    params = [start_date, end_date]
    account_filter = None
    query = """
        SELECT *
        FROM entries
        WHERE occurred_on >= ? AND occurred_on < ?
    """
    if args.type:
        query += " AND entry_type = ?"
        params.append(args.type)
    if args.category:
        query += " AND category_name_snapshot = ?"
        params.append(args.category.strip())

    with closing(connect_db(db_path)) as conn:
        if args.account:
            account_filter = resolve_account(conn, args.account, allow_default=True)["label"]
            query += " AND account_name_snapshot = ?"
            params.append(account_filter)
        query += " ORDER BY occurred_on DESC, id DESC LIMIT ?"
        params.append(args.limit)
        rows = conn.execute(query, params).fetchall()

    emit(
        {
            "ok": True,
            "command": "list-transactions",
            "db_path": str(db_path),
            **build_period_metadata(period_type, period_value),
            "start_date": start_date,
            "end_date_exclusive": end_date,
            "type_filter": args.type,
            "category_filter": args.category,
            "account_filter": account_filter,
            "limit": args.limit,
            "entries": [serialize_entry_row(row) for row in rows],
        }
    )


def cmd_recent_transactions(args):
    db_path = resolve_db_path(args.db)
    params = []
    account_filter = None
    query = """
        SELECT *
        FROM entries
    """
    filters = []
    if args.type:
        filters.append("entry_type = ?")
        params.append(args.type)
    if args.category:
        filters.append("category_name_snapshot = ?")
        params.append(args.category.strip())
    if filters:
        query += " WHERE " + " AND ".join(filters)

    with closing(connect_db(db_path)) as conn:
        if args.account:
            account_filter = resolve_account(conn, args.account, allow_default=True)["label"]
            if filters:
                query += " AND account_name_snapshot = ?"
            else:
                query += " WHERE account_name_snapshot = ?"
            params.append(account_filter)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(args.limit)
        rows = conn.execute(query, params).fetchall()

    emit(
        {
            "ok": True,
            "command": "recent-transactions",
            "db_path": str(db_path),
            "type_filter": args.type,
            "category_filter": args.category,
            "account_filter": account_filter,
            "limit": args.limit,
            "entries": [serialize_entry_row(row) for row in rows],
        }
    )


def cmd_latest_entry(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        row = fetch_latest_entry(conn)
        if row is None:
            fail("No entries available.")

    emit(
        {
            "ok": True,
            "command": "latest-entry",
            "db_path": str(db_path),
            "entry": serialize_entry_row(row),
        }
    )


def cmd_month_report(args):
    db_path = resolve_db_path(args.db)
    month_value, start_date, end_date = month_bounds(args.month)
    emit_period_report("month-report", db_path, "month", month_value, start_date, end_date)


def cmd_day_report(args):
    db_path = resolve_db_path(args.db)
    day_value, start_date, end_date = day_bounds(args.date)
    emit_period_report("day-report", db_path, "date", day_value, start_date, end_date)


def cmd_week_report(args):
    db_path = resolve_db_path(args.db)
    week_value, start_date, end_date = week_bounds(week_value=args.week, date_value=args.date)
    emit_period_report("week-report", db_path, "week", week_value, start_date, end_date)


def cmd_year_report(args):
    db_path = resolve_db_path(args.db)
    year_value, start_date, end_date = year_bounds(args.year)
    emit_period_report("year-report", db_path, "year", year_value, start_date, end_date)


def cmd_add_recurring(args):
    db_path = resolve_db_path(args.db)
    amount_cents = parse_amount_to_cents(args.amount)
    next_due_on = parse_iso_date(args.next_date).isoformat()
    description = args.description.strip()
    if not description:
        fail("Description is required.")
    note = args.note.strip() if args.note else None
    source_text = args.source_text.strip() if args.source_text else None

    with closing(connect_db(db_path)) as conn:
        category_id, category_snapshot, category_matched = resolve_category(conn, args.category)
        active_categories = active_category_names(conn)
        if args.strict_category and not category_matched:
            fail(
                "Category does not match an active predefined category.",
                provided_category=category_snapshot,
                active_categories=active_categories,
            )
        account_context, currency, active_accounts = resolve_account_context_for_write(
            conn, args.account, args.currency, args.strict_account
        )
        now = utc_now()
        cursor = conn.execute(
            """
            INSERT INTO recurring_transactions (
                entry_type,
                amount_cents,
                currency,
                category_id,
                category_name_snapshot,
                account_id,
                account_name_snapshot,
                description,
                note,
                frequency,
                interval_count,
                next_due_on,
                source_text,
                is_active,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """,
            (
                args.type,
                amount_cents,
                currency,
                category_id,
                category_snapshot,
                account_context["id"],
                account_context["label"],
                description,
                note,
                args.frequency,
                args.interval,
                next_due_on,
                source_text,
                now,
                now,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM recurring_transactions WHERE id = ?", (cursor.lastrowid,)).fetchone()

    payload = serialize_recurring_row(row)
    payload["category_matched_active_category"] = category_matched
    payload["account_matched_active_account"] = account_context["matched"]
    emit(
        {
            "ok": True,
            "command": "add-recurring",
            "db_path": str(db_path),
            "active_accounts": active_accounts,
            "recurring_transaction": payload,
        }
    )


def cmd_list_recurring(args):
    db_path = resolve_db_path(args.db)
    params = []
    account_filter = None
    query = """
        SELECT *
        FROM recurring_transactions
    """
    filters = []
    if not args.all:
        filters.append("is_active = 1")
    if args.type:
        filters.append("entry_type = ?")
        params.append(args.type)
    if args.frequency:
        filters.append("frequency = ?")
        params.append(args.frequency)
    if args.category:
        filters.append("category_name_snapshot = ?")
        params.append(args.category.strip())
    due_by = None
    if args.due_by:
        due_by = parse_iso_date(args.due_by).isoformat()
        filters.append("next_due_on <= ?")
        params.append(due_by)

    with closing(connect_db(db_path)) as conn:
        if args.account:
            account_filter = resolve_account(conn, args.account, allow_default=True)["label"]
            filters.append("account_name_snapshot = ?")
            params.append(account_filter)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY next_due_on ASC, id ASC LIMIT ?"
        params.append(args.limit)
        rows = conn.execute(query, params).fetchall()

    emit(
        {
            "ok": True,
            "command": "list-recurring",
            "db_path": str(db_path),
            "include_inactive": bool(args.all),
            "type_filter": args.type,
            "frequency_filter": args.frequency,
            "category_filter": args.category,
            "account_filter": account_filter,
            "due_by": due_by,
            "limit": args.limit,
            "recurring_transactions": [serialize_recurring_row(row) for row in rows],
        }
    )


def cmd_update_recurring(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        row = fetch_recurring_by_id(conn, args.id)
        if row is None:
            fail("Recurring transaction not found.", recurring_transaction_id=args.id)

        updates = {}
        updated_fields = []
        category_matched = None
        account_matched = None
        active_categories = None
        active_accounts = None
        current_account_context = current_account_context_from_row(conn, row)
        requested_currency = normalize_currency(args.currency, default=DEFAULT_CURRENCY) if args.currency is not None else None

        if args.type is not None:
            updates["entry_type"] = args.type
            updated_fields.append("type")
        if args.amount is not None:
            updates["amount_cents"] = parse_amount_to_cents(args.amount)
            updated_fields.append("amount")
        if args.category is not None:
            category_id, category_snapshot, category_matched = resolve_category(conn, args.category)
            active_categories = active_category_names(conn)
            if args.strict_category and not category_matched:
                fail(
                    "Category does not match an active predefined category.",
                    provided_category=category_snapshot,
                    active_categories=active_categories,
                )
            updates["category_id"] = category_id
            updates["category_name_snapshot"] = category_snapshot
            updated_fields.append("category")
        if args.account is not None:
            account_context = resolve_account_context(conn, args.account, raw_currency=args.currency, allow_default=True)
            active_accounts = active_account_labels(conn)
            if args.strict_account and not account_context["matched"]:
                fail(
                    "Account does not match an active predefined account.",
                    provided_account=account_context["label"],
                    active_accounts=active_accounts,
                    default_accounts=[build_account_label(name, currency) for name, currency in DEFAULT_ACCOUNT_SPECS],
                )
            currency_input = args.currency
            if currency_input is None and account_context["currency"] is None:
                currency_input = row["currency"]
            final_currency = resolve_transaction_currency(currency_input, account_context)
            if account_context["name"] != DEFAULT_UNSPECIFIED_ACCOUNT and account_context["currency"] is None:
                account_context["currency"] = final_currency
                account_context["label"] = build_account_label(account_context["name"], final_currency)
            updates["account_id"] = account_context["id"]
            updates["account_name_snapshot"] = account_context["label"]
            updated_fields.append("account")
            account_matched = account_context["matched"]
            if final_currency != row["currency"] or args.currency is not None:
                updates["currency"] = final_currency
                if "currency" not in updated_fields:
                    updated_fields.append("currency")
        elif args.currency is not None:
            if current_account_context["id"] is not None and current_account_context["name"] != DEFAULT_UNSPECIFIED_ACCOUNT:
                if requested_currency != current_account_context["currency"]:
                    fail(
                        "Currency does not match the selected account.",
                        provided_currency=requested_currency,
                        account=current_account_context["label"],
                        account_currency=current_account_context["currency"],
                    )
            updates["currency"] = requested_currency
            updated_fields.append("currency")
        if args.description is not None:
            description = args.description.strip()
            if not description:
                fail("Description is required.")
            updates["description"] = description
            updated_fields.append("description")
        if args.note is not None:
            note = args.note.strip()
            updates["note"] = note or None
            updated_fields.append("note")
        if args.frequency is not None:
            updates["frequency"] = args.frequency
            updated_fields.append("frequency")
        if args.interval is not None:
            updates["interval_count"] = args.interval
            updated_fields.append("interval")
        if args.next_date is not None:
            updates["next_due_on"] = parse_iso_date(args.next_date).isoformat()
            updated_fields.append("next_date")
        if args.source_text is not None:
            source_text = args.source_text.strip()
            updates["source_text"] = source_text or None
            updated_fields.append("source_text")
        if args.activate:
            updates["is_active"] = 1
            updated_fields.append("activate")
        if args.deactivate:
            updates["is_active"] = 0
            updated_fields.append("deactivate")

        if not updates:
            fail("Provide at least one field to update.")

        updates["updated_at"] = utc_now()
        update_pairs = list(updates.items())
        query = (
            "UPDATE recurring_transactions SET "
            + ", ".join(f"{column} = ?" for column, _ in update_pairs)
            + " WHERE id = ?"
        )
        values = [value for _, value in update_pairs]
        values.append(args.id)
        conn.execute(query, values)
        conn.commit()
        updated_row = fetch_recurring_by_id(conn, args.id)

    payload = serialize_recurring_row(updated_row)
    if category_matched is not None:
        payload["category_matched_active_category"] = category_matched
    if account_matched is not None:
        payload["account_matched_active_account"] = account_matched
    emit(
        {
            "ok": True,
            "command": "update-recurring",
            "db_path": str(db_path),
            "updated_fields": updated_fields,
            "active_categories": active_categories,
            "active_accounts": active_accounts,
            "recurring_transaction": payload,
        }
    )


def cmd_delete_recurring(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        row = fetch_recurring_by_id(conn, args.id)
        if row is None:
            fail("Recurring transaction not found.", recurring_transaction_id=args.id)
        if not row["is_active"]:
            fail("Recurring transaction is already inactive.", recurring_transaction_id=args.id)
        deleted_payload = serialize_recurring_row(row)
        conn.execute(
            "UPDATE recurring_transactions SET is_active = 0, updated_at = ? WHERE id = ?",
            (utc_now(), args.id),
        )
        conn.commit()
        counts = get_db_counts(conn)

    emit(
        {
            "ok": True,
            "command": "delete-recurring",
            "db_path": str(db_path),
            "deleted_recurring_transaction": deleted_payload,
            **counts,
        }
    )


def cmd_update_entry(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        row = fetch_entry_by_id(conn, args.id)
        if row is None:
            fail("Entry not found.", entry_id=args.id)

        updates = {}
        updated_fields = []
        matched = None
        account_matched = None
        active_names = None
        active_accounts = None
        current_account_context = current_account_context_from_row(conn, row)
        requested_currency = normalize_currency(args.currency, default=DEFAULT_CURRENCY) if args.currency is not None else None

        if args.type is not None:
            updates["entry_type"] = args.type
            updated_fields.append("type")
        if args.amount is not None:
            updates["amount_cents"] = parse_amount_to_cents(args.amount)
            updated_fields.append("amount")
        if args.category is not None:
            category_id, category_snapshot, matched = resolve_category(conn, args.category)
            active_names = active_category_names(conn)
            if args.strict_category and not matched:
                fail(
                    "Category does not match an active predefined category.",
                    provided_category=category_snapshot,
                    active_categories=active_names,
                )
            updates["category_id"] = category_id
            updates["category_name_snapshot"] = category_snapshot
            updated_fields.append("category")
        if args.account is not None:
            account_context = resolve_account_context(conn, args.account, raw_currency=args.currency, allow_default=True)
            active_accounts = active_account_labels(conn)
            if args.strict_account and not account_context["matched"]:
                fail(
                    "Account does not match an active predefined account.",
                    provided_account=account_context["label"],
                    active_accounts=active_accounts,
                    default_accounts=[build_account_label(name, currency) for name, currency in DEFAULT_ACCOUNT_SPECS],
                )
            currency_input = args.currency
            if currency_input is None and account_context["currency"] is None:
                currency_input = row["currency"]
            final_currency = resolve_transaction_currency(currency_input, account_context)
            if account_context["name"] != DEFAULT_UNSPECIFIED_ACCOUNT and account_context["currency"] is None:
                account_context["currency"] = final_currency
                account_context["label"] = build_account_label(account_context["name"], final_currency)
            updates["account_id"] = account_context["id"]
            updates["account_name_snapshot"] = account_context["label"]
            updated_fields.append("account")
            account_matched = account_context["matched"]
            if final_currency != row["currency"] or args.currency is not None:
                updates["currency"] = final_currency
                if "currency" not in updated_fields:
                    updated_fields.append("currency")
        elif args.currency is not None:
            if current_account_context["id"] is not None and current_account_context["name"] != DEFAULT_UNSPECIFIED_ACCOUNT:
                if requested_currency != current_account_context["currency"]:
                    fail(
                        "Currency does not match the selected account.",
                        provided_currency=requested_currency,
                        account=current_account_context["label"],
                        account_currency=current_account_context["currency"],
                    )
            updates["currency"] = requested_currency
            updated_fields.append("currency")
        if args.description is not None:
            description = args.description.strip()
            if not description:
                fail("Description is required.")
            updates["description"] = description
            updated_fields.append("description")
        if args.note is not None:
            note = args.note.strip()
            updates["note"] = note or None
            updated_fields.append("note")
        if args.date is not None:
            updates["occurred_on"] = parse_iso_date(args.date).isoformat()
            updated_fields.append("date")
        if args.source_text is not None:
            source_text = args.source_text.strip()
            updates["source_text"] = source_text or None
            updated_fields.append("source_text")

        if not updates:
            fail("Provide at least one field to update.")

        update_pairs = list(updates.items())
        query = "UPDATE entries SET " + ", ".join(f"{column} = ?" for column, _ in update_pairs) + " WHERE id = ?"
        values = [value for _, value in update_pairs]
        values.append(args.id)
        conn.execute(query, values)
        conn.commit()
        updated_row = fetch_entry_by_id(conn, args.id)

    payload = serialize_entry_row(updated_row)
    if matched is not None:
        payload["category_matched_active_category"] = matched
    if account_matched is not None:
        payload["account_matched_active_account"] = account_matched
    emit(
        {
            "ok": True,
            "command": "update-entry",
            "db_path": str(db_path),
            "updated_fields": updated_fields,
            "active_categories": active_names,
            "active_accounts": active_accounts,
            "entry": payload,
        }
    )


def cmd_delete_entry(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        row = fetch_entry_by_id(conn, args.id)
        if row is None:
            fail("Entry not found.", entry_id=args.id)
        deleted_entry = serialize_entry_row(row)
        conn.execute("DELETE FROM entries WHERE id = ?", (args.id,))
        conn.commit()
        counts = get_db_counts(conn)

    emit(
        {
            "ok": True,
            "command": "delete-entry",
            "db_path": str(db_path),
            "deleted_entry": deleted_entry,
            **counts,
        }
    )


def cmd_delete_category(args):
    db_path = resolve_db_path(args.db)
    category_name = args.name.strip()
    if not category_name:
        fail("Category name is required.")

    with closing(connect_db(db_path)) as conn:
        row = fetch_category_by_name(conn, category_name)
        if row is None:
            fail("Category not found.", category=category_name)
        if not row["is_active"]:
            fail("Category is already inactive.", category=category_name)

        now = utc_now()
        conn.execute(
            """
            UPDATE categories
            SET is_active = 0, updated_at = ?
            WHERE id = ?
            """,
            (now, row["id"]),
        )
        conn.commit()
        deleted_category = fetch_category_by_name(conn, category_name)
        categories = [serialize_category_row(item) for item in list_categories_rows(conn, include_inactive=False)]

    emit(
        {
            "ok": True,
            "command": "delete-category",
            "db_path": str(db_path),
            "deleted_category": serialize_category_row(deleted_category),
            "categories": categories,
            "active_category_names": [item["name"] for item in categories],
        }
    )


def cmd_update_account(args):
    db_path = resolve_db_path(args.db)
    new_name = normalize_account_base_name(args.new_name, allow_default=False) if args.new_name is not None else None
    new_currency = normalize_currency(args.currency, default=None, allow_none=True) if args.currency is not None else None

    if new_name is None and new_currency is None:
        fail("Provide at least one field to update.")

    with closing(connect_db(db_path)) as conn:
        row = resolve_existing_account_row(conn, args.name)
        target_name = new_name or row["name"]
        target_currency = new_currency or row["currency"]
        if target_name == row["name"] and target_currency == row["currency"]:
            fail("Provide at least one changed field to update.")

        conflict_row = fetch_account(conn, target_name, target_currency, include_inactive=True)
        if conflict_row is not None and conflict_row["id"] != row["id"]:
            fail(
                "Account already exists.",
                target_account=build_account_label(target_name, target_currency),
            )

        previous_account = serialize_account_row(row)
        updated_fields = []
        if target_name != row["name"]:
            updated_fields.append("name")
        if target_currency != row["currency"]:
            updated_fields.append("currency")

        updated_label = build_account_label(target_name, target_currency)
        now = utc_now()
        linked_entry_count = conn.execute(
            "SELECT COUNT(*) AS count FROM entries WHERE account_id = ?",
            (row["id"],),
        ).fetchone()["count"]
        linked_recurring_count = conn.execute(
            "SELECT COUNT(*) AS count FROM recurring_transactions WHERE account_id = ?",
            (row["id"],),
        ).fetchone()["count"]

        conn.execute(
            """
            UPDATE accounts
            SET name = ?, currency = ?, updated_at = ?
            WHERE id = ?
            """,
            (target_name, target_currency, now, row["id"]),
        )
        conn.execute(
            """
            UPDATE entries
            SET account_name_snapshot = ?, currency = ?
            WHERE account_id = ?
            """,
            (updated_label, target_currency, row["id"]),
        )
        conn.execute(
            """
            UPDATE recurring_transactions
            SET account_name_snapshot = ?, currency = ?, updated_at = ?
            WHERE account_id = ?
            """,
            (updated_label, target_currency, now, row["id"]),
        )
        conn.commit()

        updated_account = fetch_account_by_id(conn, row["id"], include_inactive=True)
        accounts = [serialize_account_row(item) for item in list_accounts_rows(conn, include_inactive=False)]

    emit(
        {
            "ok": True,
            "command": "update-account",
            "db_path": str(db_path),
            "updated_fields": updated_fields,
            "previous_account": previous_account,
            "account": serialize_account_row(updated_account),
            "linked_entry_count": linked_entry_count,
            "linked_recurring_transaction_count": linked_recurring_count,
            "accounts": accounts,
            "active_account_labels": [item["label"] for item in accounts],
        }
    )


def cmd_delete_account(args):
    db_path = resolve_db_path(args.db)
    account_spec = parse_account_spec(args.name, allow_default=False)
    if account_spec["currency"] is None:
        fail(
            "Account currency is required. Use a wallet name with a currency, for example 支付宝:CNY or 银行卡:USD.",
            provided_account=args.name,
        )

    with closing(connect_db(db_path)) as conn:
        row = fetch_account(conn, account_spec["name"], account_spec["currency"], include_inactive=True)
        if row is None:
            fail("Account not found.", account=build_account_label(account_spec["name"], account_spec["currency"]))
        if not row["is_active"]:
            fail("Account is already inactive.", account=build_account_label(account_spec["name"], account_spec["currency"]))

        now = utc_now()
        conn.execute(
            """
            UPDATE accounts
            SET is_active = 0, updated_at = ?
            WHERE id = ?
            """,
            (now, row["id"]),
        )
        conn.commit()
        deleted_account = fetch_account(conn, account_spec["name"], account_spec["currency"], include_inactive=True)
        accounts = [serialize_account_row(item) for item in list_accounts_rows(conn, include_inactive=False)]

    emit(
        {
            "ok": True,
            "command": "delete-account",
            "db_path": str(db_path),
            "deleted_account": serialize_account_row(deleted_account),
            "accounts": accounts,
            "active_account_labels": [item["label"] for item in accounts],
            "default_accounts": [
                {"name": name, "currency": currency, "label": build_account_label(name, currency)}
                for name, currency in DEFAULT_ACCOUNT_SPECS
            ],
        }
    )


def cmd_delete_latest_entry(args):
    db_path = resolve_db_path(args.db)
    with closing(connect_db(db_path)) as conn:
        row = fetch_latest_entry(conn)
        if row is None:
            fail("No entries available to delete.")
        deleted_entry = serialize_entry_row(row)
        conn.execute("DELETE FROM entries WHERE id = ?", (row["id"],))
        conn.commit()
        counts = get_db_counts(conn)

    emit(
        {
            "ok": True,
            "command": "delete-latest-entry",
            "db_path": str(db_path),
            "deleted_entry": deleted_entry,
            **counts,
        }
    )


def build_parser():
    parser = argparse.ArgumentParser(description="money_tracker helper backed by SQLite.")
    parser.add_argument("--db", help="Custom SQLite database path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_db = subparsers.add_parser("init-db", help="Create the database file and schema")
    init_db.set_defaults(func=cmd_init_db)

    list_categories = subparsers.add_parser("list-categories", help="List categories")
    list_categories.add_argument("--all", action="store_true", help="Include inactive categories")
    list_categories.set_defaults(func=cmd_list_categories)

    list_accounts = subparsers.add_parser("list-accounts", help="List wallet accounts")
    list_accounts.add_argument("--all", action="store_true", help="Include inactive accounts")
    list_accounts.set_defaults(func=cmd_list_accounts)

    account_balances = subparsers.add_parser(
        "account-balances",
        help="Show per-wallet balances and totals grouped by currency",
    )
    account_balances.add_argument("--all", action="store_true", help="Include inactive accounts")
    account_balances.add_argument("--currency", help="Optional currency filter such as CNY, USD, or EUR")
    account_balances.set_defaults(func=cmd_account_balances)

    set_categories = subparsers.add_parser("set-categories", help="Add or replace categories")
    set_categories.add_argument("names", nargs="+", help="Category names")
    set_categories.add_argument("--replace", action="store_true", help="Replace the active category set")
    set_categories.set_defaults(func=cmd_set_categories)

    set_accounts = subparsers.add_parser("set-accounts", help="Add or replace active wallet accounts")
    set_accounts.add_argument("names", nargs="+", help="Account specs such as 支付宝:CNY or 银行卡:USD")
    set_accounts.add_argument("--replace", action="store_true", help="Replace the active account set")
    set_accounts.set_defaults(func=cmd_set_accounts)

    record = subparsers.add_parser("record", help="Record one transaction")
    record.add_argument("--type", choices=["expense", "income"], default="expense", help="Transaction type")
    record.add_argument("--amount", required=True, help="Positive amount")
    record.add_argument("--category", default=DEFAULT_UNCATEGORIZED, help="Category name")
    record.add_argument("--account", default=DEFAULT_UNSPECIFIED_ACCOUNT, help="Wallet name or wallet:currency")
    record.add_argument("--description", required=True, help="Short description")
    record.add_argument("--note", help="Additional note")
    record.add_argument("--date", default=date.today().isoformat(), help="Occurrence date in YYYY-MM-DD")
    record.add_argument("--currency", help="Currency code; defaults to the wallet currency or CNY")
    record.add_argument("--source-text", help="Original natural-language prompt")
    record.add_argument(
        "--strict-category",
        action="store_true",
        help="Require the category to match an active predefined category",
    )
    record.add_argument(
        "--strict-account",
        action="store_true",
        help="Require the account to match an active predefined account",
    )
    record.set_defaults(func=cmd_record)

    list_transactions = subparsers.add_parser(
        "list-transactions",
        help="List transactions for one date, ISO week, month, or year",
    )
    list_period = list_transactions.add_mutually_exclusive_group()
    list_period.add_argument("--date", help="Target date in YYYY-MM-DD")
    list_period.add_argument("--week", help="Target ISO week in YYYY-Www")
    list_period.add_argument("--month", help="Target month in YYYY-MM; defaults to the current month")
    list_period.add_argument("--year", help="Target year in YYYY")
    list_transactions.add_argument("--type", choices=["expense", "income"], help="Optional type filter")
    list_transactions.add_argument("--category", help="Optional category filter")
    list_transactions.add_argument("--account", help="Optional wallet filter such as 支付宝:CNY or 银行卡:USD")
    list_transactions.add_argument("--limit", type=int, default=100, help="Maximum number of entries to return")
    list_transactions.set_defaults(func=cmd_list_transactions)

    recent_transactions = subparsers.add_parser(
        "recent-transactions",
        help="List the most recent transactions across all dates",
    )
    recent_transactions.add_argument("--type", choices=["expense", "income"], help="Optional type filter")
    recent_transactions.add_argument("--category", help="Optional category filter")
    recent_transactions.add_argument("--account", help="Optional wallet filter such as 支付宝:CNY or 银行卡:USD")
    recent_transactions.add_argument("--limit", type=int, default=10, help="Maximum number of entries to return")
    recent_transactions.set_defaults(func=cmd_recent_transactions)

    latest_entry = subparsers.add_parser("latest-entry", help="Show the latest transaction")
    latest_entry.set_defaults(func=cmd_latest_entry)

    day_report = subparsers.add_parser("day-report", help="Get totals and category breakdown for one date")
    day_report.add_argument("--date", help="Target date in YYYY-MM-DD; defaults to today")
    day_report.set_defaults(func=cmd_day_report)

    week_report = subparsers.add_parser("week-report", help="Get totals and category breakdown for one ISO week")
    week_report_period = week_report.add_mutually_exclusive_group()
    week_report_period.add_argument("--week", help="Target ISO week in YYYY-Www")
    week_report_period.add_argument("--date", help="Reference date in YYYY-MM-DD; uses the ISO week containing it")
    week_report.set_defaults(func=cmd_week_report)

    month_report = subparsers.add_parser("month-report", help="Get totals and category breakdown for one month")
    month_report.add_argument("--month", help="Target month in YYYY-MM; defaults to the current month")
    month_report.set_defaults(func=cmd_month_report)

    year_report = subparsers.add_parser("year-report", help="Get totals and category breakdown for one year")
    year_report.add_argument("--year", help="Target year in YYYY; defaults to the current year")
    year_report.set_defaults(func=cmd_year_report)

    add_recurring = subparsers.add_parser("add-recurring", help="Add one recurring transaction schedule")
    add_recurring.add_argument("--type", choices=["expense", "income"], default="expense", help="Transaction type")
    add_recurring.add_argument("--amount", required=True, help="Positive amount")
    add_recurring.add_argument("--category", default=DEFAULT_UNCATEGORIZED, help="Category name")
    add_recurring.add_argument("--account", default=DEFAULT_UNSPECIFIED_ACCOUNT, help="Wallet name or wallet:currency")
    add_recurring.add_argument("--description", required=True, help="Short description")
    add_recurring.add_argument("--note", help="Additional note")
    add_recurring.add_argument("--currency", help="Currency code; defaults to the wallet currency or CNY")
    add_recurring.add_argument("--frequency", choices=sorted(RECURRING_FREQUENCIES), required=True, help="Frequency")
    add_recurring.add_argument("--interval", type=int, default=1, help="Repeat every N frequency units")
    add_recurring.add_argument("--next-date", required=True, help="Next due date in YYYY-MM-DD")
    add_recurring.add_argument("--source-text", help="Original natural-language prompt")
    add_recurring.add_argument(
        "--strict-category",
        action="store_true",
        help="Require the category to match an active predefined category",
    )
    add_recurring.add_argument(
        "--strict-account",
        action="store_true",
        help="Require the account to match an active predefined account",
    )
    add_recurring.set_defaults(func=cmd_add_recurring)

    list_recurring = subparsers.add_parser("list-recurring", help="List recurring transaction schedules")
    list_recurring.add_argument("--all", action="store_true", help="Include inactive recurring transactions")
    list_recurring.add_argument("--type", choices=["expense", "income"], help="Optional type filter")
    list_recurring.add_argument("--frequency", choices=sorted(RECURRING_FREQUENCIES), help="Optional frequency filter")
    list_recurring.add_argument("--category", help="Optional category filter")
    list_recurring.add_argument("--account", help="Optional wallet filter such as 支付宝:CNY or 银行卡:USD")
    list_recurring.add_argument("--due-by", help="Optional due date filter in YYYY-MM-DD")
    list_recurring.add_argument("--limit", type=int, default=100, help="Maximum number of rows to return")
    list_recurring.set_defaults(func=cmd_list_recurring)

    update_entry = subparsers.add_parser("update-entry", help="Update one transaction by id")
    update_entry.add_argument("--id", type=int, required=True, help="Entry id to update")
    update_entry.add_argument("--type", choices=["expense", "income"], help="Updated transaction type")
    update_entry.add_argument("--amount", help="Updated positive amount")
    update_entry.add_argument("--currency", help="Updated currency code")
    update_entry.add_argument("--category", help="Updated category name")
    update_entry.add_argument("--account", help="Updated wallet name or wallet:currency")
    update_entry.add_argument("--description", help="Updated short description")
    update_entry.add_argument("--note", help="Updated note; use an empty string to clear it")
    update_entry.add_argument("--date", help="Updated occurrence date in YYYY-MM-DD")
    update_entry.add_argument("--source-text", help="Updated original natural-language prompt")
    update_entry.add_argument(
        "--strict-category",
        action="store_true",
        help="Require the updated category to match an active predefined category",
    )
    update_entry.add_argument(
        "--strict-account",
        action="store_true",
        help="Require the updated account to match an active predefined account",
    )
    update_entry.set_defaults(func=cmd_update_entry)

    update_recurring = subparsers.add_parser("update-recurring", help="Update one recurring transaction by id")
    update_recurring.add_argument("--id", type=int, required=True, help="Recurring transaction id to update")
    update_recurring.add_argument("--type", choices=["expense", "income"], help="Updated transaction type")
    update_recurring.add_argument("--amount", help="Updated positive amount")
    update_recurring.add_argument("--currency", help="Updated currency code")
    update_recurring.add_argument("--category", help="Updated category name")
    update_recurring.add_argument("--account", help="Updated wallet name or wallet:currency")
    update_recurring.add_argument("--description", help="Updated short description")
    update_recurring.add_argument("--note", help="Updated note; use an empty string to clear it")
    update_recurring.add_argument("--frequency", choices=sorted(RECURRING_FREQUENCIES), help="Updated frequency")
    update_recurring.add_argument("--interval", type=int, help="Updated repeat interval")
    update_recurring.add_argument("--next-date", help="Updated next due date in YYYY-MM-DD")
    update_recurring.add_argument("--source-text", help="Updated original natural-language prompt")
    active_toggle = update_recurring.add_mutually_exclusive_group()
    active_toggle.add_argument("--activate", action="store_true", help="Activate this recurring transaction")
    active_toggle.add_argument("--deactivate", action="store_true", help="Deactivate this recurring transaction")
    update_recurring.add_argument(
        "--strict-category",
        action="store_true",
        help="Require the category to match an active predefined category",
    )
    update_recurring.add_argument(
        "--strict-account",
        action="store_true",
        help="Require the account to match an active predefined account",
    )
    update_recurring.set_defaults(func=cmd_update_recurring)

    delete_entry = subparsers.add_parser("delete-entry", help="Delete one transaction by id")
    delete_entry.add_argument("--id", type=int, required=True, help="Entry id to delete")
    delete_entry.set_defaults(func=cmd_delete_entry)

    delete_recurring = subparsers.add_parser("delete-recurring", help="Deactivate one recurring transaction by id")
    delete_recurring.add_argument("--id", type=int, required=True, help="Recurring transaction id to deactivate")
    delete_recurring.set_defaults(func=cmd_delete_recurring)

    delete_latest_entry = subparsers.add_parser("delete-latest-entry", help="Delete the latest transaction")
    delete_latest_entry.set_defaults(func=cmd_delete_latest_entry)

    delete_category = subparsers.add_parser("delete-category", help="Deactivate one category by name")
    delete_category.add_argument("--name", required=True, help="Active category name to deactivate")
    delete_category.set_defaults(func=cmd_delete_category)

    update_account = subparsers.add_parser("update-account", help="Rename one wallet account or change its currency")
    update_account.add_argument("--name", required=True, help="Existing wallet spec, for example 支付宝:CNY or 银行卡:USD")
    update_account.add_argument("--new-name", help="Updated wallet name")
    update_account.add_argument("--currency", help="Updated wallet currency code, for example CNY, USD, or EUR")
    update_account.set_defaults(func=cmd_update_account)

    delete_account = subparsers.add_parser("delete-account", help="Deactivate one wallet account")
    delete_account.add_argument("--name", required=True, help="Active wallet spec to deactivate, for example 银行卡:USD")
    delete_account.set_defaults(func=cmd_delete_account)

    return parser


def main():
    if sys.version_info < MIN_PYTHON:
        fail(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required.",
            python_version=".".join(str(part) for part in sys.version_info[:3]),
        )
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "limit") and args.limit <= 0:
        fail("Limit must be greater than zero.", provided=args.limit)
    if hasattr(args, "id") and args.id <= 0:
        fail("Entry id must be greater than zero.", provided=args.id)
    if hasattr(args, "interval") and args.interval is not None and args.interval <= 0:
        fail("Interval must be greater than zero.", provided=args.interval)
    args.func(args)


if __name__ == "__main__":
    main()
