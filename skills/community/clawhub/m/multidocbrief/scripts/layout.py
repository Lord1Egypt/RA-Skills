"""
Оценка числа страниц .docx без Word и LibreOffice.

Документ записки строится из простой модели (абзацы и таблицы с известными шрифтами, кеглями,
отступами и ширинами). Здесь эта модель «вёрстается» заново: переносы строк считаются по реальным
ширинам глифов Arial (Pillow + TTF из системы), затем страницы заполняются с учётом правил Word:
неразрывные строки таблиц, «не отрывать от следующего» у заголовков, запрет висячих строк.

Метрики: Arial (Windows) → Liberation Sans (Linux, метрически совместим с Arial) → DejaVu Sans из
matplotlib (шире Arial — оценка получается с запасом) → средняя ширина символа.
Оценка консервативна: перенос слов по слогам не учитывается (в Word он только экономит место).
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

PT_PER_CM = 72 / 2.54
LINE_FACTOR = 1.15  # «одинарный» интервал Arial в Word: (ascent + descent + lineGap) / em

_FONT_CANDIDATES = {
    (False, False): ["C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
                     "/Library/Fonts/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
                     "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                     "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"],
    (True, False): ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf",
                    "/Library/Fonts/Arial Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"],
    (False, True): ["C:/Windows/Fonts/ariali.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial_Italic.ttf",
                    "/Library/Fonts/Arial Italic.ttf", "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
                    "/usr/share/fonts/truetype/liberation2/LiberationSans-Italic.ttf"],
    (True, True): ["C:/Windows/Fonts/arialbi.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold_Italic.ttf",
                   "/Library/Fonts/Arial Bold Italic.ttf",
                   "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
                   "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
                   "/usr/share/fonts/truetype/liberation2/LiberationSans-BoldItalic.ttf"],
}


# ============================================================================== модель документа
@dataclass
class Run:
    text: str
    size: float
    bold: bool = False
    italic: bool = False
    color: str | None = None
    spacing: float | None = None  # разрядка, pt


@dataclass
class Para:
    runs: list
    before: float = 0.0        # pt
    after: float = 0.0         # pt
    line: float = 1.0          # множитель межстрочного интервала
    align: str | None = None   # "both" | None
    ind_left: float = 0.0      # cm
    first_line: float = 0.0    # cm; отрицательный — выступ
    keep_next: bool = False
    style: str | None = None
    border_top: tuple | None = None     # (толщина в 1/8 pt, цвет, отступ pt)
    border_bottom: tuple | None = None
    tab_right: float | None = None      # cm — правая табуляция (колонтитул)


@dataclass
class Cell:
    paras: list
    fill: str | None = None
    borders: dict = field(default_factory=dict)  # side -> (толщина 1/8 pt, цвет)


@dataclass
class Table:
    rows: list                 # list[list[Cell]]
    widths: list               # cm
    margins: tuple = (50, 50, 90, 90)  # dxa: top, bottom, left, right
    cant_split: bool = True


@dataclass
class DocModel:
    blocks: list
    margins: tuple             # cm: top, bottom, left, right
    footer: Para | None = None
    page: tuple = (21.0, 29.7)
    header_dist: float = 0.8
    footer_dist: float = 0.7
    meta: dict = field(default_factory=dict)
    profile: dict = field(default_factory=dict)

    @property
    def text_width(self) -> float:
        return self.page[0] - self.margins[2] - self.margins[3]


# ============================================================================== метрики шрифта
class Metrics:
    def __init__(self):
        from PIL import ImageFont
        self.fonts = {}
        self.source = ""
        for key, cands in _FONT_CANDIDATES.items():
            for c in cands:
                if Path(c).exists():
                    self.fonts[key] = ImageFont.truetype(c, 100)
                    if key == (False, False):
                        self.source = "Arial" if "arial" in c.lower() else "Liberation Sans (метрики Arial)"
                    break
        if (False, False) not in self.fonts:
            try:
                import matplotlib
                base = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
                for key, name in {(False, False): "DejaVuSans.ttf", (True, False): "DejaVuSans-Bold.ttf",
                                  (False, True): "DejaVuSans-Oblique.ttf",
                                  (True, True): "DejaVuSans-BoldOblique.ttf"}.items():
                    if (base / name).exists():
                        self.fonts[key] = ImageFont.truetype(str(base / name), 100)
                self.source = "DejaVu Sans (шире Arial — оценка с запасом)"
            except Exception:  # noqa: BLE001
                pass
        if not self.fonts:
            self.source = "средняя ширина символа"

    @lru_cache(maxsize=200_000)
    def width(self, text: str, bold: bool, italic: bool) -> float:
        """Ширина в долях кегля (em)."""
        f = self.fonts.get((bold, italic)) or self.fonts.get((bold, False)) or self.fonts.get((False, False))
        if f is None:
            return len(text) * (0.62 if bold else 0.58)
        return f.getlength(text) / 100.0


_METRICS: Metrics | None = None


def metrics() -> Metrics:
    global _METRICS
    if _METRICS is None:
        _METRICS = Metrics()
    return _METRICS


# ============================================================================== вёрстка
# переносимые пробелы (обычный, en/em/thin space); неразрывные (U+00A0, U+202F) — часть слова
_SPACES = "    "
_TOKEN = re.compile(r"\n|\t|[" + _SPACES + r"]+|[^" + _SPACES + r"\n\t]+")
TAB_STOP = 708 / 20.0  # pt — шаг табуляции по умолчанию (settings.xml: defaultTabStop=708)


def para_lines(p: Para, width_cm: float) -> tuple[int, float]:
    """(число строк, высота строки в pt) для абзаца в колонке шириной width_cm.
    Учитывает явные переносы (<w:br/>), табуляцию и слова длиннее строки.
    """
    m = metrics()
    width = width_cm * PT_PER_CM
    first_avail = width - (p.ind_left + p.first_line) * PT_PER_CM
    other_avail = width - p.ind_left * PT_PER_CM
    max_size = max((r.size for r in p.runs), default=10.0)
    lines, cur, avail, pending = 1, 0.0, first_avail, 0.0

    def newline():
        nonlocal lines, cur, avail, pending
        lines += 1
        cur, avail, pending = 0.0, other_avail, 0.0

    for r in p.runs:
        for tok in _TOKEN.findall(r.text):
            if tok == "\n":
                newline()
                continue
            if tok == "\t":
                cur = (int((cur + pending) // TAB_STOP) + 1) * TAB_STOP
                pending = 0.0
                if cur > avail:
                    newline()
                continue
            if tok[0] in _SPACES:
                pending += m.width(" ", r.bold, r.italic) * r.size * len(tok)
                continue
            w = m.width(tok, r.bold, r.italic) * r.size + (r.spacing or 0) * len(tok)
            if cur > 0 and cur + pending + w > avail:
                newline()
            while cur == 0 and w > avail > 0:  # слово длиннее строки — в том числе первое в абзаце
                newline()
                w -= avail
            cur += pending + w
            pending = 0.0
    return lines, max_size * LINE_FACTOR * p.line


def para_height(p: Para, width_cm: float) -> float:
    n, lh = para_lines(p, width_cm)
    return p.before + n * lh + p.after


def row_height(t: Table, row: list) -> float:
    top, bottom, left, right = (v / 20.0 for v in t.margins)
    best = 0.0
    for cell, w in zip(row, t.widths):
        inner = w - (left + right) / PT_PER_CM
        h = top + sum(para_height(p, inner) for p in cell.paras) + bottom
        best = max(best, h)
    border = max((b[0] for c in row for b in c.borders.values()), default=0) / 8.0
    return best + border


def estimate(model: DocModel) -> dict:
    """Пагинация модели. → {"pages", "last_fill", "used_height", "page_height", "fonts"}"""
    H = (model.page[1] - model.margins[0] - model.margins[1]) * PT_PER_CM
    W = model.text_width
    y, pages = 0.0, 1
    blocks = model.blocks

    def new_page():
        nonlocal y, pages
        pages += 1
        y = 0.0

    def para_total(blk) -> float:
        n, lh = para_lines(blk, W)
        bdr = sum(b[0] / 8.0 + b[2] for b in (blk.border_top, blk.border_bottom) if b)
        return blk.before + n * lh + blk.after + bdr

    def first_chunk(k: int) -> float:
        """Сколько места нужно, чтобы блок k начался на этой странице (с цепочкой «не отрывать от следующего»)."""
        if k >= len(blocks):
            return 0.0
        blk = blocks[k]
        if isinstance(blk, Table):
            return row_height(blk, blk.rows[0]) if blk.rows else 0.0
        if blk.keep_next:
            return para_total(blk) + first_chunk(k + 1)
        n, lh = para_lines(blk, W)
        return blk.before + min(n, 2) * lh

    for i, blk in enumerate(blocks):
        if isinstance(blk, Table):
            for row in blk.rows:
                h = row_height(blk, row)
                if y + h > H and y > 0:
                    new_page()
                while h > H:  # строка выше страницы (в Word «уедет» вниз) — считаем целые страницы
                    h -= H
                    new_page()
                y += h
            continue
        n, lh = para_lines(blk, W)
        bdr = sum(b[0] / 8.0 + b[2] for b in (blk.border_top, blk.border_bottom) if b)
        before = blk.before + bdr
        if blk.keep_next and y > 0 and y + para_total(blk) + first_chunk(i + 1) > H:
            new_page()
        left, first = n, True
        while True:
            sp = before if first else 0.0
            cap = max(0, int((H - y - sp) // lh)) if lh > 0 else left
            if left <= cap:
                y = min(H, y + sp + left * lh + blk.after)  # отступ после абзаца в конце страницы «съедается»
                break
            place = cap
            if left - place < 2:  # не оставлять одну строку на следующей странице
                place = left - 2
            if first and place < 2 and y > 0:  # не оставлять одну строку внизу — абзац целиком переносится
                new_page()
                continue
            place = max(place, 1 if y == 0 else 0)
            left -= place
            new_page()
            first = False
    return {"pages": pages, "last_fill": round(y / H, 3), "used_height": round(H * (pages - 1) + y, 1),
            "page_height": round(H, 1), "fonts": metrics().source}


def fits(model: DocModel, max_pages: int, reserve: float = 0.04) -> tuple[bool, dict]:
    """Помещается ли в max_pages с запасом reserve на последней странице (разница Word/оценки)."""
    est = estimate(model)
    ok = est["pages"] < max_pages or (est["pages"] == max_pages and est["last_fill"] <= 1 - reserve)
    return ok, est
