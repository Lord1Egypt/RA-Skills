#!/usr/bin/env python3
"""
generate-pdf.py
A simple script to generate a perfectly formatted PDF from HTML using Playwright.
Requires: pip install playwright && playwright install chromium
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DOCUMENTS_DIR = (REPO_ROOT / "documents").resolve()


def _is_within_directory(candidate_path: Path, base_dir: Path) -> bool:
    try:
        candidate_path.relative_to(base_dir)
        return True
    except ValueError:
        return False


def _validate_paths(input_html_path: str, output_pdf_path: str) -> tuple[Path, Path]:
    if not DOCUMENTS_DIR.exists() or not DOCUMENTS_DIR.is_dir():
        print(f"Error: Expected documents directory at {DOCUMENTS_DIR}")
        sys.exit(1)

    input_path = Path(input_html_path).expanduser().resolve()
    output_path = Path(output_pdf_path).expanduser().resolve()

    if input_path.suffix.lower() != ".html":
        print("Error: Input must be an .html file.")
        sys.exit(1)

    if output_path.suffix.lower() != ".pdf":
        print("Error: Output must be a .pdf file.")
        sys.exit(1)

    if not _is_within_directory(input_path, DOCUMENTS_DIR):
        print(f"Error: Input must be inside {DOCUMENTS_DIR}")
        sys.exit(1)

    if not _is_within_directory(output_path, DOCUMENTS_DIR):
        print(f"Error: Output must be inside {DOCUMENTS_DIR}")
        sys.exit(1)

    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist.")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    return input_path, output_path


def generate_pdf(input_html_path, output_pdf_path):
    input_path, output_path = _validate_paths(input_html_path, output_pdf_path)

    # Convert absolute paths to file:// protocol for Playwright
    html_file_url = input_path.resolve().as_uri()

    print(f"Generating PDF: {output_path}...")
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # SECURITY: Disable JavaScript and block non-local requests to avoid network exfiltration.
        context = browser.new_context(java_script_enabled=False)

        def _block_non_local_requests(route):
            url = route.request.url
            if url.startswith(("file://", "about:", "data:")):
                route.continue_()
            else:
                route.abort()

        context.route("**/*", _block_non_local_requests)
        page = context.new_page()
        page.goto(html_file_url, wait_until="load")
        page.pdf(
            path=str(output_path),
            format="Letter",
            margin={"top": "1in", "bottom": "1in", "left": "1in", "right": "1in"},
            print_background=True,
        )
        context.close()
        browser.close()
    print(f"Success! PDF saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-pdf.py <input.html> <output.pdf>")
        sys.exit(1)
    
    generate_pdf(sys.argv[1], sys.argv[2])
