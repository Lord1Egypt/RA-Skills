---
name: gp-cli-skill
description: >-
  Close empty Solana SPL token accounts and reclaim locked rent SOL back
  to your wallet, track Ghost Point earnings, claim SOUL tokens at the end
  of each weekly epoch, manage multiple encrypted wallets, and view
  lifetime and per-epoch stats — all from the command line. Use when the
  user wants to close empty SPL token accounts, reclaim rent SOL, check how many Ghost Points they've earned, claim SOUL rewards.
license: Proprietary — see LICENSE.md
metadata:
  author: graveyardprotocol
  version: 1.2.2
  source_repository: https://github.com/graveyardprotocol/gp-cli
  security:
    private_keys_transmitted: false
    local_transaction_signing: true
    agent_handles_secrets: false
    wallet_storage: local_filesystem
  openclaw:
    requires:
      bins:
        - node
        - npx
        - gp-cli
    secrets: []
---

# Graveyard Protocol CLI (gp-cli)

`gp-cli` is an open-source command-line tool for interacting with Graveyard Protocol on Solana. It scans your wallets for empty SPL token accounts, closes them in
batches, and returns the locked rent SOL to your wallet. Ghost Points are earned per closed account and accumulate toward weekly SOUL token distributions.

### Source Code

The `gp-cli` tool is open source and its implementation can be reviewed publicly.

Repository:
https://github.com/graveyardprotocol/gp-cli

The CLI builds and signs the transactions locally and only submits signed
transactions to the Graveyard Protocol backend. Private keys are never
transmitted over the network.

> [!IMPORTANT]
> **This skill only instructs agents to execute the `gp-cli` command-line tool.** 
>  The gp-cli tool has `--json` mode for all the command outputs for better machine readability. Agents can use this option for parsing results programmatically.

## Install and Set up requirements

```bash
npm install -g @graveyardprotocol/gp-cli
```

If installed globally, agent can use the shorter `gp` command:

```bash
gp add-wallet --keypair-file id.json --name "Main wallet" --json
```

Requires Node.js >= 20.

## Add/Remove Wallets
You can add as many wallets you want for rent reclaimation. Any wallet keypair is registered once and the CLI encrypts it with AES-256-GCM (PBKDF2 key derivation,
100 000 iterations) and stores it locally in `~/.gp-cli/wallets.json`.  

```bash
gp add-wallet --keypair-file ~/.config/solana/id.json --name "Main Wallet" --json 

gp list-wallets --json                      # show all saved wallets

gp remove-wallet --wallet <address> --json  # remove wallet
```

## Close Empty Token Accounts

Scan all or a specified wallet for empty SPL token accounts and close them, returning locked rent to the respective wallet(s). `-y or --yes` option provide auto confirmation to the `Close empty accounts?` interactive prompt.

```bash
gp close-empty --wallet <address> --yes --json    # target a specific walletskip confirmation prompt

gp close-empty --all -y --json                 # all saved wallets, auto-confirm

gp close-empty --wallet <address> --dry-run --yes --json  # preview — no transactions sent
```

**Flow:**
1. Operator or agent adds as many wallets for rent reclaimation during config setup.
2. Agent runs Close-empty command. 
3. Based on the command options, Backend scans the wallet(s) on-chain for empty token accounts
4. CLI provides scan summary as received from backend (accounts found, SOL to reclaim, protocol fee, Ghost Points to earn) and asks for confirmation in case `-y` or `--yes` option was not used. 
5. If confirmed, CLI builds Transaction batches based on total number of accounts; the CLI signs each batch locally and sends only the signed bytes to backend.
6. Backend submits batches of signed transactions only and returns results to agent

**Protocol economics per batch:**

| Item | Value |
|---|---|
| Protocol fee | 20% of reclaimed rent |
| You receive |  80% of total locked SOL |
| Ghost Points | 100 points per closed account |


## Check Stats

Show Ghost Point earnings, SOL reclaimed, and SOUL allocations for the
current and previous epoch, plus lifetime totals.

```bash
gp stats --wallet <address> --json           # specific wallet (saved or any address)

gp stats --all --json                        # summary JSON for all saved wallets

gp stats --wallet <address> --yes --json     # auto-write CSV without prompting

gp stats --wallet <address> --csv-out ~/report.csv --json   # write CSV to path
```

Stats output includes:

- **Lifetime:** total accounts closed, total SOL recovered, total SOUL claimed
- **Current epoch:** accounts closed, SOL earned, Ghost Points, Ghost share %
- **Previous epoch:** same fields, plus SOUL allocated and claim state

Epochs run weekly starting Monday 00:00 UTC.

## Claim SOUL Tokens

At the close of each weekly epoch, SOUL tokens are distributed
proportionally based on each wallet's share of total Ghost Points earned.
Use `gp claim-soul` to claim them on-chain.

```bash
gp claim-soul --wallet <address> --json      # specific wallet

gp claim-soul --all --json                   # claim for all saved wallets

gp claim-soul --wallet <address> --dry-run --json  # preview amount — no tx sent
```

**Important:** SOUL transfers are signed and submitted entirely in the
Graveyard Protocol backend by Project's Community Wallet keys — no local keypair signing is required.

Before claiming, the CLI shows:
- Epoch period
- Accounts closed and SOL earned that epoch
- Your Ghost Points and share % of the epoch total
- SOUL amount to be claimed

## Agent / CI Usage

Combine `--all`, `--wallet`, `--yes`, and `--json` command options for fully unattended agent/CI pipelines.

```bash
# Add a wallet non-interactively
gp add-wallet --keypair-file ~/.config/solana/id.json --name "Bot" --json

# Close empty accounts — auto-confirm, JSON output
gp close-empty --wallet <address> --yes --json

# Close for all wallets
gp close-empty --all --yes --json

# Fetch stats as JSON
gp stats --wallet <address> --json
gp stats --all --json

# Claim SOUL (auto-confirms in JSON mode)
gp claim-soul --wallet <address> --json
gp claim-soul --all --json
```

## Structured Output

Every command supports `--json` for machine-readable output. The default
human-readable output uses ANSI formatting, tables, and colour — suitable
for direct reading. Use `--json` when scripting or chaining commands.

When `--all` is used with `close-empty`, one JSON object is emitted per
wallet as it completes (newline-delimited JSON), so results can be streamed
and parsed in real time.

**`gp add-wallet --json`**
```json
{ "success": true, "publicKey": "...", "encrypted": true, "name": "Bot" }
```

**`gp list-wallets --json`**
```json
{
  "success": true,
  "wallets": [{ "publicKey": "...", "name": "Bot", "encrypted": false }]
}
```

**`gp close-empty --json`**
```json
{
  "success": true,
  "wallet": "...",
  "dryRun": false,
  "totalBatches": 3,
  "transactionsSucceeded": 3,
  "transactionsFailed": 0,
  "accountsClosed": 42,
  "solReclaimed": 0.085764,
  "results": [
    {
      "intentID": "...",
      "txSignature": "...",
      "batchAccountsClosed": 14,
      "batchRentSol": 0.028588,
      "success": true
    }
  ]
}
```

**`gp stats --json`**
```json
{
  "success": true,
  "wallets": [{
    "walletAddress": "...",
    "description": "",
    "userStats": {
      "totalAccountsClosed": 120,
      "totalSolsRecovered": 0.244800,
      "totalSoulClaimed": 5.000000
    },
    "currentEpoch": {
      "epochStartDate": 20260324,
      "userGhostEarned": 4200,
      "userGhostReferrals": 420,
      "userGhostTotal": 4620,
      "userAccountsClosed": 42,
      "userSolsRecovered": 0.085764,
      "totalUsers": 1337,
      "totalGhostEarned": 9999999,
      "ghostSharePct": "0.0462"
    },
    "previousEpoch": {
      "epochStartDate": 20260317,
      "userGhostEarned": 3000,
      "userGhostReferrals": 300,
      "userGhostTotal": 3300,
      "userAccountsClosed": 30,
      "userSolsRecovered": 0.061200,
      "userSoul": 1.234567,
      "claimState": "No",
      "totalUsers": 1200,
      "totalGhostEarned": 8500000,
      "totalSoul": 10000.000000,
      "ghostSharePct": "0.0388"
    }
  }]
}
```

**`gp claim-soul --json`**
```json
{
  "success": true,
  "wallets": [{
    "wallet": "...",
    "status": "claimed",
    "epochStartDate": 20260317,
    "soulClaimed": 1.234567,
    "txSignature": "..."
  }]
}
```

**`claim-soul` status values:**

| Status | Meaning |
|---|---|
| `claimed` | SOUL successfully claimed on-chain |
| `dry_run` | Dry-run preview — no transaction submitted |
| `already_claimed` | SOUL was already claimed for this epoch |
| `in_progress` | A claim is currently in flight |
| `no_soul` | No SOUL allocated for this wallet this epoch |
| `no_epoch` | No previous epoch data found |
| `aborted` | User declined the interactive confirm prompt |
| `error` | Unexpected failure — see `.error` field |

On any error:
```json
{ "success": false, "error": "..." }
{ "success": false, "wallet": "...", "error": "..." }
```

## Epochs & Ghost Points

Epochs run weekly, starting Monday 00:00 UTC. Ghost Points are earned at
100 points per closed account. At epoch close, SOUL tokens are distributed proportionally based on
each wallet's share of total Ghost Points.

Use `gp stats` to track your Ghost share % for the current and previous epoch, and
`gp claim-soul` to collect SOUL allocated for the previous epoch.

## Tips

- **Check before closing.** Use `--dry-run` on `close-empty` first as a simulation
  before any transaction is submitted.
- **`--json` requires `--wallet` or `--all`.** In JSON mode the interactive
  wallet picker is suppressed. Always pass an explicit wallet address or
  `--all` flag.
- **`--json` auto-confirms.** In JSON mode the "close accounts?" and "claim
  SOUL?" prompts can be skipped by using `--yes` as default response— transactions proceed automatically.
- **No signing for SOUL claims.** `gp claim-soul` does not require
  your keypair for signing. Your wallet public-key is sufficient. The SOUL tokens are transferred from Project's Community Wallet making it the transaction Signer and The backend handles signing entirely. 
- If the encrypted wallet key cannot be decrypted for transaction signing due to any reason such as data corruption, you can remove and re-add the
  wallets — on-chain history and funds are unaffected.
- **`epochStartDate` is an integer in `YYYYMMDD` format** — e.g. `20260317`
  means 17 March 2026. Parse it as a string when formatting dates.
- **`solReclaimed` is already net of the 20% protocol fee** in the
  `close-empty` JSON output. The `batchRentSol` fields in `results[]` also
  reflect the net amount returned to the wallet.

## Agent Safety Guidelines

Agents using this skill MUST follow these restrictions:

- Do not read, modify or access `~/.gp-cli/wallets.json` directly
- Do not request or expose private keys by any means
- Do not pass private keys on the command line
- Only execute documented `gp` commands

## Security Model

CLI stores the wallets in  `~/.gp-cli/wallets.json` (file mode `600`, readable only by the owner) which is encrypted at rest with AES-256-GCM (PBKDF2 key derivation, 100 000 iterations).

Agent does not access `~/.gp-cli/wallets.json` file directly. It instead uses add, remove and list commands for wallet operations. Agent can only provide the path to keypair json file when adding the wallet to gp-cli configuration.

Transactions are build and signed locally within the CLI. Only signed transactions are submitted to the Graveyard Protocol backend. Private keys are not transmitted in any form.


## Troubleshooting

**"Scan cache expired — please rescan"**
The batch count endpoint returned 0 after a successful scan. You may need to run
`gp close-empty` again — the cache has a short TTL.

**"No empty token accounts found"**
The wallet has no empty SPL token accounts to close. Nothing to do.

**"Failed to decrypt wallet"**
The wallet entry is corrupted. Run
`gp remove-wallet` and `gp add-wallet` to re-add the wallet.

**Network errors / `Non-JSON response`**
The Graveyard Protocol API at `https://api.graveyardprotocol.io` was
unreachable or returned an unexpected response. Check connectivity and
retry.
