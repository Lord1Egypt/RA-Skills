"""Reversible-by-default safety: snapshot the whole memory dir before any write,
log every change, and support `undo` back to the last snapshot."""

from __future__ import annotations

import os
import shutil
import time

WORKDIR = ".memory-doctor"
SNAP_DIR = "snapshots"
CHANGELOG = "changelog.md"


def _workdir_root(root: str) -> str:
    return os.path.join(root, WORKDIR)


def snapshot(root: str) -> str:
    """Copy every *.md (and MEMORY.md) into a timestamped snapshot. Returns its path."""
    ts = time.strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(_workdir_root(root), SNAP_DIR, ts)
    os.makedirs(dest, exist_ok=True)
    for entry in os.listdir(root):
        if entry.endswith(".md"):
            shutil.copy2(os.path.join(root, entry), os.path.join(dest, entry))
    return dest


def latest_snapshot(root: str):
    base = os.path.join(_workdir_root(root), SNAP_DIR)
    if not os.path.isdir(base):
        return None
    snaps = sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))
    return os.path.join(base, snaps[-1]) if snaps else None


def restore(root: str, snap: str) -> int:
    n = 0
    for entry in os.listdir(snap):
        shutil.copy2(os.path.join(snap, entry), os.path.join(root, entry))
        n += 1
    return n


def log_change(root: str, message: str) -> None:
    os.makedirs(_workdir_root(root), exist_ok=True)
    path = os.path.join(_workdir_root(root), CHANGELOG)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"- {time.strftime('%Y-%m-%d %H:%M:%S')}  {message}\n")
