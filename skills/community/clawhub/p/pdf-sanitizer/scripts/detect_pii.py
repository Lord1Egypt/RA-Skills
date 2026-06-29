#!/usr/bin/env python3
"""
PII Detection Script for pdf-sanitizer

Detect sensitive patterns in Chinese & international text.
Usage: python detect_pii.py < input.txt

Output: JSON array of {category, pattern, match, start, end, confidence}
"""

import re
import json
import sys
from typing import List, Dict, Any

def detect_pii(text: str) -> List[Dict[str, Any]]:
    results = []

    patterns = {
        "id_card": (
            r"[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
            "Chinese 18-digit ID Number"
        ),
        "phone": (
            r"(?<!\d)(?:(?:\+?86)?1[3-9]\d{9})(?!\d)",
            "Chinese Mobile Phone"
        ),
        "phone_landline": (
            r"(?<!\d)0\d{2,3}[-\s]?\d{7,8}(?!\d)",
            "Chinese Landline"
        ),
        "bank_card": (
            r"(?<!\d)(?:62|60|58|56|55|54|52|51|50|49|48|46|45|44|43|42|41|40|37|36|35|34|33|32|31|30)\d{14,18}(?!\d)",
            "Bank Card Number"
        ),
        "email": (
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "Email Address"
        ),
        "passport": (
            r"[A-Za-z]\d{8}",
            "Passport Number (CN)"
        ),
        "ipv4": (
            r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)",
            "IPv4 Address"
        ),
    }

    for category, (pattern, desc) in patterns.items():
        for m in re.finditer(pattern, text):
            results.append({
                "category": category,
                "description": desc,
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.95 if category != "ipv4" else 0.6,
            })

    return results


if __name__ == "__main__":
    text = sys.stdin.read()
    results = detect_pii(text)
    print(json.dumps(results, ensure_ascii=False, indent=2))
