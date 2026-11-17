"""Content-addressed cache helpers for insurance product packages."""

from __future__ import annotations

import hashlib
from pathlib import Path

SCHEMA_VERSION = "1.0.0"
TOOL_VERSION = "1.0.0"
CACHE_DIRNAME = ".product-cache"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_files(product_dir: Path) -> list[Path]:
    product_dir = Path(product_dir).resolve()
    return sorted(
        path
        for path in product_dir.rglob("*")
        if path.is_file()
        and CACHE_DIRNAME not in path.relative_to(product_dir).parts
        and path.name not in {".DS_Store", "Thumbs.db"}
    )


def build_cache_manifest(
    product_dir: Path,
    *,
    tool_version: str = TOOL_VERSION,
    schema_version: str = SCHEMA_VERSION,
) -> dict:
    product_dir = Path(product_dir).resolve()
    files = {}
    for path in source_files(product_dir):
        relative = path.relative_to(product_dir).as_posix()
        stat = path.stat()
        files[relative] = {
            "sha256": sha256_file(path),
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }
    return {
        "schema_version": schema_version,
        "tool_version": tool_version,
        "product_dir": str(product_dir),
        "files": files,
    }


def compare_manifest(old: dict | None, new: dict) -> dict:
    old = old or {}
    old_files = old.get("files", {})
    new_files = new.get("files", {})
    full_rebuild = (
        old.get("schema_version") != new.get("schema_version")
        or old.get("tool_version") != new.get("tool_version")
    )
    if full_rebuild:
        changed = sorted(new_files)
        unchanged: list[str] = []
    else:
        changed = sorted(
            name for name, metadata in new_files.items()
            if old_files.get(name, {}).get("sha256") != metadata.get("sha256")
        )
        unchanged = sorted(set(new_files) - set(changed))
    removed = sorted(set(old_files) - set(new_files))
    result = {
        "changed": changed,
        "unchanged": unchanged,
        "removed": removed,
    }
    if full_rebuild:
        result["full_rebuild"] = True
    return result
