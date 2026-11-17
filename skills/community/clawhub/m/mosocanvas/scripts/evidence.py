#!/usr/bin/env python3
"""Shared content-addressed evidence helpers for MoSoCanvas validators."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


class EvidenceError(ValueError):
    """Raised when evidence cannot be resolved or verified."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_object(path: Path, label: str = "JSON") -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"{label} cannot be loaded: {exc}") from exc
    if not isinstance(value, dict):
        raise EvidenceError(f"{label} must be a JSON object")
    return value


def load_registry(path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    registry = load_object(path, "evidence registry")
    if registry.get("schema") != "moso.evidence-registry/0.1":
        raise EvidenceError("evidence registry must use moso.evidence-registry/0.1")
    entries = registry.get("entries")
    if not isinstance(entries, list):
        raise EvidenceError("evidence registry entries must be a list")
    indexed: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict) or not entry.get("id"):
            raise EvidenceError(f"evidence entry {index} requires an id")
        entry_id = str(entry["id"])
        if entry_id in indexed:
            raise EvidenceError(f"duplicate evidence id: {entry_id}")
        indexed[entry_id] = entry
    return registry, indexed


def verify_entry(
    entry: dict[str, Any],
    registry_path: Path,
    allowed_kinds: Iterable[str] | None = None,
) -> Path:
    entry_id = str(entry.get("id", "<unknown>"))
    if allowed_kinds is not None and entry.get("kind") not in set(allowed_kinds):
        raise EvidenceError(
            f"evidence {entry_id} has kind {entry.get('kind')!r}, "
            f"expected one of {sorted(set(allowed_kinds))}"
        )
    content_ref = entry.get("content_ref")
    if not isinstance(content_ref, str) or not content_ref:
        raise EvidenceError(f"evidence {entry_id} requires content_ref")
    path = Path(content_ref).expanduser()
    if not path.is_absolute():
        path = (registry_path.resolve().parent / path).resolve()
    if not path.is_file():
        raise EvidenceError(f"evidence {entry_id} content does not exist: {path}")
    expected_size = entry.get("size_bytes")
    actual_size = path.stat().st_size
    if expected_size != actual_size:
        raise EvidenceError(
            f"evidence {entry_id} size mismatch: {actual_size}!={expected_size}"
        )
    expected_hash = str(entry.get("sha256", "")).lower()
    if len(expected_hash) != 64 or sha256_file(path).lower() != expected_hash:
        raise EvidenceError(f"evidence {entry_id} sha256 mismatch")
    return path


def require_evidence(
    evidence_id: str,
    indexed: dict[str, dict[str, Any]],
    registry_path: Path,
    allowed_kinds: Iterable[str] | None = None,
) -> tuple[dict[str, Any], Path]:
    if evidence_id not in indexed:
        raise EvidenceError(f"unregistered evidence id: {evidence_id}")
    entry = indexed[evidence_id]
    return entry, verify_entry(entry, registry_path, allowed_kinds)


def verify_registry(path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    registry, indexed = load_registry(path)
    for entry in indexed.values():
        verify_entry(entry, path)
    return registry, indexed
