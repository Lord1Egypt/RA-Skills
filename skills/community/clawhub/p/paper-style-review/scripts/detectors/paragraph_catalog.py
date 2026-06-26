#!/usr/bin/env python3
"""把论文 chapters 结构展开为可遍历的正文段落目录。"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ParagraphEntry:
    global_index: int
    chapter: str
    section_path: str
    text: str
    item_index_in_chapter: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _item_text(item: Any) -> str:
    return getattr(item, "text", None) or item.get("text", "")


def _item_type(item: Any) -> str:
    return getattr(item, "type", None) or item.get("type", "")


def _item_section_path(item: Any) -> str:
    return getattr(item, "section_path", None) or getattr(item, "sectionPath", None) or item.get("section_path") or item.get("sectionPath") or ""


def catalog_paragraphs(chapters: List[Dict[str, Any]]) -> List[ParagraphEntry]:
    """展开全部章节中的 para 项，形成全论文正文段落目录。"""
    paragraphs: List[ParagraphEntry] = []
    global_index = 1
    for chapter in chapters:
        chapter_title = chapter.get("title", "")
        for item_index, item in enumerate(chapter.get("items", []), start=1):
            if _item_type(item) != "para":
                continue
            text = (_item_text(item) or "").strip()
            if not text:
                continue
            paragraphs.append(
                ParagraphEntry(
                    global_index=global_index,
                    chapter=chapter_title,
                    section_path=_item_section_path(item),
                    text=text,
                    item_index_in_chapter=item_index,
                )
            )
            global_index += 1
    return paragraphs
