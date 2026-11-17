# insight-pretrade

> Pre-trade decision-input integrity for onchain AI agents, powered by Insight (oracleinsight.xyz).

## Why

Agents execute on the prices they read. A manipulated or stale price produces a confident agent executing a bad trade. This skill gives an agent one call to make before signing: a cross-provider oracle assessment of whether the price it is about to trust is currently trustworthy, returned as a signed EIP-712 verdict a third party can re-verify offline.

## What it does

- `GET https://www.oracleinsight.xyz/api/v1/safety/pre-trade` with `asset`, `chainId`, `action`, `tradeAmountUsd` — paid per call ($0.02 USDC on Base via x402, settlement only after success).
- Returns `verdict` (PASS/WARN/BLOCK), consensus price, max deviation %, manipulation-risk score, cross-provider agreement, and a recommended max position.
- Alternative: MCP at `https://www.oracleinsight.xyz/api/mcp` — discovery free, `pre_trade_safety_check` paid per call.
- Receipt verification is free (keyless HTTP endpoint, offline npm verifier, or web UI).

## Install

```bash
clawhub install insight-pretrade
```

## Requirements

- An x402-capable wallet in the agent runtime (built-in agentic wallet, `@x402/fetch`, or `mppx`).
- `curl` for the keyless endpoints.

## Safety

A PASS verdict is not a guarantee of price correctness and is not trade authorization. Signature verification establishes field integrity, not underlying truth. Snapshots are collected every 15 minutes — check freshness before acting.

## Version

- 1.0.0 — initial release.

## License

MIT-0 (per ClawHub policy). The Insight API itself remains a paid service via x402/MPP.
