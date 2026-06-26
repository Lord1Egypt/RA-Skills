"""
Nex PriceWatch Configuration Module
Copyright 2026 Nex AI (Kevin Blancaflor)
MIT-0 License
"""

import os
from pathlib import Path

# Data directory
DATA_DIR = Path.home() / ".nex-pricewatch"
DB_PATH = DATA_DIR / "pricewatch.db"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"

# Check interval
CHECK_INTERVAL_HOURS = 24

# Price change alert thresholds
ALERT_INCREASE_PCT = 5      # Alert on price increase > 5%
ALERT_DECREASE_PCT = 10     # Alert on price decrease > 10%

# Comparison types
COMPETITOR = "competitor"
SUPPLIER = "supplier"
MARKET = "market"
VALID_TYPES = [COMPETITOR, SUPPLIER, MARKET]

# Selector types
SELECTOR_CSS = "css"
SELECTOR_XPATH = "xpath"
SELECTOR_REGEX = "regex"
SELECTOR_TEXT = "text"
VALID_SELECTORS = [SELECTOR_CSS, SELECTOR_XPATH, SELECTOR_REGEX, SELECTOR_TEXT]

# HTTP settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Nex-PriceWatch/1.0"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 15
CONNECT_TIMEOUT = 10

# Telegram notification settings (optional)
TELEGRAM_ENABLED = False
TELEGRAM_BOT_TOKEN = os.getenv("NEX_PRICEWATCH_TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("NEX_PRICEWATCH_TELEGRAM_CHAT_ID", "")

# Currency symbols
CURRENCY_SYMBOLS = {
    "EUR": "€",
    "USD": "$",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "INR": "₹",
    "BRL": "R$",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF",
    "SEK": "kr",
    "NOK": "kr",
    "DKK": "kr",
    "PLN": "zł",
    "CZK": "Kč",
    "HUF": "Ft",
    "RON": "lei",
    "BGN": "лв",
    "HRK": "kn",
    "RUB": "₽",
    "TRY": "₺",
    "ILS": "₪",
}

# Common price patterns
PRICE_PATTERNS = [
    # €1.499,00 or €1499,00 or €1499 or €1499.00
    r'[€$£¥₹₽₺₪][\s]?[\d.,]+(?:[.,]\d{1,2})?',
    # 1.499,00 euro or 1499 EUR or 1499EUR
    r'[\d.,]+(?:[.,]\d{1,2})?\s*(?:euro|EUR|USD|$|£|GBP|¥|JPY|₹|INR|R\$|BRL|kr|SEK|NOK|DKK|zł|PLN|Kč|CZK|Ft|HUF|lei|RON|лв|BGN|kn|HRK|₽|RUB|₺|TRY|₪|ILS)',
    # From €1499 or from 1499
    r'(?:from|vanaf|à partir de|da)\s+[€$£¥₹₽₺₪]?[\s]?[\d.,]+',
]
