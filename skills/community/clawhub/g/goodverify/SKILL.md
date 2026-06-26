---
name: goodverify
description: >
  Verify emails, phones, and addresses using the goodverify CLI.
  Use when the user asks to verify contact data, check deliverability,
  validate an address, look up a phone number, check API usage, or
  mentions "goodverify", "verify email", "verify phone", "verify address".
compatibility: Requires the goodverify CLI binary and a goodverify.dev API key.
metadata:
  author: agoodway
  version: "0.1.0"
---

# GoodVerify CLI

Verify emails, phone numbers, and mailing addresses via the [goodverify.dev](https://goodverify.dev) API.

## Prerequisites

The `goodverify` CLI must be installed and configured. Check with:

```bash
goodverify --version
goodverify configure --show
```

If not installed:

```bash
curl -fsSL https://raw.githubusercontent.com/agoodway/goodverify_cli/main/install.sh | sh
```

If not configured, ask the user for their API key and base URL, then:

```bash
goodverify configure --env production --url https://goodverify.dev --key <api_key>
```

## Commands

### Verify Email

Check deliverability, domain MX records, disposable/catch-all/role flags.

```bash
goodverify verify email --email user@example.com
```

**Key response fields:**
- `deliverability.status` — `deliverable`, `undeliverable`, or `risky`
- `deliverability.reason` — `accepted_email`, `rejected_email`, `unknown`, etc.
- `flags.is_disposable` — temporary email service
- `flags.is_catch_all` — domain accepts all addresses
- `flags.is_role_account` — generic address like info@, support@
- `domain.has_mx_records` — domain can receive email

### Verify Phone

Check carrier, phone type (mobile/landline/voip), compliance (DNC/TCPA), and formatting.

```bash
goodverify verify phone --phone "+15551234567"
goodverify verify phone --phone "5551234567" --country US
```

**Key response fields:**
- `valid` — whether the number is valid
- `phone_type` — `mobile`, `landline`, `voip`, `toll_free`
- `carrier.name` — carrier name
- `compliance.dnc` — on Do Not Call list
- `compliance.tcpa` — TCPA consent required
- `formatted.e164` — standardized format

### Verify Address

Standardize, geocode, check deliverability, and find property owners.

Single string:
```bash
goodverify verify address --address "123 Main St, Springfield, IL 62701"
```

Structured fields:
```bash
goodverify verify address --street "123 Main St" --city Springfield --state IL --zip 62701
```

**Key response fields:**
- `deliverability` — `deliverable`, `undeliverable`, `missing_unit`
- `standardized_address` — USPS-standardized components
- `geo_location` — latitude, longitude, accuracy
- `owners` — property owner information (name, other addresses, phones, emails)
- `property.type` — residential, commercial, etc.

### Batch Operations

```bash
goodverify batch list                    # List all batch jobs
goodverify batch get --id <batch_id>     # Get batch job details
goodverify batch results --id <batch_id> # Download results
goodverify batch sample > template.csv   # Get CSV template
```

### Usage & Health

```bash
goodverify usage          # Credit balance, plan, rate limits
goodverify health         # API health check (no auth required)
```

## Global Options

All commands accept:
- `--env <name>` — use a specific configured environment
- `--key <key>` — override API key for this request
- `--url <url>` — override base URL for this request
- `--json` — output raw JSON (default is pretty-printed)

## Guidelines

- Always use `--json` when you need to parse the response programmatically
- For bulk verification, prefer `batch` commands over looping `verify` calls
- Phone numbers should include country code or use `--country` flag
- Address verification works best with complete addresses (street, city, state, zip)
- Check `goodverify usage` before large batch operations to confirm credit balance
- `sk_*` keys are read-write (required for batch). `pk_*` keys are read-only.
