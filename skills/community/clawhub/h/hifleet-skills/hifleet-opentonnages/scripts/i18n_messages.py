#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""i18n for hifleet-opentonnages."""

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
        "skill.reply_language": "Reply in English unless the user uses another language.",
        "config.missing_api_key": "HiFleet API Key is required. See FIRST_SETUP.md.",
        "opentonnages.list_note": (
            "Contact details are not shown in the list. "
            "To get them, tell me the record id (shown on each row) or say you want contacts for all rows."
        ),
        "opentonnages.contacts_fetched": "Contact details retrieved for record id {id}.",
        "opentonnages.contacts_need_id": "Please provide the record id from the list (e.g. 12345), or say you want all contacts.",
        "opentonnages.no_results_vessel": "No public open vessels matched your criteria.",
        "opentonnages.no_results_cargo": "No public cargo listings matched your criteria.",
        "opentonnages.api_error": "Open market API failed: {detail}",
        "opentonnages.contact_api_error": "Could not fetch contact details: {detail}",
        "route.redirect_schedule": "Liner schedules → skill **hifleet-schedule**.",
    },
    "zh": {
        "skill.reply_language": "优先简体中文回复；船名、港口、货物名等保持原文。",
        "config.missing_api_key": "需要配置 HiFleet API Key，请参阅 FIRST_SETUP.md。",
        "opentonnages.list_note": (
            "列表默认不展示联系方式。如需查看，请告诉我该条的 **记录 id**（列表中每条都有），"
            "或说需要 **全部** 船舶/货盘的联系方式。"
        ),
        "opentonnages.contacts_fetched": "已获取记录 id {id} 的联系方式。",
        "opentonnages.contacts_need_id": "请提供列表中的记录 id（例如 12345），或说明需要全部联系方式。",
        "opentonnages.no_results_vessel": "未找到符合条件的公开船盘。",
        "opentonnages.no_results_cargo": "未找到符合条件的公开货盘。",
        "opentonnages.api_error": "公开船货盘接口请求失败：{detail}",
        "opentonnages.contact_api_error": "获取联系方式失败：{detail}",
        "route.redirect_schedule": "班轮船期请使用 **hifleet-schedule** 技能。",
    },
    "zh-CN": {},
    "zh-TW": {
        "skill.reply_language": "優先繁體中文回覆；業務資料保持原文。",
        "config.missing_api_key": "需要設定 HiFleet API Key，請參閱 FIRST_SETUP.md。",
        "opentonnages.list_note": (
            "列表預設不展示聯絡方式。如需查看，請告訴我該條的 **記錄 id**，"
            "或說需要 **全部** 船舶/貨盤的聯絡方式。"
        ),
        "opentonnages.contacts_fetched": "已獲取記錄 id {id} 的聯絡方式。",
        "opentonnages.contacts_need_id": "請提供列表中的記錄 id，或說明需要全部聯絡方式。",
        "opentonnages.no_results_vessel": "未找到符合條件的公開船盤。",
        "opentonnages.no_results_cargo": "未找到符合條件的公開貨盤。",
        "opentonnages.api_error": "公開船貨盤介面請求失敗：{detail}",
        "opentonnages.contact_api_error": "獲取聯絡方式失敗：{detail}",
        "route.redirect_schedule": "班輪船期請使用 **hifleet-schedule** 技能。",
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
