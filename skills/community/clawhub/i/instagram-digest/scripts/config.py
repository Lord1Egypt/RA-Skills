import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ── Instagram accounts to track ──────────────────────────────────────────────
INSTAGRAM_ACCOUNTS = [
    "immigrant_talks",
    "yudi.j",
    "firstpost",
    "cleoabram",
    "aaronparnas",
    "fayedsouza",
]

# ── Instagram login (required for stories; optional for reels only) ───────────
# Create a free Instagram account dedicated to this bot to avoid locking your main one.
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")

# ── OpenRouter ────────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# ── Scraping limits ───────────────────────────────────────────────────────────
# How many hours back to look for new reels
LOOKBACK_HOURS = 168
# Max reels fetched per account
MAX_REELS_PER_ACCOUNT = 3
