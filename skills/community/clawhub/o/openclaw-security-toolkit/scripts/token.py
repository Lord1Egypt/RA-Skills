#!/usr/bin/env python3
"""
OpenClaw Security Guard - Token Manager
Manage authentication tokens.
"""

import json
import secrets
import string
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from utils import (
    OPENCLAW_DIR, CONFIG_FILE, load_config, Colors
)


def get_token_info() -> Dict:
    """Get token information."""
    config = load_config()
    gateway = config.get("gateway", {})
    auth = gateway.get("auth", {})
    token = auth.get("token", "")

    if not token:
        return {
            "exists": False,
            "length": 0,
            "strength": "none",
            "entropy": 0
        }

    # Analyze token
    length = len(token)
    charset = set(token)

    # Calculate entropy
    import math
    charset_size = 0
    if any(c.islower() for c in token):
        charset_size += 26
    if any(c.isupper() for c in token):
        charset_size += 26
    if any(c.isdigit() for c in token):
        charset_size += 10
    if any(c in string.punctuation for c in token):
        charset_size += len(string.punctuation)

    entropy = length * math.log2(max(charset_size, 1)) if charset_size > 0 else 0

    # Determine strength
    if length >= 32 and entropy >= 128:
        strength = "strong"
    elif length >= 24 and entropy >= 96:
        strength = "good"
    elif length >= 16:
        strength = "moderate"
    else:
        strength = "weak"

    return {
        "exists": True,
        "length": length,
        "strength": strength,
        "entropy": round(entropy, 1),
        "charset_size": charset_size,
        "has_lowercase": any(c.islower() for c in token),
        "has_uppercase": any(c.isupper() for c in token),
        "has_digits": any(c.isdigit() for c in token),
        "has_special": any(c in string.punctuation for c in token)
    }


def generate_token(length: int = 32) -> str:
    """Generate a secure random token."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def rotate_token(new_token: str = None, length: int = 32) -> Dict:
    """
    Rotate the authentication token.

    Args:
        new_token: Optional new token to use. If not provided, generates one.
        length: Length of token to generate if new_token not provided.

    Returns:
        Dict with old and new token info.
    """
    if not CONFIG_FILE.exists():
        return {"error": "Config file not found"}

    # Read current config
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    old_token = config.get("gateway", {}).get("auth", {}).get("token", "")

    # Generate new token if not provided
    if new_token is None:
        new_token = generate_token(length)

    # Update config
    if "gateway" not in config:
        config["gateway"] = {}
    if "auth" not in config["gateway"]:
        config["gateway"]["auth"] = {}

    config["gateway"]["auth"]["token"] = new_token
    config["gateway"]["auth"]["mode"] = "token"

    # Write back
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    return {
        "success": True,
        "old_token_length": len(old_token) if old_token else 0,
        "new_token": new_token,
        "new_token_length": len(new_token),
        "message": "Token rotated successfully. Restart gateway for changes to take effect."
    }


def print_token_status(info: Dict, i18n: Dict):
    """Print token status information."""
    print()

    if not info["exists"]:
        print(f"{Colors.RED}❌ No token configured{Colors.RESET}")
        print(f"\n  Run with --generate to create a new token")
        return

    # Strength color
    strength = info["strength"]
    if strength == "strong":
        color = Colors.GREEN
        emoji = "✅"
    elif strength == "good":
        color = Colors.GREEN
        emoji = "✅"
    elif strength == "moderate":
        color = Colors.YELLOW
        emoji = "⚠️"
    else:
        color = Colors.RED
        emoji = "🔴"

    print(f"{Colors.BOLD}🔑 Token Status{Colors.RESET}\n")
    print(f"  Strength: {color}{emoji} {strength.upper()}{Colors.RESET}")
    print(f"  Length: {info['length']} characters")
    print(f"  Entropy: {info['entropy']} bits")
    print()

    # Character composition
    print(f"{Colors.BOLD}📋 Character Composition{Colors.RESET}\n")
    print(f"  Lowercase: {'✅' if info['has_lowercase'] else '❌'}")
    print(f"  Uppercase: {'✅' if info['has_uppercase'] else '❌'}")
    print(f"  Digits: {'✅' if info['has_digits'] else '❌'}")
    print(f"  Special: {'✅' if info['has_special'] else '❌'}")
    print()

    # Recommendations
    if strength in ["weak", "moderate"]:
        print(f"{Colors.YELLOW}💡 Recommendation: Consider rotating to a stronger token{Colors.RESET}")
        print(f"   Run: openclaw-security token rotate")


if __name__ == "__main__":
    info = get_token_info()
    print(json.dumps(info, indent=2))