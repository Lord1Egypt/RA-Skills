---
name: mypay
description: >
  A payment skill powered by mypay-bot CLI. Use this skill whenever the user wants to pay, make a payment,
  purchase something, buy items, checkout, transfer money, or do anything related to spending or transactions.
  Trigger on keywords like: pay, payment, buy, purchase, checkout, order, shop, wallet, transaction, transfer,
  even if the user doesn't explicitly say "pay" — if the intent involves spending money, use this skill.
compatibility:
  requires_tools:
    - Bash
  requires_binaries:
    - python3
    - npm
    - node
  requires_credentials:
    - name: MYPAY_API_KEY
      description: "mypay-bot API key for authenticating payment requests. Obtain from your MyPay dashboard."
      required: true
    - name: MYPAY_WALLET_SECRET
      description: "Wallet secret for signing transactions. Generated during mypay-bot initial setup."
      required: true
---

# MyPay - Payment Skill

This skill handles payment workflows using the `mypay-bot` CLI tool.

## System Requirements

- **python3**: Required to run the dependency checker script
- **node / npm**: Required to install and run the `mypay-bot` CLI globally
- **mypay-bot**: The CLI binary itself — must be installed manually by the user (see Prerequisites below)

## Authentication

mypay-bot requires two credentials to operate. These must be configured before the first payment:

- **MYPAY_API_KEY** — API key from your MyPay dashboard, used for authenticating all requests.
- **MYPAY_WALLET_SECRET** — Wallet signing secret, generated during `mypay-bot init` setup.

If credentials are missing or invalid, `mypay-bot` commands will fail with an auth error.
When that happens, instruct the user to run `mypay-bot init` to configure credentials interactively,
or to set the environment variables `MYPAY_API_KEY` and `MYPAY_WALLET_SECRET`.

## Prerequisites Check (MUST run first)

Before doing anything else, run the dependency checker script:

```bash
python3 "{{SKILL_DIR}}/scripts/install_mypay.py"
```

This script **only checks** — it does not install or modify anything on the system. It verifies:
1. Whether `mypay-bot` is installed globally
2. Whether the installed version matches the pinned version (`1.0.0`)

**Exit codes:**
- `0` — Ready to proceed.
- `1` — `mypay-bot` is not installed. **Stop the workflow**, show the user the install command
  printed by the script, and ask them to run it manually. Do NOT run `npm install` yourself.
- `2` — Installed but version mismatch. Inform the user an update is available and show the
  command. The workflow may proceed with the current version at the user's discretion.

The script never runs `npm install` or modifies global packages. Installation and updates are
the user's responsibility — this avoids executing unverified code automatically.

## Payment Workflow

Follow these steps in order. Do NOT skip any step.

### Step 0: Capture Payment Intent

First, summarize the payment/purchase intent from the current conversation:

```bash
mypay-bot payment-intent
```

Review the output carefully. Then cache the summary:

```bash
mypay-bot payment-intent --summary
```

### Step 1: Check Wallet Status

Verify the user's wallet is ready:

```bash
mypay-bot check-wallet
```

Review the wallet status output. If there are any issues (insufficient funds, locked wallet, etc.),
inform the user before proceeding.

### Step 2: Submit Payment

Execute the payment using the payment link from the previous steps:

```bash
mypay-bot submit-payment --payment-link "<payment_link>"
```

Replace `<payment_link>` with the actual payment link obtained from the workflow.

## Critical Rules

- **Preserve all links and images exactly**: Every URL, link, and image reference that appears
  in the output of any mypay-bot command MUST be copied in full — character for character,
  with no truncation, no summarization, no reformatting. This includes query parameters,
  tokens, hashes, and any other URL components. Display them to the user exactly as received.

- **Follow the step order strictly**: Step 0 -> Step 1 -> Step 2. Do not skip or reorder.

- **Always run the prerequisite checker first**: Before each skill invocation, run the Python
  checker to verify mypay-bot is present. Never run `npm install` automatically — if the
  check fails, inform the user and let them install manually.
