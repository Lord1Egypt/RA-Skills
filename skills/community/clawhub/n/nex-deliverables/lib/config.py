"""
Nex Deliverables - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Client Deliverable Tracker for agency operators and freelancers.
All data stored locally at ~/.nex-deliverables
"""
import os
from pathlib import Path

# Data directory for all deliverable tracking data
DATA_DIR = Path(os.environ.get("NEX_DELIVERABLES_DATA", Path.home() / ".nex-deliverables"))
DB_PATH = DATA_DIR / "deliverables.db"
EXPORT_DIR = DATA_DIR / "exports"

# Deliverable lifecycle statuses
STATUSES = ["planned", "in_progress", "review", "delivered", "approved", "rejected"]

# Types of deliverables common in agency/freelance work
DELIVERABLE_TYPES = [
    "website",
    "landing_page",
    "design",
    "logo",
    "branding",
    "copy",
    "email_campaign",
    "automation",
    "funnel",
    "seo",
    "maintenance",
    "custom"
]

# Priority levels for task urgency
PRIORITY_LEVELS = ["urgent", "high", "normal", "low"]

# Default SLA (Service Level Agreement) - days to deliver by type
# Used for deadline calculations if not explicitly set
DEFAULT_SLA_DAYS = {
    "website": 30,
    "landing_page": 14,
    "design": 10,
    "logo": 7,
    "branding": 21,
    "copy": 3,
    "email_campaign": 5,
    "automation": 14,
    "funnel": 21,
    "seo": 30,
    "maintenance": 1,
    "custom": 14
}

# Email status templates for generating professional update emails
STATUS_EMAIL_TEMPLATES = {
    "status_header": "Client Deliverable Status Update",
    "open_section": "Open Deliverables",
    "delivered_section": "Delivered",
    "overdue_section": "Overdue Items",
    "next_steps": "Next Steps",
}

# Email signature
EMAIL_SIGNATURE = "---\nNex Deliverables by Nex AI | nex-ai.be"

# Pagination settings
DEFAULT_LIMIT = 50

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
