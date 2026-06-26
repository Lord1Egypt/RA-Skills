---
name: gotchi-pocket
description: Manage Aavegotchi pocket wallets (escrow) on Base with Bankr. Use when the user wants to deposit ERC20 tokens into a gotchi pocket, withdraw ERC20 tokens from a pocket, check pocket balances/ownership by gotchi ID, or issue plain-English pocket commands.
homepage: https://github.com/aavegotchi/aavegotchi-agent-skills
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
        - python3
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
---

# Gotchi Pocket

Send and receive ERC20 tokens with Aavegotchi pockets on Base, using Bankr for signing/submission.

## What this skill does

- Resolve gotchi owner + pocket address from gotchi ID
- Check owner and pocket token balances
- Deposit ERC20 tokens from owner wallet into pocket
- Withdraw ERC20 tokens from pocket with `transferEscrow(...)`
- Enforce owner-control check against active Bankr wallet (default)
- Parse plain-English commands and dispatch to scripts automatically
- Require explicit approval for natural-language withdraw intents

## Scripts

- `./scripts/pocket-info.sh <gotchi-id> [--check-bankr]`
- `./scripts/pocket-balance.sh <gotchi-id> <token-alias-or-address>`
- `./scripts/pocket-deposit.sh <gotchi-id> <token-alias-or-address> <amount> [--raw]`
- `./scripts/pocket-withdraw.sh <gotchi-id> <token-alias-or-address> <to-address> <amount> [--raw]`
- `./scripts/pocket-command.sh [--approve-withdraw] [--dry-run] "<natural-language command>"`

## Natural-language command layer

Use one plain-English command and let the skill route it.

Examples:

```bash
./scripts/pocket-command.sh "send 25 GHST to gotchi 9638 pocket"
./scripts/pocket-command.sh "send 25 GHST from gotchi 9638 pocket to 0xb96b48a6b190a9d509ce9312654f34e9770f2110"
./scripts/pocket-command.sh "check pocket GHST balance for gotchi 9638"
./scripts/pocket-command.sh "show pocket info for gotchi 9638"
```

Preview parsing without sending tx:

```bash
./scripts/pocket-command.sh --dry-run "send 25 GHST to gotchi 9638 pocket"
```

## Withdraw approval safety

Natural-language withdraws are blocked unless explicitly approved.

```bash
# First call returns approval_required=true and exits without sending
./scripts/pocket-command.sh "send 25 GHST from gotchi 9638 pocket to 0xb96b48a6b190a9d509ce9312654f34e9770f2110"

# Approved execution
./scripts/pocket-command.sh --approve-withdraw "send 25 GHST from gotchi 9638 pocket to 0xb96b48a6b190a9d509ce9312654f34e9770f2110"
```

## Token input

Use either a token address or aliases:

- `GHST`
- `FUD`
- `FOMO`
- `ALPHA`
- `KEK`
- `USDC`
- `WETH`
- `DAI`

## Standard workflow

1. Resolve addresses:

```bash
./scripts/pocket-info.sh 9638 --check-bankr
```

2. Check balance before mutation:

```bash
./scripts/pocket-balance.sh 9638 GHST
```

3. Deposit or withdraw:

```bash
# Deposit 100 GHST to pocket
./scripts/pocket-deposit.sh 9638 GHST 100

# Withdraw 100 GHST from pocket to owner
./scripts/pocket-withdraw.sh 9638 GHST 0xb96b48a6b190a9d509ce9312654f34e9770f2110 100
```

4. Re-check balance after tx:

```bash
./scripts/pocket-balance.sh 9638 GHST
```

## Notes

- Amounts are token units by default (for example `100` GHST).
- Use `--raw` only when the amount is already base units.
- Owner check is on by default and can be skipped with `SKIP_BANKR_OWNER_CHECK=1`.
- All txs use `waitForConfirmation=true` and return a BaseScan URL.

## Contracts

- Aavegotchi Diamond (Base): `0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`
- GHST (Base): `0xcD2F22236DD9Dfe2356D7C543161D4d260FD9BcB`
