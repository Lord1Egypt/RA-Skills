"""
Nex Vault - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import platform
from pathlib import Path

# Data directory (all vault data stored locally, no cloud sync)
# All documents and metadata stay on this machine
DATA_DIR = Path(os.environ.get("NEX_VAULT_DATA", Path.home() / ".nex-vault"))
DB_PATH = DATA_DIR / "vault.db"
VAULT_DIR = DATA_DIR / "documents"
EXPORT_DIR = DATA_DIR / "exports"

# Create directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
VAULT_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Document types
DOCUMENT_TYPES = [
    "CONTRACT",
    "LEASE",
    "INSURANCE",
    "SLA",
    "WARRANTY",
    "LICENSE",
    "SUBSCRIPTION",
    "CERTIFICATE",
    "PERMIT",
    "OTHER",
]

# Alert thresholds: days before expiry to create alerts
ALERT_DAYS = [90, 60, 30, 14, 7, 1]

# Notification settings
TELEGRAM_BOT_TOKEN = os.environ.get("NEX_VAULT_TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("NEX_VAULT_TELEGRAM_CHAT_ID", "")

# Supported file formats
SUPPORTED_FORMATS = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}

# Date extraction patterns (optimized for Belgian/EU formats)
DATE_PATTERNS = [
    r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",  # DD/MM/YYYY or DD-MM-YYYY
    r"\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b",  # YYYY/MM/DD or YYYY-MM-DD
    r"\b(\d{1,2})\s+(januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december|january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})\b",  # Day Month Year
    r"\b(\d{1,2})\s+(?:de|st|nd|rd)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{4})\b",  # Abbreviated formats
]

# Auto-renewal detection keywords
AUTO_RENEWAL_KEYWORDS = [
    "automatische verlenging",
    "automatisch vernieuwd",
    "auto-renewal",
    "automatic renewal",
    "automatically renewed",
    "automatically renews",
    "unless terminated",
    "tenzij opgezeit",
    "unless cancelled",
    "renewal clause",
    "vernieuwingsclausule",
    "extend for",
    "verlengd voor",
    "will renew",
    "zal verlengen",
]

# Termination notice keywords
TERMINATION_KEYWORDS = [
    "termination notice",
    "notice to terminate",
    "opzeggingstermijn",
    "opzegperiode",
    "notice period",
    "days' notice",
    "days notice",
    "maanden opzeg",
    "dagen opzeg",
    "months' notice",
]

# Key clause types
CLAUSE_TYPES = [
    "termination",
    "renewal",
    "payment",
    "liability",
    "confidentiality",
    "liability",
    "indemnification",
    "force_majeure",
]

# Security settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_TEXT_LENGTH = 500_000  # Max chars to extract from document
MAX_PARTIES = 10  # Max party names to extract per document

# API rate limiting (for Telegram notifications)
API_MIN_INTERVAL = 5
API_MAX_RETRIES = 3
API_BACKOFF_BASE = 2

# File hashing for duplicate detection
HASH_ALGORITHM = "sha256"

# Log settings
LOG_PATH = DATA_DIR / "vault.log"

# Security: ensure data directory has restricted permissions
if platform.system() != "Windows":
    os.chmod(str(DATA_DIR), 0o700)  # rwx------
