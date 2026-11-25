# india-id-check 🇮🇳

An AI agent skill that **validates, decodes, masks and redacts Indian IDs — offline**. 17 identifier types, real checksums, zero dependencies.

Works with **OpenClaw, Claude Code, Codex, Cursor** and any agent that reads `SKILL.md`.

## Why
Every Indian app, form and KYC flow handles Aadhaar, PAN, IFSC, UPI IDs and phone numbers. LLMs guess at these formats and can't compute check digits reliably. This skill gives your agent exact answers — and keeps personal data out of logs.

## What it covers
| | |
|---|---|
| **Checksums** | Aadhaar (Verhoeff), GSTIN (mod-36), cards (Luhn) — catches typos and swapped digits |
| **Decoding** | PAN holder type · GSTIN state + PAN · IFSC → bank · UPI handle → app (PhonePe, Google Pay, Paytm's new handles…) · PIN → likely state · vehicle → state & RTO (BH series, TG/TS) · CIN → listed?, year, company type · Udyam → state |
| **Privacy** | `mask` for safe display (`XXXX XXXX 2346`) and `redact` to strip Aadhaar, PAN, phone, email, UPI, cards, passport and voter IDs from any text — checksum-guarded so order numbers and amounts aren't wrongly removed |
| **Cross-checks** | PAN vs GSTIN, PAN 5th letter vs surname, PAN type vs entity, IFSC vs bank, PIN vs state |
| **Optional online** | IFSC branch details and PIN post offices via free public APIs |

## Example
```bash
python3 scripts/idcheck.py validate '{"value": "U72900MH2015PTC123456"}'
# -> valid, unlisted Private Limited Company, Maharashtra, incorporated 2015

python3 scripts/idcheck.py redact '{"text": "Aadhaar 2341 2341 2346, call 9876543210, order 123456789012"}'
# -> "Aadhaar XXXX XXXX 2346, call XXXXXX3210, order 123456789012"
```

## Install
```bash
openclaw skills install india-id-check     # OpenClaw
# or copy this folder into ~/.claude/skills/   # Claude Code
```

## Test
```bash
python3 tests/test_idcheck.py     # 52 tests
```

## Important
A valid format/checksum means an ID is **well-formed**, not that it exists or belongs to someone. Use official services (UIDAI, Income Tax portal, GST portal, MCA, VAHAN) for real verification. Sample IDs in tests are synthetic.
