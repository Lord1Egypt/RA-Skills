#!/usr/bin/env python3
"""
IMAP 邮件处理流水线 —— 调度主入口（main.py）v1.0.0
"""

__version__ = "1.0.0"

import os
import sys
import json
from datetime import datetime

from reader import fetch_emails, resolve_server, PROVIDER_ROUTES
from pusher import push as push_message


def _from_env() -> dict:
    if not os.environ.get("SKILL_EMAIL_ACCOUNT"):
        return {}
    return {
        "email_account":    os.environ.get("SKILL_EMAIL_ACCOUNT", ""),
        "auth_password":    os.environ.get("SKILL_AUTH_PASSWORD", ""),
        "provider":         os.environ.get("SKILL_PROVIDER", ""),
        "imap_host":        os.environ.get("SKILL_IMAP_HOST", ""),
        "imap_port":        int(os.environ.get("SKILL_IMAP_PORT", "0") or 0),
        "start_datetime":   os.environ.get("SKILL_START_DATETIME", ""),
        "end_datetime":     os.environ.get("SKILL_END_DATETIME", ""),
        "subject_keywords": os.environ.get("SKILL_SUBJECT_KEYWORDS", ""),
        "body_keywords":    os.environ.get("SKILL_BODY_KEYWORDS", ""),
        "match_logic":      os.environ.get("SKILL_MATCH_LOGIC", "AND"),
        "extract_patterns": os.environ.get("SKILL_EXTRACT_PATTERNS", ""),
        "preview_length":   int(os.environ.get("SKILL_PREVIEW_LENGTH", "500") or 500),
        "push_platform":    os.environ.get("SKILL_PUSH_PLATFORM", ""),
        "webhook_url":      os.environ.get("SKILL_WEBHOOK_URL", ""),
        "push_secret":      os.environ.get("SKILL_PUSH_SECRET", ""),
    }


def _from_stdin() -> dict:
    if sys.stdin.isatty():
        return {}
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def _load_params() -> dict:
    p = _from_env() or _from_stdin()
    if not p:
        _exit_error("缺少参数。请通过环境变量或 stdin JSON 提供 email_account 与 auth_password。")

    for k, v in {
        "provider": "", "imap_host": "", "imap_port": 0,
        "start_datetime": "", "end_datetime": "",
        "subject_keywords": "", "body_keywords": "", "match_logic": "AND",
        "extract_patterns": None, "preview_length": 500,
        "push_platform": "", "webhook_url": "", "push_secret": "",
    }.items():
        p.setdefault(k, v)
    return p


def _exit_error(msg: str):
    print(json.dumps({"success": False, "error": msg}, ensure_ascii=False), flush=True)
    sys.exit(1)


def _describe_filter(window, subj, body, logic, patterns) -> str:
    parts = [f"时间窗[{window['from']} ~ {window['to']}]"]
    if subj:
        parts.append(f"主题[{logic}:{subj}]")
    if body:
        parts.append(f"正文[{logic}:{body}]")
    if patterns:
        names = ",".join(patterns.keys()) if isinstance(patterns, dict) else "patterns"
        parts.append(f"提取[{names}]")
    return " AND ".join(parts)


def main():
    p = _load_params()

    email_account = (p.get("email_account") or "").strip()
    auth_password = (p.get("auth_password") or "").strip()
    if not email_account or not auth_password:
        _exit_error("email_account 和 auth_password 均为必填项。")

    # extract_patterns：dict 直传 或 JSON 字符串
    patterns = p.get("extract_patterns")
    if isinstance(patterns, str):
        patterns = patterns.strip()
        if patterns:
            try:
                patterns = json.loads(patterns)
            except json.JSONDecodeError as exc:
                _exit_error(f"extract_patterns 不是合法 JSON：{exc}")
        else:
            patterns = None

    try:
        result = fetch_emails(
            email_account    = email_account,
            auth_password    = auth_password,
            start_datetime   = (p.get("start_datetime") or "").strip(),
            end_datetime     = (p.get("end_datetime") or "").strip(),
            subject_keywords = p.get("subject_keywords", ""),
            body_keywords    = p.get("body_keywords", ""),
            match_logic      = (p.get("match_logic") or "AND").upper(),
            extract_patterns = patterns,
            preview_length   = int(p.get("preview_length") or 500),
            provider         = (p.get("provider") or "").strip(),
            imap_host        = (p.get("imap_host") or "").strip(),
            imap_port        = int(p.get("imap_port") or 0),
        )
    except Exception as exc:
        _exit_error(f"邮件抓取失败：{exc}")

    filter_desc = _describe_filter(
        result["window"], p.get("subject_keywords", ""),
        p.get("body_keywords", ""), (p.get("match_logic") or "AND").upper(),
        patterns,
    )

    output = {
        "success": True,
        "server":  result["server"],
        "window":  result["window"],
        "filter":  filter_desc,
        "count":   len(result["emails"]),
        "emails":  result["emails"],
    }

    platform = (p.get("push_platform") or "").strip().lower()
    if platform:
        output["push"] = push_message(
            platform    = platform,
            webhook_url = (p.get("webhook_url") or "").strip(),
            secret      = (p.get("push_secret") or "").strip(),
            emails      = result["emails"],
            keyword_desc= filter_desc,
        )

    print(json.dumps(output, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
