#!/usr/bin/env python3
"""
OpenClaw Security Guard - Utility Functions
"""

import json
import locale
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Constants
VERSION = "1.0.0"
OPENCLAW_DIR = Path.home() / ".openclaw"
CONFIG_FILE = OPENCLAW_DIR / "openclaw.json"
SKILL_DIR = Path(__file__).parent.parent

# ANSI Colors
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"

    # Background
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"


def detect_language() -> str:
    """Auto-detect user language based on system locale."""
    try:
        lang = locale.getdefaultlocale()[0]
        if lang and lang.lower().startswith('zh'):
            return 'zh'
    except:
        pass
    return 'en'


def load_i18n(lang: str = None) -> Dict:
    """Load internationalization strings."""
    if lang is None:
        lang = detect_language()

    i18n_file = SKILL_DIR / "config" / "i18n" / f"{lang}.json"

    if i18n_file.exists():
        try:
            with open(i18n_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass

    # Fallback to English
    return get_default_i18n()


def get_default_i18n() -> Dict:
    """Get default English strings."""
    return {
        "title": "OpenClaw Security Guard",
        "version": f"v{VERSION}",
        "description": "Security tool for OpenClaw users",
        "commands": {
            "audit": "Run security audit",
            "scan": "Scan for secrets",
            "access": "Manage access control",
            "token": "Manage tokens",
            "report": "Generate security report",
            "harden": "Apply security hardening",
            "status": "Quick security status"
        },
        "severity": {
            "critical": "CRITICAL",
            "high": "HIGH",
            "medium": "MEDIUM",
            "low": "LOW",
            "info": "INFO"
        },
        "status": {
            "excellent": "Excellent",
            "good": "Good",
            "warning": "Warning",
            "poor": "Poor",
            "critical": "Critical"
        },
        "messages": {
            "no_issues": "No security issues found",
            "fix_available": "Auto-fix available",
            "run_harden": "Run with --fix to auto-fix issues",
            "scan_complete": "Scan complete",
            "audit_complete": "Audit complete",
            "report_generated": "Report generated",
            "no_config": "OpenClaw config not found"
        }
    }


def load_config() -> Dict:
    """Load OpenClaw configuration."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def load_skill_config() -> Dict:
    """Load skill configuration."""
    config_file = SKILL_DIR / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def print_header(title: str, i18n: Dict):
    """Print formatted header."""
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}🔐 {title} v{VERSION}{Colors.RESET}")
    print(f"{Colors.WHITE}{'━' * 50}{Colors.RESET}")
    print()


def print_severity(severity: str, i18n: Dict) -> str:
    """Get colored severity string."""
    severity_map = {
        "critical": (Colors.BG_RED + Colors.WHITE, "🔴 CRITICAL"),
        "high": (Colors.RED, "🔴 HIGH"),
        "medium": (Colors.YELLOW, "⚠️  MEDIUM"),
        "low": (Colors.BLUE, "📝 LOW"),
        "info": (Colors.CYAN, "ℹ️  INFO")
    }
    color, text = severity_map.get(severity.lower(), (Colors.WHITE, severity.upper()))
    return f"{color}{text}{Colors.RESET}"


def get_score_rating(score: int) -> tuple:
    """Get rating and emoji for score."""
    if score >= 90:
        return ("excellent", "✅")
    elif score >= 75:
        return ("good", "✅")
    elif score >= 50:
        return ("warning", "⚠️")
    elif score >= 25:
        return ("poor", "🔴")
    else:
        return ("critical", "🔴")


def calculate_score(findings: List[Dict], weights: Dict) -> int:
    """Calculate security score based on findings."""
    base_score = 100

    for finding in findings:
        severity = finding.get("severity", "info").lower()
        base_score -= weights.get(severity, 0)

    return max(0, min(100, base_score))


def format_table(rows: List[List[str]], headers: List[str] = None) -> str:
    """Format data as table."""
    if not rows:
        return ""

    # Calculate column widths
    all_rows = [headers] + rows if headers else rows
    col_count = max(len(row) for row in all_rows)
    col_widths = [0] * col_count

    for row in all_rows:
        for i, cell in enumerate(row):
            # Strip ANSI codes for width calculation
            clean = re.sub(r'\033\[[0-9;]*m', '', str(cell))
            col_widths[i] = max(col_widths[i], len(clean))

    # Build table
    lines = []
    for row_idx, row in enumerate(all_rows):
        cells = []
        for i in range(col_count):
            cell = str(row[i]) if i < len(row) else ""
            clean = re.sub(r'\033\[[0-9;]*m', '', cell)
            padding = " " * (col_widths[i] - len(clean))
            cells.append(f"{cell}{padding}")
        lines.append("  ".join(cells))

        # Add separator after headers
        if headers and row_idx == 0:
            separator = "  ".join("─" * w for w in col_widths)
            lines.append(separator)

    return "\n".join(lines)


def mask_secret(value: str, show_len: int = 4) -> str:
    """Mask sensitive value for display."""
    if len(value) <= show_len:
        return "*" * len(value)
    return value[:show_len] + "*" * (len(value) - show_len)


def check_openclaw_installed() -> bool:
    """Check if OpenClaw is installed."""
    return OPENCLAW_DIR.exists() and CONFIG_FILE.exists()


def get_gateway_info(config: Dict) -> Dict:
    """Extract gateway information from config."""
    gateway = config.get("gateway", {})
    return {
        "port": gateway.get("port", 18789),
        "mode": gateway.get("mode", "local"),
        "bind": gateway.get("bind", "loopback"),
        "auth_mode": gateway.get("auth", {}).get("mode", "none")
    }


def get_channels_info(config: Dict) -> Dict:
    """Extract channels information from config."""
    channels = config.get("channels", {})
    result = {}
    for channel_name, channel_config in channels.items():
        if channel_config.get("enabled", False):
            accounts = channel_config.get("accounts", {})
            result[channel_name] = {
                "enabled": True,
                "accounts": list(accounts.keys())
            }
    return result


def get_models_info(config: Dict) -> Dict:
    """Extract models/providers information from config."""
    providers = config.get("models", {}).get("providers", {})
    result = []
    for provider_name, provider_config in providers.items():
        models = provider_config.get("models", [])
        for model in models:
            result.append({
                "provider": provider_name,
                "model_id": model.get("id", "unknown"),
                "name": model.get("name", model.get("id", "unknown"))
            })
    return result