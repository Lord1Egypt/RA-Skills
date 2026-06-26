---
name: payspawn
description: "Give any AI agent on-chain spending limits without sharing a private key. Use when: (1) agent needs to pay for x402 APIs (web scraping, search, AI services), (2) setting daily/per-tx USDC caps on an agent wallet, (3) whitelisting which contracts an agent can pay, (4) pausing a rogue agent's spending instantly, (5) provisioning credentials for agent fleets. Works on Base mainnet with USDC. NOT for: fiat payments, non-Base chains (yet), or custody of funds."
metadata:
  {
    "openclaw": {
      "emoji": "🔐",
      "color": "#F65B1A"
    }
  }
---

# PaySpawn — On-Chain Spending Limits for AI Agents

**PaySpawn** gives OpenClaw agents a credential instead of a raw private key. Spending limits, whitelists, and a kill switch — all enforced by a smart contract on Base. Math, not code.

## Quick Start

Install the SDK:

```bash
npm install @payspawn/sdk
```

Set your credential as an environment variable:

```
PAYSPAWN_CREDENTIAL=your_credential_from_dashboard
```

Get your credential at [payspawn.ai/dashboard](https://payspawn.ai/dashboard) — connect wallet, set limits, copy the credential string. No private key needed.

---

## Basic Usage

```typescript
import { PaySpawn } from "@payspawn/sdk";

const ps = new PaySpawn(process.env.PAYSPAWN_CREDENTIAL);

// Pay an x402 API automatically
const res = await ps.fetch("https://api.example.com/data");
const data = await res.json();

// Direct USDC payment
await ps.pay("recipient-wallet-address", 1.00);

// Check remaining balance
const { balance, remaining } = await ps.check();

// Kill switch — stops all spending instantly
await ps.agent.pause();
```

---

## What You Get

**Daily cap** — max USDC the agent can spend per day

**Per-tx limit** — max per single payment

**Address whitelist** — only allowed counterparties can receive payments

**Velocity limit** — max transactions per hour

**Kill switch** — pause all spending with one call

---

## x402 Auto-Pay

`ps.fetch()` handles HTTP 402 payment flows automatically. Agent calls a paid API, PaySpawn pays within the credential limits, returns the result:

```typescript
// Works with any x402-compatible API
const result = await ps.fetch("https://paid-api.example.com/endpoint", {
  method: "POST",
  body: JSON.stringify({ task: "do something" })
});
```

---

## Agent Fleets

Provision multiple agents from one shared budget pool:

```typescript
// Create a pool for multiple agents
const pool = await ps.pool.create({ totalBudget: 100, agentDailyLimit: 10 });

// Provision 10 agent credentials in one call
const fleet = await ps.fleet.provision({ poolAddress: pool.address, count: 10 });
```

One pool. One API call. Each agent gets its own credential with its own daily limit. All draw from the shared pool budget.

---

## Why Use This

Agents with raw wallet keys have unlimited access. One bad prompt or leaked env file and the wallet is drained. PaySpawn credentials are scoped and revocable:

- Credential limits are enforced by the smart contract, not software
- Leaked credential still cannot exceed the daily cap
- Prompt injection tries to pay an unknown address — whitelist blocks it
- One call stops spending instantly

---

## Links

- Dashboard: [payspawn.ai/dashboard](https://payspawn.ai/dashboard)
- Docs: [payspawn.ai](https://payspawn.ai)
- X: [@payspawn](https://x.com/payspawn)
