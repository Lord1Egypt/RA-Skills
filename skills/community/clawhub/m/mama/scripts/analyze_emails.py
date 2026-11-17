#!/usr/bin/env python3
"""Analyze mailbox messages for focus items."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from _version import VERSION

DEFAULT_KEYWORDS = [
    "会议", "培训", "审批", "待办", "任务", "项目", "需求", "合同",
    "报价", "付款", "发票", "客户", "面试", "报名", "确认", "通知",
]
DEFAULT_DEADLINE_HINTS = [
    "截止",
    "截至",
    "限于",
    "之前",
    "前完成",
    "前反馈",
    "前报送",
    "请于",
    "务必于",
    "须于",
    "需于",
    "最迟",
    "办理期限",
    "反馈期限",
    "报送期限",
    "完成时间",
    "截止时间",
    "deadline",
    "due",
    "before",
    "by",
]

DATE_PATTERNS = [
    r"\d{4}[-/年.]\d{1,2}[-/月.]\d{1,2}[日号]?(?:\s*\d{1,2}[:：]\d{2})?\s*(?:之前|前完成|前反馈|前报送|前提交|前)?",
    r"\d{1,2}月\d{1,2}[日号]?(?:\s*(?:上午|下午|晚上)?\s*\d{1,2}[:：]\d{2})?\s*(?:之前|前完成|前反馈|前报送|前提交|前)?",
    r"\d{4}[-/年.]\d{1,2}[-/月.]\d{1,2}[日号]?(?:\s*\d{1,2}[:：]\d{2})?",
    r"\d{1,2}月\d{1,2}[日号]?(?:\s*(?:上午|下午|晚上)?\s*\d{1,2}[:：]\d{2})?",
    r"(?:今天|今日|明天|明日|后天)(?:上午|下午|晚上|下班前)?(?:\s*\d{1,2}[:：]\d{2})?",
    r"(?:本周|下周)[一二三四五六日天](?:前|上午|下午|晚上|下班前)?",
    r"\d{1,2}[:：]\d{2}\s*前",
]

# ---------------------------------------------------------------------------
# Precompiled at import time – avoids re-compilation on every email processed.
# ---------------------------------------------------------------------------
_DEADLINE_SHAPE_RE = re.compile(
    r"(?:\d{1,2}月\d{1,2}[日号]?|\d{4}[-/年.]\d{1,2}[-/月.]\d{1,2}[日号]?|\d{1,2}[:：]\d{2})\s*(?:前|之前|前完成|前反馈|前报送|前提交)",
)
_DATE_PATTERNS_RE = [re.compile(p, flags=re.IGNORECASE) for p in DATE_PATTERNS]


def load_python_config(path: Path) -> dict:
    if not path.exists():
        return {}
    import importlib.util

    spec = importlib.util.spec_from_file_location("digest_config", str(path))
    if spec is None or spec.loader is None:
        return {}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {key: getattr(module, key) for key in dir(module) if key.isupper()}


def extract_deadline_matches(text: str, hints: list[str]) -> list[str]:
    found: list[str] = []
    lower = text.lower()
    has_hint = any(hint.lower() in lower for hint in hints)
    has_deadline_shape = _DEADLINE_SHAPE_RE.search(text)
    if not has_hint and not has_deadline_shape:
        return found

    for compiled in _DATE_PATTERNS_RE:
        for match in compiled.findall(text):
            if isinstance(match, tuple):
                match = "".join(match)
            if match:
                found.append(str(match).strip())

    unique = list(dict.fromkeys(found))
    if unique:
        filtered = []
        for item in sorted(unique, key=len, reverse=True):
            normalized = item.rstrip("前")
            if not any(
                item != other and (item in other or normalized in other)
                for other in filtered
            ):
                filtered.append(item)
        return list(reversed(filtered))[:5]

    for hint in hints:
        idx = lower.find(hint.lower())
        if idx >= 0:
            snippet = text[max(0, idx - 20) : idx + 60].strip()
            if snippet:
                return [snippet]
    return []


def make_summary(body: str) -> str:
    clean = re.sub(r"\s+", " ", (body or "").strip())
    return clean[:220] + ("..." if len(clean) > 220 else "")


def make_todo(subject: str, reasons: list[str], deadlines: list[str]) -> str:
    if deadlines:
        return "按邮件要求在识别到的时间前完成处理或反馈。"
    if "会议" in reasons:
        return "确认会议时间、参会方式和需准备材料。"
    if "培训" in reasons:
        return "确认培训安排，判断是否需要报名、参训或转发。"
    if any(item in reasons for item in ["审批", "待办", "任务", "项目", "需求"]):
        return "确认处理要求、负责人和下一步动作。"
    if any(item in reasons for item in ["合同", "报价", "付款", "发票", "客户"]):
        return "核对业务信息、金额或客户诉求，并安排跟进。"
    if any(item in reasons for item in ["面试", "报名", "确认", "通知"]):
        return "确认是否需要回复、报名、确认或转发相关人员。"
    return f"查看并处理邮件：{subject}"


def analyze_email(
    email_item: dict,
    keywords: list[str],
    deadline_hints: list[str],
    trusted_domains: list[str],
) -> dict:
    subject = email_item.get("subject", "")
    from_addr = email_item.get("from", "")
    body_truncated = email_item.get("body", "")[:3000]
    attachments_str = " ".join(email_item.get("attachments", []))

    # Build and lowercase combined text once; reuse for all keyword checks.
    combined = f"{subject}\n{from_addr}\n{body_truncated}\n{attachments_str}"
    combined_lower = combined.lower()
    matched_keywords = [kw for kw in keywords if kw and kw.lower() in combined_lower]

    # Deadline detection uses subject + body only (excludes from/attachments).
    deadline_text = f"{subject}\n{body_truncated}"
    deadlines = extract_deadline_matches(deadline_text, deadline_hints)
    reasons = matched_keywords[:]
    if deadlines:
        reasons.append("时间要求")

    is_focus = bool(reasons)
    return {
        "account": email_item.get("account", ""),
        "subject": email_item.get("subject", "(无主题)"),
        "from": email_item.get("from", "(未知发件人)"),
        "date": email_item.get("date", ""),
        "message_id": email_item.get("message_id", ""),
        "is_focus": is_focus,
        "matched_keywords": matched_keywords,
        "deadline_matches": deadlines,
        "focus_reasons": list(dict.fromkeys(reasons)),
        "summary": make_summary(email_item.get("body", "")),
        "todo": make_todo(email_item.get("subject", ""), reasons, deadlines),
        "attachments": email_item.get("attachments", []),
        "links": email_item.get("links", []),
    }


def analyze_emails(
    emails: list[dict],
    config: dict | None = None,
    keywords_override: list[str] | None = None,
) -> list[dict]:
    config = config or {}
    keywords = keywords_override or config.get("WATCH_KEYWORDS", DEFAULT_KEYWORDS)
    deadline_hints = config.get("DEADLINE_HINTS", DEFAULT_DEADLINE_HINTS)
    trusted_domains = config.get("TRUSTED_DOMAINS", [])
    return [
        analyze_email(item, keywords, deadline_hints, trusted_domains)
        for item in emails
    ]


def format_markdown(analysis: list[dict], since_hours: int, total_count: int) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    focus = [item for item in analysis if item["is_focus"]]
    lines = [
        "# 多账户邮箱智能体",
        "",
        f"版本：{VERSION}",
        f"检查时间：{now}",
        f"检查范围：最近 {since_hours} 小时",
        f"新邮件：{total_count} 封",
        f"重点邮件：{len(focus)} 封",
        "",
    ]

    if not focus:
        lines.append("本轮已检查，暂无需要重点关注的邮件。")
        return "\n".join(lines)

    lines.append("## 重点事项")
    lines.append("")
    for idx, item in enumerate(focus, 1):
        lines.extend(
            [
                f"### {idx}. {item['subject']}",
                f"- 账号：{item.get('account') or '默认账号'}",
                f"- 发件人：{item['from']}",
                f"- 时间：{item['date']}",
                f"- 命中原因：{'、'.join(item['focus_reasons'])}",
            ]
        )
        if item["deadline_matches"]:
            lines.append(f"- 识别到的时间：{'；'.join(item['deadline_matches'])}")
        if item["summary"]:
            lines.append(f"- 摘要：{item['summary']}")
        lines.append(f"- 待办：{item['todo']}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze email JSON")
    parser.add_argument("json_file")
    parser.add_argument(
        "--config", default=str(Path(__file__).with_name("digest_config.py"))
    )
    parser.add_argument("--keywords", default="")
    parser.add_argument("--since-hours", type=int, default=2)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    emails = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    config = load_python_config(Path(args.config))
    keywords = (
        [item.strip() for item in args.keywords.split(",") if item.strip()]
        if args.keywords
        else None
    )
    analysis = analyze_emails(emails, config, keywords)
    if args.json:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(analysis, args.since_hours, len(emails)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
