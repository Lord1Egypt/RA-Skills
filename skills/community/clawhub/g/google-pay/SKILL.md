---
name: Google Pay
slug: google-pay
version: 1.0.0
homepage: https://clawic.com/skills/google-pay
description: Implement Google Pay for web and Android with tokenization safety, gateway alignment, and production-ready checkout operations.
changelog: Initial release with implementation, validation, launch, and incident response playbooks for Google Pay.
metadata: {"clawdbot":{"emoji":"💳","requires":{"bins":["curl","jq"],"env":["GOOGLE_PAY_MERCHANT_ID"]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` and confirm platform, PSP, and release target before making code changes.

## When to Use

User needs Google Pay in checkout, subscriptions, or wallet-first conversion flows. Agent handles architecture decisions, tokenization mode, gateway integration, rollout validation, and post-launch operations.

## Architecture

Memory lives in `~/google-pay/`. See `memory-template.md` for setup and status fields.

```
~/google-pay/
|-- memory.md                 # Project snapshot, risk status, and rollout state
|-- implementations.md        # Selected approach and platform notes
|-- validation-log.md         # Test evidence and environment results
`-- incidents.md              # Failed payments, root causes, and fixes
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory template | `memory-template.md` |
| Implementation plan | `implementation-playbook.md` |
| Validation matrix | `validation-checklist.md` |
| Failure recovery | `failure-handling.md` |
| Release and operations | `launch-playbook.md` |
| Recurring and subscription flows | `recurring-payments.md` |

## Requirements

- Environment variable: `GOOGLE_PAY_MERCHANT_ID`
- CLI tools for diagnostics: `curl`, `jq`
- Access to Google Pay business console and target PSP account

Never ask users to paste private keys, full token payloads, or PSP secrets into chat.

## Data Storage

Local notes stay under `~/google-pay/`:
- memory file for current state and integration decisions
- validation log file for test outcomes and evidence
- incidents file for failure signatures and mitigations

## Core Rules

### 1. Confirm Business Goal Before Choosing Integration Path
Start by identifying the target outcome:
- Higher mobile checkout conversion
- Faster repeat purchases
- Lower payment friction on Android and Chrome
- Fewer payment failures

Then choose one primary path:
- Web with Google Pay API and gateway tokenization
- Android with Google Pay API in app flow
- PSP-mediated integration path

Do not mix paths in one patch unless the user asks for a migration plan.

### 2. Require Environment and Merchant Prerequisites
Before implementation, confirm:
- Google Pay merchant profile exists for production
- Gateway or PSP supports Google Pay in target countries
- Test environment is isolated from production
- Origin and app package configuration are correct

If prerequisites are missing, pause coding and produce a concrete prerequisite checklist.

### 3. Enforce Server Truth for Amounts and Currency
Amounts and currency must match across:
- Client payment data request
- Server-side cart or order totals
- PSP authorization and capture calls

Never trust client totals for final charge amount.

### 4. Keep Token Handling Minimal and Auditable
Treat Google Pay token payloads as sensitive:
- Forward payload only to backend or PSP
- Persist metadata only (request id, status, amount, currency)
- Never store raw token payload in logs, notes, or screenshots

### 5. Choose Tokenization Path Explicitly
Use one clear tokenization mode per project:
- `PAYMENT_GATEWAY` for most integrations
- `DIRECT` only when user explicitly owns decryption and PCI scope

Do not mix tokenization modes without a documented migration and risk review.

### 6. Build Idempotent and Recoverable Payment Steps
Require idempotency and reconciliation for all critical calls:
- Authorization request
- Capture request
- Refund or void operations

Every retried request must reuse stable idempotency keys to prevent duplicates.

### 7. Separate Test and Production Release Gates
Do not recommend production rollout until all gates pass:
- Test success, decline, cancellation, and timeout paths are covered
- Device and browser matrix is complete for supported audience
- Fallback card or alternative checkout works when Google Pay is unavailable
- Failure observability and alerts are active

## Common Traps

- Shipping test environment config to production -> checkout fails for live users
- Mismatching gateway merchant ids across environments -> token processing errors
- Skipping `isReadyToPay` style capability checks -> broken wallet button behavior
- Trusting client totals -> mismatch between authorized and captured amounts
- Missing idempotency on retries -> duplicate charges and refund overhead
- Launching without fallback checkout -> conversion loss when wallet is unavailable

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://pay.google.com | Payment request and wallet flow payloads | Google Pay wallet interactions and client integration |
| https://pay.google.com/gp/p/js/pay.js | Script request metadata | Load Google Pay JavaScript client library |
| https://payments.developers.google.com | Documentation fetch traffic | Reference integration docs and test cards |

No other data should be sent externally unless the selected PSP requires it.

## Security & Privacy

Data that leaves your machine:
- Google Pay request payloads needed for wallet flow
- Payment token payloads sent to configured PSP or backend

Data that stays local:
- Integration notes and rollout state under `~/google-pay/`
- Validation evidence and failure logs without raw token payloads

This skill does NOT:
- Store raw token payloads in memory files
- Skip mandatory merchant and gateway requirements
- Enable production release without explicit readiness checks

## Trust

Google Pay integrations depend on Google infrastructure and the chosen PSP.
Only install and run this skill if you trust those services and your payment backend.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `payments` - General payment design and checkout decision frameworks
- `android` - Android implementation and runtime troubleshooting patterns
- `billing` - Billing models, reconciliation, and payment lifecycle decisions
- `auth` - Authentication and session hardening in transaction flows
- `api` - Reliable backend API contracts and failure-safe integrations

## Feedback

- If useful: `clawhub star google-pay`
- Stay updated: `clawhub sync`
