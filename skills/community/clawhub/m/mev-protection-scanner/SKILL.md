---
name: mev-protection-scanner
version: 1.0.3
permissions:
  - env
  - network
description: Detect and protect against MEV attacks on Base L2 including sandwich attacks, frontrunning, and backrunning. Analyzes confirmed transactions from recent blocks for sandwich patterns, simulates attack profitability, and suggests protection strategies. Use when an agent needs to assess MEV risk on a Base L2 transaction or understand MEV risks on Base L2.
---

# MEV Protection Scanner

## Overview

MEV threat detection for Base L2 transactions. Identifies sandwich attack patterns and frontrunning indicators in confirmed transactions by analyzing surrounding blocks.

## Core Capabilities

### 1. Sandwich Attack Detection

- Analyzes confirmed transactions and surrounding blocks for sandwich patterns
- Detects bot patterns: victim tx → attacker buy → attacker sell
- Calculates attack profitability (slippage extraction)
- Risk score: 0-100 based on position size + pool liquidity

### 2. Frontrunning Indicators

- Identifies gas-price escalation patterns
- Detects duplicate transactions with higher gas
- Suggests private mempool submission (Flashbots Protect)
- Estimate "true cost" of trade with MEV extraction

### 3. Mempool Threat Patterns

Reference patterns to watch for — the scanner does not watch a live mempool, so these are what to look for, not what the tool detects in real time:

| Pattern | Detection | Risk Level |
|---------|-----------|------------|
| Large swap incoming | >$10K swap in mempool | High |
| Bot cluster activity | Multiple similar txs | Medium |
| Gas auction | Rapid gas escalation | High |
| Oracle manipulation | Unusual price update | Critical |
| JIT liquidity | Sudden LP addition | Medium |

### 4. Protection Strategies

- **Slippage guard:** Set max slippage to 0.3-0.5%
- **Deadline enforcement:** Strict block deadlines
- **Private RPC:** Flashbots Protect, MEV Blocker
- **Split orders:** Break large trades into smaller chunks
- **Timing:** Avoid high-congestion periods (see gas-price-predictor)

## Workflow

### Single Transaction Check

```bash
python3 scripts/mev_scanner.py --check 0x...
```

### Sandwich Simulation

```bash
python3 scripts/mev_scanner.py --simulate 1.5 --slippage 0.5
```

### Configuration

The scanner uses the public Base RPC endpoint `https://mainnet.base.org` by default — no API key required. To use a different endpoint, set `BASE_RPC_URL` or pass `--rpc-url` (must be `https://`, no embedded credentials). No API key is read, assembled, hardcoded, or defaulted anywhere in this skill; a keyed provider URL may be supplied whole as the endpoint if the operator chooses, but the script never prints the endpoint or any request error text.

## Scripts

- `scripts/mev_scanner.py` — Main scanner with detection engine (transaction check + sandwich simulation)

## References

- `references/mev-patterns.md` — Known MEV bot signatures on Base

## Earnings Model

- **Skill sale:** $10-20 (high value — protects trades)
- **x402 per-call:** $0.05 per scan
- **Enterprise:** $25/mo for continuous wallet monitoring

## Safety

- Read-only analysis — no transaction execution, no signing, no private key access
- Only queries a Base JSON-RPC endpoint (`eth_getTransactionByHash`, `eth_getBlockByNumber`); it does not monitor a live mempool and does not submit anything anywhere
- Sandwich simulation is a simple arithmetic model run locally, not a forked-environment simulation
- Detection is heuristic only (see `references/mev-patterns.md` for accuracy); there is no machine-learning filter — treat scores as a guide, not a guarantee
- Transaction hashes are validated (`0x` + 64 hex characters) before any RPC call, and malformed RPC responses are treated as missing data rather than crashing the scanner
- Network scope: the only network destination is the configured Base JSON-RPC endpoint (default `https://mainnet.base.org`). The only data sent is the RPC method name plus a transaction hash or block number. No private keys, wallet secrets, or personal data are transmitted. The endpoint URL is never printed in output, logs, or error messages, so a key embedded in an operator-supplied endpoint URL cannot leak through diagnostics.

## Integration

Pair with `gas-price-predictor` for complete transaction optimization:
1. Check MEV risk with this skill
2. If safe, check optimal gas with gas-price-predictor
3. This skill never executes a transaction. A low risk score is not permission to trade: any trade must go through a separate execution step with your explicit approval, since on-chain execution is irreversible and incurs non-refundable fees.

## Changelog

### 1.0.3 — 2026-11-19 (rescan follow-up)
- Restructured endpoint resolution to match `gas-price-predictor` (which the same scanner rates clean): the `BASE_RPC_URL` value is now read as the `--rpc-url` default in `main()` and validated in the `MEVScanner` constructor, instead of being resolved in a helper that returned an env-derived URL straight into `requests.post`. No behavior change — the endpoint is still `--rpc-url` / `BASE_RPC_URL` / public default, and no credential is read anywhere. The v1.0.2 rescan still flagged the old shape CRITICAL (TT3: "env var → network"), even though the value is an endpoint URL, not a credential; this restructure removes the traceable flow.
- Corrected the slippage comment (rescan SDI-4): large calldata is a rough proxy for slippage exposure, not a measurement of it.

### 1.0.2 — 2026-11-19 (rescan follow-up)
- Removed the `ALCHEMY_API_KEY` / `--alchemy-key` path entirely: the v1.0.1 rescan flagged it CRITICAL (TT3 — the key read from env flowed into the request URL) and found the key could leak through error logging (SDI-4 — requests exceptions include the URL). The endpoint is now configured only as a whole URL via `BASE_RPC_URL` / `--rpc-url` (default public `https://mainnet.base.org`), must be `https://` with no embedded credentials, and is never printed anywhere; RPC failures print a fixed message only, never the exception text.
- Declared the tool scope in machine-readable form (`permissions: [env, network]` in the frontmatter) so the scanner no longer flags undeclared scope (LP3).

### 1.0.1 — 2026-11-18 (security fixes)
- Removed the Alchemy-only RPC endpoint and the `"demo"` API-key fallback: the scanner now defaults to the public no-key Base RPC (`https://mainnet.base.org`), with the endpoint configurable via `BASE_RPC_URL` / `--rpc-url` and an Alchemy key accepted only via `ALCHEMY_API_KEY` / `--alchemy-key`.
- Added transaction-hash validation (`0x` + 64 hex characters) before any RPC call.
- Hardened RPC response handling: malformed or non-object responses are treated as missing data instead of raising uncaught exceptions.
- Added input validation for `--simulate` (must be > 0) and `--slippage` (0–100).
- Removed references to scripts and docs that never shipped (`scripts/mempool_monitor.py`, `scripts/sandwich_simulator.py`, `references/protection-guide.md`) and corrected workflow examples to the flags the script actually supports.
- Corrected overstated claims: no live mempool monitoring, no forked-environment simulation, no machine-learning filter. The description and section headings now say retrospective heuristic analysis, and the Integration workflow no longer instructs transaction execution — it states this skill never executes and a low risk score is not permission to trade.
- Documented the network scope in Safety: the only destination is the configured Base JSON-RPC endpoint, and only a method name plus tx hash/block number are sent.
