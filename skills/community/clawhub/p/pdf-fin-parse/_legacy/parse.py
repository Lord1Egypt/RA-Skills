"""主解析入口：编排 layout / table_extractor / numeric_normalizer / vlm_fallback。

文本路径：
  - fitz 负责段落/标题/页眉页脚识别（依赖 span 字号信息）
  - pdfplumber（table_extractor）负责表格抽取与跨页合并
  - 扫描页（字符 < text_density_threshold）记入 failed_pages，留待 VLM 兜底
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF

# 同目录模块（运行 `python parse.py` 时 scripts/ 已在 sys.path）
sys.path.insert(0, str(Path(__file__).parent))
from numeric_normalizer import parse_number, detect_unit_in_context  # noqa: E402
from table_extractor import (                                       # noqa: E402
    Table,
    extract_tables_from_pdf,
)
from layout import reorder_reading_order, detect_two_columns         # noqa: E402
from vlm_fallback import (                                            # noqa: E402
    VLMError, extract_tables_via_vlm, vlm_config_from_env,
)

TEXT_DENSITY_THRESHOLD = 50  # 与 skill.config.example.yaml 默认值一致


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="pdf-finance-parser 主入口")
    p.add_argument("--input", required=True, help="输入 PDF 路径")
    p.add_argument("--output", required=True, help="输出目录（自动创建）")
    p.add_argument("--format", default="both", choices=["json", "markdown", "both"])
    p.add_argument("--config", default=None, help="skill.config.yaml 路径")
    p.add_argument("--pages", default=None, help="仅解析指定页范围，如 1-10,15")
    p.add_argument("--force_vlm", action="store_true", help="强制走 VLM 路径（MVP 未实现）")
    p.add_argument("--extract_statement", default=None,
                   choices=[None, "balance_sheet", "income_statement", "cash_flow"])
    p.add_argument("--password", default=None, help="加密 PDF 的密码")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args(argv)


def _parse_page_range(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(p for p in set(out) if 1 <= p <= total)


def _body_font_size(page: fitz.Page) -> float:
    """以该页 span 数量最多的字号为正文字号。"""
    sizes: list[float] = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                sizes.append(round(span["size"], 1))
    if not sizes:
        return 10.0
    return Counter(sizes).most_common(1)[0][0]


# 句末标点（heading 不应以此结尾，否则多半是被字号迷惑的正文）
_SENTENCE_END = set("。！？.!?")
# 续接标点（以此结尾说明半句话，绝不是 heading）
_CONTINUATION = set("，、,;；：:")


def _is_heading(span_size: float, body_size: float, text: str) -> bool:
    """更严格的 heading 启发式：字号 + 长度 + 标点联合判定。"""
    if span_size < body_size * 1.15:
        return False
    t = text.strip()
    if not t:
        return False
    if len(t) > 30:                    # 超过 30 字符极可能是正文
        return False
    last = t[-1]
    if last in _SENTENCE_END:          # 完整句子 → 正文
        return False
    if last in _CONTINUATION:          # 半句 → 正文续行
        return False
    return True


def _line_in_any_bbox(line_bbox: tuple, exclude: list) -> bool:
    """以行中心点是否落在任一 exclude bbox 内来判定。"""
    cx = (line_bbox[0] + line_bbox[2]) / 2
    cy = (line_bbox[1] + line_bbox[3]) / 2
    for bb in exclude:
        if bb[0] <= cx <= bb[2] and bb[1] <= cy <= bb[3]:
            return True
    return False


def extract_blocks(page: fitz.Page, page_num: int,
                   exclude_bboxes: list | None = None) -> list[dict[str, Any]]:
    """抽取文本 blocks；exclude_bboxes 内的行会被跳过（避免与表格重复）。"""
    exclude = exclude_bboxes or []
    body = _body_font_size(page)
    out: list[dict[str, Any]] = []
    for raw in page.get_text("dict").get("blocks", []):
        if raw.get("type") != 0:           # 0=text, 1=image
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


def _table_to_dict(t: Table, table_id: str) -> dict[str, Any]:
    """把 table_extractor.Table 转成 parse.py 下游使用的 dict（贴近 output_schema）。"""
    return {
        "table_id": table_id,
        "n_rows": t.n_rows,
        "n_cols": t.n_cols,
        "header_rows": t.header_rows,
        "engine": t.engine,
        "confidence": t.confidence,
        "source_page": t.page,                                     # 起始页
        "source_bbox": [round(v, 2) for v in t.bbox],
        "spans_pages": list(t.spans_pages),
        "cells": [
            {"row": c.row, "col": c.col, "text": c.text,
             "rowspan": c.rowspan, "colspan": c.colspan}
            for c in t.cells
        ],
    }


def write_table_files(tables: list[dict[str, Any]], out_dir: Path,
                      table_objs: list[Table]) -> None:
    """把每张表写成 tables/table_XXX.html 和 .csv（SKILL.md 承诺产物）。

    先删掉旧的 t_*.html / t_*.csv，避免上一次 run 多出来的残留文件混在里面。
    """
    tdir = out_dir / "tables"
    tdir.mkdir(parents=True, exist_ok=True)
    for old in list(tdir.glob("t_*.html")) + list(tdir.glob("t_*.csv")):
        old.unlink()
    for tdict, tobj in zip(tables, table_objs):
        stem = tdict["table_id"]
        (tdir / f"{stem}.html").write_text(tobj.to_html(), encoding="utf-8")
        (tdir / f"{stem}.csv").write_text(tobj.to_csv(), encoding="utf-8-sig")


_PARAGRAPH_END = set("。！？.!?")


def _join_text(prev: str, cur: str) -> str:
    """合并两段文本：英文/数字交界处加空格，CJK 不加。"""
    a = prev.rstrip()
    b = cur.lstrip()
    if not a:
        return b
    if not b:
        return a
    if a[-1].isascii() and a[-1].isalnum() and b[0].isascii() and b[0].isalnum():
        return f"{a} {b}"
    return a + b


def merge_consecutive_lines(blocks: list[dict]) -> tuple[list[dict], int]:
    """合并明显属于同一段的相邻 line blocks。返回 (合并后, 合并次数)。

    判定：同页、同 paragraph 类型、前一行不以句末标点结尾、垂直间距 < 1.2×行高。
    """
    if not blocks:
        return blocks, 0
    blocks = sorted(blocks, key=lambda b: (b["source_page"],
                                           b["source_bbox"][1],
                                           b["source_bbox"][0]))
    merged: list[dict] = [blocks[0].copy()]
    merge_count = 0
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
            merge_count += 1
        else:
            merged.append(cur.copy())
    return merged, merge_count


def _should_merge(prev: dict, cur: dict) -> bool:
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


_UNIT_DECL_RE = re.compile(r"单位\s*[:：]\s*([^\s币]+)")


def _collect_unit_declarations(blocks: list[dict]) -> list[tuple[int, float, str]]:
    """扫一遍所有 blocks，返回按 (page, top_y) 排序的 (page, top_y, 单位) 三元组。"""
    decls: list[tuple[int, float, str]] = []
    for b in blocks:
        u = detect_unit_in_context(b["text"])
        if u:
            decls.append((b["source_page"], b["source_bbox"][1], u))
    decls.sort()
    return decls


def find_table_unit(table: dict, decls: list[tuple[int, float, str]]) -> str | None:
    """从已收集的声明列表中找"出现在该表之前的最近一条"。

    跨页传播：财报常在某一页声明"单位：元"，后续页的表沿用该单位直到出现新声明。
    """
    page = table["source_page"]
    top_y = table["source_bbox"][1]
    current: str | None = None
    for dp, dy, du in decls:
        if dp < page or (dp == page and dy < top_y):
            current = du                # 保留最新的、出现在表前的声明
        else:
            break                       # decls 已排序，后续不会再 qualify
    return current


def _detect_percent_axes(table: dict) -> tuple[set[int], set[int]]:
    """识别表格中的"百分比列"和"百分比行"。

    启发式：
      - 一列被标为百分比 ⇔ 存在一个"全非数字"的行（候选表头行），且该行此列的文本含 %。
      - 一行被标为百分比 ⇔ 存在一个"全非数字"的列（候选标签列），且该列此行的文本含 %。
    这样可同时处理"标准表头表"和"key-value 式小表"。
    """
    cells_by_row: dict[int, list[dict]] = {}
    cells_by_col: dict[int, list[dict]] = {}
    for c in table["cells"]:
        cells_by_row.setdefault(c["row"], []).append(c)
        cells_by_col.setdefault(c["col"], []).append(c)

    percent_cols: set[int] = set()
    for row_cells in cells_by_row.values():
        if any(parse_number(c["text"]).parse_ok for c in row_cells):
            continue                                # 不是纯文本行，跳过
        for c in row_cells:
            if "%" in c["text"] or "％" in c["text"]:
                percent_cols.add(c["col"])

    percent_rows: set[int] = set()
    for col_cells in cells_by_col.values():
        if any(parse_number(c["text"]).parse_ok for c in col_cells):
            continue
        for c in col_cells:
            if "%" in c["text"] or "％" in c["text"]:
                percent_rows.add(c["row"])

    return percent_cols, percent_rows


def enrich_tables_with_numerics(tables: list[dict], blocks: list[dict]) -> int:
    """为每个 cell 增设 value / unit 字段。返回成功 parse 的 cell 数。"""
    decls = _collect_unit_declarations(blocks)
    parsed = 0
    for t in tables:
        unit_ctx = find_table_unit(t, decls)
        percent_cols, percent_rows = _detect_percent_axes(t)
        for cell in t["cells"]:
            is_percent = cell["col"] in percent_cols or cell["row"] in percent_rows
            cell_unit = "percent" if is_percent else unit_ctx
            nv = parse_number(cell["text"], default_unit=cell_unit)
            cell["value"] = nv.value
            cell["unit"] = nv.unit
            if nv.parse_ok:
                parsed += 1
    return parsed


# 页码模式：纯页码 / "1/12" / "第 1 页" / "Page 1" 等
_PAGE_NUM_PATTERNS = [
    re.compile(r"^\d+\s*[/／]\s*\d+$"),
    re.compile(r"^-?\s*\d+\s*-?$"),
    re.compile(r"^第\s*\d+\s*页$"),
    re.compile(r"^Page\s+\d+", re.IGNORECASE),
]


def _is_page_number(text: str) -> bool:
    t = text.strip()
    return any(p.match(t) for p in _PAGE_NUM_PATTERNS)


def filter_headers_footers(blocks: list[dict], page_heights: dict[int, float],
                           total_pages: int, band_ratio: float = 0.10
                           ) -> tuple[list[dict], list[dict]]:
    """剔除页眉/页脚。返回 (保留, 被剔除)。

    判定：
      1) 文本在 >= max(2, total_pages//2) 个不同页都出现 → recurring；
      2) 或者匹配纯页码 pattern；
    且 bbox 位于页面顶部/底部 band_ratio 带内 → 视为页眉/页脚。
    """
    from collections import defaultdict
    text_pages: dict[str, set[int]] = defaultdict(set)
    for b in blocks:
        text_pages[b["text"]].add(b["source_page"])
    threshold = max(2, total_pages // 2)
    recurring = {t for t, ps in text_pages.items() if len(ps) >= threshold}

    def at_edge(bbox: list[float], page_h: float) -> bool:
        top_band = page_h * band_ratio
        bot_band = page_h * (1 - band_ratio)
        return bbox[3] <= top_band or bbox[1] >= bot_band

    kept, removed = [], []
    for b in blocks:
        page_h = page_heights.get(b["source_page"], 842.0)  # A4 fallback
        if at_edge(b["source_bbox"], page_h) and (
            b["text"] in recurring or _is_page_number(b["text"])
        ):
            removed.append(b)
        else:
            kept.append(b)
    return kept, removed


def render_markdown(blocks: list[dict], tables: list[dict],
                    page_widths: dict[int, float] | None = None) -> str:
    """渲染 Markdown。识别为双栏的页：先输出左栏（按 y），再右栏，表格按 y 插入。"""
    page_widths = page_widths or {}
    blocks_by_page: dict[int, list[dict]] = {}
    for b in blocks:
        blocks_by_page.setdefault(b["source_page"], []).append(b)
    tables_by_page: dict[int, list[dict]] = {}
    for t in tables:
        tables_by_page.setdefault(t["source_page"], []).append(t)

    lines: list[str] = []
    for page in sorted(set(blocks_by_page) | set(tables_by_page)):
        lines.append(f"\n<!-- page {page} -->\n")
        page_blocks = blocks_by_page.get(page, [])
        page_w = page_widths.get(page, 0)
        # 双栏：先按 reading_order 把 blocks 排好；表格仍按 y 顺序插入到 blocks 之间
        if page_w and detect_two_columns(page_blocks, page_w) is not None:
            page_blocks = reorder_reading_order(page_blocks, page_w)
            ordered_items: list[tuple[str, dict]] = [("block", b) for b in page_blocks]
            # 表格按 y 插入：找最接近上方的 block 位置插入
            for t in sorted(tables_by_page.get(page, []), key=lambda x: x["source_bbox"][1]):
                t_top = t["source_bbox"][1]
                insert_at = len(ordered_items)
                for i, (_, item) in enumerate(ordered_items):
                    if item.get("type") and item["source_bbox"][1] > t_top:
                        insert_at = i
                        break
                ordered_items.insert(insert_at, ("table", t))
        else:
            # 单栏：按 y 排序，blocks 和 tables 混在一起
            items = [(b["source_bbox"][1], "block", b) for b in page_blocks]
            items += [(t["source_bbox"][1], "table", t)
                      for t in tables_by_page.get(page, [])]
            ordered_items = [(k, it) for _, k, it in sorted(items, key=lambda x: x[0])]

        for kind, item in ordered_items:
            if kind == "block":
                if item["type"] == "heading":
                    lines.append(f"## {item['text']}\n")
                else:
                    lines.append(item["text"] + "\n")
            else:
                # 把锚 cell 的文本铺到所有被覆盖的 (row, col)，让 Markdown 可读
                rows: dict[int, dict[int, str]] = {}
                for c in item["cells"]:
                    rs = c.get("rowspan", 1)
                    cs = c.get("colspan", 1)
                    for r_off in range(rs):
                        for c_off in range(cs):
                            rows.setdefault(c["row"] + r_off, {})[c["col"] + c_off] = c["text"]
                n_cols = item["n_cols"]
                hr = max(1, item.get("header_rows", 1))
                # 多级表头按列拼接（去重保序）
                if hr == 1:
                    header = [rows.get(0, {}).get(i, "") for i in range(n_cols)]
                else:
                    header = []
                    for i in range(n_cols):
                        seen: set[str] = set()
                        parts: list[str] = []
                        for r in range(hr):
                            t = rows.get(r, {}).get(i, "")
                            if t and t not in seen:
                                parts.append(t)
                                seen.add(t)
                        header.append(" / ".join(parts))
                lines.append("| " + " | ".join(header) + " |")
                lines.append("|" + "|".join([" --- "] * n_cols) + "|")
                for r in sorted(k for k in rows if k >= hr):
                    vals = [rows[r].get(i, "") for i in range(n_cols)]
                    lines.append("| " + " | ".join(vals) + " |")
                lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    doc = fitz.open(args.input)
    if doc.is_encrypted:
        if not args.password or not doc.authenticate(args.password):
            print("[ERROR] PDF 加密，请通过 --password 提供密码（E001）", file=sys.stderr)
            return 1

    pages = _parse_page_range(args.pages, len(doc))
    page_heights: dict[int, float] = {}
    routing = {"text_pages": 0, "scan_pages": 0, "vlm_pages": 0}
    failed: list[dict] = []

    # Phase 1: 按字符密度路由页面
    text_pages: list[int] = []
    for pn in pages:
        page = doc[pn - 1]
        page_heights[pn] = page.rect.height
        if len(page.get_text().strip()) < TEXT_DENSITY_THRESHOLD:
            routing["scan_pages"] += 1
            failed.append({"page": pn, "reason": "scanned_page_mvp_unsupported"})
        else:
            routing["text_pages"] += 1
            text_pages.append(pn)

    # Phase 2: 一次性抽表（跨页合并需要全局视角）
    table_objs: list[Table] = []
    if text_pages:
        try:
            table_objs = extract_tables_from_pdf(args.input, pages=text_pages)
        except Exception as e:
            failed.append({"page": -1, "reason": f"table_extractor: {type(e).__name__}: {e}"})

    all_tables: list[dict] = [_table_to_dict(t, f"t_{i:03d}")
                              for i, t in enumerate(table_objs, 1)]

    # 每页要 exclude 的表格 bbox（含跨页延续页）
    bboxes_by_page: dict[int, list[list[float]]] = defaultdict(list)
    for t in table_objs:
        for p, bb in t.bboxes_by_page.items():
            bboxes_by_page[p].append([round(v, 2) for v in bb])

    # Phase 3: 按页抽 blocks（fitz 路径）；多栏阅读顺序在 render 阶段才重排
    all_blocks: list[dict] = []
    page_widths: dict[int, float] = {}
    two_col_pages: list[int] = []
    for pn in text_pages:
        page = doc[pn - 1]
        page_widths[pn] = page.rect.width
        try:
            blocks_on_page = extract_blocks(page, pn,
                                            exclude_bboxes=bboxes_by_page.get(pn, []))
            if detect_two_columns(blocks_on_page, page.rect.width) is not None:
                two_col_pages.append(pn)
            all_blocks.extend(blocks_on_page)
        except Exception as e:
            failed.append({"page": pn, "reason": f"{type(e).__name__}: {e}"})

    # Phase 3.5: VLM 兜底（扫描页 / --force_vlm）
    vlm_pages_processed: list[int] = []
    pages_for_vlm: list[int] = []
    if args.force_vlm:
        pages_for_vlm = list(pages)                                    # 强制 → 所有选定页
    else:
        # 自动：仅扫描页（之前进了 failed）
        pages_for_vlm = [f["page"] for f in failed
                         if f.get("reason", "").startswith("scanned_page")]
    if pages_for_vlm:
        cfg = vlm_config_from_env()
        if cfg is None:
            print("[parse.py] VLM 跳过：未配置 ARK_API_KEY / OPENAI_API_KEY",
                  file=sys.stderr)
        else:
            for pn in pages_for_vlm:
                try:
                    vlm_tables = extract_tables_via_vlm(args.input, pn, cfg)
                    for i, t in enumerate(vlm_tables, start=len(table_objs) + 1):
                        table_objs.append(t)
                        all_tables.append(_table_to_dict(t, f"t_{i:03d}"))
                    vlm_pages_processed.append(pn)
                    routing["vlm_pages"] += 1
                    # 从 failed 列表里移除该页
                    failed = [f for f in failed if f.get("page") != pn]
                except VLMError as e:
                    failed.append({"page": pn, "reason": f"VLMError: {e}"})

    # 后处理顺序：先过滤页眉页脚 → 再合并跨行段落 → 最后给 cells 注入 value/unit
    all_blocks, removed = filter_headers_footers(all_blocks, page_heights, len(doc))
    all_blocks, merge_count = merge_consecutive_lines(all_blocks)
    parsed_cells = enrich_tables_with_numerics(all_tables, all_blocks)

    # Phase 4: 写 tables/table_XXX.html + .csv
    if all_tables:
        write_table_files(all_tables, out_dir, table_objs)

    output = {
        "doc_id": Path(args.input).stem,
        "source_file": args.input,
        "pages": len(doc),
        "language": "zh",
        "blocks": all_blocks,
        "tables": all_tables,
    }
    if args.format in ("json", "both"):
        (out_dir / "output.json").write_text(
            json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.format in ("markdown", "both"):
        (out_dir / "output.md").write_text(
            render_markdown(all_blocks, all_tables, page_widths), encoding="utf-8")

    engine_counts = Counter(t["engine"] for t in all_tables)
    meta = {
        "input": args.input,
        "output_dir": str(out_dir),
        "wall_time_seconds": round(time.time() - t0, 3),
        "routing": routing,
        "failed_pages": failed,
        "n_blocks": len(all_blocks),
        "n_tables": len(all_tables),
        "n_tables_cross_page": sum(1 for t in all_tables if len(t["spans_pages"]) > 1),
        "n_tables_with_merged_cells": sum(
            1 for t in all_tables
            if any(c["rowspan"] > 1 or c["colspan"] > 1 for c in t["cells"])
        ),
        "n_tables_multi_level_header": sum(
            1 for t in all_tables if t.get("header_rows", 1) > 1
        ),
        "two_column_pages": two_col_pages,
        "vlm_pages_processed": vlm_pages_processed,
        "table_engines": dict(engine_counts),
        "n_header_footer_removed": len(removed),
        "n_lines_merged": merge_count,
        "n_cells_parsed_as_number": parsed_cells,
        "status": "ok" if not failed else "partial",
    }
    (out_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[parse.py] {len(all_blocks)} blocks ({merge_count} merged), "
          f"{len(all_tables)} tables ({meta['n_tables_cross_page']} cross-page, "
          f"{parsed_cells} numeric cells), "
          f"text={routing['text_pages']} scan={routing['scan_pages']} "
          f"hdr/ftr removed={len(removed)} failed={len(failed)} | "
          f"{meta['wall_time_seconds']}s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
