"""LAS 输出 HTML `<table>` → ParsedTable dataclass.

LAS 的 markdown 里表格是 HTML 形态：
    <table>
      <thead><tr><th rowspan="3"></th><th colspan="2">本集团</th>...</tr> ...</thead>
      <tbody><tr><td>货币资金</td><td>1,234</td>...</tr> ...</tbody>
    </table>

本模块只做"结构化"：BS4 解析 → 处理 rowspan/colspan 展开成 (row, col) 网格 →
返回 ParsedTable。**不**做数值规整（那是 numeric_normalizer 的事），
**不**判断"哪几行是表头"（那是 multi_header_detector 的事）。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from bs4 import BeautifulSoup, Tag


@dataclass
class ParsedCell:
    row: int
    col: int
    rowspan: int = 1
    colspan: int = 1
    text: str = ""
    is_header: bool = False          # 来自 <th>（先验头），multi_header 还会修正
    is_anchor: bool = True           # 合并单元格的锚点；非锚位置自动生成时 False
    raw_html: str = ""


@dataclass
class ParsedTable:
    cells: List[ParsedCell] = field(default_factory=list)
    n_rows: int = 0
    n_cols: int = 0
    # 表格紧邻上方的若干行文字（用于 caption / unit 提取）
    preface_lines: List[str] = field(default_factory=list)
    # 表格紧邻下方的若干行文字（脚注 / 注释）
    epilogue_lines: List[str] = field(default_factory=list)
    raw_html: str = ""

    def caption(self) -> Optional[str]:
        """从 preface 提取表标题。

        启发式（优先级递减）：
          1. 含"表"字或常见报表关键词的行（最靠近 <table> 的优先）
          2. 非纯数字/日期的可读行
          3. 兜底：最近的非空非括号行
        """
        # 1) 含报表关键词
        keywords = ("表", "现金流", "权益变动", "综合收益", "利润")
        for line in reversed(self.preface_lines):
            s = line.strip()
            if s and any(k in s for k in keywords):
                return s
        # 2) 非纯数字/日期
        for line in reversed(self.preface_lines):
            s = line.strip()
            if not s or s.startswith("(") or s.startswith("（"):
                continue
            # 跳过形如 "2026年3月31日" / "2026-03-31" 的纯日期行
            if re.fullmatch(r"\d{4}年\s*\d{1,2}月\s*\d{1,2}日", s):
                continue
            if re.fullmatch(r"[\d\-/\s]+", s):
                continue
            return s
        # 3) 兜底
        for line in reversed(self.preface_lines):
            s = line.strip()
            if s and not s.startswith("(") and not s.startswith("（"):
                return s
        return None

    def context_text(self) -> str:
        """整段上下文文本，用于单位声明/单位币种识别。"""
        return "\n".join(self.preface_lines)


# ---------------------------------------------------------------------------
# Markdown 切块：用 <table>...</table> 拆出 [preface, table, epilogue]
# ---------------------------------------------------------------------------

_TABLE_BLOCK_RE = re.compile(r"<table\b.*?</table>", re.IGNORECASE | re.DOTALL)


def split_page_markdown(page_md: str) -> List[dict]:
    """把单页 markdown 切成 [{type, content}] 顺序段。

    type ∈ {"text", "table"}。table 段的 content 是 <table>...</table> HTML。
    """
    parts: List[dict] = []
    pos = 0
    for m in _TABLE_BLOCK_RE.finditer(page_md):
        if m.start() > pos:
            text_chunk = page_md[pos: m.start()]
            if text_chunk.strip():
                parts.append({"type": "text", "content": text_chunk})
        parts.append({"type": "table", "content": m.group(0)})
        pos = m.end()
    tail = page_md[pos:]
    if tail.strip():
        parts.append({"type": "text", "content": tail})
    return parts


# ---------------------------------------------------------------------------
# HTML <table> → ParsedTable
# ---------------------------------------------------------------------------

def _cell_text(tag: Tag) -> str:
    """提取 <td>/<th> 的可读文本：<br> → 换行，其他保留 inline 文本。"""
    # 用 separator=" " 避免 "本集团" 和数值粘在一起
    text = tag.get_text(separator="\n", strip=True)
    # 折叠连续的换行/空白
    text = re.sub(r"\s*\n\s*", "\n", text).strip()
    return text


def _row_tags(table: Tag) -> List[Tag]:
    """汇总表格内所有 <tr>，保持文档顺序。thead/tbody/tfoot 都展开。"""
    rows: List[Tag] = []
    for el in table.descendants:
        if isinstance(el, Tag) and el.name == "tr":
            rows.append(el)
    # 用 find_all 更直观但需要去重（descendants 已有序）
    seen = set()
    unique = []
    for r in rows:
        rid = id(r)
        if rid in seen:
            continue
        seen.add(rid)
        unique.append(r)
    return unique


def parse_table(html_fragment: str) -> Optional[ParsedTable]:
    """解析 <table>...</table> → ParsedTable（cells 已按 rowspan/colspan 展开到网格）。

    展开规则：
      - 合并单元格的"锚位置"（左上角）记录原 text + rowspan/colspan + is_anchor=True
      - 被覆盖位置自动填一个 is_anchor=False 的空 cell（text="", 继承 is_header 标记）
    """
    soup = BeautifulSoup(html_fragment, "lxml")
    table = soup.find("table")
    if table is None:
        return None

    tr_list = _row_tags(table)
    if not tr_list:
        return ParsedTable(raw_html=html_fragment)

    # occupied[(row, col)] = True 表示已被某 rowspan/colspan 覆盖
    occupied: dict[tuple[int, int], bool] = {}
    cells: List[ParsedCell] = []
    max_col = 0

    for r_idx, tr in enumerate(tr_list):
        col_cursor = 0
        for td in tr.find_all(["td", "th"], recursive=False):
            # 跳过已被覆盖的列
            while occupied.get((r_idx, col_cursor)):
                col_cursor += 1

            is_header = (td.name == "th")
            try:
                rowspan = int(td.get("rowspan", 1))
            except (TypeError, ValueError):
                rowspan = 1
            try:
                colspan = int(td.get("colspan", 1))
            except (TypeError, ValueError):
                colspan = 1
            rowspan = max(1, rowspan)
            colspan = max(1, colspan)

            text = _cell_text(td)
            anchor = ParsedCell(
                row=r_idx, col=col_cursor,
                rowspan=rowspan, colspan=colspan,
                text=text, is_header=is_header,
                is_anchor=True,
                raw_html=str(td),
            )
            cells.append(anchor)

            # 标记被覆盖的位置并补 placeholder
            for dr in range(rowspan):
                for dc in range(colspan):
                    if dr == 0 and dc == 0:
                        occupied[(r_idx, col_cursor)] = True
                        continue
                    rr = r_idx + dr
                    cc = col_cursor + dc
                    occupied[(rr, cc)] = True
                    cells.append(ParsedCell(
                        row=rr, col=cc,
                        rowspan=1, colspan=1,
                        text="", is_header=is_header,
                        is_anchor=False,
                    ))

            col_cursor += colspan
            if col_cursor > max_col:
                max_col = col_cursor

    n_rows = max((c.row for c in cells), default=-1) + 1
    n_cols = max_col

    return ParsedTable(
        cells=cells, n_rows=n_rows, n_cols=n_cols,
        raw_html=html_fragment,
    )


# ---------------------------------------------------------------------------
# 顶层入口：单页 markdown → List[ParsedTable]
# ---------------------------------------------------------------------------

_PREFACE_LINES = 8   # 取表格上方多少行作 preface
_EPILOGUE_LINES = 4


def parse_page_tables(page_md: str) -> List[ParsedTable]:
    """单页 markdown → 多个 ParsedTable（含 preface/epilogue 文本）。

    每个 table 会绑定它**紧邻**上方/下方的文字段，便于 caption / unit 识别。
    """
    parts = split_page_markdown(page_md)
    tables: List[ParsedTable] = []
    n = len(parts)
    for i, part in enumerate(parts):
        if part["type"] != "table":
            continue
        t = parse_table(part["content"])
        if t is None:
            continue
        # preface = 上一个 text part
        if i > 0 and parts[i - 1]["type"] == "text":
            lines = [ln for ln in parts[i - 1]["content"].splitlines() if ln.strip()]
            t.preface_lines = lines[-_PREFACE_LINES:]
        # epilogue
        if i + 1 < n and parts[i + 1]["type"] == "text":
            lines = [ln for ln in parts[i + 1]["content"].splitlines() if ln.strip()]
            t.epilogue_lines = lines[:_EPILOGUE_LINES]
        tables.append(t)
    return tables
