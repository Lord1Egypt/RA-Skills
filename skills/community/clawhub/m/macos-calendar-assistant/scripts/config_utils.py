#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from zoneinfo import ZoneInfo


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def config_path() -> Path:
    return skill_root() / "config.json"


def load_config() -> dict:
    p = config_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def _system_timezone() -> str | None:
    """Detect macOS system timezone via systemsetup."""
    try:
        out = subprocess.check_output(
            ["/usr/sbin/systemsetup", "-gettimezone"],
            text=True, timeout=5, stderr=subprocess.DEVNULL,
        )
        # Output: "Time Zone: Asia/Shanghai"
        tz = out.strip().split(":", 1)[-1].strip()
        ZoneInfo(tz)  # validate
        return tz
    except Exception:
        return None


def get_timezone_name(default: str = "Asia/Shanghai") -> str:
    cfg = load_config()
    tz = cfg.get("timezone")
    if tz:
        return str(tz)
    # No timezone in config → try system timezone, then fall back to default
    return _system_timezone() or default


def get_zoneinfo(default: str = "Asia/Shanghai") -> ZoneInfo:
    try:
        return ZoneInfo(get_timezone_name(default))
    except Exception:
        return ZoneInfo(default)
