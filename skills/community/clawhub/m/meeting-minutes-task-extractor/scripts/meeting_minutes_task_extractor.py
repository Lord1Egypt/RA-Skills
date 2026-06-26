#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
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


def validate_payload(payload: dict[str, Any]) -> dict[str, str]:
    user_id = str(payload.get("user_id", "")).strip()
    meeting_title = str(payload.get("meeting_title", "")).strip()
    meeting_notes = str(payload.get("meeting_notes", "")).strip()

    if not user_id:
        raise ValidationError("`user_id` is required")
    if len(meeting_title) < 2 or len(meeting_title) > 120:
        raise ValidationError("`meeting_title` length must be 2-120")
    if len(meeting_notes) < 20:
        raise ValidationError("`meeting_notes` length must be >= 20")

    return {
        "user_id": user_id,
        "meeting_title": meeting_title,
        "meeting_notes": meeting_notes,
    }


def _extract_tasks(notes: str) -> list[dict[str, str]]:
    lines = [line.strip(" -•\t") for line in notes.splitlines() if line.strip()]
    keywords = ["todo", "to do", "action", "负责", "完成", "截止", "需要", "follow up", "by "]
    tasks: list[dict[str, str]] = []

    for line in lines:
        lowered = line.lower()
        if any(keyword in lowered for keyword in keywords):
            assignee = "待分配"
            due_date = "未设置"

            assignee_match = re.search(r"(由|负责人|owner|@)([^，,。:：\s]{1,20})", line, flags=re.IGNORECASE)
            if assignee_match:
                assignee = assignee_match.group(2)

            due_match = re.search(r"(截止|before|by)\s*([0-9]{4}[-/][0-9]{1,2}[-/][0-9]{1,2}|周[一二三四五六日天]|明天|本周)", line, flags=re.IGNORECASE)
            if due_match:
                due_date = due_match.group(2)

            tasks.append(
                {
                    "task": line,
                    "assignee": assignee,
                    "due_date": due_date,
                    "priority": "P1" if "紧急" in line or "urgent" in lowered else "P2",
                }
            )

    if not tasks:
        fallback = lines[:3] if lines else ["整理会议结论并确认责任人"]
        tasks = [{"task": item, "assignee": "待分配", "due_date": "未设置", "priority": "P2"} for item in fallback]

    return tasks[:5]


def run(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_payload(payload)
    tier = str(payload.get("tier", "free")).strip().lower()

    upgrade = {
        "premium_available": True,
        "price_usdt": "0.10",
        "payment_url": _payment_url(validated["user_id"]),
        "premium_features": ["自动识别更多任务（20条）", "自动拆分里程碑", "导出飞书/Notion任务模板"],
    }

    if tier == "premium":
        return {
            "success": False,
            "error": "PREMIUM_UPGRADE_REQUIRED",
            "message": "当前仅开放免费基础版，付费高级版接口已预留。",
            "upgrade": upgrade,
        }

    tasks = _extract_tasks(validated["meeting_notes"])
    return {
        "success": True,
        "tier": "free",
        "meeting_title": validated["meeting_title"],
        "tasks": tasks,
        "summary": {
            "task_count": len(tasks),
            "high_priority_count": len([item for item in tasks if item["priority"] == "P1"]),
        },
        "upgrade": upgrade,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Meeting minutes to tasks extractor (free tier)")
    parser.add_argument("--input-json")
    parser.add_argument("--input-file")
    parser.add_argument("--user-id")
    parser.add_argument("--meeting-title")
    parser.add_argument("--meeting-notes")
    parser.add_argument("--tier", default="free")
    return parser.parse_args()


def _payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.input_json:
        return json.loads(args.input_json)
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return {
        "user_id": args.user_id,
        "meeting_title": args.meeting_title,
        "meeting_notes": args.meeting_notes,
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
