#!/usr/bin/env python3
"""
Academic PDF → Clean Markdown + Extracted Figures.

Handles:
  - Double-column reading-order (left column ↓ then right column ↓ per page)
  - Mixed-layout first pages (single-col title/abstract → double-col body)
  - Header/footer/page-number removal (position + fingerprint based)
  - Drop-cap & decorative element filtering
  - Sentence merging across page breaks (hyphenated words, mid-sentence cuts)
  - Figure region rendering (vector + raster) → PNG with text markers
  - Reference/bibliography section pruning
  - Paragraph reconstruction (merge PDF line-breaks, keep real paragraph breaks)

Usage:
    python3 pdf_to_clean_md.py <input.pdf> <output_dir> [--slug SLUG] [--no-figures] [--figure-dpi 200]
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

try:  # PyMuPDF >= 1.24 ships the `pymupdf` module; `fitz` is a deprecated alias
    import pymupdf as fitz
except ImportError:  # older PyMuPDF builds
    import fitz  # PyMuPDF

# Semantic version of the parser. Stamped into the first line of every output
# (`<!-- pdfparse v2.0.0 -->`) so a stale .md produced by an older parser can be
# spotted at a glance (the 7 Sep 2026 double-column reading-order fix is the
# reason this exists). Bump it whenever parser behaviour changes.
__version__ = "2.0.0"

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------

HEADER_PCT = 0.08         # top N% of page → potential header zone
FOOTER_PCT = 0.06         # bottom N% of page → potential footer zone
SPAN_WIDTH_MIN = 0.65     # block wider than this fraction of page → spanning

# Section headings that mark the start of reference list (case-insensitive)
REF_PATTERNS = [
    r"^references?\s*$",
    r"^bibliography\s*$",
    r"^literature\s+cited\s*$",
    r"^kaynak[çc]a\s*$",
    r"^kaynaklar\s*$",
]
REF_PATTERN_COMBINED = re.compile("|".join(f"({p})" for p in REF_PATTERNS), re.I)

# Figure/table caption patterns
FIG_CAPTION_RE = re.compile(
    r"^(?:Fig\.?|Figure|Extended\s+Data\s+(?:Fig\.?|Figure))\s+\S+",
    re.IGNORECASE,
)
TABLE_CAPTION_RE = re.compile(r"^Table\s+\S+", re.IGNORECASE)

# Page boundary marker emitted per page by _render_page
PAGE_MARKER_RE = re.compile(r"^<!-- page \d+ -->$")

# Font-size thresholds (points)
DROP_CAP_MIN_SIZE = 22.0   # anything above this with ≤3 chars → decorative
TINY_FONT = 6.0            # superscripts, reference markers
SMALL_FONT = 8.5           # footnotes, table footers, journal metadata


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _block_text(block: dict) -> str:
    """Concatenate all span text from a text block, preserving internal line-breaks."""
    parts: list[str] = []
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            parts.append(span["text"])
        parts.append("\n")
    return "".join(parts).rstrip("\n")


def _block_fonts(block: dict) -> set[float]:
    """Unique font sizes (rounded to 1 decimal) used in a block."""
    return {round(s["size"], 1) for l in block.get("lines", []) for s in l.get("spans", [])}


def _is_figure_caption(block: dict) -> bool:
    return bool(FIG_CAPTION_RE.match(_block_text(block).strip()))


def _is_table_caption(block: dict) -> bool:
    return bool(TABLE_CAPTION_RE.match(_block_text(block).strip()))


def _fig_number(text: str) -> int | None:
    """Return the integer figure number from a main-figure caption.

    Handles 'Fig. 1', 'Fig. 1 ...', 'Figure 2 ...', 'Fig. 1A ...'. Returns
    None for supplementary/extended-data/other captions so they are not
    mistaken for a numbered main figure.
    """
    m = re.match(r"^(?:Fig\.?|Figure)\s*([0-9]+)", text.strip(), re.IGNORECASE)
    if not m:
        return None
    return int(m.group(1))


def _text_blocks(blocks: list[dict]) -> list[dict]:
    return [b for b in blocks if b["type"] == 0]


def _img_blocks(blocks: list[dict]) -> list[dict]:
    return [b for b in blocks if b["type"] == 1]


# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------

def slugify(title: str, max_len: int = 60) -> str:
    """Turn a paper title into a stable, filesystem-safe slug.

    Deterministic per title: the same paper always yields the same slug no
    matter what the PDF file is named, so output filenames and figure names
    stay stable when files get renamed.
    """
    s = unicodedata.normalize("NFKD", title)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).lower().strip("-")
    if len(s) <= max_len:
        return s
    cut = s[:max_len].rstrip("-")
    if "-" in cut:
        cut = cut[: cut.rfind("-")].rstrip("-")
    return cut or s[:max_len]


def _looks_like_title_line(line: str) -> bool:
    """Heuristic filter for spotting the paper title on the first page."""
    line = line.strip()
    if len(line) < 30:
        return False
    if re.search(r"https?://|doi\s*:?\s*10\.|ISSN|©|\(?20\d\d\)?|^\s*vol\.?", line, re.I):
        return False
    if re.fullmatch(r"[\d\s.,;:()\[\]-]+", line):
        return False
    return True


def _first_page_title(doc) -> str | None:
    """Best-effort title from the first page's largest-font text block.

    A paper title is almost always set in a font clearly larger than the body
    (e.g. 26pt vs 10pt in Nature-family journals). Finding the block with the
    largest font on page 1 is far more robust than scanning lines with a
    length heuristic, which can drop the first line of a multi-line title
    (e.g. "HMG-CoA reductase inhibition" is only 27 chars, under a naive
    minimum-length filter) and produce a truncated slug.
    """
    try:
        blocks = doc[0].get_text("dict")["blocks"]
    except Exception:
        return None
    best: tuple[float, str] | None = None
    for b in blocks:
        if b["type"] != 0:
            continue
        text = _block_text(b).strip()
        if not text:
            continue
        fonts = _block_fonts(b)
        if not fonts:
            continue
        max_f = max(fonts)
        if max_f < 12.0:  # body text is usually 9-10pt; titles are bigger
            continue
        if best is None or max_f > best[0]:
            best = (max_f, text)
    return best[1] if best else None


def derive_slug(doc, fallback_stem: str) -> str:
    """Slug for this PDF, preferring the real paper title over the filename.

    Resolution order:
      1. PDF metadata title (unless it merely echoes the filename)
      2. first-page title heuristic (handles missing/empty metadata)
      3. filename stem (the old behaviour, as a last resort)
    """
    meta = re.sub(r"\s+", " ", ((doc.metadata or {}).get("title") or "")).strip()
    if meta:
        s = slugify(meta)
        if s and s != slugify(fallback_stem) and s not in ("untitled", "unknown"):
            return s
    hint = _first_page_title(doc)
    if hint:
        s = slugify(hint)
        if s:
            return s
    return slugify(fallback_stem)


# ---------------------------------------------------------------------------
# Main processor
# ---------------------------------------------------------------------------

class AcademicPDFCleaner:
    """Convert an academic PDF into clean markdown + extracted figure images."""

    def __init__(
        self,
        pdf_path: str,
        output_dir: str,
        slug: str | None = None,
        render_figures: bool = True,
        figure_dpi: int = 200,
        keep_embedded: bool = False,
        keep_references: bool = False,
        page_markers: bool = False,
        json_output: bool = False,
        quiet: bool = False,
    ):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.output_dir = Path(output_dir)
        self.slug = slug or derive_slug(self.doc, Path(pdf_path).stem)
        self.render_figures = render_figures
        self.figure_dpi = figure_dpi
        self.keep_embedded = keep_embedded
        self.keep_references = keep_references
        self.page_markers = page_markers
        self.json_output = json_output
        self.quiet = quiet

        self._fig_counter = 0
        self._figures: list[dict] = []
        self._footer_fingerprints: dict[str, int] = defaultdict(int)
        # Crosscheck accounting: real figure numbers seen in captions vs extracted
        self._caption_fig_numbers: set[int] = set()
        self._extracted_fig_numbers: set[int] = set()
        self._skipped_embedded: list[tuple[int, list[float]]] = []
        # image↔caption pairing across the whole document (see _build_image_caption_map)
        self._image_caption_map: dict[tuple, int] = {}
        self._unmatched_caption_blocks: list[tuple[int, dict]] = []  # (page, block)
        # split-caption continuations: (page, left_bbox) -> right_part_text
        self._caption_right_parts: dict[tuple, str] = {}

    # ==================================================================
    # Public API
    # ==================================================================

    def process(self) -> str:
        # Pass 1: build footer fingerprint database
        for page in self.doc:
            self._fingerprint_footers(page)

        # Pass 2: build document-level image↔caption pairing (handles figures
        # whose image and caption straddle a page boundary)
        if self.render_figures:
            self._build_image_caption_map()

        # Pass 3: extract each page
        page_texts: list[str] = []
        for pn, page in enumerate(self.doc):
            blocks = page.get_text("dict")["blocks"]
            layout = self._analyze_page(page, blocks)
            text, figs = self._render_page(page, pn, blocks, layout)
            page_texts.append(text)
            self._figures.extend(figs)

        fulltext = "\n\n".join(page_texts)
        fulltext = self._merge_page_breaks(fulltext, keep_markers=self.page_markers)
        if not self.keep_references:
            fulltext = self._strip_references(fulltext)
        fulltext = self._reconstruct_paragraphs(fulltext)
        fulltext = self._final_polish(fulltext)
        fulltext = f"<!-- pdfparse v{__version__} -->\n\n{fulltext}"

        self._write(fulltext)
        if self.json_output:
            self._emit_json(fulltext)
        elif not self.quiet:
            self._emit_metadata()
        return fulltext

    # ==================================================================
    # Footer fingerprinting
    # ==================================================================

    def _fingerprint_footers(self, page: fitz.Page) -> None:
        """Record recurring text at the bottom of pages for later filtering."""
        tblocks = _text_blocks(page.get_text("dict")["blocks"])
        if not tblocks:
            return
        h = page.rect.height
        footer_y = h * (1.0 - FOOTER_PCT)
        # Bottom-most 3 blocks
        bottom = sorted(tblocks, key=lambda b: -b["bbox"][3])[:3]
        for b in bottom:
            if b["bbox"][3] < footer_y:
                continue  # not in footer zone (block bottom above the zone)
            text = _block_text(b).strip()
            if 0 < len(text) < 250:
                norm = re.sub(r"\d+", "#", text)
                self._footer_fingerprints[norm] += 1

    def _is_footer(self, block: dict, page_h: float) -> bool:
        """Check whether a block is a recurring footer element."""
        bbox = block["bbox"]
        if bbox[3] < page_h * (1.0 - FOOTER_PCT):
            return False
        # Small-font bottom block
        fonts = _block_fonts(block)
        if fonts and max(fonts) < SMALL_FONT:
            return True
        # Fingerprint match (≥3 occurrences across document)
        text = _block_text(block).strip()
        norm = re.sub(r"\d+", "#", text)
        return self._footer_fingerprints.get(norm, 0) >= 3

    # ==================================================================
    # Page layout analysis
    # ==================================================================

    def _analyze_page(self, page: fitz.Page, blocks: list[dict]) -> dict:
        """Classify every block on the page: header / footer / spanning / col-L / col-R."""
        rect = page.rect
        w, h = rect.width, rect.height
        header_y = h * HEADER_PCT
        footer_y = h * (1.0 - FOOTER_PCT)

        tblocks = _text_blocks(blocks)
        iblocks = _img_blocks(blocks)

        # --- classify text blocks ---
        headers: list[dict] = []
        footers: list[dict] = []
        spanning: list[dict] = []
        columnar: list[dict] = []
        figures: list[dict] = []   # caption blocks — we keep them but mark as figure anchors
        tables: list[dict] = []    # table-caption blocks

        for b in tblocks:
            bbox = b["bbox"]
            bw = bbox[2] - bbox[0]
            y0, y1 = bbox[1], bbox[3]
            text = _block_text(b).strip()

            # --- header zone ---
            if y1 < header_y:
                headers.append(b)
                continue

            # --- footer zone ---
            if self._is_footer(b, h):
                footers.append(b)
                continue

            # --- figure / table captions ---
            if _is_figure_caption(b) or _is_table_caption(b):
                if _is_figure_caption(b):
                    figures.append(b)
                else:
                    tables.append(b)
                # Still include in body flow — just tagged
                columnar.append(b)
                continue

            # --- spanning (full-width) blocks ---
            if bw > w * SPAN_WIDTH_MIN:
                spanning.append(b)
                continue

            # --- columnar body text ---
            columnar.append(b)

        # --- detect column boundary from columnar blocks ---
        col_boundary = self._detect_columns(columnar, w)

        # --- fixup: blocks in left column that appear BEFORE the first
        #     right-column block are really single-column elements (authors,
        #     section headings in the intro area). Reclassify as spanning. ---
        # IMPORTANT: only promote when the left block clearly ends ABOVE the
        # start of the first right block (e.g. title/author lines). Two-column
        # body text often starts at the same y in both columns — promoting a
        # left-column paragraph there would wrongly reclassify it as a
        # full-width block and break the reading order on that page.
        if col_boundary is not None:
            right_blocks = [b for b in columnar if b["bbox"][0] >= col_boundary]
            first_right_y = (
                min(b["bbox"][1] for b in right_blocks) if right_blocks else float("inf")
            )
            promoted = []
            still_columnar = []
            for b in columnar:
                if (
                    b["bbox"][0] < col_boundary
                    and b["bbox"][3] < first_right_y - 15  # clearly above → single-col element
                ):
                    spanning.append(b)
                    promoted.append(b)
                else:
                    still_columnar.append(b)
            columnar = still_columnar
            # Re-detect columns after promotion
            if promoted:
                col_boundary = self._detect_columns(columnar, w)

        # --- handle image blocks ---
        for b in iblocks:
            bw = b["bbox"][2] - b["bbox"][0]
            if bw > w * SPAN_WIDTH_MIN:
                spanning.append(b)
            else:
                columnar.append(b)

        return {
            "w": w,
            "h": h,
            "header_y": header_y,
            "footer_y": footer_y,
            "col_boundary": col_boundary,
            "is_single": col_boundary is None,
            "headers": headers,
            "footers": footers,
            "spanning": spanning,
            "columnar": columnar,
            "figure_captions": figures,
            "table_captions": tables,
        }

    def _detect_columns(self, blocks: list[dict], page_w: float) -> float | None:
        """Return x-coordinate of column gutter, or None if single-column."""
        tblocks = [b for b in blocks if b["type"] == 0]
        if len(tblocks) < 3:
            return None

        x_centers = [(b["bbox"][0] + b["bbox"][2]) / 2 for b in tblocks]
        x_centers.sort()
        mid = page_w / 2

        lefts = [x for x in x_centers if x < mid]
        rights = [x for x in x_centers if x > mid]
        if not lefts or not rights:
            return None

        l_med = lefts[len(lefts) // 2]
        r_med = rights[len(rights) // 2]
        gap = r_med - l_med

        return (l_med + r_med) / 2 if gap > page_w * 0.12 else None

    # ==================================================================
    # Per-page rendering
    # ==================================================================

    def _render_page(
        self,
        page: fitz.Page,
        pn: int,
        blocks: list[dict],
        layout: dict,
    ) -> tuple[str, list[dict]]:
        """Produce markdown text + extracted figures for one page."""
        figures: list[dict] = []
        parts: list[str] = []

        # --- build ordered body block list ---
        spanning = sorted(layout["spanning"], key=lambda b: b["bbox"][1])
        columnar = layout["columnar"]

        if layout["is_single"]:
            columnar = sorted(columnar, key=lambda b: (b["bbox"][1], b["bbox"][0]))
            ordered = self._interleave(spanning, columnar)
        else:
            col = layout["col_boundary"]
            left = sorted(
                [b for b in columnar if b["bbox"][0] < col], key=lambda b: b["bbox"][1]
            )
            right = sorted(
                [b for b in columnar if b["bbox"][0] >= col], key=lambda b: b["bbox"][1]
            )
            ordered = self._interleave_double(spanning, left, right)

        # --- process each block ---
        # Blocks that are the right-hand continuation of a split caption are
        # emitted together with their left caption part; skip them here so they
        # are not printed twice. meta["bbox"] = (page, right_bbox_tuple).
        skip_blocks: set[tuple] = set()
        skip_page = pn + 1
        for meta in self._caption_right_parts.values():
            if meta["bbox"][0] == skip_page:
                skip_blocks.add(meta["bbox"][1])

        prev_y1 = layout["header_y"]
        for block in ordered:
            bbox = block["bbox"]

            # Skip right-half continuation of a split caption (printed after
            # its left part in the caption branch).
            if (
                block["type"] == 0
                and tuple(round(v, 1) for v in bbox) in skip_blocks
            ):
                continue

            if block["type"] == 1:
                # Look up the figure number pre-computed for this image block
                # (document-level pairing in _build_image_caption_map).
                key = (pn + 1, tuple(round(v, 1) for v in bbox))
                fig_num = self._image_caption_map.get(key)
                if fig_num is not None:
                    fig = self._extract_embedded_image(page, pn, block, fig_num=fig_num)
                    if fig:
                        figures.append(fig)
                        parts.append(
                            f"\n![{fig['label']}](figures/{fig['filename']})\n"
                        )
                else:
                    # Unmatched image → logo/badge → skip (or keep if requested)
                    if self.keep_embedded:
                        fig = self._extract_embedded_image(page, pn, block)
                        if fig:
                            figures.append(fig)
                            parts.append(
                                f"\n![{fig['label']}](figures/{fig['filename']})\n"
                            )
                    else:
                        self._skipped_embedded.append((pn + 1, list(bbox)))
                continue

            text = _block_text(block)
            if not text.strip():
                continue

            # --- drop-cap / decorative filter ---
            if self._is_decorative(block, text, pn):
                continue

            # --- figure caption → emit text (figure rendered via the image block) ---
            if _is_figure_caption(block):
                n = _fig_number(text)
                if n is not None:
                    self._caption_fig_numbers.add(n)
                parts.append(text)
                # Springer-style split captions: the caption's right-hand
                # continuation block should follow immediately, not leak into
                # the body text as if it were a new paragraph.
                right_part = self._caption_right_parts.get(
                    (pn + 1, tuple(round(v, 1) for v in bbox))
                )
                if right_part is not None:
                    parts.append(right_part["text"])

            elif _is_table_caption(block):
                # Tables: keep as text for now but mark them
                parts.append(f"\n**{text}**\n")
            else:
                parts.append(text)

            prev_y1 = bbox[3]

        page_md = f"<!-- page {pn + 1} -->\n\n" + "\n\n".join(
            p for p in parts if p.strip()
        )
        return page_md, figures

    # --- block ordering ---

    @staticmethod
    def _interleave(spanning: list[dict], col: list[dict]) -> list[dict]:
        """Interleave spanning blocks into a single column by y-position."""
        result: list[dict] = []
        si = 0
        for c in col:
            cy = c["bbox"][1]
            while si < len(spanning) and spanning[si]["bbox"][1] < cy:
                result.append(spanning[si])
                si += 1
            result.append(c)
        result.extend(spanning[si:])
        return result

    @staticmethod
    def _interleave_double(
        spanning: list[dict], left: list[dict], right: list[dict]
    ) -> list[dict]:
        """Two-column reading order with full-width figure regions respected.

        Strategy (matches how a human reads a two-column page):
          1. If there is a full-width (spanning) block whose y is BELOW some
             two-column body text, the body text above it must come FIRST.
             So: emit all body text (left column, then right column) for
             blocks ABOVE the first spanning block; then the spanning
             (figure) block; then the remaining body text below it.
          2. Otherwise (no early spanning block), emit the full left column,
             then the full right column — which keeps a paragraph that starts
             in the left column and continues in the right column in one flow.
             NEVER merge left/right row by row: a paragraph running from the
             bottom-left onto the top-right would get split.
        """
        if not spanning:
            return list(left) + list(right)

        first_span_y = min(s["bbox"][1] for s in spanning)
        # Any body text above the first spanning block?
        above_left = [b for b in left if b["bbox"][1] < first_span_y]
        above_right = [b for b in right if b["bbox"][1] < first_span_y]
        below_left = [b for b in left if b["bbox"][1] >= first_span_y]
        below_right = [b for b in right if b["bbox"][1] >= first_span_y]

        # Spanning blocks must always be emitted. They sit at the top of the
        # page (figure at the top, body text below) OR after the body text
        # above them (figure below a header/summary). Order the three groups by
        # their y position: body-above → spanning → body-below.
        if above_left or above_right:
            # Body text above a full-width figure: read left → right first,
            # then the figure, then the text below it.
            return (
                list(above_left)
                + list(above_right)
                + list(spanning)
                + list(below_left)
                + list(below_right)
            )

        # No body text above the spanning block → spanning comes first,
        # then the left column, then the right column.
        return list(spanning) + list(left) + list(right)

    # --- filters ---

    @staticmethod
    def _is_decorative(block: dict, text: str, pn: int) -> bool:
        """Drop caps, large decorative initial letters."""
        fonts = _block_fonts(block)
        if not fonts:
            return False
        max_f = max(fonts)
        stripped = text.strip()
        # Very large font + 1-3 chars + no sentence content → decorative
        if max_f > DROP_CAP_MIN_SIZE and len(stripped) <= 3:
            # But allow short section headings (e.g. "Results", "Methods")
            if re.match(r"^[A-Z][a-z]+$", stripped):
                return False
            return True
        return False

    # ==================================================================
    # Figure extraction
    # ==================================================================

    def _build_image_caption_map(self) -> None:
        """Pair every embedded image block with its real 'Fig. N' caption.

        Runs once across the whole document before per-page extraction so that
        figures whose image and caption straddle a page boundary (image at the
        bottom of page N, caption at the top of page N+1) still get matched.

        Matching heuristic: each figure caption (in document reading order)
        grabs the nearest previously-unmatched image block that lies directly
        above it — same page and horizontally overlapping, or the previous page
        for a caption near the top of a page. An image that no caption claims
        is treated as a journal logo/badge and skipped.
        """
        # Collect all figure captions and image blocks in reading order.
        # A Springer-style two-column caption is split into TWO text blocks:
        # the left one starts with "Fig. N ...", the right one continues it at
        # the same vertical band. We pair both parts so the caption is emitted
        # as one unit instead of the right half leaking into the body text.
        c_keys: list[tuple[int, int, float, dict]] = []  # (page_idx, order, top, block)
        i_keys: list[tuple[int, int, float, dict]] = []  # (page_idx, order, top, block)
        caption_parts: dict[int, tuple[int, dict]] = {}  # cap_idx -> (page, right_part_block)
        for pn, page in enumerate(self.doc):
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                if b["type"] == 1:
                    i_keys.append((pn, b["bbox"][1], 0.0, b))
                    continue
                if _is_figure_caption(b):
                    n = _fig_number(_block_text(b))
                    if n is not None:
                        c_keys.append((pn, b["bbox"][1], float(n), b))
        # Second pass: match the right-hand continuation of each split caption.
        # A split caption has its left block start with "Fig. N ..." and a
        # right block continue THE SAME CLAUSE at the same y band. The decisive
        # test is visible continuity: the left part ends with a connector
        # (",", ";", "-") or the right part opens with "(" — e.g.
        #   "...of young" + "(9–12-week-old)..."       (accept)
        #   "...A and C, and" + "quantitative analyses"  (accept)
        #   "...observed;" + "the confidence score"      (accept)
        #   "...young mice" + "lack of hemodynamic..."   (REJECT — caption done)
        # New headings/body text that merely sit at the same height are rejected.
        for cap_idx, (pn, _, _, b) in enumerate(c_keys):
            cb = b["bbox"]
            page = self.doc[pn]
            left_text = _block_text(b).strip()
            left_end = left_text.rstrip()[-1] if left_text else ""
            for other in page.get_text("dict")["blocks"]:
                if other["type"] != 0:
                    continue
                otext = _block_text(other).strip()
                if not otext or _is_figure_caption(other):
                    continue
                ob = other["bbox"]
                # Must be on the right half of the page.
                if ob[0] < page.rect.width / 2:
                    continue
                # Vertical overlap with the caption's band.
                if max(ob[1], cb[1]) > min(ob[3], cb[3]) + 10:
                    continue
                # Continuity test: left ends with a connector punctuation or a
                # dangling connector word ("and", "or", "of", "the", "with",
                # "in", "to"), or the right opens with "(" (parenthetical
                # continuation). Otherwise it's a new sentence/paragraph and
                # NOT part of this caption.
                if left_end in ",;:-" or otext.startswith("("):
                    caption_parts[cap_idx] = (pn, other)
                    break
                last_word = left_text.rsplit(" ", 1)[-1].rstrip().lower()
                if last_word in ("and", "or", "but", "of", "the", "with", "in", "to", "by", "for", "as", "a", "an", "that", "which", "was", "were", "is", "are", "for"):
                    caption_parts[cap_idx] = (pn, other)
                    break

        used_images: set[int] = set()
        used_captions: set[int] = set()

        def nearest_image_for(cap_idx: int) -> int | None:
            page = c_keys[cap_idx][0]
            cy0 = c_keys[cap_idx][1]
            best: tuple[float, int] | None = None
            for i in range(len(i_keys)):
                if i in used_images:
                    continue
                ipage = i_keys[i][0]
                ix0, iy0, ix1, iy1 = i_keys[i][3]["bbox"]
                # Candidate must be above the caption in reading order.
                if ipage > page:
                    continue
                if ipage == page:
                    if iy1 > cy0 + 6:
                        continue  # image starts below the caption → not its figure
                    gap = cy0 - iy1
                else:
                    # caption near the top of its page can pair with an image on
                    # the previous page (figure+legend straddles the boundary)
                    if cy0 > 160:
                        continue
                    gap = 500 + (cy0 - iy1)
                # horizontal overlap (same column width)
                if i_keys[i][3]["bbox"][2] < ix0 - 12 or i_keys[i][3]["bbox"][0] > ix1 + 12:
                    continue
                gap = max(gap, 0.0)
                if gap > 500:
                    continue
                if best is None or gap < best[0]:
                    best = (gap, i)
            return best[1] if best is not None else None

        # Release captions in reading order, each pairing to the nearest image.
        for cap_idx in range(len(c_keys)):
            img_idx = nearest_image_for(cap_idx)
            if img_idx is None:
                self._unmatched_caption_blocks.append(
                    (c_keys[cap_idx][0], c_keys[cap_idx][3])
                )
                continue
            used_images.add(img_idx)
            used_captions.add(cap_idx)
            num = int(c_keys[cap_idx][2])
            ipage = i_keys[img_idx][0]
            ibbox = i_keys[img_idx][3]["bbox"]
            key = (ipage + 1, tuple(round(v, 1) for v in ibbox))
            self._image_caption_map[key] = num

        # Record captions that found no image (for crosscheck reporting).
        self._caption_fig_numbers |= {
            int(c_keys[c][2]) for c in range(len(c_keys)) if c in used_captions
        }

        # Save the split-caption continuations for _render_page to emit
        # right after the caption's left part. Key = (page, left bbox),
        # value = {"bbox": (page, right bbox), "text": right part text}.
        for cap_idx, (pn, right_block) in caption_parts.items():
            left_bbox = c_keys[cap_idx][3]["bbox"]
            right_text = _block_text(right_block).strip()
            if right_text:
                key = (pn + 1, tuple(round(v, 1) for v in left_bbox))
                right_key = (pn + 1, tuple(round(v, 1) for v in right_block["bbox"]))
                self._caption_right_parts[key] = {"bbox": right_key, "text": right_text}

    def _extract_embedded_image(
        self, page: fitz.Page, pn: int, block: dict, fig_num: int | None = None
    ) -> dict | None:
        """Render an embedded raster image block."""
        bbox = block["bbox"]
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if w < 25 or h < 25:
            return None
        return self._save_figure_pix(
            page.get_pixmap(dpi=self.figure_dpi, clip=fitz.Rect(*bbox)),
            pn,
            list(bbox),
            "embedded",
            fig_num=fig_num,
        )

    def _render_figure_above(
        self,
        page: fitz.Page,
        pn: int,
        caption_block: dict,
        layout: dict,
        prev_y1: float,
    ) -> dict | None:
        """Render the figure region above a caption as a PNG."""
        cb = caption_block["bbox"]
        caption_top = cb[1]

        # Figure region: between previous content bottom and caption top
        fig_top = max(prev_y1 + 3, layout["header_y"] + 3)
        fig_bottom = caption_top - 3
        fig_left = cb[0]
        fig_right = cb[2]

        # Expand horizontally to capture full figure if it spans wider
        if layout.get("col_boundary") and (fig_right - fig_left) < 100:
            fig_left -= 40
            fig_right += 40

        fig_rect = fitz.Rect(fig_left, fig_top, fig_right, fig_bottom)
        if fig_rect.height < 30 or fig_rect.width < 40:
            return None

        # Deduplicate: skip if overlapping a previously extracted figure on this page
        for prev in self._figures:
            if prev.get("page") != pn + 1:
                continue
            pb = prev.get("bbox", [])
            if len(pb) == 4:
                ox = max(0, min(fig_rect.x1, pb[2]) - max(fig_rect.x0, pb[0]))
                oy = max(0, min(fig_rect.y1, pb[3]) - max(fig_rect.y0, pb[1]))
                overlap = ox * oy
                if overlap > 0 and overlap / (fig_rect.width * fig_rect.height) > 0.4:
                    return None

        try:
            pix = page.get_pixmap(dpi=self.figure_dpi, clip=fig_rect)
        except Exception:
            return None

        return self._save_figure_pix(
            pix,
            pn,
            [fig_rect.x0, fig_rect.y0, fig_rect.x1, fig_rect.y1],
            "rendered",
            fig_num=_fig_number(_block_text(caption_block)),
        )

    def _save_figure_pix(self, pix, pn: int, bbox: list[float], source: str, fig_num: int | None = None) -> dict:
        """Save a pixmap as PNG and return metadata.

        When fig_num is given (figure derived from a 'Fig. N' caption), label
        the figure with that real number so it matches the paper — e.g.
        'fig_3' is genuinely the article's Figure 3. Otherwise fall back to a
        running counter (used for uncaptioned embedded images).
        """
        if fig_num is not None:
            label = f"fig_{fig_num}"
            self._extracted_fig_numbers.add(fig_num)
        else:
            self._fig_counter += 1
            label = f"fig_{self._fig_counter}"
        filename = f"{self.slug}_{label}.png"
        fig_dir = self.output_dir / "figures"
        fig_dir.mkdir(parents=True, exist_ok=True)
        pix.save(str(fig_dir / filename))
        return {
            "label": label,
            "filename": filename,
            "page": pn + 1,
            "bbox": bbox,
            "source": source,
            "fig_num": fig_num,
        }

    # ==================================================================
    # Post-processing
    # ==================================================================

    def _merge_page_breaks(self, text: str, keep_markers: bool = False) -> str:
        """Heal sentences split across page boundaries.

        Page markers are emitted per page upstream and are dropped here by
        default (clean reading text). With keep_markers=True they are put back
        between the pages, so downstream readers can cite a page number.

        A marker is *not* restored at a boundary that was healed: the joining
        happens inside a word or a sentence, and re-inserting the marker there
        would split it again.
        """
        tokens = re.split(r"(<!-- page \d+ -->)\n*", text)
        chunks = tokens[0::2]
        markers = tokens[1::2]
        if len(chunks) <= 1:
            return text

        merged = [chunks[0]]
        before = [""]  # marker that would precede merged[i] (i > 0)
        for i in range(1, len(chunks)):
            marker = markers[i - 1] if i - 1 < len(markers) else ""
            prev = merged[-1].rstrip()
            cur = chunks[i].strip()
            if not prev or not cur:
                merged.append(chunks[i])
                before.append(marker)
                continue

            prev_last = prev.split("\n")[-1].strip()
            cur_first = cur.split("\n")[0].strip()

            # Hyphenated word across pages
            if prev_last.endswith("-") and cur_first:
                merged[-1] = prev[: -len(prev_last)] + prev_last[:-1] + cur_first
                merged.append(cur[len(cur_first):])
                before.append("")
            # Mid-sentence break: previous doesn't end with .!?
            elif (
                prev_last
                and not re.search(r"[.!?]\s*$", prev_last)
                and cur_first
                and not cur_first[0].isdigit()
            ):
                merged[-1] = prev + " " + cur
                before.append("")
            else:
                merged.append(chunks[i])
                before.append(marker)

        out: list[str] = []
        for i, chunk in enumerate(merged):
            if not chunk.strip():
                continue
            if keep_markers and i < len(before) and before[i]:
                out.append(before[i])
            out.append(chunk.strip())
        return "\n\n".join(out)

    def _strip_references(self, text: str) -> str:
        """Remove the reference/bibliography section from the end of the paper.

        Uses multi-strategy detection:
          1. Line-by-line scan for "References" / "Bibliography" / "Kaynakça" heading
             followed by reference-like entries.
          2. Full-text regex for reference-heading patterns.
          3. Fallback: "Received: … Accepted: … Published:" block (Nature style).
          4. Last resort: scan backward for dense numbered-line clusters.
        """
        lines = text.split("\n")

        # ---- Strategy 1: line-by-line heading scan ----
        for i, line in enumerate(lines):
            s = line.strip()
            if not REF_PATTERN_COMBINED.match(s):
                continue
            if len(s) > 35:
                continue
            # Context check: previous line blank, ends with period, or near top of page.
            # Page markers are transparent: a marker between the body text and the
            # "References" heading must not defeat the check.
            j = i - 1
            prev = ""
            while j >= 0:
                cand = lines[j].strip()
                if not cand:
                    break
                if PAGE_MARKER_RE.match(cand):
                    j -= 1
                    continue
                prev = cand
                break
            prev_ok = i == 0 or not prev or re.search(r"[.!?]\s*$", prev)
            # Also accept if previous non-blank line contains "Online content"
            prev_ok = prev_ok or (i > 0 and "online content" in prev.lower())
            if not prev_ok and i >= 5:
                continue

            # Verify: next few non-blank lines look like reference entries
            score = 0
            for j in range(i + 1, min(i + 12, len(lines))):
                rl = lines[j].strip()
                if not rl:
                    continue
                if re.match(r"^\d+\.\s", rl):         # numbered ref
                    score += 2
                elif re.match(r"^[A-Z][a-zÀ-ÿ]+,\s+[A-Z]\.", rl):  # Author, X.
                    score += 2
                elif re.search(r"\b(?:doi|PMID|https?://)", rl, re.I):
                    score += 1
                elif re.search(r"\(\d{4}\)", rl):       # year in parens
                    score += 1
            if score >= 3:
                return "\n".join(lines[:i]).rstrip()

        # ---- Strategy 2: full-text regex ----
        # Nature/Springer: "Online content" block then references
        ref_section = re.search(
            r"\n(Online\s+content\b.*?)(?=\n\d+\.\s|\nReferences?\s*\n)",
            text, re.I | re.DOTALL
        )
        if ref_section:
            # Find where references start after this block
            after = text[ref_section.start():]
            ref_start = re.search(r"\n\d+\.\s", after)
            if ref_start:
                cut = ref_section.start() + ref_start.start()
                return text[:cut].rstrip()

        # ---- Strategy 3: "Received: … Accepted: … Published:" ----
        for i, line in enumerate(lines):
            if re.match(r"^Received:\s", line.strip()):
                # Check if there are reference-like entries nearby (before or after)
                for j in range(max(0, i - 10), min(i + 10, len(lines))):
                    if re.match(r"^\d+\.\s", lines[j].strip()):
                        return "\n".join(lines[:i]).rstrip()
                # Also: cut at "Received:" if there's reference content after
                for j in range(i + 1, min(i + 15, len(lines))):
                    rl = lines[j].strip()
                    if re.match(r"^\d+\.\s", rl) or re.match(r"^[A-Z][a-z]+,\s+[A-Z]\.", rl):
                        return "\n".join(lines[:i]).rstrip()
                break

        # ---- Strategy 4: backward scan for dense numbered clusters ----
        # Find the last cluster of ≥5 consecutive numbered lines (reference section tail)
        cluster_start = -1
        consecutive = 0
        for i in range(len(lines) - 1, -1, -1):
            rl = lines[i].strip()
            if re.match(r"^\d+\.\s", rl):
                consecutive += 1
            elif rl == "" or PAGE_MARKER_RE.match(rl):
                continue  # blank lines and page markers don't break the cluster
            else:
                if consecutive >= 5:
                    cluster_start = i + 1
                    break
                consecutive = 0
        if consecutive >= 5:  # cluster reaches the beginning
            cluster_start = 0
        if cluster_start > 0:
            # Walk back to find the section heading
            for i in range(cluster_start - 1, max(0, cluster_start - 30), -1):
                s = lines[i].strip()
                if REF_PATTERN_COMBINED.match(s) or re.match(
                    r"^(?:Online\s+content|Supplementary|Acknowledgments?)", s, re.I
                ):
                    return "\n".join(lines[:i]).rstrip()
            # No heading found, just cut at cluster
            return "\n".join(lines[:cluster_start]).rstrip()

        return text

    def _reconstruct_paragraphs(self, text: str) -> str:
        """Convert PDF line-breaks into flowing paragraphs.

        Strategy:
          - Double (or more) newlines → paragraph boundary (preserved)
          - Single newline between lines of the same paragraph → join with space
          - Single newline where previous line ends with sentence punctuation
            AND next line starts with capital → likely a new paragraph that
            PDF didn't separate with blank line → keep as paragraph break
        """
        paragraphs = re.split(r"\n\s*\n", text)
        rebuilt: list[str] = []

        for para in paragraphs:
            lines = [l.strip() for l in para.split("\n") if l.strip()]
            if not lines:
                rebuilt.append("")
                continue

            # Image markers should stay on their own lines
            img_lines: set[int] = set()
            for li, line in enumerate(lines):
                if re.match(r"^!\[.*\]\(.*\)$", line):
                    img_lines.add(li)

            merged: list[str] = []
            buf = lines[0]
            for li in range(1, len(lines)):
                curr = lines[li]
                prev = lines[li - 1]

                # Keep image markers isolated
                if li in img_lines:
                    merged.append(buf)
                    buf = curr
                    continue

                # Previous is an image marker OR current is an image marker → break
                if (li - 1) in img_lines:
                    merged.append(buf)
                    buf = curr
                    continue

                # Previous ends with sentence-ending punctuation → paragraph break
                if re.search(r"[.!?]\s*$", prev):
                    # And current starts with capital letter → new paragraph
                    if curr and curr[0].isupper():
                        merged.append(buf)
                        buf = curr
                        continue
                    # Also break if current starts with a section-like heading
                    if re.match(r"^(?:Results|Methods|Discussion|Introduction|Abstract|Conclusion)", curr):
                        merged.append(buf)
                        buf = curr
                        continue

                # Previous ends with hyphen → word continuation (de-hyphenate)
                if prev.endswith("-"):
                    buf = buf[:-1] + curr
                else:
                    buf = buf + " " + curr

            merged.append(buf)

            # Within each merged chunk, collapse multiple spaces
            rebuilt.append("\n\n".join(merged))

        return "\n\n".join(p for p in rebuilt if p.strip())

    def _final_polish(self, text: str) -> str:
        """Remove artifacts and normalize whitespace (image markers kept intact)."""
        # Protect image markers: whitespace normalization below would otherwise
        # glue a marker into its neighbouring paragraph (e.g. "...and both
        # ![fig_1](...)" or "<!-- page 6 -->![fig_2](...)"). Hold them aside and
        # restore after polishing, each on its own line.
        markers: list[str] = []
        def stash(m: re.Match) -> str:
            markers.append(m.group(0))
            return f"\n@@IMG{len(markers) - 1}@@\n"
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)", stash, text)

        # Remove empty page markers
        text = re.sub(r"<!-- page \d+ -->\s*(?=<!-- page \d+ -->)", "", text)
        # Collapse >3 consecutive newlines
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        # Fix multiple spaces
        text = re.sub(r"  +", " ", text)
        # Fix space before punctuation
        text = re.sub(r"\s+([.,;:!?)])", r"\1", text)

        # Restore image markers on their own lines
        for i, m in enumerate(markers):
            text = text.replace(f"@@IMG{i}@@", f"{m}")
        return text.strip()

    # ==================================================================
    # Output
    # ==================================================================

    def _write(self, text: str) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        md_path = self.output_dir / "fulltext.md"
        md_path.write_text(text, encoding="utf-8")
        if not self.quiet and not self.json_output:
            print(f"FULLTEXT: {md_path}")

    def _emit_metadata(self) -> None:
        meta = self.doc.metadata or {}
        print(f"TITLE: {(meta.get('title') or '').strip()}")
        print(f"AUTHOR: {(meta.get('author') or '').strip()}")
        print(f"PAGES: {self.doc.page_count}")
        print(f"FIGURES: {len(self._figures)}")
        print(f"OUTPUT_DIR: {self.output_dir}")
        print(f"SLUG: {self.slug}")
        print(f"REFERENCES: {'kept' if self.keep_references else 'stripped'}")
        self._emit_figure_crosscheck()

    def _emit_figure_crosscheck(self) -> None:
        """Report whether extracted figure numbers match the paper's captions.

        Lets the user trust that 'fig_3' is genuinely the article's Figure 3,
        and flags gaps (e.g. a caption that produced no image) or leftover
        uncaptioned graphics that were deliberately skipped.
        """
        caps = sorted(self._caption_fig_numbers)
        extr = sorted(self._extracted_fig_numbers)
        print(f"FIG_CAPTIONS: {caps}" if caps else "FIG_CAPTIONS: none")
        print(f"FIG_EXTRACTED: {extr}" if extr else "FIG_EXTRACTED: none")
        missing = sorted(set(caps) - set(extr))
        if missing:
            print(f"FIG_MISSING: {missing}")
        else:
            print("FIG_MISSING: none")
        if self._skipped_embedded:
            pages = sorted({p for p, _ in self._skipped_embedded})
            print(
                f"EMBEDDED_SKIPPED: {len(self._skipped_embedded)} uncaptioned "
                f"image(s) on page(s) {pages} (journallogo/badge — skipped)"
            )
        else:
            print("EMBEDDED_SKIPPED: none")

    def _emit_json(self, text: str) -> None:
        """Emit one machine-readable summary on stdout.

        Intended for programmatic callers (e.g. paper-vault) so they parse a
        stable structure instead of the human-readable TITLE:/FIG_… block.
        """
        meta = self.doc.metadata or {}
        caps = sorted(self._caption_fig_numbers)
        extr = sorted(self._extracted_fig_numbers)
        print(json.dumps({
            "status": "ok",
            "version": __version__,
            "pdf": str(Path(self.pdf_path).resolve()),
            "slug": self.slug,
            "title": (meta.get("title") or "").strip(),
            "authors": (meta.get("author") or "").strip(),
            "pages": self.doc.page_count,
            "figures": len(self._figures),
            "output_dir": str(self.output_dir.resolve()),
            "output_path": str((self.output_dir / "fulltext.md").resolve()),
            "references": "kept" if self.keep_references else "stripped",
            "page_markers": self.page_markers,
            "text_chars": len(text),
            "fig_captions": caps,
            "fig_extracted": extr,
            "fig_missing": sorted(set(caps) - set(extr)),
            "embedded_skipped": len(self._skipped_embedded),
        }, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description="Academic PDF → clean markdown + figures")
    p.add_argument("pdf", help="Input PDF path")
    p.add_argument("output_dir", help="Output directory")
    p.add_argument("--slug", help="Paper slug (default: derived from the paper title)")
    p.add_argument("--no-figures", action="store_true", help="Skip figure extraction")
    p.add_argument("--figure-dpi", type=int, default=200, help="Figure render DPI")
    p.add_argument(
        "--keep-embedded",
        action="store_true",
        help="Also extract uncaptioned embedded images (logos/badges). Off by "
        "default so figure numbers stay aligned with the paper's real Figure N.",
    )
    p.add_argument(
        "--keep-references",
        action="store_true",
        help="Keep the reference/bibliography section instead of pruning it. "
        "Use when you need the bibliography itself (citation extraction, "
        "reference tracing) rather than clean reading text.",
    )
    p.add_argument(
        "--page-markers",
        action="store_true",
        help="Keep <!-- page N --> markers between pages so the output can be "
        "cited by page number. Markers are omitted at boundaries healed across "
        "pages, where they would split the joined word.",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Print one JSON summary on stdout instead of the human-readable "
        "metadata block. Errors are reported as JSON as well.",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file metadata (FULLTEXT/TITLE/AUTHOR/…/figure crosscheck).",
    )
    args = p.parse_args()

    if not os.path.exists(args.pdf):
        msg = f"PDF not found: {args.pdf}"
        if args.json:
            print(json.dumps({"status": "error", "error": msg, "pdf": args.pdf},
                             ensure_ascii=False))
        else:
            print(f"ERROR: {msg}", file=sys.stderr)
        sys.exit(1)

    AcademicPDFCleaner(
        args.pdf,
        args.output_dir,
        slug=args.slug,
        render_figures=not args.no_figures,
        figure_dpi=args.figure_dpi,
        keep_embedded=args.keep_embedded,
        keep_references=args.keep_references,
        page_markers=args.page_markers,
        json_output=args.json,
        quiet=args.quiet,
    ).process()


if __name__ == "__main__":
    main()
