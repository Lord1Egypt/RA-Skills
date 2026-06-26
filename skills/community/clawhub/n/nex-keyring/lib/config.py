"""
Nex Keyring - Configuration Module
Configuration settings, constants, and policies for API key/secret rotation tracking.
"""

import os
from pathlib import Path
from typing import Dict, Optional

# Data storage paths
DATA_DIR = Path(os.path.expanduser("~/.nex-keyring"))
DB_PATH = DATA_DIR / "keyring.db"
EXPORT_DIR = DATA_DIR / "exports"

# Rotation policies (in days)
DEFAULT_ROTATION_DAYS = 90
STRICT_ROTATION_DAYS = 30

# Service categories
SERVICE_CATEGORIES = [
    "API",
    "DATABASE",
    "SSH",
    "OAUTH",
    "WEBHOOK",
    "SMTP",
    "DNS",
    "HOSTING",
    "AI",
    "PAYMENT",
    "OTHER"
]

# Risk levels based on staleness (days since last rotation)
RISK_LEVELS = {
    "FRESH": (0, 30),          # Last rotated within 30 days
    "OK": (30, 90),            # 30-90 days
    "STALE": (90, 180),        # 90-180 days
    "CRITICAL": (180, float('inf'))  # Over 180 days
}

# Common service presets with default rotation policies (in days)
SERVICE_PRESETS: Dict[str, int] = {
    "cloudflare": 180,
    "openai": 90,
    "resend": 90,
    "firebase": 180,
    "github": 90,
    "transip": 365,
    "dashscope": 90,
    "stripe": 90,
    "telegram": 365,
}

# Encryption settings
try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
    ENCRYPTION_METHOD = "fernet"
except ImportError:
    ENCRYPTION_AVAILABLE = False
    ENCRYPTION_METHOD = "base64"

# Service detection patterns (key name -> service mapping)
SERVICE_PATTERNS = {
    "openai": ["OPENAI_", "GPT_"],
    "cloudflare": ["CF_", "CLOUDFLARE_"],
    "firebase": ["FIREBASE_", "FB_"],
    "resend": ["RESEND_"],
    "github": ["GITHUB_", "GH_"],
    "transip": ["TRANSIP_"],
    "dashscope": ["DASHSCOPE_", "QWEN_"],
    "stripe": ["STRIPE_", "SK_", "PK_"],
    "telegram": ["TELEGRAM_", "TG_"],
    "aws": ["AWS_", "AWSACCESS"],
    "gcp": ["GOOGLE_", "GCP_"],
    "azure": ["AZURE_"],
    "mongodb": ["MONGODB_", "MONGO_"],
    "postgres": ["POSTGRES_", "PG_", "DATABASE_"],
    "mysql": ["MYSQL_", "DB_"],
    "slack": ["SLACK_"],
    "twilio": ["TWILIO_"],
    "sendgrid": ["SENDGRID_"],
    "mailgun": ["MAILGUN_"],
    "auth0": ["AUTH0_"],
    "okta": ["OKTA_"],
    "jwt": ["JWT_", "SECRET_KEY", "PRIVATE_KEY", "ACCESS_TOKEN"],
    "ssh": ["SSH_", "RSA_", "PRIVATE_KEY"],
    "api": ["API_KEY", "API_SECRET", "API_TOKEN"],
}

# File templates for export formats
EXPORT_TEMPLATES = {
    "json": {
        "extension": ".json",
        "description": "JSON format (metadata only)"
    },
    "csv": {
        "extension": ".csv",
        "description": "CSV format (metadata only)"
    },
    "markdown": {
        "extension": ".md",
        "description": "Markdown format (metadata only)"
    },
}
