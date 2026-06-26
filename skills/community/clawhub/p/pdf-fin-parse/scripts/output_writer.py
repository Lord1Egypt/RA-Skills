"""LAS 后处理结果 → output.json (符合 assets/output_schema.json) + output.md.

把 MergedTable 链转换成 schema-compliant 的 tables 数组：
  - 仅输出 anchor cells（合并锚点）+ rowspan/colspan，下游可重建网格
  - 每个 cell 含：row/col/rowspan/colspan/text/value/unit/_raw
  - table 含：table_id/caption/n_rows/n_cols/cells/source_page(s)/engine
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from cross_page_merger import MergedTable
from finance_terms_aligner import (
    classify_row_label, detect_statement_type, is_subtotal_row,
)
from finance_validator import ValidationReport, validate
from html_table_parser import ParsedTable
from multi_header_detector import compute_column_paths
from numeric_normalizer import detect_unit_in_context, parse_number


# ---------------------------------------------------------------------------
# 一张 MergedTable → schema 的 tables[] 元素
# ---------------------------------------------------------------------------

def _row_label_of(merged: MergedTable, row: int) -> str:
    """返回该 row 第 0 列的文本（行标签）。"""
    for c in merged.cells:
        if c.row == row and c.col == 0 and c.is_anchor:
            return c.text
    return ""


def _data_columns(merged: MergedTable) -> List[int]:
    """非标签列（默认 col 0 是 row label，1.. 是数值列）。"""
    return list(range(1, merged.n_cols))


def merged_table_to_schema(merged: MergedTable,
                            table_id: str,
                            context_text: str = "",
                            engine: str = "vlm-ark") -> Dict[str, Any]:
    """转换单张 MergedTable 为 schema 兼容 dict（含 cells / source_page / validation）。

    engine 字段受 schema 约束 enum；P2 LAS 输出暂归在 "vlm-ark"（与之前 v0.2 同源 provider）。
    后续如需新增 "las/las_pdf_parse_doubao" 枚举可改 schema。
    """
    default_unit = detect_unit_in_context(context_text)
    statement_type = detect_statement_type(merged.caption, context_text)

    # 数值规整：在每个 anchor data cell 上算 value/unit
    schema_cells: List[Dict[str, Any]] = []
    for c in merged.cells:
        if not c.is_anchor:
            continue
        cell_out: Dict[str, Any] = {
            "row": c.row, "col": c.col,
            "text": c.text,
        }
        if c.rowspan != 1:
            cell_out["rowspan"] = c.rowspan
        if c.colspan != 1:
            cell_out["colspan"] = c.colspan

        # 表头单元格不做数值规整
        if c.is_header or c.row < merged.header_rows:
            schema_cells.append(cell_out)
            continue
        # 数据行：仅对非 row-label 列（col >= 1）做数值
        if c.col == 0:
            schema_cells.append(cell_out)
            continue

        nv = parse_number(c.text, default_unit=default_unit)
        if nv.parse_ok and nv.value is not None:
            cell_out["value"] = nv.value
            if nv.unit:
                cell_out["unit"] = nv.unit
        else:
            cell_out["value"] = None
            cell_out["unit"] = None
        if nv.raw != c.text:
            cell_out["_raw"] = nv.raw
        schema_cells.append(cell_out)

    # 跑业务规则校验（balance_sheet 才有效）
    rep = _run_validation(merged, schema_cells, statement_type)

    out: Dict[str, Any] = {
        "table_id": table_id,
        "caption": merged.caption or "",
        "n_rows": merged.n_rows,
        "n_cols": merged.n_cols,
        "engine": engine,
        "confidence": 1.0,
        "cells": schema_cells,
    }
    # source_page 字段 schema 要求 int；跨页表给 source_pages 数组 + source_page=首页
    if merged.source_pages:
        out["source_page"] = merged.source_pages[0]
        if len(merged.source_pages) > 1:
            out["source_pages"] = merged.source_pages
    else:
        out["source_page"] = 1

    # source_bbox 我们暂时没准（LAS detail.box 可补，留到 P2.5）
    out["source_bbox"] = [0.0, 0.0, 0.0, 0.0]

    # 派生信息（非 schema 必须字段，但有用）
    if statement_type:
        out["statement_type"] = statement_type
    if merged.column_paths:
        out["column_paths"] = merged.column_paths
    if merged.header_rows:
        out["header_rows"] = merged.header_rows
    if default_unit:
        out["declared_unit"] = default_unit
    if rep.warnings:
        out["validation"] = {
            "stats": rep.stats,
            "warnings": [w.__dict__ for w in rep.warnings],
        }
    return out


def _run_validation(merged: MergedTable,
                     schema_cells: List[Dict[str, Any]],
                     statement_type: Optional[str]) -> ValidationReport:
    if statement_type != "balance_sheet":
        return ValidationReport()
    # 转成 finance_validator.validate 期望的 rows 视图
    by_row: Dict[int, Dict[int, Dict[str, Any]]] = {}
    for c in schema_cells:
        by_row.setdefault(c["row"], {})[c["col"]] = c
    rows: List[Dict[str, Any]] = []
    for r in sorted(by_row.keys()):
        if r < merged.header_rows:
            continue
        label_cell = by_row[r].get(0, {})
        cells_view: Dict[int, Optional[float]] = {}
        for col, cell in by_row[r].items():
            if col == 0:
                continue
            cells_view[col] = cell.get("value")
        rows.append({
            "row_label": label_cell.get("text", ""),
            "cells": cells_view,
        })
    data_cols = list(range(1, merged.n_cols))
    return validate(rows, data_cols, statement_type)


# ---------------------------------------------------------------------------
# 顶层：LAS resp + merged tables → output.json + output.md
# ---------------------------------------------------------------------------

def build_output_doc(las_resp: Dict[str, Any],
                      merged_tables_with_ctx: List[tuple[MergedTable, str]],
                      doc_id: str,
                      source_file: str,
                      pages: int,
                      engine: str = "vlm-ark") -> Dict[str, Any]:
    """组装 output.json。

    Args:
        las_resp: 原始 LAS 响应（暂只用 detail[].page_md 拼回 output.md）
        merged_tables_with_ctx: [(MergedTable, context_text), ...]
        doc_id / source_file / pages: 元信息
        engine: schema 受限的 enum 之一
    """
    tables_out: List[Dict[str, Any]] = []
    for i, (mt, ctx) in enumerate(merged_tables_with_ctx):
        tables_out.append(
            merged_table_to_schema(mt, table_id=f"t{i + 1}", context_text=ctx,
                                    engine=engine)
        )

    blocks: List[Dict[str, Any]] = []   # P2 阶段先空，P2.5 用 text_blocks 填充

    doc = {
        "doc_id": doc_id,
        "source_file": source_file,
        "pages": pages,
        "language": "zh",
        "blocks": blocks,
        "tables": tables_out,
    }
    return doc


def write_output_files(out_dir: Path,
                        doc: Dict[str, Any],
                        markdown: str) -> Dict[str, str]:
    """落盘 output.json + output.md，返回 {key: path}。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "output.json"
    md_path = out_dir / "output.md"
    json_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2),
                          encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {"output_json": str(json_path), "output_md": str(md_path)}
