"""Person name detector — multi-region, context-keyword gated.

CN: Chinese name (2-4 characters) after/before context keywords.
INTL: Western name (First Last) after context keywords.
All detections require keyword context to reduce false positives.
"""

import re
from .base import BaseDetector, Match


class PersonNameDetector(BaseDetector):
    label = "PERSON_NAME"

    # ---- CN: keyword before name ----
    CN_BEFORE = re.compile(
        r'(?:姓名|名字|收件人|联系人|持卡人|户名|开户人|患者|被告|原告|当事人)'
        r'[：:\s]*'
        r'([\u4e00-\u9fff]{2,4})',
    )
    # CN: name followed by honorific title
    CN_AFTER_TITLE = re.compile(
        r'([\u4e00-\u9fff]{2,4})'
        r'(?:先生|女士|同志|老师|教授|医生|律师)',
    )

    # ---- Multi-language keyword + name ----
    # Structured: "Name:" / "姓名：" + value (CN or Western)
    STRUCTURED_CN = re.compile(
        r'(?:name|姓名|收件人|联系人|持卡人|户名)'
        r'[\s：:=]*'
        r'([\u4e00-\u9fff]{2,4})',
        re.IGNORECASE
    )
    STRUCTURED_WESTERN = re.compile(
        r'(?:name|full\s*name|recipient|account\s*holder|customer|passenger|patient)'
        r'[\s：:=]*'
        r'([A-Z][a-z]{1,15}\s[A-Z][a-z]{1,15}(?:\s[A-Z][a-z]{1,15})?)',
        re.IGNORECASE
    )

    # ---- Western name after title (Mr./Mrs./Ms./Dr./Prof.) ----
    WESTERN_TITLE = re.compile(
        r'(?:Mr\.?|Mrs\.?|Ms\.?|Miss|Dr\.?|Prof\.?)\s+'
        r'([A-Z][a-z]{1,15}\s[A-Z][a-z]{1,15}(?:\s[A-Z][a-z]{1,15})?)'
    )

    # ---- DE/FR name keywords ----
    DE_NAME = re.compile(
        r'(?:Name|Vorname|Nachname|Inhaber|Empf[aä]nger)'
        r'[\s：:=]*'
        r'([A-Z\u00c0-\u00ff][a-z\u00e0-\u00ff]{1,15}\s'
        r'[A-Z\u00c0-\u00ff][a-z\u00e0-\u00ff]{1,15})',
        re.IGNORECASE
    )
    FR_NAME = re.compile(
        r'(?:nom|pr[eé]nom|destinataire|titulaire)'
        r'[\s：:=]*'
        r'([A-Z\u00c0-\u00ff][a-z\u00e0-\u00ff]{1,15}\s'
        r'[A-Z\u00c0-\u00ff][a-z\u00e0-\u00ff]{1,15})',
        re.IGNORECASE
    )

    def _mask_name(self, name):
        """Mask name: keep first char, mask the rest."""
        parts = name.split()
        if len(parts) >= 2:
            return parts[0][0] + '***' + ' ' + parts[-1][0] + '***'
        return name[0] + '*' * (len(name) - 1)

    def detect(self, text):
        matches = []
        seen = set()

        def _add(name, start, end, region, confidence):
            if name in seen:
                return
            seen.add(name)
            if len(name) <= 1:
                return
            masked = self._mask_name(name)
            matches.append(Match(
                label=self.label, confidence=confidence,
                masked_preview=masked, start=start, end=end,
                region=region,
            ))

        # CN patterns
        for pat in [self.CN_BEFORE, self.CN_AFTER_TITLE, self.STRUCTURED_CN]:
            for m in pat.finditer(text):
                _add(m.group(1), m.start(1), m.end(1), 'CN', 0.70)

        # Western structured (English keyword + First Last)
        for m in self.STRUCTURED_WESTERN.finditer(text):
            _add(m.group(1), m.start(1), m.end(1), 'INTL', 0.72)

        # Western title prefix (Mr./Mrs./Dr. + name)
        for m in self.WESTERN_TITLE.finditer(text):
            _add(m.group(1), m.start(1), m.end(1), 'INTL', 0.75)

        # DE name patterns
        for m in self.DE_NAME.finditer(text):
            _add(m.group(1), m.start(1), m.end(1), 'DE', 0.70)

        # FR name patterns
        for m in self.FR_NAME.finditer(text):
            _add(m.group(1), m.start(1), m.end(1), 'FR', 0.70)

        return matches
