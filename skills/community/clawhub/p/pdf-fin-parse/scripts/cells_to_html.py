"""把 output_schema 形态的 cells[] 反向序列化成 HTML <table>.

用途：
  1. 跨页合并后整张逻辑表 → 输出 HTML，用于 X-TEDS 评测
  2. GT 标注辅助：v0.3 自动合并结果 → HTML 初稿，人工在初稿上校对
"""
from __future__ import annotations

from html import escape
from typing import Any, Dict, Iterable, List, Tuple


def _cells_by_pos(cells: Iterable[Dict[str, Any]]
                  ) -> Tuple[Dict[Tuple[int, int], Dict[str, Any]], int, int]:
    """{(row, col): anchor_cell} + (n_rows, n_cols)。仅保留 anchor（rowspan/colspan 用属性表达）。"""
    by_pos: Dict[Tuple[int, int], Dict[str, Any]] = {}
    n_rows = 0
    n_cols = 0
    for c in cells:
        r = c.get("row")
        col = c.get("col")
        if r is None or col is None:
            continue
        by_pos[(r, col)] = c
        n_rows = max(n_rows, r + 1)
        n_cols = max(n_cols, col + c.get("colspan", 1))
    return by_pos, n_rows, n_cols


def cells_to_html(cells: List[Dict[str, Any]], *,
                   header_rows: int = 0,
                   prefer_value: bool = False) -> str:
    """渲染 cells[] 为 <table>。

    Args:
        header_rows: 前 N 行用 <thead><th>，后面用 <tbody><td>
        prefer_value: True 时数据 cell 用 value（数字 + 千分位）；False 用 text 原文。
                      X-TEDS 评测建议 False（与 GT 原文形态一致）。
    """
    by_pos, n_rows, n_cols = _cells_by_pos(cells)
    if n_rows == 0:
        return "<table></table>"

    occupied: Dict[Tuple[int, int], bool] = {}
    # 标记非锚位置（按 rowspan/colspan 展开）
    for (r, c), cell in by_pos.items():
        rs = max(1, cell.get("rowspan", 1))
        cs = max(1, cell.get("colspan", 1))
        for dr in range(rs):
            for dc in range(cs):
                if dr == 0 and dc == 0:
                    continue
                occupied[(r + dr, c + dc)] = True

    def _cell_text(cell: Dict[str, Any]) -> str:
        if prefer_value and cell.get("value") is not None:
            v = cell["value"]
            if isinstance(v, float) and v.is_integer():
                v = int(v)
            return f"{v:,}" if isinstance(v, (int, float)) else str(v)
        return cell.get("text", "")

    out: List[str] = ["<table>"]
    in_thead = header_rows > 0
    in_tbody = False
    if in_thead:
        out.append("<thead>")

    for r in range(n_rows):
        if in_thead and r >= header_rows:
            out.append("</thead>")
            out.append("<tbody>")
            in_thead = False
            in_tbody = True
        if not in_thead and not in_tbody and r >= header_rows:
            out.append("<tbody>")
            in_tbody = True

        out.append("<tr>")
        for c in range(n_cols):
            if occupied.get((r, c)):
                continue
            cell = by_pos.get((r, c))
            tag = "th" if r < header_rows else "td"
            if cell is None:
                out.append(f"<{tag}></{tag}>")
                continue
            attrs = []
            rs = cell.get("rowspan", 1)
            cs = cell.get("colspan", 1)
            if rs and rs != 1:
                attrs.append(f'rowspan="{rs}"')
            if cs and cs != 1:
                attrs.append(f'colspan="{cs}"')
            attr_str = (" " + " ".join(attrs)) if attrs else ""
            text = escape(_cell_text(cell))
            out.append(f"<{tag}{attr_str}>{text}</{tag}>")
        out.append("</tr>")

    if in_thead:
        out.append("</thead>")
    if in_tbody:
        out.append("</tbody>")
    out.append("</table>")
    return "".join(out)
