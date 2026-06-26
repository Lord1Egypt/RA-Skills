"""Minimal zero-dep i18n for user-facing Core strings.

Resolution order:
  1. NO0_LANG env: explicit "en" or "zh" wins.
  2. LC_ALL / LANG env: if it starts with "zh" → zh; any other non-empty
     value → en. Empty/unset → zh (preserves existing Chinese defaults).

Keep the catalog below narrow: audit.csv action labels, rule-group names,
and internal debug logs stay as-is. Only translate text a user reads.
"""
from __future__ import annotations

import os
from typing import Any, Dict


def resolve_lang() -> str:
    explicit = os.environ.get("NO0_LANG", "").strip().lower()
    if explicit in ("en", "zh"):
        return explicit
    locale = (os.environ.get("LC_ALL") or os.environ.get("LANG") or "").strip().lower()
    if not locale:
        return "zh"
    if locale.startswith("zh"):
        return "zh"
    return "en"


_CATALOG: Dict[str, Dict[str, str]] = {
    # hourly_report.py
    "report.header": {
        "zh": "📋 No.0 hourly report:",
        "en": "📋 No.0 hourly report:",
    },
    "report.new_changes": {
        "zh": "  • {n} 条新变更记录 (change_log)",
        "en": "  • {n} new change record(s) in change_log",
    },
    "report.l5_pushed": {
        "zh": "  • {n} 次 L5 决策已推送",
        "en": "  • {n} L5 decision request(s) pushed",
    },
    "report.l5_deduped": {
        "zh": "  • {n} 次 L5 去重（已有 lock 在等）",
        "en": "  • {n} L5 event(s) deduped (lock already pending)",
    },
    "report.rejected_schema": {
        "zh": "  • {n} 个事件因 schema 不匹配被拒",
        "en": "  • {n} event(s) rejected for schema mismatch",
    },
    "report.locks_header": {
        "zh": "  • {n} 个未处置 L5 锁:",
        "en": "  • {n} outstanding L5 lock(s):",
    },
    "report.locks_hint": {
        "zh": "    处置：./no0 decide <file> rollback v<n> | keep",
        "en": "    Resolve with: ./no0 decide <file> rollback v<n> | keep",
    },
    "report.no_rules": {
        "zh": "(无规则)",
        "en": "(no rules)",
    },
    "report.pending_backlog": {
        "zh": "  ⚠ 事件队列积压：{n} 条未被 DLC 消费",
        "en": "  ⚠ Event queue backlog: {n} event(s) not yet consumed by DLC",
    },
    # skill_launcher.py — status pending line
    "status.pending_prefix": {
        "zh": "\n事件队列 pending: {n}",
        "en": "\nEvent queue pending: {n}",
    },
    "status.pending_detail": {
        "zh": "（最老 {age_h:.1f}h，上限 {cap}，TTL {ttl_h}h）",
        "en": " (oldest {age_h:.1f}h, cap {cap}, TTL {ttl_h}h)",
    },
    "status.pending_warn": {
        "zh": "  ⚠️ 未被 DLC 消费 — 确认 handler 是否运行或装了 DLC",
        "en": "  ⚠️ Not consumed by DLC — check handler is running or DLC installed",
    },
    # event_emitter.py — core direct push
    "core_push.header": {
        "zh": "⚠️ No.0 Core 直推告警（当前没有 DLC handler）",
        "en": "⚠️ No.0 Core direct alert (no DLC handler in charge)",
    },
    "core_push.file": {"zh": "文件：{name}", "en": "File: {name}"},
    "core_push.time": {"zh": "时间：{ts}", "en": "Time: {ts}"},
    "core_push.rules": {"zh": "命中规则：{rules}", "en": "Rules: {rules}"},
    "core_push.none": {"zh": "(无)", "en": "(none)"},
    "core_push.inspect": {
        "zh": "查看版本：./no0 versions {name}",
        "en": "Inspect: ./no0 versions {name}",
    },
}


def t(key: str, **kwargs: Any) -> str:
    entry = _CATALOG.get(key)
    if entry is None:
        return key
    lang = resolve_lang()
    template = entry.get(lang) or entry.get("en") or entry.get("zh") or key
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
