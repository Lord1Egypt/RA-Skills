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
    repo = str(payload.get("repo", "")).strip()
    issue_title = str(payload.get("issue_title", "")).strip()
    issue_body = str(payload.get("issue_body", "")).strip()

    if not user_id:
        raise ValidationError("`user_id` is required")
    if not re.match(r"^[^/\s]+/[^/\s]+$", repo):
        raise ValidationError("`repo` must be in owner/repo format")
    if len(issue_title) < 4:
        raise ValidationError("`issue_title` is too short")
    if len(issue_body) < 10:
        raise ValidationError("`issue_body` is too short")

    return {
        "user_id": user_id,
        "repo": repo,
        "issue_title": issue_title,
        "issue_body": issue_body,
    }


def _build_free_reply(issue_title: str, issue_body: str) -> dict[str, Any]:
    body_preview = issue_body.strip().replace("\n", " ")[:120]
    is_bug = any(token in f"{issue_title} {issue_body}".lower() for token in ["bug", "error", "crash", "异常", "报错"])

    if is_bug:
        label = "bug"
        reply = (
            "感谢反馈，我们已确认这是一个可复现问题。\n"
            "为加快修复，请补充：复现步骤、预期结果、实际结果和运行环境。\n"
            "我们会在定位后同步修复进展。"
        )
    else:
        label = "enhancement"
        reply = (
            "感谢建议！这个需求方向很有价值。\n"
            "我们会先评估适用场景、实现成本和对现有用户的影响，\n"
            "确认后会在 roadmap 中同步优先级与预期时间。"
        )

    checklist = [
        "确认 issue 分类和优先级",
        "补齐复现信息或业务背景",
        "关联到对应里程碑",
    ]

    return {
        "suggested_label": label,
        "reply": reply,
        "checklist": checklist,
        "context_preview": body_preview,
    }


def run(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_payload(payload)
    tier = str(payload.get("tier", "free")).strip().lower()

    upgrade = {
        "premium_available": True,
        "price_usdt": "0.10",
        "payment_url": _payment_url(validated["user_id"]),
        "premium_features": ["多语种回复", "自动生成修复草案", "关联相似issue聚类"],
    }

    if tier == "premium":
        return {
            "success": False,
            "error": "PREMIUM_UPGRADE_REQUIRED",
            "message": "当前仅开放免费基础版，付费高级版接口已预留。",
            "upgrade": upgrade,
        }

    return {
        "success": True,
        "tier": "free",
        "repo": validated["repo"],
        "issue_title": validated["issue_title"],
        "suggestion": _build_free_reply(validated["issue_title"], validated["issue_body"]),
        "upgrade": upgrade,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GitHub issue reply assistant (free tier)")
    parser.add_argument("--input-json")
    parser.add_argument("--input-file")
    parser.add_argument("--user-id")
    parser.add_argument("--repo")
    parser.add_argument("--issue-title")
    parser.add_argument("--issue-body")
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
        "repo": args.repo,
        "issue_title": args.issue_title,
        "issue_body": args.issue_body,
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
