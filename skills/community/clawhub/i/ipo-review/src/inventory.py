from __future__ import annotations

import hashlib
from pathlib import Path

from .models import DocumentInfo


SUPPORTED_SUFFIXES = {".pdf", ".docx", ".xlsx", ".txt"}


def build_inventory(input_dir: str | Path, roles: dict) -> list[DocumentInfo]:
    root = Path(input_dir)
    docs: list[DocumentInfo] = []
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)
    for idx, path in enumerate(sorted(p for p in root.rglob("*") if p.is_file()), 1):
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        role, role_meta = detect_role(path, roles)
        docs.append(DocumentInfo(
            doc_id=f"DOC{idx:03d}",
            path=str(path),
            filename=path.name,
            suffix=path.suffix.lower(),
            role=role,
            role_name=role_meta["name"],
            priority=int(role_meta["priority"]),
            version=detect_version(path.name),
            sha256=file_hash(path),
        ))
    return docs


def detect_role(path: Path, roles: dict) -> tuple[str, dict]:
    haystack = str(path)
    best = ("other", roles.get("other", {"name": "其他文件", "priority": 9, "keywords": []}), 0)
    for role, meta in roles.items():
        score = sum(1 for kw in meta.get("keywords", []) if kw and kw in haystack)
        if score > best[2]:
            best = (role, meta, score)
    return best[0], best[1]


def detect_version(filename: str) -> str:
    if any(k in filename for k in ["修订", "更新", "补充"]):
        return "修订/更新版"
    return "普通版"


def file_hash(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()
