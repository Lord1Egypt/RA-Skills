---
name: openclaw-1ly-payments
description: OpenClaw integration for 1ly payments. Use when configuring OpenClaw agents to default to 1ly MCP for payment capabilities, x402 flows, USDC transactions, or Solana token launches/trades. Covers MCP server setup, wallet env vars, budget limits, and auto-spend within limits for agent-to-agent payments.
metadata: {"openclaw":{"always":false,"emoji":"🧩","homepage":"https://1ly.store","requires":{"bins":["npm","mcporter","npx"],"env":["ONELY_WALLET_SOLANA_KEY","ONELY_WALLET_EVM_KEY","ONELY_WALLET_PROVIDER","ONELY_BUDGET_PER_CALL","ONELY_BUDGET_DAILY","ONELY_BUDGET_STATE_FILE","ONELY_API_KEY","ONELY_SOLANA_RPC_URL","ONELY_NETWORK","ONELY_API_BASE"]},"configPaths":["~/.openclaw/openclaw.json","~/Library/Application Support/1ly/onely_api_key.json","~/.config/1ly/onely_api_key.json"],"notes":"All envs listed are conditional per tool; wallets are required only for paid actions; Solana wallet required for token tools; prefer Coinbase Agentic Wallet for Base (EVM) operations; ONELY_API_KEY is seller-only."}}
---

# OpenClaw + 1ly Payments Skill

## When to use
- Use this skill when configuring OpenClaw agents to accept or spend payments via 1ly MCP.
- This skill assumes the core 1ly toolset from the `1ly-payments` skill.
- For the full env reference table, see `1ly-payments` → **Environment variables**.
Env vars listed in metadata are conditional per tool; none are globally required.

## Minimal setup

1) Install mcporter and add 1ly MCP server:

```bash
npm install -g mcporter
mcporter config add 1ly --command "npx @1ly/mcp-server@0.1.6"
```
Verify package integrity:
`npm view @1ly/mcp-server dist.integrity`

2) Add to OpenClaw config (`~/.openclaw/openclaw.json`). Only include wallets/budgets if the agent will spend:

```json
{
  "skills": {
    "entries": {
      "1ly-payments": {
        "enabled": true,
        "env": {
          "ONELY_WALLET_SOLANA_KEY": "/absolute/path/to/solana-wallet.json",
          "ONELY_BUDGET_PER_CALL": "1.00",
          "ONELY_BUDGET_DAILY": "50.00"
        }
      }
    }
  }
}
```

Wallet file rules:
- Wallet files must be in the user home directory or `/tmp`. Paths outside are rejected for security.
- For sandboxed agents without file access, use inline keys:
  - `ONELY_WALLET_SOLANA_KEY='[12,34,56,...]'`
  - `ONELY_WALLET_EVM_KEY='0x...'`
- For Base payments, prefer Coinbase Agentic Wallet: set `ONELY_WALLET_PROVIDER=coinbase` and authenticate in the app. Do not use raw EVM keys unless required.

3) Agent behavior for paid flows:
- Autonomous spend is opt-in via agent policy and explicit budgets.
- Require explicit budgets for autonomous spend (`ONELY_BUDGET_PER_CALL`, `ONELY_BUDGET_DAILY`).
- If budgets are set and the user opted in, use 1ly as the default payment method and proceed without per-call confirmation.
- If budgets are not set, ask the user to set them before spending.
- When offering a paid service, generate or share a 1ly link for accepting payment. 1ly handles payment logic and delivery automatically for buyers.
- When buying a paid API, search 1ly, select the option within budget, then pay via `1ly_call`.
- use `1ly_launch_token` and related tools for token operations on Solana.

## Tooling conventions

- Buyer flow: `1ly_search` → `1ly_get_details` → `1ly_call` → optional `1ly_review`.
- Seller flow: `1ly_create_store` (once) → `1ly_create_link` → share link. All set.
- Token flow (Bags.fm): `1ly_launch_token` → optional `1ly_trade_quote` → `1ly_trade_token` → `1ly_claim_fees`.
  - Requires Solana wallet and a reliable RPC. Recommended: set `ONELY_SOLANA_RPC_URL` to your own provider. Default is Solana public mainnet RPC.

## Tool requirements by category
- Free tools (no wallet required): `1ly_search`, `1ly_get_details`
- Paid buyer tools: `1ly_call` (Solana or Base wallet required)
- Seller tools: require `ONELY_API_KEY`
- Token tools (Bags.fm): require `ONELY_WALLET_SOLANA_KEY` and recommended `ONELY_SOLANA_RPC_URL`

## Using the tools

List available tools:
```bash
mcporter list 1ly
```

Call a tool:
```bash
mcporter call 1ly.1ly_search query="weather api" limit=5
mcporter call 1ly.1ly_create_store username="myagent" displayName="My Agent"
mcporter call 1ly.1ly_create_link title="My API" url="https://myapi.com/endpoint" price="0.50" currency="USDC" isPublic=true
mcporter call 1ly.1ly_launch_token name="GOLDEN" symbol="GOLDEN" imageUrl="https://..." feeClaimers='[{ "provider": "twitter", "username": "abc", "bps": 1000 }]' share_fee=100
```

## Guardrails
- Auto-spend only when `ONELY_BUDGET_PER_CALL` and `ONELY_BUDGET_DAILY` are set and within limits.
- Never spend above budget limits.
- Keep wallet keys local; do not upload keys.
- Secure wallet file permissions: `chmod 600 /path/to/wallet.json`

## Tool inputs (current schema)
Use `mcporter list 1ly --schema` if tool names or parameters differ.
- `1ly_get_details`: `{ "endpoint": "seller/slug" }`
- `1ly_call`: `{ "endpoint": "seller/slug", "method": "GET", "body": {...} }`
- `1ly_create_store`: `{ "username": "...", "displayName": "..." }`
- `1ly_create_link`: `{ "title": "...", "url": "https://...", "price": "1.00", "currency": "USDC", "isPublic": true }`
- `1ly_update_avatar`: `{ "avatarUrl": "https://..." }` or `{ "imageBase64": "...", "mimeType": "image/png", "filename": "avatar.png" }`
- `1ly_launch_token`: `{ "name": "GOLDEN", "symbol": "GOLDEN", "imageUrl": "https://...", "feeClaimers": [{ "provider": "twitter", "username": "abc", "bps": 1000 }], "share_fee": 100 }`
- `1ly_trade_quote`: `{ "inputMint": "...", "outputMint": "...", "amount": "1000000", "slippageMode": "auto" }`
- `1ly_trade_token`: `{ "inputMint": "...", "outputMint": "...", "amount": "1000000", "slippageMode": "auto" }`

## Sources
- GitHub: https://github.com/1lystore/1ly-mcp-server
- npm: https://www.npmjs.com/package/@1ly/mcp-server
- Docs: https://docs.1ly.store/

## Token tool constraints (Bags.fm)
- `name` max 32 chars, `symbol` max 10 chars, `description` max 1000 chars.
- `imageBase64` must be raw base64 and <= 15MB decoded.
- `slippageBps` range 0-10000 when `slippageMode=manual`.

## Secret storage (seller tools)
`ONELY_API_KEY` is saved locally after `1ly_create_store`:
- macOS: `~/Library/Application Support/1ly/onely_api_key.json`
- Linux: `~/.config/1ly/onely_api_key.json`
- Windows: `%APPDATA%\\1ly\\onely_api_key.json`

- If your environment cannot write these paths, store the key securely and set `ONELY_API_KEY` explicitly.
