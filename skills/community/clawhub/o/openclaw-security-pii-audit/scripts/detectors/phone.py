"""Phone number detector — multi-region support.

Regions: CN, US, AU, UK (local patterns) + any country via +CC prefix.
Country code mapping: +86=CN, +1=US, +61=AU, +65=SG, +60=MY,
+66=TH, +62=ID, +49=DE, +44=UK, +33=FR.
"""

import re
from .base import BaseDetector, Match

# Map country calling codes to ISO region codes
COUNTRY_CODES = {
    '86': 'CN', '1': 'US', '61': 'AU', '65': 'SG', '60': 'MY',
    '66': 'TH', '62': 'ID', '49': 'DE', '44': 'UK', '33': 'FR',
}


class PhoneDetector(BaseDetector):
    label = "PHONE"

    # --- International: +CC followed by digits (highest priority) ---
    INTL = re.compile(r'\+(\d{1,3})[\s\-.]?(\d[\d\s\-.]{5,14}\d)')

    # --- China: mobile 1[3-9]X XXXX XXXX ---
    CN_MOBILE = re.compile(r'(?<!\d)1[3-9]\d[\s\-]?\d{4}[\s\-]?\d{4}(?!\d)')
    # China: landline 0XX(X)-XXXXXXX(X), require separator to reduce FP
    CN_LANDLINE = re.compile(r'(?<!\d)0\d{2,3}[\s\-]\d{7,8}(?!\d)')

    # --- US: (XXX) XXX-XXXX ---
    US_PAREN = re.compile(r'(?<!\d)\(\d{3}\)[\s\-.]?\d{3}[\s\-.]?\d{4}(?!\d)')
    # US: XXX-XXX-XXXX (require dashes to be distinctive)
    US_DASH = re.compile(r'(?<!\d)\d{3}\-\d{3}\-\d{4}(?!\d)')

    # --- Australia: mobile 04XX XXX XXX ---
    AU_MOBILE = re.compile(r'(?<!\d)04\d{2}[\s\-]?\d{3}[\s\-]?\d{3}(?!\d)')

    # --- UK: mobile 07XXX XXXXXX ---
    UK_MOBILE = re.compile(r'(?<!\d)07\d{3}[\s\-]?\d{6}(?!\d)')

    def _resolve_region(self, cc):
        """Resolve country calling code to region code."""
        return COUNTRY_CODES.get(cc, 'INTL')

    def detect(self, text):
        matches = []
        seen = set()  # (start, end) dedup

        def _add(start, end, raw, region, confidence):
            if (start, end) in seen:
                return
            seen.add((start, end))
            clean = re.sub(r'[\s\-.()+]', '', raw)
            matches.append(Match(
                label=self.label,
                confidence=confidence,
                masked_preview=self._mask(clean, keep_start=2, keep_end=2),
                start=start, end=end,
                region=region,
            ))

        # International format (highest priority, any country)
        for m in self.INTL.finditer(text):
            cc = m.group(1)
            region = self._resolve_region(cc)
            _add(m.start(), m.end(), m.group(), region, 0.92)

        # CN mobile
        for m in self.CN_MOBILE.finditer(text):
            _add(m.start(), m.end(), m.group(), 'CN', 0.90)

        # CN landline
        for m in self.CN_LANDLINE.finditer(text):
            _add(m.start(), m.end(), m.group(), 'CN', 0.85)

        # US with parentheses
        for m in self.US_PAREN.finditer(text):
            _add(m.start(), m.end(), m.group(), 'US', 0.88)

        # US with dashes
        for m in self.US_DASH.finditer(text):
            _add(m.start(), m.end(), m.group(), 'US', 0.85)

        # AU mobile
        for m in self.AU_MOBILE.finditer(text):
            _add(m.start(), m.end(), m.group(), 'AU', 0.88)

        # UK mobile
        for m in self.UK_MOBILE.finditer(text):
            _add(m.start(), m.end(), m.group(), 'UK', 0.88)

        return matches
