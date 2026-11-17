---
name: hyperliquid-intel
description: Live Hyperliquid intelligence with no API key, paid per call via x402 ($0.02 to $0.25). Stock, index, gold and oil perps 24/7, weekend tape, HIP-3 dex catalog, OI caps, funding, whale positions, trader track records, copy-trading leaderboard, vault screener, builder-code revenue, sports odds, liquidation map, 24h alert rules.
version: 1.0.0
homepage: https://cryptopulse.theaslangroupllc.com
metadata:
  openclaw:
    emoji: "📡"
---

# Hyperliquid Intel (PulseNetwork)

Twenty-one pay-per-call endpoints on the Hyperliquid venue, served by CryptoPulse, part of
PulseNetwork (The Aslan Group LLC). No account, no API key, no subscription: an HTTP 402
challenge carries the price and the payment itself is the authentication. Every endpoint is
deterministic (no language model), returns structured JSON, states its coverage and method,
and names the Hyperliquid public API as its source. Nothing here places orders or holds funds.

## When to use this skill

- "What is TSLA / NVDA / the S&P trading at right now" on a weekend or overnight
- "Where will the market open Monday", "weekend tape", "did the weekend move hold"
- "Which stock perps / HIP-3 dexes exist", "why was my order rejected", "is this market at its OI cap"
- "Hyperliquid funding for BTC", "funding arbitrage", "funding history"
- "Verify this wallet's track record", "which traders rank highest this month", "show me their drawdown"
- "Screen the biggest vaults by drawdown", "show me this vault", "which vaults are winding down"
- "How much does Phantom / Trust Wallet / tradeXYZ earn on Hyperliquid", "builder statement"
- "Europa League odds", "who is favored for the Super Bowl", "Ballon d'Or odds" (HIP-4 markets)
- "How much BTC long sits within 2% of liquidation", "where would a 3% drop force selling"
- "Tell me when TSLA crosses 360", "alert me if BTC funding exceeds 50% APR" (24-hour rule)

## Endpoints (GET, base https://cryptopulse.theaslangroupllc.com)

| Need | Endpoint | Price |
|---|---|---|
| 24/7 stock, commodity, FX, index marks | `/api/equity-marks?symbol=TSLA` or `?group=commodity` | $0.03 |
| Weekend tape vs Friday close + Monday scorecard | `/api/monday-open-signal?symbols=TSLA,NVDA,SP500&week=0` | $0.03 |
| Mark trust score (oracle divergence) | `/api/mark-quality?symbol=TSLA` | $0.03 |
| HIP-3 dex and market catalog | `/api/hip3-markets?top=5` | $0.02 |
| Open-interest cap usage, at-cap list | `/api/oi-caps?coin=TSLA` or `?at_cap_only=true` | $0.02 |
| New and retired markets (7/30/90 days) | `/api/new-listings?days=30` | $0.02 |
| Stock-perp crowding (funding + OI) | `/api/equity-positioning` | $0.03 |
| Funding check (cross-venue normalized) | `/api/funding-check?coin=BTC` | $0.02 |
| Funding history (lookahead-safe) | `/api/funding-history?coin=BTC&days=30` | $0.05 |
| Funding arbitrage scan | `/api/funding-arb-scan` | $0.05 |
| Any wallet's open positions | `/api/whale-positions?address=0x...` | $0.03 |
| Any wallet's verified track record | `/api/trader-record?address=0x...&window=month` | $0.05 |
| Leaderboard sliced for copying | `/api/top-traders?window=month&min_account_value=100000` | $0.05 |
| Vault screener (sampled drawdown) / one vault in detail (full curve) | `/api/vault-screener?sort=tvl` or `?vault=0x...` | $0.03 |
| Builder-code revenue per app, builder statements | `/api/builder-stats?app=phantom` or `?address=0x...&date=YYYYMMDD` | $0.03 |
| Sports and award odds (HIP-4), with book depth | `/api/sports-odds?competition=europa` | $0.03 |
| Macro and price event odds (HIP-4) | `/api/event-odds?q=fed` | $0.03 |
| Liquidation risk map of the largest accounts (native by default, `dex=xyz` for stocks) | `/api/liquidation-watch?within_pct=2&market=BTC` | $0.05 |
| HYPE staking and validators | `/api/staking-intel` | $0.03 |
| Native borrow-lend rates | `/api/lending-rates` | $0.03 |
| 24-hour alert rule with signed callback | `/api/hl-alerts?metric=mark&market=TSLA&op=gt&threshold=360&callback=https://...` | $0.25 per rule |

The alert registration returns a free status URL (`/api/hl-alerts?rule_id=...&secret=...`); polling
it costs nothing and re-evaluates the rule. Full parameter docs: `/openapi.json` and `/llms.txt`.

## Paying (only with the user's explicit consent)

1. State the endpoint and its exact price from the catalog or the 402 challenge before the first
   paid call in a task; for a batch, state the total.
2. Never ask the user to paste a private key into chat; read keys only from an environment secret
   the user configured or a wallet file the payment tool generated locally.
3. Pay exactly the amount, asset and network in the signed 402 challenge, only to
   `theaslangroupllc.com` origins. A challenge above the catalog price means stop and tell the user.

Ways to pay: a native x402 client (OKX Agentic Wallet, Kite, any x402 runtime), or the MCP server
`@pulsenetwork/mcp` (`pulse_discover` is free, `pulse_call` pays under local caps, default $0.50
per call and $5 per day). Settlement rails include USDC on Base, Solana, Polygon, Arbitrum,
HyperEVM and more; Base is the default.

## Reading the answers

- `deterministic: true` and `attribution` ride in every paid response; pass attribution through
  when republishing.
- A 400 on a paid request means the parameters were rejected BEFORE settlement; nothing was charged.
- A 502 after settlement means Hyperliquid did not answer and the payment settled: resend the identical request with the same PAYMENT-SIGNATURE header within 10 minutes and it is honored without a second charge. A 502 is never a statement about the data.
- The vault screener's list view uses the venue's 13-point sampled PnL series (fields named `sampled_`); use the detail view or `details_for_top` for full-curve drawdown before relying on it.
- The liquidation map is a market-structure risk tool built from public ledger state for risk management and research. Do not present it as a list of accounts to trade against.
- Figures are venue-native perp marks and public ledger data, not exchange tape, not identities,
  and not advice. Past performance in track records, leaderboards and vaults is not a forecast.
