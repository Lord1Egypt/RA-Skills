#!/usr/bin/env python3
"""Shared, agent-agnostic runtime paths and optional environment loading."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Sequence

APP_NAME = "ninebot-show-skill"
CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")).expanduser()
DATA_HOME = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")).expanduser()
CONFIG_DIR = CONFIG_HOME / APP_NAME
DEFAULT_CONFIG = CONFIG_DIR / "config.json"
DEFAULT_OUTPUT_DIR = DATA_HOME / APP_NAME


def config_path() -> Path:
    """Return config path; old env name remains supported for compatibility."""
    raw = os.environ.get("NINEBOT_SHOW_CONFIG") or os.environ.get("NINEBOT_REPORT_CONFIG")
    return Path(raw).expanduser() if raw else DEFAULT_CONFIG


def output_dir() -> Path:
    raw = os.environ.get("NINEBOT_OUTPUT_DIR")
    return Path(raw).expanduser() if raw else DEFAULT_OUTPUT_DIR


def env_value(names: Iterable[str]) -> str:
    """Read selected keys from process env, then an optional skill-local env file.

    This intentionally never reads arbitrary Agent credential stores. The fallback
    file is ~/.config/ninebot-show-skill/.env, or NINEBOT_ENV_FILE when set.
    """
    names = tuple(names)
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value

    explicit = os.environ.get("NINEBOT_ENV_FILE", "").strip()
    candidates = [Path(explicit).expanduser()] if explicit else [CONFIG_DIR / ".env"]
    for env_file in candidates:
        try:
            lines = env_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        values: dict[str, str] = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key in names:
                values[key] = value.strip().strip('"').strip("'")
        for name in names:
            if values.get(name):
                return values[name]
    return ""


READ_ONLY_NINECLI_COMMANDS = frozenset({"status", "battery", "travel", "whoami", "vehicles"})

def ninecli_path(skill_dir: Path) -> Path:
    """Resolve ninecli and reject non-files/non-executable overrides."""
    raw = os.environ.get("NINECLI_BIN", "").strip()
    candidate = Path(raw).expanduser() if raw else (skill_dir / ".venv" / "bin" / "ninecli")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError(f"ninecli 不存在: {candidate}") from exc
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise RuntimeError(f"ninecli 不是可执行文件: {resolved}")
    return resolved

def ninecli_argv(skill_dir: Path, subcommand: str, *args: object) -> list[str]:
    """Build a ninecli argv, hard-blocking vehicle-control/write subcommands."""
    if subcommand not in READ_ONLY_NINECLI_COMMANDS:
        raise RuntimeError(f"拒绝非只读 ninecli 子命令: {subcommand}")
    return [str(ninecli_path(skill_dir)), subcommand, *(str(x) for x in args)]

def district_safe_gcj02(lat: float, lon: float) -> tuple[float, float]:
    """Reduce third-party precision for district-only reverse geocoding (~1 km scale)."""
    return round(lat, 2), round(lon, 2)
