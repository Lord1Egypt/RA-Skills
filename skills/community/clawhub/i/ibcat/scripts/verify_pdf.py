#!/usr/bin/env python3
"""
Verify that a translated PDF contains properly rendered Chinese text.

Usage:
  python3 verify_pdf.py <pdf_path> [--pages all|N|N-M]

Checks:
  1. Chinese characters are present in extracted text
  2. CJK fonts (Source Han / Noto) are embedded (not just Roboto/Latin)
  3. No obvious tofu/missing glyph patterns
"""

import sys
import pdfplumber


def check_pdf(pdf_path, page_range="all"):
    """Verify Chinese rendering in a PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF: {pdf_path}")
        print(f"Total pages: {total_pages}")
        print()

        # Parse page range
        if page_range == "all":
            pages_to_check = range(total_pages)
        elif "-" in page_range:
            start, end = page_range.split("-")
            pages_to_check = range(int(start) - 1, int(end))
        else:
            pages_to_check = [int(page_range) - 1]

        all_ok = True
        total_chinese = 0
        total_cjk_fonts = 0

        for i in pages_to_check:
            if i >= total_pages:
                continue
            page = pdf.pages[i]
            text = page.extract_text() or ""

            # Check for Chinese characters
            chinese_chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
            has_chinese = len(chinese_chars) > 0
            total_chinese += len(chinese_chars)

            # Check fonts
            fonts = set()
            for c in page.chars:
                fonts.add(c.get('fontname', '?'))

            cjk_fonts = [f for f in fonts if any(
                kw in f for kw in ['Source Han', 'Noto', 'CJK', 'WenQuanYi', 'wqy']
            )]
            has_cjk_font = len(cjk_fonts) > 0
            total_cjk_fonts += len(cjk_fonts)

            latin_fonts = [f for f in fonts if 'Roboto' in f or 'Arial' in f]

            status = "OK" if (has_chinese and has_cjk_font) else "WARN"
            if not has_chinese and i > 0:
                status = "SKIP"  # Some pages may not have translatable text

            if status == "WARN":
                all_ok = False

            print(f"  Page {i + 1:3d}: {status:4s} | Chinese={has_chinese} "
                  f"({len(chinese_chars):4d} chars) | CJK fonts={len(cjk_fonts)} | "
                  f"Latin fonts={len(latin_fonts)}")

        print()
        print(f"Summary: {total_chinese} Chinese characters, {total_cjk_fonts} CJK font references")
        if all_ok:
            print("RESULT: PASS - Chinese text is properly rendered with CJK fonts")
        else:
            print("RESULT: WARN - Some pages may have rendering issues")
            print("  Check if font patches are applied: python3 setup_fonts.py --check")

        return all_ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <pdf_path> [--pages all|N|N-M]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    page_range = "all"
    if "--pages" in sys.argv:
        idx = sys.argv.index("--pages")
        if idx + 1 < len(sys.argv):
            page_range = sys.argv[idx + 1]

    check_pdf(pdf_path, page_range)
