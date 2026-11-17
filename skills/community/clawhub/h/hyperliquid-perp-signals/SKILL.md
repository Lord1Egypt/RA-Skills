---
name: hyperliquid-perp-signals
description: Perpetual futures signal scanner for Hyperliquid L1 DEX. Tracks funding rates, open interest shifts, large position changes, and liquidation cascades across BTC, ETH, SOL, and altcoin perps. Computes funding-rate arbitrage setups between Hyperliquid and Binance/Bybit, flags crowded trades when OI spikes on declining price, and surfaces squeeze setups when short interest is elevated. Built for crypto day traders, DeFi quants, and basis-trade funds looking for on-chain perp edge outside CEX.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash
---

# Hyperliquid Perp Signals

Signal scanner for the Hyperliquid perpetual futures DEX. Funding rates, open interest shifts, liquidation events, and cross-venue basis setups — all in a single CLI.

## When to use

- User wants perp alpha on Hyperliquid
- Hunting funding-rate arb between Hyperliquid and Binance/Bybit
- Watching for liquidation cascades on-chain
- Tracking crowded long/short positioning via OI divergence
- Surfacing squeeze setups before they happen

## Commands

```bash
python3 scripts/hl_signals.py funding           # All perps, current funding rate
python3 scripts/hl_signals.py funding SOL       # Specific coin
python3 scripts/hl_signals.py oi                # Open interest ranked by 24h change
python3 scripts/hl_signals.py liqs              # Recent liquidation events
python3 scripts/hl_signals.py basis BTC         # HL vs Binance funding basis
python3 scripts/hl_signals.py squeeze ETH       # Short squeeze risk score
```

## Output

JSON with: coin, mark_price, oracle_price, funding_rate (1h, annualized %), open_interest_usd, oi_change_24h_pct, next_funding_eta_seconds, signal (LONG_BIAS, SHORT_BIAS, NEUTRAL, SQUEEZE_SETUP, CASCADE_RISK), and a confidence score 0-100.

## Environment

- `HL_API_URL` - Hyperliquid info endpoint (default: https://api.hyperliquid.xyz/info)
- `HL_BINANCE_FUNDING_COMPARE` - whether to include Binance basis (default: true)
- Works with mock data when API is unreachable; production uses Hyperliquid's public info endpoint
