#!/usr/bin/env python3
"""Entry point for the bundled kalo CLI — run directly, no install needed.

    python3 scripts/kalo.py product rank --region US
"""

import os
import sys

if sys.version_info < (3, 11):
    running = "%d.%d.%d" % sys.version_info[:3]
    script = os.path.abspath(__file__)
    print("error: kalo needs Python 3.11+ (this interpreter is %s)" % running)
    print("help[3]:")
    print("  Try a newer interpreter: python3.11 %s ..." % script)
    print("  Or without installing anything: uv run --python 3.11 --no-project python %s ..." % script)
    print("  macOS ships Python 3.9 as `python3`; `brew install python@3.12` also fixes this")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kalodata.cli import main  # noqa: E402

sys.exit(main())
