#!/usr/bin/env python3
"""
redact.py — PII redaction utility for UXR Observer.

Reads JSON from stdin (expects objects with "text" fields, or a list of session objects),
applies PII redaction, and writes the redacted JSON to stdout.

Supports two input modes:
  1. A single object with a "text" field
  2. A list of session objects (from collect.sh output) — redacts all message text fields

Redaction targets:
  - Email addresses → [EMAIL]
  - Phone numbers → [PHONE]
  - API keys / tokens → [API_KEY]
  - File paths containing usernames → [PATH]
  - IP addresses → [IP]
  - Proper names (heuristic) → [NAME]
"""

import json
import re
import sys
import os


# --- Regex patterns ---

EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b'
)

PHONE_PATTERN = re.compile(
    r'(?<!\d)'
    r'(?:\+?1[-.\s]?)?'
    r'(?:\(?\d{3}\)?[-.\s]?)'
    r'\d{3}[-.\s]?\d{4}'
    r'(?!\d)'
)

# Matches common API key / token patterns: long hex strings, base64-ish tokens,
# sk-xxx, pk-xxx, ghp_xxx, gho_xxx, Bearer tokens, etc.
API_KEY_PATTERNS = [
    re.compile(r'\b(?:sk|pk|api|key|token|secret|password|bearer)[-_]?[A-Za-z0-9\-_]{20,}\b', re.IGNORECASE),
    re.compile(r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b'),
    re.compile(r'\b(?:xox[bpas])-[A-Za-z0-9\-]{10,}\b'),
    re.compile(r'\bAIza[A-Za-z0-9\-_]{35}\b'),
    re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    re.compile(r'\b[A-Fa-f0-9]{40}\b'),  # SHA-1 / generic hex tokens
    re.compile(r'\beyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_.+/=]+\b'),  # JWT
]

IP_PATTERN = re.compile(
    r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
)

# File paths that contain a username segment (e.g., /Users/john/, /home/jane/, C:\Users\Bob\)
USERNAME_PATH_PATTERN = re.compile(
    r'(?:/(?:Users|home)/[A-Za-z0-9._\-]+(?:/[^\s,;\"\')\]}>]*)?)|'
    r'(?:[A-Z]:\\Users\\[A-Za-z0-9._\-]+(?:\\[^\s,;\"\')\]}>]*)?)'
)

# Heuristic name detection: capitalized word sequences that look like names.
# We use a conservative approach — 2-3 capitalized words in sequence, not at sentence start.
NAME_PATTERN = re.compile(
    r'(?:^|(?<=\s)|(?<=,)|(?<=;)|(?<=:)|(?<=!))'  # preceded by space/punctuation/start
    r'(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)?\s?'
    r'([A-Z][a-z]{1,15}(?:\s[A-Z][a-z]{1,15}){1,2})'
    r'(?=[\s,;:!?.\'\"]|$)'
)

# Common words that look like names but aren't (to reduce false positives)
NAME_ALLOWLIST = {
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December",
    "New York", "San Francisco", "Los Angeles", "United States", "United Kingdom",
    "Open Source", "Visual Studio", "Machine Learning", "Deep Learning",
    "Stack Overflow", "Pull Request", "Merge Request", "Code Review",
    "Hello World", "Thank You", "No Problem", "Good Morning", "Good Evening",
    "Type Script", "Java Script", "Next Js",
    "The End", "In Progress", "To Do", "In Review",
}


def redact_text(text: str) -> str:
    """Apply all PII redaction rules to a text string."""
    if not text or not isinstance(text, str):
        return text

    # Order matters: do API keys first (longer patterns), then emails, then others

    # API keys / tokens
    for pattern in API_KEY_PATTERNS:
        text = pattern.sub("[API_KEY]", text)

    # Email addresses
    text = EMAIL_PATTERN.sub("[EMAIL]", text)

    # Phone numbers
    text = PHONE_PATTERN.sub("[PHONE]", text)

    # IP addresses (but not version numbers like 2.0.1)
    def replace_ip(match):
        ip = match.group(0)
        parts = ip.split(".")
        # Skip if it looks like a version number (starts with small numbers, short segments)
        if all(int(p) < 30 for p in parts):
            return ip
        return "[IP]"

    text = IP_PATTERN.sub(replace_ip, text)

    # File paths with usernames
    text = USERNAME_PATH_PATTERN.sub("[PATH]", text)

    # Proper names (heuristic — run last to avoid clobbering other replacements)
    def replace_name(match):
        name = match.group(1)
        if name in NAME_ALLOWLIST:
            return match.group(0)
        # Skip if it looks like a code identifier (camelCase following)
        if name and len(name.split()) >= 2:
            return match.group(0).replace(name, "[NAME]")
        return match.group(0)

    text = NAME_PATTERN.sub(replace_name, text)

    return text


def redact_session_data(data):
    """Recursively redact PII in session data structures."""
    if isinstance(data, str):
        return redact_text(data)
    elif isinstance(data, list):
        return [redact_session_data(item) for item in data]
    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key in ("text", "content_preview"):
                result[key] = redact_text(value) if isinstance(value, str) else value
            elif key == "messages":
                result[key] = redact_session_data(value)
            elif key == "tool_calls":
                result[key] = redact_session_data(value)
            else:
                result[key] = value
        return result
    else:
        return data


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            print("{}")
            return

        data = json.loads(raw)
        redacted = redact_session_data(data)
        print(json.dumps(redacted, indent=2, ensure_ascii=False))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Redaction failed: {e}"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
