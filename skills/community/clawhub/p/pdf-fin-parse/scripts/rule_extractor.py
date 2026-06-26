"""规则路径：纯本地解析（fitz blocks + fitz find_tables + 数值规整）。

设计目标：
  - 完全离线，零 API 调用，sub-second per page
  - 输出 schema 与 VLM 路径完全一致（page_no/markdown/blocks/tables）
  - 供 router 在"简单页（纯文本 / 单张有边框表）"上替代 VLM

不擅长的场景（要 router 路由给 VLM）：
  - 扫描页 / 低文本密度页
  - 无边框表格 / 多级表头 / 合并单元格
  - 多栏排版（虽然 layout.py 能检测，但 fitz 文字块顺序常不可靠）
  - 跨页延续表格

依赖：仅 fitz (PyMuPDF) + _legacy/{numeric_normalizer,layout}.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import fitz

# 引入 _legacy 里干净的两个工具模块
_LEGACY_DIR = Path(__file__).resolve().parent.parent / "_legacy"
if str(_LEGACY_DIR) not in sys.path:
    sys.path.insert(0, str(_LEGACY_DIR))

from numeric_normalizer import parse_number, detect_unit_in_context  # noqa: E402
from layout import detect_two_columns                                 # noqa: E402


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# 判定扫描页的字符密度阈值（< 此值则没法走规则路径）
TEXT_DENSITY_FOR_SCAN = 50

# heading 启发式
_SENTENCE_END = set("。！？.!?")
_CONTINUATION = set("，、,;；：:")

_PAGE_NUM_PATTERNS = [
    re.compile(r"^\d+\s*[/／]\s*\d+$"),
    re.compile(r"^-?\s*\d+\s*-?$"),
    re.compile(r"^第\s*\d+\s*页$"),
    re.compile(r"^Page\s+\d+", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Block 抽取（fitz）
# ---------------------------------------------------------------------------

def _body_font_size(page: fitz.Page) -> float:
    """该页 span 数量最多的字号 ≈ 正文字号。"""
    sizes: List[float] = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                sizes.append(round(span["size"], 1))
    if not sizes:
        return 10.0
    return Counter(sizes).most_common(1)[0][0]


def _is_heading(span_size: float, body_size: float, text: str) -> bool:
    if span_size < body_size * 1.15:
        return False
    t = text.strip()
    if not t or len(t) > 30:
        return False
    last = t[-1]
    if last in _SENTENCE_END or last in _CONTINUATION:
        return False
    return True


def _line_in_any_bbox(line_bbox: tuple, exclude: List[List[float]]) -> bool:
    cx = (line_bbox[0] + line_bbox[2]) / 2
    cy = (line_bbox[1] + line_bbox[3]) / 2
    for bb in exclude:
        if bb[0] <= cx <= bb[2] and bb[1] <= cy <= bb[3]:
            return True
    return False


def _extract_blocks(page: fitz.Page, page_num: int,
                    exclude_bboxes: Optional[List[List[float]]] = None
                    ) -> List[Dict[str, Any]]:
    exclude = exclude_bboxes or []
    body = _body_font_size(page)
    out: List[Dict[str, Any]] = []
    for raw in page.get_text("dict").get("blocks", []):
        if raw.get("type") != 0:                         # 0=text, 1=image
            continue
        for line in raw.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            if _line_in_any_bbox(line["bbox"], exclude):
                continue
            text = "".join(s["text"] for s in spans).strip()
            if not text:
                continue
            avg = sum(s["size"] for s in spans) / len(spans)
            is_h = _is_heading(avg, body, text)
            out.append({
                "type": "heading" if is_h else "paragraph",
                "level": 1 if is_h else None,
                "text": text,
                "source_page": page_num,
                "source_bbox": [round(v, 2) for v in line["bbox"]],
            })
    return out


# ---------------------------------------------------------------------------
# 段落合并
# ---------------------------------------------------------------------------

_PARAGRAPH_END = set("。！？.!?")


def _join_text(prev: str, cur: str) -> str:
    a, b = prev.rstrip(), cur.lstrip()
    if not a:
        return b
    if not b:
        return a
    if a[-1].isascii() and a[-1].isalnum() and b[0].isascii() and b[0].isalnum():
        return f"{a} {b}"
    return a + b


def _should_merge(prev: Dict, cur: Dict) -> bool:
    if prev["source_page"] != cur["source_page"]:
        return False
    if prev["type"] != "paragraph" or cur["type"] != "paragraph":
        return False
    prev_text = prev["text"].rstrip()
    if prev_text and prev_text[-1] in _PARAGRAPH_END:
        return False
    prev_h = prev["source_bbox"][3] - prev["source_bbox"][1]
    cur_h = cur["source_bbox"][3] - cur["source_bbox"][1]
    line_h = (prev_h + cur_h) / 2 if (prev_h and cur_h) else max(prev_h, cur_h, 10)
    gap = cur["source_bbox"][1] - prev["source_bbox"][3]
    return gap <= line_h * 1.2


def _merge_consecutive_lines(blocks: List[Dict]) -> List[Dict]:
    if not blocks:
        return blocks
    blocks = sorted(blocks, key=lambda b: (b["source_page"],
                                            b["source_bbox"][1],
                                            b["source_bbox"][0]))
    merged: List[Dict] = [blocks[0].copy()]
    for cur in blocks[1:]:
        prev = merged[-1]
        if _should_merge(prev, cur):
            prev["text"] = _join_text(prev["text"], cur["text"])
            prev["source_bbox"] = [
                round(min(prev["source_bbox"][0], cur["source_bbox"][0]), 2),
                prev["source_bbox"][1],
                round(max(prev["source_bbox"][2], cur["source_bbox"][2]), 2),
                cur["source_bbox"][3],
            ]
        else:
            merged.append(cur.copy())
    return merged


# ---------------------------------------------------------------------------
# 页眉页脚过滤（单页版：仅靠 bbox 位置启发，没全局 recurring 表）
# ---------------------------------------------------------------------------

def _is_page_number(text: str) -> bool:
    t = text.strip()
    return any(p.match(t) for p in _PAGE_NUM_PATTERNS)


def _filter_headers_footers_single_page(blocks: List[Dict], page_height: float,
                                        band_ratio: float = 0.07
                                        ) -> Tuple[List[Dict], List[Dict]]:
    """单页版：只剔除 bbox 在顶 7%/底 7% 且匹配页码 pattern 的行。

    (全局 recurring 文本检测需要整本 PDF 视角，由 skill.py 的 router 层在合并阶段做)
    """
    top_band = page_height * band_ratio
    bot_band = page_height * (1 - band_ratio)
    kept, removed = [], []
    for b in blocks:
        bb = b["source_bbox"]
        at_edge = bb[3] <= top_band or bb[1] >= bot_band
        if at_edge and _is_page_number(b["text"]):
            removed.append(b)
        else:
            kept.append(b)
    return kept, removed


# ---------------------------------------------------------------------------
# 表格抽取（fitz find_tables）
# ---------------------------------------------------------------------------

def _extract_tables(page: fitz.Page, page_num: int
                    ) -> Tuple[List[Dict[str, Any]], List[List[float]]]:
    """用 PyMuPDF 1.23+ 的 find_tables；返回 (tables, bboxes)。

    fitz.TableFinder 对**有边框/半边框**表格效果好；无边框/多级表头会失败，
    router 应把这种页路由给 VLM。
    """
    try:
        finder = page.find_tables()
    except Exception:                                    # noqa: BLE001
        return [], []
    out_tables: List[Dict[str, Any]] = []
    bboxes: List[List[float]] = []
    for ti, t in enumerate(finder.tables, 1):
        try:
            rows = t.extract()
        except Exception:                                # noqa: BLE001
            continue
        if not rows or not rows[0]:
            continue
        n_rows = len(rows)
        n_cols = max(len(r) for r in rows)
        cells: List[Dict[str, Any]] = []
        for r_idx, row in enumerate(rows):
            for c_idx, cell_text in enumerate(row):
                if cell_text is None:
                    cell_text = ""
                cells.append({
                    "row": r_idx, "col": c_idx,
                    "rowspan": 1, "colspan": 1,
                    "text": str(cell_text).strip(),
                    "value": None, "unit": None,
                })
        bbox = list(t.bbox)
        out_tables.append({
            "table_id_local": f"t_p{page_num}_{ti:02d}",
            "caption": None,
            "n_rows": n_rows, "n_cols": n_cols,
            "header_rows": 1,                             # 规则路径默认单表头
            "source_page": page_num,
            "source_bbox": [round(v, 2) for v in bbox],
            "cells": cells,
        })
        bboxes.append([round(v, 2) for v in bbox])
    return out_tables, bboxes


def _enrich_tables_numerics(tables: List[Dict[str, Any]],
                            blocks: List[Dict[str, Any]]) -> int:
    """把单位上下文（"单位：万元"）应用到 cell.value/unit。"""
    decls: List[Tuple[int, float, str]] = []
    for b in blocks:
        u = detect_unit_in_context(b["text"])
        if u:
            decls.append((b["source_page"], b["source_bbox"][1], u))
    decls.sort()

    def _unit_for(table: Dict) -> Optional[str]:
        p, ty = table["source_page"], table["source_bbox"][1]
        cur = None
        for dp, dy, du in decls:
            if dp < p or (dp == p and dy < ty):
                cur = du
            else:
                break
        return cur

    parsed = 0
    for t in tables:
        unit_ctx = _unit_for(t)
        for c in t["cells"]:
            nv = parse_number(c["text"], default_unit=unit_ctx)
            c["value"] = nv.value
            c["unit"] = nv.unit
            if nv.parse_ok:
                parsed += 1
    return parsed


# ---------------------------------------------------------------------------
# Markdown 渲染（单页）
# ---------------------------------------------------------------------------

def _render_markdown(blocks: List[Dict], tables: List[Dict],
                     page_width: float) -> str:
    """渲染单页 markdown。双栏识别 → 重排；其余按 y 顺序，表格按 y 插入。"""
    is_two_col = detect_two_columns(blocks, page_width) is not None
    if is_two_col:
        left, right = detect_two_columns(blocks, page_width) or ([], [])
        ordered_blocks = (
            sorted(left, key=lambda b: b["source_bbox"][1])
            + sorted(right, key=lambda b: b["source_bbox"][1])
        )
    else:
        ordered_blocks = sorted(blocks, key=lambda b: b["source_bbox"][1])

    # 表格按 y 插入到 blocks 之间
    items: List[Tuple[str, Dict]] = [("block", b) for b in ordered_blocks]
    for t in sorted(tables, key=lambda x: x["source_bbox"][1]):
        t_top = t["source_bbox"][1]
        insert_at = len(items)
        for i, (_, it) in enumerate(items):
            if it.get("source_bbox", [0, 0, 0, 0])[1] > t_top:
                insert_at = i
                break
        items.insert(insert_at, ("table", t))

    lines: List[str] = []
    for kind, item in items:
        if kind == "block":
            if item["type"] == "heading":
                lines.append(f"## {item['text']}")
            else:
                lines.append(item["text"])
        else:
            # 简单 GFM table（不展开 rowspan/colspan，规则路径只处理简单表）
            cells_by_pos: Dict[Tuple[int, int], str] = {}
            for c in item["cells"]:
                cells_by_pos[(c["row"], c["col"])] = c["text"]
            n_cols = item["n_cols"]
            hr = max(1, item.get("header_rows", 1))
            header = [cells_by_pos.get((0, ci), "") for ci in range(n_cols)]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("|" + "|".join([" --- "] * n_cols) + "|")
            for r in sorted({k[0] for k in cells_by_pos if k[0] >= hr}):
                row_vals = [cells_by_pos.get((r, ci), "") for ci in range(n_cols)]
                lines.append("| " + " | ".join(row_vals) + " |")
            lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 路由用：页特征分析（cheap，sub-second）
# ---------------------------------------------------------------------------

_NUM_TOKEN_RE = re.compile(
    r"(?:[\(（\-－]?\s*[\d,，]+(?:\.\d+)?\s*[\)）]?%?)"
)
# 纯数字行：整行只是一个数（可能带千分位/小数/括号/百分号），无中文无字母
_PURE_NUM_LINE_RE = re.compile(
    r"^\s*[\(（\-－]?\s*[\d,，]+(?:\.\d+)?\s*[\)）]?\s*%?\s*$"
)


def _count_numeric_lines(text: str) -> Tuple[int, int]:
    """统计两种"表格嫌疑行"的数量。返回 (horizontal, vertical)。

    - horizontal: 含 ≥2 个数字 token 的行（标签 数字1 数字2 形态，行内表格）
    - vertical: 整行只是一个数字的行（fitz 对无边框表常把每个 cell 拆一行，
                密集垂直数字流是财务报表的强信号）

    两个信号任一足够强 → 这页应路由给 VLM（fitz find_tables 拿不到无边框表）。
    """
    horizontal = vertical = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if len(line) < 1:
            continue
        if _PURE_NUM_LINE_RE.match(line):
            vertical += 1
            continue
        if len(line) >= 4:
            tokens = _NUM_TOKEN_RE.findall(line)
            if len(tokens) >= 2:
                horizontal += 1
    return horizontal, vertical


def analyze_page(pdf_path: str, page_no: int,
                 password: Optional[str] = None) -> Dict[str, Any]:
    """快速页特征分析，供 router 决策。不做完整抽取。

    Returns:
      {
        "text_density": int,          # 字符数
        "n_tables": int,              # find_tables 的表数（仅有边框）
        "numeric_line_density": int,  # "标签 数字 数字 数字" 形态的行数（兜底捕获无边框表）
        "has_complex_table": bool,    # >=2 张表 / 任一表 > 6 列（多级表头嫌疑）/ 任一表外接矩形面积 > 50% 页面
        "is_multi_column": bool,
        "image_area_ratio": float,    # image blocks 总面积 / 页面面积
      }
    """
    doc = fitz.open(pdf_path)
    try:
        if doc.is_encrypted and not (password and doc.authenticate(password)):
            raise RuntimeError("PDF 加密，请提供 password")
        page = doc[page_no - 1]
        page_w, page_h = page.rect.width, page.rect.height
        page_area = page_w * page_h

        # 1. 文本密度
        text = page.get_text().strip()
        text_density = len(text)

        # 2. 图像占比
        img_area = 0.0
        for raw in page.get_text("dict").get("blocks", []):
            if raw.get("type") == 1:
                bb = raw.get("bbox") or [0, 0, 0, 0]
                img_area += max(0, bb[2] - bb[0]) * max(0, bb[3] - bb[1])
        image_area_ratio = round(img_area / page_area, 3) if page_area else 0.0

        # 3. 表格检测
        n_tables = 0
        complex_table = False
        try:
            tables = page.find_tables()
            for t in tables.tables:
                n_tables += 1
                try:
                    rows = t.extract()
                except Exception:                        # noqa: BLE001
                    continue
                if not rows:
                    continue
                n_cols = max(len(r) for r in rows)
                t_bbox = t.bbox
                t_area = (t_bbox[2] - t_bbox[0]) * (t_bbox[3] - t_bbox[1])
                if n_cols > 6:
                    complex_table = True
                if t_area / page_area > 0.5:
                    complex_table = True
        except Exception:                                # noqa: BLE001
            pass
        if n_tables >= 2:
            complex_table = True

        # 4. 多栏（用 _extract_blocks 的轻量子集 + layout.detect_two_columns）
        blocks_for_layout: List[Dict] = []
        for raw in page.get_text("dict").get("blocks", []):
            if raw.get("type") != 0:
                continue
            for line in raw.get("lines", []):
                bb = line.get("bbox")
                if bb:
                    blocks_for_layout.append({"source_bbox": list(bb)})
        is_two_col = detect_two_columns(blocks_for_layout, page_w) is not None

        h_lines, v_lines = _count_numeric_lines(text)

        return {
            "text_density": text_density,
            "n_tables": n_tables,
            "numeric_lines_horizontal": h_lines,   # "标签 数字1 数字2" 行数
            "numeric_lines_vertical": v_lines,     # 纯数字行（无边框表常见）
            "has_complex_table": complex_table,
            "is_multi_column": is_two_col,
            "image_area_ratio": image_area_ratio,
            "page_width": page_w,
            "page_height": page_h,
        }
    finally:
        doc.close()


# ---------------------------------------------------------------------------
# 完整页抽取（规则路径主入口）
# ---------------------------------------------------------------------------

def extract_page_via_rules(pdf_path: str, page_no: int,
                           password: Optional[str] = None) -> Dict[str, Any]:
    """规则路径：返回与 vlm_client.parse_page_via_vlm 同 schema 的 dict。

    Returns:
      {
        "page_no": int,
        "markdown": str,
        "blocks": [...],
        "tables": [...],
        "engine": "rules",
        "confidence": float,         # 启发式 confidence
        "_routing_hints": {...}      # 决策依据，便于调试
      }
    """
    doc = fitz.open(pdf_path)
    try:
        if doc.is_encrypted and not (password and doc.authenticate(password)):
            raise RuntimeError("PDF 加密，请提供 password")
        page = doc[page_no - 1]
        page_w, page_h = page.rect.width, page.rect.height

        # 1. 抽表（拿到 bbox 让 blocks 跳过表格区域）
        tables, table_bboxes = _extract_tables(page, page_no)

        # 2. 抽 blocks，跳过表格区域
        blocks = _extract_blocks(page, page_no, exclude_bboxes=table_bboxes)

        # 3. 单页页眉页脚过滤（仅页码）
        blocks, _removed = _filter_headers_footers_single_page(blocks, page_h)

        # 4. 段落合并
        blocks = _merge_consecutive_lines(blocks)

        # 5. 数值规整
        parsed = _enrich_tables_numerics(tables, blocks)

        # 6. 渲染 markdown
        md = _render_markdown(blocks, tables, page_w)

        # 7. 启发式 confidence：tables 都 parse 出 cell 且 blocks 非空 → 0.9；否则 0.7
        total_cells = sum(len(t["cells"]) for t in tables)
        confidence = 0.9 if (blocks and (total_cells == 0 or parsed > 0)) else 0.7

        return {
            "page_no": page_no,
            "markdown": md,
            "blocks": blocks,
            "tables": tables,
            "engine": "rules",
            "confidence": confidence,
        }
    finally:
        doc.close()
