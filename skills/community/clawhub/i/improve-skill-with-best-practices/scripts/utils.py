"""Shared utilities for all skill scripts.

Centralizes:
- Data directory discovery (.skills-data/google-analytics-and-search-improve/)
- .env loading
- Google Service Account credential auto-discovery
- Warning suppression for clean output
"""

import os
import sys
import warnings
from pathlib import Path

# ---------------------------------------------------------------------------
# Suppress noisy warnings before any third-party imports
# ---------------------------------------------------------------------------
# FutureWarning: Python 3.9 EOL notices from google-auth / google-api-core
# NotOpenSSLWarning: urllib3 v2 + LibreSSL on macOS
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*urllib3.*OpenSSL.*")

from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Data directory discovery
# ---------------------------------------------------------------------------

_SKILL_DIR_NAME = "google-analytics-and-search-improve"


def find_data_dir() -> Path | None:
    """Locate .skills-data/google-analytics-and-search-improve/ by walking up
    from this script's directory toward the filesystem root.

    Returns the Path if found, or None.
    """
    d = Path(__file__).resolve().parent
    while d != d.parent:
        candidate = d / ".skills-data" / _SKILL_DIR_NAME
        if candidate.is_dir():
            return candidate
        d = d.parent
    return None


DATA_DIR: Path | None = find_data_dir()


# ---------------------------------------------------------------------------
# .env loading (runs once at import time)
# ---------------------------------------------------------------------------

if DATA_DIR:
    _env_path = DATA_DIR / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)


# ---------------------------------------------------------------------------
# Google Service Account credential discovery
# ---------------------------------------------------------------------------

def find_google_credentials() -> str | None:
    """Auto-discover a Google Service Account JSON key.

    Resolution order:
    1. ``GOOGLE_APPLICATION_CREDENTIALS`` env var (if set and file exists)
    2. First ``*.json`` file (alphabetically) inside ``DATA_DIR/configs/``

    When a key is found via (2), ``GOOGLE_APPLICATION_CREDENTIALS`` is set in
    the environment so that Google client libraries that read the env var
    (e.g. ``BetaAnalyticsDataClient``) can pick it up automatically.

    Returns the path string, or None if no key is found.
    """
    # 1. Explicit env var takes priority
    explicit = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if explicit and Path(explicit).is_file():
        return explicit

    # 2. Auto-discover from configs/
    if DATA_DIR:
        configs_dir = DATA_DIR / "configs"
        if configs_dir.is_dir():
            json_files = sorted(configs_dir.glob("*.json"))
            if json_files:
                path = str(json_files[0])
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
                return path

    return None


def require_google_credentials() -> str:
    """Like :func:`find_google_credentials` but exits with an error message
    when no credentials are found."""
    path = find_google_credentials()
    if not path:
        print(
            "Error: No Google Service Account JSON key found.\n"
            "Place your *.json key file in: .skills-data/google-analytics-and-search-improve/configs/",
            file=sys.stderr,
        )
        sys.exit(1)
    return path
