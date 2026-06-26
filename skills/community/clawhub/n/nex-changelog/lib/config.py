"""Configuration for nex-changelog."""

import os
from pathlib import Path

# Data storage
DATA_DIR = Path.home() / ".nex-changelog"
DB_PATH = DATA_DIR / "changelog.db"
EXPORT_DIR = DATA_DIR / "exports"

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Change types (aligned with Keep a Changelog and conventional commits)
CHANGE_TYPES = {
    "ADDED": "Added",
    "CHANGED": "Changed",
    "FIXED": "Fixed",
    "REMOVED": "Removed",
    "SECURITY": "Security",
    "DEPRECATED": "Deprecated",
    "PERFORMANCE": "Performance"
}

# Audience types
AUDIENCE_TYPES = {
    "INTERNAL": "Internal (dev team)",
    "CLIENT": "Client-facing",
    "PUBLIC": "Public (marketing/blog)"
}

# Version format
VERSION_FORMAT = "SEMVER"  # major.minor.patch

# Template styles for export
TEMPLATE_STYLES = {
    "KEEPACHANGELOG": "Keep a Changelog format",
    "SIMPLE": "Simple bullet list",
    "CLIENT_EMAIL": "Professional client email",
    "TELEGRAM": "Telegram-friendly (compact with emojis)"
}

# Default settings
DEFAULT_PROJECT = None
DEFAULT_CLIENT = None
DEFAULT_TEMPLATE = "KEEPACHANGELOG"
DEFAULT_AUDIENCE = "CLIENT"

# Mapping of conventional commit types to change types
COMMIT_TYPE_MAPPING = {
    "feat": "ADDED",
    "feature": "ADDED",
    "fix": "FIXED",
    "bugfix": "FIXED",
    "docs": "CHANGED",
    "style": "CHANGED",
    "refactor": "CHANGED",
    "perf": "PERFORMANCE",
    "performance": "PERFORMANCE",
    "test": "CHANGED",
    "chore": "CHANGED",
    "ci": "CHANGED",
    "security": "SECURITY",
    "deprecation": "DEPRECATED",
    "breaking": "REMOVED"
}

# Emojis for changelog formatting
CHANGE_TYPE_EMOJIS = {
    "ADDED": "✨",
    "CHANGED": "📝",
    "FIXED": "🐛",
    "REMOVED": "🗑️",
    "SECURITY": "🔒",
    "DEPRECATED": "⚠️",
    "PERFORMANCE": "⚡"
}

# Telegram emojis (more compact)
TELEGRAM_EMOJIS = {
    "ADDED": "✨",
    "CHANGED": "📝",
    "FIXED": "🐛",
    "REMOVED": "🗑️",
    "SECURITY": "🔒",
    "DEPRECATED": "⚠️",
    "PERFORMANCE": "⚡"
}
