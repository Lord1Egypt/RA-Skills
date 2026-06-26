# KB Framework Konfiguration
# DEPRECATED: Use kb.base.config.KBConfig instead.
# This file exists ONLY as a last-resort fallback for legacy scripts
# that import via 'from config import ...'.
#
# New code should use: from kb.base.config import KBConfig
# or: from kb.framework.paths import get_default_db_path
#
# NOTE: The 4 scripts that still import from this module
# (migrate_fts5.py, migrate.py, kb_full_audit.py, fts5_setup.py)
# now prefer paths.py and only fall back to this file if paths.py
# is unavailable. Once those scripts are confirmed working,
# this file can be removed entirely.

import os
from pathlib import Path

# Resolve DB path portably (was: hardcoded "library/biblio.db")
_env = os.getenv("KB_DB_PATH")
if _env:
    DB_PATH = _env
else:
    try:
        from kb.framework.paths import get_default_base_path
        _base = os.getenv("KB_BASE_PATH", str(get_default_base_path()))
    except ImportError:
        _base = os.getenv("KB_BASE_PATH", str(Path.home() / ".openclaw" / "kb"))
    DB_PATH = str(Path(_base) / "library" / "biblio.db")

# Bibliothek
LIBRARY_PATH = str(Path(DB_PATH).parent) + "/"  # Same dir as DB

# Such-Parameter
DEFAULT_LIMIT = 20
SEMANTIC_WEIGHT = 0.6
KEYWORD_WEIGHT = 0.4

# OCR (für bildbasierte PDFs)
OCR_LANGUAGES = ["de", "en"]
OCR_GPU = False  # True wenn GPU verfügbar