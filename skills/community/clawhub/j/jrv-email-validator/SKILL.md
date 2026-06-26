---
name: email-validator
description: Validate email addresses with syntax checks (RFC 5322), MX record verification, disposable/temporary email detection, and common typo suggestions. Use when validating user signups, cleaning email lists, checking deliverability, or detecting throwaway addresses. Supports batch validation from file. No API keys required.
---

# Email Validator

Multi-layer email validation: syntax, DNS, disposable detection, typo correction.

## Quick Start

```bash
# Validate a single email
python3 scripts/email_validate.py user@example.com

# Validate multiple emails
python3 scripts/email_validate.py user@gmail.com admin@company.org test@mailinator.com

# JSON output
python3 scripts/email_validate.py user@example.com --json

# Batch validate from file
python3 scripts/email_validate.py --file emails.txt

# Skip DNS checks (syntax + disposable only)
python3 scripts/email_validate.py user@example.com --no-dns
```

## Validation Checks

1. **Syntax** — RFC 5322 compliance (local part, domain, length limits)
2. **MX Records** — DNS lookup to verify the domain accepts email
3. **Disposable Detection** — Flags 80+ known throwaway email providers
4. **Typo Suggestion** — Catches common misspellings (gmial.com → gmail.com)

## Flags

- `--json` — Machine-readable JSON output
- `--file, -f <path>` — Read emails from file (one per line)
- `--no-dns` — Skip MX record checks
- `--no-disposable` — Skip disposable email check

## Exit Codes

- `0` — All emails valid
- `1` — One or more emails invalid
