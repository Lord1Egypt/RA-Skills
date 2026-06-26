"""
Nex Ghostwriter - Configuration
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path

# Paths
DATA_DIR = Path(os.environ.get("NEX_GHOSTWRITER_DIR", Path.home() / ".nex-ghostwriter"))
DB_PATH = DATA_DIR / "ghostwriter.db"
EXPORT_DIR = DATA_DIR / "exports"
TEMPLATES_DIR = DATA_DIR / "templates"

# Meeting types
MEETING_TYPES = [
    "client",
    "internal",
    "sales",
    "discovery",
    "kickoff",
    "review",
    "standup",
    "retrospective",
    "pitch",
    "negotiation",
    "onboarding",
    "support",
    "other",
]

# Email tones
TONES = [
    "professional",
    "friendly",
    "formal",
    "casual",
    "direct",
]

# Default tone
DEFAULT_TONE = "professional"

# Urgency levels
URGENCY_LEVELS = ["low", "normal", "high"]

# Follow-up statuses
STATUS_DRAFT = "draft"
STATUS_SENT = "sent"
STATUS_SKIPPED = "skipped"

# Display
SEPARATOR = "=" * 60
SUBSEPARATOR = "-" * 60
