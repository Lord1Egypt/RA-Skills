"""Ownership manifest updates for generated outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import MANIFEST_REL, PRODUCT_ID, atomic_write_json, is_within, load_json, normalized


def register_generated_files(config: dict[str, Any], files: list[Path]) -> Path:
    workspace = normalized(config["workspace"])
    internal = normalized(config["paths"]["internal"])
    manifest_path = internal / MANIFEST_REL
    manifest = load_json(manifest_path)
    if manifest.get("product") != PRODUCT_ID:
        raise ValueError("Cannot update an unrecognized ownership manifest.")
    if normalized(manifest.get("workspace", "")) != workspace:
        raise ValueError("Cannot update an ownership manifest for another workspace.")
    existing = {str(value) for value in manifest.get("generated_files", []) if isinstance(value, str)}
    for path in files:
        path = normalized(path)
        if not is_within(workspace, path):
            raise ValueError(f"Generated file escaped workspace: {path}")
        existing.add(path.relative_to(workspace).as_posix())
    manifest["generated_files"] = sorted(existing)
    atomic_write_json(manifest_path, manifest)
    return manifest_path
