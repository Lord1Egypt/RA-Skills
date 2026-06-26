#!/usr/bin/env python3
# Nex SkillMon - Configuration Module
# MIT-0 License - Copyright 2026 Nex AI

import os
from decimal import Decimal
from pathlib import Path

# Data directory
DATA_DIR = Path.home() / ".nex-skillmon"
DB_PATH = DATA_DIR / "skillmon.db"
LOG_PATH = DATA_DIR / "logs"
ENV_FILE = DATA_DIR / ".env"

# Skills directory - default OpenClaw skills directory
SKILLS_BASE_DIR = os.getenv(
    "SKILLS_BASE_DIR",
    os.path.expanduser("~/.config/openclaw/skills")
)

# ClawHub API configuration
CLAWHUB_API_URL = "https://api.clawhub.dev"

# Cost tracking - input token costs
COST_PER_TOKEN = {
    "gpt-4o": Decimal("0.0025") / 1000,
    "gpt-4o-mini": Decimal("0.00015") / 1000,
    "gpt-4-turbo": Decimal("0.003") / 1000,
    "gpt-4": Decimal("0.03") / 1000,
    "gpt-3.5-turbo": Decimal("0.0005") / 1000,
    "claude-3-opus": Decimal("0.015") / 1000,
    "claude-3-sonnet": Decimal("0.003") / 1000,
    "claude-3-haiku": Decimal("0.00025") / 1000,
    "claude-3-5-sonnet": Decimal("0.003") / 1000,
    "claude-haiku": Decimal("0.00025") / 1000,
    "gemini-1.5-pro": Decimal("0.00125") / 1000,
    "gemini-1.5-flash": Decimal("0.0001") / 1000,
}

# Thresholds and intervals
STALE_DAYS = 30
SECURITY_CHECK_HOURS = 24

# Alert categories
ALERT_CATEGORIES = {
    "UPDATE_AVAILABLE": "info",
    "SECURITY_FLAG": "critical",
    "STALE_SKILL": "warning",
    "HIGH_COST": "warning",
    "DEPRECATED": "warning",
    "INTEGRITY_CHANGED": "critical",
}

# Default currency
CURRENCY = os.getenv("CURRENCY", "EUR")
CURRENCY_SYMBOL = {"EUR": "€", "USD": "$", "GBP": "£", "JPY": "¥"}

# Log configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"

# API timeouts
API_TIMEOUT_SECONDS = 10
