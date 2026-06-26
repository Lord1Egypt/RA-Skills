#!/usr/bin/env python3
# Nex GDPR - Configuration
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

import os
from pathlib import Path

# Base data directory
DATA_DIR = Path.home() / ".nex-gdpr"
DB_PATH = DATA_DIR / "gdpr.db"
EXPORT_DIR = DATA_DIR / "exports"
AUDIT_DIR = DATA_DIR / "audit"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# GDPR Request Types (Articles)
REQUEST_TYPES = {
    "ACCESS": "Article 15 - Right to Access",
    "ERASURE": "Article 17 - Right to Erasure (Right to be Forgotten)",
    "PORTABILITY": "Article 20 - Right to Data Portability",
    "RECTIFICATION": "Article 16 - Right to Rectification",
    "RESTRICTION": "Article 18 - Right to Restrict Processing",
    "OBJECTION": "Article 21 - Right to Object",
}

# Request Status Values
REQUEST_STATUSES = {
    "RECEIVED": "Request received, verification pending",
    "VERIFIED": "Identity verified, processing",
    "IN_PROGRESS": "Active processing",
    "COMPLETED": "Completed and responded",
    "DENIED": "Request denied",
    "EXPIRED": "Request deadline expired",
}

# Legal Deadlines (GDPR Compliance)
RESPONSE_DEADLINE_DAYS = 30  # GDPR requires response within 1 month
EXTENSION_DAYS = 60  # Can extend by 2 months for complex requests
MAX_EXTENSION_TOTAL_DAYS = 90  # Total max 3 months with extension

# Data Scan Paths
SESSION_DIRS = [
    Path.home() / ".openclaw" / "sessions",
    Path.home() / ".claw" / "sessions",
    os.getenv("OPENCLAW_SESSIONS", ""),
]

MEMORY_DIR = Path.home() / ".nex-memory"
LOG_DIR = Path.home() / ".nex-logs"
UPLOAD_DIR = Path.home() / ".nex-uploads"

# Database scan paths for other nex-* skills
DB_FILES = [
    Path.home() / ".life-logger" / "activity.db",
    Path.home() / ".nex-inbox" / "inbox.db",
    Path.home() / ".nex-notes" / "notes.db",
]

# Retention Policies
DEFAULT_RETENTION_DAYS = 365  # Default 1 year retention
RETENTION_POLICIES = {
    "sessions": 365,
    "memory": 365,
    "logs": 90,
    "uploads": 180,
    "audit": 2555,  # 7 years for audit trail (compliance)
}

# Anonymization Settings
PII_ANONYMIZE_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
    r"\+?1?\d{9,15}",  # Phone numbers
    r"\b\d{8}\b",  # Belgian national number (YYYYMMDD)
    r"\bBE\d{10}\b",  # Belgian VAT number
]

# Response Letter Templates (Dutch/English)
RESPONSE_LETTER_TEMPLATE_NL = """Gerespecteerde {name},

Dank u voor uw verzoek ingevolge artikel {article} van de AVG (Algemene Verordening Gegevensbescherming).

Wij hebben uw verzoek ontvangen op {received_date} en hebben een deadline van {deadline_date} om te reageren.

Verzoektype: {request_type}
Status: {status}

{body}

Met vriendelijke groet,
{organization}
Dataprotectionofficer
nex-ai.be
"""

RESPONSE_LETTER_TEMPLATE_EN = """Dear {name},

Thank you for your request under Article {article} of the GDPR (General Data Protection Regulation).

We received your request on {received_date} and have a deadline of {deadline_date} to respond.

Request Type: {request_type}
Status: {status}

{body}

Best regards,
{organization}
Data Protection Officer
nex-ai.be
"""

# Footer
FOOTER = "[Nex GDPR by Nex AI | nex-ai.be]"
