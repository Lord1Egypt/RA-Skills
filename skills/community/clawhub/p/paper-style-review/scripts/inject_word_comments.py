#!/usr/bin/env python3
"""
inject_word_comments.py
-----------------------
统一 Word 批注注入入口。

能力：
1. 支持统一 annotation items（annotation_assembler.py 输出的列表 JSON）；
2. 按“问题 + 建议/改写示范 + 依据 + 风险”的统一风格写入批注；
3. 同一段落的多来源问题会合并为一条批注，避免把文档打成蜂窝煤。

用法：
  python3 inject_word_comments.py \
    --target /path/to/target.docx \
    --report /path/to/annotations.json \
    --output /path/to/annotated.docx \
    [--author "Scout"] [--initials "SC"]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from zipfile import ZipFile

from lxml import etree
from target_document_index import build_xml_paragraph_locator
from word_text_surface import (
    build_paragraph_text_surface,
    get_paragraph_visible_text,
    get_run_visible_text,
    split_run_at_surface_position,
)

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
COMMENTS_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
COMMENTS_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"

SOURCE_LABELS = {
    "style_deviation": "风格模仿偏离",
    "format": "格式",
    "terminology": "术语",
    "logic": "逻辑",
    "historical_format": "往届格式规则",
}

ISSUE_LABELS = {
    "font_size": "字号问题",
    "font_name": "字体问题",
    "line_spacing": "行距问题",
    "space_before": "段前距问题",
    "space_after": "段后距问题",
    "first_line_indent": "首行缩进问题",
    "left_indent": "左缩进问题",
    "right_indent": "右缩进问题",
    "alignment": "对齐方式问题",
    "variant_usage": "术语变体混用",
    "must_keep_missing": "规范术语缺失",
    "weak_chinese_context": "中文语境不足",
    "coined_term": "疑似自造词",
    "jargon_like_phrase": "疑似行业黑话/宣传腔",
    "abbreviation_without_anchor": "缩写缺少中文锚点",
    "external_verification_candidate": "术语需外部核验",
    "logic_coherence": "逻辑不通顺",
    "style_deviation_semantic_role": "refs推进角色偏离",
}


def get_paragraph_text(p_elem: etree._Element) -> str:
    return get_paragraph_visible_text(p_elem)


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def find_max_comment_id(doc_root: etree._Element, comments_root: etree._Element) -> int:
    max_id = -1
    for root in [doc_root, comments_root]:
        for tag in ["comment", "commentRangeStart", "commentRangeEnd", "commentReference"]:
            for el in root.iter(f"{{{W_NS}}}{tag}"):
                raw = el.get(f"{{{W_NS}}}id", el.get("id", "-1"))
                try:
                    cid = int(raw)
                except Exception:
                    continue
                if cid > max_id:
                    max_id = cid
    return max_id


def build_comment_element(comment_id: int, author: str, initials: str, date_str: str, text_lines: List[str]) -> etree._Element:
    comment = etree.Element(f"{{{W_NS}}}comment")
    comment.set(f"{{{W_NS}}}id", str(comment_id))
    comment.set(f"{{{W_NS}}}author", author)
    comment.set(f"{{{W_NS}}}initials", initials)
    comment.set(f"{{{W_NS}}}date", date_str)

    for i, line in enumerate(text_lines):
        p = etree.SubElement(comment, f"{{{W_NS}}}p")
        if i == 0:
            ppr = etree.SubElement(p, f"{{{W_NS}}}pPr")
            ps = etree.SubElement(ppr, f"{{{W_NS}}}pStyle")
            ps.set(f"{{{W_NS}}}val", "CommentText")
            r_ref = etree.SubElement(p, f"{{{W_NS}}}r")
            rpr_ref = etree.SubElement(r_ref, f"{{{W_NS}}}rPr")
            rs_ref = etree.SubElement(rpr_ref, f"{{{W_NS}}}rStyle")
            rs_ref.set(f"{{{W_NS}}}val", "CommentReference")
            etree.SubElement(r_ref, f"{{{W_NS}}}annotationRef")

        r_text = etree.SubElement(p, f"{{{W_NS}}}r")
        t = etree.SubElement(r_text, f"{{{W_NS}}}t")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = line

    return comment


def load_annotation_items(report_path: str | Path) -> List[Dict[str, Any]]:
    report_path = Path(report_path)
    data = json.loads(report_path.read_text(encoding="utf-8"))

    # 1) 统一 annotation items：顶层就是列表
    if isinstance(data, list):
        return data

    # 2) 统一 annotation items：包装在 annotations 字段里
    if isinstance(data, dict) and isinstance(data.get("annotations"), list):
        return data["annotations"]

    raise ValueError(f"无法识别的批注报告格式：{report_path}")


def _extract_paragraph_index(location_hint: str) -> Optional[int]:
    if not location_hint:
        return None
    patterns = [
        r"第\s*(\d+)\s*段",
        r"paragraph\s*(\d+)",
        r"para[-_ ]?(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, location_hint, re.I)
        if match:
            try:
                return int(match.group(1))
            except Exception:
                return None
    return None


def _looks_global_paragraph_ref(location_hint: str) -> bool:
    if not location_hint:
        return False
    return ("章" not in location_hint and ">" not in location_hint and "section" not in location_hint.lower())


def _can_use_hint_only_fallback(location_hint: str, source_text: str) -> bool:
    """只有在缺少可靠 source_text 时，才允许退回到 location hint 文本匹配。

    否则很容易把“第X章 > 第Y段”或章节标题误挂到封面空段/章标题上。
    """
    if normalize(source_text):
        return False
    return bool(normalize(location_hint))


COMMENT_TIMEZONE = ZoneInfo("Asia/Shanghai")


def _serialize_comment_datetime(now: Optional[datetime] = None) -> str:
    """按北京时间序列化批注时间。"""
    current = (now or datetime.now(COMMENT_TIMEZONE)).astimezone(COMMENT_TIMEZONE).replace(microsecond=0)
    return current.isoformat()


def _anchor_kind(item: Dict[str, Any]) -> str:
    anchor = item.get("anchor") if isinstance(item.get("anchor"), dict) else {}
    return str(anchor.get("kind", "") or "")


def _anchor_node_id(item: Dict[str, Any]) -> Optional[str]:
    anchor = item.get("anchor") if isinstance(item.get("anchor"), dict) else {}
    for key in ["presentation_node_id", "node_id"]:
        value = anchor.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _anchor_xml_paragraph_index(item: Dict[str, Any]) -> Optional[int]:
    anchor = item.get("anchor") if isinstance(item.get("anchor"), dict) else {}
    for key in ["xml_paragraph_index", "proxy_xml_paragraph_index"]:
        raw = anchor.get(key)
        try:
            value = int(raw)
        except Exception:
            continue
        if value > 0:
            return value
    return None


def locate_paragraph(paragraphs: List[etree._Element], node_targets: Dict[str, Dict[str, Any]], item: Dict[str, Any]) -> Optional[int]:
    """返回匹配到的段落下标（0-based）。

    规则：
    - 逻辑/风格类 locationHint 往往是“第X章 > 第Y段”，不是全局段号，不能盲信；
    - 对这类提示先按 source_text 精确匹配，再考虑显式全局段号；
    - 只有像“第88段”这种纯全局提示，才允许段号 fallback；
    - 只有在缺少可靠 source_text 时，才允许用 hint 文本兜底；
    - 宁可 unmatched，也不把后文问题错挂到封面页或空段落。
    """
    location_hint = item.get("location_hint") or item.get("locationHint") or item.get("location", "")
    source_text = item.get("source_text") or item.get("sourceText") or item.get("original", "")

    anchor_node_id = _anchor_node_id(item)
    if anchor_node_id and anchor_node_id in node_targets:
        return int(node_targets[anchor_node_id]["order_index"])

    anchor_para_idx = _anchor_xml_paragraph_index(item)
    if anchor_para_idx is not None and 1 <= anchor_para_idx <= len(paragraphs):
        return anchor_para_idx - 1

    norm_source = normalize(source_text)
    if norm_source:
        for idx, p in enumerate(paragraphs):
            p_norm = normalize(get_paragraph_text(p))
            if not p_norm:
                continue
            if p_norm == norm_source:
                return idx
            if len(norm_source) > 10 and norm_source in p_norm:
                return idx
            if len(p_norm) > 20 and p_norm in norm_source:
                return idx

        prefix = norm_source[:50]
        if prefix:
            for idx, p in enumerate(paragraphs):
                p_norm = normalize(get_paragraph_text(p))
                if not p_norm:
                    continue
                if p_norm.startswith(prefix):
                    return idx

    para_index = _extract_paragraph_index(location_hint)
    if _looks_global_paragraph_ref(location_hint) and para_index is not None and 1 <= para_index <= len(paragraphs):
        return para_index - 1

    norm_hint = normalize(location_hint)
    if _can_use_hint_only_fallback(location_hint, source_text) and norm_hint and len(norm_hint) > 10:
        for idx, p in enumerate(paragraphs):
            p_norm = normalize(get_paragraph_text(p))
            if not p_norm:
                continue
            if norm_hint in p_norm or (len(p_norm) > 20 and p_norm in norm_hint):
                return idx

    return None


def _format_source_label(item: Dict[str, Any]) -> str:
    source = item.get("source", "")
    issue_type = item.get("issue_type") or item.get("issueType") or ""
    source_label = SOURCE_LABELS.get(source, source or "问题")
    issue_label = ISSUE_LABELS.get(issue_type, issue_type)
    if issue_label:
        return f"[{source_label} / {issue_label}]"
    return f"[{source_label}]"


def format_annotation_comment_text(item: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    header = _format_source_label(item)
    problem = item.get("problem", "")
    suggestion = item.get("suggestion", "")
    rewrite_text = item.get("rewrite_text") or item.get("rewriteText") or ""
    basis = item.get("basis", "")
    risk = item.get("risk", "")
    diff_type = item.get("diff_type") or item.get("diffType")

    lines.append(f"{header} 问题：{problem}" if problem else header)

    if suggestion:
        lines.append(f"建议：{suggestion}")

    if diff_type in ["~", "+", "-"]:
        diff_label = {"~": "替换", "+": "新增", "-": "删除/压缩"}.get(diff_type, "调整")
        lines.append(f"操作：{diff_label}")
    if rewrite_text:
        lines.append(f"示例：{rewrite_text}")

    if basis:
        lines.append(f"依据：{basis}")
    if risk:
        lines.append(f"风险：{risk}")

    return lines


def group_items_by_paragraph(
    paragraphs: List[etree._Element],
    node_targets: Dict[str, Dict[str, Any]],
    items: List[Dict[str, Any]],
) -> Tuple[Dict[int, List[Dict[str, Any]]], List[str]]:
    grouped: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    unmatched: List[str] = []
    seen = set()

    for item in items:
        para_idx = locate_paragraph(paragraphs, node_targets, item)
        if para_idx is None:
            label = item.get("location_hint") or item.get("locationHint") or item.get("location") or "未知位置"
            snippet = (item.get("source_text") or item.get("sourceText") or "")[:80]
            unmatched.append(f"{label}: {snippet}")
            continue

        dedupe_key = (
            para_idx,
            normalize(item.get("source_text") or item.get("sourceText") or ""),
            item.get("problem", ""),
            item.get("source", ""),
        )
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        grouped[para_idx].append(item)

    return grouped, unmatched


def _get_run_text(run: etree._Element) -> str:
    return get_run_visible_text(run)


def _candidate_anchor_text(item: Dict[str, Any]) -> str:
    anchor = item.get("anchor") if isinstance(item.get("anchor"), dict) else {}
    attach_text = anchor.get("attach_text")
    if isinstance(attach_text, str) and attach_text.strip():
        return attach_text.strip()
    for key in ["focus_text", "focusText", "sentence_text", "sentenceText", "term_issue", "termIssue", "source_text", "sourceText", "original"]:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _anchor_selection_mode(item: Dict[str, Any]) -> str:
    anchor = item.get("anchor") if isinstance(item.get("anchor"), dict) else {}
    return str(anchor.get("selection_mode", "") or "")


def _anchor_span_offsets(item: Dict[str, Any]) -> Optional[Tuple[int, int]]:
    anchor = item.get("anchor") if isinstance(item.get("anchor"), dict) else {}
    try:
        start = int(anchor.get("start_offset"))
        end = int(anchor.get("end_offset"))
    except Exception:
        return None
    if start < 0 or end <= start:
        return None
    return start, end


def _normalize_char_for_match(ch: str) -> str:
    if ch.isspace():
        return ""
    if ch in {"“", "”", "「", "」"}:
        return '"'
    if ch in {"‘", "’"}:
        return "'"
    return ch


def _normalized_text_with_raw_offsets(text: str) -> Tuple[str, List[int]]:
    normalized_chars: List[str] = []
    raw_offsets: List[int] = []
    for raw_idx, ch in enumerate(text or ""):
        mapped = _normalize_char_for_match(ch)
        if not mapped:
            continue
        normalized_chars.append(mapped)
        raw_offsets.append(raw_idx)
    return "".join(normalized_chars), raw_offsets


def _find_anchor_span_in_paragraph(paragraph_text: str, anchor_text: str) -> Optional[Tuple[int, int]]:
    if not paragraph_text or not anchor_text:
        return None
    literal_start = paragraph_text.find(anchor_text)
    if literal_start >= 0:
        return literal_start, literal_start + len(anchor_text)

    paragraph_norm, paragraph_offsets = _normalized_text_with_raw_offsets(paragraph_text)
    anchor_norm, _ = _normalized_text_with_raw_offsets(anchor_text)
    if not paragraph_norm or not anchor_norm:
        return None
    norm_start = paragraph_norm.find(anchor_norm)
    if norm_start < 0:
        return None
    norm_end = norm_start + len(anchor_norm) - 1
    raw_start = paragraph_offsets[norm_start]
    raw_end = paragraph_offsets[norm_end] + 1
    return raw_start, raw_end


def _build_comment_reference_run(comment_id: int) -> etree._Element:
    ref_run = etree.Element(f"{{{W_NS}}}r")
    ref_rpr = etree.SubElement(ref_run, f"{{{W_NS}}}rPr")
    ref_style = etree.SubElement(ref_rpr, f"{{{W_NS}}}rStyle")
    ref_style.set(f"{{{W_NS}}}val", "CommentReference")
    cr = etree.SubElement(ref_run, f"{{{W_NS}}}commentReference")
    cr.set(f"{{{W_NS}}}id", str(comment_id))
    return ref_run



def _attach_comment_to_span(para: etree._Element, comment_id: int, start_pos: int, end_pos: int) -> bool:
    surface = build_paragraph_text_surface(para)
    if not surface.text:
        return False
    if end_pos <= start_pos or end_pos > len(surface.chars):
        return False
    end_char = surface.chars[end_pos - 1]
    split_run_at_surface_position(
        end_char.run,
        end_char.node,
        end_char.node_char_index,
        after=True,
    )

    surface = build_paragraph_text_surface(para)
    if end_pos > len(surface.chars):
        return False
    start_char = surface.chars[start_pos]
    split_run_at_surface_position(
        start_char.run,
        start_char.node,
        start_char.node_char_index,
        after=False,
    )

    surface = build_paragraph_text_surface(para)
    if end_pos > len(surface.chars):
        return False
    selected_chars = surface.chars[start_pos:end_pos]
    if not selected_chars:
        return False
    start_run = selected_chars[0].run
    end_run = selected_chars[-1].run

    start_parent = start_run.getparent()
    crs = etree.Element(f"{{{W_NS}}}commentRangeStart")
    crs.set(f"{{{W_NS}}}id", str(comment_id))
    start_parent.insert(start_parent.index(start_run), crs)

    end_parent = end_run.getparent()
    end_idx = end_parent.index(end_run)
    cre = etree.Element(f"{{{W_NS}}}commentRangeEnd")
    cre.set(f"{{{W_NS}}}id", str(comment_id))
    end_parent.insert(end_idx + 1, cre)
    end_parent.insert(end_idx + 2, _build_comment_reference_run(comment_id))
    return True


def try_attach_comment_to_exact_text(para: etree._Element, item: Dict[str, Any], comment_id: int) -> bool:
    """尽量把批注挂到词/短语级文本；mainline 优先消费已固化 span offsets。"""
    selection_mode = _anchor_selection_mode(item)
    span_offsets = _anchor_span_offsets(item)
    if selection_mode == "paragraph":
        return False
    if span_offsets is not None:
        return _attach_comment_to_span(para, comment_id, span_offsets[0], span_offsets[1])

    anchor = _candidate_anchor_text(item)
    if not anchor or len(anchor) > 80:
        return False

    para_text = get_paragraph_text(para)
    if not para_text or normalize(anchor) == normalize(para_text):
        return False
    anchor_span = _find_anchor_span_in_paragraph(para_text, anchor)
    if anchor_span is None:
        return False
    return _attach_comment_to_span(para, comment_id, anchor_span[0], anchor_span[1])


def ensure_comments_relationship(rels_root: etree._Element) -> None:
    has_comments_rel = False
    for rel in rels_root:
        if rel.get("Type") == COMMENTS_TYPE:
            has_comments_rel = True
            break
    if has_comments_rel:
        return

    max_rid = 0
    for rel in rels_root:
        rid = rel.get("Id", "")
        if rid.startswith("rId"):
            try:
                max_rid = max(max_rid, int(rid[3:]))
            except ValueError:
                pass

    new_rel = etree.SubElement(rels_root, "Relationship")
    new_rel.set("Id", f"rId{max_rid + 1}")
    new_rel.set("Type", COMMENTS_TYPE)
    new_rel.set("Target", "comments.xml")


def ensure_comments_content_type(ct_root: etree._Element) -> None:
    for override in ct_root:
        if "comments.xml" in override.get("PartName", ""):
            return
    override = etree.SubElement(ct_root, "Override")
    override.set("PartName", "/word/comments.xml")
    override.set("ContentType", COMMENTS_CT)


def inject_comments(target_path: str | Path, report_path: str | Path, output_path: str | Path, author: str = "Scout", initials: str = "SC") -> None:
    target_path = Path(target_path)
    report_path = Path(report_path)
    output_path = Path(output_path)

    items = load_annotation_items(report_path)
    if not items:
        print("报告中没有可注入批注的条目，直接复制原文件。")
        shutil.copy2(target_path, output_path)
        return

    shutil.copy2(target_path, output_path)

    with ZipFile(output_path, "r") as zin:
        all_names = set(zin.namelist())
        doc_xml_bytes = zin.read("word/document.xml")
        rels_bytes = zin.read("word/_rels/document.xml.rels")
        ct_bytes = zin.read("[Content_Types].xml")
        comments_bytes = zin.read("word/comments.xml") if "word/comments.xml" in all_names else None

    doc_root = etree.fromstring(doc_xml_bytes)
    rels_root = etree.fromstring(rels_bytes)
    ct_root = etree.fromstring(ct_bytes)
    comments_root = etree.fromstring(comments_bytes) if comments_bytes else etree.Element(f"{{{W_NS}}}comments", nsmap={"w": W_NS, "r": R_NS})

    body = doc_root.find(f"{{{W_NS}}}body")
    paragraphs, node_targets = build_xml_paragraph_locator(body)
    grouped, unmatched = group_items_by_paragraph(paragraphs, node_targets, items)

    next_id = find_max_comment_id(doc_root, comments_root) + 1
    now_str = _serialize_comment_datetime()

    matched_item_count = 0
    comment_count = 0
    source_counter = Counter()

    exact_count = 0
    fallback_count = 0

    for para_idx in sorted(grouped.keys()):
        para = paragraphs[para_idx]
        para_items = grouped[para_idx]

        # 策略：每个 item 先尝试词级精细标注；失败的收集起来合并为段落级
        fallback_items: List[Dict[str, Any]] = []
        for item in para_items:
            comment_id = next_id
            next_id += 1
            lines = format_annotation_comment_text(item)
            comments_root.append(build_comment_element(comment_id, author, initials, now_str, lines))
            source_counter[item.get("source", "unknown")] += 1
            matched_item_count += 1

            anchor_kind = _anchor_kind(item)
            allow_exact = anchor_kind in {"", "body_paragraph", "table_cell"}
            if allow_exact and try_attach_comment_to_exact_text(para, item, comment_id):
                exact_count += 1
                comment_count += 1
            else:
                # 精细定位失败，或 anchor 明确要求以 proxy 段落挂载，则退回段落级
                crs = etree.Element(f"{{{W_NS}}}commentRangeStart")
                crs.set(f"{{{W_NS}}}id", str(comment_id))
                ppr = para.find(f"{{{W_NS}}}pPr")
                if ppr is not None:
                    para.insert(list(para).index(ppr) + 1, crs)
                else:
                    para.insert(0, crs)
                cre = etree.Element(f"{{{W_NS}}}commentRangeEnd")
                cre.set(f"{{{W_NS}}}id", str(comment_id))
                para.append(cre)
                ref_run = etree.SubElement(para, f"{{{W_NS}}}r")
                ref_rpr = etree.SubElement(ref_run, f"{{{W_NS}}}rPr")
                ref_style = etree.SubElement(ref_rpr, f"{{{W_NS}}}rStyle")
                ref_style.set(f"{{{W_NS}}}val", "CommentReference")
                cr = etree.SubElement(ref_run, f"{{{W_NS}}}commentReference")
                cr.set(f"{{{W_NS}}}id", str(comment_id))
                fallback_count += 1
                comment_count += 1

    ensure_comments_relationship(rels_root)
    ensure_comments_content_type(ct_root)

    doc_xml_out = etree.tostring(doc_root, xml_declaration=True, encoding="UTF-8", standalone=True)
    comments_xml_out = etree.tostring(comments_root, xml_declaration=True, encoding="UTF-8", standalone=True)
    rels_xml_out = etree.tostring(rels_root, xml_declaration=True, encoding="UTF-8", standalone=True)
    ct_xml_out = etree.tostring(ct_root, xml_declaration=True, encoding="UTF-8", standalone=True)

    tmp_path = output_path.with_suffix(".tmp.docx")
    with ZipFile(target_path, "r") as zin, ZipFile(tmp_path, "w") as zout:
        for item_info in zin.infolist():
            if item_info.filename == "word/document.xml":
                zout.writestr(item_info, doc_xml_out)
            elif item_info.filename == "word/_rels/document.xml.rels":
                zout.writestr(item_info, rels_xml_out)
            elif item_info.filename == "[Content_Types].xml":
                zout.writestr(item_info, ct_xml_out)
            elif item_info.filename == "word/comments.xml":
                zout.writestr(item_info, comments_xml_out)
            else:
                zout.writestr(item_info, zin.read(item_info.filename))
        if "word/comments.xml" not in all_names:
            zout.writestr("word/comments.xml", comments_xml_out)

    tmp_path.replace(output_path)

    print(f"匹配并注入批注条目：{matched_item_count}/{len(items)}")
    print(f"实际生成批注数（按段落合并后）：{comment_count}")
    print(f"词/短语级精确锚点：{exact_count}，段落级回退：{fallback_count}")
    if source_counter:
        print("各来源命中：")
        for source, count in source_counter.most_common():
            print(f"  - {SOURCE_LABELS.get(source, source)}: {count}")
    if unmatched:
        print(f"未匹配条目（{len(unmatched)}）：")
        for line in unmatched[:20]:
            print(f"  - {line}")
    print(f"输出文件：{output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="将统一批注 JSON 注入 DOCX")
    parser.add_argument("--target", required=True, help="目标 .docx 路径")
    parser.add_argument("--report", required=True, help="统一批注 JSON 文件")
    parser.add_argument("--output", required=True, help="输出带批注 .docx 路径")
    parser.add_argument("--author", default="Scout", help="批注作者")
    parser.add_argument("--initials", default="SC", help="批注作者缩写")
    args = parser.parse_args()

    inject_comments(args.target, args.report, args.output, args.author, args.initials)


if __name__ == "__main__":
    main()
