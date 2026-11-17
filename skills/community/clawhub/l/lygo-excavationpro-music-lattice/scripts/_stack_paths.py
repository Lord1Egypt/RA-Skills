#!/usr/bin/env python3
"""Resolve LYGO_STACK_ROOT for optional stack CLI."""
from __future__ import annotations

import os
from pathlib import Path


def resolve_stack_root() -> Path:
    raw = (os.environ.get("LYGO_STACK_ROOT") or "").strip()
    if not raw:
        raise SystemExit("LYGO_STACK_ROOT not set")
    root = Path(raw).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")
    # light trust markers
    markers = [
        root / "tools" / "build_public_music_stream.py",
        root / "data" / "music_catalog",
        root / "docs",
    ]
    if not any(m.exists() for m in markers):
        raise SystemExit(f"does not look like lygo-protocol-stack: {root}")
    return root
