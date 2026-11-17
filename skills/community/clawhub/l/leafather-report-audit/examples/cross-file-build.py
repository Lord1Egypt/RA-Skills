#!/usr/bin/env python3
"""cross-file demo 第一步：造数据、账本、两份交付件。

零依赖：只用 Python 标准库 sqlite3（不需要 duckdb）。
跑完会告诉你下一步该输入什么命令。

场景（真实事故形态）：
  data 补录后「发货单数」从 7 变成 8，只改了 report_a.md，report_b.html 还是旧数 7。
  另一个指标「净发货额」两份文件写法不同（85.25万 / 85.250万），值一样但表述不一。
"""
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
# 输出到「当前工作目录」下的 rla-demo/，不写技能目录 ——
# 否则这些演示数据会被打进商店包（技能包里不许有 .demo 这种运行时产物）
OUT = Path.cwd() / "rla-demo"

ROWS = [
    ("D001", "甲药房", "山东", 120000.00, "2026-09-30"),
    ("D002", "乙药房", "山东", 98000.00, "2026-09-30"),
    ("D003", "丙药房", "河南", 76500.00, "2026-09-30"),
    ("D004", "丁药房", "河南", 152000.00, "2026-09-30"),
    ("D005", "甲药房", "山东", 21000.00, "2026-09-29"),
    ("D006", "戊药房", "河北", 88000.00, "2026-09-29"),
    ("D007", "乙药房", "山东", 143000.00, "2026-09-28"),
    ("D008", "丙药房", "河南", 154000.00, "2026-09-28"),
]


def main() -> int:
    OUT.mkdir(exist_ok=True)
    db = OUT / "demo.sqlite"

    if db.exists():
        db.unlink()
    con = sqlite3.connect(str(db))
    con.execute("""CREATE TABLE raw_shipment_detail(
        doc_no TEXT, customer TEXT, province TEXT, amt_tax REAL, sale_date TEXT)""")
    con.executemany("INSERT INTO raw_shipment_detail VALUES (?,?,?,?,?)", ROWS)
    con.commit()

    q = lambda sql: con.execute(sql).fetchone()[0]  # noqa: E731
    amt = q("SELECT round(sum(amt_tax), 2) FROM raw_shipment_detail")
    docs = q("SELECT count(DISTINCT doc_no) FROM raw_shipment_detail")
    cust = q("SELECT count(DISTINCT customer) FROM raw_shipment_detail")
    con.close()

    ledger = {
        "schema": "report-ledger/1.0",
        "report": {"name": "9 月发货小结", "files": ["report_a.md", "report_b.html"],
                   "data_as_of": "2026-09-30", "generated_at": "2026-10-28T10:00:00+08:00",
                   "agent": "cross-file demo"},
        "sources": [],
        "numbers": [
            {"id": "n1", "metric_id": "ship.amt", "label": "净发货额", "value": amt,
             "unit": "元", "caliber": "sum(amt_tax)，含税，基本单位",
             "verifiable": True,
             "sql": "SELECT round(sum(amt_tax), 2) FROM raw_shipment_detail"},
            {"id": "n2", "metric_id": "ship.docs", "label": "发货单据数", "value": docs,
             "unit": "单", "caliber": "count(distinct doc_no)", "verifiable": True,
             "sql": "SELECT count(DISTINCT doc_no) FROM raw_shipment_detail"},
            {"id": "n3", "metric_id": "ship.cust", "label": "客户数", "value": cust,
             "unit": "家", "caliber": "count(distinct customer)", "verifiable": True,
             "sql": "SELECT count(DISTINCT customer) FROM raw_shipment_detail"},
        ],
    }
    (OUT / "ledger.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    wan = amt / 10000
    # 新版（正确）
    (OUT / "report_a.md").write_text(
        "# 9 月发货小结（数据截止 2026-09-30）\n\n"
        f"净发货额 {wan:.2f} 万元，发货单据数 {docs} 单，客户数 {cust} 家。\n",
        encoding="utf-8")
    # 旧版：单数还是补录前的 7（漏改）；净发货额多写一位小数（写法不同）
    (OUT / "report_b.html").write_text(
        "<h1>9 月发货小结</h1>\n"
        f"<p>净发货额 {wan:.3f} 万元，发货单据数 {docs - 1} 单，客户数 {cust} 家。</p>\n",
        encoding="utf-8")

    print("已生成：")
    for p in ("demo.sqlite", "ledger.json", "report_a.md", "report_b.html"):
        print(f"  {OUT / p}")
    print(f"""
账本真值：净发货额 {amt}（{wan:.2f} 万）、发货单据数 {docs} 单、客户数 {cust} 家
故意做坏两处：
  · report_b.html 的发货单据数还是补录前的 {docs - 1} 单  → 会被判「来源不明」拦下
  · 两份文件净发货额小数位不同（{wan:.2f} 万 / {wan:.3f} 万）  → 会进跨件矩阵标红

下一步（第 2 步）：
  python3 scripts/rla_audit.py --ledger {OUT}/ledger.json \\
      --files report_a.md report_b.html \\
      --command "python3 scripts/cmd_sqlite.py --db {OUT}/demo.sqlite" \\
      --out {OUT}/audit.md

第 3 步：打开 {OUT}/audit.html，看「跨件一致性」里的红格，以及「拦下的问题」。
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
