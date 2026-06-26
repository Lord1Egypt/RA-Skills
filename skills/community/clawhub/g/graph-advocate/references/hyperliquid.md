# Hyperliquid Reference

Hyperliquid perps data comes in two layers: **raw** market/user/vault data
via the Token API, and **derived trader intelligence** via Graph Advocate's
own paid `/hyperliquid/*` endpoints.

## When to Use Which

**Raw data → Token API** (`/v1/hyperliquid/*`): markets, OHLCV, open
interest, funding, liquidations, per-user fills, vault flows. Plain REST,
no scoring. Use when you want the numbers and will analyze them yourself.

**Derived scores → GA's `/hyperliquid/*` endpoints**: skill scores,
classifications, vault evaluation, counterparty risk. Use when you want a
decision-ready answer instead of raw fills. Paid via x402 from call 1.

## GA's paid `/hyperliquid/*` endpoints

| Endpoint | Price | Returns |
|----------|-------|---------|
| `POST /hyperliquid/score` | $0.02 | Composite skill_score 0-100, classification (sharp/neutral/retail), liquidation rate, funding burn, profit factor |
| `POST /hyperliquid/pnl` | $0.05 | Full dossier — scores + open positions + recent fills |
| `POST /hyperliquid/screen` | $0.05 | Top N traders of a coin, each scored; sharp/retail headline counts |
| `POST /hyperliquid/vault` | $0.10 | Vault evaluator — leader skill, depositor concentration, redemption pressure |
| `POST /hyperliquid/risk` | $0.02 | Counterparty risk — liquidation rate, funding burn, recent-outflow flag |

Request body: `{"user": "0x..."}` for score/pnl/risk, `{"coin": "HYPE", "n": 10}`
for screen, `{"vault": "0x..."}` for vault. Catalog (free, JSON):
`GET https://graphadvocate.com/hyperliquid`.

## Coin identifiers

- Core perps: bare symbol — `BTC`, `ETH`, `HYPE`, `SOL`
- Spot pairs: `@N` form — `@107`
- Builder DEX markets: `dex:symbol` — `xyz:SP500`, `cash:TSLA`

## Raw Token API endpoints (`/v1/hyperliquid/*`)

`markets`, `markets/ohlc`, `markets/oi`, `markets/liquidations`,
`markets/activity`, `users`, `users/activity`, `users/positions`,
`vaults`, `vaults/depositors`, `platform`. Standard REST under the
Token API base — no npm install.

## Scoring formula

`skill_score` weights profitability 40% (PnL as bps of volume), risk
control 40% (liquidation rate), efficiency 20% (profit factor), then
shrinks toward neutral by sample-size confidence (`log10(trades)/6`).
`sharp` ≥ 70, `retail` ≤ 35; under 100 trades returns `insufficient_data`.

Full docs: https://docs.graphadvocate.com/hyperliquid
