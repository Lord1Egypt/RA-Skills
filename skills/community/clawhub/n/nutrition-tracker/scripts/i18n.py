#!/usr/bin/env python3
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def load(lang: str):
    # normalize
    lang = (lang or os.environ.get("NUTRITION_LANG") or "zh-CN").strip()
    if lang.lower().startswith("zh"):
        lang = "zh-CN"
    elif lang.lower().startswith("en"):
        lang = "en-US"
    p = BASE / "locales" / f"{lang}.json"
    if not p.exists():
        p = BASE / "locales" / "zh-CN.json"
    return json.loads(p.read_text(encoding="utf-8"))


def t(lang: str, key: str, **kwargs):
    data = load(lang)
    s = data.get(key, key)
    for k, v in kwargs.items():
        s = s.replace("{" + k + "}", str(v))
    return s
