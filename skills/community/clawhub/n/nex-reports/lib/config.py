"""
Nex Reports - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# Data directory
DATA_DIR = Path.home() / ".nex-reports"
DB_PATH = DATA_DIR / "reports.db"
REPORTS_DIR = DATA_DIR / "reports"
TEMPLATES_DIR = DATA_DIR / "templates"

# Report modules available
REPORT_MODULES = {
    "EMAIL": {
        "name": "Email",
        "description": "Check unread emails via IMAP",
        "config_keys": ["imap_host", "imap_user", "imap_pass", "imap_port", "unread_limit"],
    },
    "CALENDAR": {
        "name": "Calendar",
        "description": "Parse ICS calendar file for events",
        "config_keys": ["ics_path", "show_days"],
    },
    "TASKS": {
        "name": "Tasks",
        "description": "Read JSON taskboard file",
        "config_keys": ["taskboard_path"],
    },
    "HEALTH": {
        "name": "Health Check",
        "description": "Run nex-healthcheck command",
        "config_keys": [],
    },
    "CRM": {
        "name": "CRM Pipeline",
        "description": "Run nex-crm pipeline command",
        "config_keys": [],
    },
    "EXPENSES": {
        "name": "Expenses",
        "description": "Run nex-expenses summary",
        "config_keys": [],
    },
    "DELIVERABLES": {
        "name": "Deliverables",
        "description": "Run nex-deliverables overdue",
        "config_keys": [],
    },
    "DOMAINS": {
        "name": "Domains",
        "description": "Run nex-domains expiring",
        "config_keys": [],
    },
    "VAULT": {
        "name": "Vault",
        "description": "Run nex-vault alerts",
        "config_keys": [],
    },
    "CUSTOM": {
        "name": "Custom Command",
        "description": "Run arbitrary shell command",
        "config_keys": ["command"],
    },
}

# Schedule presets
SCHEDULE_PRESETS = {
    "DAILY_MORNING": "0 8 * * *",  # Every day at 8:00 AM
    "DAILY_EVENING": "0 18 * * *",  # Every day at 6:00 PM
    "WEEKLY_MONDAY": "0 8 * * 1",  # Every Monday at 8:00 AM
    "WEEKLY_FRIDAY": "0 17 * * 5",  # Every Friday at 5:00 PM
    "MONTHLY_FIRST": "0 8 1 * *",  # First day of month at 8:00 AM
}

# Output formats
OUTPUT_FORMATS = {
    "TELEGRAM": "telegram",
    "MARKDOWN": "markdown",
    "HTML": "html",
    "JSON": "json",
}

# Output targets
OUTPUT_TARGETS = {
    "TELEGRAM": "telegram",
    "FILE": "file",
    "BOTH": "both",
}

# IMAP settings from environment
IMAP_HOST = os.getenv("IMAP_HOST", "imap.gmail.com")
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASS = os.getenv("IMAP_PASS", "")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))

# Telegram settings from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Report metadata
REPORT_FOOTER = "[Nex Reports by Nex AI | nex-ai.be]"

# Database schema
DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS report_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    schedule TEXT NOT NULL,
    modules TEXT NOT NULL,
    output_format TEXT NOT NULL,
    output_target TEXT NOT NULL,
    enabled INTEGER DEFAULT 1,
    last_run TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS report_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_id INTEGER NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL,
    output_path TEXT,
    module_results TEXT,
    errors TEXT,
    FOREIGN KEY (config_id) REFERENCES report_configs (id)
);

CREATE INDEX IF NOT EXISTS idx_report_runs_config_id ON report_runs(config_id);
CREATE INDEX IF NOT EXISTS idx_report_runs_started_at ON report_runs(started_at);
"""
