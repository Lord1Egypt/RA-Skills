from __future__ import annotations

import re
from pathlib import Path


INVALID_CHARS = r'<>:"|?*'


def normalize_repo_path(value: str) -> str:
    path = (value or "").replace("\\", "/").strip()
    while "//" in path:
        path = path.replace("//", "/")
    path = path.lstrip("/")
    parts = []
    for part in path.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            raise ValueError("repository path must not contain '..'")
        parts.append(sanitize_filename(part))
    return "/".join(parts)


def sanitize_filename(value: str, fallback: str = "untitled") -> str:
    name = (value or "").strip()
    if not name:
        name = fallback
    for ch in INVALID_CHARS:
        name = name.replace(ch, "-")
    name = re.sub(r"\s+", " ", name).strip()
    return name[:180] or fallback


def stem(value: str) -> str:
    return sanitize_filename(Path(value or "untitled").stem, "untitled")


def source_folder(file_kind: str, filename: str = "") -> str:
    kind = (file_kind or "").lower()
    suffix = Path(filename).suffix.lower()
    if kind == "pdf" or suffix == ".pdf":
        return "pdfs"
    if kind in {"word", "doc", "docx"} or suffix in {".doc", ".docx"}:
        return "docs"
    if kind in {"sheet", "xls", "xlsx", "csv"} or suffix in {".xls", ".xlsx", ".csv"}:
        return "sheets"
    if kind in {"text", "md", "markdown", "txt"} or suffix in {".txt", ".md", ".markdown"}:
        return "text"
    if kind == "code_pack":
        return "code"
    if kind == "archive" or suffix in {".zip", ".rar", ".7z", ".tar", ".gz"}:
        return "archives"
    return "other"
