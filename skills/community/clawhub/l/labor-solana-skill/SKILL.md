---
name: solana_native_transfer
description: >-
  Transfers native SOL on Solana to a recipient address using a funded signing
  key from environment configuration. Use when the user asks to send SOL, transfer
  lamports, pay someone in SOL, or move native tokens on Solana mainnet-beta,
  devnet, or a custom RPC.
metadata:
  openclaw:
    primaryEnv: SOLANA_PRIVATE_KEY
    requires:
      bins:
        - node
      env:
        - SOLANA_PRIVATE_KEY
---

# Solana native SOL transfer

## When to use

Apply this skill when the user wants to **send native SOL** (not SPL tokens) from
their wallet to another Solana address.

## Preconditions

1. **Node.js** is available on PATH (`node`).
2. User has set **`SOLANA_PRIVATE_KEY`** (see README — never commit or paste keys
   into chat). Optionally set **`SOLANA_RPC_URL`** (defaults to public devnet).
3. Dependencies installed once in this skill folder: `npm install` (or `npm ci`).
4. This skill uses TypeScript source compiled to JavaScript via `npm run build`
   and does not require Solana CLI (`solana`) or Python.

## Safety

- **Do not** echo, log, or copy the private key. Use env vars or OpenClaw secrets only.
- Prefer **devnet** for testing. For **mainnet-beta**, require explicit user
  confirmation and a `SOLANA_RPC_URL` pointing at mainnet (or user clearly opts in).
- Reject transfers to invalid addresses. Confirm recipient and amount with the user
  for non-trivial sums.

## How to run the transfer

From the directory that contains this `SKILL.md` (skill root), after `npm install`:

```bash
SOLANA_RPC_URL="${SOLANA_RPC_URL:-https://api.devnet.solana.com}" \
SOLANA_PRIVATE_KEY="<set-by-user-or-secrets>" \
npm run transfer -- --to "<RECIPIENT_PUBKEY>" --sol "<AMOUNT_SOL>"
```

- `--to` — base58 public key of the recipient.
- `--sol` — amount in SOL (decimal string or number, e.g. `0.01`).
- Optional: `--rpc <url>` overrides `SOLANA_RPC_URL`.

On success, report the **signature** (transaction id) and a **Solscan**
link (`explorerUrl` in CLI output) using the appropriate cluster (`devnet` vs `mainnet-beta`).

On failure, report the error message from the script without exposing secrets.

## Execution constraints (important)

- Use only this command path: `npm run transfer -- --to ... --sol ...`.
- Do not switch to `scripts/transfer_sol.py`, `.skill` bundles, or any Python flow.
- Do not require `solana` CLI for this skill; transfers are sent via `@solana/web3.js`.

## Mandatory user-facing workflow

Always show a visible step plan before execution and mark completed steps with a
green indicator.

Use this exact checklist style in chat:

- `🟩 Step 1 - Collect input` when done, otherwise `⬜ Step 1 - Collect input`
- `🟩 Step 2 - Validate input` when done, otherwise `⬜ Step 2 - Validate input`
- `🟩 Step 3 - User confirmation` when done, otherwise `⬜ Step 3 - User confirmation`
- `🟩 Step 4 - Execute transfer` when done, otherwise `⬜ Step 4 - Execute transfer`
- `🟩 Step 5 - Report result` when done, otherwise `⬜ Step 5 - Report result`

### Step 1 - Collect input (ask if missing)

Required input:

- recipient address (`to`)
- amount in SOL (`sol`)
- network (`devnet` or `mainnet-beta`, default `devnet`)

If any field is missing, ask follow-up questions. Do not execute until all fields
are present.

### Step 2 - Validate input

Validate:

- recipient is a valid base58 Solana address
- amount is numeric and positive
- network is one of: `devnet`, `mainnet-beta`

If validation fails, explain the exact invalid field and stop.

### Step 3 - User confirmation (strict gate)

Before running any command, send a confirmation summary and ask user to confirm:

- `To`: recipient
- `Amount`: SOL amount
- `Network`: selected network
- `Source wallet`: signer public key (if available)

Only continue on explicit confirmation such as: `confirm`, `yes`, or equivalent.
If user rejects/corrects any value, cancel current run and return to Step 1.

### Step 4 - Execute transfer

Run only after confirmation:

```bash
SOLANA_RPC_URL="${SOLANA_RPC_URL:-https://api.devnet.solana.com}" \
SOLANA_PRIVATE_KEY="<set-by-user-or-secrets>" \
npm run transfer -- --to "<RECIPIENT_PUBKEY>" --sol "<AMOUNT_SOL>"
```

### Step 5 - Report result

If transaction succeeds, the response must include:

- `Successfully` + icon (`✅` or `🎉`)
- transaction signature
- explorer URL
- network and amount

Success response template:

`✅ Successfully transferred <AMOUNT_SOL> SOL to <RECIPIENT> on <NETWORK>.`

If transaction fails, report concise failure reason and suggest the next safe action
(retry with corrected input, check balance, or switch network).

## Response style (concise + polished)

Keep all user-facing messages short, clear, and visually clean.

- Max 4-6 lines per response.
- Use compact bullets (`-`) or short blocks; no long paragraphs.
- Show only essential fields: amount, to, network, signature, explorer URL.
- For confirmations, ask one short yes/no question.

### Confirmation message format

Use this exact compact template before execution:

`Confirm this transaction?`
`- Amount: <AMOUNT_SOL> SOL`
`- To: <RECIPIENT>`
`- Network: <NETWORK>`
`Reply: yes / no`

### Success message format

Use this exact compact template on success:

`✅ Successfully transferred <AMOUNT_SOL> SOL`
`- To: <RECIPIENT>`
`- Network: <NETWORK>`
`- Signature: <SIGNATURE>`
`- Explorer: <EXPLORER_URL>`

### Failure message format

Use this exact compact template on failure:

`❌ Transfer failed: <SHORT_REASON>`
`- Network: <NETWORK>`
`- Next: check amount/address/balance and confirm to retry`

## Extending this skill

Implementation lives under `src/` (shared Solana helpers) and `scripts/` (one thin entry per user-facing command). Add new Solana features by new modules + a new script, then update this file so the agent knows when to use them.
