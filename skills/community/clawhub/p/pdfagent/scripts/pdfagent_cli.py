#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "typer>=0.12.3",
#   "pypdf>=4.3.1",
#   "pillow>=10.4.0",
#   "img2pdf>=0.5.1",
#   "reportlab>=4.2.2",
#   "python-pptx>=1.0.2",
# ]
# ///
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pdfagent.cli import app


if __name__ == "__main__":
    app()
