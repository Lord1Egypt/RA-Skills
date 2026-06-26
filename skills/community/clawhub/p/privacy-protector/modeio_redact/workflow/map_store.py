#!/usr/bin/env python3
"""
Local mapping storage utilities for privacy-protector modules.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from modeio_redact.core.models import MappingEntry, MapRecord, MapRef

MAP_DIR_ENV = "MODEIO_REDACT_MAP_DIR"
DEFAULT_MAP_DIR = Path.home() / ".modeio" / "redact" / "maps"
SCHEMA_VERSION = "1"
MAP_FILE_SUFFIX = ".json"
MAP_TTL_DAYS = 7


class MapStoreError(RuntimeError):
    pass


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hash_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _safe_chmod(path: Path, mode: int) -> None:
    try:
        os.chmod(path, mode)
    except OSError:
        return


def get_map_dir() -> Path:
    override = os.environ.get(MAP_DIR_ENV, "").strip()
    map_dir = Path(override).expanduser() if override else DEFAULT_MAP_DIR
    map_dir.mkdir(parents=True, exist_ok=True)
    _safe_chmod(map_dir, 0o700)
    return map_dir


# ---------------------------------------------------------------------------
# Entry normalization
# ---------------------------------------------------------------------------


def normalize_mapping_entries(data: Dict[str, Any]) -> List[MappingEntry]:
    entries: List[MappingEntry] = []
    seen_placeholders: set = set()

    def _collect(items: Any) -> None:
        if not isinstance(items, list):
            return
        for item in items:
            entry = MappingEntry.from_raw(item)
            if entry is None:
                continue
            if entry.placeholder == entry.original:
                continue
            if entry.placeholder in seen_placeholders:
                continue
            seen_placeholders.add(entry.placeholder)
            entries.append(entry)

    local_detection = data.get("localDetection")
    if isinstance(local_detection, dict):
        _collect(local_detection.get("items"))

    _collect(data.get("mapping"))
    return entries


def _coerce_entries(entries: Sequence[Any]) -> List[MappingEntry]:
    normalized: List[MappingEntry] = []
    for item in entries:
        if isinstance(item, MappingEntry):
            normalized.append(item)
            continue
        if isinstance(item, dict):
            entry = MappingEntry.from_raw(item)
            if entry is not None:
                normalized.append(entry)
    return normalized


def _prune_old_maps(map_dir: Path) -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAP_TTL_DAYS)
    cutoff_timestamp = cutoff.timestamp()
    for candidate in map_dir.glob(f"*{MAP_FILE_SUFFIX}"):
        try:
            if candidate.stat().st_mtime < cutoff_timestamp:
                candidate.unlink()
        except OSError:
            continue


def _new_map_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rand = uuid.uuid4().hex[:8]
    return f"{ts}-{rand}"


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------


def save_map(
    raw_input: str,
    anonymized_content: str,
    entries: Sequence[Any],
    level: str,
    source_mode: str,
) -> MapRef:
    normalized_entries = _coerce_entries(entries)
    if not normalized_entries:
        raise MapStoreError("cannot save map: no mapping entries found")

    map_dir = get_map_dir()
    _prune_old_maps(map_dir)

    map_id = _new_map_id()
    path = map_dir / f"{map_id}{MAP_FILE_SUFFIX}"

    record = MapRecord(
        schema_version=SCHEMA_VERSION,
        map_id=map_id,
        created_at=_utc_now_iso(),
        level=level,
        source_mode=source_mode,
        input_hash=hash_text(raw_input),
        anonymized_hash=hash_text(anonymized_content),
        entries=normalized_entries,
    )

    temp_name = None
    try:
        fd, temp_name = tempfile.mkstemp(prefix=f"{map_id}-", suffix=".tmp", dir=str(map_dir))
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(record.to_dict(), handle, ensure_ascii=False, indent=2)
        temp_path = Path(temp_name)
        _safe_chmod(temp_path, 0o600)
        os.replace(temp_path, path)
        _safe_chmod(path, 0o600)
    except OSError as exc:
        if temp_name:
            try:
                Path(temp_name).unlink()
            except OSError:
                pass
        raise MapStoreError(f"failed to persist local map file: {exc}") from exc

    return record.to_ref(str(path))


def _resolve_map_path(map_ref: Optional[str]) -> Path:
    map_dir = get_map_dir()

    if map_ref:
        direct_path = Path(map_ref).expanduser()
        if direct_path.is_file():
            return direct_path

        ref = map_ref.strip()
        if ref.endswith(MAP_FILE_SUFFIX):
            ref = ref[: -len(MAP_FILE_SUFFIX)]
        id_path = map_dir / f"{ref}{MAP_FILE_SUFFIX}"
        if id_path.is_file():
            return id_path
        raise MapStoreError(f"mapping file not found for reference: {map_ref}")

    candidates = [p for p in map_dir.glob(f"*{MAP_FILE_SUFFIX}") if p.is_file()]
    if not candidates:
        raise MapStoreError("no local map files found; run anonymize first")

    candidates.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return candidates[0]


def _validate_record(raw: Dict[str, Any], fallback_map_id: str) -> MapRecord:
    entries_raw = raw.get("entries")
    if not isinstance(entries_raw, list):
        raise MapStoreError("invalid map file: missing entries array")

    entries: List[MappingEntry] = []
    for item in entries_raw:
        entry = MappingEntry.from_raw(item)
        if entry is not None:
            entries.append(entry)

    if not entries:
        raise MapStoreError("invalid map file: entries are empty or malformed")

    map_id = raw.get("mapId")
    if not isinstance(map_id, str) or not map_id.strip():
        map_id = fallback_map_id

    return MapRecord(
        schema_version=str(raw.get("schemaVersion") or SCHEMA_VERSION),
        map_id=map_id,
        created_at=str(raw.get("createdAt") or ""),
        level=str(raw.get("level") or ""),
        source_mode=str(raw.get("sourceMode") or ""),
        input_hash=str(raw.get("inputHash") or ""),
        anonymized_hash=str(raw.get("anonymizedHash") or ""),
        entries=entries,
    )


def load_map(map_ref: Optional[str]) -> Tuple[MapRecord, Path]:
    path = _resolve_map_path(map_ref)
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except OSError as exc:
        raise MapStoreError(f"failed to read map file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise MapStoreError(f"map file is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise MapStoreError("invalid map file: root must be an object")

    record = _validate_record(raw, fallback_map_id=path.stem)
    return record, path


def update_anonymized_hash(map_ref: str, anonymized_content: str) -> MapRecord:
    path = _resolve_map_path(map_ref)
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except OSError as exc:
        raise MapStoreError(f"failed to read map file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise MapStoreError(f"map file is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise MapStoreError("invalid map file: root must be an object")

    raw["anonymizedHash"] = hash_text(anonymized_content)

    temp_name = None
    try:
        fd, temp_name = tempfile.mkstemp(prefix=f"{path.stem}-", suffix=".tmp", dir=str(path.parent))
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(raw, handle, ensure_ascii=False, indent=2)
        temp_path = Path(temp_name)
        _safe_chmod(temp_path, 0o600)
        os.replace(temp_path, path)
        _safe_chmod(path, 0o600)
    except OSError as exc:
        if temp_name:
            try:
                Path(temp_name).unlink()
            except OSError:
                pass
        raise MapStoreError(f"failed to persist local map file: {exc}") from exc

    return _validate_record(raw, fallback_map_id=path.stem)
