"""Bind a score plan to the exact local source assets it was read from.

Coordinate facts are only meaningful for one rendered page image.  This
module therefore records content hashes at extraction time and checks them
again before generation or rendering.  It prevents the common failure mode
where a plan made for an old page, crop, or DPI is silently reused.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


HASH_ALGORITHM = "sha256"


def resolve_local_path(raw: str, base: Path) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (base / path).resolve()


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def visual_asset_records(pages: list[dict[str, Any]], base: Path) -> list[dict[str, Any]]:
    """Return stable, absolute records for every rendered visual page."""
    records: list[dict[str, Any]] = []
    for page in sorted(pages, key=lambda item: int(item["page"])):
        raw = str(page.get("image", "")).strip()
        if not raw:
            raise ValueError(f"page {page['page']} has no image for provenance")
        image = resolve_local_path(raw, base)
        if not image.is_file():
            raise ValueError(f"page image not found for provenance: {image}")
        records.append({
            "role": "rendered_page",
            "page": int(page["page"]),
            "path": str(image),
            "sha256": file_digest(image),
            "bytes": image.stat().st_size,
        })
    return records


def structured_asset_record(path: Path) -> dict[str, Any]:
    source = path.resolve()
    if not source.is_file():
        raise ValueError(f"structured score source not found: {source}")
    return {
        "role": "structured_score",
        "path": str(source),
        "sha256": file_digest(source),
        "bytes": source.stat().st_size,
    }


def verify_source_assets(plan: dict[str, Any]) -> list[str]:
    """Return provenance failures without attempting to repair or relocate files."""
    source_type = str(plan.get("source", {}).get("type", "")).lower()
    recognition = plan.get("recognition", {})
    records = recognition.get("source_assets")
    if not isinstance(records, list) or not records:
        return ["recognition.source_assets is required; recreate the plan from the current source"]
    errors: list[str] = []
    page_numbers = {int(page.get("page", 0)) for page in plan.get("pages", []) if isinstance(page, dict)}
    seen: set[tuple[str, int | None]] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"recognition.source_assets[{index}] must be an object")
            continue
        role = str(record.get("role", ""))
        try:
            page = int(record["page"]) if role == "rendered_page" else None
        except (TypeError, ValueError, KeyError):
            errors.append(f"recognition.source_assets[{index}] has an invalid page")
            continue
        key = (role, page)
        if key in seen:
            errors.append(f"recognition.source_assets[{index}] duplicates {role} {page or ''}".strip())
            continue
        seen.add(key)
        raw_path = str(record.get("path", "")).strip()
        expected = str(record.get("sha256", "")).lower()
        if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
            errors.append(f"recognition.source_assets[{index}] has no valid SHA-256 digest")
            continue
        path = Path(raw_path)
        if not path.is_absolute() or not path.is_file():
            errors.append(f"recognition.source_assets[{index}] source asset is missing: {raw_path}")
            continue
        if int(record.get("bytes", -1)) != path.stat().st_size:
            errors.append(f"recognition.source_assets[{index}] byte length changed: {path}")
            continue
        if file_digest(path) != expected:
            errors.append(f"recognition.source_assets[{index}] content changed: {path}")
    if source_type in {"pdf", "image"}:
        recorded_pages = {page for role, page in seen if role == "rendered_page"}
        if recorded_pages != page_numbers:
            errors.append("recognition.source_assets must contain exactly one rendered_page record for every plan page")
    elif source_type == "musicxml" and ("structured_score", None) not in seen:
        errors.append("recognition.source_assets must contain the structured MusicXML/MXL source")
    return errors
