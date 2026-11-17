---
name: jerithchain
description: >
  JerithChain (JER) wallet and chain client for OpenClaw. Local encrypted
  wallet, balances, indexed transaction history, on-chain sends with
  spending limits and fee estimates, network/supply status, block/tx
  queries, deposit watching, wallet backup/restore, and node-side mining
  (the node performs all proof-of-work and validates everything).
  Application-layer client of a JER node — never touches chain databases
  and never invents balances, txids, or rewards.
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🪙", "requires": {"bins": ["python3"], "files": [], "config": []}}}
---

# JerithChain (JER) skill

JER is the native coin of JerithChain — a standalone SHA-256 proof-of-work
blockchain (NOT a token on another chain). Balances are blockchain balances:
the skill only asks a JER node and reports what it says. **Never state a
balance, txid, height, or mined reward that the node did not return.**

## Setup (one time)

```bash
~/.openclaw/plugin-skills/jerithchain/jerith_skill.py wallet-create
```

Requires a reachable JER node (default `http://127.0.0.1:8300`) with its
exchange token readable (auto-detected at `~/.openclaw/jerith-coin/keys/exchange.token`,
or set `JERITH_SKILL_TOKEN` / `JERITH_SKILL_TOKEN_FILE`).

Wallet backup: `~/.config/jerith/` holds `skill-wallet.json` + `wallet.key`
(both required to spend). Use `wallet-backup` / `wallet-restore` (below) to
move or copy them safely.

## Command reference

Run via bash. Add `--json` for structured output (preferred for parsing).

```bash
J=~/.openclaw/plugin-skills/jerithchain/jerith_skill.py
$J wallet                # address + balance + height summary
$J address               # receiving address
$J balance               # confirmed balance (uJ + JER) + pending mempool
$J status                # connected node, height, tip, difficulty, versions
$J history --limit 10    # indexed tx history (explorer-backed)
$J supply                # circulating/emitted/max supply + next halving
$J estimate-fee 0.5      # total cost + whether it would send without prompting
$J send 5.0 JER1B0E257B00C8F7AA9B2733172C3764CD   # send (see safety below)
$J send 25.0 JER... --yes        # only AFTER the user explicitly confirmed
$J watch <txid> --target 20      # poll until N confirmations (or timeout)
$J block 11              # block details
$J blockhash 11          # block hash at height
$J tx <txid>             # transaction + confirmations
$J confirmations <txid>  # confirmation count vs standard (20)
$J netinfo               # node peer/diagnostics mirror
$J validate JER1B0E...   # offline address syntax check (no node needed)
$J wallet-backup ~/backups/jerith-$(date +%F).tar.gz
$J wallet-restore ~/backups/jerith-2026-10-08.tar.gz
$J mine --discord-id <id>        # mining attempt (node does the PoW)
$J mine --discord-id <id> --wait 330   # auto-retry through a cooldown
```

## Receiving and checking deposits

Give the user your address with `$J address`. After a deposit is expected,
verify it on-chain — never from memory:

- `confirmations <txid>` — one-shot count vs standard (20).
- `watch <txid> --target 20 --timeout 600` — polls until it reaches the
  target; reports `confirmed-at-target`, `pending (N confirmations)`, or
  `not yet in a block`. Never claim a deposit arrived before this says so.
- `history` — indexed in/out list with counterparty, memo, and
  confirmations (served by the local explorer API, port 8303).

## Pricing a send before committing

`estimate-fee <amount>` shows fee (0.1 JER), total, affordability against
the live balance, and — importantly for you — `needs_confirmation` and
`within_daily_limit`. Use it to explain a pending send to the user BEFORE
triggering the exit-3 confirmation flow. It sends nothing and records
nothing.

## Transaction confirmation rule (MANDATORY)

`send` refuses (exit 3, `status: confirmation_required`) any amount above
`automatic_send_limit_jer` (default **1 JER**) unless `--yes` is passed.
When you see that result you MUST ask the user to confirm and only re-run
with `--yes` after they agree. Never pass `--yes` on your own initiative for
large amounts. A hard daily limit (`daily_limit_jer`, default 10 JER) is
enforced client-side regardless — and is checked even for confirmed sends.

`validate <address>` checks address syntax offline (JER + 32 alphanumeric,
35 chars). It does NOT prove the address exists on chain or is controlled
by anyone in particular — but it does reject typos, traversal, and
injection strings before anything is built.

## Mining — what is true

- `mine` asks the NODE to mine. The node performs the proof-of-work, applies
  cooldowns and the reward schedule, and appends the block. The skill never
  mints anything.
- `ok: true` + `reward_jer` in the response means a real block was produced.
  Anything else means no JER was created — say so plainly.
- Cooldowns (5 min after success, 3 min after failure) are enforced by the
  node; `reason: cooldown` means exactly that. `--wait N` makes the skill
  poll for up to N seconds (30 s spacing) and report `waited_seconds` —
  prefer that over rapid manual retries.
- The credited identity is `--discord-id`, falling back to the
  `default_discord_id` config key. Mining is opt-in (`mining.enabled`),
  default off. Conversational mining (`--source passive --message-id <id>`)
  is deduplicated by the node and throttled client-side
  (`conversation_mining.daily_attempt_limit`).

## Wallet backup & restore

```bash
$J wallet-backup ~/backups/jerith.tar.gz   # refuses to overwrite without --force
$J wallet-restore ~/backups/jerith.tar.gz  # refuses to clobber without --force
```

The bundle is a tar.gz of the wallet + key file. **Anyone holding that file
controls the wallet's JER** — store it offline, never in chat uploads, and
mention the risk when you create one. Restores are verified by the address
they recover.

## Security rules for the agent

1. Never ask for, display, or transmit the wallet's private key. The skill
   has no command that prints it, by design.
2. Balances/heights/txids come only from command output. If the node is
   unreachable, say the node is unreachable — do not estimate.
3. A submitted transaction is NOT confirmed. Use `confirmations`/`watch`
   and compare against `standard_confirmations` (20). Report the count,
   never "confirmed" without it.
4. If a command fails, show the error to the user. Errors are written to be
   user-safe (insufficient balance, cooldown, limits).
5. Never edit the config to raise spending limits without explicit user
   request in the conversation.

## Configuration

`~/.config/jerith/skill-config.json` (all keys optional, defaults below):

```json
{
  "rpc_url": "http://127.0.0.1:8300",
  "explorer_url": "http://127.0.0.1:8303",
  "network": "mainnet",
  "wallet_path": "~/.config/jerith/skill-wallet.json",
  "default_discord_id": "",
  "spending": {
    "automatic_send_limit_jer": 1.0,
    "daily_limit_jer": 10.0,
    "require_confirmation": true
  },
  "mining": { "enabled": false },
  "conversation_mining": { "enabled": true, "daily_attempt_limit": 50 },
  "http_timeout_seconds": 20,
  "cache_seconds": 15
}
```

Env: `JERITH_SKILL_TOKEN` (node API token), `JERITH_SKILL_TOKEN_FILE`,
`JERITH_SKILL_CONFIG`, `JERITH_SKILL_KEYDIR`, `JERITH_SKILL_STATE_DIR`
(send-state location; tests/parallel instances should isolate it).

## Troubleshooting

- `offline` / cannot reach node → check `systemctl --user status jerith-coin-node`
- `HTTP 401` → exchange token missing/mismatched; set `JERITH_SKILL_TOKEN`
- `insufficient balance` → the on-chain balance (amount + 0.1 JER fee)
- `confirmation required` → ask the user, re-run with `--yes`
- `daily send limit exceeded` → wait for the UTC day to roll over or the
  user to explicitly raise `daily_limit_jer` in config
- `cooldown` → wait; or use `mine --wait` — the node enforces cooldowns
- wallet decryption failed → the wallet key file was replaced; restore from
  backup (`wallet-restore`)
- history unavailable → explorer not running (`explorer_url`); balance and
  sends still work via the node

## Limitations

- Balance cache ~15 s (configurable) to avoid hammering the node.
- History/supply need the local explorer (8303); everything else needs only
  the node (8300).
- The skill cannot recover a wallet whose `~/.config/jerith/wallet.key` and
  `skill-wallet.json` were both lost — keep a `wallet-backup` offline.
- `watch` stops at `--timeout`; a still-pending tx just needs re-running.
