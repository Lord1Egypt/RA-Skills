"""Bounded source scanning that never stores file bodies."""

from __future__ import annotations

import hashlib
from fnmatch import fnmatchcase
import json
import os
from pathlib import Path
import re
from collections.abc import Callable
from typing import Any

from .config import is_within, normalized
from .markdown import parse_markdown


SKIP_DIR_NAMES = {".git", ".obsidian", ".trash", "node_modules", "__pycache__"}
SENSITIVE_LEVELS = {"confidential", "restricted", "private"}
DEFAULT_MAX_FILE_BYTES = 5 * 1024 * 1024
DEFAULT_MAX_FILES = 50_000
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[^\s]{8,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


class ScanLimitExceeded(RuntimeError):
    """Raised before index replacement when the configured file budget is exceeded."""


class ScanCancelled(RuntimeError):
    """Raised before index replacement when a caller requests cancellation."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _under_generated_path(path: Path, generated_roots: list[Path]) -> bool:
    return any(is_within(root, path) for root in generated_roots)


def _matches(relative: str, pattern: str) -> bool:
    pattern = pattern.replace("\\", "/").lstrip("./")
    return fnmatchcase(relative, pattern) or (
        pattern.startswith("**/") and fnmatchcase(relative, pattern[3:])
    )


def _excluded_directory(relative: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        normalized_pattern = pattern.replace("\\", "/").lstrip("./")
        if _matches(relative, normalized_pattern):
            return True
        if normalized_pattern.endswith("/**"):
            prefix = normalized_pattern[:-3].rstrip("/")
            if relative == prefix or relative.startswith(prefix + "/"):
                return True
    return False


def _selected(relative: str, includes: list[str], excludes: list[str]) -> bool:
    included = not includes or any(_matches(relative, pattern) for pattern in includes)
    excluded = any(_matches(relative, pattern) for pattern in excludes)
    return included and not excluded


def _contains_secret_pattern(record: dict[str, Any]) -> bool:
    # Inspect every metadata field that can reach a derived view or a future
    # semantic envelope. File bodies are deliberately absent from ``record``.
    material = json.dumps(record, ensure_ascii=False, sort_keys=True, default=str)
    return any(pattern.search(material) for pattern in SECRET_PATTERNS)


def scan_config(
    config: dict[str, Any],
    max_file_bytes: int | None = None,
    *,
    max_files: int | None = None,
    cancel_check: Callable[[], bool] | None = None,
) -> list[dict[str, Any]]:
    paths = config["paths"]
    scan_settings = config.get("scan", {}) if isinstance(config.get("scan"), dict) else {}
    max_file_bytes = int(
        scan_settings.get("max_file_bytes", DEFAULT_MAX_FILE_BYTES)
        if max_file_bytes is None
        else max_file_bytes
    )
    max_files = int(scan_settings.get("max_files", DEFAULT_MAX_FILES) if max_files is None else max_files)
    if max_file_bytes < 1 or max_files < 1:
        raise ValueError("Scan limits must be positive integers.")
    generated_roots = [normalized(paths[key]) for key in ("internal", "knowledge", "dashboard")]
    content_access = str(config.get("content_access", "local-parse"))
    records: list[dict[str, Any]] = []

    for source in config["sources"]:
        source_id = str(source["id"])
        source_sensitivity = str(source.get("sensitivity", "internal")).lower()
        includes = [str(value) for value in source.get("include", ["**/*"])]
        excludes = [str(value) for value in source.get("exclude", [])]
        root = normalized(source["root"])
        if not root.is_dir():
            continue
        for current_text, dirnames, filenames in os.walk(root, followlinks=False):
            current = Path(current_text)
            kept_dirs: list[str] = []
            for name in dirnames:
                candidate = current / name
                try:
                    relative_dir = candidate.relative_to(root).as_posix()
                    resolved_dir = candidate.resolve(strict=True)
                except (OSError, ValueError):
                    continue
                if (
                    name.startswith(".")
                    or name in SKIP_DIR_NAMES
                    or candidate.is_symlink()
                    or not is_within(root, resolved_dir)
                    or _under_generated_path(candidate, generated_roots)
                    or _excluded_directory(relative_dir, excludes)
                ):
                    continue
                kept_dirs.append(name)
            dirnames[:] = kept_dirs
            for filename in sorted(filenames):
                if cancel_check is not None and cancel_check():
                    raise ScanCancelled("Source scan was cancelled before the index was replaced.")
                if filename.startswith("."):
                    continue
                path = current / filename
                if path.is_symlink() or not path.is_file() or _under_generated_path(path, generated_roots):
                    continue
                try:
                    relative = path.relative_to(root).as_posix()
                    resolved = path.resolve(strict=True)
                    if not is_within(root, resolved) or not _selected(relative, includes, excludes):
                        continue
                    if len(records) >= max_files:
                        raise ScanLimitExceeded(
                            f"Source scan exceeded the configured maximum of {max_files} files."
                        )
                    stat = path.stat()
                    digest = file_sha256(path)
                except (OSError, ValueError):
                    continue
                suffix = path.suffix.lower()
                record: dict[str, Any] = {
                    "source_id": source_id,
                    "path": relative,
                    "name": path.name,
                    "extension": suffix,
                    "kind": "markdown" if suffix == ".md" else "file",
                    "size": stat.st_size,
                    "mtime_ns": stat.st_mtime_ns,
                    "sha256": digest,
                    "title": path.stem,
                    "properties": {},
                    "tags": [],
                    "links": [],
                    "progress": None,
                    "parse_skipped": False,
                }
                if suffix == ".md":
                    if stat.st_size <= max_file_bytes:
                        record.update(parse_markdown(path, content_access=content_access))
                    else:
                        record["parse_skipped"] = True
                sensitivity = str(record["properties"].get("sensitivity", "")).lower()
                if record["kind"] != "markdown" and not sensitivity:
                    sensitivity = source_sensitivity
                record["sensitivity"] = sensitivity
                secret_pattern_detected = _contains_secret_pattern(record)
                record["secret_pattern_detected"] = secret_pattern_detected
                record["sensitive"] = sensitivity in SENSITIVE_LEVELS or not sensitivity or secret_pattern_detected
                records.append(record)
    return sorted(records, key=lambda row: (row["source_id"], row["path"].casefold()))
