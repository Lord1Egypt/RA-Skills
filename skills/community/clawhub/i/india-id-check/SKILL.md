---
name: india-id-check
description: Validate, identify, mask and redact Indian identifiers offline - Aadhaar (Verhoeff check digit), PAN, GSTIN, TAN, IFSC, UPI ID, mobile, PIN code, vehicle number (incl. BH series and TG/TS), driving licence, passport, voter ID, CIN, LLPIN, Udyam and card numbers. Use when checking form inputs or KYC data, decoding what an Indian ID means, masking Aadhaar/PAN for display, or removing personal data from text before storing or sharing it.
version: 1.0.0
tags: [india, kyc, validation, aadhaar, pan, ifsc, upi, privacy, pii, developer]
---

# India ID Check

Offline validation and decoding of Indian identifiers, plus privacy-safe masking and redaction. **Never judge an ID by eye or recompute checksums in your head — run the script.**

Script: `scripts/idcheck.py` (Python 3, standard library only). Input: a JSON string or a `.json` file. Output: JSON.

## Commands

| The user wants to… | Command | Example input |
|---|---|---|
| Check one ID (type auto-detected) | `validate` | `{"value": "ABCPE1234F"}` |
| Check with a known type | `validate` | `{"type": "aadhaar", "value": "2341 2341 2346"}` |
| Check many at once | `validate` | `{"values": ["27AAPFU0939F1ZV", "SBIN0001234"]}` |
| "What kind of number is this?" | `detect` | `{"value": "UDYAM-MH-26-0012345"}` |
| Show an ID safely | `mask` | `{"value": "234123412346"}` → `XXXX XXXX 2346` |
| Remove personal data from text | `redact` | `{"text": "...", "style": "mask" or "label", "types": ["aadhaar","pan"]}` |
| Check IDs agree with each other | `crosscheck` | `{"pan": "...", "gstin": "...", "name": "...", "entity": "firm", "ifsc": "...", "bank": "...", "pin": "...", "state": "..."}` |
| Branch of an IFSC / post offices of a PIN | `lookup` (needs internet) | `{"ifsc": "HDFC0000123"}` or `{"pin": "411001"}` |

Run: `python3 scripts/idcheck.py <command> '<json>'`

PAN tip: pass `"name"` with a PAN to check the 5th character against the surname (individuals) or entity name.

## What each check proves

| ID | Offline check | What it decodes |
|---|---|---|
| Aadhaar | 12 digits, not starting 0/1, **Verhoeff check digit** | — (masked only) |
| PAN | pattern, valid holder-type letter, optional name initial | holder type (individual, company, firm…) |
| GSTIN | pattern, state code, **check character** | state, embedded PAN, holder type |
| IFSC | pattern, 5th char `0` | bank (≈55 banks offline), branch code |
| UPI ID | `name@handle` format | app/bank behind the handle (PhonePe, Google Pay, Paytm…) |
| Mobile | 10 digits starting 6–9, strips +91/0 | E.164 form |
| PIN code | 6 digits, not starting 0 | postal zone, likely state |
| Vehicle | state code, RTO, series; BH series year | state, RTO, formatted plate |
| Driving licence | state + RTO + year + serial | state, year issued |
| Passport / Voter ID / TAN / LLPIN | pattern | — |
| CIN | pattern, state, year, company type | listed?, industry code, state, year, company type |
| Udyam | `UDYAM-XX-00-0000000` | state, district code |
| Card | **Luhn check** | network (Visa, Mastercard, RuPay, Amex…) |

## Rules for the agent
1. **Valid ≠ real.** A valid result means well-formed. It does not prove the ID exists, is active, or belongs to the person. Say so, and point to the official verifier given in `details.note` when it matters.
2. **Privacy first.** Never repeat a full Aadhaar or card number back to the user or into files/logs; use the `masked` field. When asked to store or share text containing personal data, run `redact` first.
3. For PAN, explain that its check character's algorithm is not public, so a typo that keeps the pattern intact can't be caught offline.
4. Use `lookup` only when the user wants branch/post-office details and internet access is available; if it fails, the offline result still stands.
5. When presenting results: one line per ID — ✅/❌, type, the key decoded facts, and any warning.
