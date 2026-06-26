#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any


class ValidationError(ValueError):
    pass


def _payment_url(user_id: str) -> str:
    template = os.getenv("SKILLPAY_PAYMENT_URL_TEMPLATE", "").strip()
    if template:
        return template.format(user_id=user_id)
    base = os.getenv("SKILLPAY_TOPUP_BASE_URL", "https://skillpay.me/pay").strip()
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}user_id={user_id}"


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    user_id = str(payload.get("user_id", "")).strip()
    week_label = str(payload.get("week_label", "")).strip()
    records = payload.get("records", [])

    if not user_id:
        raise ValidationError("`user_id` is required")
    if len(week_label) < 2:
        raise ValidationError("`week_label` is required")
    if not isinstance(records, list) or not records:
        raise ValidationError("`records` must be a non-empty list")

    normalized = []
    for item in records:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "title": str(item.get("title", "")).strip() or "未命名事项",
                "owner": str(item.get("owner", "")).strip() or "未分配",
                "status": str(item.get("status", "进行中")).strip(),
                "progress": int(item.get("progress", 0)) if str(item.get("progress", "")).isdigit() else 0,
            }
        )

    if not normalized:
        raise ValidationError("`records` contains no valid rows")

    return {
        "user_id": user_id,
        "week_label": week_label,
        "records": normalized,
    }


def _build_report(week_label: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(records)
    done = len([row for row in records if row["status"] in ["done", "完成", "已完成"]])
    in_progress = len([row for row in records if row["status"] in ["doing", "进行中", "in_progress"]])
    avg_progress = round(sum(int(row.get("progress", 0)) for row in records) / total, 1)

    top_risks = [row["title"] for row in records if int(row.get("progress", 0)) < 40][:3]
    highlights = [row["title"] for row in records if int(row.get("progress", 0)) >= 80][:3]

    lines = [
        f"# {week_label} 周报",
        "",
        "## 数据概览",
        f"- 总任务数：{total}",
        f"- 已完成：{done}",
        f"- 进行中：{in_progress}",
        f"- 平均进度：{avg_progress}%",
        "",
        "## 本周亮点",
    ]
    lines.extend([f"- {item}" for item in (highlights or ["暂无高进度事项"])])
    lines.append("")
    lines.append("## 风险与阻塞")
    lines.extend([f"- {item}" for item in (top_risks or ["暂无明显阻塞"])])

    return {
        "stats": {
            "total": total,
            "done": done,
            "in_progress": in_progress,
            "avg_progress": avg_progress,
        },
        "markdown": "\n".join(lines),
        "highlights": highlights,
        "risks": top_risks,
    }


def run(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_payload(payload)
    tier = str(payload.get("tier", "free")).strip().lower()

    upgrade = {
        "premium_available": True,
        "price_usdt": "0.10",
        "payment_url": _payment_url(validated["user_id"]),
        "premium_features": ["自动生成趋势图", "跨周对比分析", "自动发送管理层摘要"],
    }

    if tier == "premium":
        return {
            "success": False,
            "error": "PREMIUM_UPGRADE_REQUIRED",
            "message": "当前仅开放免费基础版，付费高级版接口已预留。",
            "upgrade": upgrade,
        }

    report = _build_report(validated["week_label"], validated["records"])
    return {
        "success": True,
        "tier": "free",
        "week_label": validated["week_label"],
        "report": report,
        "upgrade": upgrade,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notion DB to weekly report generator (free tier)")
    parser.add_argument("--input-json")
    parser.add_argument("--input-file")
    parser.add_argument("--user-id")
    parser.add_argument("--week-label")
    parser.add_argument("--records-json", help="JSON list string for records")
    parser.add_argument("--tier", default="free")
    return parser.parse_args()


def _payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.input_json:
        return json.loads(args.input_json)
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as file:
            return json.load(file)
    records = json.loads(args.records_json) if args.records_json else []
    return {
        "user_id": args.user_id,
        "week_label": args.week_label,
        "records": records,
        "tier": args.tier,
    }


def main() -> int:
    args = _parse_args()
    try:
        result = run(_payload_from_args(args))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success") else 3
    except ValidationError as err:
        print(json.dumps({"success": False, "error": "VALIDATION_ERROR", "message": str(err)}, ensure_ascii=False))
        return 2
    except json.JSONDecodeError as err:
        print(json.dumps({"success": False, "error": "INVALID_JSON", "message": str(err)}, ensure_ascii=False))
        return 5


if __name__ == "__main__":
    sys.exit(main())
