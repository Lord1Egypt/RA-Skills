> Follow the FORMAT ENFORCEMENT rules from SKILL.md. Output must match templates character-for-character.

# Report F — Loop Strategy

Simulate a leverage loop strategy: deposit collateral → borrow → re-deposit → repeat.

**Input:** The user must provide `<collateral_asset> <borrow_asset> <initial_amount> [target_loops]`.

If not already provided, ask:

> **EN:** What collateral asset, borrow asset, and initial amount? (e.g. slisBNB WBNB 10)
> **中文：** 請提供抵押品、借款資產和初始數量（例如 slisBNB WBNB 10）

## F.1 — Find the relevant market

The `keyword` parameter of `lista_get_borrow_markets` filters by **loan token name**,
not collateral name. Search by the borrow asset, then filter by collateral:

```
lista_get_borrow_markets({ keyword: "<borrow_asset>", pageSize: 50 })
```

From the returned list, find the entry where `collateral == <collateral_asset>`. Collect:
- `rate` — borrow APY (decimal)
- `lltv` — liquidation LTV (decimal, e.g. "0.860000000000000000") — already in the response, no separate RPC call needed
- `id` — market identifier
- `collateralToken` — collateral token contract address
- `loanToken` — loan token contract address

If no matching market is found, paginate (`page: 2`, `page: 3`) or drop the keyword
filter and scan all markets. Inform the user if the market still cannot be found.

**Fallback — moolah.js** (if MCP unavailable):
```bash
node skills/lista/scripts/moolah.js --chain <bsc|eth> markets <borrow_asset>
```
Returns JSON with `markets[]` containing `borrowApy`, `lltv`, `id`, `collateral`, `loan`, `zone` per market. Filter by `collateral` field to find the matching market.

## F.2 — Fetch token prices

Use the **Token price resolution** section in `domain.md` to get collateral and loan prices.

## F.3 — Get collateral native yield

For slisBNB, ankrBNB, wstBNB, BNBx:

```
lista_get_staking_info()
```

Use the returned staking APR/APY as native yield.

**Fallback — moolah.js** (if MCP unavailable):
```bash
node skills/lista/scripts/moolah.js staking
```
Returns JSON with `apr`, `comprehensiveApy`, and `locked` (3m/6m/12m).

If moolah.js is also unavailable: slisBNB → use 2.8% default. Other LSTs → use 0%.

For other assets:
- PT tokens: use fixed rate from `terms.apy` in market response
- BTCB, stablecoins: 0% native yield

## F.4 — Simulate loops

Variables:
- `P_c` = collateral price (USD), `P_b` = borrow price (USD)
- `r` = `rate` (annual), `y` = native yield (annual)
- `L` = LLTV, `targetLTV` = 0.70 (conservative default)

```
coll[0] = initial_amount
debt[0] = 0

for i in 1..N:
  borrowed_value = coll[i-1] × targetLTV × P_c / P_b   # in borrow token units
  coll[i] = coll[i-1] + borrowed_value × P_b / P_c       # convert back to collateral
  debt[i] = debt[i-1] + borrowed_value

  currentLTV = debt[i] × P_b / (coll[i] × P_c)
  stop recommending when currentLTV > 0.75 × L
```

Net APY at N loops:
```
grossYield  = coll[N] × y × P_c
borrowCost  = debt[N] × r × P_b
netAPY      = (grossYield − borrowCost) / (initial_amount × P_c)

liqPrice    = debt[N] × P_b / (coll[N] × L)   # in collateral asset USD
buffer      = (P_c − liqPrice) / P_c × 100%
```

Recommend the loop count that maximises net APY while keeping buffer ≥ 20%.

## F.5 — Output template

⛔ STOP BEFORE OUTPUTTING. You MUST copy the template below character-for-character. Substitute `<placeholder>` values with real data. Change NOTHING else — no bullet points, no overview section, no preamble, no trailing remarks. Your response must start with the exact first line shown in the template.

### English

```
Lista Lending — Loop Strategy: slisBNB/WBNB
━━━━━━━━━━━━━━━━━━━━━━━━━
LLTV: 86%  |  Borrow Rate: 2.6% APY  |  slisBNB Native Yield: 4.2%

- - - - -

Loop 0
Collateral: 10.0 slisBNB
Debt: 0
Leverage: 1.00x
Net APY: 4.20%
Liq. price: —
Buffer: —


Loop 1
Collateral: 17.0 slisBNB
Debt: 7.0 WBNB
Leverage: 1.70x
Net APY: 5.80%
Liq. price: ＄195
Buffer: 28%


Loop 2
Collateral: 21.9 slisBNB
Debt: 11.9 WBNB
Leverage: 2.19x
Net APY: 6.40%
Liq. price: ＄210
Buffer: 23%


Loop 3  <- Optimal
Collateral: 25.3 slisBNB
Debt: 15.3 WBNB
Leverage: 2.53x
Net APY: 6.70%
Liq. price: ＄221
Buffer: 19%


Loop 4  ⚠️
Collateral: 27.7 slisBNB
Debt: 17.7 WBNB
Leverage: 2.77x
Net APY: 6.60%
Liq. price: ＄230
Buffer: 15%

- - - - -

✅ Recommended: 3 loops
   Net position: 25.3 slisBNB / 15.3 WBNB debt  |  Leverage: 2.53×
   Net APY: ~6.70% (vs 4.20% unlooped)
   Liquidation price: ＄221  (current ~＄272, 19% buffer)

⚠️  Risk: Borrow rate is variable. If it rises above ~5.8%, strategy turns net negative.

━━━━━━━━━━━━━━━━━━━━━━━━━
Data: <DATA_SOURCE>  |  <NETWORK>
```

### 繁體中文

```
Lista Lending — 槓桿策略：slisBNB/WBNB
━━━━━━━━━━━━━━━━━━━━━━━━━
LLTV：86%  |  借款利率：2.6% APY  |  slisBNB 原生收益：4.2%

- - - - -

循環 0
抵押品：10.0 slisBNB
負債：0
槓桿：1.00x
淨年化：4.20%
清算價格：—
緩衝：—


循環 1
抵押品：17.0 slisBNB
負債：7.0 WBNB
槓桿：1.70x
淨年化：5.80%
清算價格：＄195
緩衝：28%


循環 2
抵押品：21.9 slisBNB
負債：11.9 WBNB
槓桿：2.19x
淨年化：6.40%
清算價格：＄210
緩衝：23%


循環 3  <- 最佳
抵押品：25.3 slisBNB
負債：15.3 WBNB
槓桿：2.53x
淨年化：6.70%
清算價格：＄221
緩衝：19%


循環 4  ⚠️
抵押品：27.7 slisBNB
負債：17.7 WBNB
槓桿：2.77x
淨年化：6.60%
清算價格：＄230
緩衝：15%

- - - - -

✅ 建議：3 次循環
   淨部位：25.3 slisBNB / 負債 15.3 WBNB  |  槓桿：2.53×
   淨年化：約 6.70%（未槓桿 4.20%）
   清算價格：＄221（當前約 ＄272，緩衝 19%）

⚠️  風險：借款利率為浮動利率。若利率上升至約 5.8% 以上，策略將轉為淨虧損。

━━━━━━━━━━━━━━━━━━━━━━━━━
資料來源：<DATA_SOURCE>  |  <NETWORK>
```
