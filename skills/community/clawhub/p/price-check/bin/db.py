#!/usr/bin/env python3
"""price-check v0.3 SQLite 持久化模块

存储位置：~/.openclaw/data/price-check/price-check.db
三张表：queries / price_snapshots / query_cache

写库失败 swallow（不影响主输出），日志走 stderr。
"""
from __future__ import annotations

import json
import sqlite3
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional

DATA_DIR = Path.home() / ".openclaw" / "data" / "price-check"
DB_PATH = DATA_DIR / "price-check.db"
CACHE_TTL_SECONDS = 1800  # 30 分钟


SCHEMA = """
CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    source TEXT,
    page INTEGER,
    queried_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verdict TEXT,
    verdict_reason TEXT,
    best_deal_json TEXT,
    stats_json TEXT,
    stats_raw_json TEXT,
    flagged_count INTEGER,
    low_relevance_count INTEGER,
    removed_outliers_count INTEGER,
    duration_ms INTEGER
);
CREATE INDEX IF NOT EXISTS idx_q_query ON queries(query);
CREATE INDEX IF NOT EXISTS idx_q_at ON queries(queried_at);

CREATE TABLE IF NOT EXISTS price_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER NOT NULL REFERENCES queries(id),
    snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    goodsId TEXT,
    source TEXT,
    platform TEXT,
    shop TEXT,
    title TEXT,
    price REAL,
    original_price REAL,
    coupon_amount REAL,
    condition_ TEXT,
    is_trusted_shop INTEGER,
    relevance_score REAL,
    relevance_ambiguous INTEGER,
    in_best_deal INTEGER DEFAULT 0,
    in_flagged INTEGER DEFAULT 0,
    in_low_relevance INTEGER DEFAULT 0,
    in_removed INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_s_goodsid ON price_snapshots(goodsId);
CREATE INDEX IF NOT EXISTS idx_s_at ON price_snapshots(snapshot_at);
CREATE INDEX IF NOT EXISTS idx_s_query ON price_snapshots(query_id);

CREATE TABLE IF NOT EXISTS query_cache (
    query_key TEXT PRIMARY KEY,
    cached_json TEXT NOT NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def _ensure_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


@contextmanager
def _conn():
    _ensure_dir()
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def _warn(msg: str) -> None:
    print(f"[price-check.db] {msg}", file=sys.stderr)


# ---------- query_cache ----------
def cache_get(query: str, source: str = "0", page: int = 1) -> Optional[dict[str, Any]]:
    """30min TTL 内同 query 直接复用。失败返回 None。"""
    key = f"{query}|{source}|{page}"
    try:
        with _conn() as c:
            row = c.execute(
                "SELECT cached_json, cached_at FROM query_cache WHERE query_key = ?",
                (key,),
            ).fetchone()
            if not row:
                return None
            cached_at_str = row["cached_at"]
            cached_at = time.mktime(time.strptime(cached_at_str, "%Y-%m-%d %H:%M:%S"))
            if time.time() - cached_at > CACHE_TTL_SECONDS:
                return None
            return json.loads(row["cached_json"])
    except Exception as e:
        _warn(f"cache_get failed: {e}")
        return None


def cache_set(query: str, source: str, page: int, result: dict[str, Any]) -> None:
    """upsert 缓存。失败 swallow。"""
    key = f"{query}|{source}|{page}"
    try:
        with _conn() as c:
            c.execute(
                """INSERT INTO query_cache (query_key, cached_json, cached_at)
                   VALUES (?, ?, CURRENT_TIMESTAMP)
                   ON CONFLICT(query_key) DO UPDATE SET
                     cached_json = excluded.cached_json,
                     cached_at = CURRENT_TIMESTAMP""",
                (key, json.dumps(result, ensure_ascii=False)),
            )
    except Exception as e:
        _warn(f"cache_set failed: {e}")


# ---------- queries + price_snapshots ----------
# ---------- 历史查询（v0.4 HistoryProvider 用） ----------
def query_history_by_query(query: str, days: int = 90) -> list[dict[str, Any]]:
    """该 query 历次查询的 best_deal + 市场分布序列。

    返回按 queried_at 升序的列表：
      [{queried_at, best_deal_price, stats_min, stats_median, stats_max}, ...]
    """
    try:
        with _conn() as c:
            rows = c.execute(
                """SELECT queried_at, verdict, best_deal_json, stats_json
                   FROM queries
                   WHERE query = ?
                     AND datetime(queried_at) >= datetime('now', '-' || ? || ' days')
                   ORDER BY queried_at ASC""",
                (query, days),
            ).fetchall()
            out = []
            for r in rows:
                bd = json.loads(r["best_deal_json"]) if r["best_deal_json"] else {}
                stats = json.loads(r["stats_json"]) if r["stats_json"] else {}
                out.append({
                    "queried_at": r["queried_at"],
                    "verdict": r["verdict"],
                    "best_deal_price": (bd or {}).get("price"),
                    "best_deal_shop": (bd or {}).get("shopName"),
                    "best_deal_goodsId": (bd or {}).get("goodsId"),
                    "stats_min": (stats or {}).get("min"),
                    "stats_median": (stats or {}).get("median"),
                    "stats_max": (stats or {}).get("max"),
                })
            return out
    except Exception as e:
        _warn(f"query_history_by_query failed: {e}")
        return []


def query_history_by_goodsid(goods_id: str, days: int = 90) -> list[dict[str, Any]]:
    """某个 goodsId 在历次查询里的价格快照序列（按 snapshot_at 升序）。"""
    if not goods_id:
        return []
    try:
        with _conn() as c:
            rows = c.execute(
                """SELECT snapshot_at, price, shop, platform, title
                   FROM price_snapshots
                   WHERE goodsId = ?
                     AND datetime(snapshot_at) >= datetime('now', '-' || ? || ' days')
                   ORDER BY snapshot_at ASC""",
                (goods_id, days),
            ).fetchall()
            return [{
                "snapshot_at": r["snapshot_at"],
                "price": r["price"],
                "shop": r["shop"],
                "platform": r["platform"],
                "title": r["title"],
            } for r in rows]
    except Exception as e:
        _warn(f"query_history_by_goodsid failed: {e}")
        return []


def query_history_by_signature(
    shop: str, title_prefix: str, days: int = 90
) -> list[dict[str, Any]]:
    """按 (shop + title 前 N 字符) 模糊匹配历史快照。

    shopmind 的 goodsId 每次返回都含 session token（中间一段会变），
    精确 goodsId 匹配往往失效。改用 (shop, title 前 30 字符) 作为商品稳定指纹。
    """
    if not shop or not title_prefix:
        return []
    try:
        with _conn() as c:
            rows = c.execute(
                """SELECT snapshot_at, price, shop, platform, title, goodsId
                   FROM price_snapshots
                   WHERE shop = ?
                     AND substr(title, 1, ?) = ?
                     AND datetime(snapshot_at) >= datetime('now', '-' || ? || ' days')
                   ORDER BY snapshot_at ASC""",
                (shop, len(title_prefix), title_prefix, days),
            ).fetchall()
            return [{
                "snapshot_at": r["snapshot_at"],
                "price": r["price"],
                "shop": r["shop"],
                "platform": r["platform"],
                "title": r["title"],
                "goodsId": r["goodsId"],
            } for r in rows]
    except Exception as e:
        _warn(f"query_history_by_signature failed: {e}")
        return []


def persist_query(
    query: str,
    source: str,
    page: int,
    result: dict[str, Any],
    duration_ms: int,
) -> Optional[int]:
    """写一条 queries + 全部 price_snapshots。返回 query_id，失败返回 None。"""
    try:
        with _conn() as c:
            cur = c.execute(
                """INSERT INTO queries (
                       query, source, page,
                       verdict, verdict_reason,
                       best_deal_json, stats_json, stats_raw_json,
                       flagged_count, low_relevance_count, removed_outliers_count,
                       duration_ms
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    query, source, page,
                    result.get("verdict"),
                    result.get("verdict_reason"),
                    json.dumps(result.get("best_deal"), ensure_ascii=False) if result.get("best_deal") else None,
                    json.dumps(result.get("stats"), ensure_ascii=False),
                    json.dumps(result.get("stats_raw"), ensure_ascii=False),
                    len(result.get("flagged_items") or []),
                    len(result.get("low_relevance_items") or []),
                    len(result.get("removed_outliers") or []),
                    duration_ms,
                ),
            )
            query_id = cur.lastrowid

            best_deal = result.get("best_deal") or {}
            best_deal_id = best_deal.get("goodsId")
            flagged_ids = {i.get("goodsId") for i in (result.get("flagged_items") or [])}
            low_rel_ids = {i.get("goodsId") for i in (result.get("low_relevance_items") or [])}
            removed_ids = {i.get("goodsId") for i in (result.get("removed_outliers") or [])}

            for item in (result.get("all_platforms") or []):
                gid = item.get("goodsId")
                rel = item.get("relevance") or {}
                c.execute(
                    """INSERT INTO price_snapshots (
                           query_id, goodsId, source, platform, shop, title,
                           price, original_price, coupon_amount,
                           condition_, is_trusted_shop,
                           relevance_score, relevance_ambiguous,
                           in_best_deal, in_flagged, in_low_relevance, in_removed
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        query_id, gid, item.get("source"), item.get("platform"),
                        item.get("shopName"), item.get("title"),
                        item.get("price"), item.get("originalPrice"), item.get("couponAmount"),
                        item.get("condition"),
                        1 if item.get("is_trusted_shop") else 0,
                        rel.get("score"),
                        1 if rel.get("ambiguous") else 0,
                        1 if gid == best_deal_id else 0,
                        1 if gid in flagged_ids else 0,
                        1 if gid in low_rel_ids else 0,
                        1 if gid in removed_ids else 0,
                    ),
                )
            return query_id
    except Exception as e:
        _warn(f"persist_query failed: {e}")
        return None
