#!/usr/bin/env python3
"""统一的目标文档索引。

目标：
- 让 annotation 组装层和 Word 注入层共享同一套节点标识；
- 消除 body/xml 两套段落索引被混用导致的漂移；
- 为 proxy 类问题显式区分“问题对象”和“实际挂注位置”。
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from docx import Document
from lxml import etree
from word_text_surface import get_paragraph_visible_text

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
REVIEWABLE_MAIN_ZONES = {"abstract_cn", "abstract_en", "body"}


def make_body_node_id(paragraph_index: Optional[int]) -> Optional[str]:
    if paragraph_index is None:
        return None
    return f"body:{int(paragraph_index)}"


def make_table_cell_node_id(
    table_index: Optional[int],
    row_index: Optional[int],
    column_index: Optional[int],
    cell_paragraph_index: Optional[int],
) -> Optional[str]:
    if None in (table_index, row_index, column_index, cell_paragraph_index):
        return None
    return f"table:{int(table_index)}:{int(row_index)}:{int(column_index)}:{int(cell_paragraph_index)}"


def make_section_proxy_node_id(section_index: Optional[int]) -> Optional[str]:
    if section_index is None:
        return None
    return f"section-proxy:{int(section_index)}"


def make_header_proxy_node_id(section_index: Optional[int], header_part: Optional[str]) -> Optional[str]:
    if section_index is None:
        return None
    part = (header_part or "__missing_header__").strip() or "__missing_header__"
    return f"header-proxy:{int(section_index)}:{part}"


def make_footer_proxy_node_id(section_index: Optional[int], footer_part: Optional[str]) -> Optional[str]:
    if section_index is None:
        return None
    part = (footer_part or "__missing_footer__").strip() or "__missing_footer__"
    return f"footer-proxy:{int(section_index)}:{part}"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class TargetDocumentIndex:
    """基于 DOCX 构建统一节点视图。

    `body_nodes` 保留既有字段名，但语义上表示“主文档段落节点”：
    包含 front matter / 摘要 / 正文 / 参考文献等位于 docx body 中的主段落，
    让上游结构图谱和下游批注都使用同一套 canonical node id。
    `review_paragraph_nodes` 只保留真正参与语义审查的主文档正文段：
    当前包含中文摘要、英文摘要和正文。
    """

    def __init__(self) -> None:
        self.body_nodes: List[Dict[str, Any]] = []
        self.review_paragraph_nodes: List[Dict[str, Any]] = []
        self.table_cell_nodes: List[Dict[str, Any]] = []
        self.proxy_nodes: List[Dict[str, Any]] = []
        self.xml_paragraphs: List[Dict[str, Any]] = []
        self.path_buckets: Dict[Tuple[str, ...], List[Dict[str, Any]]] = defaultdict(list)
        self.review_path_buckets: Dict[Tuple[str, ...], List[Dict[str, Any]]] = defaultdict(list)
        self.table_cell_by_location: Dict[str, Dict[str, Any]] = {}
        self.node_by_id: Dict[str, Dict[str, Any]] = {}
        self.review_paragraph_by_global_index: Dict[int, Dict[str, Any]] = {}
        self.review_paragraphs_by_chapter: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._looks_like_chapter_heading = None

    @classmethod
    def from_docx(cls, path: Path) -> "TargetDocumentIndex":
        from detectors.format_checker import (  # type: ignore
            _build_part_proxy_maps,
            _build_section_proxy_paragraphs,
            _build_section_start_map,
            _collect_main_paragraphs,
            _collect_table_cell_paragraphs,
            _looks_like_chapter_heading,
        )

        index = cls()
        index._looks_like_chapter_heading = _looks_like_chapter_heading

        document = Document(str(path))
        main_infos = _collect_main_paragraphs(document)
        current_headings: Dict[int, Optional[str]] = {1: None, 2: None, 3: None, 4: None}
        review_global_index = 0
        review_index_by_chapter: Dict[str, int] = defaultdict(int)

        for info in main_infos:
            raw_text = get_paragraph_visible_text(info.raw_paragraph._element) if info.raw_paragraph is not None else (info.text or "")
            text = raw_text.strip()
            if not text or info.paragraph_type == "table_cell":
                continue
            if info.paragraph_type.startswith("heading") and info.heading_level:
                level = int(info.heading_level)
                current_headings[level] = text
                for key in [k for k in current_headings if k > level]:
                    current_headings[key] = None
            path_tuple = tuple(value for _, value in sorted(current_headings.items()) if value)
            node = {
                "node_id": make_body_node_id(info.index),
                "kind": "body_paragraph",
                "index": info.index,
                "xml_paragraph_index": info.xml_paragraph_index,
                "section_index": info.section_index,
                "location": info.location,
                "text": raw_text,
                "path": path_tuple,
                "paragraph_type": info.paragraph_type,
                "zone": info.zone,
                "presentation_node_id": make_body_node_id(info.index),
                "presentation_kind": "body_paragraph",
            }
            index.body_nodes.append(node)
            if node["node_id"]:
                index.node_by_id[node["node_id"]] = node
            for size in range(1, len(path_tuple) + 1):
                index.path_buckets[path_tuple[:size]].append(node)
            if not str(info.paragraph_type).startswith("heading") and str(info.zone) in REVIEWABLE_MAIN_ZONES:
                review_global_index += 1
                chapter_title = path_tuple[0] if path_tuple else ""
                review_index_by_chapter[chapter_title] += 1
                node["review_paragraph_index"] = review_global_index
                node["review_paragraph_index_in_chapter"] = review_index_by_chapter[chapter_title]
                node["chapter_title"] = chapter_title
                index.review_paragraph_nodes.append(node)
                index.review_paragraph_by_global_index[review_global_index] = node
                if chapter_title:
                    index.review_paragraphs_by_chapter[chapter_title].append(node)
                for size in range(1, len(path_tuple) + 1):
                    index.review_path_buckets[path_tuple[:size]].append(node)

        for info in _collect_table_cell_paragraphs(document):
            raw_text = get_paragraph_visible_text(info.raw_paragraph._element) if info.raw_paragraph is not None else (info.text or "")
            text = raw_text.strip()
            if not text:
                continue
            node = {
                "node_id": make_table_cell_node_id(info.table_index, info.row_index, info.column_index, info.cell_paragraph_index),
                "kind": "table_cell",
                "location": info.location,
                "text": raw_text,
                "xml_paragraph_index": info.xml_paragraph_index,
                "table_index": info.table_index,
                "row_index": info.row_index,
                "column_index": info.column_index,
                "cell_paragraph_index": info.cell_paragraph_index,
                "presentation_node_id": make_table_cell_node_id(info.table_index, info.row_index, info.column_index, info.cell_paragraph_index),
                "presentation_kind": "table_cell",
            }
            index.table_cell_nodes.append(node)
            if node["node_id"]:
                index.node_by_id[node["node_id"]] = node
            index.table_cell_by_location[node["location"]] = node

        section_starts = _build_section_start_map(document)
        section_proxies = _build_section_proxy_paragraphs(main_infos, section_starts)
        for section_index, proxy in sorted(section_proxies.items()):
            presentation_node_id = make_body_node_id(proxy.index)
            node = {
                "node_id": make_section_proxy_node_id(section_index),
                "kind": "section_proxy",
                "section_index": section_index,
                "proxy_paragraph_index": proxy.index,
                "proxy_xml_paragraph_index": proxy.xml_paragraph_index,
                "proxy_location": proxy.location,
                "proxy_text": (proxy.text or "").strip()[:120],
                "presentation_node_id": presentation_node_id,
                "presentation_kind": "body_paragraph",
            }
            if node["node_id"]:
                index.proxy_nodes.append(node)
                index.node_by_id[node["node_id"]] = node

        header_map, footer_map = _build_part_proxy_maps(path, section_starts)
        for header_part, section_index in sorted(header_map.items()):
            proxy = section_proxies.get(section_index)
            if not proxy:
                continue
            presentation_node_id = make_body_node_id(proxy.index)
            node = {
                "node_id": make_header_proxy_node_id(section_index, header_part),
                "kind": "header_proxy",
                "section_index": section_index,
                "header_part": header_part,
                "proxy_paragraph_index": proxy.index,
                "proxy_xml_paragraph_index": proxy.xml_paragraph_index,
                "proxy_location": proxy.location,
                "proxy_text": (proxy.text or "").strip()[:120],
                "presentation_node_id": presentation_node_id,
                "presentation_kind": "body_paragraph",
            }
            if node["node_id"]:
                index.proxy_nodes.append(node)
                index.node_by_id[node["node_id"]] = node

        for footer_part, section_index in sorted(footer_map.items()):
            proxy = section_proxies.get(section_index)
            if not proxy:
                continue
            presentation_node_id = make_body_node_id(proxy.index)
            node = {
                "node_id": make_footer_proxy_node_id(section_index, footer_part),
                "kind": "footer_proxy",
                "section_index": section_index,
                "footer_part": footer_part,
                "proxy_paragraph_index": proxy.index,
                "proxy_xml_paragraph_index": proxy.xml_paragraph_index,
                "proxy_location": proxy.location,
                "proxy_text": (proxy.text or "").strip()[:120],
                "presentation_node_id": presentation_node_id,
                "presentation_kind": "body_paragraph",
            }
            if node["node_id"]:
                index.proxy_nodes.append(node)
                index.node_by_id[node["node_id"]] = node

        for xml_idx, paragraph in enumerate(document._body._element.iter(f"{{{W_NS}}}p"), start=1):
            raw_text = get_paragraph_visible_text(paragraph)
            if raw_text.strip():
                index.xml_paragraphs.append({
                    "xml_paragraph_index": xml_idx,
                    "text": raw_text,
                })

        return index

    def candidate_body_nodes(self, path_parts: Optional[List[str]]) -> List[Dict[str, Any]]:
        if not path_parts:
            return self.body_nodes
        key = tuple(path_parts)
        if key in self.path_buckets:
            return self.path_buckets[key]
        normalized_key = tuple(self.normalize_text(part) for part in key)
        for bucket_path, bucket in self.path_buckets.items():
            if tuple(self.normalize_text(part) for part in bucket_path) == normalized_key:
                return bucket
        subsequence_hits = [
            node
            for node in self.body_nodes
            if self._is_path_subsequence(normalized_key, tuple(self.normalize_text(part) for part in (node.get("path") or ())))
        ]
        if subsequence_hits:
            return subsequence_hits
        return []

    def candidate_review_nodes(self, path_parts: Optional[List[str]]) -> List[Dict[str, Any]]:
        if not path_parts:
            return self.review_paragraph_nodes
        key = tuple(path_parts)
        if key in self.review_path_buckets:
            return self.review_path_buckets[key]
        normalized_key = tuple(self.normalize_text(part) for part in key)
        for bucket_path, bucket in self.review_path_buckets.items():
            if tuple(self.normalize_text(part) for part in bucket_path) == normalized_key:
                return bucket
        subsequence_hits = [
            node
            for node in self.review_paragraph_nodes
            if self._is_path_subsequence(normalized_key, tuple(self.normalize_text(part) for part in (node.get("path") or ())))
        ]
        if subsequence_hits:
            return subsequence_hits
        return []

    @staticmethod
    def normalize_text(text: str) -> str:
        return (
            "".join(ch for ch in (text or "") if not ch.isspace())
            .replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
            .replace("「", '"')
            .replace("」", '"')
        )

    def looks_like_heading(self, text: str) -> bool:
        if not text:
            return False
        checker = self._looks_like_chapter_heading
        return bool(checker and checker((text or "").strip()))

    @staticmethod
    def _is_path_subsequence(expected: Tuple[str, ...], actual: Tuple[str, ...]) -> bool:
        if not expected:
            return True
        pos = 0
        for part in actual:
            if pos < len(expected) and part == expected[pos]:
                pos += 1
        return pos == len(expected)


def build_xml_paragraph_locator(body: Optional[etree._Element]) -> Tuple[List[etree._Element], Dict[str, Dict[str, Any]]]:
    if body is None:
        return [], {}

    ordered_paragraphs = list(body.iter(f"{{{W_NS}}}p"))
    order_index_by_element = {id(paragraph): idx for idx, paragraph in enumerate(ordered_paragraphs)}
    targets: Dict[str, Dict[str, Any]] = {}

    body_index = 0
    table_index = 0
    for child in body.iterchildren():
        tag = _local_name(child.tag)
        if tag == "p":
            body_index += 1
            node_id = make_body_node_id(body_index)
            if node_id:
                targets[node_id] = {
                    "element": child,
                    "order_index": order_index_by_element[id(child)],
                    "kind": "body_paragraph",
                }
            continue
        if tag != "tbl":
            continue
        table_index += 1
        rows = child.findall("w:tr", NS)
        for row_idx, row in enumerate(rows, start=1):
            cells = row.findall("w:tc", NS)
            for col_idx, cell in enumerate(cells, start=1):
                para_idx = 0
                for cell_child in cell.iterchildren():
                    if _local_name(cell_child.tag) != "p":
                        continue
                    para_idx += 1
                    node_id = make_table_cell_node_id(table_index, row_idx, col_idx, para_idx)
                    if node_id:
                        targets[node_id] = {
                            "element": cell_child,
                            "order_index": order_index_by_element[id(cell_child)],
                            "kind": "table_cell",
                        }

    return ordered_paragraphs, targets
