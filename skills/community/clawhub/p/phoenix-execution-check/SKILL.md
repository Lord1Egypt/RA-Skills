---
name: phoenix-execution-check
description: Before sending an on-chain transaction, swap, bridge or x402 payment on an L2 (Base, Arbitrum, Optimism, zkSync, Scroll, Linea, Blast, Mantle, Mode, Taiko, Polygon zkEVM), check whether the network is healthy enough to execute right now or whether to wait. Also get this agent's own behavioural identity passport (agent / human / bot) from Silicon DNA.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"] }
      }
  }
---

# Phoenix Execution Check

Phoenix Zero measures 12 chains every ~2 seconds against 2-3 independent RPC nodes (only real
JSON-RPC answers count) and answers one question: **send now, or wait?**
Base URL: `https://rtt.phoenix-ai.work`

## 1. Before you send a transaction or payment

Free check (the verdict is delayed ~60 s; limit 100 calls/day per IP):

```bash
curl -s "https://rtt.phoenix-ai.work/api/v1/demo/safe?chain=base"
```

Response: `{"safe": true, "reason": "ok", "chain": "base", "delayed_s": 63.6, "as_of": "...", ...}`

- `safe: true`  → the network was healthy a minute ago; proceed.
- `safe: false` → wait 10-30 s and check again, or execute on another chain.
- `reason` is one of: `ok`, `elevated_latency`, `high_latency`, `sequencer_stall`, `elevated_revert`, `high_revert`, `data_stale`.

Chains: `base`, `arbitrum`, `optimism`, `zksync`, `scroll`, `linea`, `blast`, `mantle`, `mode`, `taiko`, `polygon_zkevm`, `casper`.

**Live verdict (no delay)** — paid, $0.01 USDC per call via the x402 protocol (Base, Polygon or Arbitrum):

```bash
curl -s -i "https://rtt.phoenix-ai.work/api/v1/safe?chain=base"
```

Without payment it returns HTTP 402 with the payment terms (x402 v2 `PAYMENT-REQUIRED` header and the
same `accepts` list in the body). Only use it if you have an x402-capable wallet/tool; otherwise use the
free delayed check above. The paid answer adds p99 latency and revert ratio and is signed (EIP-191,
signer `0xdac8adC44f621bC3A56E9DC108d2F76Be3142294`).

Current price (free, no verdict inside): `curl -s https://rtt.phoenix-ai.work/api/v1/price`

## 2. Get your own agent passport

Silicon DNA classifies **the caller** (you) from your request timing and headers:

```bash
curl -s https://rtt.phoenix-ai.work/api/agent/passport
```

The `timing_dna` block is computed from your own request intervals (Shannon entropy, Spearman ρ,
coefficient of variation). Until you have made ~20 requests it honestly says `"verdict": "insufficient"`.
It cannot classify a third party — it always describes whoever calls it.

## Rules
- Never treat a delayed `safe: true` as a guarantee; it describes the network ~60 s ago.
- Do not call more than needed: one check right before sending is enough.
- Full endpoint list: `https://rtt.phoenix-ai.work/llms.txt`
