"""Minimal zero-dep i18n for user-facing DLC strings.

Same resolution rule as Core's i18n: NO0_LANG wins, otherwise LC_ALL/LANG
prefix drives zh vs en. Duplicated (not imported from Core) so DLC stays
self-contained for separate installs.
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
    # cognitive_event_handler.py — L5 push alert body
    "push.header": {
        "zh": "⚠️ 紧急：L5 认知文件篡改",
        "en": "⚠️ URGENT: L5 cognitive file tampering",
    },
    "push.file": {"zh": "文件：{name}", "en": "File: {name}"},
    "push.time": {"zh": "时间：{ts}", "en": "Time: {ts}"},
    "push.rules": {"zh": "命中规则：{rules}", "en": "Rule hits: {rules}"},
    "push.none": {"zh": "(无)", "en": "(none)"},
    "push.versions_label": {"zh": "可选版本：", "en": "Available versions:"},
    "push.versions_unavailable": {
        "zh": "(不可用 — 请跑 ./no0 versions)",
        "en": "(unavailable — run ./no0 versions)",
    },
    "push.prompt": {
        "zh": "请回复 'rollback v<n>' 选择恢复，或 'keep' 接受现状。",
        "en": "Reply 'rollback v<n>' to restore, or 'keep' to accept as-is.",
    },
    "push.cleanup": {
        "zh": "处置后请删除：{lock}",
        "en": "After deciding, delete: {lock}",
    },
    # dlc_cli.py — decide command user-facing messages
    "decide.no_pending": {
        "zh": "[dlc] 无待处置决定：{name}",
        "en": "[dlc] No pending decision for {name}.",
    },
    "decide.no_pending_at": {
        "zh": "[dlc] 无待处置决定：{name} 位于 {lock}",
        "en": "[dlc] No pending decision for {name} at {lock}",
    },
    "decide.prior_failures": {
        "zh": "\n[dlc] ⚠ {name} 此前有 {n} 次推送失败：",
        "en": "\n[dlc] ⚠ {n} prior push failure(s) for {name}:",
    },
    "decide.prior_failure_row": {
        "zh": "  - 原因={reason}  重试={retries}  时间={ts}",
        "en": "  - reason={reason}  retries={retries}  recorded_at={ts}",
    },
    "decide.rollback_needs_version": {
        "zh": "[dlc] 'rollback' 需要指定版本（如 v3）。",
        "en": "[dlc] 'rollback' requires a version (e.g. v3).",
    },
    "decide.no_dispatcher": {
        "zh": "[dlc] 找不到 ./no0 调度器。",
        "en": "[dlc] Could not locate ./no0 dispatcher.",
    },
    "decide.rollback_failed": {
        "zh": "[dlc] 回滚失败 (rc={rc})；保留 lock。",
        "en": "[dlc] rollback failed (rc={rc}); lock preserved.",
    },
    "decide.available_versions": {
        "zh": "[dlc] 可用版本：",
        "en": "[dlc] Available versions:",
    },
    "decide.retry_hint": {
        "zh": "[dlc] 重试：./no0 decide {name} rollback <version>",
        "en": "[dlc] Try: ./no0 decide {name} rollback <version>",
    },
    "decide.rolled_back": {
        "zh": "[dlc] 已将 {name} 回滚到 {version}；lock 已释放。",
        "en": "[dlc] rolled back {name} to {version}; lock released.",
    },
    "decide.kept": {
        "zh": "[dlc] 已保留 {name} 当前状态；lock 已释放。",
        "en": "[dlc] kept {name} as-is; lock released.",
    },
    "decide.unknown_action": {
        "zh": "[dlc] 未知操作：'{action}'",
        "en": "[dlc] unknown action '{action}'",
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
