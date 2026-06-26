"""
font_metrics.py — Accurate text width measurement using Pillow + system fonts.

Measures text rendering width using the same TrueType font files available
on the system, providing a reliable baseline for PPT text box sizing.
Results are in CSS pixels (matching the HTML viewport coordinate system).

Cross-platform safety margin is applied on top of the measured width to
account for DirectWrite (MS PPT) vs FreeType (Pillow/Linux) differences.
Empirical measurement shows DirectWrite renders 5-15% wider for Latin text.

Reference: Pillow ImageFont.getlength() uses FreeType2 advance widths
with 1/64 pixel precision (PR #4959).
"""

import os
import functools

from PIL import ImageFont

_FONT_SEARCH_PATHS = [
    "/usr/share/fonts/opentype/noto",
    "/usr/share/fonts/truetype/msttcorefonts",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/inter",
]

_FONT_MAP = {
    "Noto Sans CJK SC": "NotoSansCJK-Regular.ttc",
    "Noto Sans CJK SC Bold": "NotoSansCJK-Bold.ttc",
    "Microsoft YaHei": "NotoSansCJK-Regular.ttc",
    "PingFang SC": "NotoSansCJK-Regular.ttc",
    "Hiragino Sans GB": "NotoSansCJK-Regular.ttc",
    "SimSun": "NotoSansCJK-Regular.ttc",
    "Arial": "Arial.ttf",
    "Arial Bold": "Arial_Bold.ttf",
    "DejaVu Sans": "DejaVuSans.ttf",
    "Liberation Sans": "LiberationSans-Regular.ttf",
    "Inter": "Inter-Regular.ttf",
    "sans-serif": "DejaVuSans.ttf",
}

CROSS_PLATFORM_SAFETY_BASE = 1.12
CROSS_PLATFORM_SAFETY_LARGE = 1.20
LARGE_TEXT_THRESHOLD_PX = 54


@functools.lru_cache(maxsize=64)
def _find_font_file(family_name):
    """Resolve font family name to a file path on disk."""
    mapped = _FONT_MAP.get(family_name)
    if mapped:
        for search_dir in _FONT_SEARCH_PATHS:
            candidate = os.path.join(search_dir, mapped)
            if os.path.exists(candidate):
                return candidate

    for search_dir in _FONT_SEARCH_PATHS:
        if not os.path.isdir(search_dir):
            continue
        for fname in os.listdir(search_dir):
            if family_name.lower().replace(" ", "") in fname.lower().replace(" ", ""):
                return os.path.join(search_dir, fname)

    fallback = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return fallback if os.path.exists(fallback) else None


@functools.lru_cache(maxsize=128)
def _load_font(font_path, size_px):
    """Load a PIL ImageFont at the given pixel size."""
    return ImageFont.truetype(font_path, int(round(size_px)))


def measure_text_width(text, font_family, size_px, letter_spacing_em=0, bold=False):
    """Measure rendered text width in CSS pixels.

    Returns the total width including letter-spacing, with cross-platform
    safety margin applied.
    """
    family_key = font_family
    if bold and "Bold" not in family_key:
        family_key = family_key + " Bold"

    font_path = _find_font_file(family_key)
    if not font_path:
        font_path = _find_font_file(font_family)
    if not font_path:
        return None

    try:
        font = _load_font(font_path, size_px)
        base_width = font.getlength(text)
    except Exception:
        return None

    ls_total = letter_spacing_em * size_px * len(text)
    total = base_width + ls_total
    safety = CROSS_PLATFORM_SAFETY_LARGE if size_px >= LARGE_TEXT_THRESHOLD_PX else CROSS_PLATFORM_SAFETY_BASE
    return total * safety


def measure_region_width(region):
    """Measure the text width for a manifest region dict.

    Falls back to None if font measurement is unavailable.
    """
    text = region.get("text", "")
    if not text:
        return None

    font_family = region.get("fontFamily", "sans-serif")
    size_px = region.get("fontSizePx", 16)
    ls_em = region.get("letterSpacingEm", 0)
    bold = region.get("bold", False)

    return measure_text_width(text, font_family, size_px, ls_em, bold)


def measure_max_line_width(region):
    """Measure per-line width for multi-line text, return the widest.

    Splits text on whitespace boundaries to approximate line breaks,
    measures each word/segment individually, and returns the max.
    For single-line text, delegates to measure_region_width.
    """
    text = region.get("text", "")
    line_count = region.get("lineCount", 1)
    if not text or line_count <= 1:
        return measure_region_width(region)

    font_family = region.get("fontFamily", "sans-serif")
    size_px = region.get("fontSizePx", 16)
    ls_em = region.get("letterSpacingEm", 0)
    bold = region.get("bold", False)

    words = text.split()
    if not words:
        return None

    max_w = 0
    for word in words:
        w = measure_text_width(word, font_family, size_px, ls_em, bold)
        if w is not None and w > max_w:
            max_w = w
    return max_w if max_w > 0 else None
