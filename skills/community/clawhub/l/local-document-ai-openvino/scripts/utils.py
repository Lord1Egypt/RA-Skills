#!/usr/bin/env python3
"""
utils.py

Shared helpers for the Local Document AI with OpenVINO skill.

This module is intentionally lightweight and dependency-free.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff"}
SUPPORTED_PDF_EXTS = {".pdf"}


def now_iso() -> str:
    """Return a UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> None:
    """Create a directory if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)


def ensure_artifact_layout(out_dir: Path) -> None:
    """
    Create the standard artifact folder layout.
    Safe to call multiple times.
    """
    ensure_dir(out_dir)
    ensure_dir(out_dir / "tables")
    ensure_dir(out_dir / "figures")
    ensure_dir(out_dir / "task_output")


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    """Write pretty JSON to disk."""
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """Write UTF-8 text to disk."""
    path.write_text(content, encoding="utf-8")


def append_text(path: Path, content: str) -> None:
    """Append UTF-8 text to disk."""
    with path.open("a", encoding="utf-8") as f:
        f.write(content)


def write_error(
    out_dir: Path,
    stage: str,
    message: str,
    **extra: Any,
) -> Path:
    """
    Write a standard error.json file and return its path.
    """
    ensure_dir(out_dir)
    payload: dict[str, Any] = {
        "stage": stage,
        "message": message,
        "timestamp": now_iso(),
    }
    payload.update(extra)
    error_path = out_dir / "error.json"
    write_json(error_path, payload)
    return error_path


def slugify(text: str, default: str = "item") -> str:
    """Convert arbitrary text into a simple snake_case slug."""
    value = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return value or default


def short_text(text: str, limit: int = 80) -> str:
    """Trim text for labels/logging."""
    clean = " ".join(text.split())
    return clean if len(clean) <= limit else clean[: limit - 3] + "..."


def normalize_whitespace(value: str) -> str:
    """Collapse repeated whitespace."""
    return " ".join(value.split())


def detect_input_type(file_path: Path) -> str:
    """Return 'pdf' or 'image' based on file extension."""
    suffix = file_path.suffix.lower()
    if suffix in SUPPORTED_PDF_EXTS:
        return "pdf"
    if suffix in SUPPORTED_IMAGE_EXTS:
        return "image"
    raise ValueError(f"Unsupported file type: {suffix}")


def sha256_file(file_path: Path) -> str:
    """Compute SHA256 for a file."""
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_document_id(file_path: Path, file_hash: str) -> str:
    """Stable document run ID."""
    return f"{file_path.stem}-{file_hash[:8]}"


def make_source_ref(page_id: str | None, block_id: str | None) -> dict[str, Any]:
    """Standard source reference object."""
    return {"page_id": page_id, "block_id": block_id}


def iter_blocks(document: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Flatten blocks across pages in reading order.

    Returns:
        [
          {
            "page_id": "...",
            "page_index": 1,
            "block": {...}
          }
        ]
    """
    rows: list[dict[str, Any]] = []
    for page in document.get("pages", []):
        page_id = page.get("page_id")
        page_index = page.get("page_index")
        blocks = sorted(page.get("blocks", []), key=lambda b: b.get("reading_order", 0))
        for block in blocks:
            rows.append(
                {
                    "page_id": page_id,
                    "page_index": page_index,
                    "block": block,
                }
            )
    return rows


def count_block_types(document: dict[str, Any]) -> dict[str, int]:
    """Count block types across the document."""
    counts: dict[str, int] = {}
    for row in iter_blocks(document):
        block_type = row["block"].get("type") or "unknown"
        counts[block_type] = counts.get(block_type, 0) + 1
    return counts


def detect_title(document: dict[str, Any], override: str | None = None) -> str:
    """
    Try to derive a human-readable title from the document.
    Priority:
    1. override
    2. first heading block
    3. source filename stem
    4. document_id
    """
    if override:
        return override

    for row in iter_blocks(document):
        block = row["block"]
        if block.get("type") == "heading":
            text = (block.get("text") or "").strip()
            if text:
                return text

    source = document.get("source", {})
    filename = source.get("filename")
    if filename:
        return Path(filename).stem.replace("_", " ").replace("-", " ").title()

    document_id = document.get("document_id")
    if document_id:
        return str(document_id).replace("_", " ").replace("-", " ").title()

    return "Generated Document"


def get_default_artifact_dir(file_path: Path, base_dir: Path | None = None) -> Path:
    """
    Default artifact directory:
      ./artifacts/<document_stem>/

    If base_dir is provided, artifacts live under that folder.
    """
    root = (base_dir or Path.cwd()) / "artifacts"
    return root / slugify(file_path.stem, default="document")


def build_parse_status(document: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    """Build a standard parse summary payload."""
    return {
        "ok": True,
        "document_id": document.get("document_id"),
        "output_dir": str(output_dir),
        "page_count": len(document.get("pages", [])),
        "table_count": len(document.get("tables", [])),
        "figure_count": len(document.get("figures", [])),
        "entity_count": len(document.get("entities", [])),
        "block_type_counts": count_block_types(document),
        "parsed_json": str(output_dir / "parsed.json"),
        "parsed_md": str(output_dir / "parsed.md"),
        "warnings": document.get("parse_info", {}).get("warnings", []),
    }


def validate_document_schema(document: dict[str, Any]) -> list[str]:
    """
    Minimal schema validation.
    Returns a list of problems. Empty list means basic validation passed.
    """
    problems: list[str] = []

    required_top = ["schema_version", "document_id", "source", "parse_info", "pages", "outputs"]
    for key in required_top:
        if key not in document:
            problems.append(f"Missing top-level field: {key}")

    if "source" in document and not isinstance(document["source"], dict):
        problems.append("Field 'source' must be an object")

    if "parse_info" in document and not isinstance(document["parse_info"], dict):
        problems.append("Field 'parse_info' must be an object")

    if "pages" in document:
        if not isinstance(document["pages"], list):
            problems.append("Field 'pages' must be a list")
        elif len(document["pages"]) == 0:
            problems.append("Field 'pages' must contain at least one page")

    page_ids: set[str] = set()
    block_ids: set[str] = set()

    for page in document.get("pages", []):
        page_id = page.get("page_id")
        if not page_id:
            problems.append("A page is missing page_id")
        elif page_id in page_ids:
            problems.append(f"Duplicate page_id: {page_id}")
        else:
            page_ids.add(page_id)

        blocks = page.get("blocks", [])
        if not isinstance(blocks, list):
            problems.append(f"Page {page_id} blocks must be a list")
            continue

        last_order = -1
        for block in blocks:
            block_id = block.get("block_id")
            if not block_id:
                problems.append(f"Page {page_id} has a block without block_id")
            else:
                full_id = f"{page_id}:{block_id}"
                if full_id in block_ids:
                    problems.append(f"Duplicate block id within document: {full_id}")
                block_ids.add(full_id)

            ro = block.get("reading_order")
            if isinstance(ro, int):
                if ro < last_order:
                    problems.append(f"Reading order is not monotonic on page {page_id}")
                last_order = ro

    return problems


def parse_json_from_subprocess_output(stdout: str) -> dict[str, Any]:
    """
    Best-effort parse of JSON status from subprocess stdout.
    Uses the last non-empty line.
    """
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Subprocess produced no stdout")
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse subprocess JSON status: {exc}") from exc


def safe_relative_path(path: Path, base: Path) -> str:
    """
    Return relative path if possible, otherwise absolute path string.
    """
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def summarize_generated_files(out_dir: Path) -> list[str]:
    """
    Return a stable list of generated files under out_dir.
    """
    files: list[str] = []
    if not out_dir.exists():
        return files
    for path in sorted(p for p in out_dir.rglob("*") if p.is_file()):
        files.append(safe_relative_path(path, out_dir))
    return files
