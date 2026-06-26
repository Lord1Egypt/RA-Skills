"""
Nex CRM - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path

# Data directory (same as the desktop app - shared database)
# All prospect data is stored locally in this directory. No data is sent externally
# unless the user explicitly configures an LLM provider for AI analysis.
DATA_DIR = Path(os.environ.get("NEX_CRM_DATA", Path.home() / ".nex-crm"))
DB_PATH = DATA_DIR / "crm.db"
LOG_PATH = DATA_DIR / "nex-crm.log"
EXPORT_DIR = DATA_DIR / "exports"

# Pipeline stages (in order)
PIPELINE_STAGES = [
    "lead",
    "contacted",
    "demo_scheduled",
    "demo_done",
    "proposal_sent",
    "negotiation",
    "won",
    "lost",
    "churned",
]

# Pipeline stage labels (Dutch + English)
PIPELINE_STAGE_LABELS = {
    "lead": "Lead / Nieuw",
    "contacted": "Gecontacteerd",
    "demo_scheduled": "Demo gepland",
    "demo_done": "Demo gedaan",
    "proposal_sent": "Offerte verstuurd",
    "negotiation": "Onderhandeling",
    "won": "Gewonnen",
    "lost": "Verloren",
    "churned": "Churned",
}

# Lead sources
LEAD_SOURCES = ["scrape", "referral", "inbound", "outreach", "event", "website", "other"]

# Activity types
ACTIVITY_TYPES = ["call", "email", "meeting", "demo", "note", "follow_up", "proposal", "invoice"]

# Priority levels
PRIORITY_LEVELS = ["hot", "warm", "cold"]

# Default follow-up intervals per stage (in days)
FOLLOW_UP_DAYS = {
    "lead": 3,
    "contacted": 5,
    "demo_scheduled": 1,
    "demo_done": 2,
    "proposal_sent": 7,
    "negotiation": 3,
    "won": 365,
    "lost": None,
    "churned": None,
}

# Retainer tiers matching Nex AI pricing
RETAINER_TIERS = {
    "starter": 299,
    "growth": 799,
    "premium": 1499,
    "enterprise": 2499,
}

# Currency
CURRENCY = "EUR"

# Notification settings
NOTIFY_STALE_DAYS = 14  # Days without contact before flagging
NOTIFY_FOLLOW_UP = True

# Tags/industry defaults for Belgian SME market
DEFAULT_INDUSTRIES = [
    "Manufacturing",
    "Retail",
    "Services",
    "Technology",
    "Healthcare",
    "Finance",
    "Hospitality",
    "Real Estate",
    "Legal",
    "Consulting",
    "Education",
    "Non-profit",
    "Other",
]

DEFAULT_TAGS = [
    "belgian-sme",
    "decision-maker-identified",
    "budget-approved",
    "urgent-timeline",
    "vat-verified",
    "contract-ready",
]

# API rate limiting
API_MIN_INTERVAL = 5
API_MAX_RETRIES = 3
API_BACKOFF_BASE = 2

# AI Conversation Memory - must be explicitly configured by the user
AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_API_BASE = os.environ.get("AI_API_BASE", "")
AI_MODEL = os.environ.get("AI_MODEL", "")

# Autosave / Backup
AUTOSAVE_ENABLED = True
AUTOSAVE_HOUR = 6
AUTOSAVE_WEEKLY_DAY = 5
AUTOSAVE_MONTHLY = True
AUTOSAVE_KEEP_MAX = 20
