"""
Nex PriceWatch Storage Module
SQLite database for price tracking and history
Copyright 2026 Nex AI (Kevin Blancaflor)
MIT-0 License
"""

import sqlite3
import json
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import DB_PATH, DATA_DIR, SNAPSHOTS_DIR


def init_db():
    """Initialize database with required tables."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Create targets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            url TEXT NOT NULL,
            competitor_name TEXT,
            type TEXT NOT NULL DEFAULT 'competitor',
            selector_type TEXT NOT NULL,
            selector TEXT NOT NULL,
            currency TEXT DEFAULT 'EUR',
            current_price REAL,
            previous_price REAL,
            last_checked TIMESTAMP,
            check_interval_hours INTEGER DEFAULT 24,
            enabled INTEGER DEFAULT 1,
            tags TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create price_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER NOT NULL,
            price REAL NOT NULL,
            raw_text TEXT,
            snapshot_hash TEXT,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE
        )
    """)

    # Create alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            old_price REAL,
            new_price REAL,
            change_pct REAL,
            message TEXT,
            sent INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_target_id ON price_history(target_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_checked_at ON price_history(checked_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_alert_target ON alerts(target_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_alert_created ON alerts(created_at)")

    conn.commit()
    conn.close()


def get_conn():
    """Get database connection."""
    return sqlite3.connect(str(DB_PATH))


def save_target(name: str, url: str, selector_type: str, selector: str,
                competitor_name: Optional[str] = None, type_: str = "competitor",
                currency: str = "EUR", check_interval_hours: int = 24,
                tags: Optional[str] = None, notes: Optional[str] = None) -> int:
    """Save or update a price target."""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO targets
        (name, url, competitor_name, type, selector_type, selector, currency,
         check_interval_hours, tags, notes, enabled)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    """, (name, url, competitor_name, type_, selector_type, selector,
          currency, check_interval_hours, tags, notes))

    conn.commit()
    target_id = cursor.lastrowid
    conn.close()

    return target_id


def get_target(name: str) -> Optional[Dict[str, Any]]:
    """Get target by name."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM targets WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return _row_to_dict_target(cursor.description, row)
    return None


def get_target_by_id(target_id: int) -> Optional[Dict[str, Any]]:
    """Get target by ID."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM targets WHERE id = ?", (target_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return _row_to_dict_target(cursor.description, row)
    return None


def list_targets(enabled_only: bool = False) -> List[Dict[str, Any]]:
    """List all targets."""
    conn = get_conn()
    cursor = conn.cursor()

    if enabled_only:
        cursor.execute("SELECT * FROM targets WHERE enabled = 1 ORDER BY name")
    else:
        cursor.execute("SELECT * FROM targets ORDER BY name")

    rows = cursor.fetchall()
    conn.close()

    return [_row_to_dict_target(cursor.description, row) for row in rows]


def update_target(name: str, **kwargs) -> bool:
    """Update a target."""
    target = get_target(name)
    if not target:
        return False

    allowed_fields = ['url', 'competitor_name', 'type', 'selector_type', 'selector',
                      'currency', 'check_interval_hours', 'enabled', 'tags', 'notes']

    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    if not updates:
        return False

    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [name]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE targets SET {set_clause} WHERE name = ?", values)
    conn.commit()
    conn.close()

    return True


def delete_target(name: str) -> bool:
    """Delete a target and its history."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM targets WHERE name = ?", (name,))
    conn.commit()
    conn.close()

    return cursor.rowcount > 0


def save_price(target_id: int, price: float, raw_text: str,
               snapshot_hash: Optional[str] = None) -> int:
    """Save price to history and update current price."""
    conn = get_conn()
    cursor = conn.cursor()

    # Get current price before update
    cursor.execute("SELECT current_price FROM targets WHERE id = ?", (target_id,))
    row = cursor.fetchone()
    previous_price = row[0] if row else None

    # Save to history
    cursor.execute("""
        INSERT INTO price_history (target_id, price, raw_text, snapshot_hash)
        VALUES (?, ?, ?, ?)
    """, (target_id, price, raw_text, snapshot_hash))

    history_id = cursor.lastrowid

    # Update current and previous prices
    cursor.execute("""
        UPDATE targets
        SET current_price = ?, previous_price = ?, last_checked = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (price, previous_price, target_id))

    conn.commit()
    conn.close()

    return history_id


def get_price_history(target_id: int, since: Optional[datetime] = None,
                      limit: Optional[int] = 100) -> List[Dict[str, Any]]:
    """Get price history for a target."""
    conn = get_conn()
    cursor = conn.cursor()

    try:
        if limit is None:
            limit = 999999

        if since:
            cursor.execute("""
                SELECT * FROM price_history
                WHERE target_id = ? AND checked_at >= ?
                ORDER BY checked_at DESC
                LIMIT ?
            """, (target_id, since.isoformat() if isinstance(since, datetime) else since, limit))
        else:
            cursor.execute("""
                SELECT * FROM price_history
                WHERE target_id = ?
                ORDER BY checked_at DESC
                LIMIT ?
            """, (target_id, limit))

        rows = cursor.fetchall()
    finally:
        conn.close()

    return [_row_to_dict(cursor.description, row) for row in rows]


def get_latest_prices() -> List[Dict[str, Any]]:
    """Get latest prices for all targets."""
    targets = list_targets(enabled_only=True)
    results = []

    for target in targets:
        history = get_price_history(target['id'], limit=1)
        if history:
            results.append({
                **target,
                'latest_price': history[0]['price'],
                'latest_checked': history[0]['checked_at']
            })
        else:
            results.append({
                **target,
                'latest_price': target.get('current_price'),
                'latest_checked': target.get('last_checked')
            })

    return results


def detect_price_change(target_id: int, new_price: float) -> Dict[str, Any]:
    """Detect price change and return change info."""
    target = get_target_by_id(target_id)
    if not target:
        return {'change': False, 'type': 'unknown'}

    old_price = target.get('current_price')

    if old_price is None:
        return {'change': False, 'type': 'new_price', 'old_price': None, 'new_price': new_price}

    if new_price == old_price:
        return {'change': False, 'type': 'no_change', 'old_price': old_price, 'new_price': new_price}

    change_pct = ((new_price - old_price) / old_price * 100) if old_price != 0 else 0

    if new_price > old_price:
        change_type = 'increase'
    else:
        change_type = 'decrease'

    return {
        'change': True,
        'type': change_type,
        'old_price': old_price,
        'new_price': new_price,
        'change_pct': round(change_pct, 2),
        'change_amount': round(new_price - old_price, 2)
    }


def get_price_stats(target_id: int) -> Dict[str, Any]:
    """Get price statistics for a target."""
    history = get_price_history(target_id, limit=None)

    if not history:
        return {'count': 0, 'min': None, 'max': None, 'avg': None, 'trend': None}

    prices = [h['price'] for h in history]

    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices) / len(prices)

    # Determine trend (comparing recent vs older)
    recent = prices[:5] if len(prices) >= 5 else prices
    older = prices[-5:] if len(prices) >= 5 else prices

    recent_avg = sum(recent) / len(recent)
    older_avg = sum(older) / len(older)

    if recent_avg > older_avg:
        trend = 'up'
    elif recent_avg < older_avg:
        trend = 'down'
    else:
        trend = 'stable'

    return {
        'count': len(prices),
        'min': round(min_price, 2),
        'max': round(max_price, 2),
        'avg': round(avg_price, 2),
        'trend': trend,
        'recent_avg': round(recent_avg, 2)
    }


def save_alert(target_id: int, alert_type: str, old_price: Optional[float],
               new_price: float, change_pct: float, message: str) -> int:
    """Save an alert."""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (target_id, alert_type, old_price, new_price, change_pct, message, sent)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (target_id, alert_type, old_price, new_price, change_pct, message))

    conn.commit()
    alert_id = cursor.lastrowid
    conn.close()

    return alert_id


def get_all_changes(since: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """Get all recent price changes (alerts)."""
    conn = get_conn()
    cursor = conn.cursor()

    if since:
        cursor.execute("""
            SELECT a.*, t.name as target_name, t.competitor_name
            FROM alerts a
            JOIN targets t ON a.target_id = t.id
            WHERE a.created_at >= ?
            ORDER BY a.created_at DESC
        """, (since.isoformat(),))
    else:
        cursor.execute("""
            SELECT a.*, t.name as target_name, t.competitor_name
            FROM alerts a
            JOIN targets t ON a.target_id = t.id
            ORDER BY a.created_at DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    return [_row_to_dict(cursor.description, row) for row in rows]


def search_targets(query: str) -> List[Dict[str, Any]]:
    """Search targets by name, competitor name, or tags."""
    conn = get_conn()
    cursor = conn.cursor()

    search_term = f"%{query}%"
    cursor.execute("""
        SELECT * FROM targets
        WHERE name LIKE ? OR competitor_name LIKE ? OR tags LIKE ?
        ORDER BY name
    """, (search_term, search_term, search_term))

    rows = cursor.fetchall()
    conn.close()

    return [_row_to_dict_target(cursor.description, row) for row in rows]


def export_history(target_id: int, format_: str = 'json') -> str:
    """Export price history."""
    history = get_price_history(target_id, limit=None)
    target = get_target_by_id(target_id)

    if format_ == 'csv':
        lines = [f"target,date,price,raw_text"]
        for h in history:
            lines.append(f'{target["name"]},{h["checked_at"]},{h["price"]},"{h["raw_text"]}"')
        return "\n".join(lines)
    else:  # json
        return json.dumps({
            'target': target,
            'history': history
        }, indent=2, default=str)


def mark_alert_sent(alert_id: int):
    """Mark an alert as sent."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE alerts SET sent = 1 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()


def _row_to_dict(description, row):
    """Convert database row to dict."""
    return {description[i][0]: row[i] for i in range(len(description))}


def _row_to_dict_target(description, row):
    """Convert target row to dict with parsed values."""
    d = _row_to_dict(description, row)
    if d.get('tags'):
        d['tags'] = d['tags'].split(',')
    return d
