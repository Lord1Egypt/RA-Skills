"""
Nex MeetCost - Configuration
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path

# Paths
DATA_DIR = Path(os.environ.get("NEX_MEETCOST_DIR", Path.home() / ".nex-meetcost"))
DB_PATH = DATA_DIR / "meetcost.db"
EXPORT_DIR = DATA_DIR / "exports"

# Default hourly rates per role
DEFAULT_RATES = {
    "developer": 95.00,
    "designer": 90.00,
    "manager": 110.00,
    "sales": 85.00,
    "support": 70.00,
    "intern": 35.00,
    "executive": 150.00,
    "consultant": 120.00,
    "other": 85.00,
}

# Meeting types
MEETING_TYPES = [
    "standup", "planning", "review", "retro", "client",
    "sales", "internal", "onboarding", "brainstorm", "other",
]

CURRENCY_SYMBOL = "\u20ac"

# Display
SEPARATOR = "=" * 60
SUBSEPARATOR = "-" * 60
