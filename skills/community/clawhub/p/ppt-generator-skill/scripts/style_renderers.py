#!/usr/bin/env python3
"""
style_renderers.py — Per-category visual layout renderers for PptxGenJS.

Each renderer generates JS lines for a single slide, using the category's
unique visual language (layout structure, decorative elements, spacing).
All renderers share the same function signature:

    render(lines, slide_data, palette, fonts, has_visual, visual_lines)

Where:
  lines        — list[str] to append JS code to (mutated in place)
  slide_data   — dict with keys: layout, title, subtitle, body, notes
  palette      — dict with keys: primary, secondary, accent
  fonts        — dict with keys: heading, body
  has_visual   — bool: whether visual_lines is non-empty
  visual_lines — list[str]: pre-built JS lines for chart/image (from chart_builder)

v4.3 — initial creation with 10 category renderers + 1 default fallback.
"""

import json as _json


# ═══════════════════════════════════════════════════════════════════════════════
# Helper: emit speaker notes + footer
# ═══════════════════════════════════════════════════════════════════════════════

def _notes(lines, notes_text):
    if notes_text:
        lines.append(f"  slide.addNotes({_json.dumps(notes_text)});")


def _footer_bar(lines, primary):
    """Thin colored footer strip for light slides."""
    lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 5.425, w: 10, h: 0.2, fill: {{ color: PRIMARY, transparency: 70 }}, line: {{ color: PRIMARY, width: 0 }} }});")


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 企业商务 — Corporate: dark title bar on top, clean structure
# ═══════════════════════════════════════════════════════════════════════════════

def render_corporate(lines, sd, pal, fonts, has_visual, visual_lines):
    layout   = sd.get("layout", "content")
    title    = sd.get("title", "")
    subtitle = sd.get("subtitle", "")
    body     = sd.get("body", [])
    notes    = sd.get("notes", "")

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")

    if layout == "title":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 4.8, w: 10, h: 0.825, fill: {{ color: ACCENT, transparency: 85 }}, line: {{ color: ACCENT, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.7, y: 1.6, w: 8.6, h: 1.6, fontSize: 44, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'middle' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.7, y: 3.3, w: 8.6, h: 0.8, fontSize: 20, fontFace: FONT_B, color: SECONDARY, align: 'left' }});")

    elif layout == "section":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0.6, y: 2.4, w: 0.08, h: 1.0, fill: {{ color: SECONDARY }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.9, y: 2.2, w: 8.5, h: 1.3, fontSize: 36, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'middle' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.9, y: 3.6, w: 8.5, h: 0.7, fontSize: 16, fontFace: FONT_B, color: SECONDARY }});")

    elif layout == "stat":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        _corporate_title_bar(lines, title, subtitle)
        _render_stat_boxes(lines, body, title)
        _footer_bar(lines, pal["primary"])

    elif layout == "quote":
        _render_quote(lines, body, title, subtitle)

    elif layout == "two-column":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        _corporate_title_bar(lines, title, subtitle)
        _render_two_col(lines, body)
        _footer_bar(lines, pal["primary"])

    else:  # content
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        _corporate_title_bar(lines, title, subtitle)
        body_y = 1.55 if subtitle else 1.05
        body_h = round(5.425 - body_y - 0.2, 3)
        if body and has_visual:
            _render_bullets(lines, body, 0.4, body_y, 4.4, body_h, 15)
        elif body:
            _render_bullets(lines, body, 0.5, body_y, 9.0, body_h, 16)
        if has_visual and layout not in ("title", "section", "quote"):
            lines.extend(visual_lines)
        _footer_bar(lines, pal["primary"])

    _notes(lines, notes)
    lines.append("}")
    lines.append("")


def _corporate_title_bar(lines, title, subtitle):
    lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 10, h: 0.9, fill: {{ color: PRIMARY }}, line: {{ color: PRIMARY, width: 0 }} }});")
    lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 24, fontFace: FONT_H, color: ACCENT, bold: true, valign: 'middle', margin: 0 }});")
    if subtitle:
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0.4, y: 0.95, w: 1.2, h: 0.05, fill: {{ color: SECONDARY }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.4, y: 1.0, w: 9.2, h: 0.45, fontSize: 14, fontFace: FONT_B, color: '555555', italic: true }});")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 未来科技 — Tech: left sidebar navigation feel
# ═══════════════════════════════════════════════════════════════════════════════

def render_tech(lines, sd, pal, fonts, has_visual, visual_lines):
    layout   = sd.get("layout", "content")
    title    = sd.get("title", "")
    subtitle = sd.get("subtitle", "")
    body     = sd.get("body", [])
    notes    = sd.get("notes", "")

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")

    if layout == "title":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        # Geometric accent block
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 3.5, h: 5.625, fill: {{ color: SECONDARY, transparency: 80 }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 3.8, w: 10, h: 0.06, fill: {{ color: SECONDARY }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 1.2, w: 8.4, h: 2.0, fontSize: 42, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'bottom' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 4.0, w: 8.4, h: 0.8, fontSize: 18, fontFace: FONT_B, color: SECONDARY }});")

    elif layout == "section":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 2.5, w: 10, h: 0.04, fill: {{ color: SECONDARY }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 1.5, w: 8.4, h: 1.0, fontSize: 36, fontFace: FONT_H, color: ACCENT, bold: true }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 2.7, w: 8.4, h: 0.7, fontSize: 16, fontFace: FONT_B, color: SECONDARY }});")

    elif layout == "stat":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 0.5, h: 5.625, fill: {{ color: PRIMARY }}, line: {{ color: PRIMARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.2, w: 8.5, h: 0.7, fontSize: 22, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        _render_stat_boxes(lines, body, title)

    elif layout == "quote":
        _render_quote(lines, body, title, subtitle)

    elif layout == "two-column":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 0.5, h: 5.625, fill: {{ color: PRIMARY }}, line: {{ color: PRIMARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.2, w: 8.5, h: 0.7, fontSize: 22, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        _render_two_col(lines, body, left_x=0.8, right_x=5.3, y=1.1)

    else:  # content
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        # Left sidebar accent
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 0.5, h: 5.625, fill: {{ color: PRIMARY }}, line: {{ color: PRIMARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.2, w: 8.5, h: 0.7, fontSize: 22, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 0.85, w: 8.5, h: 0.35, fontSize: 13, fontFace: FONT_B, color: '888888', italic: true }});")
        body_y = 1.35 if subtitle else 1.05
        body_h = 4.2
        if body and has_visual:
            _render_bullets(lines, body, 0.8, body_y, 4.0, body_h, 15)
        elif body:
            _render_bullets(lines, body, 0.8, body_y, 8.5, body_h, 16)
        if has_visual:
            lines.extend(visual_lines)

    _notes(lines, notes)
    lines.append("}")
    lines.append("")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 学术研究 — Academic: clean, generous whitespace, thin separator
# ═══════════════════════════════════════════════════════════════════════════════

def render_academic(lines, sd, pal, fonts, has_visual, visual_lines):
    layout   = sd.get("layout", "content")
    title    = sd.get("title", "")
    subtitle = sd.get("subtitle", "")
    body     = sd.get("body", [])
    notes    = sd.get("notes", "")

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")

    if layout == "title":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 10, h: 2.8, fill: {{ color: PRIMARY }}, line: {{ color: PRIMARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.6, w: 8.4, h: 1.5, fontSize: 38, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'bottom' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 3.2, w: 8.4, h: 0.8, fontSize: 18, fontFace: FONT_B, color: '555555' }});")

    elif layout == "section":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 1.0, y: 2.0, w: 8.0, h: 1.2, fontSize: 32, fontFace: FONT_H, color: PRIMARY, bold: true, align: 'center', valign: 'middle' }});")
        lines.append(f"  slide.addShape(pres.shapes.LINE, {{ x: 4.0, y: 3.3, w: 2.0, h: 0, line: {{ color: PRIMARY, width: 1.5 }} }});")

    elif layout == "stat":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.3, w: 8.4, h: 0.7, fontSize: 22, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        lines.append(f"  slide.addShape(pres.shapes.LINE, {{ x: 0.8, y: 1.05, w: 8.4, h: 0, line: {{ color: SECONDARY, width: 0.5 }} }});")
        _render_stat_boxes(lines, body, title)

    elif layout == "quote":
        _render_quote(lines, body, title, subtitle)

    elif layout == "two-column":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.3, w: 8.4, h: 0.7, fontSize: 22, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        lines.append(f"  slide.addShape(pres.shapes.LINE, {{ x: 0.8, y: 1.05, w: 8.4, h: 0, line: {{ color: SECONDARY, width: 0.5 }} }});")
        _render_two_col(lines, body, y=1.3)

    else:  # content
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.3, w: 8.4, h: 0.7, fontSize: 24, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        lines.append(f"  slide.addShape(pres.shapes.LINE, {{ x: 0.8, y: 1.05, w: 8.4, h: 0, line: {{ color: SECONDARY, width: 0.5 }} }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 1.1, w: 8.4, h: 0.35, fontSize: 13, fontFace: FONT_B, color: '888888', italic: true }});")
        body_y = 1.55 if subtitle else 1.2
        body_h = 4.0
        if body and has_visual:
            _render_bullets(lines, body, 0.8, body_y, 4.0, body_h, 15)
        elif body:
            _render_bullets(lines, body, 0.8, body_y, 8.4, body_h, 16)
        if has_visual:
            lines.extend(visual_lines)

    _notes(lines, notes)
    lines.append("}")
    lines.append("")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 年终总结 — Year-end: large numbering, timeline feel
# ═══════════════════════════════════════════════════════════════════════════════

def render_yearend(lines, sd, pal, fonts, has_visual, visual_lines):
    layout   = sd.get("layout", "content")
    title    = sd.get("title", "")
    subtitle = sd.get("subtitle", "")
    body     = sd.get("body", [])
    notes    = sd.get("notes", "")
    index    = sd.get("index", 1)

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")

    if layout == "title":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        # Large year number watermark
        lines.append(f"  slide.addText('2024', {{ x: -0.5, y: 1.0, w: 11, h: 3.5, fontSize: 140, fontFace: FONT_H, color: ACCENT, bold: true, align: 'center', valign: 'middle', transparency: 90 }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 1.8, w: 8.4, h: 1.4, fontSize: 40, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'middle' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 3.4, w: 8.4, h: 0.7, fontSize: 18, fontFace: FONT_B, color: SECONDARY }});")

    elif layout == "section":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.LINE, {{ x: 0.8, y: 2.8, w: 8.4, h: 0, line: {{ color: SECONDARY, width: 1 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 1.5, w: 8.4, h: 1.2, fontSize: 34, fontFace: FONT_H, color: ACCENT, bold: true }});")

    elif layout == "stat":
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 0.3, w: 8.4, h: 0.7, fontSize: 22, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        _render_stat_boxes(lines, body, title)
        _footer_bar(lines, pal["primary"])

    elif layout == "quote":
        _render_quote(lines, body, title, subtitle)

    else:  # content + two-column
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        # Large index number on left
        idx_str = f"{index:02d}" if index < 100 else str(index)
        lines.append(f"  slide.addText({_json.dumps(idx_str)}, {{ x: 0.3, y: 0.2, w: 1.2, h: 1.2, fontSize: 48, fontFace: FONT_H, color: PRIMARY, bold: true, align: 'center', valign: 'middle', transparency: 30 }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 1.6, y: 0.25, w: 7.8, h: 0.7, fontSize: 22, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 1.6, y: 0.9, w: 7.8, h: 0.35, fontSize: 13, fontFace: FONT_B, color: '888888', italic: true }});")
        body_y = 1.4 if subtitle else 1.1
        body_h = 4.0
        if body and has_visual:
            _render_bullets(lines, body, 1.6, body_y, 3.2, body_h, 15)
        elif body:
            _render_bullets(lines, body, 1.6, body_y, 7.8, body_h, 16)
        if has_visual:
            lines.extend(visual_lines)
        _footer_bar(lines, pal["primary"])

    _notes(lines, notes)
    lines.append("}")
    lines.append("")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 扁平简约 — Minimal: almost no decoration, Keynote-like
# ═══════════════════════════════════════════════════════════════════════════════

def render_minimal(lines, sd, pal, fonts, has_visual, visual_lines):
    layout   = sd.get("layout", "content")
    title    = sd.get("title", "")
    subtitle = sd.get("subtitle", "")
    body     = sd.get("body", [])
    notes    = sd.get("notes", "")

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")
    lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")

    if layout == "title":
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 1.0, y: 1.8, w: 8.0, h: 1.6, fontSize: 42, fontFace: FONT_H, color: PRIMARY, bold: true, align: 'left', valign: 'bottom' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 1.0, y: 3.6, w: 8.0, h: 0.6, fontSize: 16, fontFace: FONT_B, color: '999999' }});")

    elif layout == "section":
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 1.0, y: 2.2, w: 8.0, h: 1.0, fontSize: 30, fontFace: FONT_H, color: PRIMARY, bold: true, align: 'left', valign: 'middle' }});")

    elif layout == "stat":
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 1.0, y: 0.4, w: 8.0, h: 0.6, fontSize: 20, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        _render_stat_boxes(lines, body, title)

    elif layout == "quote":
        _render_quote(lines, body, title, subtitle)

    else:  # content, two-column
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 1.0, y: 0.4, w: 8.0, h: 0.7, fontSize: 24, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 1.0, y: 1.05, w: 8.0, h: 0.3, fontSize: 13, fontFace: FONT_B, color: '999999' }});")
        body_y = 1.45 if subtitle else 1.2
        body_h = 4.0
        if body and has_visual:
            _render_bullets(lines, body, 1.0, body_y, 3.8, body_h, 15)
        elif body:
            _render_bullets(lines, body, 1.0, body_y, 8.0, body_h, 16)
        if has_visual:
            lines.extend(visual_lines)

    _notes(lines, notes)
    lines.append("}")
    lines.append("")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 中国风 — Chinese traditional: right-side accent strip, warm tones
# ═══════════════════════════════════════════════════════════════════════════════

def render_chinese(lines, sd, pal, fonts, has_visual, visual_lines):
    layout   = sd.get("layout", "content")
    title    = sd.get("title", "")
    subtitle = sd.get("subtitle", "")
    body     = sd.get("body", [])
    notes    = sd.get("notes", "")

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")

    if layout == "title":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 8.8, y: 0, w: 1.2, h: 5.625, fill: {{ color: SECONDARY, transparency: 75 }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 1.5, w: 7.5, h: 1.8, fontSize: 40, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'middle' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 3.5, w: 7.5, h: 0.7, fontSize: 18, fontFace: FONT_B, color: SECONDARY }});")

    elif layout == "section":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 9.5, y: 0, w: 0.5, h: 5.625, fill: {{ color: SECONDARY, transparency: 50 }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 2.0, w: 8.0, h: 1.2, fontSize: 34, fontFace: FONT_H, color: ACCENT, bold: true }});")

    else:  # content, stat, quote, two-column
        lines.append(f"  slide.background = {{ color: SECONDARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 9.5, y: 0, w: 0.5, h: 5.625, fill: {{ color: PRIMARY }}, line: {{ color: PRIMARY, width: 0 }} }});")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.6, y: 0.3, w: 8.5, h: 0.7, fontSize: 24, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.6, y: 0.95, w: 8.5, h: 0.35, fontSize: 13, fontFace: FONT_B, color: '777777', italic: true }});")

        if layout == "stat":
            _render_stat_boxes(lines, body, title)
        elif layout == "quote":
            _render_quote_inline(lines, body, subtitle)
        else:
            body_y = 1.45 if subtitle else 1.15
            body_h = 4.0
            if body and has_visual:
                _render_bullets(lines, body, 0.6, body_y, 4.0, body_h, 15)
            elif body:
                _render_bullets(lines, body, 0.6, body_y, 8.5, body_h, 16)
            if has_visual:
                lines.extend(visual_lines)

    _notes(lines, notes)
    lines.append("}")
    lines.append("")


# ═══════════════════════════════════════════════════════════════════════════════
# 7-10: Remaining styles — each with their own layout identity
# ═══════════════════════════════════════════════════════════════════════════════

def render_art(lines, sd, pal, fonts, has_visual, visual_lines):
    """文化艺术 — Gallery: centered titles, cream backgrounds, elegant."""
    _render_generic_with_motif(lines, sd, pal, has_visual, visual_lines,
        title_bg=False, content_bg_color="SECONDARY",
        title_align="center", accent_element="bottom_line")

def render_fresh(lines, sd, pal, fonts, has_visual, visual_lines):
    """文艺清新 — Fresh: rounded corners feel, soft tones, generous padding."""
    _render_generic_with_motif(lines, sd, pal, has_visual, visual_lines,
        title_bg=False, content_bg_color="'FFFFFF'",
        title_align="left", accent_element="top_dots")

def render_cartoon(lines, sd, pal, fonts, has_visual, visual_lines):
    """卡通手绘 — Cartoon: colored rounded card, vibrant, playful."""
    _render_generic_with_motif(lines, sd, pal, has_visual, visual_lines,
        title_bg=True, content_bg_color="SECONDARY",
        title_align="center", accent_element="corner_circle")

def render_creative(lines, sd, pal, fonts, has_visual, visual_lines):
    """创意趣味 — Creative: asymmetric, diagonal accent, bold."""
    _render_generic_with_motif(lines, sd, pal, has_visual, visual_lines,
        title_bg=True, content_bg_color="'FFFFFF'",
        title_align="left", accent_element="diagonal_bar")


def _render_generic_with_motif(lines, sd, pal, has_visual, visual_lines,
                                title_bg, content_bg_color,
                                title_align, accent_element):
    """Shared renderer for styles 7-10 with customizable motif."""
    layout   = sd.get("layout", "content")
    title    = sd.get("title", "")
    subtitle = sd.get("subtitle", "")
    body     = sd.get("body", [])
    notes    = sd.get("notes", "")

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")

    if layout in ("title", "section"):
        if title_bg:
            lines.append(f"  slide.background = {{ color: PRIMARY }};")
            t_color = "ACCENT"
            s_color = "SECONDARY"
        else:
            lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
            t_color = "PRIMARY"
            s_color = "'777777'"

        # Accent element
        if accent_element == "bottom_line":
            lines.append(f"  slide.addShape(pres.shapes.LINE, {{ x: 3.5, y: 3.5, w: 3.0, h: 0, line: {{ color: SECONDARY, width: 2 }} }});")
        elif accent_element == "top_dots":
            for dx in range(3):
                lines.append(f"  slide.addShape(pres.shapes.OVAL, {{ x: {4.6 + dx * 0.35}, y: 1.5, w: 0.15, h: 0.15, fill: {{ color: SECONDARY }}, line: {{ color: SECONDARY, width: 0 }} }});")
        elif accent_element == "corner_circle":
            lines.append(f"  slide.addShape(pres.shapes.OVAL, {{ x: 8.5, y: -0.5, w: 2.0, h: 2.0, fill: {{ color: SECONDARY, transparency: 50 }}, line: {{ color: SECONDARY, width: 0 }} }});")
            lines.append(f"  slide.addShape(pres.shapes.OVAL, {{ x: -0.5, y: 4.5, w: 1.5, h: 1.5, fill: {{ color: SECONDARY, transparency: 60 }}, line: {{ color: SECONDARY, width: 0 }} }});")
        elif accent_element == "diagonal_bar":
            lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: -1, y: 4.0, w: 12, h: 0.6, fill: {{ color: SECONDARY, transparency: 60 }}, line: {{ color: SECONDARY, width: 0 }}, rotate: -3 }});")

        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.8, y: 1.8, w: 8.4, h: 1.5, fontSize: {38 if layout == 'title' else 32}, fontFace: FONT_H, color: {t_color}, bold: true, align: '{title_align}', valign: 'middle' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.8, y: 3.5, w: 8.4, h: 0.6, fontSize: 16, fontFace: FONT_B, color: {s_color}, align: '{title_align}' }});")
    else:
        lines.append(f"  slide.background = {{ color: {content_bg_color} }};")
        lines.append(f"  slide.addText({_json.dumps(title)}, {{ x: 0.6, y: 0.3, w: 8.8, h: 0.7, fontSize: 24, fontFace: FONT_H, color: PRIMARY, bold: true, align: '{title_align}' }});")
        if subtitle:
            lines.append(f"  slide.addText({_json.dumps(subtitle)}, {{ x: 0.6, y: 0.95, w: 8.8, h: 0.35, fontSize: 13, fontFace: FONT_B, color: '888888', italic: true }});")

        if layout == "stat":
            _render_stat_boxes(lines, body, title)
        elif layout == "quote":
            _render_quote_inline(lines, body, subtitle)
        else:
            body_y = 1.45 if subtitle else 1.15
            body_h = 4.0
            if body and has_visual:
                _render_bullets(lines, body, 0.6, body_y, 4.2, body_h, 15)
            elif body:
                _render_bullets(lines, body, 0.6, body_y, 8.8, body_h, 16)
            if has_visual:
                lines.extend(visual_lines)
        _footer_bar(lines, pal["primary"])

    _notes(lines, notes)
    lines.append("}")
    lines.append("")


# ═══════════════════════════════════════════════════════════════════════════════
# Shared layout primitives
# ═══════════════════════════════════════════════════════════════════════════════

def _render_bullets(lines, body, x, y, w, h, font_size):
    runs = [{"text": b, "options": {"bullet": True, "breakLine": True}} for b in body[:-1]]
    runs.append({"text": body[-1], "options": {"bullet": True}})
    lines.append(f"  slide.addText({_json.dumps(runs)}, {{")
    lines.append(f"    x: {x}, y: {y}, w: {w}, h: {h}, fontSize: {font_size}, fontFace: FONT_B,")
    lines.append(f"    color: '2D2D2D', valign: 'top', paraSpaceAfter: 6")
    lines.append(f"  }});")


def _render_stat_boxes(lines, body, title):
    stat_items = body[:3] if body else [title]
    n = len(stat_items)
    box_w = 8.0 / n
    for i, stat in enumerate(stat_items):
        parts = stat.split("|") if "|" in stat else [stat, ""]
        num   = parts[0].strip()
        label = parts[1].strip() if len(parts) > 1 else ""
        bx = 1.0 + i * box_w
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: {round(bx,2)}, y: 1.4, w: {round(box_w-0.2,2)}, h: 2.8, fill: {{ color: SECONDARY, transparency: 30 }}, line: {{ color: SECONDARY, width: 1 }}, shadow: makeShadow() }});")
        lines.append(f"  slide.addText({_json.dumps(num)}, {{ x: {round(bx,2)}, y: 1.6, w: {round(box_w-0.2,2)}, h: 1.6, fontSize: 52, fontFace: FONT_H, bold: true, color: PRIMARY, align: 'center', valign: 'middle' }});")
        if label:
            lines.append(f"  slide.addText({_json.dumps(label)}, {{ x: {round(bx,2)}, y: 3.3, w: {round(box_w-0.2,2)}, h: 0.7, fontSize: 14, fontFace: FONT_B, color: '555555', align: 'center' }});")


def _render_quote(lines, body, title, subtitle):
    lines.append(f"  slide.background = {{ color: SECONDARY }};")
    quote_text = body[0] if body else title
    lines.append(f"  slide.addText('\u201c', {{ x: 0.5, y: 0.2, w: 2, h: 1.5, fontSize: 96, fontFace: FONT_H, color: PRIMARY, bold: true }});")
    lines.append(f"  slide.addText({_json.dumps(quote_text)}, {{ x: 1.0, y: 1.2, w: 8.0, h: 2.8, fontSize: 26, fontFace: FONT_H, color: PRIMARY, italic: true, align: 'center', valign: 'middle' }});")
    if subtitle:
        lines.append(f"  slide.addText('\\u2014 ' + {_json.dumps(subtitle)}, {{ x: 1.0, y: 4.2, w: 8.0, h: 0.6, fontSize: 14, fontFace: FONT_B, color: PRIMARY, align: 'center' }});")


def _render_quote_inline(lines, body, subtitle):
    """Quote inside a content-style slide (not full-slide)."""
    quote_text = body[0] if body else ""
    if quote_text:
        lines.append(f"  slide.addText({_json.dumps('\u201c' + quote_text + '\u201d')}, {{ x: 1.0, y: 1.5, w: 8.0, h: 2.5, fontSize: 22, fontFace: FONT_H, color: PRIMARY, italic: true, align: 'center', valign: 'middle' }});")


def _render_two_col(lines, body, left_x=0.4, right_x=5.3, y=1.1):
    mid = len(body) // 2
    left_items  = body[:mid] if body else []
    right_items = body[mid:] if body else []
    if left_items:
        left_runs = [{"text": b, "options": {"bullet": True, "breakLine": True}} for b in left_items[:-1]]
        left_runs.append({"text": left_items[-1], "options": {"bullet": True}})
        lines.append(f"  slide.addText({_json.dumps(left_runs)}, {{ x: {left_x}, y: {y}, w: 4.3, h: 4.0, fontSize: 15, fontFace: FONT_B, color: '2D2D2D', valign: 'top' }});")
    if right_items:
        right_runs = [{"text": b, "options": {"bullet": True, "breakLine": True}} for b in right_items[:-1]]
        right_runs.append({"text": right_items[-1], "options": {"bullet": True}})
        lines.append(f"  slide.addText({_json.dumps(right_runs)}, {{ x: {right_x}, y: {y}, w: 4.3, h: 4.0, fontSize: 15, fontFace: FONT_B, color: '2D2D2D', valign: 'top' }});")
    sep_x = round((left_x + 4.3 + right_x) / 2, 1)
    lines.append(f"  slide.addShape(pres.shapes.LINE, {{ x: {sep_x}, y: {round(y + 0.1, 1)}, w: 0, h: 3.7, line: {{ color: SECONDARY, width: 1 }} }});")


# ═══════════════════════════════════════════════════════════════════════════════
# Registry — maps category name → renderer function
# ═══════════════════════════════════════════════════════════════════════════════

STYLE_RENDERERS = {
    "企业商务": render_corporate,
    "未来科技": render_tech,
    "学术研究": render_academic,
    "年终总结": render_yearend,
    "扁平简约": render_minimal,
    "中国风":   render_chinese,
    "文化艺术": render_art,
    "文艺清新": render_fresh,
    "卡通手绘": render_cartoon,
    "创意趣味": render_creative,
}


def get_renderer(category: str):
    """Return the renderer function for a style category, defaulting to corporate."""
    return STYLE_RENDERERS.get(category, render_corporate)
