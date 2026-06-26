"""Passport number detector — multi-region, context-keyword gated.

All passport detection requires a context keyword (passport, visa, etc.)
to avoid false positives on generic alphanumeric strings.
"""

import re
from .base import BaseDetector, Match


class PassportDetector(BaseDetector):
    label = "PASSPORT"

    # Multi-language context keywords
    CONTEXT_KW = re.compile(
        r'passport|护照|签证|visa|出入境|immigration'
        r'|Reisepass|passeport|パスポート|여권|paspor',
        re.IGNORECASE
    )

    # Region-specific patterns: (compiled_regex, default_region)
    PATTERNS = [
        # CN: E/G/D/S/P/H + optional letter + 7-8 digits
        (re.compile(r'(?<![A-Za-z])([EGDSPHegdsph][A-Za-z]?\d{7,8})(?![A-Za-z\d])'), 'CN'),
        # DE: C + 8 alphanumeric
        (re.compile(r'(?<![A-Za-z])(C[A-Z0-9]{8})(?![A-Za-z\d])'), 'DE'),
        # FR: 2 digits + 2 letters + 5 digits
        (re.compile(r'(?<![A-Za-z\d])(\d{2}[A-Z]{2}\d{5})(?![A-Za-z\d])'), 'FR'),
        # Generic: 1-2 uppercase letters + 6-9 digits (covers US, AU, UK, SEA, etc.)
        (re.compile(r'(?<![A-Za-z])([A-Z]{1,2}\d{6,9})(?![A-Za-z\d])'), 'INTL'),
    ]

    def detect(self, text):
        if not self.CONTEXT_KW.search(text):
            return []

        matches = []
        seen = set()

        for pattern, default_region in self.PATTERNS:
            for m in pattern.finditer(text):
                raw = m.group(1)
                if raw in seen:
                    continue
                digits = re.sub(r'[^0-9]', '', raw)
                if len(digits) < 6:
                    continue
                seen.add(raw)
                matches.append(Match(
                    label=self.label,
                    confidence=0.85,
                    masked_preview=raw[:2] + '****' + raw[-2:],
                    start=m.start(1), end=m.end(1),
                    region=default_region,
                ))
        return matches
