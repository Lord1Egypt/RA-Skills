#!/usr/bin/env python3
"""统一批注锚点基础设施。

职责：
- 将 legacy location/source_text 升级为稳定的结构化锚点；
- 对可做词/短语级挂注的问题，提前固化 paragraph + span offsets；
- 让 orchestrator / annotation_assembler / inject_word_comments 共用同一套解析契约。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from contracts import ANCHOR_CONTRACT_VERSION, AnchorKind, SourceType, normalize_anchor_dict, normalize_anchor_text
from target_document_index import (
    TargetDocumentIndex,
    make_body_node_id,
    make_footer_proxy_node_id,
    make_header_proxy_node_id,
    make_section_proxy_node_id,
    make_table_cell_node_id,
)

STYLE_DEVIATION_FILENAME = "style-deviation-report.json"
FORMAT_ANCHOR_V2_FILENAME = "format-review-report.format-anchor-v2.json"
STRUCTURED_ANCHOR_REPORTS = {
    "format-review-report.json": SourceType.FORMAT.value,
    "terminology-review-report.json": SourceType.TERMINOLOGY.value,
    "logic-review-report.json": SourceType.LOGIC.value,
    STYLE_DEVIATION_FILENAME: SourceType.STYLE_DEVIATION.value,
}
SPAN_PREFERRED_SOURCES = {
    SourceType.FORMAT.value,
    SourceType.TERMINOLOGY.value,
    SourceType.STYLE_DEVIATION.value,
}


def infer_target_path(output_dir: Path) -> Optional[Path]:
    summary_path = output_dir / "run-summary.json"
    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            target_path = ((summary.get("target") or {}).get("path") or "").strip()
            if target_path:
                path = Path(target_path)
                if path.exists():
                    return path
        except Exception:
            pass
    workspace_doc = output_dir.parents[2] / "论文修改版.docx"
    if workspace_doc.exists():
        return workspace_doc
    return None


class AnchorInfrastructure:
    """统一解析 paragraph anchor 和 span anchor。"""

    def __init__(self, target_path: Path):
        self.target_path = target_path
        self.index = TargetDocumentIndex.from_docx(target_path)
        self.body_nodes = list(self.index.body_nodes)
        self.review_nodes = list(self.index.review_paragraph_nodes)
        self.table_cells = list(self.index.table_cell_nodes)
        self.table_cell_by_location = self.index.table_cell_by_location
        self.xml_paragraphs = list(self.index.xml_paragraphs)
        self.known_heading_labels = {
            self.index.normalize_text(part)
            for node in self.body_nodes
            for part in (node.get("path") or ())
            if self.index.normalize_text(part)
        }

    @staticmethod
    def _ordered_contains(text: str, fragments: List[str]) -> bool:
        pos = 0
        for fragment in fragments:
            next_pos = text.find(fragment, pos)
            if next_pos < 0:
                return False
            pos = next_pos + len(fragment)
        return True

    @staticmethod
    def _ellipsis_fragments(text: str) -> List[str]:
        return [normalize_anchor_text(part) for part in re.split(r"(?:…+|\.{3,})", text or "") if normalize_anchor_text(part)]

    @staticmethod
    def _attach_fragments(text: str) -> List[str]:
        pieces = []
        for part in re.split(r"(?:…+|\.{3,}|\[[^\]]+\]|[，,。；;：:（）()、])", text or ""):
            stripped = (part or "").strip()
            if stripped:
                pieces.append(stripped)
        pieces.sort(key=len, reverse=True)
        return pieces

    def _is_heading_like(self, text: str) -> bool:
        stripped = (text or "").strip()
        if not stripped:
            return False
        if self.index.normalize_text(stripped) in self.known_heading_labels:
            return True
        if len(stripped) > 60 or re.search(r"[。！？；;：:，,]", stripped):
            return False
        if self.index.looks_like_heading(stripped):
            return True
        return any(
            re.match(pattern, stripped)
            for pattern in [
                r"^第[一二三四五六七八九十百零〇\d]+章\s*\S+",
                r"^第[一二三四五六七八九十百零〇\d]+节\s*\S+",
                r"^\d+(?:\.\d+){0,3}\s*\S+",
                r"^[一二三四五六七八九十]+、\S+",
            ]
        )

    def _parse_location_hint(self, location_hint: str) -> Tuple[Optional[List[str]], Optional[int], Optional[int], Optional[str]]:
        hint = (location_hint or "").strip()
        if not hint:
            return None, None, None, None
        wrapped = re.match(r"^第\s*(\d+)\s*段（(.+)）$", hint)
        if wrapped:
            inner = wrapped.group(2)
            inner_parts = [part.strip() for part in inner.split(">") if part.strip()]
            global_ordinal = int(wrapped.group(1))
            return inner_parts or None, None, global_ordinal, None
        parts = [part.strip() for part in hint.split(">") if part.strip()]
        path_ordinal = None
        if parts:
            tail_match = re.match(r"^第\s*(\d+)\s*段$", parts[-1])
            if tail_match:
                path_ordinal = int(tail_match.group(1))
                parts = parts[:-1]
        if len(parts) >= 2:
            return parts, path_ordinal, None, None
        if parts and self._is_heading_like(parts[0]):
            return parts, path_ordinal, None, None
        if self._is_heading_like(hint):
            return [hint], None, None, None
        return None, None, None, hint

    def _match_text(self, candidates: List[Dict[str, Any]], text: str, *, allow_short_substring: bool = False) -> List[Dict[str, Any]]:
        normalized = normalize_anchor_text(text)
        if not normalized:
            return []
        fragments = self._ellipsis_fragments(text)
        matched: List[Dict[str, Any]] = []
        for candidate in candidates:
            candidate_norm = normalize_anchor_text(candidate.get("text", ""))
            if not candidate_norm:
                continue
            ok = False
            if candidate_norm == normalized:
                ok = True
            elif (allow_short_substring or len(normalized) > 6) and normalized in candidate_norm:
                ok = True
            elif len(candidate_norm) > 20 and candidate_norm in normalized:
                ok = True
            elif len(fragments) >= 2 and self._ordered_contains(candidate_norm, fragments):
                ok = True
            if ok:
                matched.append(candidate)
        return matched

    @staticmethod
    def _prefer_non_heading_hits(hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        non_heading_hits = [hit for hit in hits if not str(hit.get("paragraph_type", "")).startswith("heading")]
        return non_heading_hits or hits

    def _attach_text_candidates(self, paragraph_text: str, item: Dict[str, Any]) -> List[Tuple[str, str]]:
        source = str(item.get("source", "") or "")
        if source == SourceType.LOGIC.value:
            return []

        prioritized_values: List[Tuple[str, Any, bool]] = []
        if source == SourceType.STYLE_DEVIATION.value:
            prioritized_values.extend([
                ("focus_text", item.get("focus_text") or item.get("focusText"), False),
                ("sentence_text", item.get("sentence_text") or item.get("sentenceText"), False),
                ("source_text", item.get("source_text") or item.get("sourceText"), False),
            ])
        else:
            prioritized_values.extend([
                ("term_issue", item.get("term_issue") or item.get("termIssue"), True),
                ("source_text", item.get("source_text") or item.get("sourceText"), False),
            ])

        candidates: List[Tuple[str, str]] = []
        seen = set()
        for source_key, value, allow_short in prioritized_values:
            if not isinstance(value, str) or not value.strip():
                continue
            if value in paragraph_text and len(value.strip()) <= 80:
                candidate = (value.strip(), source_key)
                if candidate[0] not in seen:
                    candidates.append(candidate)
                    seen.add(candidate[0])
                continue
            for fragment in self._attach_fragments(value):
                if len(fragment) <= 80 and fragment in paragraph_text:
                    if fragment not in seen:
                        candidates.append((fragment, source_key))
                        seen.add(fragment)
                    break
                if allow_short and normalize_anchor_text(fragment) and normalize_anchor_text(fragment) in normalize_anchor_text(paragraph_text):
                    if fragment not in seen:
                        candidates.append((fragment, source_key))
                        seen.add(fragment)
                    break
        anchor = item.get("anchor") if isinstance(item.get("anchor"), dict) else {}
        existing_attach = anchor.get("attach_text")
        if isinstance(existing_attach, str) and existing_attach.strip():
            candidate = existing_attach.strip()
            if candidate not in seen:
                candidates.append((candidate, "existing_anchor"))
        return candidates

    @staticmethod
    def _normalized_text_with_raw_offsets(text: str) -> Tuple[str, List[int]]:
        normalized_chars: List[str] = []
        raw_offsets: List[int] = []
        for raw_idx, ch in enumerate(text or ""):
            mapped = ch
            if ch.isspace():
                mapped = ""
            elif ch in {"“", "”", "「", "」"}:
                mapped = '"'
            elif ch in {"‘", "’"}:
                mapped = "'"
            if not mapped:
                continue
            normalized_chars.append(mapped)
            raw_offsets.append(raw_idx)
        return "".join(normalized_chars), raw_offsets

    def _find_span_offsets(self, paragraph_text: str, attach_text: str) -> Optional[Tuple[int, int]]:
        if not paragraph_text or not attach_text:
            return None
        if normalize_anchor_text(attach_text) == normalize_anchor_text(paragraph_text):
            return None
        literal_start = paragraph_text.find(attach_text)
        if literal_start >= 0:
            return literal_start, literal_start + len(attach_text)

        paragraph_norm, paragraph_offsets = self._normalized_text_with_raw_offsets(paragraph_text)
        anchor_norm, _ = self._normalized_text_with_raw_offsets(attach_text)
        if not paragraph_norm or not anchor_norm:
            return None
        norm_start = paragraph_norm.find(anchor_norm)
        if norm_start < 0:
            return None
        if paragraph_norm.find(anchor_norm, norm_start + 1) >= 0:
            return None
        norm_end = norm_start + len(anchor_norm) - 1
        raw_start = paragraph_offsets[norm_start]
        raw_end = paragraph_offsets[norm_end] + 1
        return raw_start, raw_end

    def _finalize_anchor(self, anchor: Dict[str, Any], item: Dict[str, Any], paragraph_text: Optional[str]) -> Dict[str, Any]:
        payload = dict(anchor)
        payload.pop("start_offset", None)
        payload.pop("end_offset", None)
        payload.pop("selection_mode", None)
        source = str(item.get("source", "") or "")
        attach_candidates = self._attach_text_candidates(paragraph_text or "", item)
        if attach_candidates:
            payload["attach_text"] = attach_candidates[0][0]
            payload["attach_text_source"] = attach_candidates[0][1]
        selection_mode = "paragraph"
        if source in SPAN_PREFERRED_SOURCES and paragraph_text and attach_candidates:
            for attach_text, attach_text_source in attach_candidates:
                span = self._find_span_offsets(paragraph_text, attach_text)
                if span is None:
                    continue
                payload["attach_text"] = attach_text
                payload["attach_text_source"] = attach_text_source
                payload["start_offset"] = span[0]
                payload["end_offset"] = span[1]
                selection_mode = "span"
                break
        payload["selection_mode"] = selection_mode
        payload["resolver"] = "annotation_anchor_infra"
        payload["contract_version"] = ANCHOR_CONTRACT_VERSION
        return normalize_anchor_dict(payload) or {}

    def _build_body_anchor(self, node: Dict[str, Any], item: Dict[str, Any], matched_from: str) -> Dict[str, Any]:
        anchor = {
            "kind": AnchorKind.BODY_PARAGRAPH.value,
            "node_id": node.get("node_id"),
            "presentation_kind": node.get("presentation_kind") or AnchorKind.BODY_PARAGRAPH.value,
            "presentation_node_id": node.get("presentation_node_id") or node.get("node_id"),
            "paragraph_index": node.get("index"),
            "xml_paragraph_index": node.get("xml_paragraph_index"),
            "section_index": node.get("section_index"),
            "zone": node.get("zone"),
            "paragraph_type": node.get("paragraph_type"),
            "location": node.get("location"),
            "section_path": list(node.get("path") or []),
            "section_path_text": " > ".join(node.get("path") or []),
            "matched_from": matched_from,
        }
        return self._finalize_anchor(anchor, item, node.get("text"))

    @staticmethod
    def _anchor_path_parts(anchor: Dict[str, Any]) -> Optional[List[str]]:
        raw = anchor.get("section_path")
        if isinstance(raw, list):
            parts = [str(part).strip() for part in raw if str(part).strip()]
            return parts or None
        section_path_text = str(anchor.get("section_path_text") or "").strip()
        if section_path_text:
            parts = [part.strip() for part in section_path_text.split(">") if part.strip()]
            return parts or None
        return None

    @staticmethod
    def _anchor_location_hint(anchor: Dict[str, Any]) -> str:
        parts = AnchorInfrastructure._anchor_path_parts(anchor) or []
        ordinal = anchor.get("proxy_paragraph_index")
        if isinstance(ordinal, int) and ordinal > 0:
            parts = [*parts, f"第{ordinal}段"]
        return " > ".join(parts)

    def _resolve_body_anchor_from_item(
        self,
        item: Dict[str, Any],
        *,
        location_hint_override: str = "",
    ) -> Optional[Dict[str, Any]]:
        location_hint = location_hint_override or item.get("location_hint") or item.get("locationHint") or item.get("location") or ""
        source_text = item.get("source_text") or item.get("sourceText") or item.get("original") or ""
        term_issue = item.get("term_issue") or item.get("termIssue") or ""

        path_parts, path_ordinal, global_ordinal, context_text = self._parse_location_hint(str(location_hint or ""))

        if global_ordinal:
            node = self.index.review_paragraph_by_global_index.get(global_ordinal)
            if node:
                return self._build_body_anchor(node, item, "global_review_paragraph")

        candidates = self.index.candidate_review_nodes(path_parts)

        if context_text:
            hits = self._match_text(self.review_nodes, context_text)
            hits = self._prefer_non_heading_hits(hits)
            if len(hits) == 1:
                return self._build_body_anchor(hits[0], item, "context_text")

        for matched_from, text, allow_short in [
            ("source_text", source_text, False),
            ("term_issue", term_issue, True),
        ]:
            hits = self._match_text(candidates, text, allow_short_substring=allow_short)
            hits = self._prefer_non_heading_hits(hits)
            if len(hits) == 1:
                return self._build_body_anchor(hits[0], item, matched_from)
            if len(hits) > 1 and path_ordinal and 1 <= path_ordinal <= len(candidates):
                ordinal_target = candidates[path_ordinal - 1]
                if any(hit.get("review_paragraph_index") == ordinal_target.get("review_paragraph_index") for hit in hits):
                    return self._build_body_anchor(ordinal_target, item, f"{matched_from}+path_ordinal")

        if path_ordinal and candidates and 1 <= path_ordinal <= len(candidates):
            return self._build_body_anchor(candidates[path_ordinal - 1], item, "path_ordinal")
        return None

    def _upgrade_existing_anchor(self, anchor: Dict[str, Any], item: Dict[str, Any]) -> Dict[str, Any]:
        upgraded = dict(anchor)
        kind = str(upgraded.get("kind", "") or "")
        node = None
        if kind == AnchorKind.BODY_PARAGRAPH.value:
            node_id = upgraded.get("node_id") or make_body_node_id(upgraded.get("paragraph_index"))
            if node_id:
                upgraded.setdefault("node_id", node_id)
                upgraded.setdefault("presentation_kind", AnchorKind.BODY_PARAGRAPH.value)
                upgraded.setdefault("presentation_node_id", node_id)
                node = self.index.node_by_id.get(str(node_id))
            if not isinstance(node, dict):
                rebuilt = self._resolve_body_anchor_from_item(
                    item,
                    location_hint_override=self._anchor_location_hint(upgraded),
                )
                if rebuilt:
                    return rebuilt
        elif kind == AnchorKind.TABLE_CELL.value:
            node_id = upgraded.get("node_id") or make_table_cell_node_id(
                upgraded.get("table_index"),
                upgraded.get("row_index"),
                upgraded.get("column_index"),
                upgraded.get("cell_paragraph_index"),
            )
            if node_id:
                upgraded.setdefault("node_id", node_id)
                upgraded.setdefault("presentation_kind", AnchorKind.TABLE_CELL.value)
                upgraded.setdefault("presentation_node_id", node_id)
                node = self.index.node_by_id.get(str(node_id))
        elif kind == AnchorKind.SECTION_PROXY.value:
            node_id = upgraded.get("node_id") or make_section_proxy_node_id(upgraded.get("section_index"))
            presentation_node_id = upgraded.get("presentation_node_id") or make_body_node_id(upgraded.get("proxy_paragraph_index"))
            if node_id:
                upgraded.setdefault("node_id", node_id)
            if presentation_node_id:
                upgraded.setdefault("presentation_kind", AnchorKind.BODY_PARAGRAPH.value)
                upgraded.setdefault("presentation_node_id", presentation_node_id)
                node = self.index.node_by_id.get(str(presentation_node_id))
        elif kind == AnchorKind.HEADER_PROXY.value:
            node_id = upgraded.get("node_id") or make_header_proxy_node_id(upgraded.get("section_index"), upgraded.get("header_part"))
            presentation_node_id = upgraded.get("presentation_node_id") or make_body_node_id(upgraded.get("proxy_paragraph_index"))
            if node_id:
                upgraded.setdefault("node_id", node_id)
            if presentation_node_id:
                upgraded.setdefault("presentation_kind", AnchorKind.BODY_PARAGRAPH.value)
                upgraded.setdefault("presentation_node_id", presentation_node_id)
                node = self.index.node_by_id.get(str(presentation_node_id))
        elif kind == AnchorKind.FOOTER_PROXY.value:
            node_id = upgraded.get("node_id") or make_footer_proxy_node_id(upgraded.get("section_index"), upgraded.get("footer_part"))
            presentation_node_id = upgraded.get("presentation_node_id") or make_body_node_id(upgraded.get("proxy_paragraph_index"))
            if node_id:
                upgraded.setdefault("node_id", node_id)
            if presentation_node_id:
                upgraded.setdefault("presentation_kind", AnchorKind.BODY_PARAGRAPH.value)
                upgraded.setdefault("presentation_node_id", presentation_node_id)
                node = self.index.node_by_id.get(str(presentation_node_id))
        return self._finalize_anchor(upgraded, item, node.get("text") if isinstance(node, dict) else None)

    def _resolve_table_cell_anchor(self, item: Dict[str, Any], location_hint: str, source_text: str) -> Optional[Dict[str, Any]]:
        hint = (location_hint or "").strip()
        if not hint.startswith("表格"):
            return None
        cell = self.table_cell_by_location.get(hint)
        matched_from = "table_location" if cell else None
        if not cell and source_text:
            hits = self._match_text(self.table_cells, source_text, allow_short_substring=True)
            if len(hits) == 1:
                cell = hits[0]
                matched_from = "table_source_text"
        if not cell and source_text:
            normalized = normalize_anchor_text(source_text)
            exact_xml_hits = [paragraph for paragraph in self.xml_paragraphs if normalize_anchor_text(paragraph.get("text", "")) == normalized]
            if len(exact_xml_hits) == 1:
                parsed = re.match(r"^表格(\d+)\s*第(\d+)行第(\d+)列（段(\d+)）$", hint)
                if parsed:
                    table_index, row_index, column_index, cell_paragraph_index = [int(value) for value in parsed.groups()]
                    cell = {
                        "location": hint,
                        "text": exact_xml_hits[0].get("text", ""),
                        "xml_paragraph_index": exact_xml_hits[0].get("xml_paragraph_index"),
                        "table_index": table_index,
                        "row_index": row_index,
                        "column_index": column_index,
                        "cell_paragraph_index": cell_paragraph_index,
                        "node_id": make_table_cell_node_id(table_index, row_index, column_index, cell_paragraph_index),
                        "presentation_node_id": make_table_cell_node_id(table_index, row_index, column_index, cell_paragraph_index),
                        "presentation_kind": AnchorKind.TABLE_CELL.value,
                    }
                    matched_from = "table_source_text_xml"
        if not cell:
            return None
        anchor = {
            "kind": AnchorKind.TABLE_CELL.value,
            "node_id": cell.get("node_id"),
            "presentation_kind": cell.get("presentation_kind") or AnchorKind.TABLE_CELL.value,
            "presentation_node_id": cell.get("presentation_node_id") or cell.get("node_id"),
            "xml_paragraph_index": cell.get("xml_paragraph_index"),
            "table_index": cell.get("table_index"),
            "row_index": cell.get("row_index"),
            "column_index": cell.get("column_index"),
            "cell_paragraph_index": cell.get("cell_paragraph_index"),
            "location": cell.get("location"),
            "matched_from": matched_from,
        }
        return self._finalize_anchor(anchor, item, cell.get("text"))

    def resolve_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        existing_anchor = normalize_anchor_dict(item.get("anchor"))
        if existing_anchor:
            return self._upgrade_existing_anchor(existing_anchor, item)

        location_hint = item.get("location_hint") or item.get("locationHint") or item.get("location") or ""
        source_text = item.get("source_text") or item.get("sourceText") or item.get("original") or ""
        term_issue = item.get("term_issue") or item.get("termIssue") or ""

        table_anchor = self._resolve_table_cell_anchor(item, location_hint, source_text)
        if table_anchor:
            return table_anchor

        return self._resolve_body_anchor_from_item(item, location_hint_override=str(location_hint or ""))

    def upgrade_report(self, report_path: Path, source: str) -> Dict[str, int]:
        if not report_path.exists():
            return {"resolved": 0, "unresolved": 0}
        data = json.loads(report_path.read_text(encoding="utf-8"))
        items = data.get("annotationItems") if isinstance(data, dict) else None
        if not isinstance(items, list):
            return {"resolved": 0, "unresolved": 0}

        changed = False
        resolved = 0
        unresolved = 0
        for item in items:
            if not isinstance(item, dict):
                continue
            item.setdefault("source", source)
            anchor = self.resolve_item(item)
            if anchor:
                if item.get("anchor") != anchor:
                    item["anchor"] = anchor
                    changed = True
                resolved += 1
            else:
                unresolved += 1

        meta = data.setdefault("meta", {}) if isinstance(data, dict) else {}
        meta["anchorContract"] = {
            "version": ANCHOR_CONTRACT_VERSION,
            "resolver": "annotation_anchor_infra",
            "source": source,
            "resolvedCount": resolved,
            "unresolvedCount": unresolved,
        }
        if changed or True:
            report_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"resolved": resolved, "unresolved": unresolved}


def materialize_report_anchors(output_dir: Path, target_path: Optional[Path] = None) -> Dict[str, Dict[str, int]]:
    actual_target = target_path or infer_target_path(output_dir)
    if not actual_target:
        return {}
    infra = AnchorInfrastructure(actual_target)
    summaries: Dict[str, Dict[str, int]] = {}
    for filename, source in STRUCTURED_ANCHOR_REPORTS.items():
        summaries[source] = infra.upgrade_report(output_dir / filename, source)
    snapshot_path = output_dir / FORMAT_ANCHOR_V2_FILENAME
    if snapshot_path.exists():
        summaries["format_anchor_snapshot"] = infra.upgrade_report(snapshot_path, SourceType.FORMAT.value)
    return summaries
