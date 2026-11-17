#!/usr/bin/env python3
"""Regression tests for report_triage.py (fail-closed)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "report_triage.py"
PY = sys.executable

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} :: {detail}")
        FAILURES.append(name)


def write_xlsx(path: Path, rows: list[list]) -> None:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    for r in rows:
        ws.append(r)
    wb.save(path)


def write_csv(path: Path, rows: list[list]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        import csv as _csv
        _csv.writer(fh).writerows(rows)


def run(root: Path, out: Path, extra: list[str] | None = None) -> dict:
    cmd = [PY, str(SCRIPT), "--input-root", str(root), "--output", str(out),
           "--run-id", "smoke-run-0001", "--client-scope", "smoke-client",
           "--team-version", "2.0.3-candidate.1"]
    if extra:
        cmd += extra
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode not in (0, 3):
        raise SystemExit(f"triage crashed rc={proc.returncode}\n{proc.stdout}\n{proc.stderr}")
    return json.loads(proc.stdout)


def load(out: Path) -> dict:
    return json.loads(out.read_text(encoding="utf-8"))


def by_name(inv: dict, name: str) -> dict:
    for r in inv["reports"]:
        if r["file_name"] == name:
            return r
    raise AssertionError(f"{name} missing from inventory")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="triage_smoke_"))
    root = tmp / "input"
    root.mkdir(parents=True)

    # S1: header sits on row 3 (typical 生意参谋 export)
    write_xlsx(root / "交易概况_2026-08.xlsx", [
        ["天猫旗舰店交易概况", None, None, None, None, None],
        ["统计周期：2026-08-01 至 2026-08-31", None, None, None, None, None],
        ["日期", "商品ID", "访客数", "支付金额", "支付买家数", "客单价"],
        ["2026-08-01", "A001", 1200, 34000.5, 80, 425.0],
        ["2026-08-02", "A002", 1350, 36120.0, 86, 420.0],
        ["2026-08-03", "A003", 1100, 29800.0, 71, 419.7],
    ])

    # S2: customer service csv
    write_csv(root / "客服接待报表_2026-08.csv", [
        ["日期", "客服昵称", "接待人数", "首次响应时长", "满意度"],
        ["2026-08-01", "小A", 320, 18, "96%"],
        ["2026-08-02", "小B", 280, 25, "93%"],
    ])

    # S3: unrecognised structure
    write_csv(root / "数据导出.csv", [
        ["a1", "b2", "c3"],
        ["x", "y", "z"],
    ])

    # S4: header only, no data rows
    write_csv(root / "退款明细.csv", [["退款金额", "退款笔数", "退款原因"]])

    # S5: 30% missing but has standard metrics
    sparse = [["日期", "商品ID", "支付金额", "访客数", "备注"]]
    for i in range(1, 11):
        sparse.append([f"2026-08-{i:02d}", f"P{i}",
                       None if i <= 5 else 1000.0 * i, 300 + i, None])
    write_csv(root / "商品明细_2026-08.csv", sparse)

    out1 = tmp / "inv1.json"
    res1 = run(root, out1)
    inv1 = load(out1)

    print("[S1] header offset + trade type")
    check("scans all five files", inv1["report_count"] == 5, str(inv1["report_count"]))
    trade = by_name(inv1, "交易概况_2026-08.xlsx")
    check("trade type detected", trade["report_type"] == "trade_sales", trade["report_type"])
    check("domain transaction", trade["domain"] == "transaction", trade["domain"])
    check("header row offset detected", trade.get("header_row_index") == 2,
          str(trade.get("header_row_index")))
    check("row count excludes title rows", trade["row_count"] == 3, str(trade["row_count"]))
    std = {m["standard_name"] for m in trade["metrics"]}
    check("gmv standardised", "gmv" in std, str(std))
    check("uv standardised", "uv" in std, str(std))
    check("aov standardised", "aov" in std, str(std))
    check("period detected", trade["time_scope"]["start"] == "2026-08-01"
          and trade["time_scope"]["end"] == "2026-08-03",
          f"{trade['time_scope']['start']}..{trade['time_scope']['end']}")
    check("granularity daily", trade["granularity"] == "daily", trade["granularity"])
    check("verdict analyzable", trade["verdict"] == "analyzable", trade["verdict"])
    check("platform tmall", trade["platform"] == "tmall", trade["platform"])

    print("[S2] customer service csv")
    cs = by_name(inv1, "客服接待报表_2026-08.csv")
    check("service type", cs["report_type"] == "customer_service", cs["report_type"])
    check("service domain", cs["domain"] == "service", cs["domain"])
    check("rule identified", cs["identified_by"] == "rule", cs["identified_by"])
    check("high confidence", cs["confidence"] == "high", cs["confidence"])
    check("agent dimension", "agent" in cs["dimensions"], str(cs["dimensions"]))

    print("[S3] unrecognised goes to model review, never dropped")
    unk = by_name(inv1, "数据导出.csv")
    check("still in inventory", unk["report_id"] in [r["report_id"] for r in inv1["reports"]])
    check("type unidentified", unk["report_type"] == "unidentified", unk["report_type"])
    check("in model_review_pending",
          any(p["report_id"] == unk["report_id"] for p in inv1["identification"]["model_review_pending"]))
    check("status flags pending", res1["status"] == "inventory_pending_model_review", res1["status"])

    print("[S4] header-only file is insufficient with reason")
    empty = by_name(inv1, "退款明细.csv")
    check("type from filename", empty["report_type"] == "refund_aftersales", empty["report_type"])
    check("insufficient verdict", empty["verdict"] == "insufficient", empty["verdict"])
    check("reason present", bool(empty.get("verdict_reason")), empty.get("verdict_reason", ""))

    print("[S5] 30% missing degrades to partial, not dropped")
    sp = by_name(inv1, "商品明细_2026-08.csv")
    check("partial verdict", sp["verdict"] in ("partial", "insufficient"), sp["verdict"])
    check("reason present", bool(sp.get("verdict_reason")), sp.get("verdict_reason", ""))

    print("[S6] model verdicts backfill")
    verdicts = tmp / "model-verdicts.json"
    verdicts.write_text(json.dumps({
        unk["report_id"]: {
            "report_type": "market_benchmark",
            "domain": "market",
            "confidence": "medium",
            "identified_by": "model",
            "identify_evidence": ["表头为 a1/b2/c3，模型结合目录名判定为行业大盘导出"],
        }
    }, ensure_ascii=False), encoding="utf-8")
    out2 = tmp / "inv2.json"
    run(root, out2, ["--model-verdicts", str(verdicts)])
    inv2 = load(out2)
    unk2 = by_name(inv2, "数据导出.csv")
    check("model type applied", unk2["report_type"] == "market_benchmark", unk2["report_type"])
    check("identified_by model", unk2["identified_by"] == "model", unk2["identified_by"])
    check("model_hits counted", inv2["identification"]["model_hits"] == 1,
          str(inv2["identification"]["model_hits"]))
    check("no pending left", inv2["identification"]["model_review_pending"] == [],
          str(inv2["identification"]["model_review_pending"]))

    print()
    if FAILURES:
        print(f"FAILED {len(FAILURES)}: {FAILURES}")
        return 1
    print(f"ALL PASSED (6 scenarios, {inv1['report_count']} files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
