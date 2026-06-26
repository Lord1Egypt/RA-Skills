"""
Nex Keyring - Scanner Module
Environment and .env file scanning for API keys and secrets.
"""

import hashlib
import os
import re
from pathlib import Path
from typing import List, Dict, Optional

from .config import SERVICE_PATTERNS, SERVICE_PRESETS


def hash_key(key_value: str) -> str:
    """Generate SHA256 hash of key for change detection."""
    return hashlib.sha256(key_value.encode()).hexdigest()


def detect_service(key_name: str) -> str:
    """
    Detect service from environment variable name.
    Returns service name or 'other' if not recognized.
    """
    key_upper = key_name.upper()

    for service, patterns in SERVICE_PATTERNS.items():
        for pattern in patterns:
            if pattern in key_upper:
                return service

    return "other"


def scan_env_file(path: str) -> List[Dict[str, str]]:
    """
    Scan .env file and extract key names and metadata.
    Returns list of dicts with key name, service, and whether it has a value.
    Security: Does NOT extract actual key values.
    """
    env_path = Path(path)

    if not env_path.exists():
        return []

    found_keys = []

    try:
        with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue

                # Parse key=value
                if "=" not in line:
                    continue

                key_name, _, value = line.partition("=")
                key_name = key_name.strip()
                value = value.strip()

                # Skip if not a valid key name
                if not key_name or not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key_name):
                    continue

                service = detect_service(key_name)

                found_keys.append({
                    "name": key_name,
                    "service": service,
                    "has_value": bool(value.strip()),
                    "line": line_num,
                    "file": str(env_path),
                })

    except Exception as e:
        print(f"Error scanning {path}: {e}", flush=True)

    return found_keys


def scan_env_vars() -> List[Dict[str, str]]:
    """
    Scan current environment variables for known API key patterns.
    Returns list of detected keys.
    """
    found_keys = []

    for key_name in os.environ.keys():
        # Skip common system variables
        if any(x in key_name for x in ["PATH", "HOME", "USER", "SHELL", "TERM", "LANG"]):
            continue

        service = detect_service(key_name)

        # Only include if detected as a known service or contains suspicious keywords
        if service != "other" or any(x in key_name.lower() for x in ["secret", "key", "token", "password", "api"]):
            found_keys.append({
                "name": key_name,
                "service": service,
                "has_value": bool(os.environ.get(key_name)),
            })

    return found_keys


def check_key_rotation(secret: Dict[str, any]) -> Dict[str, any]:
    """
    Check if a key needs rotation based on its policy.
    Returns dict with rotation status and recommendations.
    """
    from datetime import datetime, timedelta

    now = datetime.now()
    policy_days = secret.get("rotation_policy_days", 90)
    last_rotated = secret.get("last_rotated")
    created_date = secret.get("created_date")

    result = {
        "needs_rotation": False,
        "days_since_rotation": 0,
        "risk_level": "OK",
        "recommendation": "Current rotation status is acceptable.",
    }

    if last_rotated:
        try:
            last_date = datetime.fromisoformat(last_rotated)
            days_since = (now - last_date).days
            result["days_since_rotation"] = days_since

            if days_since > policy_days:
                result["needs_rotation"] = True
                result["recommendation"] = f"Key is overdue for rotation by {days_since - policy_days} days."

            # Determine risk level
            if days_since < 30:
                result["risk_level"] = "FRESH"
            elif days_since < 90:
                result["risk_level"] = "OK"
            elif days_since < 180:
                result["risk_level"] = "STALE"
            else:
                result["risk_level"] = "CRITICAL"

        except ValueError:
            pass

    elif created_date:
        try:
            created = datetime.fromisoformat(created_date)
            days_since = (now - created).days
            result["days_since_rotation"] = days_since

            if days_since > policy_days:
                result["needs_rotation"] = True
                result["recommendation"] = f"Key was created {days_since} days ago and has never been rotated."

            # Risk level when never rotated
            if days_since < 30:
                result["risk_level"] = "FRESH"
            elif days_since < 90:
                result["risk_level"] = "OK"
            elif days_since < 180:
                result["risk_level"] = "STALE"
            else:
                result["risk_level"] = "CRITICAL"

        except ValueError:
            pass

    return result


def bulk_check(secrets: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """
    Check all secrets for rotation status.
    Returns list of status reports.
    """
    report = []

    for secret in secrets:
        check_result = check_key_rotation(secret)
        report.append({
            "name": secret.get("name"),
            "service": secret.get("service"),
            "category": secret.get("category"),
            **check_result
        })

    return report
