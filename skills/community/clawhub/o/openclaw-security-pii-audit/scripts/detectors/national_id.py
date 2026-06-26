"""National ID detector — multi-region support.

Supported:
  CN  - Chinese ID card (18-digit, ISO 7064 checksum)
  US  - Social Security Number (SSN, context-keyword gated)
  AU  - Tax File Number (TFN, 9-digit with check algorithm)
  SG  - NRIC/FIN (letter + 7 digits + check letter)
  MY  - MyKad (12 digits, date + state + seq)
  TH  - Thai National ID (13 digits with check digit)
  ID  - NIK/KTP (16 digits, region + date + seq)
  DE  - Steuer-ID (11 digits, context-keyword gated)
  UK  - National Insurance Number (NIN, context-keyword gated)
  FR  - NIR/INSEE (15 digits with mod-97 check)
"""

import re
from .base import BaseDetector, Match


class NationalIdDetector(BaseDetector):
    label = "NATIONAL_ID"

    # ---- Context keywords per region ----
    CN_KW = re.compile(
        r'身份证|ID\s*card|identity\s*card|居民身份', re.IGNORECASE)
    US_KW = re.compile(
        r'SSN|Social\s*Security|social\s*security\s*number', re.IGNORECASE)
    AU_KW = re.compile(
        r'TFN|Tax\s*File\s*Number|tax\s*file', re.IGNORECASE)
    SG_KW = re.compile(
        r'NRIC|FIN|identity\s*card|IC\s*number', re.IGNORECASE)
    MY_KW = re.compile(
        r'MyKad|IC\s*number|NRIC|kad\s*pengenalan', re.IGNORECASE)
    TH_KW = re.compile(
        r'Thai\s*ID|national\s*ID|บัตรประชาชน|เลขบัตร', re.IGNORECASE)
    ID_KW = re.compile(
        r'NIK|KTP|kartu\s*tanda\s*penduduk', re.IGNORECASE)
    DE_KW = re.compile(
        r'Steuer[\-\s]?ID|Steueridentifikationsnummer|IdNr|Tax\s*ID', re.IGNORECASE)
    UK_KW = re.compile(
        r'NIN|National\s*Insurance|NI\s*number|NINO', re.IGNORECASE)
    FR_KW = re.compile(
        r'NIR|INSEE|num[eé]ro\s*de\s*s[eé]curit[eé]\s*sociale|social\s*security',
        re.IGNORECASE)

    # ---- Patterns ----
    # CN: 6 region + 8 birthday + 3 seq + 1 check
    CN_PAT = re.compile(
        r'(?<!\d)(\d{6})((?:19|20)\d{2})((?:0[1-9]|1[0-2]))'
        r'((?:0[1-9]|[12]\d|3[01]))(\d{3})(\d|X|x)(?!\d)')
    # US SSN: XXX-XX-XXXX (9 digits, with or without separators)
    US_SSN_PAT = re.compile(
        r'(?<!\d)(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{4})(?!\d)')
    # AU TFN: XXX XXX XXX (9 digits)
    AU_TFN_PAT = re.compile(
        r'(?<!\d)(\d{3})[\s\-]?(\d{3})[\s\-]?(\d{3})(?!\d)')
    # SG NRIC/FIN: [STFGM] + 7 digits + check letter
    SG_NRIC_PAT = re.compile(
        r'(?<![A-Za-z])([STFGM]\d{7}[A-Z])(?![A-Za-z])')
    # MY MyKad: XXXXXX-XX-XXXX (12 digits)
    MY_MYKAD_PAT = re.compile(
        r'(?<!\d)(\d{6})[\s\-]?(\d{2})[\s\-]?(\d{4})(?!\d)')
    # TH: 13 digits (optionally formatted X-XXXX-XXXXX-XX-X)
    TH_PAT = re.compile(
        r'(?<!\d)(\d[\s\-]?\d{4}[\s\-]?\d{5}[\s\-]?\d{2}[\s\-]?\d)(?!\d)')
    # ID NIK: 16 consecutive digits
    ID_NIK_PAT = re.compile(r'(?<!\d)(\d{16})(?!\d)')
    # DE Steuer-ID: 11 digits (optionally spaced XX XXX XXX XXX)
    DE_STID_PAT = re.compile(
        r'(?<!\d)(\d{2}[\s]?\d{3}[\s]?\d{3}[\s]?\d{3})(?!\d)')
    # UK NIN: 2 letters + 6 digits + 1 letter (spaces optional)
    UK_NIN_PAT = re.compile(
        r'(?<![A-Za-z])([A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z]'
        r'[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}[\s]?[A-D])(?![A-Za-z])')
    # FR NIR: 15 digits (1/2 sex + year + month + dept + commune + seq + check)
    FR_NIR_PAT = re.compile(
        r'(?<!\d)([12][\s]?\d{2}[\s]?\d{2}[\s]?\d{2}[\s]?\d{3}[\s]?\d{3}[\s]?\d{2})(?!\d)')

    # ---- CN checksum (ISO 7064 Mod 11-2) ----
    _CN_W = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    _CN_CHK = '10X98765432'

    def _cn_check(self, s):
        if len(s) != 18 or not s[:17].isdigit():
            return False
        total = sum(int(d) * w for d, w in zip(s[:17], self._CN_W))
        return s[17].upper() == self._CN_CHK[total % 11]

    # ---- AU TFN check (weights 1,4,3,7,5,8,6,9,10) ----
    _AU_W = [1, 4, 3, 7, 5, 8, 6, 9, 10]

    def _au_tfn_check(self, digits):
        if len(digits) != 9 or not digits.isdigit():
            return False
        return sum(int(d) * w for d, w in zip(digits, self._AU_W)) % 11 == 0

    # ---- TH check digit (mod 11) ----
    def _th_check(self, digits):
        if len(digits) != 13 or not digits.isdigit():
            return False
        total = sum(int(digits[i]) * (13 - i) for i in range(12))
        return int(digits[12]) == (11 - total % 11) % 10

    # ---- FR NIR check (mod 97) ----
    def _fr_nir_check(self, digits):
        if len(digits) != 15 or not digits.isdigit():
            return False
        return int(digits[13:15]) == 97 - (int(digits[:13]) % 97)

    # ---- Main detect ----
    def detect(self, text):
        matches = []

        # CN (checksum-gated, no keyword required)
        for m in self.CN_PAT.finditer(text):
            raw = m.group()
            if self._cn_check(raw):
                matches.append(Match(
                    label=self.label, confidence=0.98,
                    masked_preview=raw[:3] + '**************' + raw[-1:],
                    start=m.start(), end=m.end(), region='CN'))

        # US SSN (keyword-gated)
        if self.US_KW.search(text):
            for m in self.US_SSN_PAT.finditer(text):
                area, grp, serial = m.group(1), m.group(2), m.group(3)
                if area in ('000', '666') or area[0] == '9':
                    continue
                if grp == '00' or serial == '0000':
                    continue
                matches.append(Match(
                    label=self.label, confidence=0.90,
                    masked_preview=f'***-**-**{serial[-2:]}',
                    start=m.start(), end=m.end(), region='US'))

        # AU TFN (keyword-gated + checksum)
        if self.AU_KW.search(text):
            for m in self.AU_TFN_PAT.finditer(text):
                digits = m.group(1) + m.group(2) + m.group(3)
                if self._au_tfn_check(digits):
                    matches.append(Match(
                        label=self.label, confidence=0.92,
                        masked_preview=digits[:2] + ' ***** ' + digits[-1:],
                        start=m.start(), end=m.end(), region='AU'))

        # SG NRIC (keyword-gated)
        if self.SG_KW.search(text):
            for m in self.SG_NRIC_PAT.finditer(text):
                raw = m.group(1)
                matches.append(Match(
                    label=self.label, confidence=0.88,
                    masked_preview=raw[0] + '*******' + raw[-1:],
                    start=m.start(), end=m.end(), region='SG'))

        # MY MyKad (keyword-gated + date validation)
        if self.MY_KW.search(text):
            for m in self.MY_MYKAD_PAT.finditer(text):
                digits = m.group(1) + m.group(2) + m.group(3)
                if len(digits) != 12:
                    continue
                mm, dd = int(digits[2:4]), int(digits[4:6])
                if mm < 1 or mm > 12 or dd < 1 or dd > 31:
                    continue
                matches.append(Match(
                    label=self.label, confidence=0.88,
                    masked_preview=digits[:2] + '********' + digits[-1:],
                    start=m.start(), end=m.end(), region='MY'))

        # TH National ID (keyword-gated + checksum)
        if self.TH_KW.search(text):
            for m in self.TH_PAT.finditer(text):
                digits = re.sub(r'[\s\-]', '', m.group())
                if self._th_check(digits):
                    matches.append(Match(
                        label=self.label, confidence=0.90,
                        masked_preview=digits[:2] + '-***********-' + digits[-1],
                        start=m.start(), end=m.end(), region='TH'))

        # ID NIK (keyword-gated + date validation)
        if self.ID_KW.search(text):
            for m in self.ID_NIK_PAT.finditer(text):
                d = m.group(1)
                dd, mm = int(d[6:8]), int(d[8:10])
                if dd > 40:
                    dd -= 40  # female offset
                if mm < 1 or mm > 12 or dd < 1 or dd > 31:
                    continue
                matches.append(Match(
                    label=self.label, confidence=0.85,
                    masked_preview=d[:2] + '************' + d[-1:],
                    start=m.start(), end=m.end(), region='ID'))

        # DE Steuer-ID (keyword-gated)
        if self.DE_KW.search(text):
            for m in self.DE_STID_PAT.finditer(text):
                digits = re.sub(r'\s', '', m.group(1))
                if len(digits) != 11 or not digits.isdigit():
                    continue
                if digits[0] == '0':
                    continue
                matches.append(Match(
                    label=self.label, confidence=0.85,
                    masked_preview=digits[:2] + ' ******* ' + digits[-1:],
                    start=m.start(), end=m.end(), region='DE'))

        # UK NIN (keyword-gated)
        if self.UK_KW.search(text):
            for m in self.UK_NIN_PAT.finditer(text):
                raw = re.sub(r'\s', '', m.group(1))
                matches.append(Match(
                    label=self.label, confidence=0.90,
                    masked_preview=raw[:2] + ' ****** ' + raw[-1],
                    start=m.start(), end=m.end(), region='UK'))

        # FR NIR (keyword-gated + mod-97 check)
        if self.FR_KW.search(text):
            for m in self.FR_NIR_PAT.finditer(text):
                digits = re.sub(r'\s', '', m.group(1))
                if self._fr_nir_check(digits):
                    matches.append(Match(
                        label=self.label, confidence=0.92,
                        masked_preview=digits[0] + ' ************ ' + digits[-1:],
                        start=m.start(), end=m.end(), region='FR'))

        return matches
