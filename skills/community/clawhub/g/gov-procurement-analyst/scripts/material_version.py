#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标书素材库 · 双哈希去重与版本链（16.10，v5.5 新增）

- MD5：完全去重（内容一字不差直接判重）
- SimHash（64 位）：相似度归并（汉明距离 <= 3 视为同类素材）
- gov_material.db · material_versions：同一 material_id 下版本链 v1/v2/...
- 引用时取最新版，并标注来源项目

用法：
  python material_version.py add --category 技术方案 --title "政务云方案" \
      --content-file ./plan.md --source "XX市政务云项目"
  python material_version.py latest --material-id <id>
  python material_version.py versions --material-id <id>
  python material_version.py stats
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_DB = os.path.expanduser("~/.workbuddy/output/gov_material.db")
SIMHASH_THRESHOLD = 3


def resolve_db(path=None):
    return os.path.expanduser(path or DEFAULT_DB)


def md5_of(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _features(text):
    text = re.sub(r"\s+", "", text or "")
    if len(text) < 2:
        return [text] if text else ["\x00"]
    return [text[i:i + 2] for i in range(len(text) - 1)]


def simhash64(text):
    v = [0] * 64
    for feat in _features(text):
        h = int(hashlib.md5(feat.encode("utf-8")).hexdigest(), 16)
        for i in range(64):
            v[i] += 1 if (h >> i) & 1 else -1
    out = 0
    for i in range(64):
        if v[i] > 0:
            out |= 1 << i
    return format(out, "016x")


def hamming(a, b):
    try:
        return bin(int(a, 16) ^ int(b, 16)).count("1")
    except ValueError:
        return 64


def init_db(path=None):
    db = resolve_db(path)
    os.makedirs(os.path.dirname(db), exist_ok=True)
    conn = sqlite3.connect(db)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS material_versions (
               id INTEGER PRIMARY KEY,
               material_id TEXT NOT NULL,
               version_no INTEGER NOT NULL,
               category TEXT,
               title TEXT,
               content_md5 TEXT,
               content_simhash TEXT,
               source_project TEXT,
               content TEXT,
               created_at TEXT DEFAULT (datetime('now'))
           )"""
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_mv_mid ON material_versions(material_id, version_no)"
    )
    conn.commit()
    return conn


def _latest_per_material(conn, category=None):
    sql = (
        "SELECT material_id, MAX(version_no) FROM material_versions "
        "WHERE 1=1"
    )
    params = []
    if category:
        sql += " AND category=?"
        params.append(category)
    sql += " GROUP BY material_id"
    out = {}
    for mid, mx in conn.execute(sql, params):
        row = conn.execute(
            "SELECT id, material_id, version_no, category, title, content_md5, "
            "content_simhash, source_project, content FROM material_versions "
            "WHERE material_id=? AND version_no=?",
            (mid, mx),
        ).fetchone()
        out[mid] = row
    return out


def add_material(category, title, content, source_project="", path=None):
    conn = init_db(path)
    digest = md5_of(content)
    sim = simhash64(content)

    for mid, row in _latest_per_material(conn, category).items():
        if row[5] == digest:
            conn.close()
            return {"action": "skipped", "material_id": mid, "version_no": row[2],
                    "reason": "MD5 相同，判为同一素材"}
        if row[6] and hamming(row[6], sim) <= SIMHASH_THRESHOLD:
            new_no = row[2] + 1
            cur = conn.execute(
                """INSERT INTO material_versions
                   (material_id, version_no, category, title, content_md5,
                    content_simhash, source_project, content)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (mid, new_no, category, title, digest, sim, source_project, content),
            )
            conn.commit()
            conn.close()
            return {"action": "versioned", "material_id": mid, "version_no": new_no,
                    "id": cur.lastrowid, "reason": "SimHash 距离 <= %d，归并为同类素材新版本" % SIMHASH_THRESHOLD}

    new_id = "mat_%s" % digest[:12]
    cur = conn.execute(
        """INSERT INTO material_versions
           (material_id, version_no, category, title, content_md5,
            content_simhash, source_project, content)
           VALUES(?,?,?,?,?,?,?,?)""",
        (new_id, 1, category, title, digest, sim, source_project, content),
    )
    conn.commit()
    conn.close()
    return {"action": "new", "material_id": new_id, "version_no": 1, "id": cur.lastrowid}


def get_latest(material_id, path=None):
    conn = init_db(path)
    row = conn.execute(
        "SELECT id, material_id, version_no, category, title, content_md5, "
        "content_simhash, source_project, content, created_at "
        "FROM material_versions WHERE material_id=? ORDER BY version_no DESC LIMIT 1",
        (material_id,),
    ).fetchone()
    conn.close()
    return row


def list_versions(material_id, path=None):
    conn = init_db(path)
    rows = conn.execute(
        "SELECT id, version_no, title, source_project, content_md5, created_at "
        "FROM material_versions WHERE material_id=? ORDER BY version_no",
        (material_id,),
    ).fetchall()
    conn.close()
    return rows


def stats(path=None):
    conn = init_db(path)
    total = conn.execute("SELECT COUNT(*) FROM material_versions").fetchone()[0]
    mats = conn.execute("SELECT COUNT(DISTINCT material_id) FROM material_versions").fetchone()[0]
    by_cat = conn.execute(
        "SELECT category, COUNT(*) FROM material_versions GROUP BY category ORDER BY 2 DESC"
    ).fetchall()
    conn.close()
    return {"total_versions": total, "materials": mats, "by_category": by_cat}


def main():
    ap = argparse.ArgumentParser(description="素材库双哈希去重与版本链")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _add_db(p):
        p.add_argument("--db")

    p_add = sub.add_parser("add")
    _add_db(p_add)
    p_add.add_argument("--category", required=True)
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--content", default="")
    p_add.add_argument("--content-file")
    p_add.add_argument("--source", default="")

    p_latest = sub.add_parser("latest")
    _add_db(p_latest)
    p_latest.add_argument("--material-id", required=True)

    p_ver = sub.add_parser("versions")
    _add_db(p_ver)
    p_ver.add_argument("--material-id", required=True)

    p_stats = sub.add_parser("stats")
    _add_db(p_stats)

    args = ap.parse_args()
    if args.cmd == "add":
        content = args.content
        if args.content_file:
            with open(args.content_file, encoding="utf-8") as fh:
                content = fh.read()
        print(json.dumps(add_material(args.category, args.title, content, args.source, args.db),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "latest":
        print(json.dumps(get_latest(args.material_id, args.db), ensure_ascii=False, indent=2, default=str))
    elif args.cmd == "versions":
        for r in list_versions(args.material_id, args.db):
            print("  v%s  %s  source=%s  md5=%s  %s" % (r[1], r[2], r[3] or "-", (r[4] or "")[:8], r[5]))
    elif args.cmd == "stats":
        print(json.dumps(stats(args.db), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
