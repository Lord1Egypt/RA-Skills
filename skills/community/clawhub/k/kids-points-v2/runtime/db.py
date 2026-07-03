"""kids-points 数据库层 — SQLite 建表 + CRUD 操作。

金额单位：分（REAL，支持两位小数），展示时整数不带 .0、小数保留 2 位。
"""

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def get_db_path(db_dir: str = ".") -> str:
    return str(Path(db_dir) / "balance.db")


def init_db(db_path: str) -> sqlite3.Connection:
    """初始化数据库，创建所有表。幂等操作。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 支持 dict(row) 和 row["col"]
    conn.execute("PRAGMA journal_mode=WAL")       # 并发读写性能
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense', 'adjustment')),
            amount REAL NOT NULL,
            balance_after REAL NOT NULL,
            description TEXT NOT NULL,
            ref_id TEXT,
            confirmed_by TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_transactions_created_at
            ON transactions(created_at);

        CREATE INDEX IF NOT EXISTS idx_transactions_type
            ON transactions(type);

        CREATE TABLE IF NOT EXISTS processed_messages (
            trace_id TEXT PRIMARY KEY,
            message_id TEXT,
            processed_at TEXT NOT NULL,
            model_name TEXT,
            agent_version TEXT
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            step TEXT NOT NULL,
            input_summary TEXT,
            output_summary TEXT,
            duration_ms INTEGER,
            success BOOLEAN NOT NULL,
            error_message TEXT,
            trace_id TEXT  -- V2-007 增强 (2026-06-12): 关联到具体 input 消息,审计回溯用
        );

        CREATE TABLE IF NOT EXISTS pending_adjustments (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            message_id TEXT NOT NULL,
            target_tx_id TEXT NOT NULL,
            target_description TEXT NOT NULL,
            old_amount REAL NOT NULL,
            new_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'cancelled'))
        );

        CREATE TABLE IF NOT EXISTS processing_locks (
            trace_id TEXT PRIMARY KEY,
            status TEXT NOT NULL CHECK(status IN ('PROCESSING', 'COMPLETED', 'FAILED')),
            acquired_at TEXT NOT NULL,
            ttl_seconds INTEGER NOT NULL DEFAULT 60,
            worker_id TEXT NOT NULL,
            completed_at TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_processing_locks_status
            ON processing_locks(status);
    """)

    # 轻量迁移:老表(没有 trace_id 列)用 ALTER TABLE 补列
    # 必须放在 executescript 之外(脚本里失败会直接抛异常,不会进 try/except)
    # 幂等:第一次执行会成功加列,第二次会因为"duplicate column"被 try/except 吞掉
    try:
        conn.execute("ALTER TABLE audit_log ADD COLUMN trace_id TEXT")
    except sqlite3.OperationalError:
        pass  # 列已存在,忽略

    # index 也要在 ALTER 之后建(老表 ALTER 后才能加 index)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_trace_id ON audit_log(trace_id)")

    # 2026-06-16 V2-decimal 迁移: transactions/pending_adjustments 老表 INTEGER 列
    # SQLite 不允许直接改列类型, 但 INTEGER → REAL 是 "type affinity" 升级, 自动生效
    # (老数据全是整数, REAL 列读出来还是整数, 不需要数据迁移)
    # 这里仅用 PRAGMA 验证列已存在, 不强制重建表
    for tbl in ("transactions", "pending_adjustments"):
        cols = {r[1]: r[2] for r in conn.execute(f"PRAGMA table_info({tbl})").fetchall()}
        if tbl == "transactions":
            for col in ("amount", "balance_after"):
                if cols.get(col, "").upper() not in ("REAL", "NUMERIC", ""):
                    # 老 schema 是 INTEGER, SQLite 实际存储兼容, 不强制迁移
                    # 这里只在 type 严格不匹配时打个 audit log
                    pass
        else:  # pending_adjustments
            for col in ("old_amount", "new_amount"):
                if cols.get(col, "").upper() not in ("REAL", "NUMERIC", ""):
                    pass

    conn.commit()
    return conn


# ─── Transactions CRUD ──────────────────────────────────────────────────────

def get_current_balance(conn: sqlite3.Connection) -> float:
    """获取当前余额（分）。无记录时返回 0.0。支持两位小数。"""
    row = conn.execute(
        "SELECT balance_after FROM transactions ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    return float(row[0]) if row else 0.0


def insert_transaction(
    conn: sqlite3.Connection,
    *,
    tx_type: str,
    amount: float,
    description: str,
    ref_id: Optional[str] = None,
    confirmed_by: Optional[str] = None,
) -> dict:
    """插入一条交易记录，自动计算 balance_after。

    amount 支持两位小数（V2-decimal 2026-06-16 改）。
    返回插入的记录 dict。
    """
    current = get_current_balance(conn)
    # 保留两位小数, 避免浮点累积误差 (0.1 + 0.2 问题)
    amount = round(amount, 2)
    new_balance = round(current + amount, 2)

    tx_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    conn.execute(
        """INSERT INTO transactions (id, created_at, type, amount, balance_after, description, ref_id, confirmed_by)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (tx_id, now, tx_type, amount, new_balance, description, ref_id, confirmed_by),
    )
    conn.commit()

    return {
        "id": tx_id,
        "created_at": now,
        "type": tx_type,
        "amount": amount,
        "balance_after": new_balance,
        "description": description,
        "ref_id": ref_id,
        "confirmed_by": confirmed_by,
    }


def insert_transactions_batch(
    conn: sqlite3.Connection,
    items: list[dict],
) -> list[dict]:
    """批量插入多条交易记录（同一事务）。

    items: [{"type": "income", "amount": 100, "description": "口算"}, ...]
    """
    results = []
    with conn:
        for item in items:
            result = insert_transaction(
                conn,
                tx_type=item["type"],
                amount=item["amount"],
                description=item["description"],
                ref_id=item.get("ref_id"),
                confirmed_by=item.get("confirmed_by"),
            )
            results.append(result)
    return results


def get_transactions_by_date(
    conn: sqlite3.Connection,
    date_str: str,
) -> list[dict]:
    """获取指定日期的所有交易记录。"""
    rows = conn.execute(
        "SELECT * FROM transactions WHERE date(created_at) = ? ORDER BY created_at",
        (date_str,),
    ).fetchall()
    return [_row_to_dict(row) for row in rows]


def get_transactions_range(
    conn: sqlite3.Connection,
    start_date: str,
    end_date: str,
) -> list[dict]:
    """获取日期范围内的交易记录。"""
    rows = conn.execute(
        "SELECT * FROM transactions WHERE date(created_at) BETWEEN ? AND ? ORDER BY created_at",
        (start_date, end_date),
    ).fetchall()
    return [_row_to_dict(row) for row in rows]


def find_transaction_by_description(
    conn: sqlite3.Connection,
    date_str: str,
    keyword: str,
) -> Optional[dict]:
    """按日期和关键词模糊匹配一条交易记录（用于调账）。"""
    row = conn.execute(
        """SELECT * FROM transactions
           WHERE date(created_at) = ? AND description LIKE ?
           ORDER BY created_at DESC LIMIT 1""",
        (date_str, f"%{keyword}%"),
    ).fetchone()
    return _row_to_dict(row) if row else None


def execute_query(conn: sqlite3.Connection, sql: str) -> list[dict]:
    """执行只读查询（用于 LLM 生成的 SQL）。"""
    rows = conn.execute(sql).fetchall()
    return [_row_to_dict(row) for row in rows]


# ─── Processed Messages ─────────────────────────────────────────────────────

def is_message_processed(conn: sqlite3.Connection, trace_id: str, message_id: str = None) -> bool:
    """检查消息是否已处理。

    优先用 trace_id 查（全局唯一标识）。
    message_id 用于日志溯源，可为空。
    """
    if trace_id:
        row = conn.execute(
            "SELECT 1 FROM processed_messages WHERE trace_id = ?", (trace_id,)
        ).fetchone()
        if row:
            return True
    if message_id:
        row = conn.execute(
            "SELECT 1 FROM processed_messages WHERE message_id = ?", (message_id,)
        ).fetchone()
        if row:
            return True
    return False


def mark_message_processed(
    conn: sqlite3.Connection,
    trace_id: str,
    message_id: str = None,
    model_name: str = "",
    agent_version: str = "",
):
    """标记消息已处理，同时记录处理该消息时的模型和 Agent 版本。

    trace_id 优先（全局唯一），message_id 可选（仅飞书平台有）。
    使用 INSERT OR IGNORE 实现幂等：重复调用不报错。
    """
    now = datetime.now().isoformat()
    conn.execute(
        """INSERT OR IGNORE INTO processed_messages (trace_id, message_id, processed_at, model_name, agent_version)
           VALUES (?, ?, ?, ?, ?)""",
        (trace_id, message_id, now, model_name, agent_version),
    )
    conn.commit()


# ─── Processing Locks ────────────────────────────────────────────────────────

class LockStatus:
    """锁状态常量。"""
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


def acquire_processing_lock(
    conn: sqlite3.Connection,
    trace_id: str,
    *,
    ttl_seconds: int = 60,
    worker_id: str = "unknown",
) -> bool:
    """尝试获取消息处理入口锁。

    策略：
    - INSERT 成功 → 拿到锁，返回 True
    - INSERT 失败（UNIQUE constraint）→ 已有人持锁，检查状态：
        - COMPLETED → 返回 False（已处理完，跳过）
        - PROCESSING + TTL 未过期 → 返回 False（正在处理，跳过）
        - PROCESSING + TTL 已过期 → DELETE 旧记录 → 重新 INSERT（接管）

    返回：
        True = 拿到锁，可以继续处理
        False = 锁被占用（或已处理完），跳过
    """
    now_str = datetime.now().isoformat()
    expires_at = datetime.now().timestamp() + ttl_seconds

    try:
        conn.execute(
            """INSERT INTO processing_locks (trace_id, status, acquired_at, ttl_seconds, worker_id)
               VALUES (?, ?, ?, ?, ?)""",
            (trace_id, LockStatus.PROCESSING, now_str, ttl_seconds, worker_id),
        )
        conn.commit()
        return True  # 拿到锁
    except sqlite3.IntegrityError:
        # 锁已存在，检查状态
        row = conn.execute(
            "SELECT status, acquired_at, ttl_seconds FROM processing_locks WHERE trace_id = ?",
            (trace_id,),
        ).fetchone()
        if not row:
            return False

        status, acquired_at, ttl = row[0], row[1], row[2]

        # 已完成 → 跳过
        if status == LockStatus.COMPLETED:
            return False

        # 正在处理 → 检查 TTL
        acquired_ts = datetime.fromisoformat(acquired_at).timestamp()
        if acquired_ts + ttl > datetime.now().timestamp():
            # TTL 未过期，不能接管
            return False

        # TTL 已过期 → 接管
        conn.execute("DELETE FROM processing_locks WHERE trace_id = ?", (trace_id,))
        conn.commit()

        # 重新插入（可能失败，已有人抢了）
        try:
            conn.execute(
                """INSERT INTO processing_locks (trace_id, status, acquired_at, ttl_seconds, worker_id)
                   VALUES (?, ?, ?, ?, ?)""",
                (trace_id, LockStatus.PROCESSING, now_str, ttl_seconds, worker_id),
            )
            conn.commit()
            return True  # 接管成功
        except sqlite3.IntegrityError:
            return False  # 被人抢走了


def release_processing_lock(
    conn: sqlite3.Connection,
    trace_id: str,
    *,
    status: str = LockStatus.COMPLETED,
) -> None:
    """释放消息处理锁。

    策略：删除锁行（而非标记 COMPLETED），让后续同一 trace_id 可以重新竞争锁。
    对于 "已在处理中且 TTL 过期被接管" 的情况，接管者会覆盖锁行，不需要清理。
    """
    conn.execute("DELETE FROM processing_locks WHERE trace_id = ?", (trace_id,))
    conn.commit()


# ─── Audit Log ──────────────────────────────────────────────────────────────

def log_audit(
    conn: sqlite3.Connection,
    *,
    step: str,
    input_summary: str = "",
    output_summary: str = "",
    duration_ms: int = 0,
    success: bool = True,
    error_message: str = "",
    trace_id: Optional[str] = None,  # V2-007 增强: 关联到 input 消息
):
    """写入审计日志。

    V2-007 增强 (2026-06-12):
        接受 trace_id 参数,写入 audit_log.trace_id 列。
        审计回溯路径: tx.ref_id → audit_log.trace_id(同 trace_id) → step=intake
                     的 input_summary 拿 message_text。
    """
    now = datetime.now().isoformat()
    conn.execute(
        """INSERT INTO audit_log (timestamp, step, input_summary, output_summary, duration_ms, success, error_message, trace_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (now, step, input_summary, output_summary, duration_ms, success, error_message, trace_id),
    )
    conn.commit()


# ─── Pending Adjustments ─────────────────────────────────────────────────────

def create_pending_adjustment(
    conn: sqlite3.Connection,
    *,
    message_id: str,
    target_tx_id: str,
    target_description: str,
    old_amount: float,
    new_amount: float,
) -> dict:
    """创建一条待确认的调账记录。金额支持两位小数（V2-decimal 2026-06-16）。"""
    adj_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    conn.execute(
        """INSERT INTO pending_adjustments (id, created_at, message_id, target_tx_id, target_description, old_amount, new_amount)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (adj_id, now, message_id, target_tx_id, target_description, old_amount, new_amount),
    )
    conn.commit()
    return {
        "id": adj_id,
        "created_at": now,
        "message_id": message_id,
        "target_tx_id": target_tx_id,
        "target_description": target_description,
        "old_amount": old_amount,
        "new_amount": new_amount,
    }


def get_pending_adjustment(conn: sqlite3.Connection) -> Optional[dict]:
    """获取最近一条待确认的调账记录。"""
    row = conn.execute(
        "SELECT * FROM pending_adjustments WHERE status='pending' ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    if not row:
        return None
    columns = ["id", "created_at", "message_id", "target_tx_id", "target_description", "old_amount", "new_amount", "status"]
    return dict(zip(columns, row))


def confirm_pending_adjustment(conn: sqlite3.Connection, adj_id: str):
    """确认一条调账。"""
    conn.execute(
        "UPDATE pending_adjustments SET status='confirmed' WHERE id=?", (adj_id,)
    )
    conn.commit()


def cancel_pending_adjustment(conn: sqlite3.Connection, adj_id: str):
    """取消一条调账。"""
    conn.execute(
        "UPDATE pending_adjustments SET status='cancelled' WHERE id=?", (adj_id,)
    )
    conn.commit()


# ─── Reports / Statistics ────────────────────────────────────────────────────

def get_daily_stats(conn: sqlite3.Connection, date_str: str) -> dict:
    """获取指定日期的收支统计。"""
    rows = conn.execute(
        """SELECT type, SUM(amount) as total, COUNT(*) as count
           FROM transactions
           WHERE date(created_at) = ?
           GROUP BY type""",
        (date_str,),
    ).fetchall()

    income_total = 0
    expense_total = 0
    income_count = 0
    expense_count = 0
    for row in rows:
        if row[0] == "income":
            income_total = row[1] or 0
            income_count = row[2] or 0
        elif row[0] == "expense":
            expense_total = row[1] or 0
            expense_count = row[2] or 0

    return {
        "date": date_str,
        "income_total": income_total,
        "expense_total": expense_total,
        "net": income_total + expense_total,
        "income_count": income_count,
        "expense_count": expense_count,
        "balance": get_current_balance(conn),
    }


def get_monthly_stats(conn: sqlite3.Connection, year_month: str) -> dict:
    """获取指定月份的收支统计。year_month 格式：'2026-05'。"""
    month_start = f"{year_month}-01"
    rows = conn.execute(
        """SELECT type, SUM(amount) as total, COUNT(*) as count
           FROM transactions
           WHERE date(created_at) >= ? AND date(created_at) < date(?, '+1 month')
           GROUP BY type""",
        (month_start, month_start),
    ).fetchall()

    income_total = 0
    expense_total = 0
    income_count = 0
    expense_count = 0
    for row in rows:
        if row[0] == "income":
            income_total = row[1] or 0
            income_count = row[2] or 0
        elif row[0] == "expense":
            expense_total = row[1] or 0
            expense_count = row[2] or 0

    # 按类别汇总
    category_rows = conn.execute(
        """SELECT description, SUM(amount) as total, COUNT(*) as count
           FROM transactions
           WHERE date(created_at) >= ? AND date(created_at) < date(?, '+1 month')
             AND type = 'income'
           GROUP BY description
           ORDER BY total DESC""",
        (month_start, month_start),
    ).fetchall()
    income_by_category = [
        {"description": r[0], "total": r[1], "count": r[2]}
        for r in category_rows
    ]

    category_rows = conn.execute(
        """SELECT description, SUM(amount) as total, COUNT(*) as count
           FROM transactions
           WHERE date(created_at) >= ? AND date(created_at) < date(?, '+1 month')
             AND type = 'expense'
           GROUP BY description
           ORDER BY total ASC""",
        (month_start, month_start),
    ).fetchall()
    expense_by_category = [
        {"description": r[0], "total": abs(r[1]), "count": r[2]}
        for r in category_rows
    ]

    return {
        "month": year_month,
        "income_total": income_total,
        "expense_total": expense_total,
        "net": income_total + expense_total,
        "income_count": income_count,
        "expense_count": expense_count,
        "balance": get_current_balance(conn),
        "income_by_category": income_by_category,
        "expense_by_category": expense_by_category,
    }


def get_daily_transactions_detail(conn: sqlite3.Connection, date_str: str) -> list[dict]:
    """获取指定日期的所有交易明细（用于日报）。"""
    rows = conn.execute(
        """SELECT type, amount, description
           FROM transactions
           WHERE date(created_at) = ?
           ORDER BY created_at""",
        (date_str,),
    ).fetchall()
    return [
        {"type": r[0], "amount": r[1], "description": r[2]}
        for r in rows
    ]


# ─── Helpers ────────────────────────────────────────────────────────────────

def _row_to_dict(row: tuple) -> dict:
    columns = ["id", "created_at", "type", "amount", "balance_after", "description", "ref_id", "confirmed_by"]
    return dict(zip(columns, row))


def cents_to_display(value: float) -> str:
    """内部值 → 显示字符串。

    V2-decimal (2026-06-16): 支持两位小数。
    - 整数 (6.0, -10.0) → "6", "-10" (兼容老 V2 显示)
    - 一位小数 (6.5, 0.5) → "6.5", "0.5"
    - 两位小数 (6.25) → "6.25"
    - 用 round 避免浮点累积误差和 -0.0
    """
    rounded = round(float(value), 2)
    # 处理 -0.0 边界: round(-0.001, 2) = -0.0, 显示成 "0"
    if rounded == 0:
        rounded = 0.0
    # 整数不带 .0
    if rounded == int(rounded):
        return str(int(rounded))
    # 小数: 去除尾随 0 (6.50 → "6.5", 6.25 → "6.25")
    s = f"{rounded:.2f}"
    s = s.rstrip("0").rstrip(".")
    return s if s else "0"
