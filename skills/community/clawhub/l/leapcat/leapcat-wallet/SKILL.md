---
name: leapcat-wallet
description: Manage wallet balances, deposits, withdrawals, debt status, and fund activity on Leapcat via the leapcat CLI.
homepage: https://leapcat.ai
---

# LeapCat Wallet Management Skill

Manage wallet balances, deposits, withdrawals, debt status, and fund activity using the leapcat.

## Prerequisites

- Node.js 18+ is required (commands use `npx leapcat@0.1.1` which auto-downloads the CLI)
- User must be authenticated — run `npx leapcat@0.1.1 auth login --email <email>` first
- For withdrawals: a Turnkey session is required — run `npx leapcat@0.1.1 auth reauth --json` first
- For withdrawals: trade password must be set

## Commands

### wallet balance

Check the user's current wallet balance.

```bash
npx leapcat@0.1.1 wallet balance --json
```

### wallet deposit-address

Get the deposit address for receiving funds.

```bash
npx leapcat@0.1.1 wallet deposit-address --json
```

### wallet deposits

List all deposit transactions.

```bash
npx leapcat@0.1.1 wallet deposits --json
```

### wallet deposit

Get details of a specific deposit.

```bash
npx leapcat@0.1.1 wallet deposit --id <deposit-id> --json
```

**Parameters:**
- `--id <deposit-id>` — The deposit transaction identifier

### wallet withdraw

Initiate a withdrawal. Requires an elevated session (`auth reauth`) and trade password.

```bash
npx leapcat@0.1.1 wallet withdraw --amount <amount> --address <address> --json
```

**Parameters:**
- `--amount <amount>` — Amount to withdraw
- `--address <address>` — Destination wallet address

### wallet withdrawals

List all withdrawal transactions.

```bash
npx leapcat@0.1.1 wallet withdrawals --json
```

### wallet debt-status

Check if the user has any outstanding debt or margin obligations.

```bash
npx leapcat@0.1.1 wallet debt-status --json
```

### wallet fund-activities

View a history of all fund activities (deposits, withdrawals, trades, fees, etc.).

```bash
npx leapcat@0.1.1 wallet fund-activities --json
```

## Workflow

### Checking Balance

```bash
npx leapcat@0.1.1 wallet balance --json
```

### Depositing Funds

1. **Get deposit address** — Run `wallet deposit-address --json` to obtain the address.
2. **Share address with user** — Provide the address so the user can transfer funds from an external source.
3. **Monitor deposit** — Periodically run `wallet deposits --json` to check if the deposit has arrived and been confirmed.

### Withdrawing Funds

1. **Re-authenticate** — Run `npx leapcat@0.1.1 auth reauth --json` to elevate the session (Turnkey session).
2. **Initiate withdrawal** — Run `wallet withdraw --amount <amount> --address <address> --json`. The user will be prompted for their trade password.
3. **Monitor withdrawal** — Run `wallet withdrawals --json` to track the withdrawal status.

### Reviewing Activity

```bash
npx leapcat@0.1.1 wallet fund-activities --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NOT_AUTHENTICATED` | Session expired | Re-authenticate with `auth login` |
| `REAUTH_REQUIRED` | Elevated session needed for withdrawal | Run `auth reauth --json` first |
| `TRADE_PASSWORD_NOT_SET` | Trade password required for withdrawal | Set via `auth trade-password set` |
| `INSUFFICIENT_BALANCE` | Not enough funds to withdraw | Check balance and adjust amount |
| `INVALID_ADDRESS` | Destination address is malformed | Verify the withdrawal address |
| `WITHDRAWAL_LIMIT_EXCEEDED` | Amount exceeds daily/monthly limit | Reduce the withdrawal amount |
| `DEPOSIT_NOT_FOUND` | Invalid deposit ID | Re-check with `wallet deposits --json` |
