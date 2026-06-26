#!/usr/bin/env python3
"""
SVG Page Generator with proper Chinese text wrapping.
Uses PIL/Pillow to measure actual character widths.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

# Default font settings
FONT_FAMILY = "PingFang SC,Microsoft YaHei,Noto Sans CJK SC,sans-serif"
BODY_FONT_SIZE = 14
TITLE_FONT_SIZE = 18
HEADING_FONT_SIZE = 22
LARGE_FONT_SIZE = 36
CARD_PADDING_X = 24
CARD_PADDING_TOP = 36
LINE_HEIGHT_RATIO = 1.6
CARD_RADIUS = 8


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load font with fallback chain."""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    # Try system fonts first
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except OSError:
            pass
    # PIL default
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def measure_text_width(text: str, size: int, bold: bool = False) -> int:
    """Measure exact pixel width of text using PIL."""
    try:
        font = get_font(size, bold)
        # Use getlength for accurate measurement
        return int(font.getlength(text))
    except Exception:
        # Fallback: estimate based on char count
        return int(len(text) * size * 0.6)


def wrap_text_chinese(text: str, max_width: int, size: int = BODY_FONT_SIZE) -> list[str]:
    """
    Wrap Chinese text to fit within max_width pixels.
    Handles mixed Chinese/English text correctly.
    """
    if not text:
        return []

    font = get_font(size)
    lines = []
    current_line = ""

    # Split by explicit newlines first
    paragraphs = text.replace('\\n', '\n').split('\n')

    for paragraph in paragraphs:
        if not paragraph.strip():
            if current_line:
                lines.append(current_line)
                current_line = ""
            continue

        for char in paragraph:
            test_line = current_line + char
            width = int(font.getlength(test_line))
            if width > max_width and current_line:
                lines.append(current_line)
                current_line = char
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)
            current_line = ""

    if current_line:
        lines.append(current_line)

    return lines


def card(x: int, y: int, w: int, h: int,
          title: str = "", body: str = "",
          accent: str = "#2563EB",
          rx: int = CARD_RADIUS) -> str:
    """
    Generate SVG card with properly wrapped Chinese text.
    """
    lines = [
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#F8F9FA" stroke="#E5E7EB" stroke-width="1"/>',
    ]

    if title:
        title_lines = wrap_text_chinese(title, w - CARD_PADDING_X * 2, TITLE_FONT_SIZE)
        ty = y + CARD_PADDING_TOP
        for ln in title_lines[:2]:
            lines.append(
                f'  <text x="{x + CARD_PADDING_X}" y="{ty}" '
                f'font-family="{FONT_FAMILY}" font-size="{TITLE_FONT_SIZE}" font-weight="bold" fill="#1A1A2E">'
                f'{escape_svg(ln)}</text>'
            )
            ty += int(TITLE_FONT_SIZE * LINE_HEIGHT_RATIO)

    if body:
        body_width = w - CARD_PADDING_X * 2
        body_lines = wrap_text_chinese(body, body_width, BODY_FONT_SIZE)
        by = ty + 16
        max_lines = 7
        for i, ln in enumerate(body_lines[:max_lines]):
            lines.append(
                f'  <text x="{x + CARD_PADDING_X}" y="{by + i * int(BODY_FONT_SIZE * LINE_HEIGHT_RATIO)}" '
                f'font-family="{FONT_FAMILY}" font-size="{BODY_FONT_SIZE}" fill="#4B5563">'
                f'{escape_svg(ln)}</text>'
            )

    return '\n'.join(lines)


def big_number(x: int, y: int, number: str, unit: str, description: str,
               bg: str = "#FEF3C7", accent: str = "#F59E0B") -> str:
    """Generate a big stat callout block."""
    lines = [
        f'  <rect x="{x}" y="{y}" width="520" height="260" rx="{CARD_RADIUS}" fill="{bg}" stroke="{accent}" stroke-width="1"/>',
        f'  <text x="{x + 40}" y="{y + 80}" font-family="{FONT_FAMILY}" font-size="56" font-weight="bold" fill="{accent}">{escape_svg(number)}</text>',
        f'  <text x="{x + 40}" y="{y + 120}" font-family="{FONT_FAMILY}" font-size="18" fill="{accent}">{escape_svg(unit)}</text>',
    ]
    if description:
        desc_lines = wrap_text_chinese(description, 440, BODY_FONT_SIZE)
        for i, ln in enumerate(desc_lines[:4]):
            lines.append(
                f'  <text x="{x + 40}" y="{y + 160 + i * 24}" '
                f'font-family="{FONT_FAMILY}" font-size="{BODY_FONT_SIZE}" fill="#4B5563">{escape_svg(ln)}</text>'
            )
    return '\n'.join(lines)


def chapter_intro(page_num: str, title: str, subtitle: str = "",
                  bg: str = "#1E3A8A", accent: str = "#F59E0B") -> str:
    """Generate a chapter intro slide."""
    num_size = 80
    title_size = 40
    subtitle_size = 16
    content = [
        f'  <rect width="1280" height="720" fill="{bg}"/>',
        f'  <rect x="0" y="0" width="8" height="720" fill="{accent}"/>',
        f'  <text x="80" y="200" font-family="{FONT_FAMILY}" font-size="{num_size}" font-weight="bold" fill="#FFFFFF">{escape_svg(page_num)}</text>',
        f'  <text x="80" y="320" font-family="{FONT_FAMILY}" font-size="{title_size}" font-weight="bold" fill="{accent}">{escape_svg(title)}</text>',
        f'  <line x1="80" y1="370" x2="500" y2="370" stroke="#FFFFFF" stroke-width="3"/>',
    ]
    if subtitle:
        sub_lines = wrap_text_chinese(subtitle, 900, subtitle_size)
        for i, ln in enumerate(sub_lines[:3]):
            content.append(
                f'  <text x="80" y="{460 + i * 28}" font-family="{FONT_FAMILY}" font-size="{subtitle_size}" fill="#9CA3AF">{escape_svg(ln)}</text>'
            )
    content.append('  <rect width="1280" height="720" fill="none" stroke="none"/>')
    return '\n'.join(content)


def cover_page(title: str, subtitle: str = "", source: str = "") -> str:
    """Generate cover slide."""
    lines = [
        '  <rect width="1280" height="720" fill="#1E3A8A"/>',
        '  <rect x="0" y="0" width="8" height="720" fill="#F59E0B"/>',
    ]
    title_lines = wrap_text_chinese(title, 1100, 48)
    ty = 280
    for ln in title_lines[:3]:
        lines.append(
            f'  <text x="80" y="{ty}" font-family="{FONT_FAMILY}" font-size="48" font-weight="bold" fill="#FFFFFF">{escape_svg(ln)}</text>'
        )
        ty += 60
    if subtitle:
        sub_lines = wrap_text_chinese(subtitle, 900, 20)
        for i, ln in enumerate(sub_lines[:2]):
            lines.append(
                f'  <text x="80" y="{ty + 10 + i * 30}" font-family="{FONT_FAMILY}" font-size="20" fill="#93C5FD">{escape_svg(ln)}</text>'
            )
    lines.append('  <line x1="80" y1="430" x2="500" y2="430" stroke="#F59E0B" stroke-width="3"/>')
    if source:
        src_lines = wrap_text_chinese(source, 900, 12)
        for i, ln in enumerate(src_lines[:2]):
            lines.append(
                f'  <text x="80" y="{660 + i * 20}" font-family="{FONT_FAMILY}" font-size="12" fill="#9CA3AF">{escape_svg(ln)}</text>'
            )
    return '\n'.join(lines)


def toc_page(items: list[tuple[str, str]]) -> str:
    """Generate table of contents slide."""
    lines = [
        '  <text x="80" y="100" font-family="{FONT_FAMILY}" font-size="36" font-weight="bold" fill="#1E3A8A">目录</text>',
        '  <line x1="80" y1="130" x2="200" y2="130" stroke="#2563EB" stroke-width="3"/>',
    ]
    for i, (num, title) in enumerate(items):
        y = 160 + i * 85
        lines.append(f'  <rect x="80" y="{y}" width="1120" height="70" rx="8" fill="#F8F9FA" stroke="#E5E7EB" stroke-width="1"/>')
        lines.append(f'  <text x="110" y="{y+45}" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold" fill="#1E3A8A">{escape_svg(num)}</text>')
        lines.append(f'  <text x="180" y="{y+45}" font-family="{FONT_FAMILY}" font-size="18" fill="#1A1A2E">{escape_svg(title)}</text>')
    return '\n'.join(lines)


def summary_page(key_points: list[str], accent: str = "#2563EB") -> str:
    """Generate summary slide."""
    lines = [
        '  <rect width="1280" height="720" fill="#1E3A8A"/>',
        '  <rect x="0" y="0" width="8" height="720" fill="#F59E0B"/>',
        '  <text x="80" y="100" font-family="{FONT_FAMILY}" font-size="36" font-weight="bold" fill="#FFFFFF">总结与展望</text>',
        '  <line x1="80" y1="135" x2="300" y2="135" stroke="#F59E0B" stroke-width="3"/>',
    ]
    y = 170
    for i, point in enumerate(key_points[:6]):
        pt_lines = wrap_text_chinese(point, 1000, 15)
        for j, ln in enumerate(pt_lines):
            lines.append(
                f'  <rect x="80" y="{y - 12}" width="4" height="20" rx="2" fill="#F59E0B"/>'
            )
            lines.append(
                f'  <text x="100" y="{y + j * 24}" font-family="{FONT_FAMILY}" font-size="15" fill="#FFFFFF">{escape_svg(ln)}</text>'
            )
        y += 20 + len(pt_lines) * 24
    return '\n'.join(lines)


def page_title_text(x: int, y: int, text: str, size: int = 28) -> str:
    """Generate a page title with underline."""
    lines = [
        f'  <text x="{x}" y="{y}" font-family="{FONT_FAMILY}" font-size="{size}" font-weight="bold" fill="#1A1A2E">{escape_svg(text)}</text>',
        f'  <line x1="{x}" y1="{y + 8}" x2="{x + 600}" y2="{y + 8}" stroke="#E5E7EB" stroke-width="1"/>',
    ]
    return '\n'.join(lines)


def escape_svg(text: str) -> str:
    """Escape special characters for SVG text element."""
    return (str(text)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&apos;'))


def make_svg(body_content: str) -> str:
    """Wrap content in complete SVG document."""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
{body_content}
</svg>'''


def main() -> int:
    if len(sys.argv) != 3:
        print('Usage: generate_svg.py <input.json> <output_dir>', file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        data = json.loads(input_path.read_text(encoding='utf-8'))
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    pages = data.get('pages', [])
    for i, page in enumerate(pages, 1):
        content = page.get('content', '')
        out_path = output_dir / f'page_{i:02d}.svg'
        out_path.write_text(make_svg(content), encoding='utf-8')
        print(f'WROTE {out_path.name}')

    print(f'DONE {len(pages)} pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
