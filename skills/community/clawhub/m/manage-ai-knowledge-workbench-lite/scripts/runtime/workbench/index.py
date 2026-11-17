"""Atomic JSONL index persistence and content-based change detection."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from typing import Any


def record_key(record: dict[str, Any]) -> tuple[str, str]:
    return str(record["source_id"]), str(record["path"])


def load_index(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict) or "source_id" not in payload or "path" not in payload:
                raise ValueError(f"Invalid index record at line {line_number}")
            records.append(payload)
    return records


def write_index(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            for record in sorted(records, key=record_key):
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def diff_records(old: list[dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, Any]:
    old_map = {record_key(record): record for record in old}
    new_map = {record_key(record): record for record in new}
    added_keys = set(new_map) - set(old_map)
    deleted_keys = set(old_map) - set(new_map)
    common = set(old_map) & set(new_map)
    modified_keys = {
        key
        for key in common
        if old_map[key].get("sha256") != new_map[key].get("sha256")
    }

    old_hashes: dict[str, list[tuple[str, str]]] = {}
    new_hashes: dict[str, list[tuple[str, str]]] = {}
    for key in deleted_keys:
        old_hashes.setdefault(str(old_map[key].get("sha256", "")), []).append(key)
    for key in added_keys:
        new_hashes.setdefault(str(new_map[key].get("sha256", "")), []).append(key)
    moved: list[dict[str, str]] = []
    for digest in sorted(set(old_hashes) & set(new_hashes)):
        if digest and len(old_hashes[digest]) == 1 and len(new_hashes[digest]) == 1:
            old_key = old_hashes[digest][0]
            new_key = new_hashes[digest][0]
            moved.append(
                {
                    "source_id": new_key[0],
                    "from": old_key[1],
                    "to": new_key[1],
                    "sha256": digest,
                }
            )
            deleted_keys.remove(old_key)
            added_keys.remove(new_key)

    def display(keys: set[tuple[str, str]]) -> list[dict[str, str]]:
        return [
            {"source_id": source_id, "path": path}
            for source_id, path in sorted(keys)
        ]

    return {
        "added": display(added_keys),
        "modified": display(modified_keys),
        "moved": moved,
        "deleted": display(deleted_keys),
        "unchanged": len(common - modified_keys),
        "changed_total": len(added_keys) + len(modified_keys) + len(moved) + len(deleted_keys),
    }

