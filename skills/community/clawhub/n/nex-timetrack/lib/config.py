"""
Nex Timetrack - Configuration
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path

# Paths
DATA_DIR = Path(os.environ.get("NEX_TIMETRACK_DIR", Path.home() / ".nex-timetrack"))
DB_PATH = DATA_DIR / "timetrack.db"
EXPORT_DIR = DATA_DIR / "exports"

# Activity categories
CATEGORIES = [
    "development",
    "design",
    "meeting",
    "research",
    "admin",
    "support",
    "review",
    "testing",
    "deployment",
    "planning",
    "communication",
    "other",
]

# Billable status
BILLABLE = "billable"
NON_BILLABLE = "non-billable"

# Default hourly rate (EUR)
DEFAULT_RATE = 85.00

# Currency
CURRENCY = "EUR"
CURRENCY_SYMBOL = "\u20ac"

# Rounding: round up to nearest X minutes for invoicing
ROUND_TO_MINUTES = 15

# Display
SEPARATOR = "=" * 60
SUBSEPARATOR = "-" * 60
