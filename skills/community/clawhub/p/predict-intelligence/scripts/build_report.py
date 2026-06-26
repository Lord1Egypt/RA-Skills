#!/usr/bin/env python3
"""
Geopolitical Predict Report Builder
Renders a Jinja2 HTML template with JSON data, exports to PDF via Playwright.
Maps (Leaflet) and entity graphs (D3) render client-side in the browser.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    sys.exit("Missing: pip install jinja2")


def html_to_pdf(html_path: str, pdf_path: str, timeout: int = 45):
    """Render HTML to PDF using Playwright Chromium."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Missing: pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 860, "height": 1200})

        abs_html = os.path.abspath(html_path)
        page.goto(f"file://{abs_html}", wait_until="networkidle", timeout=timeout * 1000)
        page.wait_for_timeout(5000)

        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Build geopolitical predict report")
    parser.add_argument("--data", required=True, help="Path to report_data.json")
    parser.add_argument("--template", required=True, help="Path to report.html template")
    parser.add_argument("--output", default="predict_report.pdf", help="Output PDF path")
    parser.add_argument("--timeout", type=int, default=45, help="PDF timeout in seconds")
    parser.add_argument("--html-only", action="store_true", help="Skip PDF, generate HTML only")
    args = parser.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    tpl_path = Path(args.template)
    env = Environment(loader=FileSystemLoader(str(tpl_path.parent)))
    template = env.get_template(tpl_path.name)

    rendered = template.render(**data)

    stem = Path(args.output).stem
    html_out = f"{stem}.html"

    with open(html_out, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"[OK] HTML: {html_out}")

    if not args.html_only:
        html_to_pdf(html_out, args.output, timeout=args.timeout)
        print(f"[OK] PDF:  {args.output}")


if __name__ == "__main__":
    main()
