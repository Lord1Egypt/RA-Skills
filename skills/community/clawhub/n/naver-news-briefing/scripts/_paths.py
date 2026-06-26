from __future__ import annotations

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
CONFIG_PATH = DATA_DIR / "config.json"
DB_PATH = DATA_DIR / "watch_state.db"
TEST_CACHE_DIR = DATA_DIR / ".pytest-cache"
UPSTREAM_REPO = Path(r"C:\Users\김태완\.openclaw\workspace\navernews-tabsearch")


def ensure_data_dir() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR
