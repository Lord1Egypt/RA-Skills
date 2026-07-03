"""Resolve LYGO stack root — no hardcoded machine paths (security)."""

from __future__ import annotations

import json
import os
from pathlib import Path

_MARKER = ("tools/verify_kernel_eggs.py", "tools/joy_loop_protocol.py")


def resolve_stack_root(*, config_path: Path | None = None) -> Path:
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        root = Path(env)
        if _valid(root):
            return root
        raise FileNotFoundError(f"LYGO_STACK_ROOT invalid (missing stack tools): {root}")
    if config_path and config_path.is_file():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            raw = (cfg.get("lygo_stack_root") or "").strip()
            if raw:
                root = Path(raw)
                if _valid(root):
                    return root
        except (json.JSONDecodeError, OSError):
            pass
    raise FileNotFoundError(
        "LYGO_STACK_ROOT unset — set environment variable to your lygo-protocol-stack clone"
    )


def _valid(root: Path) -> bool:
    return any((root / m).is_file() for m in _MARKER)


def resolve_stack_root_or_none(config_path: Path | None = None) -> Path | None:
    try:
        return resolve_stack_root(config_path=config_path)
    except FileNotFoundError:
        return None