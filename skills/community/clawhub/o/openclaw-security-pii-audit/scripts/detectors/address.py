"""Address detector — multi-region support.

CN: Structural province/city/district patterns + keyword-gated.
US: State abbreviation + ZIP code anchor.
AU: State abbreviation + 4-digit postcode.
UK: Distinctive postcode format (e.g. SW1A 1AA).
DE/FR: Keyword-gated with postal code patterns.
SEA: Keyword-gated only.
"""

import re
from .base import BaseDetector, Match

# US state abbreviations
_US_STATES = (
    'AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI'
    '|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX'
    '|UT|VT|VA|WA|WV|WI|WY|DC'
)

# AU state abbreviations
_AU_STATES = 'NSW|VIC|QLD|WA|SA|TAS|ACT|NT'


class AddressDetector(BaseDetector):
    label = "ADDRESS"

    # ---- Multi-language address keyword ----
    ADDR_KW = re.compile(
        r'address|地址|住址|收货地址|寄送地址|通讯地址'
        r'|Adresse|adresse|alamat|ที่อยู่|住所',
        re.IGNORECASE
    )

    # ---- CN: keyword-gated ----
    CN_KEYWORD = re.compile(
        r'(?:地址|住址|收货地址|寄送地址|通讯地址|address)'
        r'[：:\s]*'
        r'([\u4e00-\u9fff\w\d\-\u2014#\u53f7\u697c\u680b\u5355\u5143'
        r'\u5ba4\u5c42\u5e62\u5f04\u5df7\u8def\u8857\u9053\u533a\u53bf'
        r'\u5e02\u7701]{8,60})',
        re.IGNORECASE
    )
    # CN: Province + City structural
    CN_PROVINCIAL = re.compile(
        r'([\u4e00-\u9fff]{2,6}(?:\u7701|\u81ea\u6cbb\u533a)'
        r'[\u4e00-\u9fff]{2,10}(?:\u5e02|\u5dde|\u76df)'
        r'[\u4e00-\u9fff\w\d\-\u2014#\u53f7\u697c\u680b\u5355\u5143'
        r'\u5ba4\u5c42\u5e62\u5f04\u5df7\u8def\u8857\u9053\u533a\u53bf]{4,40})'
    )
    # CN: Direct-controlled municipalities
    CN_MUNICIPAL = re.compile(
        r'((?:\u5317\u4eac|\u4e0a\u6d77|\u5929\u6d25|\u91cd\u5e86)\u5e02?'
        r'[\u4e00-\u9fff]{2,6}(?:\u533a|\u53bf)'
        r'[\u4e00-\u9fff\w\d\-\u2014#\u53f7\u697c\u680b\u5355\u5143'
        r'\u5ba4\u5c42\u5e62\u5f04\u5df7\u8def\u8857\u9053]{4,30})'
    )

    # ---- US: street + state abbreviation + ZIP ----
    US_ADDR = re.compile(
        r'(\d{1,6}\s[\w\s.]{3,40},?\s*(?:' + _US_STATES + r')\s+\d{5}(?:\-\d{4})?)',
        re.IGNORECASE
    )

    # ---- AU: street + state + 4-digit postcode ----
    AU_ADDR = re.compile(
        r'(\d{1,5}\s[\w\s.]{3,40},?\s*(?:' + _AU_STATES + r')\s+\d{4})',
        re.IGNORECASE
    )

    # ---- UK: postcode pattern (very distinctive) ----
    UK_POSTCODE = re.compile(
        r'\b([A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b'
    )

    # ---- DE: street + PLZ (5-digit postal code) ----
    DE_ADDR = re.compile(
        r'([\w\s\-\.]+(?:stra[sß]e|str\.|weg|platz|gasse|allee)'
        r'\s*\d{1,5}[\w\s,]*\d{5}\s+[\w\s\-]+)',
        re.IGNORECASE
    )

    # ---- FR: number + street type + code postal ----
    FR_ADDR = re.compile(
        r'(\d{1,5}[\s,]+(?:rue|avenue|boulevard|place|chemin|'
        r'all[eé]e|impasse)[\w\s\-\u00e0-\u00ff]+\d{5}\s+[\w\s\-\u00e0-\u00ff]+)',
        re.IGNORECASE
    )

    def _mask_addr(self, addr):
        """Mask address keeping first 4 and last 2 characters."""
        if len(addr) > 6:
            return addr[:4] + '****' + addr[-2:]
        return '****'

    def detect(self, text):
        matches = []
        seen = set()

        def _add(addr, start, end, region, confidence):
            if addr in seen or len(addr) < 8:
                return
            seen.add(addr)
            matches.append(Match(
                label=self.label, confidence=confidence,
                masked_preview=self._mask_addr(addr),
                start=start, end=end, region=region,
            ))

        # CN patterns (no global keyword required — structural is distinctive)
        for m in self.CN_KEYWORD.finditer(text):
            _add(m.group(1), m.start(1), m.end(1), 'CN', 0.78)
        for m in self.CN_PROVINCIAL.finditer(text):
            _add(m.group(1), m.start(1), m.end(1), 'CN', 0.75)
        for m in self.CN_MUNICIPAL.finditer(text):
            _add(m.group(1), m.start(1), m.end(1), 'CN', 0.75)

        # US
        for m in self.US_ADDR.finditer(text):
            _add(m.group(1).strip(), m.start(1), m.end(1), 'US', 0.80)

        # AU
        for m in self.AU_ADDR.finditer(text):
            _add(m.group(1).strip(), m.start(1), m.end(1), 'AU', 0.78)

        # UK postcode (requires address keyword nearby for full confidence)
        has_addr_kw = bool(self.ADDR_KW.search(text))
        for m in self.UK_POSTCODE.finditer(text):
            conf = 0.80 if has_addr_kw else 0.60
            if conf < 0.65:
                continue  # Skip low confidence without keyword
            _add(m.group(1), m.start(1), m.end(1), 'UK', conf)

        # DE (keyword-gated)
        if self.ADDR_KW.search(text):
            for m in self.DE_ADDR.finditer(text):
                _add(m.group(1).strip(), m.start(1), m.end(1), 'DE', 0.75)
            for m in self.FR_ADDR.finditer(text):
                _add(m.group(1).strip(), m.start(1), m.end(1), 'FR', 0.75)

        return matches
