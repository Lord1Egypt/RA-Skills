"""Extract text, tables, and metadata from PDFs with auto routing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import pdfplumber

from pdf_extract.detector import (
    MIN_TEXT_CHARS,
    PageAnalysis,
    PageMode,
    analysis_to_dict,
    analyze_pdf,
)

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover - optional at import for clearer error
    fitz = None  # type: ignore[assignment]


OutputFormat = Literal["text", "json", "markdown"]


@dataclass
class PageResult:
    """Extracted content for one page."""

    page_number: int
    mode: PageMode
    text: str
    tables: list[list[list[str | None]]] = field(default_factory=list)
    analysis: PageAnalysis | None = None


@dataclass
class ExtractResult:
    """Full document extraction result."""

    path: str
    page_count: int
    metadata: dict[str, Any]
    pages: list[PageResult]
    analyses: list[PageAnalysis]

    @property
    def full_text(self) -> str:
        """Concatenate all page texts with page markers."""
        parts: list[str] = []
        for page in self.pages:
            header = f"--- Page {page.page_number} [{page.mode.value}] ---"
            body = page.text.strip()
            parts.append(f"{header}\n{body}" if body else header)
        return "\n\n".join(parts).strip() + ("\n" if self.pages else "")


def parse_page_range(spec: str | None, total_pages: int) -> list[int] | None:
    """Parse a page range string such as ``1,3-5,8``.

    Parameters
    ----------
    spec : str or None
        Page selection. ``None`` or empty means all pages.
    total_pages : int
        Document page count for bounds checking.

    Returns
    -------
    list[int] or None
        1-based page numbers, or ``None`` for all pages.

    Raises
    ------
    ValueError
        If the specification is invalid or out of range.
    """
    if not spec or not spec.strip():
        return None

    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if start > end:
                raise ValueError(f"Invalid range: {part}")
            for n in range(start, end + 1):
                pages.add(n)
        else:
            pages.add(int(part))

    ordered = sorted(pages)
    for n in ordered:
        if n < 1 or n > total_pages:
            raise ValueError(f"Page {n} out of range (1-{total_pages})")
    return ordered


def _extract_native_text(page: pdfplumber.page.Page, *, layout: bool) -> str:
    """Extract text from a page with pdfplumber."""
    if layout:
        text = page.extract_text(layout=True) or ""
    else:
        text = page.extract_text() or ""
    return text.strip()


def _extract_tables(
    page: pdfplumber.page.Page,
) -> list[list[list[str | None]]]:
    """Extract tables from a page with pdfplumber."""
    raw_tables = page.extract_tables() or []
    cleaned: list[list[list[str | None]]] = []
    for table in raw_tables:
        if not table:
            continue
        rows: list[list[str | None]] = []
        for row in table:
            if row is None:
                continue
            rows.append(
                [cell.strip() if isinstance(cell, str) else cell for cell in row]
            )
        if rows:
            cleaned.append(rows)
    return cleaned


def _extract_ocr_text(
    pdf_path: Path,
    page_index: int,
    *,
    language: str,
    dpi: int,
) -> str:
    """OCR a single page via PyMuPDF + Tesseract.

    Parameters
    ----------
    pdf_path : Path
        Path to the PDF file.
    page_index : int
        0-based page index.
    language : str
        Tesseract language codes, e.g. ``eng`` or ``eng+chi_tra``.
    dpi : int
        Render resolution for OCR.

    Returns
    -------
    str
        Recognized text.

    Raises
    ------
    RuntimeError
        If PyMuPDF is missing or OCR fails.
    """
    if fitz is None:
        raise RuntimeError(
            "PyMuPDF (pymupdf) is required for OCR. Install with: pip install pymupdf"
        )

    doc = fitz.open(pdf_path)
    try:
        page = doc[page_index]
        # full=True OCRs the whole page image (needed for scanned PDFs).
        textpage = page.get_textpage_ocr(
            flags=0,
            language=language,
            dpi=dpi,
            full=True,
            tessdata=None,
        )
        text = page.get_text("text", textpage=textpage) or ""
        return text.strip()
    except Exception as exc:  # noqa: BLE001 - surface OCR backend errors clearly
        raise RuntimeError(
            f"OCR failed on page {page_index + 1}: {exc}. "
            "Ensure tesseract is installed and language data is available "
            f"(requested: {language})."
        ) from exc
    finally:
        doc.close()


def extract_pdf(
    pdf_path: str | Path,
    *,
    pages: str | None = None,
    mode: Literal["auto", "text", "ocr"] = "auto",
    include_tables: bool = False,
    layout: bool = False,
    ocr_lang: str = "eng",
    ocr_dpi: int = 200,
    min_text_chars: int = MIN_TEXT_CHARS,
) -> ExtractResult:
    """Extract content from a PDF, auto-choosing text vs OCR per page.

    Parameters
    ----------
    pdf_path : str or Path
        Path to the PDF file.
    pages : str or None, optional
        Page range like ``1-3,5``. Default all pages.
    mode : {'auto', 'text', 'ocr'}, optional
        Extraction mode. ``auto`` classifies each page.
    include_tables : bool, optional
        Also extract tables (native text pages only).
    layout : bool, optional
        Preserve layout for native text extraction.
    ocr_lang : str, optional
        Tesseract language(s), e.g. ``eng`` or ``eng+chi_tra``.
    ocr_dpi : int, optional
        OCR render DPI.
    min_text_chars : int, optional
        Auto-mode text threshold.

    Returns
    -------
    ExtractResult
        Structured extraction result.
    """
    path = Path(pdf_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF file: {path}")

    force_mode: PageMode | None
    if mode == "text":
        force_mode = PageMode.TEXT
    elif mode == "ocr":
        force_mode = PageMode.OCR
    else:
        force_mode = None

    with pdfplumber.open(path) as pdf:
        page_count = len(pdf.pages)
        page_numbers = parse_page_range(pages, page_count)
        analyses = analyze_pdf(
            pdf,
            page_numbers=page_numbers,
            min_text_chars=min_text_chars,
            force_mode=force_mode,
        )
        metadata = dict(pdf.metadata or {})

        # Normalize metadata values to JSON-friendly strings.
        clean_meta: dict[str, Any] = {}
        for key, value in metadata.items():
            if value is None:
                continue
            clean_meta[str(key)] = value if isinstance(value, (str, int, float, bool)) else str(value)

        results: list[PageResult] = []
        for analysis in analyses:
            idx = analysis.page_number - 1
            page = pdf.pages[idx]
            tables: list[list[list[str | None]]] = []

            if analysis.mode is PageMode.TEXT:
                text = _extract_native_text(page, layout=layout)
                if include_tables:
                    tables = _extract_tables(page)
            else:
                text = _extract_ocr_text(
                    path,
                    idx,
                    language=ocr_lang,
                    dpi=ocr_dpi,
                )
                # Tables from pure image pages are unreliable without layout models.

            results.append(
                PageResult(
                    page_number=analysis.page_number,
                    mode=analysis.mode,
                    text=text,
                    tables=tables,
                    analysis=analysis,
                )
            )

    return ExtractResult(
        path=str(path),
        page_count=page_count,
        metadata=clean_meta,
        pages=results,
        analyses=analyses,
    )


def result_to_dict(result: ExtractResult, *, include_analysis: bool = True) -> dict[str, Any]:
    """Convert ExtractResult to a JSON-serializable dict."""
    payload: dict[str, Any] = {
        "path": result.path,
        "page_count": result.page_count,
        "metadata": result.metadata,
        "pages": [],
    }
    if include_analysis:
        payload["analyses"] = [analysis_to_dict(a) for a in result.analyses]

    for page in result.pages:
        entry: dict[str, Any] = {
            "page": page.page_number,
            "mode": page.mode.value,
            "text": page.text,
        }
        if page.tables:
            entry["tables"] = page.tables
        payload["pages"].append(entry)
    return payload


def result_to_markdown(result: ExtractResult, *, include_meta: bool = False) -> str:
    """Render ExtractResult as Markdown."""
    lines: list[str] = [f"# {Path(result.path).name}", ""]

    if include_meta and result.metadata:
        lines.append("## Metadata")
        lines.append("")
        for key, value in result.metadata.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")

    lines.append("## Pages")
    lines.append("")
    for page in result.pages:
        lines.append(f"### Page {page.page_number} (`{page.mode.value}`)")
        lines.append("")
        body = page.text.strip() if page.text else "_(empty)_"
        lines.append(body)
        lines.append("")
        if page.tables:
            for t_idx, table in enumerate(page.tables, start=1):
                lines.append(f"#### Table {t_idx}")
                lines.append("")
                lines.extend(_table_to_markdown(table))
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _table_to_markdown(table: list[list[str | None]]) -> list[str]:
    """Convert a 2D table to GitHub-flavored Markdown."""
    if not table:
        return ["_(empty table)_"]

    def cell(value: str | None) -> str:
        text = "" if value is None else str(value)
        return text.replace("|", "\\|").replace("\n", " ").strip()

    width = max(len(row) for row in table)
    normalized = [list(row) + [None] * (width - len(row)) for row in table]
    header = normalized[0]
    body = normalized[1:] if len(normalized) > 1 else []

    # If first row looks empty, treat all rows as body with generic headers.
    if all(not cell(c) for c in header) and body:
        header = [f"col{i + 1}" for i in range(width)]
        body = normalized

    lines = [
        "| " + " | ".join(cell(c) for c in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(cell(c) for c in row) + " |")
    return lines


def result_to_plain(
    result: ExtractResult,
    *,
    page_markers: bool = True,
    include_tables: bool = False,
) -> str:
    """Render ExtractResult as plain text."""
    if not page_markers and not include_tables:
        chunks = [p.text for p in result.pages if p.text]
        return "\n\n".join(chunks).strip() + ("\n" if chunks else "")

    parts: list[str] = []
    for page in result.pages:
        if page_markers:
            parts.append(f"--- Page {page.page_number} [{page.mode.value}] ---")
        if page.text:
            parts.append(page.text)
        if include_tables and page.tables:
            for t_idx, table in enumerate(page.tables, start=1):
                parts.append(f"[Table {t_idx}]")
                for row in table:
                    cells = ["" if c is None else str(c) for c in row]
                    parts.append("\t".join(cells))
        parts.append("")
    text = "\n".join(parts).rstrip()
    return text + ("\n" if text else "")


def sanitize_filename(name: str) -> str:
    """Make a string safe for use as a filename stem."""
    cleaned = re.sub(r"[^\w.\-]+", "_", name, flags=re.UNICODE)
    return cleaned.strip("._") or "output"
