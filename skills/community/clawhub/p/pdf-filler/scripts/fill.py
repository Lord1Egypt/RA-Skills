#!/usr/bin/env python3
"""Fill a PDF AcroForm with values from a JSON file.

Usage:
  python scripts/fill.py <input.pdf> <values.json> --output <out.pdf>
                         [--backend auto|pypdf|pdfrw|pymupdf|pdftk]
                         [--flatten] [--strict] [--best-effort]
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
    sys.exit(main(["fill", *sys.argv[1:]]))
