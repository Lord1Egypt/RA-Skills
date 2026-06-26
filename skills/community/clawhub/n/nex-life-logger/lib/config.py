"""
Nex Life Logger - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import platform
from pathlib import Path

# Data directory (same as the desktop app - shared database)
# All collected data is stored locally in this directory. No data is sent externally
# unless the user explicitly configures an LLM provider for summary generation.
DATA_DIR = Path(os.environ.get("LIFELOGGER_DATA", Path.home() / ".life-logger"))
DB_PATH = DATA_DIR / "activity.db"
LOG_PATH = DATA_DIR / "life-logger.log"

# How often (in seconds) to poll browser history and active window
POLL_INTERVAL = 30

# Security settings
MAX_URL_LENGTH = 2048
MAX_TITLE_LENGTH = 512
MAX_TRANSCRIPT_LENGTH = 100_000

# API rate limiting
API_MIN_INTERVAL = 5
API_MAX_RETRIES = 3
API_BACKOFF_BASE = 2

# Sensitive window title keywords - windows matching these are NEVER logged
SENSITIVE_WINDOW_KEYWORDS = [
    "password", "passwd", "credential", "keychain", "vault",
    "1password", "lastpass", "bitwarden", "keepass", "dashlane",
    "private browsing", "incognito", "inprivate",
    "bank", "banking",
]

# Content filtering
PRODUCTIVITY_FILTER_ENABLED = True
USE_AI_FILTER = False

# YouTube Transcripts
FETCH_TRANSCRIPTS = True

# AI Summarization - must be explicitly configured by the user
# No default API endpoint. All LLM features require the user to run:
#   nex-life-logger config set-api-key
#   nex-life-logger config set-provider <name>
AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_API_BASE = os.environ.get("AI_API_BASE", "")
AI_MODEL = os.environ.get("AI_MODEL", "")

# Autosave / Backup
AUTOSAVE_ENABLED = True
AUTOSAVE_HOUR = 6
AUTOSAVE_WEEKLY_DAY = 5
AUTOSAVE_MONTHLY = True
AUTOSAVE_KEEP_MAX = 20

# Summary schedule (24h clock)
DAILY_SUMMARY_HOUR = 23
WEEKLY_SUMMARY_DAY = 6
MONTHLY_SUMMARY_DAY = 1
YEARLY_SUMMARY_MONTH = 1
YEARLY_SUMMARY_DAY = 1

# Browser history paths (auto-detected per OS)
_system = platform.system()
_home = Path.home()

if _system == "Windows":
    BROWSER_PATHS = {
        "chrome": _home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "History",
        "edge": _home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "History",
        "firefox_dir": _home / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles",
        "brave": _home / "AppData" / "Local" / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "History",
    }
elif _system == "Darwin":
    BROWSER_PATHS = {
        "chrome": _home / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "History",
        "edge": _home / "Library" / "Application Support" / "Microsoft Edge" / "Default" / "History",
        "firefox_dir": _home / "Library" / "Application Support" / "Firefox" / "Profiles",
        "brave": _home / "Library" / "Application Support" / "BraveSoftware" / "Brave-Browser" / "Default" / "History",
    }
else:
    BROWSER_PATHS = {
        "chrome": _home / ".config" / "google-chrome" / "Default" / "History",
        "edge": _home / ".config" / "microsoft-edge" / "Default" / "History",
        "firefox_dir": _home / ".config" / "mozilla" / "firefox",
        "brave": _home / ".config" / "BraveSoftware" / "Brave-Browser" / "Default" / "History",
    }
