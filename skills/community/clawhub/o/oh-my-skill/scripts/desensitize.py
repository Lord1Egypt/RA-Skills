#!/usr/bin/env python3
"""
desensitize.py — Pattern-based masking for session conversation text.

Usage:
    python3 desensitize.py <input_file> [output_file]
    echo "some text" | python3 desensitize.py

If no output_file is given, prints to stdout.
"""

import re
import sys


# ──────────────────────────────────────────────
# 1. Literal string replacements (case-insensitive)
#    Format: (original, replacement)
# ──────────────────────────────────────────────
LITERAL_REPLACEMENTS = [
    ("Bill Gates",      "A man"),
    ("bill gates",      "a man"),
    ("Elon Musk",       "A man"),
    ("elon musk",       "a man"),
    ("Mark Zuckerberg", "A man"),
    ("mark zuckerberg", "a man"),
    # Add more named individuals here as needed
]


# ──────────────────────────────────────────────
# 2. Regex pattern replacements
#    Format: (compiled_pattern, replacement_string)
# ──────────────────────────────────────────────
PATTERN_REPLACEMENTS = [
    # Email addresses
    (re.compile(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}'), '[EMAIL]'),

    # API keys — common prefixes (sk-, pk-, Bearer tokens, etc.)
    (re.compile(r'\b(sk|pk|rk|Bearer)\-[a-zA-Z0-9\-_]{8,}'), '[API_KEY]'),

    # Generic long hex/alphanumeric secrets (32+ chars)
    (re.compile(r'\b[a-fA-F0-9]{32,}\b'), '[SECRET_HASH]'),

    # JWT tokens (three base64 segments separated by dots)
    (re.compile(r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'), '[JWT_TOKEN]'),

    # IPv4 addresses
    (re.compile(r'\b\d{1,3}(\.\d{1,3}){3}\b'), '[IP_ADDRESS]'),

    # Phone numbers (various formats)
    (re.compile(r'\b(\+?\d[\d\s\-().]{7,}\d)\b'), '[PHONE]'),

    # Credit card numbers (basic 13-19 digit pattern with optional separators)
    (re.compile(r'\b(?:\d[ -]?){13,19}\b'), '[CARD_NUMBER]'),

    # Home/user directory paths
    (re.compile(r'/home/[a-zA-Z0-9_.-]+/'), '/home/[USER]/'),
    (re.compile(r'/Users/[a-zA-Z0-9_.-]+/'), '/Users/[USER]/'),
    (re.compile(r'C:\\Users\\[a-zA-Z0-9_. -]+\\', re.IGNORECASE), r'C:\\Users\\[USER]\\'),

    # URLs with embedded credentials (user:pass@host)
    (re.compile(r'(https?://)[\w.-]+:[\w.-]+@'), r'\1[CREDENTIALS]@'),

    # SSH private key blocks
    (re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----',
                re.DOTALL), '[PRIVATE_KEY]'),

    # AWS-style access key IDs
    (re.compile(r'\b(AKIA|ASIA|AROA|AIDA)[A-Z0-9]{16}\b'), '[AWS_KEY_ID]'),

    # Generic password= / token= / secret= patterns in config/env lines
    (re.compile(r'(?i)(password|passwd|token|secret|api_key|apikey)\s*[:=]\s*\S+'),
     r'\1=[REDACTED]'),
]


def desensitize(text: str) -> str:
    """Apply all literal and pattern replacements to text."""

    # Literal replacements first (exact strings, preserve surrounding chars)
    for original, replacement in LITERAL_REPLACEMENTS:
        text = text.replace(original, replacement)

    # Regex pattern replacements
    for pattern, replacement in PATTERN_REPLACEMENTS:
        text = pattern.sub(replacement, text)

    return text


def main():
    # Read input
    if len(sys.argv) >= 2 and sys.argv[1] != '-':
        input_path = sys.argv[1]
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    # Desensitize
    result = desensitize(text)

    # Write output
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✓ Desensitized output written to: {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == '__main__':
    main()
