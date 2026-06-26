#!/usr/bin/env python3
"""
Extract text and tables from PDF files (global market data support).
Uses pdfplumber for reliable text extraction with multi-currency and unit support.
Optional OCR via PyMuPDF + vision API for scanned/image-based PDFs.

Usage:
    python extract_pdf.py input.pdf [output.md] [options]

Modes:
    Default    Extract text + tables from all pages
    --search   Find pages containing keywords
    --metrics  Extract lines with numeric indicators
    --toc      Extract table of contents / section structure
    --diff     Compare two PDFs, show pages unique to each
    --chunk    Split output into LLM-friendly chunks
    --ocr      OCR scanned/image-based pages (auto-detects low-text pages)

Options:
    --pages            Select specific pages (e.g. 1-5,10)
    --text-only        Text only, skip tables
    --tables-only      Tables only (markdown)
    --tables-only-json Tables only as JSON
    --ocr-pages        Force OCR specific pages (e.g., 1-5,10)
    --ocr-dpi          OCR image DPI (default 200)
    --ocr-api-key      Vision API key (default: OCR_API_KEY env var)
    --ocr-model        Vision model (default: from config.json or environment)
    --clean-headers    Auto-detect & remove repeated header/footer lines
    --header-lines     Manually specify lines to remove
    --output-dir       Batch output directory
    --context          Context lines around search matches (default 5)
    --max-chars        Max chars per chunk (default 8000)
    --diff-threshold   Diff similarity threshold 0.0-1.0 (default 0.8)
    --layout           Use layout-aware extraction (better multi-column)

Examples:
    python extract_pdf.py report.pdf
    python extract_pdf.py report.pdf output.md
    python extract_pdf.py report.pdf --search "Vietnam export penetration"
    python extract_pdf.py report.pdf --metrics "market size growth export penetration"
    python extract_pdf.py report.pdf --toc
    python extract_pdf.py new.pdf old.pdf --diff
    python extract_pdf.py report.pdf --chunk
    python extract_pdf.py scanned.pdf --ocr
    python extract_pdf.py report.pdf --ocr --ocr-pages 1-5,10
    python extract_pdf.py report.pdf --clean-headers
    python extract_pdf.py file1.pdf file2.pdf --output-dir ./extracted
"""

import argparse
import sys
import re
import os
import time
import base64
from pathlib import Path
from collections import Counter

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is required. Install with: python -m pip install pdfplumber")
    sys.exit(1)

# ──────────────────────────────────────────────
# OCR: PyMuPDF + vision API (optional)
# ──────────────────────────────────────────────
HAS_OCR = False
try:
    import fitz  # PyMuPDF
    from openai import OpenAI
    HAS_OCR = True
except ImportError:
    pass


def _load_skill_config():
    """Load skill's own config.json. Returns (api_key, base_url, model) or None."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    config_path = os.path.abspath(config_path)
    try:
        if not os.path.exists(config_path):
            return None
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        api_key = cfg.get("vision_api_key", "").strip() or None
        base_url = cfg.get("vision_base_url", "").strip() or None
        model = cfg.get("vision_model", "").strip() or None
        return (api_key, base_url, model)
    except Exception:
        return None

_skill_cfg = _load_skill_config() or (None, None, None)

# Precedence: CLI arg > env var > skill config.json > hardcoded default
DEFAULT_OCR_API_KEY = os.environ.get("OCR_API_KEY", os.environ.get("OPENROUTER_API_KEY", _skill_cfg[0]))
DEFAULT_OCR_BASE_URL = os.environ.get("OCR_BASE_URL", _skill_cfg[1] or "https://openrouter.ai/api/v1")
DEFAULT_OCR_MODEL = os.environ.get("OCR_MODEL", _skill_cfg[2] or "qwen/qwen3.6-plus:free")

# Vision-capable model detection
VISION_MODEL_PREFIXES = [
    "qwen/", "stepfun/", "minimax/",
    "anthropic/claude-3",
    "openai/gpt-4o", "openai/gpt-4-turbo", "openai/gpt-4-vision",
    "google/gemini", "microsoft/phi-3",
]

def _is_vision_model(model_id: str) -> bool:
    """Check if a model ID likely supports vision (image input)."""
    model_lower = model_id.lower()
    return any(model_lower.startswith(prefix) for prefix in VISION_MODEL_PREFIXES)


# ──────────────────────────────────────────────
# Extraction helpers
# ──────────────────────────────────────────────

def extract_text_from_page(page, layout: bool = False) -> str:
    """Extract text. layout=True improves multi-column via x_tolerance."""
    text = page.extract_text(x_tolerance=25) if layout else page.extract_text()
    return text if text and text.strip() else ""


def extract_tables_from_page(page) -> list:
    return page.extract_tables() or []


def format_table(table: list) -> str:
    """Format a table as markdown."""
    if not table:
        return ""
    lines = []
    for i, row in enumerate(table):
        cells = [str(c).strip() if c is not None else "" for c in row]
        lines.append(f"| {' | '.join(cells)} |")
        if i == 0:
            lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Header / Footer detection
# ──────────────────────────────────────────────

def detect_repeated_lines(texts: list, min_pages: int = 3, max_lines: int = 10) -> set:
    """Find lines that appear at the beginning or end of most pages."""
    header_counter = Counter()
    footer_counter = Counter()

    for t in texts:
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        for l in lines[:max_lines]:
            header_counter[l] += 1
        for l in lines[-max_lines:]:
            footer_counter[l] += 1

    threshold = min(len(texts) - 1, min_pages)
    repeated = set()
    for line, count in header_counter.items():
        if count >= threshold and len(line) < 200:
            repeated.add(line)
    for line, count in footer_counter.items():
        if count >= threshold and len(line) < 200:
            repeated.add(line)

    return repeated


def clean_headers_footers(texts: list, repeated: set) -> list:
    """Remove repeated header/footer lines from all page texts."""
    if not repeated:
        return texts
    cleaned = []
    for t in texts:
        lines = t.split("\n")
        filtered = [l for l in lines if l.strip() not in repeated]
        cleaned.append("\n".join(filtered))
    return cleaned


# ──────────────────────────────────────────────
# Search mode
# ──────────────────────────────────────────────

def search_pages(pages_info: list, keywords: list, context_lines: int = 5) -> list:
    """Return pages containing any of the keywords with context."""
    results = []
    for pg_num, text in pages_info:
        if not text:
            continue
        lines = text.split("\n")
        matching_lines = []
        for i, line in enumerate(lines):
            if any(kw in line for kw in keywords):
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = "\n".join(lines[start:end])
                matching_lines.append((i + 1, context))

        if matching_lines:
            results.append((pg_num, len(lines), matching_lines))
    return results


# ──────────────────────────────────────────────
# Metrics mode
# ──────────────────────────────────────────────

NUMBER_PATTERN = re.compile(
    r"[\d,]+(?:\.\d+)?\s*(?:%"
    # Global currencies
    r"|\$|€|£|¥|₩|C\$|A\$|S\$|HK\$"
    r"|USD|EUR|GBP|JPY|KRW|CAD|AUD|SGD|HKD|CNY|RMB"
    # East Asian unit scales (e.g., 万/亿) - common in many global markets
    r"|万美元|亿美元|万元|亿元|万|亿"
    # Scales and abbreviations
    r"|million|billion|trillion|k|M|B|T"
    # Other common units
    r"|pp|ppm|輛|辆|台|部|件|吨|公斤|千克|克|升|毫升"
    r")"
)

DIGIT_PATTERN = re.compile(r"\d")


# Global number patterns: common currency units and scales worldwide
# (supports USD, EUR, CNY, JPY, KRW and others; also %, pp, and units)


def extract_metrics(texts: list, keywords: list) -> list:
    """Extract lines containing keywords near numeric values."""
    results = []
    for pg_num, text in texts:
        if not text:
            continue
        for line in text.split("\n"):
            line_stripped = line.strip()
            has_keyword = any(kw in line_stripped for kw in keywords)
            has_number = bool(NUMBER_PATTERN.search(line_stripped)) or (
                bool(DIGIT_PATTERN.search(line_stripped)) and (
                    "%" in line_stripped or "ppm" in line_stripped or "pp" in line_stripped
                )
            )
            if has_keyword and has_number:
                results.append((pg_num, line_stripped))
    return results


def roman_to_int(roman: str) -> int:
    """Convert Roman numeral (I, V, X, L, C, D, M) to integer. Returns 0 on failure."""
    roman = roman.upper()
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev = 0
    for ch in reversed(roman):
        if ch not in vals:
            return 0
        curr = vals[ch]
        if curr < prev:
            total -= curr
        else:
            total += curr
        prev = curr
    return total


# ──────────────────────────────────────────────
# TOC mode
# ──────────────────────────────────────────────

def extract_toc(pages_info: list, total_pages: int = None, min_entries_per_page: int = 3) -> list:
    """
    Extract table of contents / chapter structure from PDF with robust pattern matching.

    Args:
        pages_info: List of (page_num, text) tuples
        total_pages: Total number of pages in PDF (for validation)
        min_entries_per_page: Minimum TOC entries that must appear on a page to trust that page (default: 3)

    Returns:
        List of (title, page_number, found_on_page) tuples, sorted by page_number then title.
    """
    # Expanded pattern set for diverse TOC formats
    toc_patterns = [
        # Classic: Title ..... 123
        re.compile(r"^(.+?)\s*[.\u2026\u00B7]{2,}\s*(\d{1,3})\s*$"),
        # Title 123 (no filler)
        re.compile(r"^(.+?)\s+(\d{1,3})\s*$"),
        # Title 123-125 (page range) - capture end
        re.compile(r"^(.+?)\s+(\d{1,3})\s*[-–—]\s*(\d{1,3})\s*$"),
        # Numbered: 1.1 Title ............ 45
        re.compile(r"^(?:\d+(?:\.\d+)*\s+)?(.+?)\s*[.\u2026\u00B7]{2,}\s*(\d{1,3})\s*$"),
        # Numbered: 1.1 Title 45
        re.compile(r"^(?:\d+(?:\.\d+)*\s+)?(.+?)\s+(\d{1,3})\s*$"),
        # CJK numbering: 第一章 Introduction ........... 12
        re.compile(r"^[第章节篇款条]+\s*[一-龥]{1,10}\s+(.+?)\s*[.\u2026\u00B7]{2,}\s*(\d{1,3})\s*$"),
        # CJK-only: 标题 12 (no dots)
        re.compile(r"^[一-龥].+?\s+(\d{1,3})\s*$"),
        # Roman numerals: Appendix A ............ xii
        re.compile(r"^(.+?)\s*[.\u2026\u00B7]{2,}\s*([iIvVxXlLcCdDmM]{1,5})\s*$", re.IGNORECASE),
        # Prefix with page then title: 12 - Title or 12 Title
        re.compile(r"^(\d{1,3})\s*[-–]?\s*(.+?)\s*$"),
        # Key-value style: Title: 123
        re.compile(r"^(.+?)\s*[：:]\s*(\d{1,3})\s*$"),
    ]

    # Common TOC self-reference titles to ignore
    IGNORE_TITLES = re.compile(
        r"^(table\s+of\s+contents|目录|contents?|index|索引|list\s+of\s+figures|list\s+of\s+tables|figures|tables)\s*$",
        re.IGNORECASE
    )

    # Step 1: Loose candidate extraction from all pages
    candidates = []  # (title, page, found_pg, raw_line)

    for pg_num, text in pages_info:
        if not text:
            continue
        for line in text.split("\n"):
            stripped = line.strip()
            if not stripped or len(stripped) < 2:
                continue
            # Try all patterns
            for pat in toc_patterns:
                m = pat.match(stripped)
                if m:
                    groups = m.groups()
                    # Different patterns capture different groups
                    if len(groups) == 2:
                        title, page_str = groups
                        # For patterns where title might be empty (e.g., pure number at start), skip
                        if not title or title.strip() == "":
                            continue
                    elif len(groups) == 3:
                        # Page range format: we take the end page as reference
                        title, _, page_str = groups
                    else:
                        continue

                    # Clean title
                    title = title.strip()
                    title = re.sub(r"\s+", " ", title)

                    # Skip empty or obviously wrong titles
                    if not title or len(title) < 2 or len(title) > 200:
                        continue
                    if IGNORE_TITLES.match(title):
                        continue

                    # Convert page
                    try:
                        if isinstance(page_str, str) and re.fullmatch(r"[iIvVxXlLcCdDmM]{1,5}", page_str):
                            # Roman numeral conversion
                            page = roman_to_int(page_str.upper())
                        else:
                            page = int(page_str)
                    except (ValueError, TypeError):
                        continue

                    candidates.append((title, page, pg_num, stripped))
                    break  # Only first matching pattern

    # Step 2: Page-level grouping and validation
    page_groups = {}
    for title, page, found_pg, raw in candidates:
        page_groups.setdefault(found_pg, []).append((title, page, raw))

    # Filter pages: require at least min_entries_per_page entries to trust this page as TOC
    trusted_entries = []
    for pg_num, entries in page_groups.items():
        if len(entries) >= min_entries_per_page:
            trusted_entries.extend(entries)

    # Step 3: Global validation and deduplication
    validated = []
    seen = set()  # (title_lower, page) to deduplicate

    for title, page, found_pg in trusted_entries:
        # Validate page range if total_pages known
        if total_pages and not (1 <= page <= total_pages):
            continue

        key = (title.lower(), page)
        if key in seen:
            continue
        seen.add(key)

        validated.append((title, page, found_pg))

    # Step 4: Optional ordering by page number then title
    validated.sort(key=lambda x: (x[1], x[0]))

    return validated


# ──────────────────────────────────────────────
# Diff mode
# ──────────────────────────────────────────────

def normalize_line_for_diff(line: str) -> str:
    s = line.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def compute_text_signature(text: str) -> set:
    if not text:
        return set()
    return {normalize_line_for_diff(l) for l in text.split("\n") if l.strip()}


def diff_two_pdfs(pdf1_texts: list, pdf2_texts: list, pdf1_name: str, pdf2_name: str, threshold: float = 0.8):
    """Compare two PDFs page by page using Jaccard similarity."""
    sigs1 = [(pg, compute_text_signature(t)) for pg, t in pdf1_texts]
    sigs2 = [(pg, compute_text_signature(t)) for pg, t in pdf2_texts]

    matched_1 = set()
    matched_2 = set()
    matches = []

    for pg1, sig1 in sigs1:
        best_sim = 0
        best_pg2 = None
        for pg2, sig2 in sigs2:
            if pg2 in matched_2:
                continue
            if not sig1 or not sig2:
                continue
            intersection = len(sig1 & sig2)
            union = len(sig1 | sig2)
            sim = intersection / union if union > 0 else 0
            if sim > best_sim:
                best_sim = sim
                best_pg2 = pg2

        if best_sim >= threshold or threshold == 0:
            matched_1.add(pg1)
            matched_2.add(best_pg2)
            matches.append((pg1, best_pg2, best_sim))

    unique_1 = [(pg, t) for pg, t in pdf1_texts if pg not in matched_1]
    unique_2 = [(pg, t) for pg, t in pdf2_texts if pg not in matched_2]

    return matches, unique_1, unique_2


# ──────────────────────────────────────────────
# Chunk mode
# ──────────────────────────────────────────────

def chunk_pages(pages_info: list, tables_info: list, max_chars: int) -> list:
    """Split pages into chunks of approximately max_chars."""
    items = []
    for pg_num, text in pages_info:
        if text:
            items.append((pg_num, "text", text))

    for pg_num, tables in tables_info:
        for ti, table in enumerate(tables):
            formatted = format_table(table)
            if formatted:
                items.append((pg_num, f"table-{ti+1}", formatted))

    chunks = []
    current_chars = 0
    current_parts = []
    chunk_id = 1
    first_page = None
    last_page = None

    for pg_num, ctype, content in items:
        content_with_header = f"--- Page {pg_num} [{ctype}] ---\n{content}"
        chars = len(content_with_header)

        if chars > max_chars and not current_parts:
            chunks.append((chunk_id, first_page or pg_num, last_page or pg_num, content_with_header))
            chunk_id += 1
            current_parts = []
            current_chars = 0
            first_page = None
            last_page = None
            continue

        if current_chars + chars > max_chars and current_parts:
            chunk_text = "\n\n".join(current_parts)
            chunks.append((chunk_id - 1 if not current_parts else chunk_id, first_page, last_page, chunk_text))
            chunk_id += 1
            current_parts = []
            current_chars = 0
            first_page = None

        current_parts.append(content_with_header)
        current_chars += chars
        if first_page is None:
            first_page = pg_num
        last_page = pg_num

    if current_parts:
        chunk_text = "\n\n".join(current_parts)
        chunks.append((chunk_id if not current_parts else chunk_id, first_page, last_page, chunk_text))

    final = []
    for i, (_, fp, lp, text) in enumerate(chunks):
        final.append((i + 1, fp, lp, text))

    return final


# ──────────────────────────────────────────────
# OCR engine (qwen3.6-plus vision)
# ──────────────────────────────────────────────

def ocr_pdf_pages(pdf_path: str, page_nums: list, dpi: int = 200,
                  api_key: str = None, base_url: str = None, model: str = None) -> dict[int, str]:
    """OCR specific pages of a PDF using the configured vision model."""
    if not HAS_OCR:
        print("  Warning: OCR dependencies missing. Install: python -m pip install pymupdf openai")
        return {}

    api_key = api_key or DEFAULT_OCR_API_KEY
    base_url = base_url or DEFAULT_OCR_BASE_URL
    model = model or DEFAULT_OCR_MODEL

    # Auto-detect vision support and fallback if needed
    if not _is_vision_model(model):
        print(f"    Warning: Model '{model}' may not support vision; falling back to default vision model.")
        model = "qwen/qwen3.6-plus:free"

    if not api_key:
        print("    Error: No API key. OCR skipped. Set OCR_API_KEY or use --ocr-api-key.")
        return {}

    client = OpenAI(api_key=api_key, base_url=base_url)
    doc = fitz.open(pdf_path)
    ocr_prompt = (
        "Extract ALL visible text from this PDF page image. "
        "Preserve layout, tables, numbers exactly. Return ONLY the text."
    )

    results = {}
    for pg_num in page_nums:
        try:
            page = doc[pg_num - 1]
            zoom = dpi / 72
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img_bytes = pix.tobytes("jpeg", jpg_quality=85)
            b64 = base64.b64encode(img_bytes).decode()
            data_uri = f"data:image/jpeg;base64,{b64}"

            print(f"    Page {pg_num}... ", end="", flush=True)

            for attempt in range(1, 3):
                try:
                    resp = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": [
                            {"type": "text", "text": ocr_prompt},
                            {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
                        ]}],
                        max_tokens=2000,
                        temperature=0,
                    )
                    text = resp.choices[0].message.content.strip()
                    if text:
                        results[pg_num] = text
                        print(f"OK ({len(text)} chars)")
                    break
                except Exception as e:
                    err = str(e)
                    if attempt < 2:
                        wait = attempt * 5
                        print(f"retry in {wait}s...")
                        time.sleep(wait)
                    else:
                        print(f"failed ({err[:60]})")

        except Exception as e:
            print(f"Page {pg_num}: error ({str(e)[:60]})")

    doc.close()
    return results


def merge_ocr_with_extracted(all_text: list, pdf_path: str, ocr_pages: list = None,
                             text_threshold: int = 100, ocr_args: dict = None) -> list:
    """Auto-detect low-text pages, OCR them, merge results."""
    if ocr_args is None:
        ocr_args = {}

    if ocr_pages is None:
        needs_ocr = []
        for pg_num, text in all_text:
            if not text or len(text.strip()) < text_threshold:
                needs_ocr.append(pg_num)
    else:
        needs_ocr = ocr_pages

    if not needs_ocr:
        print("  All pages have sufficient text. No OCR needed.")
        return all_text

    print(f"  [SEARCH] OCR: {len(needs_ocr)} pages need OCR: {needs_ocr}")
    dpi = ocr_args.get("dpi", 200)
    api_key = ocr_args.get("api_key")
    base_url = ocr_args.get("base_url")
    model = ocr_args.get("model")

    ocr_results = ocr_pdf_pages(pdf_path, needs_ocr, dpi=dpi, api_key=api_key, base_url=base_url, model=model)

    merged = []
    for pg_num, text in all_text:
        if pg_num in ocr_results:
            merged.append((pg_num, ocr_results[pg_num]))
        else:
            merged.append((pg_num, text))

    ocr_count = len(ocr_results)
    print(f"  OCR complete: {ocr_count}/{len(needs_ocr)} pages")
    return merged


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def process_single_pdf(input_path: Path, args, output_base_dir: str = None):
    """Process a single PDF file."""
    try:
        with pdfplumber.open(str(input_path)) as pdf:
            total_pages = len(pdf.pages)
            print(f"[{input_path.name}] PDF loaded: {total_pages} pages")

            # Parse page ranges
            page_indices = None
            if args.pages:
                page_indices = []
                for part in args.pages.split(","):
                    part = part.strip()
                    if "-" in part:
                        start, end = part.split("-", 1)
                        page_indices.extend(range(int(start) - 1, int(end)))
                    else:
                        page_indices.append(int(part) - 1)
            else:
                page_indices = list(range(total_pages))

            # Gather all page texts first
            all_text = []
            all_tables = []

            for i in page_indices:
                if i >= total_pages:
                    continue
                page = pdf.pages[i]
                text = extract_text_from_page(page, getattr(args, "layout", False))
                tables = extract_tables_from_page(page)
                all_text.append((i + 1, text))
                if tables:
                    all_tables.append((i + 1, tables))

            # OCR integration (auto-detect low-text pages if --auto-ocr (default) or --ocr)
            do_ocr = getattr(args, "ocr", False) or getattr(args, "auto_ocr", True)
            if do_ocr:
                ocr_pages = None
                if getattr(args, "ocr_pages", None):
                    ocr_pages = []
                    for part in args.ocr_pages.split(","):
                        part = part.strip()
                        if "-" in part:
                            s, e = part.split("-", 1)
                            ocr_pages.extend(range(int(s), int(e) + 1))
                        else:
                            ocr_pages.append(int(part))

                # Check if OCR can run
                if not HAS_OCR:
                    print("  OCR not available: install pymupdf and openai")
                elif not (DEFAULT_OCR_API_KEY or getattr(args, "ocr_api_key", None)):
                    print("  OCR skipped: no API key (set OCR_API_KEY or --ocr-api-key)")
                else:
                    all_text = merge_ocr_with_extracted(
                        all_text, str(input_path), ocr_pages=ocr_pages,
                        text_threshold=getattr(args, "ocr_threshold", 100),
                        ocr_args={
                            "dpi": getattr(args, "ocr_dpi", 200),
                            "api_key": getattr(args, "ocr_api_key", None),
                            "base_url": getattr(args, "ocr_base_url", None),
                            "model": getattr(args, "ocr_model", None),
                        }
                    )
                    print()

            # ── Mode: Search ──
            if args.search:
                keywords = args.search.split()
                results = search_pages(all_text, keywords, getattr(args, "context", 5))

                if not results:
                    print(f"  No pages found matching: {', '.join(keywords)}")
                    return

                out_file = determine_output_path(input_path, args, output_base_dir, "-search.md")
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(f"# Search Results: {' '.join(keywords)}\n")
                    f.write(f"Source: {input_path.name}\n\n")

                    for pg_num, total_lines, matches in results:
                        f.write(f"## Page {pg_num} ({len(matches)} matches)\n\n")
                        for line_no, context in matches:
                            f.write(f"**Line {line_no}:**\n```text\n{context}\n```\n\n")

                print(f"  Found {sum(len(m) for _, _, m in results)} matches across {len(results)} pages")
                print(f"  {out_file}")
                return

            # ── Mode: Metrics ──
            if args.metrics:
                keywords = args.metrics.split()
                results = extract_metrics(all_text, keywords)

                if not results:
                    print(f"  No metrics found matching: {', '.join(keywords)}")
                    return

                out_file = determine_output_path(input_path, args, output_base_dir, "-metrics.md")
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(f"# Key Metrics: {' '.join(keywords)}\n")
                    f.write(f"Source: {input_path.name}\n\n")
                    seen = set()
                    for pg_num, line in results:
                        if line not in seen:
                            f.write(f"- [Page {pg_num}] {line}\n")
                            seen.add(line)

                print(f"  Found {len(results)} metric lines")
                print(f"  {out_file}")
                return

            # ── Mode: TOC ──
            if args.toc:
                entries = extract_toc(all_text, total_pages=total_pages, min_entries_per_page=args.toc_min_entries)

                out_file = determine_output_path(input_path, args, output_base_dir, "-toc.md")
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(f"# Table of Contents: {input_path.name}\n\n")
                    if entries:
                        for title, page_ref, found_at in entries:
                            f.write(f"- **{title}** Page {page_ref} (in PDF page {found_at})\n")
                    else:
                        f.write("(No clear TOC structure detected)\n")

                print(f"  Found {len(entries)} TOC entries")
                print(f"  {out_file}")
                return

            # ── Mode: Chunk ──
            if args.chunk:
                max_chars = getattr(args, "max_chars", 8000)
                chunks = chunk_pages(all_text, all_tables, max_chars)

                if not chunks:
                    print("  No content to chunk.")
                    return

                if output_base_dir:
                    os.makedirs(output_base_dir, exist_ok=True)
                    base = input_path.stem
                    chunk_files = []
                    for chunk_id, fp, lp, text in chunks:
                        fname = os.path.join(output_base_dir, f"{base}-chunk-{chunk_id:03d}-p{fp}-p{lp}.md")
                        with open(fname, "w", encoding="utf-8") as f:
                            f.write(f"# {input_path.name} Chunk {chunk_id} (Pages {fp}-{lp})\n\n")
                            f.write(text)
                        chunk_files.append(fname)
                    print(f"  Created {len(chunk_files)} chunks ({max_chars} chars each)")
                    for cf in chunk_files:
                        print(f"    {cf}")
                else:
                    out_file = determine_output_path(input_path, args, output_base_dir, "-chunks.md")
                    with open(out_file, "w", encoding="utf-8") as f:
                        f.write(f"# {input_path.name} Split into {len(chunks)} chunks\n\n")
                        for chunk_id, fp, lp, text in chunks:
                            f.write(f"---\n\n# Chunk {chunk_id} (Pages {fp}-{lp})\n\n")
                            f.write(text)
                            f.write(f"\n\n--- Chunk {chunk_id} end ({len(text)} chars)\n\n")

                    print(f"  Split into {len(chunks)} chunks ({max_chars} chars each)")
                    print(f"  {out_file}")
                return

            # ── Normal mode: Full extraction ──

            # Clean headers/footers
            clean_hdr = getattr(args, "clean_headers", False)
            if clean_hdr:
                text_only = [t for _, t in all_text if t]
                if args.header_lines:
                    repeated = set(args.header_lines)
                else:
                    repeated = detect_repeated_lines(text_only)
                all_text_clean = clean_headers_footers(all_text, repeated)
                all_text = list(zip([p for p, _ in all_text], all_text_clean))
                if repeated:
                    print(f"  Cleaned {len(repeated)} repeated header/footer line(s)")

            # Determine output
            out_file = determine_output_path(input_path, args, output_base_dir, ".md")

            with open(out_file, "w", encoding="utf-8") as f:
                text_parts = []
                for pg_num, text in all_text:
                    if text:
                        text_parts.append(f"--- Page {pg_num} ---\n{text}")

                table_parts = []
                for pg_num, tables in all_tables:
                    for ti, table in enumerate(tables):
                        table_parts.append(
                            f"--- Page {pg_num}, Table {ti+1} ---\n{format_table(table)}"
                        )

                parts = text_parts + table_parts
                if not parts:
                    f.write("# No extractable content found\n\n")
                    f.write("The PDF may consist primarily of images/scanned pages.\n")
                    f.write("Consider using --ocr flag for scanned/image-based PDFs.\n")
                else:
                    f.write("\n\n".join(parts))

            print(f"  {out_file}")
            print(f"  Text sections: {len(text_parts)}")
            print(f"  Tables: {len(table_parts)}")

    except Exception as e:
        print(f"  Error extracting [{input_path.name}]: {e}")
        import traceback
        traceback.print_exc()


def process_diff_mode(pdf_paths: list, args, output_base_dir: str = None):
    """Compare two PDF files."""
    if len(pdf_paths) != 2:
        print("Error: --diff requires exactly 2 PDF files.")
        sys.exit(1)

    all_texts = []
    labels = []
    for idx, file_path in enumerate(pdf_paths):
        p = Path(file_path)
        if not p.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)

        with pdfplumber.open(str(p)) as pdf:
            texts = []
            for i, page in enumerate(pdf.pages):
                texts.append((i + 1, extract_text_from_page(page, getattr(args, "layout", False))))
            label = p.name if len(set(p.name for p in [Path(f) for f in pdf_paths])) > 1 else f"File {idx+1}"
            all_texts.append(texts)
            labels.append(label)

    threshold = getattr(args, "diff_threshold", 0.8)
    matches, unique_1, unique_2 = diff_two_pdfs(
        all_texts[0], all_texts[1], labels[0], labels[1], threshold=threshold
    )

    out_file = determine_output_path(Path(pdf_paths[0]), args, output_base_dir, "-diff.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# PDF Comparison: {labels[0]} vs {labels[1]}\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Pages matched: {len(matches)}\n")
        f.write(f"- Pages unique to **{labels[0]}**: {len(unique_1)}\n")
        f.write(f"- Pages unique to **{labels[1]}**: {len(unique_2)}\n\n")
        f.write("## Matched Pages (content similarity 80%)\n\n")
        f.write(f"| {labels[0]} | {labels[1]} | Similarity |\n")
        f.write(f"|----------|----------|------------|\n")
        for pg1, pg2, sim in matches:
            f.write(f"| Page {pg1} | Page {pg2} | {sim:.0%} |\n")

        if unique_1:
            f.write(f"\n## Unique to {labels[0]}\n\n")
            for pg_num, text in unique_1:
                f.write(f"### Page {pg_num}\n\n```text\n{text[:1000]}\n```\n\n")

        if unique_2:
            f.write(f"\n## Unique to {labels[1]}\n\n")
            for pg_num, text in unique_2:
                f.write(f"### Page {pg_num}\n\n```text\n{text[:1000]}\n```\n\n")

    print(f"[Diff] {labels[0]} vs {labels[1]}")
    print(f"  {len(matches)} matched, {len(unique_1)} unique to {labels[0]}, {len(unique_2)} unique to {labels[1]}")
    print(f"  {out_file}")




def determine_output_path(input_path: Path, args, output_base_dir: str, suffix: str) -> str:
    """Determine output file path."""
    if output_base_dir:
        os.makedirs(output_base_dir, exist_ok=True)
        return os.path.join(output_base_dir, input_path.stem + suffix)

    if args.output and len(args.files) == 1:
        return args.output

    if suffix.startswith('-'):
        return str(input_path.parent / (input_path.stem + suffix))
    return str(input_path.with_suffix(suffix))


def main():
    parser = argparse.ArgumentParser(
        description="Extract text and tables from PDF files with global market data support"
    )
    parser.add_argument("files", nargs="+", help="PDF file(s) to process")
    parser.add_argument("output", nargs="?", default=None,
                        help="Output file path (single-file mode only)")
    parser.add_argument("--text-only", action="store_true", help="Extract text only")
    parser.add_argument("--tables-only", action="store_true", help="Extract tables only")
    parser.add_argument("--pages", default=None,
                        help="Comma-separated pages or ranges (e.g., 1,2,3-5,7)")
    parser.add_argument("--search", default=None,
                        help="Search mode: find pages containing keywords (space-separated)")
    parser.add_argument("--metrics", default=None,
                        help="Metrics mode: extract lines with keywords + numbers")
    parser.add_argument("--toc", action="store_true",
                        help="Extract table of contents / chapter structure")
    parser.add_argument("--toc-min-entries", type=int, default=3,
                        help="Minimum TOC entries per page to trust detection (default: 3)")
    parser.add_argument("--diff", action="store_true",
                        help="Diff mode: compare two PDFs")
    parser.add_argument("--chunk", action="store_true",
                        help="Chunk mode: split output into LLM-friendly chunks")
    parser.add_argument("--max-chars", type=int, default=8000,
                        help="Max chars per chunk (default: 8000)")
    parser.add_argument("--ocr", action="store_true",
                        help="Force OCR on pages (with auto-detect of low-text pages)")
    parser.add_argument("--ocr-pages", default=None,
                        help="Force OCR specific pages (e.g., 1-5,10)")
    parser.add_argument("--ocr-dpi", type=int, default=200,
                        help="OCR image DPI (default 200)")
    parser.add_argument("--ocr-api-key", default=None,
                        help="Vision API key (default: OCR_API_KEY env var)")
    parser.add_argument("--ocr-base-url", default=None,
                        help="Vision API base URL (default: from config.json or https://openrouter.ai/api/v1)")
    parser.add_argument("--ocr-model", default=None,
                        help="Vision model (default: from config.json or qwen/qwen3.6-plus:free)")
    parser.add_argument("--auto-ocr", action="store_true", default=True,
                        help=argparse.SUPPRESS)  # default enabled, hidden
    parser.add_argument("--no-auto-ocr", dest="auto_ocr", action="store_false",
                        help="Disable automatic OCR for low-text pages")
    parser.add_argument("--ocr-threshold", type=int, default=100,
                        help="Minimum text length to consider page as needing OCR (default: 100 chars)")
    parser.add_argument("--layout", action="store_true",
                        help="Layout-aware extraction (multi-column)")
    parser.add_argument("--diff-threshold", type=float, default=0.8,
                        dest="diff_threshold",
                        help="Diff similarity threshold 0.0-1.0 (default 0.8)")
    parser.add_argument("--clean-headers", action="store_true",
                        help="Auto-detect and remove repeated header/footer lines")
    parser.add_argument("--header-lines", nargs="*",
                        help="Manually specify header/footer lines to remove")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (batch mode)")
    parser.add_argument("--context", type=int, default=5,
                        help="Context lines around search matches (default 5)")
    args = parser.parse_args()

    output_base_dir = args.output_dir

    # Diff mode special handling
    if args.diff:
        process_diff_mode(args.files, args, output_base_dir)
        return

    for file_path in args.files:
        p = Path(file_path)
        if not p.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        process_single_pdf(p, args, output_base_dir)
        print()


if __name__ == "__main__":
    main()




