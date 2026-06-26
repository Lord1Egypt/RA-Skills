#!/usr/bin/env python3
"""Show which fill backends are available in this environment."""
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
    sys.exit(main(["list-backends"]))
