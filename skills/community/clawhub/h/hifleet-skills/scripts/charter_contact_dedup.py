#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deduplicate unlock contact rows: same email+phone+IM → one row, keep latest date."""

from __future__ import annotations

import re
from copy import deepcopy
from datetime import datetime
from typing import Any, Optional

_EMAIL_KEYS = ("email", "mail", "contactEmail", "contact_email", "邮箱")
_PHONE_KEYS = (
    "phone",
    "tel",
    "mobile",
    "telephone",
    "contactPhone",
    "contact_phone",
    "phoneNumber",
    "电话",
    "手机",
    "联系电话",
)
_IM_KEYS = (
    "wechat",
    "whatsapp",
    "qq",
    "telegram",
    "skype",
    "im",
    "instantMessaging",
    "instant_messaging",
    "contactIm",
    "微信",
    "即时通讯",
)
_DATE_KEYS = (
    "updatetime",
    "updateTime",
    "update_time",
    "date",
    "createTime",
    "create_time",
    "time",
    "sendTime",
    "send_time",
    "更新时间",
    "日期",
)
_LIST_KEYS = ("senderInfoList", "contacts", "contactList", "list", "rows", "data")


def _norm(value: Any) -> str:
    if value is None:
        return ""
    s = str(value).strip().lower()
    s = re.sub(r"\s+", "", s)
    return s


def _first_field(record: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        if key in record and record[key] not in (None, ""):
            v = record[key]
            if isinstance(v, (list, dict)):
                continue
            return str(v).strip()
    return ""


def _contact_triple(record: dict[str, Any]) -> tuple[str, str, str]:
    return (
        _norm(_first_field(record, _EMAIL_KEYS)),
        _norm(_first_field(record, _PHONE_KEYS)),
        _norm(_first_field(record, _IM_KEYS)),
    )


def _parse_date_value(record: dict[str, Any]) -> float:
    for key in _DATE_KEYS:
        raw = record.get(key)
        if raw in (None, ""):
            continue
        if isinstance(raw, (int, float)):
            ts = float(raw)
            if ts > 1e12:
                ts /= 1000.0
            return ts
        s = str(raw).strip()
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d",
        ):
            try:
                return datetime.strptime(s[:19], fmt).timestamp()
            except ValueError:
                continue
    return 0.0


def _looks_like_contact(record: dict[str, Any]) -> bool:
    if not isinstance(record, dict):
        return False
    email, phone, im = _contact_triple(record)
    return bool(email or phone or im)


def _collect_contact_dicts(node: Any, out: list[dict[str, Any]]) -> None:
    if isinstance(node, dict):
        if _looks_like_contact(node):
            out.append(node)
        for v in node.values():
            if isinstance(v, (dict, list)):
                _collect_contact_dicts(v, out)
    elif isinstance(node, list):
        for item in node:
            _collect_contact_dicts(item, out)


def dedupe_contact_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge rows with identical email+phone+IM; keep the row with the latest date."""
    buckets: dict[tuple[str, str, str], list[tuple[float, dict[str, Any]]]] = {}
    for rec in records:
        if not _looks_like_contact(rec):
            continue
        key = _contact_triple(rec)
        if not any(key):
            continue
        buckets.setdefault(key, []).append((_parse_date_value(rec), rec))

    merged: list[dict[str, Any]] = []
    for items in buckets.values():
        items.sort(key=lambda x: x[0], reverse=True)
        merged.append(deepcopy(items[0][1]))
    return merged


def dedupe_unlock_payload(payload: Any) -> dict[str, Any]:
    """
    Extract contact-like dicts from unlock JSON, dedupe, return summary.
    Raw payload is preserved; use contacts_deduped for display.
    """
    if not isinstance(payload, dict):
        return {"contacts_raw": payload, "contacts_deduped": [], "deduped_count": 0}

    collected: list[dict[str, Any]] = []
    for key in _LIST_KEYS:
        inner = payload.get(key)
        if isinstance(inner, list):
            for item in inner:
                if isinstance(item, dict) and _looks_like_contact(item):
                    collected.append(item)
    if not collected:
        _collect_contact_dicts(payload, collected)

    deduped = dedupe_contact_records(collected)
    return {
        "contacts_raw": payload,
        "contacts_deduped": deduped,
        "deduped_count": len(deduped),
        "original_contact_count": len(collected),
    }
