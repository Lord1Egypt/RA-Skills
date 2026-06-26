#!/usr/bin/env python3
"""Physical paragraph enumeration shared by structure mapping and style tasks."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


CHAPTER_RE = re.compile(r"^第\s*([一二三四五六七八九十百千万两0-9]+)\s*章")
LEVEL3_RE = re.compile(r"^(\d+\.\d+\.\d+)\s*(.*)$")
LEVEL2_RE = re.compile(r"^(\d+\.\d+)\s*(.*)$")
ABSTRACT_HEADING_RE = re.compile(r"^(摘\s*要|摘要)$")
ABSTRACT_EN_HEADING_RE = re.compile(r"^abstract$", re.I)
KEYWORDS_RE = re.compile(r"^(关键词|关键字|Key words?|Keywords?)", re.I)
ENUM_LINE_RE = re.compile(r"^[\(（]?\d+[)）．.]|^[(（][一二三四五六七八九十]+[)）]")

CHAPTER1_BACKGROUND_KEYWORDS = ("背景", "意义", "现状与意义", "研究背景", "选题背景", "研究意义")
CHAPTER1_OBJECTIVE_KEYWORDS = ("目标", "研究目标", "研究问题", "拟解决", "研究任务")
CHAPTER1_OBJECT_KEYWORDS = ("研究对象", "对象", "问题定义", "场景定义", "应用场景")
CHAPTER1_STATUS_KEYWORDS = ("研究现状", "相关研究", "国内外研究", "国内外现状", "文献综述")
CHAPTER1_CONTENT_KEYWORDS = ("研究内容", "主要工作", "本文工作", "本文内容", "研究方案")
CHAPTER1_STRUCTURE_KEYWORDS = ("论文结构", "组织结构", "章节安排", "本文结构", "全文结构")


@dataclass
class ParagraphContextRecord:
    text: str
    chapter: str
    section_path: str
    chapter_number: Optional[int]
    heading_level: Optional[int]
    heading_title: str
    heading_number: str
    source_zone: str
    paragraph_index_in_document: int
    paragraph_index_in_chapter: int
    paragraph_index_in_section: int
    paragraph_index_in_zone: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _parse_chapter_number(title: str) -> Optional[int]:
    match = CHAPTER_RE.match(_compact(title))
    if not match:
        return None
    raw = match.group(1)
    if raw.isdigit():
        return int(raw)
    table = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    if raw == "十":
        return 10
    if raw.startswith("十") and len(raw) == 2:
        return 10 + table.get(raw[1], 0)
    if raw.endswith("十") and len(raw) == 2:
        return table.get(raw[0], 0) * 10
    if len(raw) == 3 and raw[1] == "十":
        return table.get(raw[0], 0) * 10 + table.get(raw[2], 0)
    return table.get(raw)


def _heading_number_and_title(text: str, level: Optional[int]) -> tuple[str, str]:
    stripped = (text or "").strip()
    if level == 2:
        match = LEVEL2_RE.match(stripped)
        if match:
            return match.group(1), match.group(2).strip()
    if level == 3:
        match = LEVEL3_RE.match(stripped)
        if match:
            return match.group(1), match.group(2).strip()
    return "", stripped


def _abstract_blocks(blocks: List[Any]) -> List[str]:
    start = None
    stop = None
    for idx, block in enumerate(blocks):
        text = (getattr(block, "text", None) or "").strip()
        compact = _compact(text)
        if start is None and ABSTRACT_HEADING_RE.match(compact):
            start = idx + 1
            continue
        if start is not None:
            if ABSTRACT_EN_HEADING_RE.match(compact):
                stop = idx
                break
            if KEYWORDS_RE.match(text):
                stop = idx
                break
            if CHAPTER_RE.match(compact):
                stop = idx
                break
    if start is None:
        return []
    rows = blocks[start:stop] if stop is not None else blocks[start:]
    raw_lines: List[str] = []
    for block in rows:
        text = (getattr(block, "text", None) or "").strip()
        if not text:
            continue
        if KEYWORDS_RE.match(text):
            break
        if ABSTRACT_EN_HEADING_RE.match(_compact(text)):
            break
        raw_lines.append(text)
    paragraphs: List[str] = []
    buffer = ""
    for line in raw_lines:
        if not buffer:
            buffer = line
            continue
        if ENUM_LINE_RE.match(line):
            paragraphs.append(buffer)
            buffer = line
            continue
        buffer += line
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


def enumerate_document_paragraphs(parsed_document: Any) -> List[ParagraphContextRecord]:
    """Enumerate the physical paragraphs that participate in downstream review."""
    blocks = list(getattr(parsed_document, "blocks", []) or [])
    chapters = list(getattr(parsed_document, "chapters", []) or [])

    records: List[ParagraphContextRecord] = []
    paragraph_index_in_document = 0

    abstract_paragraphs = _abstract_blocks(blocks)
    for idx, text in enumerate(abstract_paragraphs, start=1):
        paragraph_index_in_document += 1
        records.append(
            ParagraphContextRecord(
                text=text,
                chapter="摘要",
                section_path="摘要",
                chapter_number=0,
                heading_level=0,
                heading_title="摘要",
                heading_number="abstract",
                source_zone="abstract",
                paragraph_index_in_document=paragraph_index_in_document,
                paragraph_index_in_chapter=idx,
                paragraph_index_in_section=idx,
                paragraph_index_in_zone=idx,
            )
        )

    for chapter in chapters:
        chapter_title = str(chapter.get("title", "") or "")
        chapter_number = _parse_chapter_number(chapter_title)
        chapter_para_index = 0
        section_para_index = 0
        current_heading_level: Optional[int] = None
        current_heading_text = chapter_title
        current_heading_number = ""

        for item in chapter.get("items", []) or []:
            item_type = getattr(item, "type", None) or item.get("type", "")
            item_text = (getattr(item, "text", None) or item.get("text", "") or "").strip()
            if not item_text:
                continue
            if item_type == "heading":
                current_heading_level = getattr(item, "level", None) or item.get("level")
                current_heading_text = item_text
                current_heading_number, parsed_heading_title = _heading_number_and_title(item_text, current_heading_level)
                current_heading_text = parsed_heading_title or item_text
                section_para_index = 0
                continue
            if item_type != "para":
                continue

            chapter_para_index += 1
            section_para_index += 1
            paragraph_index_in_document += 1
            section_path = (
                getattr(item, "section_path", None)
                or getattr(item, "sectionPath", None)
                or item.get("section_path")
                or item.get("sectionPath")
                or chapter_title
            )
            records.append(
                ParagraphContextRecord(
                    text=item_text,
                    chapter=chapter_title,
                    section_path=section_path,
                    chapter_number=chapter_number,
                    heading_level=current_heading_level,
                    heading_title=current_heading_text,
                    heading_number=current_heading_number,
                    source_zone="body",
                    paragraph_index_in_document=paragraph_index_in_document,
                    paragraph_index_in_chapter=chapter_para_index,
                    paragraph_index_in_section=section_para_index,
                    paragraph_index_in_zone=chapter_para_index,
                )
            )
    return records
