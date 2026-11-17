#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_path(path: Path) -> str:
    path = path.expanduser().resolve()
    if path.is_file():
        return sha256_file(path)
    if not path.is_dir():
        raise FileNotFoundError(path)
    digest = hashlib.sha256()
    for child in sorted(p for p in path.rglob("*") if p.is_file() and not p.is_symlink()):
        digest.update(str(child.relative_to(path)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(child).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def path_record(raw_path: str) -> dict[str, Any]:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    stat = path.stat()
    return {
        "path": str(path),
        "kind": "directory" if path.is_dir() else "file",
        "sha256": sha256_path(path),
        "size_bytes": stat.st_size if path.is_file() else None,
        "mtime_ns": stat.st_mtime_ns,
    }


def load_manifest(path: str | Path) -> tuple[Path, dict[str, Any]]:
    manifest_path = Path(path).expanduser().resolve()
    with manifest_path.open("r", encoding="utf-8") as handle:
        return manifest_path, json.load(handle)


def save_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temp_name, target)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
