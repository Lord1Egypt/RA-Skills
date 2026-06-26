"""跨页表格合并.

LAS 单独解析每页，跨页延续的报表会被切成多张 ParsedTable（典型场景：
合并资产负债表 → 资产端 / 负债端 / 权益端 跨 2-3 页）。

合并启发式（按"且"关系，全满足才合并）：
  1. 后一张表的 caption 含 "(续)" / "（续）" 关键词，**或**
     前一张表 caption 与后一张表 caption 主标题相同（去除 "(续)" 后缀比对）
  2. 列结构匹配：两张表的 n_cols 相同 且 column_paths 完全相等
  3. 页号相邻（page_b == page_a + 1）

不合并的边界：跨页时同一表的 thead 会重复一次，合并时**舍弃**后一张表的 header_rows
（默认 = 前一张的 header_rows）。

输出：MergedTable，cells 重新编号（保留 source_page 记录每个 cell 原属页）
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from html_table_parser import ParsedCell, ParsedTable
from multi_header_detector import annotate_table


_CONTINUATION_PATTERNS = [
    re.compile(r"[（(]\s*续\s*[）)]"),
    re.compile(r"\s+续\s*$"),
    re.compile(r"\(continued\)", re.IGNORECASE),
]


@dataclass
class PageTable:
    """ParsedTable + 它所在的页信息。供 merger 使用。"""
    page_id: int
    table: ParsedTable
    caption: Optional[str] = None
    header_rows: int = 0
    column_paths: List[str] = field(default_factory=list)


@dataclass
class MergedTable:
    """跨页合并后的表格。"""
    cells: List[ParsedCell] = field(default_factory=list)
    n_rows: int = 0
    n_cols: int = 0
    header_rows: int = 0
    column_paths: List[str] = field(default_factory=list)
    caption: Optional[str] = None
    source_pages: List[int] = field(default_factory=list)
    # 每行的源页号（便于 audit）
    row_source_page: List[int] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 启发式判定
# ---------------------------------------------------------------------------

def _strip_continuation(caption: str) -> str:
    """去掉 "(续)" / "（续）" 后缀，返回 stem。"""
    if not caption:
        return ""
    s = caption
    for pat in _CONTINUATION_PATTERNS:
        s = pat.sub("", s)
    return s.strip()


def _is_continuation_caption(caption: str) -> bool:
    if not caption:
        return False
    return any(pat.search(caption) for pat in _CONTINUATION_PATTERNS)


def can_merge(prev: PageTable, curr: PageTable) -> bool:
    """是否应把 curr 并入 prev 的延续。"""
    # 1) 页号相邻
    if curr.page_id != prev.page_id + 1:
        return False
    # 2) 列结构必须一致
    if prev.column_paths != curr.column_paths:
        return False
    if prev.table.n_cols != curr.table.n_cols:
        return False
    # 3) 续表判定：curr 自带 "(续)" OR 同主标题
    if _is_continuation_caption(curr.caption):
        return True
    if (prev.caption and curr.caption
            and _strip_continuation(prev.caption) == _strip_continuation(curr.caption)):
        return True
    return False


# ---------------------------------------------------------------------------
# 实际合并
# ---------------------------------------------------------------------------

def _append_data_rows(target: MergedTable, src: ParsedTable,
                      page_id: int, drop_header_rows: int) -> None:
    """把 src 的非表头数据行（跳过 drop_header_rows 行）追加到 target，重排 row。"""
    base_row = target.n_rows
    for c in src.cells:
        if c.row < drop_header_rows:
            continue
        target.cells.append(ParsedCell(
            row=base_row + (c.row - drop_header_rows),
            col=c.col,
            rowspan=c.rowspan, colspan=c.colspan,
            text=c.text, is_header=c.is_header,
            is_anchor=c.is_anchor,
            raw_html=c.raw_html,
        ))
    added_rows = max(
        (c.row - drop_header_rows for c in src.cells if c.row >= drop_header_rows),
        default=-1,
    ) + 1
    for i in range(added_rows):
        target.row_source_page.append(page_id)
    target.n_rows = base_row + added_rows


def merge_chain(page_tables: List[PageTable]) -> MergedTable:
    """把已确认应合并的一串 PageTable 拼成一张 MergedTable。

    Caller 负责确保 page_tables 已经按页号排序且两两 can_merge。
    """
    if not page_tables:
        return MergedTable()

    head = page_tables[0]
    merged = MergedTable(
        n_cols=head.table.n_cols,
        header_rows=head.header_rows,
        column_paths=list(head.column_paths),
        caption=_strip_continuation(head.caption) if head.caption else None,
        source_pages=[head.page_id],
    )
    # 头表全量入（保留 header）
    for c in head.table.cells:
        merged.cells.append(ParsedCell(
            row=c.row, col=c.col,
            rowspan=c.rowspan, colspan=c.colspan,
            text=c.text, is_header=c.is_header,
            is_anchor=c.is_anchor, raw_html=c.raw_html,
        ))
    # 头表的每行记录页号
    merged.n_rows = head.table.n_rows
    for _ in range(head.table.n_rows):
        merged.row_source_page.append(head.page_id)

    # 后续表：跳过 header_rows 行，追加数据行
    for pt in page_tables[1:]:
        _append_data_rows(merged, pt.table, pt.page_id,
                          drop_header_rows=pt.header_rows)
        merged.source_pages.append(pt.page_id)

    return merged


# ---------------------------------------------------------------------------
# 顶层入口
# ---------------------------------------------------------------------------

def build_page_tables(pages: List[tuple[int, ParsedTable]]) -> List[PageTable]:
    """ [(page_id, ParsedTable), ...] → [PageTable]，已 annotate header_rows / column_paths。"""
    out = []
    for page_id, tab in pages:
        info = annotate_table(tab)
        out.append(PageTable(
            page_id=page_id, table=tab,
            caption=tab.caption(),
            header_rows=info["header_rows"],
            column_paths=info["column_paths"],
        ))
    return out


def merge_across_pages(page_tables: List[PageTable]) -> List[MergedTable]:
    """主入口：对一组 PageTable（同一文档全部表），按页相邻+列结构+续表判定分组合并。

    返回 List[MergedTable]，未合并的单页表也会以 1-元素 chain 形式产出 MergedTable。
    """
    if not page_tables:
        return []
    # 按 page_id 稳定排序
    sorted_pts = sorted(page_tables, key=lambda p: p.page_id)

    chains: List[List[PageTable]] = [[sorted_pts[0]]]
    for pt in sorted_pts[1:]:
        prev = chains[-1][-1]
        if can_merge(prev, pt):
            chains[-1].append(pt)
        else:
            chains.append([pt])

    return [merge_chain(chain) for chain in chains]
