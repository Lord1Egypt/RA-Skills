#!/usr/bin/env python3
"""Validate normalized period metrics and build a reproducible metric bundle."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

PACKAGE_ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(PACKAGE_ROOT/'scripts'))
from artifact_contract import native_fact_identity,validate_fact_identity

CORE_FIELDS = ("period", "gmv", "visitors", "buyers", "orders")
RATE_FIELDS = ("gross_margin_rate", "commission_rate", "refund_loss_rate")
NON_NEGATIVE_FIELDS = (
    "gmv",
    "visitors",
    "buyers",
    "orders",
    "refund_amount",
    "ad_spend",
    "fulfillment_cost_per_order",
    "search_gmv",
    "search_visitors",
    "search_buyers",
    "observed_cpc",
)
OPTIONAL_FIELDS = (
    "refund_amount",
    "ad_spend",
    "gross_margin_rate",
    "commission_rate",
    "fulfillment_cost_per_order",
    "refund_loss_rate",
    "search_gmv",
    "search_visitors",
    "search_buyers",
    "observed_cpc",
)


def parse_number(value: Any, *, rate: bool = False) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        is_percent = value.endswith("%")
        value = value.rstrip("%").replace(",", "")
    else:
        is_percent = False
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"不是有效数字: {value!r}") from exc
    if is_percent:
        number /= Decimal("100")
    if rate and not (Decimal("0") <= number <= Decimal("1")):
        raise ValueError(f"比例字段必须为 0~1 小数或百分数字符串: {value!r}")
    return number


def safe_div(numerator: Decimal | None, denominator: Decimal | None) -> Decimal | None:
    if numerator is None or denominator in (None, Decimal("0")):
        return None
    return numerator / denominator


def as_number(value: Decimal | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    quantum = Decimal("1").scaleb(-digits)
    return float(value.quantize(quantum))


def add_issue(
    issues: list[dict[str, str]], severity: str, code: str, message: str, period: str = ""
) -> None:
    issues.append(
        {"severity": severity, "code": code, "period": period, "message": message}
    )


def normalize_row(raw: dict[str, Any], issues: list[dict[str, str]]) -> dict[str, Any]:
    period = str(raw.get("period", "")).strip()
    row: dict[str, Any] = {"period": period}
    if not period:
        add_issue(issues, "error", "missing_period", "period 不能为空")

    for field in CORE_FIELDS[1:] + OPTIONAL_FIELDS:
        try:
            row[field] = parse_number(raw.get(field), rate=field in RATE_FIELDS)
        except ValueError as exc:
            row[field] = None
            add_issue(issues, "error", "invalid_number", f"{field}: {exc}", period)

    for field in CORE_FIELDS[1:]:
        if row[field] is None:
            add_issue(issues, "error", "missing_core_field", f"缺少核心字段 {field}", period)

    for field in NON_NEGATIVE_FIELDS:
        if row.get(field) is not None and row[field] < 0:
            add_issue(issues, "error", "negative_value", f"{field} 不得为负数", period)

    visitors, buyers, orders = row.get("visitors"), row.get("buyers"), row.get("orders")
    if visitors == 0 and buyers not in (None, 0):
        add_issue(issues, "error", "zero_denominator", "访客为 0 但买家不为 0", period)
    if visitors is not None and buyers is not None and buyers > visitors:
        add_issue(issues, "warning", "buyers_gt_visitors", "买家数大于访客数，检查人数口径", period)
    if orders is not None and buyers is not None and orders < buyers:
        add_issue(issues, "warning", "orders_lt_buyers", "订单数小于买家数，检查人数/订单口径", period)

    gmv, refund = row.get("gmv"), row.get("refund_amount")
    if gmv is not None and refund is not None and refund > gmv:
        add_issue(
            issues,
            "warning",
            "refund_gt_gmv",
            "退款额大于同期 GMV；可能存在退款错期，禁止直接解释为当期经营亏损",
            period,
        )

    search_fields = ("search_gmv", "search_visitors", "search_buyers")
    present = [row.get(field) is not None for field in search_fields]
    if any(present) and not all(present):
        add_issue(
            issues,
            "warning",
            "partial_search_contract",
            "搜索渠道字段不完整，无法计算同口径搜索转化与可承受 CPC",
            period,
        )
    if row.get("search_visitors") == 0 and row.get("search_buyers") not in (None, 0):
        add_issue(issues, "error", "zero_search_denominator", "搜索访客为 0 但搜索买家不为 0", period)

    return row


def compute_metrics(row: dict[str, Any]) -> dict[str, Any]:
    gmv = row.get("gmv")
    visitors = row.get("visitors")
    buyers = row.get("buyers")
    refund = row.get("refund_amount")
    ad_spend = row.get("ad_spend")

    conversion_rate = safe_div(buyers, visitors)
    aov = safe_div(gmv, buyers)
    refund_rate = safe_div(refund, gmv)
    net_gmv = gmv - refund if gmv is not None and refund is not None else None
    roas = safe_div(gmv, ad_spend)
    net_roas = safe_div(net_gmv, ad_spend)

    search_uv_value = safe_div(row.get("search_gmv"), row.get("search_visitors"))
    search_conversion_rate = safe_div(row.get("search_buyers"), row.get("search_visitors"))
    allowable_inputs = (
        search_uv_value,
        search_conversion_rate,
        refund_rate,
        row.get("gross_margin_rate"),
        row.get("commission_rate"),
        row.get("fulfillment_cost_per_order"),
        row.get("refund_loss_rate"),
    )
    allowable_cpc = None
    if all(value is not None for value in allowable_inputs):
        gross_margin = row["gross_margin_rate"]
        commission = row["commission_rate"]
        fulfillment = row["fulfillment_cost_per_order"]
        refund_loss = row["refund_loss_rate"]
        allowable_cpc = (
            search_uv_value * (Decimal("1") - refund_rate) * (gross_margin - commission)
            - search_conversion_rate * fulfillment
            - search_uv_value
            * refund_rate
            * refund_loss
            * (Decimal("1") - gross_margin)
        )

    observed_cpc = row.get("observed_cpc")
    cpc_headroom = (
        allowable_cpc - observed_cpc
        if allowable_cpc is not None and observed_cpc is not None
        else None
    )

    return {
        "period": row["period"],
        "inputs": {
            field: as_number(row.get(field))
            for field in CORE_FIELDS[1:] + OPTIONAL_FIELDS
            if row.get(field) is not None
        },
        "metrics": {
            "conversion_rate": as_number(conversion_rate),
            "aov": as_number(aov),
            "refund_rate_amount": as_number(refund_rate),
            "net_gmv_reference": as_number(net_gmv),
            "roas": as_number(roas),
            "net_roas_reference": as_number(net_roas),
            "search_uv_value": as_number(search_uv_value),
            "search_conversion_rate": as_number(search_conversion_rate),
            "allowable_cpc_scenario": as_number(allowable_cpc),
            "cpc_headroom": as_number(cpc_headroom),
        },
    }


def analyze(rows: list[dict[str, Any]], source: str = "") -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    if not rows:
        add_issue(issues, "error", "empty_input", "输入没有数据行")

    normalized = [normalize_row(row, issues) for row in rows]
    seen: set[str] = set()
    for row in normalized:
        period = row["period"]
        if period and period in seen:
            add_issue(issues, "error", "duplicate_period", "同一期间出现多行", period)
        seen.add(period)

    if any(issue["severity"] == "error" for issue in issues):
        status = "BLOCKED"
    elif issues:
        status = "WARN"
    else:
        status = "PASS"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "gate_status": status,
        "issues": issues,
        "rows": [compute_metrics(row) for row in normalized],
        "notes": [
            "net_gmv_reference 仅为 GMV-退款额，不自动等于财务确认收入或回款",
            "allowable_cpc_scenario 仅在搜索渠道与成本字段齐全时生成，不是建议出价",
            "脚本不会为缺失成本填默认值",
        ],
    }


def load_rows(path: Path,team_version: str,run_id: str,client_scope: str) -> tuple[list[dict[str, Any]],str]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle)),"direct_scoped_csv"
    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8-sig") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
            validate_fact_identity(payload,"normalized_report",team_version,run_id,client_scope)
            return payload["rows"],"native_normalized_report"
        raise ValueError("2.0 JSON 必须是绑定本次客户、运行和版本的 normalized-report")
    raise ValueError("仅支持规范 CSV 或 JSON")


def self_test() -> None:
    valid = analyze(
        [
            {
                "period": "2026-07",
                "gmv": "10000",
                "visitors": "1000",
                "buyers": "100",
                "orders": "120",
                "refund_amount": "1000",
                "ad_spend": "1000",
            }
        ]
    )
    assert valid["gate_status"] == "PASS"
    assert valid["rows"][0]["metrics"]["conversion_rate"] == 0.1
    assert valid["rows"][0]["metrics"]["refund_rate_amount"] == 0.1

    duplicate = analyze(
        [
            {"period": "2026-07", "gmv": 1, "visitors": 1, "buyers": 1, "orders": 1},
            {"period": "2026-07", "gmv": 1, "visitors": 1, "buyers": 1, "orders": 1},
        ]
    )
    assert duplicate["gate_status"] == "BLOCKED"
    print("metric_gate self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验规范化电商期间指标并输出可复算指标包"
    )
    parser.add_argument("input", nargs="?", help="规范 CSV 或 JSON")
    parser.add_argument("--output", help="输出 JSON 路径；省略时打印到标准输出")
    parser.add_argument("--source-label", help="输出中的来源标签；默认只保留输入文件名，不写入绝对路径")
    parser.add_argument("--run-id", help="本次运行编号")
    parser.add_argument("--client-scope", help="本次客户范围")
    parser.add_argument("--team-version", help="本次专家团版本")
    parser.add_argument("--self-test", action="store_true", help="运行内置测试")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.self_test:
        self_test()
        return 0
    if not args.input:
        parser.error("必须提供 input，或使用 --self-test")
    if not all((args.run_id,args.client_scope,args.team_version)):
        parser.error("2.0 输出必须提供 --run-id、--client-scope 和 --team-version")

    input_path = Path(args.input).resolve()
    try:
        rows,source_contract=load_rows(input_path,args.team_version,args.run_id,args.client_scope)
        result = analyze(rows, args.source_label or input_path.name)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    result.update(**native_fact_identity('metric_gate',args.team_version),run_id=args.run_id,
                  client_scope=args.client_scope,team_version=args.team_version,
                  source_file=input_path.name,source_sha256=hashlib.sha256(input_path.read_bytes()).hexdigest(),
                  source_contract=source_contract)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output).resolve()
        if output_path==input_path or (output_path.exists() and input_path.exists() and output_path.samefile(input_path)):
            print("ERROR: metric_output_overlaps_input",file=sys.stderr); return 2
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload + "\n", encoding="utf-8")
        print(output_path)
    else:
        print(payload)
    return 0 if result["gate_status"] != "BLOCKED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
