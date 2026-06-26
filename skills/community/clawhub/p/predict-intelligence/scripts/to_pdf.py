#!/usr/bin/env python3
"""
Minimal HTML → PDF converter using Playwright Chromium.

Usage:
    python to_pdf.py report.html                    # → report.pdf
    python to_pdf.py report.html predict.pdf       # → predict.pdf
    python to_pdf.py report.html out.pdf --timeout 60
"""

import argparse
import os
import sys


def convert(html_path: str, pdf_path: str, timeout: int = 45):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Missing dependency: pip install playwright && playwright install chromium")

    abs_html = os.path.abspath(html_path)
    if not os.path.isfile(abs_html):
        sys.exit(f"File not found: {html_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 860, "height": 1200})
        page.goto(f"file://{abs_html}", wait_until="networkidle", timeout=timeout * 1000)
        page.wait_for_timeout(5000)
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()
    print(f"[OK] {pdf_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert HTML to PDF via Playwright")
    parser.add_argument("html", help="Input HTML file")
    parser.add_argument("pdf", nargs="?", default=None, help="Output PDF file (default: same name .pdf)")
    parser.add_argument("--timeout", type=int, default=45, help="Page load timeout in seconds")
    args = parser.parse_args()

    pdf_path = args.pdf or args.html.rsplit(".", 1)[0] + ".pdf"
    convert(args.html, pdf_path, args.timeout)


if __name__ == "__main__":
    main()
