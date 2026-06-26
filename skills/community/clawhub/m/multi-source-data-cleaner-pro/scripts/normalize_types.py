"""Normalize common Chinese/English data types."""
from __future__ import annotations
import re
from datetime import datetime
from typing import Any

DATE_FORMATS = [
    "%Y-%m-%d","%Y/%m/%d","%Y.%m.%d","%Y年%m月%d日",
    "%d-%m-%Y","%d/%m/%Y","%m/%d/%Y","%Y%m%d",
]
TRUE_TOKENS = {"y","yes","true","t","1","是","对","✓"}
FALSE_TOKENS = {"n","no","false","f","0","否","错","✗"}


def to_number(s: Any):
    if s is None or s == "": return None
    if isinstance(s, (int, float)): return s
    cleaned = re.sub(r"[，,\s]", "", str(s))
    cleaned = re.sub(r"[¥$￥]", "", cleaned)
    try: return float(cleaned) if "." in cleaned or "e" in cleaned.lower() else int(cleaned)
    except ValueError: return None


def to_bool(s: Any):
    if isinstance(s, bool): return s
    if s is None: return None
    t = str(s).strip().lower()
    if t in TRUE_TOKENS: return True
    if t in FALSE_TOKENS: return False
    return None


def to_iso_date(s: Any):
    if s is None or s == "": return None
    raw = str(s).strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(raw, f).date().isoformat()
        except ValueError:
            continue
    return None


def to_phone(s: Any):
    if s is None: return None
    digits = re.sub(r"\D", "", str(s))
    if len(digits) == 11 and digits.startswith("1"):
        return "+86" + digits
    if len(digits) == 13 and digits.startswith("86"):
        return "+" + digits
    return digits or None


def mask_pii(value: str, kind: str) -> str:
    if value is None: return value
    s = str(value)
    if kind == "name":
        if len(s) <= 1: return s
        return s[0] + "*" * (len(s) - 1)
    if kind == "phone":
        d = re.sub(r"\D", "", s)
        if len(d) >= 7: return d[:3] + "****" + d[-4:]
        return s
    if kind == "id":
        if len(s) >= 8: return s[:4] + "*" * (len(s) - 8) + s[-4:]
        return s
    return s
