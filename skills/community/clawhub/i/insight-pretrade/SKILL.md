---
name: insight-pretrade
description: Before your agent signs a trade, check whether the price it relies on is trustworthy — a signed, re-verifiable verdict in one call. $0.02 USDC via x402.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://www.oracleinsight.xyz
---

# Insight pre-trade decision-input integrity

Agents fail differently from humans: they act on the prices they read, and a manipulated or stale price produces a confident agent executing a bad trade. This skill calls Insight to answer the question a transaction simulator cannot — **whether the price the agent is about to trust is currently trustworthy** — and returns a signed EIP-712 verdict that a third party can re-verify offline.

## When to use

| Use it | Do not use it |
| --- | --- |
| Before the agent signs a swap, borrow, lend, liquidation, or repayment | As proof that a price is correct — a PASS is not a guarantee |
| When the agent reads prices from a single aggregator or unknown source | As real-time protection — snapshots are collected every 15 minutes |
| When stablecoin peg risk or oracle manipulation is plausible | As trade authorization — the verdict informs, it does not authorize |
| As a gate before committing execution | On non-EVM chains |

Requires an x402-capable wallet in the agent runtime (built-in agentic wallet, `@x402/fetch`, or `mppx`). Discovery and receipt verification are free.

## Call the paid endpoint (x402)

Endpoint: `GET https://www.oracleinsight.xyz/api/v1/safety/pre-trade`

| Parameter | Required | Example |
| --- | --- | --- |
| `asset` | yes | `ETH` |
| `chainId` | yes | `8453` (Base), `1` (Ethereum), `42161` (Arbitrum) |
| `action` | yes | `swap`, `borrow`, `lend`, `repay`, `liquidation` |
| `tradeAmountUsd` | yes | `1000` |
| `targetProviders` | no | restrict oracle providers |
| `protocolId` | no | protocol context |
| `schemaVersion` | no | `3` adds quorum/independence gates verifiable from signature bytes |

Flow: GET without payment credentials → HTTP 402 with a `PAYMENT-REQUIRED` header (USDC on Base, `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, 20000 atomic units, network `eip155:8453`) → sign an EIP-3009 `transferWithAuthorization` → retry with the `PAYMENT-SIGNATURE` header → HTTP 200 with the verdict. Settlement happens only after the check succeeds. No signup, no API key.

If the runtime has an x402 client (`@x402/fetch`, `mppx`, or an agentic wallet), let it answer the 402 automatically — do not hand-roll the signature.

## Read the verdict

| Field | Meaning |
| --- | --- |
| `verdict` | `PASS` / `WARN` / `BLOCK` |
| `consensusPrice` | cross-provider consensus price |
| `maxDeviationPct` | max deviation across providers |
| `manipulationRiskScore` | manipulation-risk score |
| `crossProviderAgreement` | cross-source agreement measure |
| `recommendedMaxPositionUsd` | suggested position cap |

Decision rule:

| Verdict | Action |
| --- | --- |
| `PASS` | proceed per the agent's own policy |
| `WARN` | reduce size or proceed with caution |
| `BLOCK` | do not execute |

## MCP alternative

`POST https://www.oracleinsight.xyz/api/mcp` (JSON-RPC, streamable HTTP). `initialize`, `tools/list`, and `ping` are free. `tools/call` of `pre_trade_safety_check` is paid per call via x402 when no API key is sent.

## Verify a receipt (free)

- Keyless HTTP: `POST https://www.oracleinsight.xyz/api/v1/safety/attestation/verify`
- Offline: the independent `verify-insight-receipt` npm package, or https://www.oracleinsight.xyz/verify

A valid signature establishes the issuer and integrity of the signed fields. It does not prove the underlying prices were correct or that the agent obeyed the verdict.

## Safety

- A `PASS` verdict does not guarantee price correctness, economic safety, or profitability.
- `BLOCK` verdicts are complete checks and are charged.
- Check each assessment's freshness and validity window before acting on it.

## Version history

- 1.0.0 — initial release: x402 REST flow, verdict decision rules, MCP alternative, free receipt verification.
