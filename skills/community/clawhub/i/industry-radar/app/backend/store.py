"""
数据访问层（本地演示使用 SQLite；云端替换为 RDS MySQL）。

表结构与《方案设计》第 5 节保持一致：
  user / subscription / source / custom_source / article / briefing / briefing_section / push_log

之所以用 SQLite：本地零依赖即可跑通端到端 Demo；
线上仅需把 `_connect()` 换成 MySQL 连接池即可，SQL 保持兼容。
"""
from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from config import CUSTOM_DISABLE_AFTER_FAILS, DB_PATH

# SQLite 在多线程（FastAPI）下需要 check_same_thread=False + 串行写锁
_LOCK = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS user (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email         TEXT,
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subscription (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    name         TEXT NOT NULL,
    industry_kw  TEXT NOT NULL,
    tech_kw      TEXT NOT NULL,
    extra_kw     TEXT DEFAULT '',
    sources_json TEXT DEFAULT '[]',
    frequency    TEXT DEFAULT 'weekly',
    style        TEXT DEFAULT 'standard',  -- standard 标准周报 / curated 编辑精选
    enabled      INTEGER DEFAULT 1,
    last_run_at  TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_id INTEGER NOT NULL,
    type            TEXT DEFAULT 'rss',
    url             TEXT NOT NULL,
    name            TEXT,
    enabled         INTEGER DEFAULT 1
);

-- 用户自定义订阅源（RSS/Atom）。归属 user_id，可在该用户的多个订阅间复用；
-- url 在同一用户下唯一，避免重复抓取与配额浪费。
CREATE TABLE IF NOT EXISTS custom_source (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    name          TEXT NOT NULL,
    url           TEXT NOT NULL,
    enabled       INTEGER DEFAULT 1,
    status        TEXT DEFAULT 'ok',      -- ok 正常 / failing 失败中 / disabled 连续失败已自动禁用
    fail_count    INTEGER DEFAULT 0,
    last_status   TEXT,                   -- 最近一次抓取的 HTTP 状态或结论
    last_error    TEXT,
    last_fetch_at TEXT,
    created_at    TEXT NOT NULL,
    UNIQUE(user_id, url)
);

CREATE TABLE IF NOT EXISTS article (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_id INTEGER NOT NULL,
    title           TEXT,
    url             TEXT,
    url_hash        TEXT,
    source_name     TEXT,
    published_at    TEXT,
    content         TEXT,
    summary         TEXT,
    score           REAL DEFAULT 0,
    cluster_id      INTEGER DEFAULT -1,
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS briefing (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_id INTEGER NOT NULL,
    title           TEXT,
    period_start    TEXT,
    period_end      TEXT,
    md_path         TEXT,
    pdf_path        TEXT,
    status          TEXT DEFAULT 'done',
    stats_json      TEXT DEFAULT '{}',
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS briefing_section (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    briefing_id     INTEGER NOT NULL,
    cluster_title   TEXT,
    content         TEXT,
    article_ids_json TEXT DEFAULT '[]',
    sort_no         INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS push_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    briefing_id INTEGER NOT NULL,
    channel     TEXT,
    target      TEXT,
    status      TEXT,
    sent_at     TEXT
);

CREATE INDEX IF NOT EXISTS idx_article_sub ON article(subscription_id);
CREATE INDEX IF NOT EXISTS idx_article_hash ON article(subscription_id, url_hash);
CREATE INDEX IF NOT EXISTS idx_briefing_sub ON briefing(subscription_id);
CREATE INDEX IF NOT EXISTS idx_section_briefing ON briefing_section(briefing_id);
CREATE INDEX IF NOT EXISTS idx_custom_source_user ON custom_source(user_id);
"""


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@contextmanager
def _connect():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with _LOCK, _connect() as conn:
        conn.executescript(SCHEMA)
        # 增量迁移：旧库补 style 列（编辑精选模式）
        try:
            conn.execute("ALTER TABLE subscription ADD COLUMN style TEXT DEFAULT 'standard'")
        except sqlite3.OperationalError:
            pass  # 列已存在


def _rows(cur) -> List[Dict[str, Any]]:
    return [dict(r) for r in cur.fetchall()]


# ------------------------------------------------------------------ user
def get_user_by_name(username: str) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute("SELECT * FROM user WHERE username=?", (username,))
        row = cur.fetchone()
        return dict(row) if row else None


def create_user(username: str, password_hash: str, email: str = "") -> int:
    with _LOCK, _connect() as conn:
        cur = conn.execute(
            "INSERT INTO user(username, password_hash, email, created_at) VALUES(?,?,?,?)",
            (username, password_hash, email, now()),
        )
        return cur.lastrowid


# ------------------------------------------------------------ subscription
def create_subscription(
    user_id: int,
    name: str,
    industry_kw: str,
    tech_kw: str,
    extra_kw: str = "",
    sources_json: str = "[]",
    frequency: str = "weekly",
    style: str = "standard",
) -> int:
    with _LOCK, _connect() as conn:
        cur = conn.execute(
            """INSERT INTO subscription
               (user_id, name, industry_kw, tech_kw, extra_kw, sources_json, frequency, style, enabled, created_at)
               VALUES(?,?,?,?,?,?,?,?,1,?)""",
            (user_id, name, industry_kw, tech_kw, extra_kw, sources_json, frequency, style, now()),
        )
        return cur.lastrowid


def list_subscriptions(user_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT * FROM subscription WHERE user_id=? ORDER BY id DESC", (user_id,)
        )
        rows = _rows(cur)
        for r in rows:
            cur2 = conn.execute(
                "SELECT COUNT(*) AS c FROM briefing WHERE subscription_id=?", (r["id"],)
            )
            r["briefing_count"] = cur2.fetchone()["c"]
        return rows


def get_subscription(sub_id: int) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute("SELECT * FROM subscription WHERE id=?", (sub_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def list_enabled_subscriptions() -> List[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute("SELECT * FROM subscription WHERE enabled=1")
        return _rows(cur)


def update_subscription(sub_id: int, fields: Dict[str, Any]) -> None:
    allowed = {"name", "industry_kw", "tech_kw", "extra_kw", "sources_json", "frequency", "style", "enabled"}
    sets, vals = [], []
    for k, v in fields.items():
        if k in allowed:
            sets.append(f"{k}=?")
            vals.append(v)
    if not sets:
        return
    vals.append(sub_id)
    with _LOCK, _connect() as conn:
        conn.execute(f"UPDATE subscription SET {', '.join(sets)} WHERE id=?", vals)


def update_subscription_last_run(sub_id: int) -> None:
    with _LOCK, _connect() as conn:
        conn.execute("UPDATE subscription SET last_run_at=? WHERE id=?", (now(), sub_id))


def delete_subscription(sub_id: int) -> None:
    with _LOCK, _connect() as conn:
        conn.execute("DELETE FROM article WHERE subscription_id=?", (sub_id,))
        conn.execute("DELETE FROM briefing_section WHERE briefing_id IN "
                     "(SELECT id FROM briefing WHERE subscription_id=?)", (sub_id,))
        conn.execute("DELETE FROM briefing WHERE subscription_id=?", (sub_id,))
        conn.execute("DELETE FROM source WHERE subscription_id=?", (sub_id,))
        conn.execute("DELETE FROM subscription WHERE id=?", (sub_id,))


# ----------------------------------------------------------- custom source
def count_custom_sources(user_id: int) -> int:
    with _connect() as conn:
        cur = conn.execute("SELECT COUNT(*) AS c FROM custom_source WHERE user_id=?", (user_id,))
        return int(cur.fetchone()["c"])


def list_custom_sources(user_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT * FROM custom_source WHERE user_id=? ORDER BY id DESC", (user_id,)
        )
        return _rows(cur)


def create_custom_source(user_id: int, name: str, url: str) -> int:
    with _LOCK, _connect() as conn:
        cur = conn.execute(
            """INSERT INTO custom_source(user_id, name, url, enabled, status, fail_count, created_at)
               VALUES(?,?,?,1,'ok',0,?)""",
            (user_id, name, url, now()),
        )
        return cur.lastrowid


def get_custom_source(cs_id: int) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute("SELECT * FROM custom_source WHERE id=?", (cs_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def update_custom_source(cs_id: int, fields: Dict[str, Any]) -> None:
    allowed = {"name", "url", "enabled", "status", "fail_count",
               "last_status", "last_error", "last_fetch_at"}
    sets, vals = [], []
    for k, v in fields.items():
        if k in allowed:
            sets.append(f"{k}=?")
            vals.append(v)
    if not sets:
        return
    vals.append(cs_id)
    with _LOCK, _connect() as conn:
        conn.execute(f"UPDATE custom_source SET {', '.join(sets)} WHERE id=?", vals)


def delete_custom_source(cs_id: int) -> None:
    with _LOCK, _connect() as conn:
        conn.execute("DELETE FROM custom_source WHERE id=?", (cs_id,))


def record_custom_source_result(cs_id: int, ok: bool, detail: str = "") -> None:
    """记录一次抓取结果；连续失败达到阈值自动禁用，避免长期拖累采集。"""
    with _LOCK, _connect() as conn:
        cur = conn.execute(
            "SELECT fail_count, status FROM custom_source WHERE id=?", (cs_id,)
        )
        row = cur.fetchone()
        if not row:
            return
        if ok:
            conn.execute(
                "UPDATE custom_source SET status='ok', fail_count=0, last_status='ok', "
                "last_error=NULL, last_fetch_at=? WHERE id=?",
                (now(), cs_id),
            )
            return
        fails = int(row["fail_count"] or 0) + 1
        status = row["status"] or "ok"
        if fails >= CUSTOM_DISABLE_AFTER_FAILS:
            status = "disabled"
            conn.execute("UPDATE custom_source SET enabled=0 WHERE id=?", (cs_id,))
        elif status != "disabled":
            status = "failing"
        conn.execute(
            "UPDATE custom_source SET status=?, fail_count=?, last_status='error', "
            "last_error=?, last_fetch_at=? WHERE id=?",
            (status, fails, (detail or "")[:300], now(), cs_id),
        )


def custom_source_usage(user_id: int) -> Dict[int, int]:
    """统计每个自定义源被该用户多少个订阅引用，供前端展示「被引用」数量。"""
    usage: Dict[int, int] = {}
    with _connect() as conn:
        cur = conn.execute("SELECT sources_json FROM subscription WHERE user_id=?", (user_id,))
        for r in cur.fetchall():
            try:
                ids = json.loads(r["sources_json"] or "[]")
            except (ValueError, TypeError):
                continue
            for sid in set(ids):
                if isinstance(sid, str) and sid.startswith("cs:"):
                    try:
                        key = int(sid[3:])
                    except ValueError:
                        continue
                    usage[key] = usage.get(key, 0) + 1
    return usage



# ----------------------------------------------------------------- article
def existing_url_hashes(sub_id: int) -> set:
    with _connect() as conn:
        cur = conn.execute("SELECT url_hash FROM article WHERE subscription_id=?", (sub_id,))
        return {r["url_hash"] for r in cur.fetchall()}


def recent_articles(sub_id: int, limit: int = 200) -> List[Dict[str, Any]]:
    """取最近文章用于跨期去重（simhash 比对）。"""
    with _connect() as conn:
        cur = conn.execute(
            "SELECT id, title, url_hash, cluster_id FROM article "
            "WHERE subscription_id=? ORDER BY id DESC LIMIT ?",
            (sub_id, limit),
        )
        return _rows(cur)


def insert_articles(rows: Iterable[Dict[str, Any]]) -> List[int]:
    """插入文章并返回自增主键列表（顺序与入参一一对应）。

    逐行插入而非 executemany，以便可靠地收集每条记录的主键，供
    briefing_section.article_ids_json 回填使用。
    """
    rows = list(rows)
    if not rows:
        return []
    ids: List[int] = []
    with _LOCK, _connect() as conn:
        for r in rows:
            cur = conn.execute(
                """INSERT INTO article
                   (subscription_id, title, url, url_hash, source_name, published_at,
                    content, summary, score, cluster_id, created_at)
                   VALUES(:subscription_id,:title,:url,:url_hash,:source_name,:published_at,
                          :content,:summary,:score,:cluster_id,:created_at)""",
                r,
            )
            ids.append(cur.lastrowid)
    return ids


def list_articles(sub_id: int, limit: int = 100) -> List[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT id,title,url,source_name,published_at,summary,score "
            "FROM article WHERE subscription_id=? ORDER BY score DESC, id DESC LIMIT ?",
            (sub_id, limit),
        )
        return _rows(cur)


# ---------------------------------------------------------------- briefing
def create_briefing(sub_id: int, title: str, period_start: str, period_end: str,
                    md_path: str, status: str = "done", stats: Optional[dict] = None) -> int:
    with _LOCK, _connect() as conn:
        cur = conn.execute(
            """INSERT INTO briefing
               (subscription_id, title, period_start, period_end, md_path, status, stats_json, created_at)
               VALUES(?,?,?,?,?,?,?,?)""",
            (sub_id, title, period_start, period_end, md_path, status,
             json.dumps(stats or {}, ensure_ascii=False), now()),
        )
        return cur.lastrowid


def add_section(briefing_id: int, cluster_title: str, content: str,
                article_ids: List[int], sort_no: int) -> None:
    with _LOCK, _connect() as conn:
        conn.execute(
            """INSERT INTO briefing_section
               (briefing_id, cluster_title, content, article_ids_json, sort_no)
               VALUES(?,?,?,?,?)""",
            (briefing_id, cluster_title, content,
             json.dumps(article_ids, ensure_ascii=False), sort_no),
        )


def list_briefings(sub_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT * FROM briefing WHERE subscription_id=? ORDER BY id DESC", (sub_id,)
        )
        rows = _rows(cur)
        for r in rows:
            r["stats"] = json.loads(r.get("stats_json") or "{}")
        return rows


def get_briefing(briefing_id: int) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        cur = conn.execute("SELECT * FROM briefing WHERE id=?", (briefing_id,))
        row = cur.fetchone()
        if not row:
            return None
        b = dict(row)
        b["stats"] = json.loads(b.get("stats_json") or "{}")
        cur2 = conn.execute(
            "SELECT * FROM briefing_section WHERE briefing_id=? ORDER BY sort_no", (briefing_id,)
        )
        secs = _rows(cur2)
        for s in secs:
            s["article_ids"] = json.loads(s.get("article_ids_json") or "[]")
        b["sections"] = secs
        return b


def add_push_log(briefing_id: int, channel: str, target: str, status: str) -> None:
    with _LOCK, _connect() as conn:
        conn.execute(
            "INSERT INTO push_log(briefing_id, channel, target, status, sent_at) VALUES(?,?,?,?,?)",
            (briefing_id, channel, target, status, now()),
        )


def trend_data(sub_id: int) -> Dict[str, Any]:
    """关键词热度趋势：按简报期数统计文章数 / 来源分布。"""
    with _connect() as conn:
        cur = conn.execute(
            "SELECT id, title, created_at, stats_json FROM briefing "
            "WHERE subscription_id=? ORDER BY id", (sub_id,)
        )
        briefings = _rows(cur)
        cur2 = conn.execute(
            "SELECT source_name, COUNT(*) AS c FROM article WHERE subscription_id=? "
            "GROUP BY source_name ORDER BY c DESC", (sub_id,)
        )
        sources = _rows(cur2)
    series = []
    for b in briefings:
        st = json.loads(b.get("stats_json") or "{}")
        series.append({
            "briefing_id": b["id"],
            "title": b["title"],
            "created_at": b["created_at"],
            "article_count": st.get("total_articles", 0),
        })
    return {"series": series, "sources": sources}