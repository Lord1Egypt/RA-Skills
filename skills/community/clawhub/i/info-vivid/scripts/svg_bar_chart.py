#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
svg_bar_chart.py  —  通用深色主题 SVG 横向条形图生成器
info-visualize skill 核心脚本

用法（命令行）:
    python svg_bar_chart.py --input data.json --output chart.html \
        --title "A股涨幅 TOP 20" --subtitle "2026-03-14" \
        --value-field pct_chg --label-field name \
        --value-suffix "%" --footer "数据来源: Tushare Pro"

用法（Python 导入）:
    from svg_bar_chart import build_svg_chart
    svg, html = build_svg_chart(items, config)

data.json 格式:
    {
      "title": "标题",
      "subtitle": "副标题",
      "items": [
        {"label": "标签", "value": 数字, "extra": "附加信息", "tag": "分类"},
        ...
      ],
      "kpis": [
        {"label": "KPI名称", "value": "显示值"},
        ...
      ],
      "footer": "页脚说明"
    }
"""

import json
import math
import argparse
import os
from pathlib import Path

# ─── 默认配色（深海军蓝主题）────────────────────────────────────────────
DEFAULT_THEME = {
    "bg":           "#0E1624",
    "bg_alt":       "#0A1520",
    "bg_row1":      "#131D2E",
    "bg_row2":      "#0F1A2A",
    "header_bg":    "#0A1520",
    "accent":       "#2EC4B6",
    "accent2":      "#FFC83C",
    "text_primary": "#C0CDE0",
    "text_muted":   "#5A7090",
    "text_label":   "#7A90B0",
    "divider":      "rgba(46,196,182,0.2)",
    "kpi_stroke":   "rgba(46,196,182,0.4)",
    "kpi_fill":     "rgba(46,196,182,0.08)",
    "bar_colors":   ["#FF2244", "#FF5533", "#FF8800", "#FFAA00", "#DDCC00",
                     "#2EC4B6", "#3AB0FF", "#A060FF", "#FF60C0", "#60DD80"],
    "bar_threshold_colors": None,   # 若设置，按 value 区间取色
}


def value_to_color(value, bar_colors, threshold_colors=None):
    """根据值选择条形颜色。threshold_colors: [(threshold, color), ...]"""
    if threshold_colors:
        for thresh, color in sorted(threshold_colors, reverse=True):
            if value >= thresh:
                return color
        return bar_colors[-1]
    # 默认取模循环
    idx = 0
    return bar_colors[idx % len(bar_colors)]


def build_svg_chart(items: list, config: dict) -> tuple[str, str]:
    """
    生成 SVG 图表字符串和完整 HTML 字符串。

    Parameters
    ----------
    items : list of dict
        每项必须包含 'label'(str) 和 'value'(float)。
        可选字段: 'extra'(str), 'tag'(str), 'color'(str)
    config : dict
        {
          title, subtitle, footer,
          kpis: [{"label":..., "value":...}],
          value_suffix: "%",
          theme: {...},           # 覆盖 DEFAULT_THEME
          bar_threshold_colors: [(thresh, color), ...],
          max_value_override: float,
          show_reference_line: float,   # 在该值处画参考线
          reference_label: str,
          width: int,             # 默认 900
          row_height: int,        # 默认 32
        }

    Returns
    -------
    (svg_str, html_str)
    """
    theme = {**DEFAULT_THEME, **(config.get("theme") or {})}
    W = config.get("width", 900)
    ROW_H = config.get("row_height", 32)
    HEADER_H = 160 if config.get("kpis") else 90
    FOOTER_H = 60
    BAR_LEFT = 190
    BAR_RIGHT = int(W * 0.755)
    LABEL_X = BAR_RIGHT + 8
    PAD = 8

    title    = config.get("title", "图表")
    subtitle = config.get("subtitle", "")
    footer   = config.get("footer", "Powered by WorkBuddy")
    suffix   = config.get("value_suffix", "")
    kpis     = config.get("kpis") or []
    ref_val  = config.get("show_reference_line")
    ref_lbl  = config.get("reference_label", "参考线")

    values = [item["value"] for item in items]
    max_v = config.get("max_value_override") or (max(values) * 1.05 if values else 100)

    TOTAL_H = HEADER_H + ROW_H * len(items) + 24 + FOOTER_H + 10

    # ── KPI 卡片 ──
    kpi_svg = ""
    if kpis:
        kpi_count = min(len(kpis), 4)
        card_w = int((W - 60) / kpi_count) - 10
        for ki, kpi in enumerate(kpis[:4]):
            cx = 30 + ki * (card_w + 10)
            kpi_svg += f"""
  <rect x="{cx}" y="82" width="{card_w}" height="58" rx="8"
        fill="{theme['kpi_fill']}" stroke="{theme['accent']}" stroke-width="0.8" stroke-opacity="0.4"/>
  <text x="{cx + card_w//2}" y="108" font-size="22" font-weight="bold" fill="{theme['accent2']}"
        font-family="Microsoft YaHei,sans-serif" text-anchor="middle">{kpi['value']}</text>
  <text x="{cx + card_w//2}" y="128" font-size="11" fill="{theme['text_label']}"
        font-family="Microsoft YaHei,sans-serif" text-anchor="middle">{kpi['label']}</text>"""

    # ── 数据行 ──
    rows_svg = []
    tc = theme.get("bar_threshold_colors") or config.get("bar_threshold_colors")
    bar_colors = theme["bar_colors"]

    for i, item in enumerate(items):
        y = HEADER_H + i * ROW_H
        val = item["value"]
        label = item.get("label", "")
        extra = item.get("extra", "")
        tag = item.get("tag", "")
        color = item.get("color") or value_to_color(val, bar_colors, tc)

        bar_w = max(2, (val / max_v) * (BAR_RIGHT - BAR_LEFT))
        bg = theme["bg_row1"] if i % 2 == 0 else theme["bg_row2"]
        display_val = f"{val:+.2f}{suffix}" if val >= 0 else f"{val:.2f}{suffix}"

        tooltip = label
        if extra: tooltip += f" | {extra}"
        if tag:   tooltip += f" | {tag}"
        tooltip += f" | {display_val}"

        rows_svg.append(f"""
  <rect x="0" y="{y}" width="{W}" height="{ROW_H}" fill="{bg}"/>
  <text x="{PAD}" y="{y+20}" font-size="12" fill="{theme['text_primary']}"
        font-family="Microsoft YaHei,sans-serif">{i+1:02d}. {label}</text>
  <rect x="{BAR_LEFT}" y="{y+6}" width="{bar_w:.1f}" height="18" rx="3"
        fill="{color}" opacity="0.9">
    <title>{tooltip}</title>
  </rect>
  <text x="{LABEL_X}" y="{y+20}" font-size="12" fill="{color}" font-weight="bold"
        font-family="Microsoft YaHei,sans-serif">{display_val}</text>
  <text x="{W-PAD}" y="{y+20}" font-size="10" fill="{theme['text_muted']}"
        font-family="Microsoft YaHei,sans-serif" text-anchor="end">{tag}</text>""")

    # ── 参考线 ──
    ref_svg = ""
    if ref_val is not None:
        ref_x = BAR_LEFT + (ref_val / max_v) * (BAR_RIGHT - BAR_LEFT)
        ref_svg = f"""
  <line x1="{ref_x:.1f}" y1="{HEADER_H}" x2="{ref_x:.1f}" y2="{HEADER_H + ROW_H*len(items)}"
        stroke="{theme['accent2']}" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <text x="{ref_x+4:.1f}" y="{HEADER_H+14}" font-size="10" fill="{theme['accent2']}"
        font-family="Microsoft YaHei,sans-serif" opacity="0.8">{ref_lbl}</text>"""

    # ── X 轴刻度 ──
    tick_values = [0, max_v * 0.25, max_v * 0.5, max_v * 0.75, max_v]
    xaxis_svg = "".join(
        f'<text x="{BAR_LEFT + (v/max_v)*(BAR_RIGHT-BAR_LEFT):.1f}" '
        f'y="{HEADER_H+ROW_H*len(items)+16}" '
        f'font-size="10" fill="{theme["text_muted"]}" '
        f'font-family="Microsoft YaHei,sans-serif" text-anchor="middle">'
        f'{v:.1f}{suffix}</text>'
        for v in tick_values
    )

    # ── 完整 SVG ──
    subtitle_y = 65 if subtitle else 0
    subtitle_svg = (
        f'<text x="{W//2}" y="65" font-size="13" fill="{theme["text_label"]}" '
        f'font-family="Microsoft YaHei,sans-serif" text-anchor="middle">{subtitle}</text>'
        if subtitle else ""
    )

    chart_bottom = HEADER_H + ROW_H * len(items)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{TOTAL_H}" viewBox="0 0 {W} {TOTAL_H}">
  <defs>
    <linearGradient id="hdrGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0A1520"/>
      <stop offset="100%" stop-color="#0E1624"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="{W}" height="{TOTAL_H}" fill="{theme['bg']}"/>

  <!-- Header -->
  <rect width="{W}" height="{HEADER_H}" fill="url(#hdrGrad)"/>
  <rect width="{W}" height="3" fill="{theme['accent']}"/>
  <text x="{W//2}" y="42" font-size="22" font-weight="bold" fill="{theme['accent']}"
        font-family="Microsoft YaHei,sans-serif" text-anchor="middle" letter-spacing="3">{title}</text>
  {subtitle_svg}

  <!-- KPI 卡片 -->
  {kpi_svg}

  <!-- 图表背景 -->
  <rect y="{HEADER_H}" width="{W}" height="{ROW_H*len(items)}" fill="{theme['bg']}"/>

  <!-- 数据行 -->
  {"".join(rows_svg)}

  <!-- 参考线 -->
  {ref_svg}

  <!-- X 轴刻度 -->
  <rect y="{chart_bottom}" width="{W}" height="24" fill="{theme['bg_alt']}"/>
  {xaxis_svg}

  <!-- 分割线 -->
  <line x1="0" y1="{chart_bottom+24}" x2="{W}" y2="{chart_bottom+24}"
        stroke="{theme['divider']}" stroke-width="1"/>

  <!-- Footer -->
  <rect y="{chart_bottom+24}" width="{W}" height="{FOOTER_H}" fill="{theme['bg_alt']}"/>
  <text x="{W//2}" y="{chart_bottom+24+28}" font-size="11" fill="{theme['text_muted']}"
        font-family="Microsoft YaHei,sans-serif" text-anchor="middle">{footer}</text>
  <text x="{W//2}" y="{chart_bottom+24+46}" font-size="10" fill="#2A3A50"
        font-family="Microsoft YaHei,sans-serif" text-anchor="middle">Powered by WorkBuddy</text>
</svg>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ margin: 0; background: #060E18; display: flex; justify-content: center; padding: 20px; }}
  svg {{ max-width: 100%; height: auto; display: block; }}
</style>
</head>
<body>
{svg}
</body>
</html>"""

    return svg, html


def main():
    parser = argparse.ArgumentParser(description="生成深色主题 SVG 横向条形图")
    parser.add_argument("--input", "-i", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", "-o", default="chart.html", help="输出 HTML 文件路径")
    parser.add_argument("--svg-output", help="同时输出 SVG 文件路径（可选）")
    parser.add_argument("--title", help="图表标题（覆盖 JSON 中的值）")
    parser.add_argument("--subtitle", help="副标题")
    parser.add_argument("--footer", help="页脚说明")
    parser.add_argument("--value-field", default="value", help="数值字段名（默认 value）")
    parser.add_argument("--label-field", default="label", help="标签字段名（默认 label）")
    parser.add_argument("--tag-field", help="分类标签字段名（可选）")
    parser.add_argument("--extra-field", help="附加信息字段名（可选）")
    parser.add_argument("--value-suffix", default="", help="数值后缀，如 %、亿")
    parser.add_argument("--max-value", type=float, help="Y 轴最大值（默认自动）")
    parser.add_argument("--ref-line", type=float, help="参考线数值")
    parser.add_argument("--ref-label", default="参考线", help="参考线标签")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 构建 items
    raw_items = data.get("items", data if isinstance(data, list) else [])
    items = []
    for it in raw_items:
        item = {
            "label": str(it.get(args.label_field, it.get("label", ""))),
            "value": float(it.get(args.value_field, it.get("value", 0))),
        }
        if args.tag_field and args.tag_field in it:
            item["tag"] = str(it[args.tag_field])
        elif "tag" in it:
            item["tag"] = str(it["tag"])
        if args.extra_field and args.extra_field in it:
            item["extra"] = str(it[args.extra_field])
        elif "extra" in it:
            item["extra"] = str(it["extra"])
        items.append(item)

    config = {
        "title":           args.title or data.get("title", "图表"),
        "subtitle":        args.subtitle or data.get("subtitle", ""),
        "footer":          args.footer or data.get("footer", ""),
        "kpis":            data.get("kpis"),
        "value_suffix":    args.value_suffix or data.get("value_suffix", ""),
        "max_value_override": args.max_value or data.get("max_value"),
        "show_reference_line": args.ref_line or data.get("ref_line"),
        "reference_label": args.ref_label or data.get("ref_label", "参考线"),
    }

    svg_str, html_str = build_svg_chart(items, config)

    out_path = Path(args.output)
    out_path.write_text(html_str, encoding="utf-8")
    print(f"已生成 HTML: {out_path.resolve()}")

    if args.svg_output:
        svg_path = Path(args.svg_output)
        svg_path.write_text(svg_str, encoding="utf-8")
        print(f"已生成 SVG:  {svg_path.resolve()}")


if __name__ == "__main__":
    main()
