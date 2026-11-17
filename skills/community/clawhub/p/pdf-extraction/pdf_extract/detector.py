"""Decide whether a PDF page should use native text or OCR extraction."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pdfplumber


class PageMode(str, Enum):
    """Extraction strategy for a single page."""

    TEXT = "text"
    OCR = "ocr"


# Pages with fewer than this many non-whitespace characters are treated as
# thin on text. Combined with image presence this triggers OCR.
MIN_TEXT_CHARS = 40

# If average characters per page area unit is below this, prefer OCR even when
# some characters exist (common for scanned pages with noisy OCR-like glyphs).
MIN_TEXT_DENSITY = 0.0008


@dataclass(frozen=True)
class PageAnalysis:
    """Per-page classification result."""

    page_number: int
    mode: PageMode
    char_count: int
    image_count: int
    width: float
    height: float
    reason: str


def _count_images(page: pdfplumber.page.Page) -> int:
    """Return number of embedded images on a page."""
    images = getattr(page, "images", None) or []
    return len(images)


def analyze_page(
    page: pdfplumber.page.Page,
    page_number: int,
    *,
    min_text_chars: int = MIN_TEXT_CHARS,
    force_mode: PageMode | None = None,
) -> PageAnalysis:
    """Classify a page as native-text or OCR.

    Parameters
    ----------
    page : pdfplumber.page.Page
        Opened page object.
    page_number : int
        1-based page number for reporting.
    min_text_chars : int, optional
        Character threshold below which OCR is preferred.
    force_mode : PageMode or None, optional
        Skip heuristics and force this mode.

    Returns
    -------
    PageAnalysis
        Classification details for the page.
    """
    width = float(page.width or 0)
    height = float(page.height or 0)
    text = page.extract_text() or ""
    char_count = len("".join(text.split()))
    image_count = _count_images(page)
    area = max(width * height, 1.0)
    density = char_count / area

    if force_mode is not None:
        return PageAnalysis(
            page_number=page_number,
            mode=force_mode,
            char_count=char_count,
            image_count=image_count,
            width=width,
            height=height,
            reason=f"forced:{force_mode.value}",
        )

    # Plenty of extractable text → native path.
    if char_count >= min_text_chars and density >= MIN_TEXT_DENSITY:
        return PageAnalysis(
            page_number=page_number,
            mode=PageMode.TEXT,
            char_count=char_count,
            image_count=image_count,
            width=width,
            height=height,
            reason="sufficient_native_text",
        )

    # Little or no text, but images (or empty scan) → OCR.
    if char_count < min_text_chars:
        reason = "sparse_text_with_images" if image_count > 0 else "sparse_text"
        return PageAnalysis(
            page_number=page_number,
            mode=PageMode.OCR,
            char_count=char_count,
            image_count=image_count,
            width=width,
            height=height,
            reason=reason,
        )

    # Some text but very low density (often image-heavy with captions).
    if density < MIN_TEXT_DENSITY and image_count > 0:
        return PageAnalysis(
            page_number=page_number,
            mode=PageMode.OCR,
            char_count=char_count,
            image_count=image_count,
            width=width,
            height=height,
            reason="low_density_with_images",
        )

    return PageAnalysis(
        page_number=page_number,
        mode=PageMode.TEXT,
        char_count=char_count,
        image_count=image_count,
        width=width,
        height=height,
        reason="default_native_text",
    )


def analyze_pdf(
    pdf: pdfplumber.PDF,
    *,
    page_numbers: list[int] | None = None,
    min_text_chars: int = MIN_TEXT_CHARS,
    force_mode: PageMode | None = None,
) -> list[PageAnalysis]:
    """Classify selected pages of an open PDF.

    Parameters
    ----------
    pdf : pdfplumber.PDF
        Opened pdfplumber document.
    page_numbers : list[int] or None, optional
        1-based page numbers. ``None`` means all pages.
    min_text_chars : int, optional
        Character threshold for OCR preference.
    force_mode : PageMode or None, optional
        Force every page to this mode.

    Returns
    -------
    list[PageAnalysis]
        One analysis entry per selected page.
    """
    total = len(pdf.pages)
    if page_numbers is None:
        indices = list(range(total))
    else:
        indices = []
        for n in page_numbers:
            if n < 1 or n > total:
                raise ValueError(f"Page {n} out of range (1-{total})")
            indices.append(n - 1)

    results: list[PageAnalysis] = []
    for idx in indices:
        page = pdf.pages[idx]
        results.append(
            analyze_page(
                page,
                page_number=idx + 1,
                min_text_chars=min_text_chars,
                force_mode=force_mode,
            )
        )
    return results


def analysis_to_dict(item: PageAnalysis) -> dict[str, Any]:
    """Serialize a PageAnalysis for JSON output."""
    return {
        "page": item.page_number,
        "mode": item.mode.value,
        "char_count": item.char_count,
        "image_count": item.image_count,
        "width": item.width,
        "height": item.height,
        "reason": item.reason,
    }
