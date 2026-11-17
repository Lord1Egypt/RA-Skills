#!/usr/bin/env python3
"""share-queue.py v2 — 隨時分享區（SQLite 版，2026-08-18 設計）。

AI 探索到有趣嘅嘢 → add 入分享區（唔使即刻 ping）；
分享咗出街（send 俾用戶）→ mark 做 shared（軟刪，留歷史）——list 唔再顯示，唔會重複分享。

設計跟專業 DB 慣例：
- status 狀態機（pending → shared / discarded）
- 軟刪（status='shared' + shared_at），list 只撈 pending
- audit 欄：created_at / updated_at
- 去重：content_hash（summary md5）UNIQUE

 用法：
  python3 scripts/share-queue.py add --topic "..." --summary "..." [--link "url"] [--cat "海洋"] [--channel "news"] [--score 2] [--note "..."]
  python3 scripts/share-queue.py list                # 只顯示 pending
  python3 scripts/share-queue.py list --channel "news"  # 只顯示指定管道嘅貨（DB-first 出貨用）
  python3 scripts/share-queue.py list --topic "太空"    # 只顯示 topic 含關鍵字嘅貨
  python3 scripts/share-queue.py list --all          # 連 shared/discarded 歷史一齊睇
  python3 scripts/share-queue.py remove --uuid <id>  # 軟刪（mark shared）
  python3 scripts/share-queue.py discard --uuid <id> # 放棄（mark discarded）
  python3 scripts/share-queue.py clear               # 清空所有 pending
  python3 scripts/share-queue.py stats               # 統計（總數/pending/shared/分數）
"""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import datetime
import uuid

BASE = os.environ.get("IDLE_PING_WS") or os.path.expanduser("~/.openclaw/workspace")
DB_FILE = os.path.join(BASE, "curiosity", "share-queue.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS share_queue (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid            TEXT NOT NULL UNIQUE,
  topic           TEXT NOT NULL,
  summary         TEXT NOT NULL,
  link            TEXT,
  category        TEXT,
  interest_score  INTEGER NOT NULL DEFAULT 0,
  status          TEXT NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending','shared','discarded')),
  channel         TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  updated_at      TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  shared_at       TEXT,
  note            TEXT,
  content_hash    TEXT NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS idx_share_queue_status_created
  ON share_queue (status, created_at);
"""


def get_conn():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    # migration：舊 db 冇 channel column → 加返
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(share_queue)").fetchall()]
    if "channel" not in cols:
        conn.execute("ALTER TABLE share_queue ADD COLUMN channel TEXT")
        conn.commit()
    return conn


def content_hash(summary):
    return hashlib.md5(summary.strip().encode("utf-8", "ignore")).hexdigest()


def _similar(a, b):
    """兩段文字相似度（0-1），用嚟偵測「同一單嘢唔同寫法」嘅重複。"""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, (a or "").strip().lower(), (b or "").strip().lower()).ratio()


def add(topic, summary, link="", cat="", score=0, note="", channel=""):
    conn = get_conn()
    existing = conn.execute(
        "SELECT uuid, topic, summary, link, status FROM share_queue ORDER BY id"
    ).fetchall()
    # 1) content_hash 完全一樣 → skip（舊行為）
    if any(content_hash(summary) == content_hash(r["summary"]) for r in existing):
        print("⚠️ 重複內容（content_hash 一樣），跳過——同一條嘢唔會入兩次")
        conn.close()
        return
    # 2) 相似內容（summary 相似度 ≥ 0.75 或 link 一樣）→ 照入庫但標記做 shared
    #    （留歷史做去重記錄，唔會出貨——2026-08-21 決定：重複貨唔剷，標籤做已分享）
    dup, reason = None, ""
    for r in existing:
        if link and r["link"] and link.strip() == r["link"].strip():
            dup, reason = r, "link 一樣"
            break
        ratio = _similar(summary, r["summary"])
        if ratio >= 0.75:
            dup, reason = r, f"summary 相似度 {ratio:.0%}"
            break
    if dup:
        conn.execute(
            "INSERT INTO share_queue (uuid, topic, summary, link, category, interest_score, note, content_hash, channel, status, shared_at) "
            "VALUES (?,?,?,?,?,?,?,?,?, 'shared', datetime('now','localtime'))",
            (uuid.uuid4().hex[:12], topic, summary, link or None, cat or None, score, note or None, content_hash(summary), channel or None),
        )
        conn.commit()
        print(f"🔁 偵測到重複（{reason}，同 [{dup['uuid']}] {dup['status']}）→ 自動標記為 shared，唔會出貨")
        conn.close()
        return
    # 3) 全新 → pending
    try:
        conn.execute(
            "INSERT INTO share_queue (uuid, topic, summary, link, category, interest_score, note, content_hash, channel) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (uuid.uuid4().hex[:12], topic, summary, link or None, cat or None, score, note or None, content_hash(summary), channel or None),
        )
        conn.commit()
        row = conn.execute(
            "SELECT uuid, topic FROM share_queue ORDER BY id DESC LIMIT 1"
        ).fetchone()
        print(f"✅ 已加入分享區 [{row['uuid']}] {row['topic']}")
    except sqlite3.IntegrityError:
        print("⚠️ 重複內容（content_hash 一樣），跳過——同一條嘢唔會入兩次")
    finally:
        conn.close()


def list_items(show_all=False, channel="", topic=""):
    conn = get_conn()
    sql = "SELECT * FROM share_queue"
    conds, params = [], []
    if not show_all:
        conds.append("status='pending'")
    if channel:
        conds.append("channel=?")
        params.append(channel)
    if topic:
        conds.append("(topic LIKE ? OR summary LIKE ?)")
        params += [f"%{topic}%", f"%{topic}%"]
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY created_at DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    if not rows:
        print("（分享區係空嘅）" if not show_all else "（歷史都係空嘅）")
        return
    print(f"📥 分享區有 {len(rows)} 條：")
    for i, r in enumerate(rows, 1):
        tag = {"pending": "⏳", "shared": "✅", "discarded": "🗑️"}.get(r["status"], "•")
        print(f"{i}. {tag} [{r['uuid']}] {r['topic']}｜{r['summary'][:55]}")
        if r["link"]:
            print(f"   來源: {r['link']}")
        if r["category"] or r["interest_score"]:
            print(f"   類別: {r['category'] or '—'} · 管道: {r['channel'] or '—'} · 有趣度: {r['interest_score']} · {r['status']} @ {r['created_at']}")
        if r["note"]:
            print(f"   諗法: {r['note']}")


def soft_delete(conn, uuid_val, status, field):
    cur = conn.execute(
        f"UPDATE share_queue SET status=?, {field}=datetime('now','localtime'), "
        f"updated_at=datetime('now','localtime') WHERE uuid=? AND status='pending'",
        (status, uuid_val),
    )
    conn.commit()
    return cur.rowcount


def remove(uuid_val):
    conn = get_conn()
    n = soft_delete(conn, uuid_val, "shared", "shared_at")
    conn.close()
    if n:
        print(f"🗑️ 已分享 [{uuid_val}]（軟刪，歷史保留）")
    else:
        print(f"❌ 搵唔到 pending 記錄 {uuid_val}")


def discard(uuid_val):
    conn = get_conn()
    n = soft_delete(conn, uuid_val, "discarded", "shared_at")
    conn.close()
    if n:
        print(f"🗑️ 已放棄 [{uuid_val}]")
    else:
        print(f"❌ 搵唔到 pending 記錄 {uuid_val}")


def clear():
    conn = get_conn()
    n = conn.execute("DELETE FROM share_queue WHERE status='pending'").rowcount
    conn.commit()
    conn.close()
    print(f"🧹 已清空 {n} 條 pending")


def stats():
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) c FROM share_queue").fetchone()["c"]
    pending = conn.execute("SELECT COUNT(*) c FROM share_queue WHERE status='pending'").fetchone()["c"]
    shared = conn.execute("SELECT COUNT(*) c FROM share_queue WHERE status='shared'").fetchone()["c"]
    discarded = conn.execute("SELECT COUNT(*) c FROM share_queue WHERE status='discarded'").fetchone()["c"]
    avg = conn.execute("SELECT AVG(interest_score) a FROM share_queue WHERE status='shared'").fetchone()["a"]
    by_cat = conn.execute(
        "SELECT category, COUNT(*) c FROM share_queue WHERE status='shared' GROUP BY category ORDER BY c DESC LIMIT 5"
    ).fetchall()
    conn.close()
    print(f"📊 分享區統計：總共 {total}｜pending {pending}｜已分享 {shared}｜放棄 {discarded}")
    if avg:
        print(f"   已分享平均有趣度: {avg:.1f}")
    if by_cat:
        print("   最常分享類別:", ", ".join(f"{r['category'] or '—'}×{r['c']}" for r in by_cat))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--topic", required=True)
    p_add.add_argument("--summary", required=True)
    p_add.add_argument("--link", default="")
    p_add.add_argument("--cat", default="")
    p_add.add_argument("--channel", default="", help="來源管道（news/onthisday/arxiv/reddit/randomwiki/misconceptions/xsearch）")
    p_add.add_argument("--score", type=int, default=0)
    p_add.add_argument("--note", default="")

    p_list = sub.add_parser("list")
    p_list.add_argument("--all", action="store_true", help="連歷史一齊睇")
    p_list.add_argument("--channel", default="", help="只顯示指定管道（news/onthisday/arxiv/reddit 等）")
    p_list.add_argument("--topic", default="", help="只顯示 topic/summary 含關鍵字嘅貨")

    p_rm = sub.add_parser("remove")
    p_rm.add_argument("--uuid", required=True)

    p_discard = sub.add_parser("discard")
    p_discard.add_argument("--uuid", required=True)

    sub.add_parser("clear")
    sub.add_parser("stats")

    args = parser.parse_args()
    if args.cmd == "add":
        add(args.topic, args.summary, args.link, args.cat, args.score, args.note, args.channel)
    elif args.cmd == "list":
        list_items(args.all, args.channel, args.topic)
    elif args.cmd == "remove":
        remove(args.uuid)
    elif args.cmd == "discard":
        discard(args.uuid)
    elif args.cmd == "clear":
        clear()
    elif args.cmd == "stats":
        stats()


if __name__ == "__main__":
    main()
