"""多级表头识别 + 列路径计算.

LAS HTML 表里 <th> 已是表头先验，但仍存在"<td> 当表头用"（类目行如"资产："）的情况，
且我们需要把"本集团 / 2026年3月31日 / 未经审计"这种 N 级表头展平为每列的 column_path。

输出：
  - header_rows:  int      表头占用的行数（连续从顶部开始）
  - column_paths: List[str]  长度 = n_cols，每列的拼接表头路径
"""
from __future__ import annotations

from typing import List

from html_table_parser import ParsedCell, ParsedTable


def _row_is_pure_header(cells_in_row: List[ParsedCell]) -> bool:
    """这一行是否完全由表头单元格（is_header=True）组成。"""
    if not cells_in_row:
        return False
    return all(c.is_header for c in cells_in_row)


def detect_header_rows(table: ParsedTable) -> int:
    """从顶部开始数：连续的"全表头"行数。

    LAS 通常正确把 <thead> 内的 <th> 标了 is_header=True，本函数主要做兜底。
    """
    by_row: dict[int, List[ParsedCell]] = {}
    for c in table.cells:
        by_row.setdefault(c.row, []).append(c)

    n_header = 0
    for r in sorted(by_row.keys()):
        if _row_is_pure_header(by_row[r]):
            n_header += 1
        else:
            break
    return n_header


def compute_column_paths(table: ParsedTable, header_rows: int,
                         separator: str = " / ") -> List[str]:
    """根据表头行构造每列的 column_path。

    多级表头（带 colspan）也能正确处理：表头单元格的文本会在它覆盖的所有列上传播。
    （因为 parse_table 已经把合并单元格展开成 anchor + 非锚 placeholder，
     这里我们用每行每列 anchor 锚点对应的文本，再按层级拼接。）
    """
    if header_rows <= 0 or table.n_cols <= 0:
        return ["" for _ in range(table.n_cols)]

    # 按 (row, col) 找该位置的"有效文本"：anchor 取本身 text，非锚回溯到所在 anchor
    # 但 parse_table 已把非锚 cell 文本设为 ""，且 anchor 的 rowspan/colspan 信息保留 →
    # 我们重新展开 anchor 文本到它覆盖的格子
    grid: dict[tuple[int, int], str] = {}
    for c in table.cells:
        if not c.is_anchor:
            continue
        for dr in range(c.rowspan):
            for dc in range(c.colspan):
                grid[(c.row + dr, c.col + dc)] = c.text

    column_paths: List[str] = []
    for col in range(table.n_cols):
        layers: List[str] = []
        for r in range(header_rows):
            txt = grid.get((r, col), "").strip()
            if not txt:
                continue
            # 同一文本（rowspan/colspan 引起的重复）去重
            if not layers or layers[-1] != txt:
                layers.append(txt)
        # 合并文本里的换行（"2026年\n3月31日\n(未经审计)" → 同层）
        flat = [ly.replace("\n", "") for ly in layers]
        column_paths.append(separator.join(flat))
    return column_paths


def annotate_table(table: ParsedTable, separator: str = " / ") -> dict:
    """便捷入口：返回 {"header_rows": ..., "column_paths": [...]}.

    不修改 table，仅返回派生信息。
    """
    hr = detect_header_rows(table)
    return {
        "header_rows": hr,
        "column_paths": compute_column_paths(table, hr, separator),
    }
