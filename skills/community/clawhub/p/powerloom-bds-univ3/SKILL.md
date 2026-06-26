---
name: powerloom-bds-univ3
description: |
  Autonomous Uniswap V3 monitoring on consensus-backed data with onchain provenance.
  Every data point is finalized on-chain by Powerloom's DSV network and independently
  verifiable. Ships with Whale Radar, Token-Flow, and DeFi Analyst recipes.
  Free API key at bds-metering.powerloom.io/metering (2 credits, no wallet).
  Triggers on "whale alert", "track trades", "all trades for", "by token",
  "Powerloom", "verify on-chain", "verified data".
version: 0.2.6
homepage: https://bds-metering.powerloom.io
repository: https://github.com/powerloom/powerloom-bds-univ3
tags:
  - defi
  - uniswap
  - ethereum
  - on-chain
  - verifiable
  - consensus
  - agent
metadata:
  openclaw:
    emoji: "🦄"
    requires:
      bins: ["node"]
      env:
        # Only POWERLOOM_API_KEY is mandatory at install time. The free-key path
        # (references/09-openclaw-one-shot-free-key.md) needs nothing else from
        # this skill's perspective. Wallet/plan envs below are optional and only
        # consumed by scripts/signup-pay.mjs and scripts/credits-topup.mjs.
        - POWERLOOM_API_KEY
      optional_env:
        # Wallet-funded variants (signup-pay or credits-topup) — only required
        # if the user invokes those scripts. See references/08-openclaw-one-shot.md.
        - POWERLOOM_EVM_PRIVATE_KEY
        - POWERLOOM_EVM_RPC_URL
        - POWERLOOM_EVM_CHAIN_ID
        - POWERLOOM_PLAN_ID
        - POWERLOOM_TOKEN_SYMBOL
        # Dispatch + transport overrides — never required.
        - POWERLOOM_MCP_URL
        - POWERLOOM_TELEGRAM_BOT_TOKEN
        - POWERLOOM_TELEGRAM_CHAT_ID
        - POWERLOOM_DISCORD_WEBHOOK_URL
        - POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS
        - POWERLOOM_BDS_MCP_DEBUG
        - POWERLOOM_METERING_BASE_URL
        - POWERLOOM_AGENT_NAME
        - POWERLOOM_EMAIL
---

# Powerloom BDS — Uniswap V3

## Install

> **Two onboarding paths.**
>
> **Free** — sign up at [`bds-metering.powerloom.io/metering`](https://bds-metering.powerloom.io/metering) (enter email + agent name, complete Turnstile, get `sk_live_...` immediately — no CLI, no wallet, 2 free credits). Alternatively, `bds-agent signup` runs the same flow from the terminal. Then paste [`references/09-openclaw-one-shot-free-key.md`](references/09-openclaw-one-shot-free-key.md) into OpenClaw. Sets `POWERLOOM_API_KEY` and a Whale Radar cron. Nothing else needed.
>
> **Wallet-funded** — paste [`references/08-openclaw-one-shot.md`](references/08-openclaw-one-shot.md) and `scripts/signup-pay.mjs` runs an autonomous on-chain payment for a 10-credit plan in the same prompt.
>
> **⚠️ WARNING — wallet-funded path only:** `signup-pay.mjs` and `credits-topup.mjs` need an EVM private key to broadcast on-chain payments. Use a **burner wallet** with limited funds dedicated to this purpose. Never use a wallet holding significant assets or with extensive transaction history for agentic setups. The free-key path **does not** require any wallet credentials.

**Contract:** [bds-agenthub-billing-metering](https://github.com/powerloom/bds-agenthub-billing-metering). **ClawHub** users only need a **single origin** (default [bds-metering.powerloom.io](https://bds-metering.powerloom.io))— **`bds-agent` commands are optional**; they are a reference CLI for the same JSON bodies you can send with `curl` + a wallet or `ethers`.

### Metering HTTP (authoritative)

| What | How |
|------|-----|
| List SKUs | `GET {BASE}/credits/plans` — no auth. Choose a plan row: `id`, `chain_id`, `token_symbol` (and note `payment_kind`: ERC-20 vs native / CGT). **`chains[].rpc_url`** is a **public** JSON-RPC hint only when the metering deployment sets it; it may be **empty** — use **`POWERLOOM_EVM_RPC_URL`** for wallet / script calls in that case. |
| New key, wallet-only | **Pay-signup:** `POST {BASE}/signup/pay/quote` → pay on chain → `POST {BASE}/signup/pay/claim` with `signup_nonce` + `tx_hash`. Returns `api_key`. |
| New key, browser | Human device flow on [`{BASE}/metering`](https://bds-metering.powerloom.io/metering) (same service). Enter email + agent name, complete Turnstile, get `sk_live_...` immediately. |
| More credits, existing key | `POST {BASE}/credits/topup` with `Authorization: Bearer sk_live_…` and tx / plan (not the pay-signup endpoints). |
| Check balance | `GET {BASE}/credits/balance` with `Authorization: Bearer …` |

`{BASE}` is **`POWERLOOM_METERING_BASE_URL`**, e.g. `https://bds-metering.powerloom.io`. Set **`POWERLOOM_API_KEY`** to the `sk_live_...` you get after pay-signup, device signup, or copy from the dashboard.

### OpenClaw env vars (mandatory vs optional)

| Field | When required | Role |
|-------|---------------|------|
| `POWERLOOM_API_KEY` | **Always** — only mandatory env at install time | `sk_live_...` from [`bds-metering.powerloom.io/metering`](https://bds-metering.powerloom.io/metering) or `bds-agent signup` (free path) or `signup-pay.mjs` claim (wallet path) |
| `POWERLOOM_EVM_PRIVATE_KEY` | Wallet-funded path only | Payer wallet — **use a burner wallet** |
| `POWERLOOM_EVM_RPC_URL` | Wallet-funded path only | JSON-RPC for that chain |
| `POWERLOOM_EVM_CHAIN_ID` | Wallet-funded path only | Must match the plan's `chain_id` |
| `POWERLOOM_PLAN_ID` | Wallet-funded path only | e.g. `launch_10_pl_power_cgt` from `GET /credits/plans` |
| `POWERLOOM_TOKEN_SYMBOL` | Wallet-funded path only | e.g. `POWER` (must match that row) |

The schema in `metadata.openclaw.requires.env` lists only `POWERLOOM_API_KEY` as required; the wallet/plan envs above sit in `optional_env` and are read only by `scripts/signup-pay.mjs` (new key, pay-signup) and `scripts/credits-topup.mjs` (more credits on an existing key). Free-key flows pass straight through.

### Reference client: `bds-agent` (optional)

[docs/USER_GUIDE.md](https://github.com/powerloom/bds-agent-py/blob/main/docs/USER_GUIDE.md) in **bds-agent-py** has the end-to-end order: **Metering service API** table → pay-signup → device → top-up. One-liner sequence:

1. `bds-agent credits plans` — same as `GET /credits/plans`
2. `bds-agent credits setup-evm` — writes `~/.config/bds-agent/profiles/<name>.evm.env`
3. `bds-agent signup-pay --plan-id … --chain-id … --token-symbol …` — implements quote / broadcast / claim (including **native** `payment_kind` plans)

### This repo: Node scripts (no Python, no `bds-agent` required)

| Script | What it does |
|--------|----------------|
| `node scripts/signup-pay.mjs` | **New** key: pay-signup (quote → on-chain pay → claim). Uses **`quote.payment_kind`**: `native_value` = send **native/CGT** (`tx.value` to `recipient`); `erc20` = token **`transfer`**. For **POWER (7869) CGT** plans, metering uses **`native_value`** — do not force ERC-20. **Broadcast protection:** interactive shells prompt `CONFIRM`; non-interactive shells require **`--yes`** (preferred for OpenClaw — ephemeral argv, do not persist in skill env) **or** `POWERLOOM_SIGNUP_PAY_CONFIRM=yes` (CI one-shot only). **`--dry-run`** prints quote summary and exits without sending a tx. |
| `node scripts/credits-topup.mjs` | **More** credits: uses existing **`POWERLOOM_API_KEY`**, fetches `GET /credits/plans`, matches **`POWERLOOM_PLAN_ID` + `POWERLOOM_EVM_CHAIN_ID` + `POWERLOOM_TOKEN_SYMBOL`**, sends **ERC-20** or **native** per `payment_kind`, then **`POST /credits/topup`**. Same confirmation gate as signup-pay (**`--yes`** preferred; **`POWERLOOM_CREDITS_TOPUP_CONFIRM=yes`** for CI one-shot only; TTY `CONFIRM`). **`--dry-run`** prints summary only. Set **`POWERLOOM_EVM_RPC_URL`** when **`chains[].rpc_url`** is empty or you need a specific node (the API never exposes the server's private RPC). |
| `node scripts/ensure-credits.mjs` | **Balance** only (`GET /credits/balance`); no purchase. |

`npm install` once (adds `ethers`).

**Optional env (signup script):** `POWERLOOM_METERING_BASE_URL`, `POWERLOOM_AGENT_NAME`, `POWERLOOM_EMAIL` (see [metering README](https://github.com/powerloom/bds-agenthub-billing-metering#readme)).

### After you have a key — more credits (top-up)

**Spec:** `POST {BASE}/credits/topup` with `Authorization: Bearer` and JSON `{ "plan_id", "chain_id", "tx_hash" }` after an on-chain payment that matches the plan. **In this repo:** `node scripts/credits-topup.mjs`. **Reference CLI:** [USER_GUIDE](https://github.com/powerloom/bds-agent-py/blob/main/docs/USER_GUIDE.md) (EVM `credits topup` / Tempo per deployment). **Check balance:** `node scripts/ensure-credits.mjs`.

**Default MCP endpoint:** `https://bds-mcp.powerloom.io/sse` — override with `POWERLOOM_MCP_URL` if needed.

Generic tool runner: `node scripts/powerloom-mcp-client.mjs <tool_name> '{}'`

## Common tasks → which tool

| Task phrase | Tool(s) |
|-------------|---------|
| Track **all swaps for token X** (multi-pool) | **Token-Flow** recipe (`bds_mpp_snapshot_trades_pool_address` per pool) or `bds_mpp_snapshot_allTrades` via **`whale-cron.mjs`** |
| **Whale** / USD threshold | **`whale-cron.mjs`** (all pools, bounded) or **`whale-radar.mjs`** (fixed pool list, per-pool snapshots) |
| **One pool only** | `bds_mpp_snapshot_trades_pool_address` after `bds_mpp_token_token_address_pools` or `bds_mpp_dailyActivePools` |
| **Verify** on-chain | `verify_data_provenance` with `cid`, `epoch_id`, `project_id` from API — never substitute block for epoch |

**Timeouts:** default `POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS=60000`. Raise it (e.g. **120000**) if `bds_mpp_snapshot_allTrades` times out under backlog.

## Recipes (supported surface)

Pre-built scripts + `recipes/*.yaml` defaults — prefer these over ad-hoc scripts on weaker models. **This skill does not call streaming catalog tools** (`bds_mpp_stream_*`); every recipe uses **bounded snapshot** MCP calls so runs fit cron and agent sandboxes.

**Cron default:** `whale-radar.mjs`, `token-flow.mjs`, and `defi-analyst.mjs` each run **one bounded round** and **exit** (safe for OpenClaw cron). Pass **`--daemon`** to repeat with `heartbeat.interval_seconds` between rounds (local / long-running only).

| Recipe / entrypoint | Script |
|---------------------|--------|
| Whale Radar (fixed pools) | `node scripts/whale-radar.mjs` — one round over `poll_fallback_pools`; **`--daemon`** for repeat |
| Whale alerts (cron, all pools) | `node scripts/whale-cron.mjs` — **bounded** one-shot: `bds_mpp_snapshot_allTrades` + pool metadata; alerts include **snapshot** `cid` / epoch / project from `data.verification` — see **Verification provenance** in `references/08-openclaw-one-shot.md` |
| Token-Flow | `node scripts/token-flow.mjs` (`--token 0x...`) — one round per pool for that token; **`--daemon`** for repeat |
| DeFi Analyst | `node scripts/defi-analyst.mjs` — one round: **multi-pool** (`bds_mpp_snapshot_allTrades` + all-pools volume) or `filters.scope: single_pool`; **`--daemon`** for repeat |

## Model guidance

Recipes produce the same stdout/Telegram output regardless of model. Ad-hoc "compose your own" prompts work best on GPT-4–class or GLM-5+; weaker local models may collapse multi-pool prompts onto one pool — **use the Token-Flow recipe** instead.

## Hosts & integrators (OpenClaw, cron, heartbeats)

**OpenClaw "one shot" setups** — pick the variant that matches the user's onboarding state:

| Variant | Use when | Reference |
|---------|----------|-----------|
| Free-key cron | The user already has `sk_live_...` from [`bds-metering.powerloom.io/metering`](https://bds-metering.powerloom.io/metering) or `bds-agent signup` (2 free credits, no wallet) | [`references/09-openclaw-one-shot-free-key.md`](references/09-openclaw-one-shot-free-key.md) |
| Pay-signup + cron | The user wants autonomous wallet-funded onboarding for a 10-credit plan in the same prompt | [`references/08-openclaw-one-shot.md`](references/08-openclaw-one-shot.md) |

Both prompts produce the same `Whale Radar` cron firing `node scripts/whale-cron.mjs` every 15s with onchain verification surfaced in every alert. Agents should default to the free-key variant unless the user explicitly asks for autonomous on-chain payment.

**Scheduled / cron-style runs:** Prefer **`whale-cron.mjs`**, **`whale-radar.mjs`**, **`token-flow.mjs`**, or **`defi-analyst.mjs`** with **no** `--daemon` so each invocation **exits**. **Streaming trade tools** (`bds_mpp_stream_*`) are **not** used by this skill.

## References

See `references/` for quickstart, full tool table, verification, credit budget, scope, troubleshooting, prompt patterns, **`08-openclaw-one-shot.md`** (copy-paste OpenClaw runbook), and cron notes in quickstart + tool catalog.
