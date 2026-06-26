# Detection Patterns Reference

## Label: PHONE
- **INTL**: `+CC` prefix → region resolved from country code map (+86=CN, +1=US, +61=AU, +65=SG, +60=MY, +66=TH, +62=ID, +49=DE, +44=UK, +33=FR)
- **CN mobile**: `1[3-9]X XXXX XXXX` (11 digits)
- **CN landline**: `0XX(X)-XXXXXXX(X)` (requires separator)
- **US**: `(XXX) XXX-XXXX` or `XXX-XXX-XXXX` (requires parentheses or dashes)
- **AU mobile**: `04XX XXX XXX`
- **UK mobile**: `07XXX XXXXXX`
- **Confidence**: 0.85–0.92

## Label: EMAIL
- **Pattern**: `local@domain.tld` (RFC-like, ASCII)
- **Confidence**: 0.95
- **Region**: Not assigned (universal)

## Label: NATIONAL_ID
### CN — Chinese ID Card
- 18 digits: 6 region + 8 birthday + 3 seq + 1 check digit
- **Validation**: ISO 7064 Mod 11-2 checksum
- **Confidence**: 0.98 | **Gate**: Checksum (no keyword required)

### US — Social Security Number (SSN)
- 9 digits: `XXX-XX-XXXX`
- **Validation**: Area ≠ 000/666/9xx, group ≠ 00, serial ≠ 0000
- **Confidence**: 0.90 | **Gate**: Keyword (SSN, Social Security)

### AU — Tax File Number (TFN)
- 9 digits: `XXX XXX XXX`
- **Validation**: Weighted checksum (1,4,3,7,5,8,6,9,10), sum mod 11 = 0
- **Confidence**: 0.92 | **Gate**: Keyword (TFN, Tax File Number)

### SG — NRIC/FIN
- Format: `[STFGM]` + 7 digits + check letter
- **Confidence**: 0.88 | **Gate**: Keyword (NRIC, FIN, IC)

### MY — MyKad
- 12 digits: `YYMMDD-SS-GGGG`
- **Validation**: Date validity on first 6 digits
- **Confidence**: 0.88 | **Gate**: Keyword (MyKad, IC, NRIC)

### TH — Thai National ID
- 13 digits: `X-XXXX-XXXXX-XX-X`
- **Validation**: Mod 11 check digit
- **Confidence**: 0.90 | **Gate**: Keyword (Thai ID, national ID)

### ID — NIK/KTP
- 16 digits: 6 region + 6 date (DD+40 for female) + 4 seq
- **Validation**: Date validity
- **Confidence**: 0.85 | **Gate**: Keyword (NIK, KTP)

### DE — Steuer-ID
- 11 digits, first digit ≠ 0
- **Confidence**: 0.85 | **Gate**: Keyword (Steuer-ID, IdNr, Tax ID)

### UK — National Insurance Number (NIN)
- Format: 2 letters + 6 digits + 1 letter (e.g. AB123456C)
- Letter restrictions: specific character sets for each position
- **Confidence**: 0.90 | **Gate**: Keyword (NIN, National Insurance)

### FR — NIR/INSEE
- 15 digits: sex + year + month + dept + commune + seq + check
- **Validation**: `check = 97 - (first_13 mod 97)`
- **Confidence**: 0.92 | **Gate**: Keyword (NIR, INSEE, social security)

## Label: PASSPORT
- **CN**: `[EGDSPH]` + optional letter + 7-8 digits
- **DE**: `C` + 8 alphanumeric
- **FR**: 2 digits + 2 letters + 5 digits
- **Generic**: 1-2 uppercase letters + 6-9 digits
- **Confidence**: 0.85 | **Gate**: Keyword (passport, visa, immigration — multi-language)

## Label: BANK_CARD
- **Formatted**: `XXXX XXXX XXXX XXXX` (space/dash groups of 4)
- **Continuous**: 13-19 consecutive digits
- **Validation**: Luhn algorithm (universal)
- **Confidence**: 0.92 | **Region**: Not assigned (universal)

## Label: PERSON_NAME
- **CN**: Keyword-gated (2-4 Chinese characters after context keywords or before honorific titles)
- **Western**: Keyword-gated (`name:`, `Mr./Mrs./Dr.` + First Last)
- **DE**: Keyword-gated (Name/Vorname/Nachname + name)
- **FR**: Keyword-gated (nom/prénom + name)
- **Confidence**: 0.70–0.75

## Label: ADDRESS
- **CN**: Structural (province + city + district) or keyword-gated
- **US**: Number + street + state abbreviation + ZIP (5 or 5+4)
- **AU**: Number + street + state abbreviation + 4-digit postcode
- **UK**: Postcode pattern (e.g. SW1A 1AA), keyword-boosted
- **DE**: Street name (straße/str./weg) + house number + PLZ
- **FR**: Number + street type (rue/avenue/boulevard) + code postal
- **Confidence**: 0.75–0.80

## Label: SOCIAL_ACCOUNT
- **WeChat**: keyword + letter-start ID (6-20 chars)
- **QQ**: keyword + 5-12 digit number
- **Twitter/X**: keyword + @handle
- **Generic**: keyword + account value
- **Confidence**: 0.80 | **Region**: Not assigned

## Risk Level Rules
- **HIGH**: NATIONAL_ID / PASSPORT / BANK_CARD present, or combo (PERSON_NAME + PHONE/EMAIL + ADDRESS)
- **LOW**: All other detections

## False Positive Control
1. Regex → checksum/format validation → context keyword confirmation
2. National IDs: CN/AU/TH/FR use algorithmic checksums; US/SG/MY/DE/UK use keyword gating
3. Passport: Always keyword-gated (multi-language)
4. Bank card: Luhn validation (universal)
5. Person name / address: Keyword or structural gating
6. Overlapping matches: Higher confidence wins
