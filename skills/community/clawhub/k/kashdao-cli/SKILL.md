---
name: kashdao-cli
description: Trade prediction markets non-custodially via the official KashDAO CLI (@kashdao/cli) — markets list/get, quotes, trade buy/sell with idempotency + high-value confirmation, portfolio + webhooks management, and request tracing. Both Kash-orchestrated (REST API) and self-orchestrated (direct-to-chain via @kashdao/protocol-sdk) modes from a single binary.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env: [KASH_API_KEY]
      bins: [kash]
    primaryEnv: KASH_API_KEY
    envVars:
      - name: KASH_API_KEY
        required: true
        description: Kash API key. `kash_test_*` prefix auto-routes to the staging environment (api-staging.kash.bot); `kash_live_*` routes to production (lands at v1.0). Request one by emailing `engineering@kash.bot` with your intended use case.
      - name: KASH_BASE_URL
        required: false
        description: Override the auto-routed API base URL. Use only when you want to pin a specific environment regardless of the key's prefix.
      - name: KASH_PROFILE
        required: false
        description: Select a named CLI profile from `~/.kash/config.json`. Defaults to `default`.
    install:
      node: '@kashdao/cli@latest'
    emoji: '🎯'
    homepage: https://github.com/KashDAO/cli
    os: [macos, linux, windows]
---

# Kash — Prediction Markets CLI

Official command-line interface for the [Kash](https://kash.bot)
prediction-market protocol. This skill teaches you how to drive the
`kash` binary against real markets — placing trades, reading
positions, and managing webhook deliveries — all from a single CLI.

> 🧪 **Staging release.** Today only `kash_test_*` keys work; the CLI
> auto-routes them to `https://api-staging.kash.bot/v1`. Production
> endpoints and self-service key issuance land with v1.0. Request a
> staging key by emailing `engineering@kash.bot` with your use case.

## Trust model — non-custodial by construction

Every Kash path is non-custodial: Kash never holds funds, never moves
funds, never holds keys, and never signs anything. User funds always
live in Privy-managed MPC smart accounts the user controls. The CLI
holds zero balances; the API key is a scoped, revocable delegation
the user issues against their own account. See
[SECURITY.md § Non-custodial design](https://github.com/KashDAO/cli/blob/main/SECURITY.md#non-custodial-design)
for the full statement.

## Install

```sh
npm install -g @kashdao/cli@latest
```

Requires Node.js 22+. Verify:

```sh
kash --version
```

## Authenticate

Store the API key once:

```sh
kash auth set-key kash_test_…
```

Persisted to `~/.kash/config.json` at mode `0600`. The CLI never
writes the raw key to disk in any other location. To override
per-shell without persisting, set `KASH_API_KEY` in the environment.

## Core commands

Every command supports `--json` for stable machine-readable output
(single object on stdout; errors on stderr with the documented
[Kash error envelope](https://docs.kash.bot/developer-docs/api-errors)).
Pin to `--json --quiet` for AI-agent flows.

### Browse markets

```sh
# List active markets
kash markets list --status ACTIVE --limit 20 --json

# Get one market's full state
kash markets get <market-id> --json
```

### Quote before trading

Quotes simulate price impact without moving funds:

```sh
# How much YES will $10 USDC buy?
kash quote buy <market-id> --outcome 0 --amount 10 --json

# How much USDC do I get for 5 outcome tokens?
kash quote sell <market-id> --outcome 0 --tokens 5 --json
```

### Trade lifecycle

```sh
# Buy and wait for terminal status (executed | failed | rejected)
kash trade buy <market-id> --outcome 0 --amount 10 --wait \
  --auto-idempotency-key --json

# Inspect a trade
kash trade status <trade-id> --json

# List recent trades
kash trade list --limit 50 --filter status=executed --json

# Close a position
kash trade sell <market-id> --outcome 0 --amount 5 --wait \
  --auto-idempotency-key --json
```

`--auto-idempotency-key` is **mandatory** in agent flows — it makes
the request safe to retry; replays return the cached response, so
network blips never double-execute a trade.

### High-value confirmation

Trades above the key's `high_value_threshold_usdc` return a
two-phase response:

```sh
# 1. Submit (returns pending_confirmation + a one-time token)
RESP=$(kash trade buy <market-id> --outcome 0 --amount 5000 --json)
TOKEN=$(echo "$RESP" | jq -r '.confirmation.token')
TRADE_ID=$(echo "$RESP" | jq -r '.id')

# 2. Confirm with the token (60s window)
kash trade confirm "$TRADE_ID" --token "$TOKEN" --json
```

### Portfolio

```sh
# Smart-account state, USDC balance, position summary
kash portfolio show --json

# Open positions across markets
kash portfolio positions --json
```

### Webhooks

```sh
# List recent deliveries
kash webhooks list --limit 10 --json

# Redeliver a specific event
kash webhooks redeliver <event-id> --json

# Rotate the webhook signing secret (60s cooldown)
kash webhooks rotate-secret --json
```

### Request tracing

Every API response carries a `requestId`. Use it to walk the
end-to-end event chain across services:

```sh
kash trace <correlation-id> --json
```

## Self-orchestrated direct-to-chain mode

The CLI also wraps `@kashdao/protocol-sdk` for fully self-orchestrated
trading — bring your own RPC, signer, and (optionally) bundler; the
Kash backend isn't in the path at all.

```sh
# Read the on-chain market state via your RPC
kash protocol market <market-address> --json

# Quote on-chain
kash protocol quote <market-address> --side buy --outcome 0 \
  --amount 10 --json
```

Profile fields needed for protocol mode: `rpcUrl`, `smartAccount`,
optionally `bundlerUrl`/`bundlerProvider`, and `signerKeyRef`
(`file:<path>` or `env:<NAME>` — the raw key never persists).

## Error handling

Every error envelope follows the same shape:

```json
{
  "ok": false,
  "error": {
    "code": "STABLE_ERROR_CODE",
    "message": "Human-readable summary",
    "recoverable": true,
    "suggestion": "Concrete next step",
    "retryAfterMs": 5000,
    "actions": [{ "type": "wait_and_retry", "delayMs": 5000, "description": "…" }],
    "requestId": "uuid",
    "docsUrl": "https://docs.kash.bot/developer-docs/api-errors/…"
  }
}
```

Branch on `actions[0].type` for machine-readable recovery: `wait_and_retry`,
`run_command`, `set_env`, `open_url`, `check_input`. Or look up
`kash explain <CODE>` for a structured catalog entry.

## Useful flags for agent flows

| Flag                     | Purpose                                                           |
| ------------------------ | ----------------------------------------------------------------- |
| `--json`                 | Stable machine-readable output. Always use in agent flows.        |
| `--quiet`                | Suppress progress logs; only the final JSON object on stdout.     |
| `--auto-idempotency-key` | Auto-generate `Idempotency-Key`. Mandatory for trade write paths. |
| `--wait`                 | Block until terminal status. Pairs with `--wait-timeout-ms`.      |
| `--profile <name>`       | Select a named profile (multi-account / multi-env workflows).     |
| `--base-url <url>`       | Override the auto-routed base URL.                                |
| `--timeout-ms <n>`       | Override the per-request timeout (default 30s).                   |

## Reference

- **Full command reference**: `kash docs --json` (returns the full
  command tree as machine-readable JSON) or the Mintlify-rendered
  pages at <https://docs.kash.bot/developer-docs/cli>.
- **REST API reference**: <https://docs.kash.bot/developer-docs/rest-api/overview>
- **Error catalog**: <https://docs.kash.bot/developer-docs/api-errors>
- **GitHub**: <https://github.com/KashDAO/cli>
- **npm**: <https://www.npmjs.com/package/@kashdao/cli>
- **Support / staging-key requests**: `engineering@kash.bot`
