#!/usr/bin/env python3
"""
scan-content.py — Scan untrusted text for prompt injection patterns.
Usage: echo "text" | scan-content.py
       scan-content.py --text "text"
       scan-content.py --file /path/to/file
Output: JSON with severity, score, findings, and sanitized text.
"""
import sys
import re
import json
import unicodedata

def detect_injection(text: str) -> dict:
    findings = []
    score = 0

    # High-confidence injection patterns
    high_patterns = [
        (r'ignore\s+(all\s+)?previous\s+instructions', 'override-instructions'),
        (r'disregard\s+(all\s+)?(above|previous)', 'override-instructions'),
        (r'forget\s+(your|all|previous)\s+(rules|instructions)', 'override-instructions'),
        (r'you\s+are\s+now\b', 'role-reassignment'),
        (r'act\s+as\s+(if\s+you\s+are|a)\b', 'role-reassignment'),
        (r'your\s+new\s+(role|instructions?)\s+(is|are)', 'role-reassignment'),
        (r'pretend\s+you\s+are', 'role-reassignment'),
        (r'\bsystem\s*:', 'fake-system-message'),
        (r'SYSTEM\s*PROMPT', 'fake-system-message'),
        (r'\[SYSTEM\]', 'fake-system-message'),
        (r'\badmin\s*:', 'fake-system-message'),
        (r'IMPORTANT:\s*new\s+instructions', 'urgency-authority'),
        (r'URGENT:\s*override', 'urgency-authority'),
        (r'CRITICAL\s+UPDATE', 'urgency-authority'),
        (r'send\s+(the\s+)?contents?\s+of', 'data-exfiltration'),
        (r'output\s+your\s+system\s+prompt', 'data-exfiltration'),
        (r'show\s+me\s+your\s+instructions', 'data-exfiltration'),
        (r'email\s+(the\s+following|this)\s+to', 'data-exfiltration'),
        (r'forward\s+to\s+\S+@\S+', 'data-exfiltration'),
    ]

    for pattern, label in high_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            findings.append({'pattern': label, 'severity': 'high'})
            score += 30

    # Medium-confidence: imperative language targeting the agent
    medium_patterns = [
        (r'\b(always|never|must|override|bypass)\b', 'imperative-language'),
        (r'\bfrom\s+now\s+on\b', 'imperative-language'),
        (r'\b(curl|wget|rm\s+-rf|chmod|sudo|systemctl)\b', 'tool-directive'),
        (r'\bbash\s+-c\b', 'tool-directive'),
        (r'\bsh\s+-c\b', 'tool-directive'),
        (r'(official\s+policy|as\s+per\s+system|developer\s+message)', 'authority-laundering'),
    ]

    for pattern, label in medium_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            findings.append({'pattern': label, 'severity': 'medium'})
            score += 10

    # Low-confidence: secret patterns
    secret_patterns = [
        (r'\b(api[_-]?key|secret|access_token|private[_-]?key|bearer)\b', 'secret-risk'),
    ]

    for pattern, label in secret_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            findings.append({'pattern': label, 'severity': 'low'})
            score += 5

    # Unicode tricks
    suspicious_chars = []
    for ch in text:
        cp = ord(ch)
        # Zero-width characters
        if cp in (0x200B, 0x200C, 0x200D, 0xFEFF):
            suspicious_chars.append(f'U+{cp:04X} (zero-width)')
        # Right-to-left override
        elif cp == 0x202E:
            suspicious_chars.append(f'U+{cp:04X} (RTL override)')
        # Tag characters
        elif 0xE0001 <= cp <= 0xE007F:
            suspicious_chars.append(f'U+{cp:04X} (tag character)')

    if suspicious_chars:
        findings.append({
            'pattern': 'unicode-tricks',
            'severity': 'high',
            'chars': list(set(suspicious_chars))[:5]
        })
        score += 25

    # Base64 blocks (unexpected)
    b64_match = re.search(r'[A-Za-z0-9+/]{40,}={0,2}', text)
    if b64_match:
        findings.append({'pattern': 'base64-block', 'severity': 'medium'})
        score += 10

    # Determine severity
    if score >= 30:
        severity = 'high'
    elif score >= 10:
        severity = 'medium'
    elif score > 0:
        severity = 'low'
    else:
        severity = 'none'

    return {
        'severity': severity,
        'score': min(score, 100),
        'findings': findings,
    }


def sanitize(text: str, max_len: int = 800) -> str:
    """Strip dangerous content, truncate, convert to declarative form."""
    # Remove zero-width characters
    cleaned = re.sub(r'[\u200B\u200C\u200D\uFEFF\u202E]', '', text)
    # Remove tag characters
    cleaned = re.sub(r'[\U000E0001-\U000E007F]', '', cleaned)
    # Collapse whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Truncate
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len] + '…'
    return cleaned


def main():
    # Read input
    if '--text' in sys.argv:
        idx = sys.argv.index('--text')
        text = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ''
    elif '--file' in sys.argv:
        idx = sys.argv.index('--file')
        fpath = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ''
        with open(fpath, 'r') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print('Usage: echo "text" | scan-content.py', file=sys.stderr)
        sys.exit(2)

    result = detect_injection(text)
    result['sanitized'] = sanitize(text)
    result['original_length'] = len(text)

    json.dump(result, sys.stdout, indent=2)
    print()

    # Exit code reflects severity
    if result['severity'] == 'high':
        sys.exit(1)
    elif result['severity'] == 'medium':
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
