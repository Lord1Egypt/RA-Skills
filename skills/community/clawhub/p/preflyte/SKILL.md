---
name: preflyte
description: "Evidence-based market data for AI agents deploying capital in DeFi. Empirical, not advertised."
version: 1.2.2
metadata:
  openclaw:
    requires:
      env:
        - PREFLYTE_API_KEY
      bins:
        - curl
    primaryEnv: PREFLYTE_API_KEY
    emoji: "🧠"
    homepage: https://preflyte.xyz
---

# PreFlyte

**The financial intelligence layer for DeFi agents.**

PreFlyte helps AI agents make smarter financial decisions in DeFi. It sits between your agent's goal and its execution — answering the questions that prevent costly mistakes.

Existing DeFi skills help agents execute transactions. PreFlyte helps agents think before acting.

**Read-only. No wallet access. No private keys. No transaction signing.**

Works alongside any execution skill (BankrBot, Polyclaw, etc.) as a pre-trade intelligence layer.

---

## Setup

PreFlyte offers two access modes. Pick the one that suits your agent.

### Option A — Free beta (API key)

If you do not have a PREFLYTE_API_KEY set in your environment, register for one:

```bash
curl -s -X POST 'https://api.preflyte.xyz/register?source=clawhub' \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "your-agent-name"}'
```

This returns your API key instantly. Store it as PREFLYTE_API_KEY. The key cannot be retrieved again.

Every tool requires the API key as the `api_key` parameter.

- REST API: `https://api.preflyte.xyz` (auth: `X-API-Key` header)
- MCP server: `https://mcp.preflyte.xyz/mcp` (transport: streamable-http)
- Rate limit: 60 requests per minute per key

### Option B — Pay-per-request via MPP (no signup)

For agents that prefer per-request micropayments (or are already wired up to the MPP/Tempo payments ecosystem), all tools are available at `https://pay.preflyte.xyz` as paid REST endpoints. No API key or registration required — just pay per request.

- Payment protocol: MPP (HTTP 402 challenge-response)
- Network: Tempo mainnet (chain ID 4217)
- Currency: USDC (`0x20c000000000000000000000b9537d11c60e8b50`)
- Discovery document: `https://pay.preflyte.xyz/openapi.json`
- Also listed on [MPPScan](https://www.mppscan.com/)

Pricing per request:

| Tool | Price (USD) |
|------|-------------|
| assess_opportunity | $0.05 |
| estimate_net_position | $0.03 |
| market_snapshot, check_entry_viability, check_pool_viability | $0.02 |
| gas_timing, verify_claim, get_returns, get_ranking | $0.01 |

Flow for MPP-capable agents: send a GET to the paid endpoint, receive a 402 challenge, submit payment on Tempo, retry with the payment credential, receive the response plus a `Payment-Receipt` header.

---

## How PreFlyte is Structured

PreFlyte is a unified platform made up of distinct components, each answering a different financial question. Two components are live today, with more on the way.

### 🔍 RealityCheck — "Is what I believe actually true right now?"

RealityCheck is the data verification and market intelligence component. It gives agents ground truth about current market conditions so they never act on stale, hallucinated, or misleading data.

This is where the headline tool lives — **assess_opportunity** — the single call that orients an agent the moment it wakes up with capital to deploy.

**Tools in RealityCheck:**

**assess_opportunity** ⭐ Start here, every time.
Given your capital amount, your strategy, and your risk profile — where should you go? Returns ranked opportunities across all chains with net APY calculated for your specific position size, gas cost analysis, rate anomaly detection, and capacity checks. Three modes:
- `yield_farming` — best lending rates, net APY after gas, break-even days
- `active_trading` — chain viability for frequent swaps, minimum profitable trade size, capital exhaustion timeline
- `idle_capital` — where to park money between trades, minimum hold time to profit

**verify_claim** — Submit one or more beliefs about market state and get TRUE or FALSE back with the actual current value. Supports single claims or batch verification (multiple claims in one call). Claim types: supply_rate, borrow_rate, price, gas, utilization.

**get_market_snapshot** — Complete current state of a specific lending market. Rates, risk parameters, token price, gas price, plus 7-day averages and anomaly flags that tell you whether current conditions are normal or unusual.

**gas_timing** — Is now a good time to transact? Current gas compared to 24-hour and 7-day averages, the cheapest hours of the day based on historical patterns, and cost estimates for common operations like Aave deposits and Uniswap swaps.

**check_entry_viability** — Before entering a lending position, verify the market is actually open. Checks whether the market is active, frozen, or has borrowing disabled, and whether supply or borrow caps have been reached. Prevents wasting gas on transactions that will revert.

**estimate_net_position** — Detailed financial projection for a specific lending position. Shows current rate, 7-day average, entry and exit gas costs, projected net yield over your intended holding period, break-even days, and historical risk metrics (Sharpe ratio, max drawdown, volatility) when available.

**check_pool_viability** — Before swapping on Uniswap V3, check whether the pool is deep enough for your trade. Returns a TVL-based impact assessment (negligible, low, moderate, or significant slippage risk), fee tier costs in USD, and 24-hour fee volume as an indicator of pool activity.

### 📊 ProfitLens — "What has historically worked?"

ProfitLens is the empirical returns component. It computes real, measured returns from on-chain data — not theoretical APY projections. Returns are calculated from actual index ratio changes observed over time, giving agents a factual record of what each protocol and asset combination has actually delivered.

**Tools in ProfitLens:**

**get_returns** — Query historical returns by protocol, chain, asset, strategy (supply or borrow), and time window (7, 14, 30, or 90 days). Each result includes gross APY, net APY after gas, data completeness score, and risk metrics.

**get_ranking** — Ranked list of the best-performing strategies sorted by net APY. A quick way to see what's been working across the entire monitored ecosystem.

### 🚀 PreFlyte Intelligence — Coming Soon

The third component — pre-execution transaction intelligence — is in development. This will answer: "Will this specific transaction lose money through ignorance?" It will analyse a proposed transaction before execution and flag issues like unfavourable slippage, excessive gas timing, rate model discontinuities, and position sizing problems. This is the component that gives the platform its name.

---

## Coverage

**Protocols monitored:** Aave V3, Compound V3, Uniswap V3, Lido

**Chains:** Ethereum mainnet, Arbitrum

**Data sources:** On-chain data collected directly via Alchemy and Infura RPC endpoints. Prices and TVL via DeFiLlama. No third-party data resellers.

**Update frequency:**
- Lending rates and risk parameters: every 10 minutes
- Gas prices: every 60 seconds
- Token prices: every 2 minutes
- Pool TVL and fees: every 30 minutes
- Computed returns: every 30 minutes

**Coming soon:**
- Base chain support (same protocols, next major addition)
- Optimism chain support
- 90-day return windows (data accumulating, expected June 2026)
- Historical accuracy tracking for verify_claim
- PreFlyte pre-execution intelligence (Phase 3)

---

## Tool Reference

Quick reference for all tool parameters. Every tool requires `api_key` as the first parameter.

| Tool | Key Parameters | Returns |
|------|---------------|---------|
| assess_opportunity | asset, action, position_size_usd, strategy | Ranked opportunities with net APY, gas costs, anomaly flags |
| verify_claim | claim_type, value, operator, protocol, chain, asset | TRUE/FALSE with actual value and deviation |
| get_market_snapshot | protocol, chain, asset | Current rates, risk params, price, gas, 7d context |
| gas_timing | chain | Current vs historical gas, cheapest hours, tx cost estimates |
| check_entry_viability | protocol, chain, asset, action | Viable true/false with reasons and capacity remaining |
| estimate_net_position | protocol, chain, asset, action, position_size_usd | Projected yield, gas costs, break-even days, risk metrics |
| check_pool_viability | chain, token_pair, trade_size_usd | TVL-based impact, fee costs, pool activity |
| get_returns | chain, protocol, asset, strategy, window_days | Historical returns with completeness and risk scores |
| get_ranking | window_days, strategy, top_n | Ranked strategies by net APY |

---

## Constraints

- **Read-only data service** — PreFlyte does not execute transactions or access wallets
- **Lending and DEX coverage only** — does not cover derivatives, prediction markets, bridges, or token launches
- **Rates change continuously** — projections are based on current and historical conditions, not guarantees
- **Pool slippage is directional** — trade impact assessment is based on TVL ratios, not exact tick-level concentrated liquidity calculations
- **Compound V3 risk parameters are limited** — some risk fields (pause flags, caps) return null due to contract access limitations

---

## Rules

- Always pass your PREFLYTE_API_KEY as the `api_key` parameter on every tool call
- Call `assess_opportunity` FIRST when waking up with new capital or changing strategy
- Call `verify_claim` BEFORE executing any trade based on rate assumptions
- Call `gas_timing` BEFORE transacting on Ethereum mainnet — gas varies 5x within a single day
- Do NOT treat projected returns as guaranteed
- Do NOT use PreFlyte as your only data source for critical financial decisions — cross-reference with on-chain data

---

## About

PreFlyte is built and operated from Ireland by an independent developer. All data is collected directly from on-chain sources. No third-party data resellers. No ads. No tracking beyond basic API usage counts.

Currently in free beta. Feedback welcome via GitHub.
