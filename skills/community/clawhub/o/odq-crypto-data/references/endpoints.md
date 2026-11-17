# Endpoint Reference — ODQ Crypto Data

BASE = `https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010`

All services: network `base`, currency `USDC`, paywall per x402 v2.
Unpaid request → HTTP 402 with payment requirements JSON (free to receive).

---

## 1. market-signal — $0.001 USDC

`GET {BASE}/market-signal?coin=bitcoin&vs=usd`

- `coin`: CoinGecko id (required). Examples: `bitcoin`, `ethereum`, `aerodrome-protocol`.
- `vs`: quote currency, default `usd`.

Returns: price, market cap, 24h/7d/30d change, SMA7 & SMA25 with trend
(UP/DOWN), RSI-14 (Wilder), annualized volatility (from 60d daily data),
plus raw inputs and disclaimer.

Example decision mapping:
- RSI > 70 → overbought territory (data point, not advice).
- SMA7 > SMA25 → short-term momentum above medium trend.

## 2. crypto-sentinel — $0.003 USDC

`GET {BASE}/crypto-sentinel` (no params)

One call returns for BTC/ETH/SOL: spot price, 24h change, current funding
APR (Binance USD-M), volatility regime (calm/normal/wild), and long/short
crowding regime based on funding sign and magnitude. Sources: Binance fapi,
fallback CoinGecko. ~100ms, deterministic.

## 3. funding-heatmap — $0.004 USDC

`GET {BASE}/funding-heatmap` (no params)

Annualized funding APR for 15 Binance USD-M perps (BTC, ETH, SOL, XRP, DOGE,
ADA, AVAX, LINK, SUI, TON, BNB, LTC, PEPE, WIF, ARB), ranked by |APR|, with
`crowded_long` / `crowded_short` flags on extremes. Use to see which side of
which market is paying to stay in.

## 4. pair-scan — $0.005 USDC

`GET {BASE}/pair-scan?token=0xCONTRACT&chain=base`

- `token`: EVM contract address (required).
- `chain`: one of `base|arbitrum|ethereum|bsc|solana` (default `base`).

Returns: aggregated liquidity across all DEX pairs, 24h volume, volume/liquidity
churn, best pair (DEX, price, FDV, 24h vol, txns buy/sell), up to 6 secondary
pairs. Data: DexScreener.

## 5. token-safety — $0.01 USDC

`GET {BASE}/token-safety?token=0xCONTRACT&chain=base`

Transparent rule-based rug screen. Score 0-100 (higher = safer), level
`normal_range|elevated_risk|high_risk`, with auditable flags such as:

- PAIR_YOUNGER_THAN_24H (+25)
- LIQUIDITY_BELOW_10K (+25)
- EXTREME_VOLUME_CHURN_GT_5X (+15)
- SELL_PRESSURE_GT_80PCT (+10)
- VOLATILITY_EXTREME_24H (+10)

Every response echoes `inputs_used`, `methodology` and a disclaimer that this
is NOT a security audit. Interpretation guide:

- 80-100: no red flags in the heuristics used.
- 40-79: elevated risk — read the flags before acting.
- 0-39: high risk — multiple red flags; treat as hazardous.

## Cost discipline

| Task | Calls | Cost |
|------|-------|------|
| One coin signal | 1 | $0.001 |
| Full perp snapshot | 1 | $0.003 |
| Screen one token | 2 | $0.015 (pair-scan + token-safety) |
| Screen a 50-token watchlist | 100 | $1.50 |

Always confirm batch costs with the user before running multi-token scans.

## wallet-watch ($0.0002/req)

```
GET {BASE}/wallet-watch?address=0x{40hex}&chain=eth|base|bsc&txs=false (optional)
```

Returns: live native balance (wei + whole units) from a public RPC node, Blockscout wallet flags (ENS domain, has_tokens, has_token_transfers, native exchange rate), and the 5 most recent transactions touching the address (hash, from, to, value, status, timestamp, method). `txs=false` skips the transactions fetch.

Example:
```bash
curl -s "$BASE/wallet-watch?address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&chain=eth"
```
