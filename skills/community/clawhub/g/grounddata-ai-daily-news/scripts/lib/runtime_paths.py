"""
runtime_paths.py — runtime storage paths for cross-platform skill installs
"""

import os
import sys
from pathlib import Path

APP_NAME = "ai-daily-news"

_LIB_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS_DIR = _LIB_DIR.parent
_SKILL_ROOT = _SCRIPTS_DIR.parent


def get_runtime_cache_root() -> Path:
    """Return the writable runtime cache root for this user."""
    override = os.getenv("AINEWS_CACHE_DIR")
    if override:
        return Path(override).expanduser()

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / APP_NAME

    if os.name == "nt":
        local_app_data = os.getenv("LOCALAPPDATA")
        base = Path(local_app_data) if local_app_data else (Path.home() / "AppData" / "Local")
        return base / APP_NAME

    xdg_cache_home = os.getenv("XDG_CACHE_HOME")
    base = Path(xdg_cache_home).expanduser() if xdg_cache_home else (Path.home() / ".cache")
    return base / APP_NAME


def get_dataset_cache_dir() -> Path:
    return get_runtime_cache_root() / "datasets"


def get_delivery_log_path() -> Path:
    return get_runtime_cache_root() / "delivery_log.json"


def get_manifest_cache_path() -> Path:
    return get_runtime_cache_root() / "ai_news_manifest.json"


def get_engagement_state_path() -> Path:
    return get_runtime_cache_root() / "engagement_state.json"


def get_growth_state_path() -> Path:
    return get_runtime_cache_root() / "growth_state.json"


def get_preferences_state_path() -> Path:
    return get_runtime_cache_root() / "preferences_state.json"


def get_bundled_manifest_path() -> Path:
    return _SCRIPTS_DIR / "data" / "ai_news_manifest.json"


def get_legacy_dataset_cache_dir() -> Path:
    return _SKILL_ROOT / "data" / "cache"
