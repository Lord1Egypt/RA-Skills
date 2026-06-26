#!/usr/bin/env python3
"""
Generate a PDF from an HTML file using headless Chrome.
Usage: python3 generate_pdf.py <html_path>
"""
import sys
import subprocess
from pathlib import Path
from urllib.parse import quote

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_pdf.py <html_path>", file=sys.stderr)
        sys.exit(1)

    html = Path(sys.argv[1]).resolve()
    if not html.exists():
        print(f"Error: file not found: {html}", file=sys.stderr)
        sys.exit(1)

    pdf = html.with_suffix(".pdf")
    url = "file://" + quote(str(html))

    subprocess.run([
        CHROME,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf}",
        "--no-pdf-header-footer",
        url,
    ], check=True, capture_output=True)

    print(f"{pdf.stat().st_size:,} bytes written to {pdf}")

if __name__ == "__main__":
    main()
