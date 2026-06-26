#!/usr/bin/env python3
"""Asset ingestion and manifest builder for Hyperframes Video Studio."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import mimetypes
import re
import sys
import time
import zipfile
from pathlib import Path
from xml.etree import ElementTree


BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / ".cache"
MANIFEST_DIR = CACHE_DIR / "assets"

TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".csv", ".json", ".html", ".htm", ".xml"}
OFFICE_EXTENSIONS = {".docx", ".pptx", ".xlsx"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp", ".tiff"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
MAX_FILE_BYTES = 50 * 1024 * 1024
MAX_TEXT_CHARS = 12000
MAX_FILES = 300
SKIP_DIRS = {".git", "node_modules", ".cache", "__pycache__", ".venv", "venv"}


def _print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _read_json(path: Path) -> dict:
    with path.expanduser().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def _hash_file(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except Exception:
        return None


def _text_clean(value: str) -> str:
    value = re.sub(r"<script[\s\S]*?</script>", " ", value, flags=re.I)
    value = re.sub(r"<style[\s\S]*?</style>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:MAX_TEXT_CHARS]


def _read_plain_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".html", ".htm", ".xml"}:
        return _text_clean(raw)
    if path.suffix.lower() == ".csv":
        rows = []
        with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
            for index, row in enumerate(csv.reader(handle)):
                rows.append(" | ".join(cell.strip() for cell in row[:12]))
                if index >= 40:
                    break
        return "\n".join(rows)[:MAX_TEXT_CHARS]
    return raw[:MAX_TEXT_CHARS]


def _office_text(path: Path) -> str:
    parts = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            wanted = []
            suffix = path.suffix.lower()
            if suffix == ".docx":
                wanted = [name for name in names if name.startswith("word/") and name.endswith(".xml")]
            elif suffix == ".pptx":
                wanted = [name for name in names if name.startswith("ppt/slides/") and name.endswith(".xml")]
            elif suffix == ".xlsx":
                wanted = [name for name in names if name.startswith("xl/worksheets/") and name.endswith(".xml")]
                wanted += [name for name in names if name == "xl/sharedStrings.xml"]
            for name in wanted[:80]:
                xml_bytes = archive.read(name)
                try:
                    root = ElementTree.fromstring(xml_bytes)
                    for node in root.iter():
                        if node.text and node.text.strip():
                            parts.append(node.text.strip())
                except ElementTree.ParseError:
                    continue
    except Exception:
        return ""
    return _text_clean(" ".join(parts))


def _kind_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if suffix in OFFICE_EXTENSIONS:
        return "document"
    if suffix in TEXT_EXTENSIONS:
        return "text"
    return "other"


def _extract_text(path: Path, kind: str) -> str:
    suffix = path.suffix.lower()
    try:
        if suffix in TEXT_EXTENSIONS:
            return _read_plain_text(path)
        if suffix in OFFICE_EXTENSIONS:
            return _office_text(path)
    except Exception:
        return ""
    return ""


def _iter_files(source: Path, recursive: bool) -> list[Path]:
    if source.is_file():
        return [source]
    if not source.is_dir():
        return []
    pattern = "**/*" if recursive else "*"
    files = []
    for path in source.glob(pattern):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
        if len(files) >= MAX_FILES:
            break
    return files


def ingest(request: dict) -> dict:
    sources = request.get("sources") or request.get("assets") or []
    if isinstance(sources, str):
        sources = [sources]
    recursive = bool(request.get("recursive", True))
    include_text = bool(request.get("extract_text", True))

    files = []
    for source in sources:
        files.extend(_iter_files(_resolve_path(str(source)), recursive))

    seen = set()
    items = []
    skipped = []
    for path in files[:MAX_FILES]:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        try:
            stat = resolved.stat()
        except Exception:
            skipped.append({"path": str(resolved), "reason": "stat_failed"})
            continue
        if stat.st_size > MAX_FILE_BYTES:
            skipped.append({"path": str(resolved), "reason": "too_large", "bytes": stat.st_size})
            continue

        kind = _kind_for(resolved)
        text = _extract_text(resolved, kind) if include_text else ""
        item = {
            "path": str(resolved),
            "name": resolved.name,
            "extension": resolved.suffix.lower(),
            "kind": kind,
            "mime": mimetypes.guess_type(resolved.name)[0] or "application/octet-stream",
            "bytes": stat.st_size,
            "sha256": _hash_file(resolved),
            "text_excerpt": text,
            "text_chars": len(text),
        }
        items.append(item)

    summary = {
        "total": len(items),
        "images": sum(1 for item in items if item["kind"] == "image"),
        "audio": sum(1 for item in items if item["kind"] == "audio"),
        "video": sum(1 for item in items if item["kind"] == "video"),
        "documents": sum(1 for item in items if item["kind"] == "document"),
        "text": sum(1 for item in items if item["kind"] == "text"),
        "other": sum(1 for item in items if item["kind"] == "other"),
        "skipped": len(skipped),
    }

    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = MANIFEST_DIR / f"asset-manifest-{int(time.time())}.json"
    manifest_path = MANIFEST_DIR / f"asset-manifest-{int(time.time())}.json"
    manifest = {
        "status": "ok",
        "created_at": int(time.time()),
        "manifest_path": str(manifest_path.resolve()),
        "sources": [str(_resolve_path(str(source))) for source in sources],
        "recursive": recursive,
        "summary": summary,
        "items": items,
        "skipped": skipped,
        "safety": {
            "assets_are_data": True,
            "hidden_instructions_ignored": True,
            "max_file_bytes": MAX_FILE_BYTES,
            "max_files": MAX_FILES,
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a safe asset manifest for Video Studio.")
    parser.add_argument("--input-json", required=True)
    args = parser.parse_args()
    result = ingest(_read_json(Path(args.input_json)))
    _print(result)
    return 0 if result.get("status") == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
