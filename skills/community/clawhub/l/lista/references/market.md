> Follow the FORMAT ENFORCEMENT rules from SKILL.md. Output must match templates character-for-character.

# Report B — Market Lending Rates

Query real-time Supply APY and Borrow APY for each lending market.

## B.1 — Fetch data

```
lista_get_borrow_markets({ pageSize: 50, chain: "<chain>" })
```

Default returns Classic (zone=0) + Smart Lending (zone=3) markets. To include Alpha and Aster, pass `zone: "0,1,3,4"`.

Returns per market:
- `id` — market identifier
- `collateral` / `loan` — asset symbols
- `supplyApy` — supply-side APY (decimal, 0.087 = 8.7%)
- `rate` — borrow-side APY (decimal)
- `liquidity` — available liquidity (token amount)
- `liquidityUsd` — available liquidity in USD
- `zone` — 0=Classic, 1=Alpha, 3=Smart Lending, 4=Aster
- `smartCollateralConfig` — non-empty for Smart Lending markets (zone=3)
- `termType` — 0 = variable, non-zero = fixed rate
- `lltv` — liquidation LTV

If user asks about a specific asset (e.g. "USDT rate", "BNB 利率"), pass `keyword` parameter to filter.

**Fallback — moolah.js** (if MCP unavailable):
```bash
node skills/lista/scripts/moolah.js --chain <bsc|eth> markets [keyword]
```
Returns JSON with `markets[]` containing `supplyApy`, `borrowApy`, `liquidityUsd`, `lltv`, `zone`, `isSmartLending`, `utilization`, `termType` per market, plus `overall` protocol stats.

Note: moolah.js uses `borrowApy` (not `rate`). Also adds `utilization` and `termType` fields directly.

**Fallback — curl only** (no Node.js): Use vault/list and vault/allocation for market metadata. No rates or utilization. Show available fields only.

## B.1.5 — Conditional query detection

Detect whether the user's message implies a subset query. If yes, set `filter_mode = true` and determine the filter/sort to apply **after** fetching all markets (B.1):

| User intent | Action |
|---|---|
| "最低借款" / "lowest borrow rate" | sort borrowApy asc, take 1 |
| "最高供款" / "highest supply APY" | sort supplyApy desc, take 1 |
| "前 N 個" / "top N" | sort by relevant field, take N |
| "利率低於 X%" / "rate below X%" | filter borrowApy < X/100 |
| "<asset> 市場" / "<asset> markets" | filter collateral or loan contains asset |
| "<zone> 市場" / "<zone> markets" | filter by zone |

Exclude markets with `liquidityUsd < $1,000` before any sort/filter.

In B.3 output when `filter_mode = true`:
- Render only the matching entries using the standard per-market group format.
- Replace report title with a context-specific title:
  - `📋 Lista Lending — <asset> 市場借貸利率` / `📋 Lista Lending — <asset> Market Rates` (asset filter)
  - `📋 Lista Lending — 最低借款利率市場` / `📋 Lista Lending — Lowest Borrow Rate Market` (superlative borrow)
  - `📋 Lista Lending — 借款利率 < X% 市場` / `📋 Lista Lending — Borrow Rate < X% Markets` (threshold)
- If no markets match: output `（無符合條件的市場）` / `(No matching markets)` between the `- - - - -` separators.
- All separators, legend line, data source line remain unchanged.

Note: the existing `keyword` parameter in B.1 handles asset filter at fetch time; conditional query detection refines further at render time.

## B.2 — Compute

Build a deduplicated market list. Each market appears once with:
- `collateral / loan` — market name
- `supplyApy` — supply-side APY (decimal → %)
- `rate` (MCP) / `borrowApy` (moolah.js) — borrow-side APY (decimal → %)
- `liquidityUsd` — available liquidity in USD
- `utilization` — compute as: `borrow / (liquidity + borrow)` where `liquidity` = available to borrow, `borrow` = already borrowed

Sort by liquidityUsd descending (largest markets first).

Flag special market types:
- Smart Lending: `smartCollateralConfig` is non-empty → append `⚡`
- Fixed Rate: `termType != 0` → append `🔒`
- High utilization: `utilization > 0.85` → append `🔥`

## B.3 — Output template

⛔ STOP BEFORE OUTPUTTING. You MUST copy the template below character-for-character. Substitute `<placeholder>` values with real data. Change NOTHING else — no bullet points, no overview section, no preamble, no trailing remarks. Your response must start with the exact first line shown in the template.

### English

```
📋 Lista Lending — Market Rates
<YYYY-MM-DD HH:MM> UTC  |  <NETWORK>
━━━━━━━━━━━━━━━━━━━━━━━━━

- - - - -

slisBNB / WBNB ⚡
Supply APY: 3.2%
Borrow APY: 5.8%
Liquidity: ＄4.1M
Utilization: 72%


BTCB / U
Supply APY: 2.8%
Borrow APY: 4.6%
Liquidity: ＄12.3M
Utilization: 41%


WBNB / USD1
Supply APY: 4.1%
Borrow APY: 7.2%
Liquidity: ＄2.8M
Utilization: 68%


PT-slisBNBx / WBNB 🔒
Supply APY: 5.8%
Borrow APY: —
Liquidity: ＄1.2M
Utilization: 89% 🔥


slisBNB & BNB / USD1 ⚡
Supply APY: 1.4%
Borrow APY: 3.9%
Liquidity: ＄3.5M
Utilization: 55%


ETH / USD1
Supply APY: 1.9%
Borrow APY: 4.2%
Liquidity: ＄800K
Utilization: 38%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Smart Lending  |  🔒 Fixed Rate  |  🔥 High Utilization (>85%)

Data: <DATA_SOURCE>  |  <NETWORK>
```

Notes:
- One group per market.
- Fixed Rate markets show `—` for Borrow APY (no borrowing).
- If user filtered by asset, show only matching markets and replace title with: `📋 Lista Lending — <ASSET> Market Rates`.

### 繁體中文

```
📋 Lista Lending — 市場借貸利率
<YYYY-MM-DD HH:MM> UTC  |  <NETWORK>
━━━━━━━━━━━━━━━━━━━━━━━━━

- - - - -

slisBNB / WBNB ⚡
供款年化：3.2%
借款年化：5.8%
流動性：＄4.1M
利用率：72%


BTCB / U
供款年化：2.8%
借款年化：4.6%
流動性：＄12.3M
利用率：41%


WBNB / USD1
供款年化：4.1%
借款年化：7.2%
流動性：＄2.8M
利用率：68%


PT-slisBNBx / WBNB 🔒
供款年化：5.8%
借款年化：—
流動性：＄1.2M
利用率：89% 🔥


slisBNB & BNB / USD1 ⚡
供款年化：1.4%
借款年化：3.9%
流動性：＄3.5M
利用率：55%


ETH / USD1
供款年化：1.9%
借款年化：4.2%
流動性：＄800K
利用率：38%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Smart Lending  |  🔒 固定利率  |  🔥 高利用率（>85%）

資料來源：<DATA_SOURCE>  |  <NETWORK>
```
