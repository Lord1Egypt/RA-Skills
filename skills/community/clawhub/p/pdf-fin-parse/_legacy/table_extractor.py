"""表格抽取：pdfplumber + 跨页合并。

实现思路（详见 [process.md](../../../process.md)）：
  1. 逐页用 pdfplumber 按线条提取 → 清洗（去空行、页码、混入的页眉/页脚）
  2. 判断当前页表格是否为上一页表格的延续（列数一致 + 物理位置贴边）
  3. 合并时去掉重复表头、修复跨页断开的同一行
  4. ``self_assess`` 给每张表打分，<阈值的可交 VLM 兜底
"""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from html import escape as html_escape
from typing import Iterable

try:
    import pdfplumber
except ImportError:                         # pragma: no cover - 由调用方在运行时报错
    pdfplumber = None


# 财报表格多数带边框；用 "lines" 策略最稳
DEFAULT_TABLE_SETTINGS: dict = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "intersection_tolerance": 5,
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 20,
    "min_words_vertical": 1,
    "min_words_horizontal": 1,
}

# 常见财报表头关键词，用于识别跨页重复出现的表头
DEFAULT_HEADER_KEYWORDS: tuple[str, ...] = (
    "项目", "本期", "上期", "上年", "同期", "同比",
    "增减", "金额", "原因", "占比", "比例", "期末", "期初",
)

# 跨页合并的几何判据：上一页表格底端 / 当前页表格顶端 距页边的占比阈值
PAGE_EDGE_RATIO_BOTTOM = 0.15               # 上一页表必须在底部 15% 带内
PAGE_EDGE_RATIO_TOP = 0.30                  # 当前页表必须在顶部 30% 带内（页眉占用）

# 与上一张表表头的相似度阈值，>= 此值即视为重复表头
HEADER_SIM_THRESHOLD = 0.6

# self_assess 给出的默认"低置信度"阈值，调用方据此决定是否交 VLM
LOW_CONFIDENCE_THRESHOLD = 0.6


@dataclass
class TableCell:
    row: int
    col: int
    text: str
    rowspan: int = 1
    colspan: int = 1


@dataclass
class Table:
    page: int                                                # 起始页（合并后保留首页号）
    bbox: tuple[float, float, float, float]                  # 起始页内 bbox
    cells: list[TableCell] = field(default_factory=list)
    n_rows: int = 0
    n_cols: int = 0
    engine: str = ""                                         # "pdfplumber" | "pdfplumber_text" | "vlm" | ...
    confidence: float = 0.0
    spans_pages: list[int] = field(default_factory=list)     # 该表跨越的所有页号
    header_rows: int = 1                                     # 多级表头行数（由 _detect_header_rows 推断）
    # 每页内该表的 bbox；供调用方（如 parse.py）在每页提取段落时 exclude 表格区域
    bboxes_by_page: dict[int, tuple[float, float, float, float]] = field(default_factory=dict)

    def to_rows(self, fill_merged: bool = True) -> list[list[str]]:
        """转回二维 list[list[str]]。

        fill_merged=True 时把合并单元格的文本填到被覆盖的位置（适合 CSV / 阅读）；
        False 时只在锚位置放文本，覆盖位为空串（适合需要还原 span 的下游）。
        """
        grid = [[""] * self.n_cols for _ in range(self.n_rows)]
        for cell in self.cells:
            if not (0 <= cell.row < self.n_rows and 0 <= cell.col < self.n_cols):
                continue
            if fill_merged and (cell.rowspan > 1 or cell.colspan > 1):
                for r in range(cell.row, min(cell.row + cell.rowspan, self.n_rows)):
                    for c in range(cell.col, min(cell.col + cell.colspan, self.n_cols)):
                        grid[r][c] = cell.text
            else:
                grid[cell.row][cell.col] = cell.text
        return grid

    def to_markdown(self) -> str:
        """Markdown 表格输出。多级表头按列拼接成单行（用 ' / ' 连接、去重）。"""
        rows = self.to_rows(fill_merged=True)
        if len(rows) < 2 or self.n_cols == 0:
            return ""
        hr = max(1, min(self.header_rows, len(rows)))
        if hr == 1:
            header = rows[0]
        else:
            header = []
            for c in range(self.n_cols):
                seen: set[str] = set()
                parts: list[str] = []
                for r in range(hr):
                    t = rows[r][c]
                    if t and t not in seen:
                        parts.append(t)
                        seen.add(t)
                header.append(" / ".join(parts))
        sep = "|" + "|".join([" --- "] * self.n_cols) + "|"
        body = ["| " + " | ".join(r) + " |" for r in rows[hr:]]
        return "\n".join(["| " + " | ".join(header) + " |", sep, *body])

    def to_html(self) -> str:
        """HTML 表格，正确使用 rowspan/colspan 属性。前 header_rows 行进 <thead>。"""
        if not self.cells:
            return "<table></table>"
        by_row: dict[int, list[TableCell]] = {}
        for c in self.cells:
            by_row.setdefault(c.row, []).append(c)

        def render_row(cells: list[TableCell], tag: str) -> str:
            parts = ["<tr>"]
            for cell in sorted(cells, key=lambda x: x.col):
                attrs = ""
                if cell.rowspan > 1:
                    attrs += f' rowspan="{cell.rowspan}"'
                if cell.colspan > 1:
                    attrs += f' colspan="{cell.colspan}"'
                parts.append(f"<{tag}{attrs}>{html_escape(cell.text)}</{tag}>")
            parts.append("</tr>")
            return "".join(parts)

        hr = max(1, min(self.header_rows, self.n_rows))
        parts: list[str] = ['<table border="1">', "<thead>"]
        for r in range(hr):
            parts.append(render_row(by_row.get(r, []), "th"))
        parts.append("</thead>")
        if self.n_rows > hr:
            parts.append("<tbody>")
            for r in range(hr, self.n_rows):
                parts.append(render_row(by_row.get(r, []), "td"))
            parts.append("</tbody>")
        parts.append("</table>")
        return "".join(parts)

    def to_csv(self) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        for row in self.to_rows(fill_merged=True):
            writer.writerow(row)
        return buf.getvalue()


# ─────────────────────────── 单元格 / 行级清洗 ───────────────────────────

_PAGE_NUM_PATTERNS = (
    re.compile(r"^\s*\d+\s*[/／]\s*\d+\s*$"),               # 4 / 12
    re.compile(r"^-?\s*\d+\s*-?$"),                          # 4 / -4-
    re.compile(r"^第\s*\d+\s*页(?:\s*共\s*\d+\s*页)?$"),
    re.compile(r"^Page\s+\d+", re.IGNORECASE),
)

_REPORT_TITLE_PAT = re.compile(
    r"(第[一二三四]季度报告|半年度报告|年度报告|招股说明书|10-?K)"
)


def _clean_cell(value: object | None) -> str:
    """折叠空白；剔除 CJK 字符间被 PDF 文本流强加的空格。"""
    if value is None:
        return ""
    s = re.sub(r"\s+", " ", str(value)).strip()
    s = re.sub(r"([一-鿿])\s+([一-鿿])", r"\1\2", s)
    return s


def _is_page_marker(line: str) -> bool:
    s = line.strip()
    return any(p.match(s) for p in _PAGE_NUM_PATTERNS)


def _is_header_footer_row(row: list[str]) -> bool:
    """页眉/页脚被误提为表格行：非空 cell 极少且含报告标题特征词。"""
    non_empty = [c for c in row if c]
    if len(non_empty) > 2:
        return False
    return bool(_REPORT_TITLE_PAT.search(" ".join(non_empty)))


def _clean_table_rows_with_indices(
    table: list[list[str | None]],
) -> tuple[list[list[str]], list[int]]:
    """清洗 + 返回保留下来的原始行号（用于 span 映射）。"""
    out: list[list[str]] = []
    kept: list[int] = []
    for ri, raw_row in enumerate(table):
        row = [_clean_cell(c) for c in raw_row]
        if not any(row):
            continue
        line = " ".join(row)
        if _is_page_marker(line):
            continue
        if _is_header_footer_row(row):
            continue
        out.append(row)
        kept.append(ri)
    return out, kept


def clean_table_rows(table: list[list[str | None]]) -> list[list[str]]:
    """清洗 pdfplumber 原始 rows：去空行 / 页码 / 页眉 / 折叠空白。"""
    rows, _ = _clean_table_rows_with_indices(table)
    return rows


# ─────────────────────────── 合并单元格识别 ───────────────────────────


def _detect_spans(pl_table) -> dict[tuple[int, int], tuple[int, int]]:
    """基于 pdfplumber bbox 几何反推 {(row, col): (rowspan, colspan)}。

    原理：pdfplumber 把合并单元格的非锚位置返回为 ``None``；锚位置的 bbox
    本身就横跨多个网格行/列。对每个非 None cell，比较其右下角与下一行的 top、
    下一列的 left，越过即增加 span。
    """
    rows = pl_table.rows
    n_rows = len(rows)
    n_cols = max((len(r.cells) for r in rows), default=0)
    if n_rows == 0 or n_cols == 0:
        return {}

    grid: list[list[tuple[float, ...] | None]] = [[None] * n_cols for _ in range(n_rows)]
    for ri, row in enumerate(rows):
        for ci, cb in enumerate(row.cells):
            if cb is not None and ci < n_cols:
                grid[ri][ci] = tuple(cb)

    # 每行的 top y / 每列的 left x（取该行/列首个非 None cell 的坐标）
    row_tops: list[float | None] = [None] * n_rows
    for ri in range(n_rows):
        for cb in grid[ri]:
            if cb is not None:
                row_tops[ri] = cb[1]
                break
    col_lefts: list[float | None] = [None] * n_cols
    for ci in range(n_cols):
        for ri in range(n_rows):
            if grid[ri][ci] is not None:
                col_lefts[ci] = grid[ri][ci][0]
                break

    spans: dict[tuple[int, int], tuple[int, int]] = {}
    covered: set[tuple[int, int]] = set()
    EPS = 0.5

    for ri in range(n_rows):
        for ci in range(n_cols):
            if (ri, ci) in covered:
                continue
            bb = grid[ri][ci]
            if bb is None:
                continue
            x1, y1 = bb[2], bb[3]
            cs = 1
            for cj in range(ci + 1, n_cols):
                if col_lefts[cj] is not None and col_lefts[cj] < x1 - EPS:
                    cs += 1
                else:
                    break
            rs = 1
            for rj in range(ri + 1, n_rows):
                if row_tops[rj] is not None and row_tops[rj] < y1 - EPS:
                    rs += 1
                else:
                    break
            spans[(ri, ci)] = (rs, cs)
            for r in range(ri, ri + rs):
                for c in range(ci, ci + cs):
                    if (r, c) != (ri, ci):
                        covered.add((r, c))
    return spans


def _remap_spans(raw_spans: dict[tuple[int, int], tuple[int, int]],
                 kept: list[int]) -> dict[tuple[int, int], tuple[int, int]]:
    """把"原始行号坐标系"下的 spans 映射到"清洗后行号坐标系"。"""
    kept_set = set(kept)
    new_pos = {old: new for new, old in enumerate(kept)}
    out: dict[tuple[int, int], tuple[int, int]] = {}
    for (r, c), (rs, cs) in raw_spans.items():
        if r not in kept_set:
            continue
        new_rs = sum(1 for k in range(r, r + rs) if k in kept_set)
        if new_rs <= 0:
            new_rs = 1
        out[(new_pos[r], c)] = (new_rs, cs)
    return out


# ─────────────────────────── 左侧"标签列"挂载 ───────────────────────────


def _attach_label_column(
    page, pl_table, kept_indices: list[int],
) -> tuple[list[str], float] | None:
    """对每一保留行，扫描表 bbox 左侧同 y 范围内的文字，拼成"标签列"。

    process.md 的核心建议："不要完全依赖自动表格识别，而是先找到表格的列线，
    然后每页都按同一套 x 坐标切分文本"。lines 策略经常把无边框的"项目名"列漏掉，
    本函数把那列以 row-aligned 文字的形式补回来。

    Returns: (labels_per_cleaned_row, leftmost_x_used) 或 None（没找到任何对齐文字）
    """
    bbox = pl_table.bbox
    rows = pl_table.rows
    if not rows:
        return None

    page_words = page.extract_words(use_text_flow=False, keep_blank_chars=False)
    left_words = [w for w in page_words if w["x1"] <= bbox[0] - 1]
    if not left_words:
        return None

    labels: list[str] = []
    leftmost_x = bbox[0]
    found_any = False

    for original_idx in kept_indices:
        if original_idx >= len(rows):
            labels.append("")
            continue
        row = rows[original_idx]
        row_top = row_bot = None
        for cb in row.cells:
            if cb is not None:
                row_top, row_bot = cb[1], cb[3]
                break
        if row_top is None:
            labels.append("")
            continue
        # 行 y 范围 ± 1pt 容差
        matched = [
            w for w in left_words
            if row_top - 1 <= (w["top"] + w["bottom"]) / 2 <= row_bot + 1
        ]
        if not matched:
            labels.append("")
            continue
        # 多行 label：按 (top, x0) 排序后用空字符串连接（CJK 不需要空格）
        matched.sort(key=lambda w: (w["top"], w["x0"]))
        text = "".join(w["text"] for w in matched)
        text = re.sub(r"\s+", " ", text).strip()
        labels.append(text)
        leftmost_x = min(leftmost_x, min(w["x0"] for w in matched))
        found_any = True

    if not found_any:
        return None
    return labels, leftmost_x


# ─────────────────────────── 伪表过滤 / 同页 1 列合并 ───────────────────────────


# text 策略下：≤2 字符 cell 在所有非空 cell 中的占比 ≥ 此值即认定为碎片
FRAGMENT_RATIO_THRESHOLD = 0.5
# 数值列判据：某列非首行 cell 中纯数字占比 ≥ 此值即认定为数值列
NUMERIC_COL_THRESHOLD = 0.3
# 整表数值密度阈值；text_x_tolerance 大时合并 cell 会变成 "H股 142..." 这类 text+number 混合，
# 不再算 pure numeric，所以阈值放宽到 0.10
NUMERIC_DENSITY_THRESHOLD = 0.10


def _fragment_ratio(rows: list[list[str]]) -> float:
    """非空 cell 中 ≤2 字符的占比。CJK 段落被 text 策略按字宽切碎时会很高。"""
    flat = [c for row in rows for c in row if c]
    if not flat:
        return 1.0
    return sum(1 for c in flat if len(c) <= 2) / len(flat)


def _numeric_density(rows: list[list[str]]) -> float:
    """整表非空 cell 中纯数字 cell 的占比。"""
    flat = [c for row in rows for c in row if c]
    if not flat:
        return 0.0
    return sum(1 for c in flat if _looks_numeric(c)) / len(flat)


def _avg_row_fill(rows: list[list[str]]) -> float:
    """每行非空 cell 数 / n_cols 的平均。text 策略给出过多列时这个值会很低。"""
    if not rows:
        return 0.0
    n_cols = max((len(r) for r in rows), default=0)
    if n_cols == 0:
        return 0.0
    fills = [sum(1 for c in r if c) / n_cols for r in rows]
    return sum(fills) / len(fills)


def _has_numeric_column(rows: list[list[str]]) -> bool:
    """是否存在至少一列：去掉首行后，纯数字 cell 占非空 cell 比 ≥ NUMERIC_COL_THRESHOLD。"""
    if not rows or len(rows) < 2:
        return False
    n_cols = max(len(r) for r in rows)
    for c in range(n_cols):
        body = [r[c] for r in rows[1:] if c < len(r) and r[c]]
        if len(body) < 2:
            continue
        if sum(_looks_numeric(v) for v in body) / len(body) >= NUMERIC_COL_THRESHOLD:
            return True
    return False


def _looks_like_real_table(pt: "_PageTable") -> bool:
    """text 策略下做严格校验：碎片化 / 没有数值列 / 数值密度过低 / 填充率过低 → 视为伪表。

    lines 策略一律保留（假阳性极低，且我们会挂载标签列）。
    """
    if pt.engine != "pdfplumber_text":
        return True
    if _fragment_ratio(pt.rows) >= FRAGMENT_RATIO_THRESHOLD:
        return False
    if not _has_numeric_column(pt.rows):
        return False
    if _numeric_density(pt.rows) < NUMERIC_DENSITY_THRESHOLD:
        return False
    # 文本策略给出过多列且每行填充率 < 50% 通常是把页面强行切成网格；要求列数 ≤ 8
    # 或每行平均填充 ≥ 50%
    n_cols = max((len(r) for r in pt.rows), default=0)
    if n_cols > 8 and _avg_row_fill(pt.rows) < 0.5:
        return False
    return True


def _merge_single_col_neighbors(per_page: list["_PageTable"]) -> list["_PageTable"]:
    """同页内、行数相近、y 区间高度重叠的多张 N×1 lines 表 → 横向拼成多列表。

    场景：pdfplumber 的 lines 策略只识别了部分纵线时，会把一张宽表切成几个单列表。
    判据：同页 + 都 n_cols==1 + |行数差| ≤ 1 + y0/y1 几乎一致（容差 5pt）。
    """
    Y_EPS = 5.0
    out: list[_PageTable] = []
    by_page: dict[int, list[_PageTable]] = {}
    for pt in per_page:
        by_page.setdefault(pt.page, []).append(pt)

    for page in sorted(by_page):
        page_tables = by_page[page]
        # 候选：lines 单列表，按 x 排序
        singles = sorted(
            [pt for pt in page_tables
             if pt.engine == "pdfplumber" and max((len(r) for r in pt.rows), default=0) == 1],
            key=lambda x: x.bbox[0])
        others = [pt for pt in page_tables if pt not in singles]
        out.extend(others)

        used: set[int] = set()
        for i, base in enumerate(singles):
            if i in used:
                continue
            group = [base]
            for j in range(i + 1, len(singles)):
                if j in used:
                    continue
                cand = singles[j]
                if abs(cand.bbox[1] - base.bbox[1]) > Y_EPS:
                    continue
                if abs(cand.bbox[3] - base.bbox[3]) > Y_EPS:
                    continue
                if abs(len(cand.rows) - len(base.rows)) > 1:
                    continue
                group.append(cand)
                used.add(j)
            if len(group) == 1:
                out.append(base)
                continue
            # 横向拼接：以最多行数为准，缺位填空串
            n_rows_merged = max(len(g.rows) for g in group)
            merged_rows: list[list[str]] = []
            for r in range(n_rows_merged):
                row: list[str] = []
                for g in group:
                    row.append(g.rows[r][0] if r < len(g.rows) and g.rows[r] else "")
                merged_rows.append(row)
            merged_bbox = (
                min(g.bbox[0] for g in group), min(g.bbox[1] for g in group),
                max(g.bbox[2] for g in group), max(g.bbox[3] for g in group),
            )
            out.append(_PageTable(
                page=page,
                page_height=base.page_height,
                bbox=merged_bbox,
                rows=merged_rows,
                engine="pdfplumber",
                spans={},                                          # 拼接后无 span 信息
            ))
    # 维持调用方期望的 (页号, top y) 排序
    out.sort(key=lambda x: (x.page, x.bbox[1]))
    return out


# ─────────────────────────── 跨页合并 ───────────────────────────


def _row_similarity(a: list[str], b: list[str]) -> float:
    """两行相似度：在公共长度内，文本完全相等且非空的 cell 比例。"""
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    same = sum(1 for i in range(n) if a[i] and a[i] == b[i])
    return same / n


def looks_like_repeated_header(
    row: list[str],
    prev_header: list[str] | None,
    header_keywords: Iterable[str] = DEFAULT_HEADER_KEYWORDS,
) -> bool:
    """命中其一即视为重复表头：
       1) 与上一张表表头相似度 ≥ HEADER_SIM_THRESHOLD；
       2) 整行无数字 且 命中 ≥ 2 个表头关键词。
    """
    if prev_header and _row_similarity(row, prev_header) >= HEADER_SIM_THRESHOLD:
        return True
    text = " ".join(row)
    if re.search(r"\d", text):
        return False
    return sum(1 for k in header_keywords if k in text) >= 2


def merge_broken_row(prev_row: list[str], curr_row: list[str]) -> list[str] | None:
    """处理跨页断开的同一行；不可合并则返回 None。

    典型场景：上一行末列（备注）被切到下一页，下一页第一行前几列为空，
    仅靠后的列有文字 → 视为续写，按列拼回上一行。
    """
    if not prev_row or not curr_row or len(prev_row) != len(curr_row):
        return None
    non_empty_idx = [i for i, c in enumerate(curr_row) if c]
    if not non_empty_idx:
        return None
    # 第一处非空必须明显靠后：视觉上"前半都是空"才是续写，否则是新行
    if non_empty_idx[0] < max(1, len(curr_row) // 2):
        return None
    merged = list(prev_row)
    for i, c in enumerate(curr_row):
        if not c:
            continue
        merged[i] = f"{merged[i]} {c}".strip() if merged[i] else c
    return merged


@dataclass
class _PageTable:
    """单页清洗后表格的中间表示，供合并阶段使用。"""
    page: int
    page_height: float
    bbox: tuple[float, float, float, float]
    rows: list[list[str]]
    engine: str = "pdfplumber"               # "pdfplumber" | "pdfplumber_text"（无边框降级）
    # {(行号, 列号): (rowspan, colspan)}；非 1×1 才记录
    spans: dict[tuple[int, int], tuple[int, int]] = field(default_factory=dict)


def _is_continuation(prev: Table, last_page_height: float,
                     curr: _PageTable) -> bool:
    """判断 curr 是否是 prev 的跨页延续。

    必要：列数相同 + 页号连续。
    几何加分：prev 底端贴近上一页页底，curr 顶端贴近当前页页顶。
    """
    if not curr.rows or prev.n_cols != len(curr.rows[0]):
        return False
    last_page = prev.spans_pages[-1] if prev.spans_pages else prev.page
    if curr.page - last_page != 1:
        return False
    prev_bottom_gap = (last_page_height - prev.bbox[3]) / last_page_height
    curr_top_gap = curr.bbox[1] / curr.page_height
    return prev_bottom_gap <= PAGE_EDGE_RATIO_BOTTOM and curr_top_gap <= PAGE_EDGE_RATIO_TOP


def _build_cells(rows: list[list[str]],
                 spans: dict[tuple[int, int], tuple[int, int]],
                 row_offset: int = 0) -> list[TableCell]:
    """根据二维文本 + spans 表生成 TableCell 列表（只放锚 cell，被覆盖的位置不出）。"""
    if not rows:
        return []
    n_cols = max(len(r) for r in rows)
    covered: set[tuple[int, int]] = set()
    out: list[TableCell] = []
    for ri, row in enumerate(rows):
        for ci in range(n_cols):
            if (ri, ci) in covered:
                continue
            rs, cs = spans.get((ri, ci), (1, 1))
            text = row[ci] if ci < len(row) else ""
            out.append(TableCell(row=ri + row_offset, col=ci, text=text,
                                 rowspan=rs, colspan=cs))
            for r in range(ri, ri + rs):
                for c in range(ci, ci + cs):
                    if (r, c) != (ri, ci):
                        covered.add((r, c))
    return out


def _rows_to_table(pt: _PageTable) -> Table:
    n_rows = len(pt.rows)
    n_cols = max((len(r) for r in pt.rows), default=0)
    cells = _build_cells(pt.rows, pt.spans)
    return Table(
        page=pt.page,
        bbox=pt.bbox,
        cells=cells,
        n_rows=n_rows,
        n_cols=n_cols,
        engine=pt.engine,
        spans_pages=[pt.page],
        bboxes_by_page={pt.page: pt.bbox},
    )


def _append_rows(table: Table, new_rows: list[list[str]],
                 page: int, bbox: tuple[float, float, float, float],
                 new_spans: dict[tuple[int, int], tuple[int, int]] | None = None
                 ) -> None:
    """把新行追加到已有 Table 上，更新 n_rows / spans_pages / bboxes_by_page。

    new_spans 的坐标以 new_rows 为参照（即第一行是 row 0），会自动加上 offset。
    """
    start = table.n_rows
    cells = _build_cells(new_rows, new_spans or {}, row_offset=start)
    table.cells.extend(cells)
    table.n_rows = start + len(new_rows)
    table.n_cols = max(table.n_cols, max((len(r) for r in new_rows), default=0))
    if page not in table.spans_pages:
        table.spans_pages.append(page)
    if page in table.bboxes_by_page:
        old = table.bboxes_by_page[page]
        table.bboxes_by_page[page] = (
            min(old[0], bbox[0]), min(old[1], bbox[1]),
            max(old[2], bbox[2]), max(old[3], bbox[3]),
        )
    else:
        table.bboxes_by_page[page] = bbox


def _shift_spans(spans: dict[tuple[int, int], tuple[int, int]],
                 dropped_rows: int) -> dict[tuple[int, int], tuple[int, int]]:
    """从顶部丢掉 dropped_rows 行后重新编号；锚在被丢行内的 span 一并丢弃。"""
    if dropped_rows <= 0:
        return spans
    out: dict[tuple[int, int], tuple[int, int]] = {}
    for (r, c), (rs, cs) in spans.items():
        if r < dropped_rows:
            continue
        out[(r - dropped_rows, c)] = (rs, cs)
    return out


def merge_cross_page_tables(
    per_page: list[_PageTable],
    header_keywords: Iterable[str] = DEFAULT_HEADER_KEYWORDS,
) -> list[Table]:
    """把每页若干个 _PageTable 合并为跨页 Table 列表。

    per_page 已按 (页号, 表格在页内 top 坐标) 顺序排列。
    """
    merged: list[Table] = []
    last_page_height: dict[int, float] = {}      # 记录每页页高，几何判断时用

    for pt in per_page:
        last_page_height[pt.page] = pt.page_height
        if not pt.rows:
            continue
        if merged and _is_continuation(merged[-1], last_page_height[merged[-1].spans_pages[-1]], pt):
            prev = merged[-1]
            rows = pt.rows
            spans = dict(pt.spans)
            prev_header = prev.to_rows()[0] if prev.n_rows else None
            dropped = 0
            # 1) 去掉下一页重复出现的表头
            if rows and looks_like_repeated_header(rows[0], prev_header, header_keywords):
                rows = rows[1:]
                dropped += 1
            # 2) 修复跨页断开的同一行
            if rows and prev.n_rows:
                last_row = prev.to_rows()[-1]
                fixed = merge_broken_row(last_row, rows[0])
                if fixed is not None:
                    for c in prev.cells:
                        if c.row == prev.n_rows - 1 and c.col < len(fixed):
                            c.text = fixed[c.col]
                    rows = rows[1:]
                    dropped += 1
            if rows:
                _append_rows(prev, rows, pt.page, pt.bbox,
                             new_spans=_shift_spans(spans, dropped))
        else:
            merged.append(_rows_to_table(pt))
    return merged


def _detect_header_rows(grid: list[list[str]]) -> int:
    """推断多级表头行数。

    规则收紧：
      - cap = min(3, n_rows // 4)，至少 1，避免短表把数据行全吞进 header
      - 第 0 行默认是 header
      - 从第 1 行开始：含任何数字 → 停（数据行）；含 ≥ 1 个非数字 cell → 当 header 继续；
        全空 → 停
    """
    if not grid:
        return 0
    n = len(grid)
    cap = max(1, min(3, n // 4))
    count = 1
    for r in range(1, cap):
        non_empty = [c for c in grid[r] if c]
        if not non_empty:
            break
        if any(_looks_numeric(c) for c in non_empty):
            break
        count += 1
    return count


# ─────────────────────────── 质量评估 ───────────────────────────


_NUMERIC_RE = re.compile(r"^[\s\-\(\)（）]*[\d,，.]+\s*[%％]?\s*[\)）]?$")


def _looks_numeric(text: str) -> bool:
    return bool(text and _NUMERIC_RE.match(text.strip()))


def self_assess(table: Table) -> float:
    """对一张表的"可信度"打分（0~1），低于阈值则触发 VLM 兜底。

    启发式三个维度，等权加和：
      - empty_score   = 1 - 空单元格比例
      - shape_score   = 行列形状一致性（每行实际列数 / n_cols）
      - numeric_score = "可能为数值列"中真正能解析为数字的比例
    """
    if table.n_rows == 0 or table.n_cols == 0:
        return 0.0

    grid = table.to_rows()
    total = table.n_rows * table.n_cols
    empty = sum(1 for r in grid for c in r if not c)
    empty_score = 1 - empty / total

    # 形状一致性：行长度方差
    row_fill = [sum(1 for c in r if c) / table.n_cols for r in grid]
    shape_score = sum(row_fill) / len(row_fill)

    # 数值列纯度：先选出"非首行的数字占比 ≥ 50%"的列为候选数值列
    numeric_score = 1.0
    if table.n_rows >= 2:
        scores: list[float] = []
        for col in range(table.n_cols):
            body = [grid[r][col] for r in range(1, table.n_rows) if grid[r][col]]
            if len(body) < 2:
                continue
            ratio = sum(1 for v in body if _looks_numeric(v)) / len(body)
            if ratio >= 0.5:                       # 判定为数值列
                scores.append(ratio)
        if scores:
            numeric_score = sum(scores) / len(scores)

    score = (empty_score + shape_score + numeric_score) / 3
    return round(max(0.0, min(1.0, score)), 3)


# ─────────────────────────── 顶层入口 ───────────────────────────


# 无边框降级：把 lines 策略换成 text 策略，靠文字对齐推断列边界
_TEXT_STRATEGY_OVERRIDES = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "snap_tolerance": 5,
    "join_tolerance": 5,
    # 关键：text 策略默认 text_x_tolerance=3 会把 CJK 名称 / 长数字按字宽切碎。
    # 增大到 15 让"中央汇金投资有限责任公司"和"142,857,887,595"分别归到一个 cell。
    "text_x_tolerance": 15,
}

# text 策略默认裁掉顶部/底部一段（避免页内大标题与页脚被切碎成"伪表"）
# 与 process.md 建议的 page.crop((40, 80, width-40, height-60)) 一致
_TEXT_STRATEGY_CROP = (40, 80, 40, 60)            # (left, top, right, bottom) pt


def _try_extract(src, settings: dict, page, engine: str) -> list[_PageTable]:
    """用指定 settings 抽一遍并清洗。同时检测合并单元格的 rowspan/colspan。

    对 text 策略的结果会调用 _looks_like_real_table 过滤掉碎片化的伪表（段落被切碎）。
    对 lines 策略：尝试把左侧"项目名"列挂回去（process.md 的"列坐标重建"思路）。
    """
    out: list[_PageTable] = []
    for raw in src.find_tables(settings):
        cleaned, kept = _clean_table_rows_with_indices(raw.extract())
        if not cleaned:
            continue
        spans = _remap_spans(_detect_spans(raw), kept)
        spans = {k: v for k, v in spans.items() if v != (1, 1)}
        bbox = tuple(raw.bbox)

        # lines 策略下：尝试挂载左侧"行对齐"标签列
        if engine == "pdfplumber":
            attached = _attach_label_column(page, raw, kept)
            if attached is not None:
                label_col, leftmost_x = attached
                cleaned = [[label_col[i]] + row for i, row in enumerate(cleaned)]
                bbox = (leftmost_x, bbox[1], bbox[2], bbox[3])
                # 列号整体右移 1
                spans = {(r, c + 1): (rs, cs) for (r, c), (rs, cs) in spans.items()}

        pt = _PageTable(
            page=page.page_number,
            page_height=page.height,
            bbox=bbox,
            rows=cleaned,
            engine=engine,
            spans=spans,
        )
        if not _looks_like_real_table(pt):
            continue
        out.append(pt)
    return out


def extract_page_tables(
    page,                                                       # pdfplumber.page.Page
    table_settings: dict | None = None,
    crop_margins: tuple[float, float, float, float] | None = None,
    allow_borderless_fallback: bool = True,
) -> list[_PageTable]:
    """单页提取并清洗。

    Args:
        page: pdfplumber 的 Page 对象
        table_settings: 覆盖 DEFAULT_TABLE_SETTINGS
        crop_margins: (left, top, right, bottom) 像素裁剪，可避开页眉页脚
        allow_borderless_fallback: lines 策略 0 命中时是否再用 text 策略尝试无边框表格
    """
    settings = {**DEFAULT_TABLE_SETTINGS, **(table_settings or {})}
    src = page
    if crop_margins:
        l, t, r, b = crop_margins
        src = page.crop((l, t, page.width - r, page.height - b))

    # 主路径：lines 策略
    out = _try_extract(src, settings, page, engine="pdfplumber")

    # 降级：本页 lines 0 命中且页面有文字 → 试 text 策略（无边框表常见于费用明细等）
    # text 策略额外裁顶/裁底，避免把页内大标题、页脚切碎成"伪表"
    if not out and allow_borderless_fallback:
        cl, ct, cr, cb = _TEXT_STRATEGY_CROP
        text_src = page.crop((cl, ct, max(cl + 1, page.width - cr),
                              max(ct + 1, page.height - cb)))
        if (text_src.extract_text() or "").strip():
            fallback_settings = {**settings, **_TEXT_STRATEGY_OVERRIDES}
            out = _try_extract(text_src, fallback_settings, page, engine="pdfplumber_text")

    out.sort(key=lambda x: x.bbox[1])      # 同页内按 top 坐标排序
    return out


def extract_tables_from_pdf(
    pdf_path: str,
    pages: Iterable[int] | None = None,
    table_settings: dict | None = None,
    crop_margins: tuple[float, float, float, float] | None = None,
    header_keywords: Iterable[str] = DEFAULT_HEADER_KEYWORDS,
    score: bool = True,
) -> list[Table]:
    """主入口。返回跨页合并后的 Table 列表，每张表带 confidence 分。

    Args:
        pdf_path: PDF 路径
        pages: 1-based 页号列表；None 表示全部
        table_settings: 覆盖默认 pdfplumber 参数
        crop_margins: (left, top, right, bottom) 像素裁剪，避开页眉页脚最稳
        header_keywords: 表头关键词
        score: 是否对每张表执行 self_assess
    """
    if pdfplumber is None:
        raise ImportError("pdfplumber not installed; run: pip install pdfplumber")

    selected = set(pages) if pages is not None else None
    per_page: list[_PageTable] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if selected is not None and page.page_number not in selected:
                continue
            per_page.extend(extract_page_tables(page, table_settings, crop_margins))

    per_page = _merge_single_col_neighbors(per_page)
    tables = merge_cross_page_tables(per_page, header_keywords)
    for t in tables:
        t.header_rows = _detect_header_rows(t.to_rows(fill_merged=True))
    if score:
        for t in tables:
            t.confidence = self_assess(t)
    return tables


def needs_vlm_fallback(table: Table,
                       threshold: float = LOW_CONFIDENCE_THRESHOLD) -> bool:
    """供 parse.py 路由使用：confidence 低于阈值即建议交 VLM。"""
    return table.confidence < threshold
