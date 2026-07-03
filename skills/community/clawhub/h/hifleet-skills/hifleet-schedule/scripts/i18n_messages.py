#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""User-facing messages for hifleet-schedule. English source; localize per agent locale."""

from __future__ import annotations

import os
from typing import Any

_LOCALE_ENV_KEYS = (
    "HIFLEET_USER_LOCALE",
    "OPENCLAW_USER_LOCALE",
    "OPENCLAW_LOCALE",
    "CURSOR_AGENT_LOCALE",
    "LANG",
)

_MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "skill.reply_language": "Reply to the user in English unless they write in another language.",
        "config.missing_api_key": "HiFleet API Key is required. See FIRST_SETUP.md to configure hifleet_api_key.",
        "schedule.missing_port": "Please provide a port name or code for schedule search.",
        "schedule.no_results": "No liner schedules found for the given criteria.",
        "schedule.full_list_note": "Showing all {count} schedule rows (full list policy).",
        "schedule.unlock_hint": "Some rows may be locked; use unlock API per SCHEDULE_API.md if needed.",
        "schedule.api_error": "Schedule API request failed: {detail}",
    },
    "zh": {
        "skill.reply_language": "除用户主动使用其他语言外，优先用简体中文回复；业务数据（船名、港口、航线、货物名等）保持原文。",
        "config.missing_api_key": "需要配置 HiFleet API Key，请在 FIRST_SETUP.md 中设置 hifleet_api_key。",
        "schedule.missing_port": "请提供港口名称或代码以查询班轮船期。",
        "schedule.no_results": "未找到符合条件的班轮船期。",
        "schedule.full_list_note": "已按全量策略展示全部 {count} 条船期。",
        "schedule.unlock_hint": "部分记录可能为锁定状态；如需解锁请参阅 SCHEDULE_API.md。",
        "schedule.api_error": "船期接口请求失败：{detail}",
    },
    "zh-CN": {},
    "zh-TW": {
        "skill.reply_language": "除使用者主動使用其他語言外，優先以繁體中文回覆；業務資料（船名、港口、航線、貨物名等）保持原文。",
        "config.missing_api_key": "需要設定 HiFleet API Key，請參閱 FIRST_SETUP.md 設定 hifleet_api_key。",
        "schedule.missing_port": "請提供港口名稱或代碼以查詢班輪船期。",
        "schedule.no_results": "未找到符合條件的班輪船期。",
        "schedule.full_list_note": "已依全量策略展示全部 {count} 條船期。",
        "schedule.unlock_hint": "部分記錄可能為鎖定狀態；如需解鎖請參閱 SCHEDULE_API.md。",
        "schedule.api_error": "船期介面請求失敗：{detail}",
    },
}

_MESSAGES["zh-CN"] = _MESSAGES["zh"]


def resolve_user_locale() -> str:
    for key in _LOCALE_ENV_KEYS:
        raw = os.environ.get(key, "").strip()
        if not raw:
            continue
        loc = raw.split(".")[0].replace("_", "-")
        if loc.lower().startswith("zh"):
            if "tw" in loc.lower() or "hant" in raw.lower():
                return "zh-TW"
            return "zh"
        if loc.lower().startswith("en"):
            return "en"
        return loc
    return "en"


def t(key: str, locale: str | None = None, **kwargs: Any) -> str:
    loc = locale or resolve_user_locale()
    table = _MESSAGES.get(loc) or _MESSAGES.get(loc.split("-")[0]) or _MESSAGES["en"]
    msg = table.get(key) or _MESSAGES["en"].get(key) or key
    if kwargs:
        try:
            return msg.format(**kwargs)
        except (KeyError, ValueError):
            return msg
    return msg
