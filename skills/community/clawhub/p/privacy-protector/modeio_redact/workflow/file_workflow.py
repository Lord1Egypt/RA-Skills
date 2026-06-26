#!/usr/bin/env python3
"""
File output and map-linkage helpers for privacy-protector modules.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

from modeio_redact.core.models import MapRef

from modeio_redact.workflow.file_types import (
    MAP_MARKER_STYLE_HASH,
    MAP_MARKER_STYLE_HTML_COMMENT,
    marker_style_for_extension,
)

MAP_MARKER_PREFIX = "privacy-protector-map-id"
LEGACY_MAP_MARKER_PREFIXES = ("modeio-redact-map-id",)
ALL_MAP_MARKER_PREFIXES = (MAP_MARKER_PREFIX, *LEGACY_MAP_MARKER_PREFIXES)
MAP_MARKER_PREFIX_PATTERN = "|".join(re.escape(prefix) for prefix in ALL_MAP_MARKER_PREFIXES)
MARKER_PATTERNS = {
    MAP_MARKER_STYLE_HTML_COMMENT: re.compile(
        rf"^\s*<!--\s*(?:{MAP_MARKER_PREFIX_PATTERN}):\s*([^\s]+)\s*-->\s*$"
    ),
    MAP_MARKER_STYLE_HASH: re.compile(
        rf"^\s*#\s*(?:{MAP_MARKER_PREFIX_PATTERN}):\s*([^\s]+)\s*$"
    ),
}


def _expand_path(path_value: str) -> Path:
    return Path(path_value).expanduser()


def _next_available_path(path: Path) -> Path:
    if not path.exists():
        return path

    index = 1
    while True:
        candidate = path.with_name(f"{path.stem}.{index}{path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def resolve_output_path(
    input_path: Optional[str],
    output_path: Optional[str],
    in_place: bool,
    output_tag: str,
) -> Optional[Path]:
    """Resolve output file path for text/file workflows."""
    if in_place:
        if output_path:
            raise ValueError("--in-place cannot be used together with --output.")
        if not input_path:
            raise ValueError("--in-place requires file-path input.")
        return _expand_path(input_path)

    if output_path:
        resolved = _expand_path(output_path)
        parent = resolved.parent
        if not parent.exists() or not parent.is_dir():
            raise ValueError(f"Output directory does not exist: {parent}")
        return resolved

    if not input_path:
        return None

    source = _expand_path(input_path)
    candidate = source.with_name(f"{source.stem}.{output_tag}{source.suffix}")
    return _next_available_path(candidate)


def write_output_file(path: Path, content: str) -> None:
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise ValueError(f"Output directory does not exist: {parent}")
    path.write_text(content, encoding="utf-8")


def _match_map_marker(line: str) -> Optional[str]:
    for pattern in MARKER_PATTERNS.values():
        marker_match = pattern.match(line)
        if marker_match:
            return marker_match.group(1)
    return None


def extract_embedded_map_id(content: str) -> Optional[str]:
    """Extract embedded map id from the first few lines."""
    lines = content.splitlines()
    for line in lines[:5]:
        map_id = _match_map_marker(line)
        if map_id:
            return map_id
    return None


def strip_embedded_map_marker(content: str) -> str:
    """Strip top map marker line if present."""
    lines = content.splitlines(keepends=True)
    if not lines:
        return content

    first = lines[0].strip()
    if _match_map_marker(first):
        return "".join(lines[1:])
    return content


def embed_map_marker(content: str, map_id: str, suffix: str) -> str:
    """Embed map id marker when output file type supports inline markers."""
    clean_content = strip_embedded_map_marker(content)
    marker_style = marker_style_for_extension(suffix)
    if marker_style == MAP_MARKER_STYLE_HTML_COMMENT:
        marker = f"<!-- {MAP_MARKER_PREFIX}: {map_id} -->"
        return f"{marker}\n{clean_content}"
    if marker_style == MAP_MARKER_STYLE_HASH:
        marker = f"# {MAP_MARKER_PREFIX}: {map_id}"
        return f"{marker}\n{clean_content}"
    return clean_content


def sidecar_map_path_for(content_path: Path) -> Path:
    return content_path.with_suffix(".map.json")


def _coerce_map_ref(map_ref: Union[MapRef, Dict[str, Any]]) -> MapRef:
    if isinstance(map_ref, MapRef):
        return map_ref
    if isinstance(map_ref, dict):
        return MapRef.from_dict(map_ref)
    raise ValueError("map_ref must be MapRef or mapRef-like dict")


def write_sidecar_map(content_path: Path, map_ref: Union[MapRef, Dict[str, Any]]) -> Path:
    normalized_ref = _coerce_map_ref(map_ref)
    sidecar_path = sidecar_map_path_for(content_path)
    payload = {
        "schemaVersion": "1",
        **normalized_ref.to_dict(),
    }
    sidecar_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return sidecar_path


def read_sidecar_map_reference(content_path: Path) -> Tuple[Optional[str], Optional[Path]]:
    sidecar_path = sidecar_map_path_for(content_path)
    if not sidecar_path.exists() or not sidecar_path.is_file():
        return None, None

    try:
        raw = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Sidecar map file is invalid JSON: {sidecar_path}") from exc

    if not isinstance(raw, dict):
        raise ValueError(f"Sidecar map file must be an object: {sidecar_path}")

    map_path = raw.get("mapPath")
    if isinstance(map_path, str) and map_path.strip():
        return map_path.strip(), sidecar_path

    map_id = raw.get("mapId")
    if isinstance(map_id, str) and map_id.strip():
        return map_id.strip(), sidecar_path

    raise ValueError(f"Sidecar map file missing mapId/mapPath: {sidecar_path}")
