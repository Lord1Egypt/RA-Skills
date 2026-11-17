#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-base · excel_style.py — 全库共享 Excel 视觉标准（单一事实来源 / single source of truth）

本模块集中承载 ct- 系列所有技能导出 `.xlsx` 时共用的**结构与样式逻辑**，
使 ct-registry / ct-safety / ct-pipeline / ct-literature 等技能产出的 Excel
在「同一视觉系统」下保持一致，同时允许每个技能保留**各自的品牌强调色**
（通过 ``PALETTES`` 参数化）。

──────────────────────────────────────────────────────────────────────────
设计标准（Design Standard，v1，2026-07-30 确立）
──────────────────────────────────────────────────────────────────────────
1. 渲染引擎：xlsxwriter（>=3.0，write-only）。理由：原生图标集、富文本封面、
   图表数据标签、页眉页脚、快速写入。
2. 字体：跨平台 CJK 字体自动探测——Windows=Microsoft YaHei，
   macOS=PingFang SC，Linux=SimSun（``detect_font()``）。全局用同一字体，
   避免 YaHei-only 布局在非 Windows 上静默回退导致排版崩坏。
3. 表头（header）：海军蓝/主题色底 + 白字 + 居中 + 1px 灰边框，行高 **24px**。
   所有数据表首行统一此高度与配色；**不使用**原生 Excel Table（其内建样式会
   重绘表头，破坏跨表一致性）。改用 ``autofilter`` + 逐格手动 zebra。
4. 斑马纹（zebra）：逐格（per-cell）方案——奇数行 LIGHT 主题浅底 + 1px 灰边框，
   偶数行白底 + 1px 灰边框。表格「数据区」统一此方案（不再用 conditional_format
   公式染色的第二套）。状态列按状态语义色块着色。
5. 封面（README/说明 表）：
   - 顶部 banner：主题色底、居中大标题、行高 30px；
   - 右上角品牌徽标：``positioning=2``（随单元格移动/缩放），scale≈0.16
     （416px 源 → ≈66.5px，约两行高）；x_offset≈20px 贴右对齐；
   - KPI 卡：3 列 × 2~3 行，标签行主题色底白字、数值行 LIGHT 底主题色大字；
   - 字段字典 + 状态色图例（self-explanatory）+ 注意事项 callout（WARN 底）。
6. 页面装饰（``page_decor``）：横向、水平居中、fit-to-width、隐藏网格线、
   页眉=标题、页脚=本地化页码/日期；标签页（tab）按表类型上色。
7. 图表：浮动于数据表右侧，像素高度按数据行数自适应（下限 20 行=400px），
   颜色与状态/来源色板一致；饼图百分比+类别标签、柱/条图值标签、图例精简。
8. 状态语义色板（STATUS_FILLS）：跨技能统一——绿=招募中、蓝=进行中、
   浅蓝=已完成、琥珀=尚未招募、红=终止/撤回、灰=未知。覆盖 EN+ZH 归一化值。
9. 一律通过 ``i18n.t()`` 本地化界面 chrome（xlsx.* 键）；原始数据值**不翻译**。

技能接入方式：
    from excel_style import (make_formats, banner, page_decor, kpi_card,
                             cover_logo, status_fill_hex, PALETTES, FONT,
                             add_chart, style_series, chart_h, chart_w,
                             dist_pie_points, autofit_widths, join as _join,
                             safe as _safe)
    fmts = make_formats(wb, PALETTES["registry"])   # 传递本技能调色板
"""

import os
import platform
from collections import Counter

import xlsxwriter


# ═══════════════════════════════════════════════════════════════════════════
# 1. 跨平台字体
# ═══════════════════════════════════════════════════════════════════════════
def detect_font():
    """Pick a CJK-capable face that actually exists on the host OS so the UI
    chrome renders consistently instead of silently falling back (which breaks
    YaHei-only layouts on macOS/Linux)."""
    s = platform.system()
    if s == "Windows":
        return "Microsoft YaHei"
    if s == "Darwin":
        return "PingFang SC"
    return "SimSun"


FONT = detect_font()


# ═══════════════════════════════════════════════════════════════════════════
# 2. 布局常量（所有技能共用）
# ═══════════════════════════════════════════════════════════════════════════
ROW_PX = 20             # xlsxwriter anchors ~20px per Excel row (empirical)
HEADER_H = 24           # header row height (px) — UNIFIED across all sheets
BANNER_H = 30           # cover/section banner row height (px)
MIN_CHART_ROWS = 20     # charts never shorter than 20 rows
MIN_CHART_H = MIN_CHART_ROWS * ROW_PX   # 400 px
BAND_GAP = 2            # blank rows between consecutive summary blocks
LOGO_SCALE = 0.16       # 416px source -> ~66.5px (≈ 2 rows tall)


# ═══════════════════════════════════════════════════════════════════════════
# 3. 状态语义色板（STATUS — 跨技能统一，覆盖 EN + ZH 归一化值）
# ═══════════════════════════════════════════════════════════════════════════
# 顺序重要："not yet" 须先于 "recruiting"（"not yet recruiting" 含 "recruiting"）。
# 这些 keyword 是「数据匹配键」，语言中立、绝不翻译。
STATUS_FILLS = [
    ("#FFD966", ("not yet", "尚未招募", "not yet recruiting")),     # amber  - not yet recruiting (FIRST)
    ("#70AD47", ("recruiting", "招募中", "enrolling")),             # green  - recruiting
    ("#5B9BD5", ("进行中", "ongoing", "in progress", "active")),    # blue   - in progress
    ("#9DC3E6", ("completed", "已完成", "finished")),               # light blue - completed
    ("#F4B0B0", ("withdrawn", "撤回", "terminated", "终止", "suspended",
                 "暂停", "halted")),                                # red    - stopped
    ("#E7E6E6", ("pending", "unknown", "未知", "n/a", "na", "—", "-")),  # grey - unknown/pending
]
STATUS_BAND = ["phase", "status", "source", "ind", "countries",
               "timeline", "sponsor", "enrollment", "phase_status"]
STATUS_LEGEND = ["notyet", "recruiting", "inprogress", "completed", "stopped", "unknown"]
STATUS_LEGEND_COLOR = {
    "notyet": "#FFD966", "recruiting": "#70AD47", "inprogress": "#5B9BD5",
    "completed": "#9DC3E6", "stopped": "#F4B0B0", "unknown": "#E7E6E6",
}


def status_fill_hex(status, fills=STATUS_FILLS):
    """Return a hex fill colour for a recruitment-status value (EN or ZH), or None."""
    s = str(status or "").lower()
    for color, keys in fills:
        if any(k in s for k in keys):
            return color
    return None


# ═══════════════════════════════════════════════════════════════════════════
# 4. 各技能品牌调色板（palette — 强调色各异，结构一致）
# ═══════════════════════════════════════════════════════════════════════════
# 键：navy=表头/主色, blue=强调/数据条/色阶顶, light=斑马纹/KPI 底,
#     banner=大标题底, grid=边框灰, greytx=注释字, cardhead=KPI 标签底,
#     cardbody=KPI 数值底, warn_bg/warn_bd=注意事项 callout, sumrow_bg=合计行底。
PALETTES = {
    "registry": {  # 海军蓝（试验注册）
        "navy": "#1F4E78", "blue": "#2E75B6", "light": "#EAF1FB",
        "banner": "#16335B", "grid": "#BFBFBF", "greytx": "#808080",
        "cardhead": "#1F4E78", "cardbody": "#EAF1FB", "warn_bg": "#FFF2CC",
        "warn_bd": "#BF9000", "sumrow_bg": "#DCE6F1",
    },
    "safety": {  # 医疗红（药物安全）
        "navy": "#7B241C", "blue": "#C0392B", "light": "#FDEDEC",
        "banner": "#7B241C", "grid": "#BFBFBF", "greytx": "#808080",
        "cardhead": "#C0392B", "cardbody": "#FDEDEC", "warn_bg": "#FFF2CC",
        "warn_bd": "#BF9000", "sumrow_bg": "#F5B7B1",
    },
    "pipeline": {  # 青蓝（竞争管线）
        "navy": "#0F6E7D", "blue": "#17A2B8", "light": "#E6F4F6",
        "banner": "#0B5562", "grid": "#BFBFBF", "greytx": "#808080",
        "cardhead": "#0F6E7D", "cardbody": "#E6F4F6", "warn_bg": "#FFF2CC",
        "warn_bd": "#BF9000", "sumrow_bg": "#CFE8EC",
    },
    "literature": {  # 学术绿（文献）
        "navy": "#2E7D4F", "blue": "#43A047", "light": "#E9F5EC",
        "banner": "#1B5E35", "grid": "#BFBFBF", "greytx": "#808080",
        "cardhead": "#2E7D4F", "cardbody": "#E9F5EC", "warn_bg": "#FFF2CC",
        "warn_bd": "#BF9000", "sumrow_bg": "#CFEBD6",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# 5. 格式工厂（参数化调色板 → xlsxwriter 格式字典）
# ═══════════════════════════════════════════════════════════════════════════
def make_formats(wb, palette):
    """Build the full format dictionary for a workbook using the given palette.

    Args:
        wb: xlsxwriter.Workbook
        palette: dict with keys navy/blue/light/banner/grid/greytx/cardhead/
                 cardbody/warn_bg/warn_bd/sumrow_bg (see ``PALETTES``).
    Returns: dict of named formats, including ``f["status"][hex]`` per status colour.
    """
    p = palette
    f = {}
    f["title"] = wb.add_format({"bold": True, "font_size": 16, "font_color": "white",
                                "bg_color": p["banner"], "align": "center",
                                "valign": "vcenter", "font_name": FONT})
    f["cover"] = wb.add_format({"bold": True, "font_size": 18, "font_color": "white",
                                "bg_color": p["banner"], "align": "center",
                                "valign": "vcenter", "font_name": FONT})
    f["sub"] = wb.add_format({"bold": True, "font_size": 11, "font_color": p["navy"],
                              "font_name": FONT, "align": "left", "valign": "vcenter"})
    f["body"] = wb.add_format({"font_size": 10, "font_name": FONT, "valign": "top",
                               "text_wrap": True})
    f["body_c"] = wb.add_format({"font_size": 10, "font_name": FONT, "align": "center",
                                 "valign": "vcenter", "text_wrap": True})
    f["note"] = wb.add_format({"italic": True, "font_size": 9, "font_color": p["greytx"],
                               "font_name": FONT, "valign": "vcenter"})
    f["header"] = wb.add_format({"bold": True, "font_color": "white", "bg_color": p["navy"],
                                 "align": "center", "valign": "vcenter", "border": 1,
                                 "border_color": p["grid"], "font_name": FONT,
                                 "text_wrap": True})
    f["zebra"] = wb.add_format({"bg_color": p["light"], "border": 1,
                                "border_color": p["grid"], "font_name": FONT,
                                "font_size": 10, "valign": "top", "text_wrap": True})
    f["plain"] = wb.add_format({"border": 1, "border_color": p["grid"],
                                "font_name": FONT, "font_size": 10, "valign": "top",
                                "text_wrap": True})
    f["fkey"] = wb.add_format({"border": 1, "border_color": p["grid"], "font_name": FONT,
                               "font_size": 10, "bold": True, "valign": "top",
                               "text_wrap": True})
    f["fkey_z"] = wb.add_format({"bg_color": p["light"], "border": 1,
                                 "border_color": p["grid"], "font_name": FONT,
                                 "font_size": 10, "bold": True, "valign": "top",
                                 "text_wrap": True})
    f["sumrow"] = wb.add_format({"bold": True, "font_color": p["navy"],
                                 "bg_color": p["sumrow_bg"], "border": 1,
                                 "border_color": p["grid"], "font_name": FONT,
                                 "font_size": 10, "align": "right", "valign": "vcenter"})
    f["left"] = wb.add_format({"align": "left", "valign": "top", "text_wrap": True,
                               "border": 1, "border_color": p["grid"], "font_name": FONT,
                               "font_size": 10})
    f["right"] = wb.add_format({"align": "right", "valign": "vcenter", "border": 1,
                                "border_color": p["grid"], "font_name": FONT,
                                "font_size": 10})
    f["center"] = wb.add_format({"align": "center", "valign": "vcenter", "border": 1,
                                 "border_color": p["grid"], "font_name": FONT,
                                 "font_size": 10})
    f["pct"] = wb.add_format({"align": "right", "valign": "vcenter", "border": 1,
                              "border_color": p["grid"], "font_name": FONT,
                              "font_size": 10, "num_format": "0.0%"})
    f["kpi_label"] = wb.add_format({"bold": True, "font_color": "white",
                                    "bg_color": p["cardhead"], "align": "center",
                                    "valign": "vcenter", "font_name": FONT,
                                    "font_size": 10, "text_wrap": True})
    f["kpi_value"] = wb.add_format({"bold": True, "font_color": p["navy"],
                                    "bg_color": p["cardbody"], "align": "center",
                                    "valign": "vcenter", "font_name": FONT,
                                    "font_size": 22})
    f["kpi_sub"] = wb.add_format({"italic": True, "font_color": p["greytx"],
                                  "bg_color": p["cardbody"], "align": "center",
                                  "valign": "vcenter", "font_name": FONT,
                                  "font_size": 9})
    f["warn"] = wb.add_format({"bg_color": p["warn_bg"], "border": 2,
                               "border_color": p["warn_bd"], "font_size": 10,
                               "font_color": "#7F6000", "text_wrap": True,
                               "valign": "vcenter", "font_name": FONT})
    f["link"] = wb.add_format({"font_size": 10, "font_color": "#0563C1",
                               "underline": True, "border": 1,
                               "border_color": p["grid"], "font_name": FONT,
                               "valign": "top", "text_wrap": True})
    f["divider"] = wb.add_format({"bg_color": p["light"]})
    f["block_title"] = wb.add_format({"bold": True, "font_color": "white",
                                      "bg_color": p["navy"], "align": "center",
                                      "valign": "vcenter", "border": 1,
                                      "border_color": p["grid"], "font_name": FONT,
                                      "font_size": 11})
    # status colour fills (one format per colour, shared across skills)
    f["status"] = {}
    for color, _ in STATUS_FILLS:
        f["status"][color] = wb.add_format({"bg_color": color, "align": "center",
                                            "valign": "vcenter", "border": 1,
                                            "border_color": p["grid"],
                                            "font_name": FONT, "font_size": 10})
    return f


# ═══════════════════════════════════════════════════════════════════════════
# 6. 布局助手（operate on a worksheet + formats）
# ═══════════════════════════════════════════════════════════════════════════
def banner(ws, r, c1, c2, text, fmts, height=BANNER_H):
    ws.merge_range(r, c1, r, c2, text, fmts["cover"])
    ws.set_row(r, height)


def page_decor(ws, title, fmts, footer_key="xlsx.footer"):
    """Landscape + centred + fit-to-width + no gridlines + header/footer."""
    import importlib
    ws.set_landscape()
    ws.center_horizontally()
    ws.fit_to_pages(1, 0)
    ws.hide_gridlines(2)
    ws.set_header(f"&C&B{title[:40]}")
    # footer uses i18n if available; fall back to a static string
    try:
        from i18n import t
        footer = t(footer_key)
    except Exception:
        footer = "Page &P of &N"
    ws.set_footer(footer)


def kpi_card(ws, top, left, label, value, sub, fmts):
    """A 3-col x 2-row KPI card: themed label head + light big-number body."""
    right = left + 2
    ws.merge_range(top, left, top, right, label, fmts["kpi_label"])
    ws.merge_range(top + 1, left, top + 1, right, value, fmts["kpi_value"])
    if sub:
        ws.merge_range(top + 2, left, top + 2, right, sub, fmts["kpi_sub"])


def cover_logo(ws, asset_path, col=14, scale=LOGO_SCALE, x_offset=20, y_offset=2,
               row=0, positioning=2):
    """Pin the brand mark to the TOP-RIGHT, sized to span ~2 rows.

    xlsxwriter ignores width/height for this anchor, so scale the 416px source
    (416 * 0.16 ≈ 66.5px ≈ 2 rows). ``positioning=2`` = move+size with cells.
    Silently skips if the asset file is missing.
    """
    if asset_path and os.path.exists(asset_path):
        ws.insert_image(row, col, asset_path,
                        {"x_offset": x_offset, "y_offset": y_offset,
                         "x_scale": scale, "y_scale": scale,
                         "positioning": positioning})


# ═══════════════════════════════════════════════════════════════════════════
# 7. 数据助手（library-agnostic）
# ═══════════════════════════════════════════════════════════════════════════
def join(v):
    """Flatten list-ish values to a readable string."""
    if v is None:
        return ""
    if isinstance(v, list):
        return "; ".join(str(x).strip() for x in v if str(x).strip())
    return str(v).strip()


def safe(v):
    return "" if v in (None, "", [], {}) else v


def cjk_width(s):
    """Approximate Excel column-width units (CJK glyph ≈ 2 Latin units)."""
    w = 0
    for ch in str(s):
        w += 2 if ord(ch) > 0x2E80 else 1
    return w


def autofit_widths(columns, header=None, min_w=10, max_w=60):
    """Content-aware column widths (CJK-aware)."""
    out = []
    for ci, col in enumerate(columns):
        mx = cjk_width(header[ci]) if header else 0
        for v in col:
            w = cjk_width(v)
            if w > mx:
                mx = w
        out.append(min(max_w, max(min_w, mx + 2)))
    return out


def year_of(d):
    """Extract a 4-digit year from a date-ish string, or None."""
    import re
    if not isinstance(d, str):
        return None
    m = re.search(r"(?:19|20)\d{2}", d)
    return m.group(0) if m else None


# ═══════════════════════════════════════════════════════════════════════════
# 8. 图表助手（xlsxwriter）
# ═══════════════════════════════════════════════════════════════════════════
def add_chart(wb, chart_type, title, w, h):
    kind = {"pie": "pie", "line": "line", "barh": "bar", "col": "column"}.get(
        chart_type, "column")
    ch = wb.add_chart({"type": kind})
    ch.set_title({"name": title, "name_font": {"bold": True, "size": 11,
                                                "font_name": FONT}})
    ch.set_size({"width": w, "height": h})
    ch.set_plotarea({"fill": {"color": "#FFFFFF"}})
    if chart_type in ("col", "barh", "pie"):
        ch.set_legend({"none": True})
    return ch


def style_series(ch, chart_type):
    lbl_font = {"size": 9, "font_name": FONT, "color": "#1F3864", "bold": False}
    opts = {"data_labels": {"value": True, "font": lbl_font}}
    if chart_type == "pie":
        opts = {"data_labels": {"percentage": True, "category": True,
                                "num_format": "0.0%", "font": lbl_font}, "gap": 55}
    if chart_type in ("col", "barh"):
        opts["gap"] = 55
    return opts


def chart_h(n_rows, per_row=20, base=60, cap=600):
    """Chart pixel height: floor at MIN_CHART_H, scale gently, cap to avoid runaway."""
    return int(max(MIN_CHART_H, min(n_rows * per_row + base, cap)))


def chart_w(h_px):
    """Chart pixel width: balanced landscape (≈1.2:1); pies handle their own square."""
    return min(760, int(h_px * 1.2))


def dist_pie_points(key, items, color_map=None):
    """Per-slice fill colours so pies read with the SAME palette as the rest of the
    workbook (coherence: a clinical user recognises a colour everywhere).

    Args:
        key: distribution key ("status" / "source" / ...).
        items: [(label, count), ...] in draw order.
        color_map: optional callable(label)->hex or dict label->hex for non-status keys.
    Returns list of {"fill": {"color": hex}} (one per slice); unmapped slices get a
    deterministic neutral grey (avoid duplicate default slices).
    """
    out = []
    seen = set()
    for label, _ in items:
        col = None
        if key == "status":
            col = status_fill_hex(label)
        if col is None and color_map is not None:
            col = color_map(label) if callable(color_map) else color_map.get(
                str(label).strip())
        if col is None:
            col = ["#BFBFBF", "#D9D9D9", "#A6A6A6", "#CCCCCC", "#8C8C8C",
                   "#E0E0E0", "#9DA6B0", "#C6CCD5"][len(seen) % 8]
        seen.add(col)
        out.append({"fill": {"color": col}})
    return out


__all__ = [
    "detect_font", "FONT", "ROW_PX", "HEADER_H", "BANNER_H", "MIN_CHART_ROWS",
    "MIN_CHART_H", "BAND_GAP", "LOGO_SCALE", "STATUS_FILLS", "STATUS_BAND",
    "STATUS_LEGEND", "STATUS_LEGEND_COLOR", "status_fill_hex", "PALETTES",
    "make_formats", "banner", "page_decor", "kpi_card", "cover_logo",
    "join", "safe", "cjk_width", "autofit_widths", "year_of",
    "add_chart", "style_series", "chart_h", "chart_w", "dist_pie_points",
]
