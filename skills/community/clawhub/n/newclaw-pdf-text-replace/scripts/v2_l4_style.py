"""
v2_l4_style.py - L4 Style overlay for pdf_text_replace v2.0
Uses pymupdf (fitz) to apply color, font-size, underline, bold overlays.
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple
import logging

log = logging.getLogger(__name__)


@dataclass
class StyleOptions:
    color: Optional[Tuple[float, float, float]] = None   # RGB 0-1
    font_size: Optional[int] = None
    underline: bool = False
    bold: Optional[bool] = None


def apply_style_overlay(
    pdf_path: str,
    target_text: str,
    opts: StyleOptions,
    page_num: int = 0,
) -> bool:
    """
    Apply style changes (color, size, underline, bold) to all occurrences of
    target_text on the given page using a pymupdf redaction overlay.

    Returns True on success.
    """
    try:
        import fitz  # pymupdf
    except ImportError:
        log.error("[L4] pymupdf not installed. Run: pip install pymupdf")
        return False

    try:
        doc = fitz.open(pdf_path)
        page = doc[page_num]

        instances = page.search_for(target_text)
        if not instances:
            log.warning("[L4] '%s' not found visually on page %d", target_text, page_num)
            doc.close()
            return False

        color = opts.color if opts.color else (0, 0, 0)

        for rect in instances:
            # Determine current font size at location if not overriding
            font_size = opts.font_size
            if font_size is None:
                blocks = page.get_text("dict", clip=rect)["blocks"]
                for blk in blocks:
                    for ln in blk.get("lines", []):
                        for sp in ln.get("spans", []):
                            if target_text in sp.get("text", ""):
                                font_size = sp["size"]
                                break
                if font_size is None:
                    font_size = 12

            # Redact the original text (white out)
            page.add_redact_annot(rect, fill=(1, 1, 1))
            page.apply_redactions()

            # Insert new text with style
            fontname = "helv"
            if opts.bold:
                fontname = "hebo"

            page.insert_text(
                (rect.x0, rect.y1),
                target_text,
                fontname=fontname,
                fontsize=font_size,
                color=color,
            )

            if opts.underline:
                ul_y = rect.y1 + 1
                page.draw_line(
                    fitz.Point(rect.x0, ul_y),
                    fitz.Point(rect.x1, ul_y),
                    color=color,
                    width=0.5,
                )

        doc.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        doc.close()
        log.info("[L4] Style overlay applied: color=%s bold=%s underline=%s size=%s",
                 opts.color, opts.bold, opts.underline, opts.font_size)
        return True

    except Exception as e:
        log.error("[L4] Style overlay failed: %s", e)
        return False
