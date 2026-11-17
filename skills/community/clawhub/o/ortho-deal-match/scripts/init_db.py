# -*- coding: utf-8 -*-
"""
init_db.py — 建库 / 重置 / 体检

用法：
  python init_db.py            # 建库（已存在则跳过）
  python init_db.py --reset    # 重建（会清空全部撮合数据！）
  python init_db.py --stats    # 查看当前数据规模
"""
import argparse
import os
import sqlite3
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402

SCHEMA = """
-- 主体：发布需求或能力的一方
CREATE TABLE IF NOT EXISTS parties (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    name_norm   TEXT,
    side        TEXT,          -- buyer / seller / both
    country     TEXT,
    city        TEXT,
    person      TEXT,
    title       TEXT,
    email       TEXT,
    phone       TEXT,
    website     TEXT,
    owner       TEXT,          -- 登记用户 U00x
    is_self     INTEGER DEFAULT 0,   -- 1 = 我方自有主体，撮合时我方可见
    verified    INTEGER DEFAULT 0,   -- 是否在展会名录中核验到
    expo_ref    TEXT,                -- 核验出处，如 "AAOS 2026 / DKOU 2026"
    note        TEXT,
    status      TEXT DEFAULT 'active',
    created     TEXT
);
CREATE INDEX IF NOT EXISTS ix_parties_norm ON parties(name_norm);
CREATE INDEX IF NOT EXISTS ix_parties_side ON parties(side);

-- 需求：买方发布
CREATE TABLE IF NOT EXISTS demands (
    id           TEXT PRIMARY KEY,
    party_id     TEXT,
    title        TEXT,
    raw          TEXT,
    cat          TEXT,          -- 归一化标准词，' / ' 分隔
    process      TEXT,
    material     TEXT,
    cert         TEXT,
    market       TEXT,
    cat_raw      TEXT,
    qty          TEXT,
    deadline     TEXT,
    budget       TEXT,
    status       TEXT DEFAULT 'open',   -- open / matched / closed
    owner        TEXT,
    visibility   TEXT DEFAULT 'public',  -- public=进撮合池 / private=仅自己可见
    valid_until  TEXT,
    created      TEXT
);
CREATE INDEX IF NOT EXISTS ix_demands_party ON demands(party_id);
CREATE INDEX IF NOT EXISTS ix_demands_status ON demands(status);

-- 能力：卖方发布
CREATE TABLE IF NOT EXISTS capabilities (
    id           TEXT PRIMARY KEY,
    party_id     TEXT,
    title        TEXT,
    raw          TEXT,
    cat          TEXT,
    process      TEXT,
    material     TEXT,
    cert         TEXT,
    market       TEXT,
    cat_raw      TEXT,
    capacity     TEXT,
    moq          TEXT,
    lead_time    TEXT,
    status       TEXT DEFAULT 'open',
    owner        TEXT,
    visibility   TEXT DEFAULT 'public',
    valid_until  TEXT,
    created      TEXT
);
CREATE INDEX IF NOT EXISTS ix_caps_party ON capabilities(party_id);
CREATE INDEX IF NOT EXISTS ix_caps_status ON capabilities(status);

-- 撮合：需求 × 能力
CREATE TABLE IF NOT EXISTS matches (
    id           TEXT PRIMARY KEY,
    demand_id    TEXT,
    capability_id TEXT,
    score        INTEGER,
    reason       TEXT,
    buyer_ok     INTEGER DEFAULT 0,
    seller_ok    INTEGER DEFAULT 0,
    status       TEXT DEFAULT 'suggested',  -- suggested/half/connected/declined/closed
    assignee     TEXT,                      -- 分派跟进人 U00x（member 只能看到分派给自己的单）
    created      TEXT,
    updated      TEXT
);
CREATE INDEX IF NOT EXISTS ix_matches_demand ON matches(demand_id);
CREATE INDEX IF NOT EXISTS ix_matches_status ON matches(status);

-- 对接留痕：谁在什么时候做了什么
CREATE TABLE IF NOT EXISTS intros (
    id        TEXT PRIMARY KEY,
    match_id  TEXT,
    actor     TEXT,
    side      TEXT,          -- buyer / seller / system
    action    TEXT,          -- request/accept/decline/reveal/note/feedback
    note      TEXT,
    created   TEXT
);
CREATE INDEX IF NOT EXISTS ix_intros_match ON intros(match_id);
"""


class DictRow(sqlite3.Row):
    """sqlite3.Row 支持 keys() 索引，但业务代码习惯用 .get()，这里补上"""

    def get(self, key, default=None):
        try:
            return self[key]
        except (IndexError, KeyError):
            return default


def connect():
    core._ensure()
    con = sqlite3.connect(core.DB_PATH)
    con.row_factory = DictRow
    return con


def init(reset=False):
    if reset and os.path.exists(core.DB_PATH):
        # 重置前备份旧库（安全审计 P1-1 整改：破坏性操作可回溯）
        bak = core.DB_PATH + ".bak-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        os.replace(core.DB_PATH, bak)
        print(f"  旧库已备份为 {os.path.basename(bak)}")
    con = connect()
    con.executescript(SCHEMA)
    _migrate(con)
    con.commit()
    return con


def _migrate(con):
    """旧库平滑升级：缺的列补上，不动数据。"""
    cols = {r[1] for r in con.execute("PRAGMA table_info(matches)")}
    if "assignee" not in cols:
        con.execute("ALTER TABLE matches ADD COLUMN assignee TEXT")


SQL_D_OPEN = "SELECT COUNT(*) FROM demands WHERE status='open'"
SQL_C_OPEN = "SELECT COUNT(*) FROM capabilities WHERE status='open'"


def stats(con):
    def q(s):
        return con.execute(s).fetchone()[0]
    print("=" * 68)
    print("  撮合台数据规模")
    print("=" * 68)
    print(f"  主体 parties      {q('SELECT COUNT(*) FROM parties'):>5}")
    print(f"      其中我方主体  {q('SELECT COUNT(*) FROM parties WHERE is_self=1'):>5}")
    print(f"      已核验        {q('SELECT COUNT(*) FROM parties WHERE verified=1'):>5}")
    print(f"  需求 demands      {q('SELECT COUNT(*) FROM demands'):>5}")
    print(f"      进行中        {q(SQL_D_OPEN):>5}")
    print(f"  能力 capabilities {q('SELECT COUNT(*) FROM capabilities'):>5}")
    print(f"      进行中        {q(SQL_C_OPEN):>5}")
    print(f"  撮合 matches      {q('SELECT COUNT(*) FROM matches'):>5}")
    for st in ("suggested", "half", "connected", "declined"):
        print(f"      {st:<13}{con.execute('SELECT COUNT(*) FROM matches WHERE status=?', (st,)).fetchone()[0]:>5}")
    print(f"  留痕 intros       {q('SELECT COUNT(*) FROM intros'):>5}")
    print(f"\n  数据库 {core.DB_PATH}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="撮合台建库与体检")
    ap.add_argument("--reset", action="store_true", help="重建数据库，清空全部数据")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()
    con = init(reset=a.reset)
    if a.reset:
        print("  数据库已重建（全部撮合数据已清空）")
    if a.stats:
        return stats(con)
    ok = con.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' "
        "AND name IN ('parties','demands','capabilities','matches','intros')"
    ).fetchone()[0]
    print(f"  数据库就绪：{ok}/5 张表  {core.DB_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
