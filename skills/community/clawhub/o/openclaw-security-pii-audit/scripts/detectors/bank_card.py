"""Bank card number detector with Luhn algorithm validation."""

import re
from .base import BaseDetector, Match


class BankCardDetector(BaseDetector):
    label = "BANK_CARD"

    # Formatted: groups of 4 digits separated by space or dash
    FORMATTED = re.compile(r'(?<!\d)(\d{4}[\s\-]\d{4}[\s\-]\d{4}[\s\-]?\d{1,7})(?!\d)')
    # Continuous: 13-19 digit sequence
    CONTINUOUS = re.compile(r'(?<!\d)(\d{13,19})(?!\d)')

    @staticmethod
    def _luhn_check(number):
        """Validate card number using Luhn algorithm."""
        digits = [int(d) for d in number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for d in even_digits:
            d *= 2
            total += d - 9 if d > 9 else d
        return total % 10 == 0

    def detect(self, text):
        matches = []
        seen = set()

        for pattern in [self.FORMATTED, self.CONTINUOUS]:
            for m in pattern.finditer(text):
                raw = m.group()
                clean = re.sub(r'[\s\-]', '', raw)
                if not clean.isdigit():
                    continue
                if len(clean) < 13 or len(clean) > 19:
                    continue
                if clean in seen:
                    continue
                seen.add(clean)

                if self._luhn_check(clean):
                    matches.append(Match(
                        label=self.label,
                        confidence=0.92,
                        masked_preview=clean[:2] + ' **** **** **** ' + clean[-2:],
                        start=m.start(),
                        end=m.end(),
                    ))
        return matches
