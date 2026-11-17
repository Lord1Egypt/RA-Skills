#!/usr/bin/env python3
"""rla_selftest.py — 自带数据自检：30 秒证明这套东西真的会抓错。

为什么技能必须自带这个：
    别人装完没法判断"它到底有没有在检查"。靠读文档没用，靠信作者更没用。
    这里造一个 6 行数据的小库，跑 5 个用例：
      1) 正确报告        → 应该 ✅ 通过
      2) 报告改一个数    → 应该 ❌ 来源不明
      3) 两份件写法不同  → 应该 ⚠️ 跨件不一致
      4) 客户版塞内部词  → 应该 ❌ 泄漏
      5) 账本编数        → 应该 ❌ 复算不符
    5 个全中才算通过。

两种运行模式：
    * 完整模式：有 duckdb —— 造 .duckdb 小库，复算走 --mount
    * 降级模式：没有 duckdb（或原生 DLL 被安全策略拦）—— 用 Python 内置的 sqlite3 造库，
      复算走 --command（cmd_sqlite.py）。**同样 5 个用例全跑，结论格式一致。**
      这样"装不上驱动"的环境也能验证它真的在检查，而不是只看到一句 ModuleNotFoundError。

用法：
    python3 scripts/rla_selftest.py          # 跑一遍
    python3 scripts/rla_selftest.py --keep   # 保留临时文件便于查看
"""
from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE / "rla_audit.py"

ROWS = [
    # doc_no, 客户, 省份, 金额(元), 数量
    ("D001", "甲公司", "河北", 120000.0, 30),
    ("D002", "乙公司", "河北", 80000.0, 20),
    ("D003", "丙公司", "山东", 60000.0, 15),
    ("D004", "丁公司", "山东", 40000.0, 10),
    ("D005", "戊公司", "河南", 25000.0, 5),
    ("D006", "己公司", "河南", 15000.0, 5),
]


def build_fixture(root: Path, mode: str = "full") -> Path:
    """造一个小库：raw_shipment_detail（6 行）。duckdb 可用就 duckdb，否则 sqlite3。

    两边建表语句不同，但**查询 SQL 完全一样**（都是标准 SQL：sum/round/count(distinct)），
    所以用例不需要准备两套方言。
    """
    if mode == "degraded":
        db = root / "fixture.db"
        con = sqlite3.connect(str(db))
        con.execute("""CREATE TABLE raw_shipment_detail(
            doc_no TEXT, customer TEXT, province TEXT,
            amt_tax REAL, qty INTEGER, sale_date TEXT)""")
        for d, c, p, a, q in ROWS:
            con.execute("INSERT INTO raw_shipment_detail VALUES (?,?,?,?,?,?)",
                        [d, c, p, a, q, "2026-09-30"])
        con.commit()
        con.close()
        return db

    import duckdb
    db = root / "fixture.duckdb"
    con = duckdb.connect(str(db))
    con.execute("""CREATE TABLE raw_shipment_detail(
        doc_no VARCHAR, customer VARCHAR, province VARCHAR,
        amt_tax DOUBLE, qty INTEGER, sale_date DATE)""")
    for d, c, p, a, q in ROWS:
        con.execute("INSERT INTO raw_shipment_detail VALUES (?,?,?,?,?, DATE '2026-09-30')",
                    [d, c, p, a, q])
    con.close()
    return db


def _query_one(db: Path, mode: str, sql: str):
    """从 fixture 里取一个值（两种库通用）。"""
    if mode == "degraded":
        con = sqlite3.connect(str(db))
        try:
            return con.execute(sql).fetchone()[0]
        finally:
            con.close()
    import duckdb
    con = duckdb.connect(str(db), read_only=True)
    try:
        return con.execute(sql).fetchone()[0]
    finally:
        con.close()


def make_ledger(db: Path, root: Path, mode: str = "full") -> Path:
    amt = _query_one(db, mode, "SELECT round(sum(amt_tax), 2) FROM raw_shipment_detail")
    docs = _query_one(db, mode, "SELECT count(distinct doc_no) FROM raw_shipment_detail")
    cust = _query_one(db, mode, "SELECT count(distinct customer) FROM raw_shipment_detail")
    led = {
        "schema": "report-ledger/1.0",
        "report": {"name": "自检样本", "files": ["ok.md"], "data_as_of": "2026-09-30",
                   "generated_at": "2026-10-25T00:00:00+08:00", "agent": "selftest"},
        "sources": [],
        "numbers": [
            {"id": "n1", "metric_id": "ship.amt", "label": "净发货额", "value": amt,
             "unit": "元", "caliber": "sum(amt_tax)，基本单位", "verifiable": True,
             "sql": "SELECT round(sum(amt_tax), 2) FROM raw_shipment_detail"},
            {"id": "n2", "metric_id": "ship.docs", "label": "发货单据数", "value": docs,
             "unit": "单", "caliber": "count(distinct doc_no)", "verifiable": True,
             "sql": "SELECT count(distinct doc_no) FROM raw_shipment_detail"},
            {"id": "n3", "metric_id": "ship.cust", "label": "客户数", "value": cust,
             "unit": "家", "caliber": "count(distinct customer)", "verifiable": True,
             "sql": "SELECT count(distinct customer) FROM raw_shipment_detail"},
        ],
    }
    p = root / "ledger.json"
    p.write_text(json.dumps(led, ensure_ascii=False, indent=2), encoding="utf-8")
    return p, led


def report_text(led: dict, amt=None, docs=None, cust=None, dec: int = 1) -> str:
    """报告用「万元」表述（验证单位换算），dec 控制小数位（造跨件写法差异用）。"""
    g = {n["metric_id"]: n["value"] for n in led["numbers"]}
    amt = g["ship.amt"] if amt is None else amt
    docs = g["ship.docs"] if docs is None else docs
    cust = g["ship.cust"] if cust is None else cust
    return (f"# 自检样本报告\n\n净发货额 {float(amt) / 10000:.{dec}f} 万元，"
            f"发货单据数 {docs} 单，客户数 {cust} 家。\n")


def run(ledger: Path, files: list[Path], policy: Path, db: Path, mode: str = "full") -> int:
    cmd = [sys.executable, str(AUDIT), "--ledger", str(ledger),
           "--files", *[str(f) for f in files], "--no-write", "--policy", str(policy)]
    if mode == "degraded":
        # 降级模式走 --command：证明"没有 duckdb 也能复算"这条路是真的通
        # 路径一律加引号：Windows 上 python 常装在带空格的目录里，
        # 不加引号时 posix=False 的拆分会把路径拆碎（另一类同源故障）
        cmd += ["--command",
                f'"{sys.executable}" "{HERE / "cmd_sqlite.py"}" --db "{db}"']
    else:
        cmd += ["--mount", f"={db}"]
    return subprocess.run(cmd, capture_output=True, text=True).returncode


def run_full(ledger: Path, files: list[Path], policy: Path, db: Path,
             mode: str = "full", out_dir: Path | None = None):
    """跑一次审计并落产物，返回 (退出码, stdout, 产物目录)。

    与 run() 的区别：run() 带 --no-write（只看退出码），这里要拿产物做断言。
    刻意不复用 run()，免得改坏 5 个旧用例的公共路径。
    """
    import tempfile
    out_dir = Path(out_dir or tempfile.mkdtemp(prefix="rla_out_"))
    cmd = [sys.executable, str(AUDIT), "--ledger", str(ledger),
           "--files", *[str(f) for f in files], "--policy", str(policy),
           "--out", str(out_dir / "audit.md")]
    if mode == "degraded":
        cmd += ["--command", f'"{sys.executable}" "{HERE / "cmd_sqlite.py"}" --db "{db}"']
    else:
        cmd += ["--mount", f"={db}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, out_dir


EVROW = 'class="evrow"'   # 证据行标记（html 里写死这个 class，防止两处不一致）
BAD = 'class="bad"'       # 跨件矩阵红格标记


def check_artifacts(out_dir: Path, expect_verdict_prefix: str = "") -> tuple[bool, str]:
    """用例 7：产物自检。返回 (通过, 说明)。"""
    import csv as _csv
    import json as _json
    hp, cp, mp = out_dir / "audit.html", out_dir / "evidence.csv", out_dir / "manifest.json"
    if not (hp.exists() and cp.exists() and mp.exists()):
        return False, f"产物不全（html={hp.exists()} csv={cp.exists()} manifest={mp.exists()}）"
    htxt = hp.read_text(encoding="utf-8")
    man = _json.loads(mp.read_text(encoding="utf-8"))
    rows = list(_csv.DictReader(open(cp, encoding="utf-8-sig")))
    c = man["counts"]
    problems = []
    if "其余 " in htxt:
        problems.append("html 里仍有「其余 N 条」截断")
    if htxt.count(EVROW) != c["matched"]:
        problems.append(f"html 证据行 {htxt.count(EVROW)} != matched {c['matched']}")
    want = c["matched"] + c["unmatched"] + c["weak"] + c["ambiguous"] + c["exempt"]
    if len(rows) != want:
        problems.append(f"csv 行数 {len(rows)} != {want}")
    if not man.get("integrity", {}).get("ok"):
        problems.append("manifest integrity.ok 非真")
    if man.get("schema") != "rla-audit-manifest/1.0":
        problems.append("manifest schema 不对")
    if cp.open("rb").read(3) != b"\xef\xbb\xbf":
        problems.append("csv 缺 BOM")
    if expect_verdict_prefix and not (man.get("verdict", {}).get("label") or "").startswith(expect_verdict_prefix):
        problems.append(f'结论不是 {expect_verdict_prefix}')
    return (not problems), "；".join(problems)


def main() -> int:
    ap = argparse.ArgumentParser(description="自带数据自检")
    ap.add_argument("--keep", action="store_true", help="保留临时目录")
    args = ap.parse_args()

    import deps_check as DC
    mode = DC.banner(allow_degrade=True)      # 没有 duckdb 也不挡路，自动降级

    root = Path(tempfile.mkdtemp(prefix="rla_selftest_"))
    try:
        db = build_fixture(root, mode)
        ledger, led = make_ledger(db, root, mode)

        pol = root / "policy.yaml"
        pol.write_text("""version: "1.0"
checks:
  must: ["ship.amt", "ship.docs"]
  leak_patterns: ["*客户版*"]
  leak_rules:
    - name: 内部字样
      regex: "内部|机密"
""", encoding="utf-8")

        ok = root / "ok.md"
        ok.write_text(report_text(led), encoding="utf-8")
        client = root / "客户版.md"
        client.write_text(report_text(led), encoding="utf-8")

        # 故障 1：报告改数
        bad = root / "bad.md"
        # 注意：改 1 元在「万元」表述下不可见（四舍五入吃掉），必须改到 1 万元量级
        bad.write_text(report_text(led, amt=float(led["numbers"][0]["value"]) + 10000), encoding="utf-8")
        # 故障 2：跨件写法不同（同一笔多写一位小数）
        cross = root / "摘要.md"
        cross.write_text(report_text(led, dec=2), encoding="utf-8")   # 34.00 万元 vs 34.0 万元
        # 故障 3：客户版塞内部词
        leak = root / "客户版-泄漏.md"
        leak.write_text(report_text(led) + "\n内部备注：这单有风险。\n", encoding="utf-8")
        # 故障 4：账本编数
        tampered = root / "ledger_tampered.json"
        t = json.loads(json.dumps(led))
        t["numbers"][0]["value"] = float(t["numbers"][0]["value"]) + 100
        tampered.write_text(json.dumps(t, ensure_ascii=False), encoding="utf-8")

        # ── 用例 6/7（v3.5.0）：产物层 ──────────────────────────
        rc6, out6, dir6 = run_full(ledger, [ok, cross], pol, db, mode,
                                   out_dir=root / "out_case6")
        h6 = (dir6 / "audit.html").read_text(encoding="utf-8")
        md6 = (dir6 / "audit.md").read_text(encoding="utf-8")
        case6_ok = (rc6 == 3 and "跨件一致性" in h6 and BAD in h6
                    and "需人工复核" in md6.split("## 判定依据")[0])
        case6_note = f"exit={rc6} 矩阵={'有' if '跨件一致性' in h6 else '无'} " \
                     f"红格={h6.count(BAD)}"
        rc7, out7, dir7 = run_full(ledger, [ok], pol, db, mode,
                                   out_dir=root / "out_case7")
        art7, note7 = check_artifacts(dir7, "✅ 通过")
        # audit_id 稳定性：同一账本同一数据跑两次必须相同
        _, _, dir7b = run_full(ledger, [ok], pol, db, mode,
                               out_dir=root / "out_case7b")
        id_a = json.loads((dir7 / "manifest.json").read_text(encoding="utf-8"))["audit_id"]
        id_b = json.loads((dir7b / "manifest.json").read_text(encoding="utf-8"))["audit_id"]
        id_ok = id_a == id_b
        case7_ok = art7 and id_ok
        case7_note = note7 if not art7 else ("" if id_ok else f"audit_id 不稳定 {id_a}/{id_b}")

        cases = [
            ("正确报告应通过", run(ledger, [ok, client], pol, db, mode), 0),
            ("报告改数应被拦", run(ledger, [bad], pol, db, mode), 1),
            ("跨件写法不同应报", run(ledger, [ok, cross], pol, db, mode), (1, 3)),
            ("客户版泄漏应被拦", run(ledger, [leak], pol, db, mode), (1, 3)),
            ("账本编数应被拦", run(tampered, [ok], pol, db, mode), 1),
        ]
        print(f"{'用例':<24}{'结果'}")
        passed = 0
        for name, code, expect in cases:
            exp = expect if isinstance(expect, tuple) else (expect,)
            good = code in exp
            passed += good
            print(f"{'✅' if good else '❌'} {name:<22} 退出码 {code}（期望 {'/'.join(map(str, exp))}）")
        passed += case6_ok
        print(f"{'✅' if case6_ok else '❌'} {'多文件不一致应报并标红':<20} {case6_note}")
        passed += case7_ok
        print(f"{'✅' if case7_ok else '❌'} {'产物完整且编号稳定':<20} {case7_note}")

        total = len(cases) + 2
        print(f"\n{passed}/{total} 通过"
              + ("（sqlite 降级模式：复算走 --command）" if mode == "degraded" else ""))
        if passed == total:
            print("✅ 自检通过：复算、跨件、泄漏、编数四类问题都能抓到，"
                  "且 HTML/CSV/回执三件产物完整")
            return 0
        print("❌ 自检未通过：说明有检查在空转，别急着用")
        return 1
    finally:
        if args.keep:
            print(f"\n临时目录已保留：{root}")
        else:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
