---
name: linkdrop-agent-cli
description: Create and redeem Linkdrop claim links from the command line with strict JSON output on Base, Polygon, Arbitrum, Optimism, and Avalanche.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PRIVATE_KEY
        - LINKDROP_API_KEY
        - RPC_URL
        - RPC_URL_POLYGON
        - RPC_URL_BASE
        - RPC_URL_ARBITRUM
        - RPC_URL_OPTIMISM
        - RPC_URL_AVALANCHE
        - LINKDROP_BASE_URL
        - LINKDROP_API_URL
      bins:
        - node
        - npm
    primaryEnv: PRIVATE_KEY
    homepage: https://github.com/seichris/linkdrop-sdk-cli
---

When to use
- You need to create a funded Linkdrop claim link from a local wallet.
- You need to redeem a Linkdrop claim link to a destination address.
- You need stdout to be exactly one JSON object for automation.

Files in this skill
- `linkdrop-agent.js` is the strict JSON CLI entrypoint.
- `agentdrop-core.js` contains the Linkdrop and chain logic used by the CLI.
- `.env.example` shows the supported runtime configuration.

Setup
1. Run `npm install`.
2. Set secrets in your shell or `.env`:
   - Required: `PRIVATE_KEY`, `LINKDROP_API_KEY`
   - Recommended for Base: `RPC_URL_BASE`
   - Optional fallback: `RPC_URL`
3. Keep secrets out of git history.

Supported chains
- `base` default
- `polygon`
- `arbitrum`
- `optimism`
- `avalanche`

Send a claimable transfer
1. Native token on Base:
   - `node linkdrop-agent.js send --amount 0.01 --token native --chain base`
2. ERC20 on Polygon:
   - `node linkdrop-agent.js send --amount 5 --token 0xTokenAddress --chain polygon`
3. Read these JSON fields from stdout:
   - `claimUrl`
   - `transferId`
   - `depositTx`

Claim a transfer
1. Run:
   - `node linkdrop-agent.js claim --url "https://..." --to 0xRecipient --chain base`
2. Read `redeemTx` from stdout.

JSON contract
- Success returns `{ ok: true, ... }`.
- Failure returns `{ ok: false, error: { code, name, message, details? } }`.
- The CLI writes one JSON object to stdout per invocation.

Troubleshooting
- `Missing PRIVATE_KEY`: set a 32-byte hex private key with `0x` prefix.
- `Missing LINKDROP_API_KEY`: set a valid Linkdrop API key with the `zpka_` prefix.
- `No RPC URL available`: set `RPC_URL_BASE` for Base or the matching `RPC_URL_<CHAIN>`.
- `Unsupported chain`: use one of the supported chain names above.
