---
name: mx-id-validators
description: "Validate Mexican CURP, RFC, and NSS offline — checksum, structure, and birth date. No network, no PII leaves the machine. Use for Mexican KYC, onboarding, payroll, or form validation."
metadata:
  {
    "openclaw":
      {
        "emoji": "🇲🇽",
        "requires": { "bins": ["python3"] }
      }
  }
---

# Mexican ID Validators (CURP · RFC · NSS)

Offline validation of the three Mexican identity numbers that break every
onboarding flow. No API keys, no network calls, no PII leaves the machine.

## Why this exists

Sending a CURP to a third-party API to find out whether the check digit is
right means shipping a personal identifier over the wire to learn one
character. These validators compute everything locally: structure, date
plausibility, state code, and the official check digit.

## Run it

```bash
python3 scripts/mx_validators.py curp FUSL861017HDFNNS08
python3 scripts/mx_validators.py rfc  GARC850101A13
python3 scripts/mx_validators.py nss  04008812341
```

Or import it:

```python
import sys; sys.path.insert(0, "scripts")
from mx_validators import validate_curp, validate_rfc, validate_nss

validate_curp("FUSL861017HDFNNS08")
# {'valid': True, 'birthDate': '86/10/17', 'sex': 'Hombre', 'stateCode': 'DF', 'checkDigit': 8}
```

Every call returns `{"valid": bool, ...}`. On failure it returns a specific
`error` code — never a bare `false`. Common codes: `bad_length`,
`bad_initial_block`, `bad_birthdate_block`, `bad_sex`, `bad_state_code`,
`bad_month`, `bad_day`, `bad_format`, `checksum_mismatch`.

`checksum_mismatch` also returns `expectedCheckDigit` and `actualCheckDigit`,
so the caller can show the user exactly what to fix.

## What each validator checks

**CURP** (18 chars) — initial block, `AAMMDD` birth date with month/day range,
`H`/`M` sex marker, one of the 32 official entity codes, consonant block,
homoclave, then the RENAPO check digit. Lowercase input is normalized.

**RFC** (13 persona física / 12 persona moral) — accepts hyphens and spaces,
handles both date offsets, and computes the SAT check digit. The generic RFCs
`XAXX010101000` and `XEXX010101000` are returned valid with
`personType: "generico"` even though they intentionally fail the checksum:
they are authorized by the SAT and appear on real invoices.

**NSS** (11 digits) — IMSS check digit, plus a parse of subdelegation,
registration year, birth year and consecutive number.

## Two things that trip people up

The RFC alphabet is **not** A–Z. Position 24 is `&`, which shifts everything
after it: `0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ`. Using a plain A–Z alphabet
produces wrong check digits that look plausible.

A two-digit year is ambiguous. This module treats `<= 30` as 2000s and
`> 30` as 1900s, which matches IMSS practice. If you need certainty, prefer
the four-digit date you already have.

## Dates are calendar-checked, not range-checked

`31/02`, `30/02`, `31/04` and `29/02` in a non-leap year are rejected with
`impossible_date`. Month/day is not enough: February has 28 or 29 days, and the
leap rule is the full Gregorian one (`%4`, except `%100`, unless `%400`) — so
`29/02/1900` is impossible while `29/02/2000` is valid.

For CURP the century comes from position 17: a digit means born before 2000, a
letter means 2000 or later. That decides which leap-year rule applies.

## Scope

Pure string validation. It cannot tell you whether a well-formed CURP belongs
to a real person or whether the name matches — that requires RENAPO, which has
no public API. It catches typos, bad checksums, impossible dates, and structural
forgery. It does not verify identity.
