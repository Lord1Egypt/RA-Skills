---
name: leapcat-ipo
description: Browse, estimate, subscribe to, and manage IPO subscriptions on Leapcat via the leapcat CLI.
homepage: https://leapcat.ai
---

# LeapCat IPO Subscription Skill

Browse, estimate, subscribe to, and manage IPO (Initial Public Offering) project subscriptions using the leapcat.

## Prerequisites

- Node.js 18+ is required (commands use `npx leapcat@0.1.1` which auto-downloads the CLI)
- User must be authenticated — run `npx leapcat@0.1.1 auth login --email <email>` first
- KYC must be completed and approved (`kyc status` should return `APPROVED`)
- Trade password must be set (`auth trade-password status` should confirm it is set)

## Commands

### ipo projects

List all available IPO projects.

```bash
npx leapcat@0.1.1 ipo projects --json
```

### ipo project

Get detailed information about a specific IPO project.

```bash
npx leapcat@0.1.1 ipo project --id <project-id> --json
```

**Parameters:**
- `--id <project-id>` — The IPO project identifier

### ipo estimate

Estimate the cost of subscribing to an IPO with a given quantity.

```bash
npx leapcat@0.1.1 ipo estimate --id <project-id> --quantity <shares> --json
```

**Parameters:**
- `--id <project-id>` — The IPO project identifier
- `--quantity <shares>` — Number of shares to subscribe for

### ipo subscribe

Submit an IPO subscription order.

```bash
npx leapcat@0.1.1 ipo subscribe --id <project-id> --quantity <shares> --json
```

**Parameters:**
- `--id <project-id>` — The IPO project identifier
- `--quantity <shares>` — Number of shares to subscribe for

### ipo cancel

Cancel a pending IPO subscription.

```bash
npx leapcat@0.1.1 ipo cancel --subscription-id <id> --json
```

**Parameters:**
- `--subscription-id <id>` — The subscription identifier to cancel

### ipo subscriptions

List all of the user's IPO subscriptions.

```bash
npx leapcat@0.1.1 ipo subscriptions --json
```

### ipo subscription

Get details of a specific IPO subscription.

```bash
npx leapcat@0.1.1 ipo subscription --subscription-id <id> --json
```

**Parameters:**
- `--subscription-id <id>` — The subscription identifier

## Workflow

1. **List IPO projects** — Run `ipo projects --json` to see all available IPOs.
2. **Get project details** — Run `ipo project --id <id> --json` to review terms, pricing, and deadlines.
3. **Estimate cost** — Run `ipo estimate --id <id> --quantity <shares> --json` to see the total cost before committing.
4. **Subscribe** — Run `ipo subscribe --id <id> --quantity <shares> --json` to place the subscription. The user may be prompted for their trade password.
5. **Check subscription status** — Run `ipo subscription --subscription-id <id> --json` or `ipo subscriptions --json` to monitor the result.
6. **Cancel if needed** — Run `ipo cancel --subscription-id <id> --json` to cancel a pending subscription (only before the subscription deadline).

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NOT_AUTHENTICATED` | Session expired | Re-authenticate with `auth login` |
| `KYC_NOT_APPROVED` | KYC verification incomplete | Complete the KYC flow first |
| `TRADE_PASSWORD_NOT_SET` | Trade password required | Set trade password via `auth trade-password set` |
| `INSUFFICIENT_BALANCE` | Not enough funds to cover subscription | Deposit funds via `wallet deposit-address` |
| `PROJECT_NOT_FOUND` | Invalid project ID | Re-check with `ipo projects --json` |
| `SUBSCRIPTION_DEADLINE_PASSED` | IPO subscription period has ended | No action possible — deadline has passed |
| `CANCEL_NOT_ALLOWED` | Subscription cannot be cancelled at this stage | Check subscription status for details |
