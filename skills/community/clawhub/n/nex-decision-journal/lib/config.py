"""
Nex Decision Journal - Configuration
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = Path(os.environ.get("NEX_DECISION_JOURNAL_DIR", Path.home() / ".nex-decision-journal"))
DB_PATH = DATA_DIR / "decisions.db"
EXPORT_DIR = DATA_DIR / "exports"

# ---------------------------------------------------------------------------
# Decision categories
# ---------------------------------------------------------------------------
CATEGORIES = [
    "business",
    "hiring",
    "product",
    "technical",
    "financial",
    "marketing",
    "sales",
    "partnership",
    "personal",
    "career",
    "health",
    "investment",
    "legal",
    "operational",
    "strategic",
    "other",
]

# ---------------------------------------------------------------------------
# Confidence scale
# ---------------------------------------------------------------------------
CONFIDENCE_MIN = 1
CONFIDENCE_MAX = 10
CONFIDENCE_LABELS = {
    1: "Pure guess",
    2: "Very uncertain",
    3: "Uncertain",
    4: "Slightly uncertain",
    5: "Coin flip",
    6: "Slightly confident",
    7: "Confident",
    8: "Very confident",
    9: "Almost certain",
    10: "Certain",
}

# ---------------------------------------------------------------------------
# Default follow-up periods (days)
# ---------------------------------------------------------------------------
DEFAULT_FOLLOW_UP_DAYS = 90
FOLLOW_UP_OPTIONS = {
    "1w": 7,
    "2w": 14,
    "1m": 30,
    "2m": 60,
    "3m": 90,
    "6m": 180,
    "1y": 365,
}

# ---------------------------------------------------------------------------
# Decision statuses
# ---------------------------------------------------------------------------
STATUS_PENDING = "pending"          # Decision logged, no outcome yet
STATUS_REVIEWED = "reviewed"        # Outcome recorded
STATUS_ABANDONED = "abandoned"      # Decision was never acted on

# ---------------------------------------------------------------------------
# Outcome accuracy
# ---------------------------------------------------------------------------
ACCURACY_CORRECT = "correct"
ACCURACY_PARTIALLY = "partially_correct"
ACCURACY_WRONG = "wrong"
ACCURACY_OPTIONS = [ACCURACY_CORRECT, ACCURACY_PARTIALLY, ACCURACY_WRONG]

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
SEPARATOR = "=" * 60
SUBSEPARATOR = "-" * 60
MAX_LIST_TITLE_LEN = 40
MAX_LIST_CATEGORY_LEN = 12
