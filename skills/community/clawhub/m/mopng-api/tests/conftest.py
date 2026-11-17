"""Shared test setup: make the scripts helpers importable.

``scripts/mopng_api.py`` and ``scripts/mopng_agent.py`` are run as files
(``python3 scripts/mopng_*.py``), so they import their sibling helper
``_http`` as a plain top-level module. Adding ``scripts`` to ``sys.path`` here
keeps that contract under pytest and lets tests patch the third-party modules
(``urllib``) exactly as those helpers loaded them.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))