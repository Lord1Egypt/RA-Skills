"""
Item Management - SQLite Database Module
Handles all CRUD operations for items, subitems, and history tracking.

Data is stored in the user's workspace directory (~/.qclaw/workspace/item-management-data/)
to avoid data loss when the skill is updated.
"""
import sqlite3
import json
import os
from datetime import datetime, date
from typing import Optional

# ──────────────────────────────────────────────
# Data Path - Store in USER workspace, NOT inside skill dir
# Works cross-platform: Windows (C:\Users\name), macOS (/Users/name), Linux (/home/name)
# ──────────────────────────────────────────────
def _get_workspace_dir() -> str:
    """
    Get the user's workspace data directory.
    Priority:
    1. OPENCLAW_WORKSPACE env var (for OpenClaw users)
    2. XDG_DATA_HOME env var (Linux/macOS standard)
    3. ~/Library/Application Support/item-management (macOS)
    4. ~/.local/share/item-management (Linux)
    5. ~/item-management-data (Windows/macOS/Linux fallback)
    """
    import platform
    system = platform.system()
    
    # 1. OpenClaw workspace env var
    if os.environ.get("OPENCLAW_WORKSPACE"):
        return os.path.join(os.environ["OPENCLAW_WORKSPACE"], "item-management-data")
    
    # 2. XDG Data Home (Linux/macOS standard)
    if os.environ.get("XDG_DATA_HOME"):
        base = os.environ["XDG_DATA_HOME"]
        return os.path.join(base, "item-management")
    
    home = os.path.expanduser("~")
    
    # 3. macOS: ~/Library/Application Support/
    if system == "Darwin":
        return os.path.join(home, "Library", "Application Support", "item-management")
    
    # 4. Linux: ~/.local/share/
    if system == "Linux":
        return os.path.join(home, ".local", "share", "item-management")
    
    # 5. Windows fallback or unknown: ~/item-management-data
    return os.path.join(home, "item-management-data")

def get_db_path() -> str:
    """Get the database path (in user workspace)."""
    return os.path.join(_get_workspace_dir(), "items.db")

def get_backup_dir() -> str:
    """Get the backup directory (in user workspace)."""
    backup_dir = os.path.join(_get_workspace_dir(), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir

DB_PATH = get_db_path()  # Default path for backward compat

def _get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema."""
    conn = _get_conn()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT DEFAULT '',
            quantity INTEGER DEFAULT 1,
            unit TEXT DEFAULT '个',
            production_date TEXT,
            expiry_date TEXT,
            warranty_date TEXT,
            opened_date TEXT,
            location TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            price REAL,
            tags TEXT DEFAULT '[]',
            image_path TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS subitems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            unit TEXT DEFAULT '个',
            production_date TEXT,
            expiry_date TEXT,
            opened_date TEXT,
            notes TEXT DEFAULT '',
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (parent_id) REFERENCES items(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            subitem_id INTEGER,
            field TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            changed_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
            FOREIGN KEY (subitem_id) REFERENCES subitems(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_items_expiry ON items(expiry_date);
        CREATE INDEX IF NOT EXISTS idx_items_brand ON items(brand);
        CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);
        CREATE INDEX IF NOT EXISTS idx_items_created ON items(created_at);
        CREATE INDEX IF NOT EXISTS idx_subitems_parent ON subitems(parent_id);
        CREATE INDEX IF NOT EXISTS idx_history_item ON history(item_id);
    """)
    conn.commit()
    conn.close()

# ──────────────────────────────────────────────
# Items CRUD
# ──────────────────────────────────────────────

def add_item(
    name: str,
    brand: str = "",
    quantity: int = 1,
    unit: str = "个",
    production_date: str = None,
    expiry_date: str = None,
    warranty_date: str = None,
    opened_date: str = None,
    location: str = "",
    notes: str = "",
    price: float = None,
    tags: list = None,
    image_path: str = None,
) -> int:
    """Add a new item. Returns item id."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO items (name, brand, quantity, unit, production_date, expiry_date,
            warranty_date, opened_date, location, notes, price, tags, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, brand, quantity, unit, production_date, expiry_date, warranty_date,
          opened_date, location, notes, price, json.dumps(tags or [], ensure_ascii=False), image_path))
    item_id = c.lastrowid
    conn.commit()
    conn.close()
    return item_id

def get_item(item_id: int) -> Optional[dict]:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_item(row)

def list_items(sort_by: str = "name", order: str = "asc", filter_tag: str = None) -> list:
    """List all items. sort_by: name | brand | expiry_date | created_at | quantity"""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    allowed_sorts = {
        "name": "name",
        "brand": "brand",
        "expiry_date": "expiry_date",
        "created_at": "created_at",
        "quantity": "quantity",
        "price": "price",
    }
    col = allowed_sorts.get(sort_by, "name")
    direction = "ASC" if order == "asc" else "DESC"
    
    # Handle NULL expiry dates - put them last when sorting ascending
    if col == "expiry_date":
        sort_clause = f"expiry_date IS NULL, expiry_date {direction}" if direction == "ASC" else f"expiry_date IS NOT NULL, expiry_date {direction}"
    else:
        sort_clause = f"{col} {direction}"
    
    if filter_tag:
        c.execute(f"SELECT * FROM items WHERE tags LIKE ? ORDER BY {sort_clause}", (f"%{filter_tag}%",))
    else:
        c.execute(f"SELECT * FROM items ORDER BY {sort_clause}")
    rows = c.fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

def update_item(item_id: int, **fields) -> bool:
    """Update item fields. Returns True if changed, False if not found."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    
    # Track history for specific fields
    history_fields = {"price", "opened_date", "status", "quantity"}
    for f in history_fields:
        if f in fields:
            c.execute(f"SELECT {f} FROM items WHERE id = ?", (item_id,))
            old = c.fetchone()
            if old and old[0] != fields[f]:
                _add_history(conn, item_id, None, f, str(old[0]), str(fields[f]))
    
    allowed = {
        "name", "brand", "quantity", "unit", "production_date", "expiry_date",
        "warranty_date", "opened_date", "location", "notes", "price", "tags",
        "image_path", "status"
    }
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return False
    
    if "tags" in updates and isinstance(updates["tags"], list):
        updates["tags"] = json.dumps(updates["tags"], ensure_ascii=False)
    
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    vals = list(updates.values())
    vals.append(item_id)
    # Always update updated_at via raw SQL to avoid binding issues
    if updates:
        c2 = conn.cursor()
        c2.execute(f"UPDATE items SET updated_at = datetime('now') WHERE id = ?", (item_id,))
        conn.commit()
    
    c.execute(f"UPDATE items SET {set_clause} WHERE id = ?", vals)
    if c.rowcount == 0:
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True

def delete_item(item_id: int) -> bool:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    ok = c.rowcount > 0
    conn.commit()
    conn.close()
    return ok

# ──────────────────────────────────────────────
# Subitems CRUD
# ──────────────────────────────────────────────

def add_subitem(parent_id: int, name: str, quantity: int = 1, unit: str = "个",
                production_date: str = None, expiry_date: str = None,
                opened_date: str = None, notes: str = "") -> int:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO subitems (parent_id, name, quantity, unit, production_date,
            expiry_date, opened_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (parent_id, name, quantity, unit, production_date, expiry_date, opened_date, notes))
    sub_id = c.lastrowid
    # Update parent updated_at
    c.execute("UPDATE items SET updated_at = datetime('now') WHERE id = ?", (parent_id,))
    conn.commit()
    conn.close()
    return sub_id

def list_subitems(parent_id: int) -> list:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM subitems WHERE parent_id = ? ORDER BY created_at", (parent_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_subitem(sub_id: int, **fields) -> bool:
    conn = _get_conn()
    c = conn.cursor()
    history_fields = {"price", "status", "quantity"}
    for f in history_fields:
        if f in fields:
            c.execute(f"SELECT {f} FROM subitems WHERE id = ?", (sub_id,))
            old = c.fetchone()
            if old and str(old[0]) != str(fields[f]):
                c.execute("SELECT parent_id FROM subitems WHERE id = ?", (sub_id,))
                parent = c.fetchone()
                _add_history(conn, parent["parent_id"] if parent else None, sub_id, f, str(old[0]), str(fields[f]))
    
    allowed = {"name", "quantity", "unit", "production_date", "expiry_date", "opened_date", "notes", "status"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return False
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    vals = list(updates.values())
    vals.append(sub_id)
    c.execute(f"UPDATE subitems SET {set_clause} WHERE id = ?", vals)
    ok = c.rowcount > 0
    conn.commit()
    conn.close()
    return ok

def delete_subitem(sub_id: int) -> bool:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM subitems WHERE id = ?", (sub_id,))
    ok = c.rowcount > 0
    conn.commit()
    conn.close()
    return ok

# ──────────────────────────────────────────────
# History
# ──────────────────────────────────────────────

def _add_history(conn, item_id, subitem_id, field, old_value, new_value):
    c = conn.cursor()
    c.execute("""
        INSERT INTO history (item_id, subitem_id, field, old_value, new_value)
        VALUES (?, ?, ?, ?, ?)
    """, (item_id, subitem_id, field, old_value, new_value))

def get_history(item_id: int) -> list:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM history WHERE item_id = ? ORDER BY changed_at DESC
    """, (item_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ──────────────────────────────────────────────
# Expiry & Notifications
# ──────────────────────────────────────────────

def get_expiring_items(days: int = 7) -> list:
    """Get items expiring within N days."""
    init_db()
    today = date.today().isoformat()
    future = (date.today().replace(day=25) if date.today().month == 2 else 
              (date.today().replace(day=28) if date.today().month == 2 else
               date.today().replace(day=30) if date.today().month in [4,6,9,11] else
               date.today().replace(day=31))).isoformat()
    # Actually use timedelta
    from datetime import timedelta
    future = (date.today() + timedelta(days=days)).isoformat()
    
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM items
        WHERE expiry_date IS NOT NULL
          AND expiry_date != ''
          AND expiry_date >= ?
          AND expiry_date <= ?
        ORDER BY expiry_date
    """, (today, future))
    rows = c.fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

def get_expired_items() -> list:
    """Get expired items."""
    today = date.today().isoformat()
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM items
        WHERE expiry_date IS NOT NULL
          AND expiry_date != ''
          AND expiry_date < ?
        ORDER BY expiry_date
    """, (today,))
    rows = c.fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

# ──────────────────────────────────────────────
# Statistics
# ──────────────────────────────────────────────

def get_stats() -> dict:
    """Get overall statistics."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) as total, SUM(quantity) as total_qty, SUM(price * quantity) as total_value FROM items WHERE status='active'")
    item_stats = dict(c.fetchone())
    
    c.execute("SELECT COUNT(*) as total FROM subitems WHERE status='active'")
    sub_count = c.fetchone()["total"]
    
    c.execute("SELECT COUNT(DISTINCT brand) as total FROM items WHERE brand != '' AND brand IS NOT NULL")
    brand_count = c.fetchone()["total"]
    
    c.execute("""
        SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count, SUM(price * quantity) as value
        FROM items
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    """)
    monthly = [dict(r) for r in c.fetchall()]
    
    c.execute("""
        SELECT strftime('%Y-%m', changed_at) as month, field, COUNT(*) as count
        FROM history
        GROUP BY month, field
        ORDER BY month DESC
        LIMIT 20
    """)
    changes = [dict(r) for r in c.fetchall()]
    
    conn.close()
    return {
        "total_items": item_stats["total"] or 0,
        "total_quantity": item_stats["total_qty"] or 0,
        "total_value": item_stats["total_value"] or 0.0,
        "total_subitems": sub_count,
        "total_brands": brand_count,
        "monthly_new_items": monthly,
        "recent_changes": changes,
    }

# ──────────────────────────────────────────────
# Search
# ──────────────────────────────────────────────

def search_items(query: str, field: str = None) -> list:
    """Search items by name, brand, location, tags, or notes."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    like = f"%{query}%"
    if field:
        c.execute(f"SELECT * FROM items WHERE {field} LIKE ? ORDER BY name", (like,))
    else:
        c.execute("""
            SELECT * FROM items WHERE
                name LIKE ? OR brand LIKE ? OR location LIKE ? OR notes LIKE ? OR tags LIKE ?
            ORDER BY name
        """, (like, like, like, like, like))
    rows = c.fetchall()
    conn.close()
    return [_row_to_item(r) for r in rows]

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _row_to_item(row: sqlite3.Row) -> dict:
    d = dict(row)
    if "tags" in d and d["tags"]:
        try:
            d["tags"] = json.loads(d["tags"])
        except Exception:
            d["tags"] = []
    return d

# ──────────────────────────────────────────────
# Backup & Restore - JSON export/import for cloud sync
# ──────────────────────────────────────────────

def export_all_json() -> dict:
    """Export all data as a dictionary (for backup)."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    
    c.execute("SELECT * FROM items")
    items = [_row_to_item(r) for r in c.fetchall()]
    
    c.execute("SELECT * FROM subitems")
    subitems = [dict(r) for r in c.fetchall()]
    
    c.execute("SELECT * FROM history ORDER BY changed_at DESC")
    history = [dict(r) for r in c.fetchall()]
    
    conn.close()
    
    return {
        "version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "items": items,
        "subitems": subitems,
        "history": history,
    }

def import_all_json(data: dict, merge: bool = False) -> dict:
    """
    Import data from JSON backup.
    - merge=True: add items that don't exist (by name), skip duplicates
    - merge=False: clear all and import fresh (full restore)
    Returns: {"added": N, "skipped": N, "errors": []}
    """
    if not data or data.get("version") != "1.0":
        raise ValueError("无效的备份文件格式")
    
    conn = _get_conn()
    c = conn.cursor()
    stats = {"added": 0, "skipped": 0, "errors": []}
    
    if not merge:
        # Full restore: clear existing data
        c.executescript("DELETE FROM history; DELETE FROM subitems; DELETE FROM items;")
    
    # Import items
    for item in data.get("items", []):
        try:
            if merge:
                # Check if item with same name exists
                c.execute("SELECT id FROM items WHERE name = ?", (item["name"],))
                if c.fetchone():
                    stats["skipped"] += 1
                    continue
            tags = item.pop("tags", [])
            if isinstance(tags, list):
                tags = json.dumps(tags, ensure_ascii=False)
            c.execute("""
                INSERT INTO items (name, brand, quantity, unit, production_date, expiry_date,
                    warranty_date, opened_date, location, notes, price, tags, image_path, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["name"], item.get("brand", ""), item.get("quantity", 1), item.get("unit", "个"),
                item.get("production_date"), item.get("expiry_date"), item.get("warranty_date"),
                item.get("opened_date"), item.get("location", ""), item.get("notes", ""),
                item.get("price"), tags, item.get("image_path"), item.get("status", "active"),
                item.get("created_at", datetime.now().isoformat())
            ))
            stats["added"] += 1
        except Exception as e:
            stats["errors"].append(f"物品「{item.get('name','?')}」导入失败: {e}")
    
    # Import subitems
    subitem_id_map = {}  # old_id -> new_id
    for sub in data.get("subitems", []):
        try:
            c.execute("""
                INSERT INTO subitems (parent_id, name, quantity, unit, production_date,
                    expiry_date, opened_date, notes, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sub["parent_id"], sub["name"], sub.get("quantity", 1), sub.get("unit", "个"),
                sub.get("production_date"), sub.get("expiry_date"), sub.get("opened_date"),
                sub.get("notes", ""), sub.get("status", "active"), sub.get("created_at", datetime.now().isoformat())
            ))
            old_id = sub["id"]
            new_id = c.lastrowid
            # For merge mode, we can't easily map parent_ids, so skip history for merged subitems
            if not merge:
                subitem_id_map[old_id] = new_id
        except Exception as e:
            stats["errors"].append(f"子物品「{sub.get('name','?')}」导入失败: {e}")
    
    # Import history (only for full restore, not merge)
    if not merge:
        for h in data.get("history", []):
            try:
                c.execute("""
                    INSERT INTO history (item_id, subitem_id, field, old_value, new_value, changed_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    h.get("item_id"), h.get("subitem_id"), h["field"],
                    h.get("old_value"), h.get("new_value"), h.get("changed_at", datetime.now().isoformat())
                ))
            except Exception:
                pass  # History is non-critical
    
    conn.commit()
    conn.close()
    return stats

def auto_backup() -> str:
    """Create an automatic timestamped backup. Returns backup file path."""
    data = export_all_json()
    backup_dir = get_backup_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(backup_dir, f"backup_{ts}.json")
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname

def list_backups() -> list:
    """List all backup files, newest first."""
    backup_dir = get_backup_dir()
    files = []
    for f in os.listdir(backup_dir):
        if f.startswith("backup_") and f.endswith(".json"):
            path = os.path.join(backup_dir, f)
            size = os.path.getsize(path)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            files.append({"name": f, "path": path, "size": size, "mtime": mtime.strftime("%Y-%m-%d %H:%M:%S")})
    return sorted(files, key=lambda x: x["mtime"], reverse=True)

def get_latest_backup() -> str:
    """Get the path to the latest backup file."""
    backups = list_backups()
    return backups[0]["path"] if backups else None

def get_data_info() -> dict:
    """Get data storage info (path, size, item count)."""
    db = get_db_path()
    info = {
        "db_path": db,
        "db_exists": os.path.exists(db),
        "db_size": os.path.getsize(db) if os.path.exists(db) else 0,
        "backup_dir": get_backup_dir(),
        "backup_count": len(list_backups()),
    }
    return info
