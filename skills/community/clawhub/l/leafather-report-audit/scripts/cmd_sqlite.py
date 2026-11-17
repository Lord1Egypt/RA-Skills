#!/usr/bin/env python3
"""cmd_sqlite.py — 把 SQL 变成 CSV 的最小适配器（sqlite3 版）。

它是 `--command` 接法的活例子：**SQL 从 stdin 进、CSV 从 stdout 出**，
审计器不关心后面是 SQLite / MySQL / PG / HTTP，只要能这样喂它就成。

用法：
    python3 cmd_sqlite.py --db /path/x.db   < sql.txt  > rows.csv

    # 配合审计器（这样复算就不需要 duckdb 了）：
    python3 scripts/rla_audit.py --ledger ledger.json --files report.md \
        --command "python3 scripts/cmd_sqlite.py --db /path/x.db"

为什么自带这个文件：
    1. 没有 duckdb 的环境（装不上 / 原生 DLL 被安全策略拦）也能完整跑通"复算"环节
    2. 自检在降级模式下用它，证明 --command 这条路真的可用，而不是嘴上说支持
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="SQL(stdin) → CSV(stdout)，背后是 sqlite3")
    ap.add_argument("--db", required=True, help="sqlite3 数据库文件路径")
    ap.add_argument("--timeout", type=float, default=30.0, help="单条查询超时（秒）")
    args = ap.parse_args()

    sql = sys.stdin.read().strip()
    if not sql:
        print("❌ 没有从 stdin 读到 SQL", file=sys.stderr)
        return 2

    con = sqlite3.connect(args.db, timeout=args.timeout)
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in (cur.description or [])]
        rows = cur.fetchall()
        w = csv.writer(sys.stdout, lineterminator="\n")
        if cols:
            w.writerow(cols)
        w.writerows(rows)
    except sqlite3.Error as e:
        print(f"❌ SQL 执行失败：{e}", file=sys.stderr)
        return 2
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
