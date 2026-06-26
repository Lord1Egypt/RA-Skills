#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import platform
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

ZSH = "/bin/zsh"


def run(cmd: List[str], timeout: int = 15) -> str:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except Exception as e:
        return f"ERROR: {e}"
    return (p.stdout or p.stderr or "").strip()


def run_shell(cmd: str, timeout: int = 20) -> str:
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, executable=ZSH)
    except Exception as e:
        return f"ERROR: {e}"
    return (p.stdout or p.stderr or "").strip()


def json_dump(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def bytes_human(value: Optional[float]) -> Optional[str]:
    if value is None:
        return None
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    n = float(value)
    idx = 0
    while abs(n) >= 1024 and idx < len(units) - 1:
        n /= 1024.0
        idx += 1
    return f"{n:.1f}{units[idx]}"


def parse_size_to_bytes(value: str) -> Optional[int]:
    text = value.strip()
    match = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*([KMGTP]?)(?:i?B?)?$", text, re.IGNORECASE)
    if not match:
        return None
    amount = float(match.group(1))
    unit = match.group(2).upper()
    scale = {"": 0, "K": 1, "M": 2, "G": 3, "T": 4, "P": 5}[unit]
    return int(amount * (1024 ** scale))


def now_iso() -> str:
    return run(["date", "+%Y-%m-%dT%H:%M:%S%z"])


def machine_meta() -> Dict[str, Any]:
    return {
        "hostname": platform.node(),
        "machine": platform.machine(),
        "macos_version": platform.mac_ver()[0],
        "timestamp": now_iso(),
    }


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def clamp_percent(value: Optional[float]) -> Optional[float]:
    if value is None or math.isnan(value):
        return None
    return max(0.0, min(100.0, value))
