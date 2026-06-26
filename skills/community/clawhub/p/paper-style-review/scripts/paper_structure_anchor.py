#!/usr/bin/env python3
"""论文结构图谱模块。

唯一职责：
- 读取论文正文与格式规范来源；
- 用严格、位置优先的规则建立 1/2/3 级结构树；
- 为每个正文段落输出统一的物理位置 + 功能分类结果；
- 给风格学习、风格评价、批注定位提供同一份结构事实源。

设计原则：
- 不复用通用章节树中的宽松标题判定，避免把正文句子误抓成标题；
- 物理段落身份与功能分类解耦；
- 对外只暴露一个统一结构图谱输出，不让下游自己拼装第二套结构事实。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from zipfile import ZipFile

from lxml import etree
from chapter_scope import chapter_in_scope, chapter_scope_label, filter_outline_by_chapter_scope, normalize_chapter_scope
from document_parser import ParsedDocument, compact_text, detect_author, detect_title, is_noise_paragraph, parse_blocks_with_meta
try:
    from classifiers.section_function_classifier import (
        build_section_function_index,
        classify_section_packages,
    )
    from extractors.paragraph_context import (
        CHAPTER1_BACKGROUND_KEYWORDS,
        CHAPTER1_CONTENT_KEYWORDS,
        CHAPTER1_OBJECTIVE_KEYWORDS,
        CHAPTER1_OBJECT_KEYWORDS,
        CHAPTER1_STATUS_KEYWORDS,
        CHAPTER1_STRUCTURE_KEYWORDS,
        enumerate_document_paragraphs,
    )
    from target_document_index import TargetDocumentIndex
except Exception:
    from .classifiers.section_function_classifier import (
        build_section_function_index,
        classify_section_packages,
    )
    from .extractors.paragraph_context import (
        CHAPTER1_BACKGROUND_KEYWORDS,
        CHAPTER1_CONTENT_KEYWORDS,
        CHAPTER1_OBJECTIVE_KEYWORDS,
        CHAPTER1_OBJECT_KEYWORDS,
        CHAPTER1_STATUS_KEYWORDS,
        CHAPTER1_STRUCTURE_KEYWORDS,
        enumerate_document_paragraphs,
    )
    from .target_document_index import TargetDocumentIndex


SCRIPT_ROOT = Path(__file__).resolve().parent
DEFAULT_FORMAT_RULES_PATH = SCRIPT_ROOT.parent / "references" / "format-rules.json"

CHAPTER_HEADING_RE = re.compile(r"^第\s*([一二三四五六七八九十百千万两0-9]+)\s*章\s*(.*)$")
LEVEL2_HEADING_RE = re.compile(r"^(\d+\.\d+)\s+(.+)$")
LEVEL3_HEADING_RE = re.compile(r"^(\d+\.\d+\.\d+)\s+(.+)$")
COMPACT_LEVEL2_HEADING_RE = re.compile(r"^(\d+\.\d+)([A-Za-z\u4e00-\u9fff（(].+)$")
COMPACT_LEVEL3_HEADING_RE = re.compile(r"^(\d+\.\d+\.\d+)([A-Za-z\u4e00-\u9fff（(].+)$")
BACKMATTER_HEADING_RE = re.compile(r"^(参考文献|致谢|附录|攻读.*期间|作者简介|发表.*成果|在学期间)")
DOTTED_LINE_RE = re.compile(r"\.{4,}|·{4,}|…{3,}")
STYLE_LEVEL_HINTS = [
    (1, ["heading 1", "标题 1", "标题1", "标题样式1", "title 1"]),
    (2, ["heading 2", "标题 2", "标题2", "标题样式2", "title 2"]),
    (3, ["heading 3", "标题 3", "标题3", "标题样式3", "title 3"]),
]
HEADING_FORBIDDEN_PUNCT = "。！？；!?"
CHAPTER_FALSE_POSITIVE_PREFIXES = ("为", "主要", "重点", "首先", "其次", "最后", "阐述", "介绍", "描述")
DOCX_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
FRONT_HEADING_LABELS = {
    "独创性声明": "独创性声明",
    "学位论文版权使用授权书": "学位论文版权使用授权书",
    "摘要": "摘要",
    "abstract": "Abstract",
}


@dataclass(frozen=True)
class DocxOutlineMarker:
    raw_text: str
    title: str
    level: int
    page_ordinal: int
    section_kind: str


def _contains_any(text: str, keywords: Tuple[str, ...] | List[str]) -> bool:
    compact = compact_text(text)
    return any(keyword and keyword in compact for keyword in keywords)


def _style_heading_level(style_name: str) -> Optional[int]:
    style_lower = (style_name or "").strip().lower()
    for level, hints in STYLE_LEVEL_HINTS:
        if any(hint in style_lower for hint in hints):
            return level
    return None


def _looks_like_heading_text(text: str, *, max_len: int = 80) -> bool:
    stripped = (text or "").strip()
    if not stripped or len(stripped) > max_len:
        return False
    if DOTTED_LINE_RE.search(stripped):
        return False
    if any(mark in stripped for mark in HEADING_FORBIDDEN_PUNCT):
        return False
    if stripped.count("，") + stripped.count(",") > 1:
        return False
    if stripped.endswith(("，", ",", "：", ":", "、", "（", "(")):
        return False
    return True


def _looks_like_chapter_heading(text: str) -> bool:
    stripped = (text or "").strip()
    if not stripped:
        return False
    compact = compact_text(stripped)
    match = CHAPTER_HEADING_RE.match(compact)
    if not match:
        return False
    suffix = match.group(2)
    if not suffix:
        return True
    if suffix.startswith(CHAPTER_FALSE_POSITIVE_PREFIXES):
        return False
    if any(mark in stripped for mark in "，。；：!?！？"):
        return False
    return len(stripped) <= 60


def _looks_like_numbered_heading(text: str, level: int) -> bool:
    stripped = (text or "").strip()
    if not _looks_like_heading_text(stripped):
        return False
    numbered_re = LEVEL3_HEADING_RE if level == 3 else LEVEL2_HEADING_RE
    compact_re = COMPACT_LEVEL3_HEADING_RE if level == 3 else COMPACT_LEVEL2_HEADING_RE
    match = numbered_re.match(stripped)
    if match:
        return bool(match.group(2).strip())
    compact_match = compact_re.match(compact_text(stripped))
    if compact_match:
        return bool(compact_match.group(2).strip())
    return False


def _strict_heading_level(block: Any) -> Optional[int]:
    text = (getattr(block, "text", None) or "").strip()
    if not text or is_noise_paragraph(text):
        return None

    style_level = _style_heading_level(getattr(block, "style_name", "") or "")
    if style_level == 1:
        return 1 if _looks_like_chapter_heading(text) else None
    if style_level in {2, 3}:
        return style_level if _looks_like_heading_text(text) else None

    if _looks_like_chapter_heading(text):
        return 1
    if _looks_like_numbered_heading(text, 3):
        return 3
    if _looks_like_numbered_heading(text, 2):
        return 2
    return None


def _chapter_number(title: str) -> Optional[int]:
    compact = compact_text(title)
    match = CHAPTER_HEADING_RE.match(compact)
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


def _parse_heading_parts(text: str, level: Optional[int]) -> Tuple[str, str]:
    stripped = str(text or "").strip()
    if level == 1:
        match = CHAPTER_HEADING_RE.match(compact_text(stripped))
        if match:
            suffix = match.group(2).strip() or stripped
            return f"第{match.group(1)}章", suffix
        return "", stripped
    if level == 2:
        match = LEVEL2_HEADING_RE.match(stripped)
        if match:
            return match.group(1), match.group(2).strip()
        compact_match = COMPACT_LEVEL2_HEADING_RE.match(compact_text(stripped))
        if compact_match:
            return compact_match.group(1), compact_match.group(2).strip()
        return "", stripped
    if level == 3:
        match = LEVEL3_HEADING_RE.match(stripped)
        if match:
            return match.group(1), match.group(2).strip()
        compact_match = COMPACT_LEVEL3_HEADING_RE.match(compact_text(stripped))
        if compact_match:
            return compact_match.group(1), compact_match.group(2).strip()
        return "", stripped
    return "", stripped


def _looks_like_backmatter_heading(text: str) -> bool:
    stripped = (text or "").strip()
    if not stripped:
        return False
    return bool(BACKMATTER_HEADING_RE.match(compact_text(stripped)))


def _load_docx_outline_markers(path: Path) -> List[DocxOutlineMarker]:
    if path.suffix.lower() != ".docx":
        return []

    markers: List[DocxOutlineMarker] = []
    seen_front_titles: set[str] = set()
    saw_toc = False
    page_ordinal = 1

    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = etree.fromstring(xml)
    paragraphs = root.xpath("//w:body/w:p", namespaces=DOCX_NS)

    for paragraph in paragraphs:
        breaks = paragraph.xpath('.//w:br[@w:type="page"] | .//w:lastRenderedPageBreak', namespaces=DOCX_NS)
        if breaks:
            page_ordinal += len(breaks)

        style_id = (paragraph.xpath("./w:pPr/w:pStyle/@w:val", namespaces=DOCX_NS) or [""])[0]
        text = "".join(paragraph.xpath(".//w:t/text()", namespaces=DOCX_NS)).strip()
        compact = compact_text(text)
        compact_lookup = compact.lower() if compact else compact

        if not saw_toc and style_id.upper().startswith("TOC"):
            saw_toc = True
            markers.append(
                DocxOutlineMarker(
                    raw_text="目录",
                    title="目录",
                    level=1,
                    page_ordinal=page_ordinal,
                    section_kind="frontmatter",
                )
            )

        if compact_lookup in FRONT_HEADING_LABELS:
            title = FRONT_HEADING_LABELS[compact_lookup]
            if title in seen_front_titles:
                continue
            seen_front_titles.add(title)
            markers.append(
                DocxOutlineMarker(
                    raw_text=text or title,
                    title=title,
                    level=1,
                    page_ordinal=page_ordinal,
                    section_kind="frontmatter",
                )
            )

    return markers


def _find_body_bounds(blocks: List[Any]) -> Tuple[int, int]:
    start = None
    for idx, block in enumerate(blocks):
        if _strict_heading_level(block) == 1:
            start = idx
            break
    if start is None:
        raise ValueError("failed to locate first strict chapter heading")

    end = len(blocks)
    for idx in range(start + 1, len(blocks)):
        if _looks_like_backmatter_heading(getattr(blocks[idx], "text", "")):
            end = idx
            break
    return start, end


def _build_strict_chapters(blocks: List[Any]) -> List[Dict[str, Any]]:
    start, end = _find_body_bounds(blocks)
    body_blocks = blocks[start:end]

    chapters: List[Dict[str, Any]] = []
    current_chapter: Optional[Dict[str, Any]] = None
    current_level2: Optional[str] = None
    current_level3: Optional[str] = None

    def current_path() -> str:
        parts: List[str] = []
        if current_chapter:
            parts.append(current_chapter["title"])
        if current_level2:
            parts.append(current_level2)
        if current_level3:
            parts.append(current_level3)
        return " > ".join(parts)

    for block in body_blocks:
        text = (getattr(block, "text", None) or "").strip()
        if not text:
            continue

        level = _strict_heading_level(block)
        if level == 1:
            if current_chapter is not None and compact_text(current_chapter["title"]) == compact_text(text):
                continue
            current_chapter = {"title": text, "items": [], "blocks": []}
            chapters.append(current_chapter)
            current_level2 = None
            current_level3 = None
            current_chapter["items"].append({"type": "heading", "text": text, "section_path": text, "level": 1})
            current_chapter["blocks"].append(block)
            continue

        if current_chapter is None:
            continue

        current_chapter["blocks"].append(block)
        if level == 2:
            current_level2 = text
            current_level3 = None
            current_chapter["items"].append({"type": "heading", "text": text, "section_path": current_path(), "level": 2})
            continue
        if level == 3:
            current_level3 = text
            current_chapter["items"].append({"type": "heading", "text": text, "section_path": current_path(), "level": 3})
            continue
        if is_noise_paragraph(text):
            continue
        current_chapter["items"].append({"type": "para", "text": text, "section_path": current_path()})

    return chapters


def _load_heading_rules(format_spec_path: Optional[Path]) -> Dict[str, Any]:
    candidates: List[Path] = []
    if format_spec_path and format_spec_path.suffix.lower() == ".json":
        candidates.append(format_spec_path)
    candidates.append(DEFAULT_FORMAT_RULES_PATH)
    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
            headings = data.get("headings", {})
            if isinstance(headings, dict) and headings:
                return {"source": str(candidate), "headings": headings}
        except Exception:
            continue
    return {
        "source": None,
        "headings": {
            "level1": {"label": "章标题（第一级）", "example": "第1章 XXX"},
            "level2": {"label": "条标题（第二级）", "example": "1.1 XXXXXX"},
            "level3": {"label": "款标题（第三级）", "example": "1.1.1 XXXXXX"},
            "numberingRule": "章、条、款、项用阿拉伯数字编号，各级之间用半角实心下圆点'.'相隔。",
        },
    }


@dataclass(frozen=True)
class AnchorSpec:
    anchor_type: str
    label: str
    description: str
    style_bucket: str
    specificity: str = "specific"


ANCHOR_SPECS: Dict[str, AnchorSpec] = {
    "abstract.paragraph": AnchorSpec("abstract.paragraph", "摘要段", "摘要中的正文段。", "abstract_paragraph"),
    "chapter1.section_lead": AnchorSpec("chapter1.section_lead", "第一章通用总领段", "第一章章级导语。", "chapter1_section_lead", "generic"),
    "chapter1.background_significance": AnchorSpec(
        "chapter1.background_significance",
        "第一章背景及意义段",
        "第一章背景及意义小节的正文段。",
        "chapter1_background_significance",
    ),
    "chapter1.research_objective": AnchorSpec(
        "chapter1.research_objective",
        "第一章研究对象及目标段",
        "第一章研究对象/目标小节首段。",
        "chapter1_research_objective",
    ),
    "chapter1.research_object_detail": AnchorSpec(
        "chapter1.research_object_detail",
        "第一章研究对象介绍段",
        "第一章研究对象/目标小节后续展开段。",
        "chapter1_research_object_detail",
    ),
    "chapter1.research_status_lead": AnchorSpec(
        "chapter1.research_status_lead",
        "第一章研究现状总领段",
        "第一章研究现状小节总领段。",
        "chapter1_research_status_lead",
    ),
    "chapter1.research_status_detail": AnchorSpec(
        "chapter1.research_status_detail",
        "第一章研究现状展开段",
        "第一章研究现状小节展开段。",
        "chapter1_research_status_detail",
    ),
    "chapter1.research_content_lead": AnchorSpec(
        "chapter1.research_content_lead",
        "第一章研究内容总领段",
        "第一章研究内容小节总领段。",
        "chapter1_research_content_lead",
    ),
    "chapter1.research_content_detail": AnchorSpec(
        "chapter1.research_content_detail",
        "第一章研究内容展开段",
        "第一章研究内容小节展开段。",
        "chapter1_research_content_detail",
    ),
    "chapter1.structure_overview": AnchorSpec(
        "chapter1.structure_overview",
        "第一章结构段",
        "第一章组织结构小节。",
        "chapter1_structure_overview",
    ),
    "chapter1.section_detail": AnchorSpec(
        "chapter1.section_detail",
        "第一章通用介绍段",
        "第一章未命中特定小节时的通用正文段。",
        "chapter1_section_detail",
        "generic",
    ),
    "chapter2.level2_intro": AnchorSpec(
        "chapter2.level2_intro",
        "第二章二级标题介绍段",
        "第二章二级标题下首段。",
        "chapter2_level2_intro",
    ),
    "chapter2.level2_body": AnchorSpec(
        "chapter2.level2_body",
        "第二章二级标题正文段",
        "第二章二级标题下后续正文段。",
        "chapter2_level2_body",
    ),
    "chapter2.level3_intro": AnchorSpec(
        "chapter2.level3_intro",
        "第二章三级标题介绍段",
        "第二章三级标题下首段。",
        "chapter2_level3_intro",
    ),
    "chapter2.level3_implementation": AnchorSpec(
        "chapter2.level3_implementation",
        "第二章三级标题实现段",
        "第二章三级标题下后续实现/细化段。",
        "chapter2_level3_implementation",
    ),
    "chapter3.1_intro": AnchorSpec(
        "chapter3.1_intro",
        "第三章3.1引言段",
        "第三章 3.1 引言中的正文段。",
        "chapter3_1_intro",
    ),
    "chapter3.level2_intro": AnchorSpec(
        "chapter3.level2_intro",
        "第三章二级标题介绍段",
        "第三章二级标题下首段。",
        "chapter3_level2_intro",
    ),
    "chapter3.level2_implementation": AnchorSpec(
        "chapter3.level2_implementation",
        "第三章二级标题正文段",
        "第三章二级标题下后续正文段。",
        "chapter3_level2_implementation",
    ),
    "chapter3.level3_intro": AnchorSpec(
        "chapter3.level3_intro",
        "第三章三级标题介绍段",
        "第三章三级标题下首段。",
        "chapter3_level3_intro",
    ),
    "chapter3.level3_implementation": AnchorSpec(
        "chapter3.level3_implementation",
        "第三章三级标题实现段",
        "第三章三级标题下后续实现/细化段。",
        "chapter3_level3_implementation",
    ),
    "later.level2_intro": AnchorSpec(
        "later.level2_intro",
        "后续章节二级标题介绍段",
        "第四章及以后章节二级标题下首段。",
        "later_chapter_level2_intro",
    ),
    "later.level2_implementation": AnchorSpec(
        "later.level2_implementation",
        "后续章节二级标题正文段",
        "第四章及以后章节二级标题下后续正文段。",
        "later_chapter_level2_implementation",
    ),
    "later.level3_intro": AnchorSpec(
        "later.level3_intro",
        "后续章节三级标题介绍段",
        "第四章及以后章节三级标题下首段。",
        "later_chapter_level3_intro",
    ),
    "later.level3_implementation": AnchorSpec(
        "later.level3_implementation",
        "后续章节三级标题实现段",
        "第四章及以后章节三级标题下后续实现/细化段。",
        "later_chapter_level3_implementation",
    ),
    "generic.chapter_intro": AnchorSpec(
        "generic.chapter_intro",
        "通用章节引导段",
        "未命中特定规则时的章节引导段。",
        "generic_chapter_intro",
        "generic",
    ),
}

def _anchor_spec(anchor_type: str) -> AnchorSpec:
    return ANCHOR_SPECS[anchor_type]


def _chapter1_anchor(record: Any) -> Tuple[str, str]:
    heading_text = compact_text(getattr(record, "heading_title", "") or "")
    paragraph_index_in_section = int(getattr(record, "paragraph_index_in_section", 0) or 0)

    if _contains_any(heading_text, CHAPTER1_STRUCTURE_KEYWORDS):
        return "chapter1.structure_overview", "命中第一章结构类标题关键词。"
    if _contains_any(heading_text, CHAPTER1_STATUS_KEYWORDS):
        if paragraph_index_in_section == 1 and getattr(record, "heading_level", None) == 2:
            return "chapter1.research_status_lead", "命中第一章研究现状标题关键词，且为小节首段。"
        return "chapter1.research_status_detail", "命中第一章研究现状标题关键词，按研究现状展开段定位。"
    if _contains_any(heading_text, CHAPTER1_CONTENT_KEYWORDS):
        if paragraph_index_in_section == 1:
            return "chapter1.research_content_lead", "命中第一章研究内容标题关键词，且为小节首段。"
        return "chapter1.research_content_detail", "命中第一章研究内容标题关键词，按研究内容展开段定位。"
    if _contains_any(heading_text, CHAPTER1_BACKGROUND_KEYWORDS):
        return "chapter1.background_significance", "命中第一章背景/意义标题关键词。"
    if _contains_any(heading_text, CHAPTER1_OBJECTIVE_KEYWORDS) or _contains_any(heading_text, CHAPTER1_OBJECT_KEYWORDS):
        if paragraph_index_in_section == 1:
            return "chapter1.research_objective", "命中第一章研究对象/目标标题关键词，且为小节首段。"
        return "chapter1.research_object_detail", "命中第一章研究对象/目标标题关键词，按后续介绍段定位。"
    if paragraph_index_in_section == 1:
        return "chapter1.section_lead", "第一章未知小节，按位置归为通用总领段。"
    return "chapter1.section_detail", "第一章未知小节，按位置归为通用介绍段。"


def _later_anchor(prefix: str, heading_level: Optional[int], paragraph_index_in_section: int) -> Tuple[str, str]:
    if heading_level == 3:
        if paragraph_index_in_section == 1:
            return f"{prefix}.level3_intro", "三级标题下首段，按介绍段定位。"
        return f"{prefix}.level3_implementation", "三级标题下后续段，按实现/细化段定位。"
    if heading_level == 2:
        if paragraph_index_in_section == 1:
            return f"{prefix}.level2_intro", "二级标题下首段，按介绍段定位。"
        if prefix == "chapter2":
            return f"{prefix}.level2_body", "二级标题下后续正文段。"
        return f"{prefix}.level2_implementation", "二级标题下后续正文段。"
    return "generic.chapter_intro", "未落入二/三级标题，按通用章节引导段定位。"


def _infer_position_anchor(record: Any) -> Tuple[str, str]:
    chapter_number = getattr(record, "chapter_number", None)
    heading_level = getattr(record, "heading_level", None)
    heading_number = str(getattr(record, "heading_number", "") or "")
    paragraph_index_in_section = int(getattr(record, "paragraph_index_in_section", 0) or 0)

    if chapter_number == 0:
        return "abstract.paragraph", "摘要区域正文段。"
    if chapter_number == 1:
        return _chapter1_anchor(record)
    if chapter_number == 2:
        return _later_anchor("chapter2", heading_level, paragraph_index_in_section)
    if chapter_number == 3:
        if heading_number == "3.1" or "引言" in str(getattr(record, "heading_title", "") or ""):
            return "chapter3.1_intro", "第三章 3.1 引言段，整节按引言定位。"
        return _later_anchor("chapter3", heading_level, paragraph_index_in_section)
    return _later_anchor("later", heading_level, paragraph_index_in_section)


def _text_excerpt(text: str, limit: int = 80) -> str:
    stripped = str(text or "").strip()
    if len(stripped) <= limit:
        return stripped
    return stripped[:limit] + "…"


def _path_key(section_path: str, paragraph_index_in_section: Optional[int]) -> str:
    parts = [compact_text(part) for part in section_path.split(" > ") if part.strip()]
    prefix = "/".join(parts) if parts else "unknown"
    if paragraph_index_in_section is None:
        return prefix
    return f"{prefix}#p{int(paragraph_index_in_section):02d}"


def _text_hash(text: str) -> str:
    return "sha1:" + hashlib.sha1((text or "").encode("utf-8")).hexdigest()


def _display_heading(number: str, title: str) -> str:
    if number and title:
        return f"{number} {title}"
    return title or number


def _build_outline(
    chapters: List[Dict[str, Any]],
    front_outline_nodes: Optional[List[DocxOutlineMarker]] = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, str]], Dict[str, str]]:
    outline: List[Dict[str, Any]] = []
    section_number_map: Dict[str, Dict[str, str]] = {}
    normalized_path_map: Dict[str, str] = {}
    node_index = 1

    for marker in front_outline_nodes or []:
        outline.append(
            {
                "id": f"outline-{node_index:04d}",
                "level": marker.level,
                "chapterNumber": None,
                "number": "",
                "title": marker.title,
                "rawText": marker.raw_text,
                "path": marker.title,
                "sectionKind": marker.section_kind,
                "pageOrdinalEstimate": marker.page_ordinal,
            }
        )
        node_index += 1

    for chapter in chapters:
        chapter_title = str(chapter.get("title", "") or "")
        chapter_number = _chapter_number(chapter_title)
        chapter_no, chapter_name = _parse_heading_parts(chapter_title, 1)
        chapter_display = _display_heading(chapter_no, chapter_name)
        normalized_path_map[chapter_title] = chapter_display
        level2_counter = 0
        level3_counter = 0
        outline.append(
            {
                "id": f"outline-{node_index:04d}",
                "level": 1,
                "chapterNumber": chapter_number,
                "number": chapter_no,
                "title": chapter_name,
                "rawText": chapter_title,
                "path": chapter_display,
                "sectionKind": "body",
            }
        )
        node_index += 1
        current_level2_display = ""
        for item in chapter.get("items", []) or []:
            if item.get("type") != "heading":
                continue
            level = item.get("level")
            if level not in {2, 3}:
                continue
            raw_text = str(item.get("text", "") or "").strip()
            _, title = _parse_heading_parts(raw_text, level)
            number = ""
            if level == 2:
                level2_counter += 1
                if chapter_number is not None:
                    number = f"{chapter_number}.{level2_counter}"
                level3_counter = 0
            elif level == 3:
                if level2_counter == 0:
                    level2_counter = 1
                level3_counter += 1
                if chapter_number is not None:
                    number = f"{chapter_number}.{level2_counter}.{level3_counter}"

            section_path = item.get("section_path", "")
            section_number_map[section_path] = {
                "number": number,
                "title": title,
            }
            display_text = _display_heading(number, title)
            if level == 2:
                current_level2_display = display_text
                normalized_path = " > ".join([chapter_display, display_text])
            else:
                normalized_path = " > ".join([chapter_display, current_level2_display, display_text])
            normalized_path_map[section_path] = normalized_path
            outline.append(
                {
                    "id": f"outline-{node_index:04d}",
                    "level": level,
                    "chapterNumber": chapter_number,
                    "number": number,
                    "title": title,
                    "rawText": raw_text,
                    "path": normalized_path,
                    "sectionKind": "body",
                }
            )
            node_index += 1
    return outline, section_number_map, normalized_path_map


def _build_learning_bucket_summary(paragraph_anchors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for anchor in paragraph_anchors:
        bucket = anchor["styleLearningBucket"]
        entry = grouped.setdefault(
            bucket,
            {
                "bucket": bucket,
                "count": 0,
                "anchorTypes": set(),
                "samplePaths": [],
            },
        )
        entry["count"] += 1
        entry["anchorTypes"].add(anchor["positionAnchor"]["type"])
        if len(entry["samplePaths"]) < 3 and anchor["sectionPath"] not in entry["samplePaths"]:
            entry["samplePaths"].append(anchor["sectionPath"])

    rows: List[Dict[str, Any]] = []
    for bucket, entry in grouped.items():
        rows.append(
            {
                "bucket": bucket,
                "count": entry["count"],
                "anchorTypes": sorted(entry["anchorTypes"]),
                "samplePaths": entry["samplePaths"],
            }
        )
    rows.sort(key=lambda item: (-item["count"], item["bucket"]))
    return rows


def _outline_index(outline: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(item.get("path") or ""): item for item in outline if str(item.get("path") or "").strip()}


def _normalize_match_text(text: str) -> str:
    return (
        compact_text(text or "")
        .replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("「", '"')
        .replace("」", '"')
    )


def _resolve_review_main_node(
    index: Optional[TargetDocumentIndex],
    *,
    source_zone: str,
    chapter_title: str,
    raw_section_path: str,
    paragraph_text: str,
) -> Optional[Dict[str, Any]]:
    if index is None or source_zone not in {"body", "abstract"}:
        return None

    normalized_text = _normalize_match_text(paragraph_text)
    if not normalized_text:
        return None

    path_parts = [part.strip() for part in str(raw_section_path or "").split(" > ") if part.strip()]
    candidates = index.candidate_review_nodes(path_parts) if path_parts else []
    if not candidates and chapter_title:
        candidates = index.candidate_review_nodes([chapter_title])

    def _exact_hits(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        hits: List[Dict[str, Any]] = []
        for row in rows:
            if _normalize_match_text(str(row.get("text") or "")) == normalized_text:
                hits.append(row)
        return hits

    exact_hits = _exact_hits(candidates)
    if len(exact_hits) == 1:
        matched = dict(exact_hits[0])
        matched["_resolverMatchedFrom"] = "target_document_index:path_text_exact"
        return matched

    global_exact_hits = _exact_hits(list(index.review_paragraph_nodes))
    if len(global_exact_hits) == 1:
        matched = dict(global_exact_hits[0])
        matched["_resolverMatchedFrom"] = "target_document_index:global_text_exact"
        return matched

    return None


def _synthetic_paragraph_payload(paragraph_ordinal: Optional[int], *, reason: str) -> Dict[str, Any]:
    synthetic_id = f"paragraph:{int(paragraph_ordinal or 0):04d}" if paragraph_ordinal else None
    return {
        "paragraphId": synthetic_id,
        "nodeId": synthetic_id,
        "presentationNodeId": synthetic_id,
        "presentationKind": "synthetic_paragraph",
        "paragraphIndex": None,
        "xmlParagraphIndex": None,
        "reviewParagraphIndex": paragraph_ordinal,
        "chapterParagraphIndex": None,
        "resolverMatchedFrom": reason,
    }


def _paragraph_node_payload(
    index: Optional[TargetDocumentIndex],
    record: Any,
    *,
    chapter_title: str,
    raw_section_path: str,
) -> Dict[str, Any]:
    paragraph_ordinal = getattr(record, "paragraph_index_in_document", None)
    if index is None:
        return _synthetic_paragraph_payload(paragraph_ordinal, reason="no_target_document_index")

    node = _resolve_review_main_node(
        index,
        source_zone=str(getattr(record, "source_zone", "") or ""),
        chapter_title=chapter_title,
        raw_section_path=raw_section_path,
        paragraph_text=str(getattr(record, "text", "") or ""),
    )
    if not node:
        return _synthetic_paragraph_payload(paragraph_ordinal, reason="unresolved_body_text")

    return {
        "paragraphId": node.get("node_id") or f"paragraph:{int(paragraph_ordinal or 0):04d}",
        "nodeId": node.get("node_id"),
        "presentationNodeId": node.get("presentation_node_id") or node.get("node_id"),
        "presentationKind": node.get("presentation_kind"),
        "paragraphIndex": node.get("index"),
        "xmlParagraphIndex": node.get("xml_paragraph_index"),
        "reviewParagraphIndex": node.get("review_paragraph_index"),
        "chapterParagraphIndex": node.get("review_paragraph_index_in_chapter"),
        "resolverMatchedFrom": node.get("_resolverMatchedFrom") or "target_document_index",
    }


def _physical_position_payload(
    record: Any,
    *,
    chapter_title: str,
    section_path: str,
    outline_by_path: Dict[str, Dict[str, Any]],
    physical_paragraph: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    parts = [part.strip() for part in section_path.split(" > ") if part.strip()]
    chapter_path = parts[0] if parts else chapter_title
    level2_path = " > ".join(parts[:2]) if len(parts) >= 2 else ""
    level3_path = " > ".join(parts[:3]) if len(parts) >= 3 else ""

    chapter_no, chapter_name = _parse_heading_parts(chapter_title, 1)
    level2_number = ""
    level2_title = ""
    level3_number = ""
    level3_title = ""
    if len(parts) >= 2:
        level2_number, level2_title = _parse_heading_parts(parts[1], 2)
    if len(parts) >= 3:
        level3_number, level3_title = _parse_heading_parts(parts[2], 3)

    chapter_node = outline_by_path.get(chapter_path)
    level2_node = outline_by_path.get(level2_path) if level2_path else None
    level3_node = outline_by_path.get(level3_path) if level3_path else None

    return {
        "chapter": {
            "id": chapter_node.get("id") if isinstance(chapter_node, dict) else None,
            "number": chapter_no,
            "title": chapter_name,
        },
        "level2": {
            "id": level2_node.get("id") if isinstance(level2_node, dict) else None,
            "number": level2_number,
            "title": level2_title,
        },
        "level3": {
            "id": level3_node.get("id") if isinstance(level3_node, dict) else None,
            "number": level3_number,
            "title": level3_title,
        },
        "sectionPath": section_path,
        "pathKey": _path_key(section_path, getattr(record, "paragraph_index_in_section", None)),
        "paragraphOrdinalInDocument": (
            (physical_paragraph or {}).get("reviewParagraphIndex")
            or getattr(record, "paragraph_index_in_document", None)
        ),
        "paragraphOrdinalInChapter": (
            (physical_paragraph or {}).get("chapterParagraphIndex")
            or getattr(record, "paragraph_index_in_chapter", None)
        ),
        "paragraphOrdinalInSection": getattr(record, "paragraph_index_in_section", None),
    }


def build_structure_anchor_report(
    target_path: Path,
    format_spec_path: Optional[Path] = None,
    llm_config: Optional[Dict[str, Any]] = None,
    chapter_scope: Optional[List[int] | str] = None,
) -> Dict[str, Any]:
    normalized_scope = normalize_chapter_scope(chapter_scope)
    blocks, extraction_meta = parse_blocks_with_meta(target_path)
    full_snippet = "\n".join((getattr(block, "text", None) or "") for block in blocks[:80])
    strict_chapters = _build_strict_chapters(blocks)
    front_outline_nodes = _load_docx_outline_markers(target_path)
    if not strict_chapters:
        raise ValueError("failed to extract strict body structure from target document")

    parsed = ParsedDocument(
        path=str(target_path),
        title=detect_title(full_snippet, target_path.stem),
        author=detect_author(full_snippet),
        blocks=blocks,
        chapters=strict_chapters,
        extractionRisks=[],
        extractionMeta=extraction_meta,
    )

    heading_rules = _load_heading_rules(format_spec_path)
    outline, _section_number_map, normalized_path_map = _build_outline(
        strict_chapters,
        front_outline_nodes=front_outline_nodes,
    )
    outline_by_path = _outline_index(outline)
    document_index = TargetDocumentIndex.from_docx(target_path) if target_path.suffix.lower() == ".docx" else None
    paragraph_records = [
        record
        for record in enumerate_document_paragraphs(parsed)
        if chapter_in_scope(getattr(record, "chapter_number", None), normalized_scope)
    ]
    if not paragraph_records:
        raise ValueError(f"no paragraphs matched chapter scope: {chapter_scope_label(normalized_scope)}")

    paragraphs: List[Dict[str, Any]] = []
    for index, record in enumerate(paragraph_records, start=1):
        position_anchor_type, position_reason = _infer_position_anchor(record)
        position_spec = _anchor_spec(position_anchor_type)
        chapter_title = str(getattr(record, "chapter", "") or "")
        heading_number = str(getattr(record, "heading_number", "") or "")
        heading_title = str(getattr(record, "heading_title", "") or "")
        raw_section_path = str(getattr(record, "section_path", "") or chapter_title)
        section_path = normalized_path_map.get(raw_section_path, raw_section_path)
        physical_paragraph = _paragraph_node_payload(
            document_index,
            record,
            chapter_title=chapter_title,
            raw_section_path=raw_section_path,
        )
        physical_position = _physical_position_payload(
            record,
            chapter_title=chapter_title,
            section_path=section_path,
            outline_by_path=outline_by_path,
            physical_paragraph=physical_paragraph,
        )

        paragraphs.append(
            {
                "id": f"paragraph-{index:04d}",
                "paragraphId": physical_paragraph.get("paragraphId"),
                "sourceZone": getattr(record, "source_zone", ""),
                "chapterNumber": getattr(record, "chapter_number", None),
                "chapterTitle": chapter_title,
                "sectionPath": section_path,
                "paragraphIndexInDocument": physical_position.get("paragraphOrdinalInDocument"),
                "paragraphIndexInChapter": physical_position.get("paragraphOrdinalInChapter"),
                "paragraphIndexInSection": getattr(record, "paragraph_index_in_section", None),
                "physicalParagraph": physical_paragraph,
                "physicalPosition": physical_position,
                "headingContext": {
                    "activeHeadingLevel": getattr(record, "heading_level", None),
                    "activeHeadingNumber": heading_number,
                    "activeHeadingTitle": heading_title,
                },
                "positionAnchor": {
                    "type": position_spec.anchor_type,
                    "label": position_spec.label,
                    "description": position_spec.description,
                    "reason": position_reason,
                    "specificity": position_spec.specificity,
                },
                "positionLocator": physical_position,
                "textExcerpt": _text_excerpt(getattr(record, "text", "")),
                "text": getattr(record, "text", ""),
                "textHash": _text_hash(getattr(record, "text", "")),
            }
        )

    section_classifications = classify_section_packages(paragraphs, llm_config=llm_config)
    paragraph_function_index = build_section_function_index(section_classifications)
    for paragraph in paragraphs:
        paragraph_id = str(paragraph.get("paragraphId") or "").strip()
        function_info = paragraph_function_index.get(paragraph_id)
        if not function_info:
            raise ValueError(f"missing LLM paragraph function assignment for {paragraph_id}")
        paragraph_type = str(function_info.get("paragraphType") or "").strip()
        paragraph["functionalType"] = {
            "paragraphType": paragraph_type,
            "classifierModule": "classifiers.section_function_classifier",
            "classifierMode": "llm-section-package",
            "classifierVersion": "section-function-v1",
            "confidence": function_info.get("confidence"),
            "rationale": function_info.get("rationale"),
        }
        paragraph["styleLearningBucket"] = paragraph_type
        paragraph["styleLearningBucketSource"] = "llm-section-package"
        paragraph["sectionExpansion"] = {
            "pattern": function_info.get("sectionExpansionPattern"),
            "rationale": function_info.get("sectionExpansionRationale"),
            "packageId": function_info.get("packageId"),
        }
        paragraph["responsibilityHint"] = {
            "paragraphType": paragraph_type,
            "pattern": function_info.get("sectionExpansionPattern"),
        }

    bucket_summary = _build_learning_bucket_summary(paragraphs)
    filtered_outline = filter_outline_by_chapter_scope(outline, normalized_scope)
    report = {
        "meta": {
            "module": "paper_structure_anchor",
            "version": "4.1-canonical-node-resolution",
            "method": "strict heading detection -> outline -> target_document_index canonical body-node resolution -> section-packaged llm paragraph function classification -> unified structure map",
            "targetPath": str(target_path),
            "formatSpecPath": str(format_spec_path) if format_spec_path else None,
            "formatRulesSource": heading_rules.get("source"),
            "chapterScope": list(normalized_scope) if normalized_scope is not None else None,
            "chapterScopeLabel": chapter_scope_label(normalized_scope),
            "paragraphCount": len(paragraphs),
            "sectionClassificationCount": len(section_classifications),
            "outlineNodeCount": len(filtered_outline),
            "frontMatterNodeCount": len(front_outline_nodes),
            "executionModel": {
                "structureAnchor": "code",
                "paragraphClassifier": "llm",
                "llmUsed": True,
            },
            "extractionDiagnostics": parsed.extractionMeta,
            "notes": [
                "一级标题只接受严格章标题：第X章 + 标题，不再把“第一章为……”这类正文句子识别成标题。",
                "二级、三级标题优先使用 Word 标题样式；无样式时再回退到严格编号规则。",
                "DOCX 前置部分会补抓摘要、Abstract、目录等一级标题，并给出页序号估计。",
                "所有正文段落先按物理结构切成互斥 section packages，再由 LLM 对每个 package 做一次展开模式和逐段身份分类，保证正文只被 LLM 读一遍。",
                "统一输出同时包含物理段落身份、结构位置、section 展开模式与最终段落身份，供风格学习、风格评价、批注定位共用。",
            ],
        },
        "headingRules": heading_rules.get("headings", {}),
        "outline": filtered_outline,
        "sectionClassifications": section_classifications,
        "bucketSummary": bucket_summary,
        "paragraphs": paragraphs,
    }
    return report


def build_paper_structure_map(
    target_path: Path,
    format_spec_path: Optional[Path] = None,
    llm_config: Optional[Dict[str, Any]] = None,
    chapter_scope: Optional[List[int] | str] = None,
) -> Dict[str, Any]:
    """统一结构图谱公共入口。"""
    return build_structure_anchor_report(
        target_path,
        format_spec_path=format_spec_path,
        llm_config=llm_config,
        chapter_scope=chapter_scope,
    )


def _load_llm_config(path: Optional[Path]) -> Optional[Dict[str, Any]]:
    if path is None:
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"llm config must be a JSON object: {path}")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Export unified paper structure map for style learning, style review and annotation")
    parser.add_argument("--target", required=True, help="Path to thesis document")
    parser.add_argument("--format-spec", help="Path to format spec document or extracted format-rules.json")
    parser.add_argument("--llm-config", help="Optional JSON file for section function classifier LLM settings")
    parser.add_argument("--chapters", help="Optional chapter scope, e.g. abstract,1,2")
    parser.add_argument("--output", required=True, help="Path to write structure-anchor-report.json")
    args = parser.parse_args()

    target_path = Path(args.target).expanduser().resolve()
    format_spec_path = Path(args.format_spec).expanduser().resolve() if args.format_spec else None
    llm_config_path = Path(args.llm_config).expanduser().resolve() if args.llm_config else None
    llm_config = _load_llm_config(llm_config_path)
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = build_paper_structure_map(
        target_path,
        format_spec_path=format_spec_path,
        llm_config=llm_config,
        chapter_scope=args.chapters,
    )
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output_path),
                "paragraphCount": report["meta"]["paragraphCount"],
                "outlineNodeCount": report["meta"]["outlineNodeCount"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
