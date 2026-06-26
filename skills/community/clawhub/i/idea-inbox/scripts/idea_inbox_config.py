#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(os.environ.get("IDEA_INBOX_CONFIG", str(Path.home() / ".openclaw" / "idea-inbox" / "config.json")))


def _deep_merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    out = dict(a)
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


DEFAULT_CONFIG: dict[str, Any] = {
    "prefixes": ["idea:", "灵感："],
    "daily_time": "10:02",
    "bitable": {
        "app_name": "灵感妙计",
        "app_token": None,
        "table_id": None,
        "fields": {
            "content": "内容",
            "ai_summary": "AI归纳",
            "category": "类别",
            "tags": "标签",
            "status": "状态",
            "source": "来源",
            "created_time": "创建时间",
            "note": "备注",
        },
    },
    "ai": {"enabled": True, "fallback_mode": "rules"},
    "model": {
        # codex_files_first: prefer ~/.codex/auth.json + ~/.codex/config.toml
        "mode": "codex_files_first",
        # optional fallback:
        # {"baseUrl": "...", "apiKey": "...", "api": "openai-responses"|"openai-completions", "model": "...", "authHeader": true, "headers": {}}
        "fallback": None,
    },
    "tags": {"auto_add": True, "max_tags": 5},
    "status": {"options": ["待处理", "已处理", "无法处理"], "default": "待处理"},
}


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return json.loads(json.dumps(DEFAULT_CONFIG))
    try:
        raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return json.loads(json.dumps(DEFAULT_CONFIG))
        return _deep_merge(DEFAULT_CONFIG, raw)
    except Exception:
        return json.loads(json.dumps(DEFAULT_CONFIG))


def save_config(cfg: dict[str, Any]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
