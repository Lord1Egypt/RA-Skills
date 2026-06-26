"""
Nex Domains - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
Domain & DNS Portfolio Manager
"""
import os
from pathlib import Path

# Data directory - all domain data stored locally
DATA_DIR = Path(os.environ.get("NEX_DOMAINS_DATA", Path.home() / ".nex-domains"))
DB_PATH = DATA_DIR / "domains.db"
LOG_PATH = DATA_DIR / "nex-domains.log"

# API credentials from environment variables
# Cloudflare
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "")
CF_EMAIL = os.environ.get("CF_EMAIL", "")

# TransIP
TRANSIP_LOGIN = os.environ.get("TRANSIP_LOGIN", "")
TRANSIP_PRIVATE_KEY_PATH = os.environ.get("TRANSIP_PRIVATE_KEY_PATH", "")

# DNS record types supported
DNS_RECORD_TYPES = [
    "A",
    "AAAA",
    "CNAME",
    "MX",
    "TXT",
    "NS",
    "SRV",
    "CAA",
]

# Domain registrars supported
DOMAIN_REGISTRARS = [
    "cloudflare",
    "transip",
    "other",
]

# Alert thresholds (in days)
DOMAIN_EXPIRY_WARNING_DAYS = 90
SSL_EXPIRY_WARNING_DAYS = 30

# External tools
WHOIS_COMMAND = "whois"
DIG_COMMAND = "dig"
OPENSSL_COMMAND = "openssl"

# Default nameservers for DNS checks
DEFAULT_NAMESERVERS = [
    "8.8.8.8",
    "8.8.4.4",
    "1.1.1.1",
]

# Domain status types
DOMAIN_STATUS_TYPES = [
    "active",
    "expired",
    "parked",
    "transferring",
]

# Security settings
MAX_DOMAIN_NAME_LENGTH = 253
MAX_NOTES_LENGTH = 5000

# API rate limiting
API_TIMEOUT = 10
WHOIS_TIMEOUT = 15
SSL_CHECK_TIMEOUT = 10

# Logging
LOG_LEVEL = os.environ.get("NEX_DOMAINS_LOG_LEVEL", "INFO")
