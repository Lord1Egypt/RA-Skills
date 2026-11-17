"""Build a provenance-preserving inventory of a product package."""

from __future__ import annotations

import mimetypes
from pathlib import Path

from .cache import sha256_file, source_files

DOCUMENT_RULES = [
    # Specific document types FIRST (before general policy_terms)
    ("product_manual", 1, ("产品说明书",)),
    ("product_summary", 1, ("产品摘要",)),
    ("service_manual", 2, ("增值服务", "健康管理权益", "服务手册")),
    ("underwriting_rules", 2, ("投保规则", "承保规则")),
    ("surrender_rules", 2, ("保全规则",)),
    ("cash_value_table", 3, ("现金价值表", "现金价值全表")),
    ("rate_table", 3, ("费率表",)),
    ("exemption_notice", 3, ("免除保险人责任条款的书面说明",)),
    ("application_notice", 5, ("投保提示书",)),
    ("privacy_or_identity", 7, ("个人信息保护", "税收居民", "声明与授权")),
    # General policy_terms LAST (catch-all for policy-related docs)
    ("policy_terms", 8, ("保险条款", "条款目录", "责任免除", "条款", "阅读指引", "保险合同")),
]


def classify_document(text: str, filename: str = "") -> tuple[str, int]:
    haystack = f"{text}\n{filename}".lower()
    for document_type, rank, keywords in DOCUMENT_RULES:
        if any(keyword.lower() in haystack for keyword in keywords):
            return document_type, rank
    suffix = Path(filename).suffix.lower()
    if suffix in {".xls", ".xlsx"}:
        return "spreadsheet_unknown", 6
    return "unknown", 99


def _media_type(path: Path) -> str:
    if path.suffix.lower() == ".xlsx":
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if path.suffix.lower() == ".xls":
        return "application/vnd.ms-excel"
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def build_inventory(product_dir: Path, *, extracted_text: dict[str, str] | None = None) -> list[dict]:
    product_dir = Path(product_dir).resolve()
    extracted_text = extracted_text or {}
    first_by_hash: dict[str, str] = {}
    inventory = []
    for path in source_files(product_dir):
        relative = path.relative_to(product_dir).as_posix()
        digest = sha256_file(path)
        text = extracted_text.get(relative, extracted_text.get(path.name, ""))
        document_type, authority_rank = classify_document(text, path.name)
        duplicate_of = first_by_hash.get(digest)
        first_by_hash.setdefault(digest, relative)
        inventory.append({
            "source_id": f"source-{len(inventory) + 1:03d}",
            "path": str(path),
            "relative_path": relative,
            "filename": path.name,
            "extension": path.suffix.lower(),
            "media_type": _media_type(path),
            "size": path.stat().st_size,
            "sha256": digest,
            "duplicate_of": duplicate_of,
            "document_type": document_type,
            "authority_rank": authority_rank,
        })
    return inventory
