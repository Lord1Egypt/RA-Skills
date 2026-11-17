from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OriginalPack:
    active: bool
    block: str
    source_name: str
    character_count: int


def build_original_pack(path: str | None = None) -> OriginalPack:
    if not path:
        return OriginalPack(False, "", "", 0)

    source = Path(path)
    content = source.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Original rewrite file is empty: {source}")

    return build_original_pack_text(content, source.name)


def build_original_pack_text(content: str, source_name: str = "supplied draft") -> OriginalPack:
    content = content.strip()
    if not content:
        raise ValueError("Original rewrite text is empty.")
    block = "\n".join(
        [
            "# Original Text For Rewrite Comparison",
            "",
            f"Original: {source_name}",
            "This text is the authority for meaning, claims, entities, chronology, polarity,",
            "uncertainty, causality, and constraints. Do not invent specificity to make it vivid.",
            "Do not imitate its style unless it was separately supplied as a style reference.",
            "",
            content,
        ]
    )
    return OriginalPack(True, block, source_name, len(content))
