"""Centralized configuration — reads from .env if present."""

from __future__ import annotations

import os
from pathlib import Path

# Load .env if it exists (lightweight, no extra dependency)
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# ── Paths ────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SOURCES_YAML = CONFIG_DIR / "sources.yaml"
DATA_DIR = PROJECT_ROOT / "data"
FEED_RAW_JSON = PROJECT_ROOT / "feed_raw.json"
FEED_MERGED_JSON = PROJECT_ROOT / "feed_merged.json"
MEMO_DIR = PROJECT_ROOT / "memo"

# ── Dedup ─────────────────────────────────────────────────────
SHOWN_URL_LOOKBACK_DAYS = int(os.environ.get("XFEED_SHOWN_LOOKBACK_DAYS", "7"))

# ── Pipeline ─────────────────────────────────────────────────
PIPELINE_OUTPUT = os.environ.get("XFEED_OUTPUT", str(FEED_MERGED_JSON))

# ── X Scraper (used by scrape_feed.py) ───────────────────────
X_TARGET_POSTS_PER_TAB = int(os.environ.get("X_TARGET_POSTS", "40"))
X_MAX_SCROLLS = int(os.environ.get("X_MAX_SCROLLS", "50"))
X_WAIT_SECONDS = int(os.environ.get("X_WAIT_SECONDS", "3"))
X_SCRAPE_TRENDING = os.environ.get("X_SCRAPE_TRENDING", "true").lower() == "true"
X_TRENDING_TOPIC_COUNT = int(os.environ.get("X_TRENDING_TOPICS", "10"))
X_MAX_RETRIES = int(os.environ.get("X_MAX_RETRIES", "3"))
X_RETRY_DELAY = int(os.environ.get("X_RETRY_DELAY", "5"))
X_STALE_SCROLL_LIMIT = int(os.environ.get("X_STALE_SCROLL_LIMIT", "5"))
X_GLOBAL_TIMEOUT = int(os.environ.get("X_GLOBAL_TIMEOUT", "600"))
