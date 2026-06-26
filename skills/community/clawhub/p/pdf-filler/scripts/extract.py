#!/usr/bin/env python3
"""Extract AcroForm field schema from a PDF.

Usage:
  python scripts/extract.py <input.pdf> [--output out.json] [--include-values]
"""
from __future__ import annotations

import sys

try:
    from oc_pdf_filler.cli import main
except ImportError:
    sys.stderr.write(
        "oc-pdf-filler is not installed.\n"
        "Install it with: pip install 'oc-pdf-filler[all]'\n"
    )
    sys.exit(2)

if __name__ == "__main__":
    sys.exit(main(["extract", *sys.argv[1:]]))
