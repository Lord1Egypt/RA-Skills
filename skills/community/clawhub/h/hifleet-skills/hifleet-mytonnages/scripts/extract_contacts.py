#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从邮件原文抽取联系方式，在脱敏送模后回填到解析结果（供入库与展示）。"""

from __future__ import annotations

import re
from typing import Any

_MASKED_EMPTY = frozenset({"null", "none", "undefined", "nil", ""})


def is_masked_or_empty_contact(value: Any) -> bool:
    if value is None:
        return True
    s = str(value).strip()
    if not s or s.lower() in _MASKED_EMPTY:
        return True
    return "***" in s or "[隐私信息已移除]" in s


def _dedupe_contact_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in values:
        v = (raw or "").strip()
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def extract_contact_phones_from_text(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    label_re = re.compile(
        r"(?im)^\s*[-*]?\s*"
        r"(?:Contact Number|Contact No\.?|Tel(?:ephone)?|Phone|Mobile|Fax|电话|联系电话|手机)"
        r"\s*[:\-]\s*([+\d][\d\s\-().]{5,28})"
    )
    for m in label_re.finditer(text):
        num = re.sub(r"\s+", " ", m.group(1).strip())
        num = re.sub(r"[-\s]+$", "", num)
        if not is_masked_or_empty_contact(num):
            found.append(num)
    if not found:
        for m in re.finditer(
            r"(?:\+\d{1,3}[- ]?)?\(?\d{2,4}\)?[- ]?\d{3,4}[- ]?\d{3,4}(?:[- ]?\d{1,6})?",
            text,
        ):
            num = re.sub(r"\s+", " ", m.group(0).strip())
            if is_masked_or_empty_contact(num):
                continue
            digits = re.sub(r"\D", "", num)
            if len(digits) < 7:
                continue
            found.append(num)
    return _dedupe_contact_values(found)


def extract_contact_emails_from_text(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    label_re = re.compile(
        r"(?im)^\s*[-*]?\s*"
        r"(?:Email Address|Email|E-mail|邮箱|电子邮箱)"
        r"\s*[:\-]\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
    )
    for m in label_re.finditer(text):
        found.append(m.group(1).strip())
    if not found:
        for m in re.finditer(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
            email = m.group(0).strip()
            if not is_masked_or_empty_contact(email):
                found.append(email)
    return _dedupe_contact_values(found)


def extract_instant_messaging_from_text(text: str) -> list[str]:
    """微信 / WhatsApp / QQ 等（不含邮箱，邮箱走 extract_contact_emails）。"""
    if not text:
        return []
    found: list[str] = []
    patterns = (
        r"(?i)(微信|WeChat)\s*[:：\s]+\s*([\w.@+-]{2,50})",
        r"(?i)(WhatsApp)\s*[:：\s]+\s*([\w.@+-]{2,50})",
        r"(?i)QQ\s*[:：\s]+\s*(\d{5,12})\b",
        r"(?i)(Telegram|Skype|Line)\s*[:：\s]+\s*([\w.@+-]{2,50})",
    )
    for pat in patterns:
        for m in re.finditer(pat, text):
            label = m.group(1).strip()
            val = m.group(2).strip()
            if is_masked_or_empty_contact(val):
                continue
            found.append(f"{label}: {val}")
    return _dedupe_contact_values(found)


def merge_contacts_into_parsed(parsed: dict[str, Any], original_body: str) -> dict[str, Any]:
    """
    从【未脱敏】邮件正文抽取电话/邮箱/即时通讯，回填到每条船盘/货盘。
    仅当模型字段为空或含 *** 占位时覆盖。
    """
    if not isinstance(parsed, dict) or not original_body:
        return parsed
    phones = extract_contact_phones_from_text(original_body)
    emails = extract_contact_emails_from_text(original_body)
    ims = extract_instant_messaging_from_text(original_body)
    phone_str = ";".join(phones) if phones else ""
    im_parts = _dedupe_contact_values(emails + ims)
    im_str = ";".join(im_parts) if im_parts else ""
    if not phone_str and not im_str:
        return parsed
    data = parsed.get("data")
    if not isinstance(data, dict):
        return parsed
    for section in ("openvessels", "cargo"):
        items = data.get(section)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            if phone_str and is_masked_or_empty_contact(item.get("联系电话")):
                item["联系电话"] = phone_str
            if im_str and is_masked_or_empty_contact(item.get("即时通讯")):
                item["即时通讯"] = im_str
    return parsed
