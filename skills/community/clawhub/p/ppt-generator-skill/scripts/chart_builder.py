#!/usr/bin/env python3
"""
chart_builder.py — Render chart/image visuals from structured slide data.

v4.1 redesign: eliminates fragile string micro-syntax parsing.

Two inputs are now handled separately:

1. `chart` field (structured dict — primary path for charts):
   {
     "type": "bar",
     "title": "季度营收",
     "data": [
       {"label": "Q1", "value": 120},
       {"label": "Q2", "value": 145}
     ]
   }
   → Rendered as a real PptxGenJS chart.
   → validator.py validates this field fully before it reaches here.
   → No parsing, no regex, no format drift.

2. `visual_hint` field (plain text string — non-chart visuals only):
   "image:Team photo"   → gray placeholder box (honest for content that can't be auto-generated)
   "icon:rocket"        → colored accent shape
   ""                   → nothing

   visual_hint no longer accepts chart syntax.
   If a chart dict is present, visual_hint is ignored for rendering.

This module is imported by generate_ppt.py — it does NOT run standalone.
"""

import json as _json
from typing import List


VALID_CHART_TYPES = {"bar", "line", "pie", "doughnut", "area"}


# ── Color helpers ─────────────────────────────────────────────────────────────

def _chart_colors(primary: str, secondary: str) -> list:
    """6-color series anchored on the presentation palette."""
    return [primary, secondary, "A8DADC", "457B9D", "E63946", "F1FAEE"]


# ── Chart field renderer ──────────────────────────────────────────────────────

def chart_to_js(
    chart: dict,
    slide_var: str = "slide",
    x: float = 0.5,
    y: float = 1.1,
    w: float = 9.0,
    h: float = 3.8,
    primary: str = "1E2761",
    secondary: str = "CADCFC",
) -> List[str]:
    """
    Render a `chart` field dict as PptxGenJS addChart() lines.

    chart dict schema (already validated by validator.py):
      {
        "type":  "bar" | "line" | "pie" | "doughnut" | "area",
        "title": "optional chart title string",
        "data":  [{"label": "Q1", "value": 120}, ...]
      }

    Returns [] if chart is None, empty, or missing data.
    """
    if not chart or not isinstance(chart, dict):
        return []

    chart_type = str(chart.get("type", "bar")).lower()
    if chart_type not in VALID_CHART_TYPES:
        chart_type = "bar"

    title      = str(chart.get("title", ""))
    data_items = chart.get("data", [])

    if not data_items:
        return []

    labels = [str(item.get("label", f"Item {i+1}")) for i, item in enumerate(data_items)]
    values = []
    for item in data_items:
        v = item.get("value", 0)
        try:
            values.append(float(v))
        except (TypeError, ValueError):
            values.append(0.0)

    colors = _chart_colors(primary, secondary)
    series_colors = (colors * ((len(labels) // len(colors)) + 1))[:len(labels)]

    type_map = {
        "bar":      "pres.charts.BAR",
        "line":     "pres.charts.LINE",
        "pie":      "pres.charts.PIE",
        "doughnut": "pres.charts.DOUGHNUT",
        "area":     "pres.charts.AREA",
    }
    pptx_type = type_map[chart_type]

    lines = []
    lines.append(f"  {slide_var}.addChart({pptx_type}, [{{")
    lines.append(f"    name: {_json.dumps(title or chart_type.title() + ' Chart')},")
    lines.append(f"    labels: {_json.dumps(labels)},")
    lines.append(f"    values: {_json.dumps(values)},")
    lines.append(f"  }}], {{")
    lines.append(f"    x: {x}, y: {y}, w: {w}, h: {h},")

    if chart_type == "bar":
        lines.append(f"    barDir: 'col',")

    if chart_type in ("pie", "doughnut"):
        lines.append(f"    showPercent: true,")
        lines.append(f"    chartColors: {_json.dumps(series_colors)},")
    else:
        lines.append(f"    chartColors: {_json.dumps([primary])},")

    lines.append(f"    chartArea: {{ fill: {{ color: 'FFFFFF' }}, roundedCorners: true }},")
    lines.append(f"    catAxisLabelColor: '64748B',")
    lines.append(f"    valAxisLabelColor: '64748B',")
    lines.append(f"    valGridLine: {{ color: 'E2E8F0', size: 0.5 }},")
    lines.append(f"    catGridLine: {{ style: 'none' }},")
    lines.append(f"    showValue: true,")
    lines.append(f"    dataLabelColor: '1E293B',")
    lines.append(f"    showLegend: {_json.dumps(chart_type in ('pie', 'doughnut'))},")
    lines.append(f"    showTitle: {_json.dumps(bool(title))},")

    if title:
        lines.append(f"    title: {_json.dumps(title)},")

    if chart_type == "line":
        lines.append(f"    lineSmooth: true,")
        lines.append(f"    lineSize: 2,")

    lines.append(f"  }});")
    return lines


# ── visual_hint renderer (image / icon only) ──────────────────────────────────

def visual_hint_to_js(
    hint: str,
    slide_var: str = "slide",
    x: float = 0.5,
    y: float = 1.1,
    w: float = 9.0,
    h: float = 3.8,
    primary: str = "1E2761",
    secondary: str = "CADCFC",
) -> List[str]:
    """
    Render a `visual_hint` string for non-chart visuals only.

    Accepted:
      "image:<description>"  → gray dashed placeholder box
      "icon:<name>"          → colored accent shape with first letter

    Rejected gracefully:
      "chart:..."            → emits a JS comment warning, returns no chart
                               (chart data belongs in the `chart` field)
      ""                     → returns []
    """
    if not hint or not hint.strip():
        return []

    hint = hint.strip()

    if hint.lower().startswith("chart:"):
        return [
            f"  // [ppt-generator] WARNING: chart data found in visual_hint — ignored.",
            f"  // Move chart data to the structured 'chart' field instead.",
        ]

    if hint.lower().startswith("image:"):
        label = hint[6:].strip() or "Image"
        return _emit_image_placeholder(label, slide_var, x, y, w, h, secondary)

    if hint.lower().startswith("icon:"):
        name = hint[5:].strip() or "icon"
        return _emit_icon(name, slide_var, x, y, primary)

    return []


# ── Emitters ──────────────────────────────────────────────────────────────────

def _emit_image_placeholder(label: str, sv: str, x, y, w, h, secondary: str) -> List[str]:
    """
    Gray dashed placeholder box for image content.
    The other developer's approach — correct and honest for visuals
    that cannot be auto-generated (photos, KV artwork, custom graphics).
    """
    lines = []
    lines.append(f"  {sv}.addShape(pres.shapes.RECTANGLE, {{")
    lines.append(f"    x: {x}, y: {y}, w: {w}, h: {h},")
    lines.append(f"    fill: {{ color: '{secondary}', transparency: 40 }},")
    lines.append(f"    line: {{ color: '888888', width: 1, dashType: 'dash' }},")
    lines.append(f"  }});")
    lines.append(f"  {sv}.addShape(pres.shapes.OVAL, {{")
    lines.append(f"    x: {round(x + w/2 - 0.25, 2)}, y: {round(y + h/2 - 0.55, 2)}, w: 0.5, h: 0.5,")
    lines.append(f"    fill: {{ color: 'CCCCCC' }},")
    lines.append(f"    line: {{ color: '888888', width: 1 }},")
    lines.append(f"  }});")
    lines.append(f"  {sv}.addText({_json.dumps(label)}, {{")
    lines.append(f"    x: {x}, y: {round(y + h/2 - 0.15, 2)}, w: {w}, h: 0.35,")
    lines.append(f"    fontSize: 12, color: '888888', align: 'center', italic: true")
    lines.append(f"  }});")
    return lines


def _emit_icon(name: str, sv: str, x, y, primary: str) -> List[str]:
    """Colored rounded square accent marker with first letter."""
    letter = name[0].upper()
    lines = []
    lines.append(f"  {sv}.addShape(pres.shapes.ROUNDED_RECTANGLE, {{")
    lines.append(f"    x: {x}, y: {y}, w: 0.6, h: 0.6,")
    lines.append(f"    fill: {{ color: '{primary}' }},")
    lines.append(f"    line: {{ color: '{primary}', width: 0 }},")
    lines.append(f"    rectRadius: 0.1,")
    lines.append(f"  }});")
    lines.append(f"  {sv}.addText({_json.dumps(letter)}, {{")
    lines.append(f"    x: {x}, y: {y}, w: 0.6, h: 0.6,")
    lines.append(f"    fontSize: 18, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle'")
    lines.append(f"  }});")
    return lines
