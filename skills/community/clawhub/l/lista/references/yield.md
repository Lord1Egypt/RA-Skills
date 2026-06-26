> Follow the FORMAT ENFORCEMENT rules from SKILL.md. Output must match templates character-for-character.

# Report C — Vault Yield

Query each Vault's current APY, TVL, and underlying market allocations.

## C.1 — Fetch data

```
lista_get_lending_vaults({ pageSize: 50, chain: "<chain>" })
```

Returns per vault: `address`, `name`, `apy`, `emissionApy`, `emissionEnabled`, `depositsUsd`, `assetSymbol`, `zone`, `utilization`, and `collaterals[]`.

Each `collaterals[]` entry has: `id` (marketId), `name` (collateral symbol), `loanSymbol`, `allocation` (decimal weight, e.g. 0.44 = 44%).

If user asks about a specific asset (e.g. "BNB yield", "USDT 收益"), pass `keyword` parameter to filter.

**Fallback — moolah.js** (if MCP unavailable):
```bash
node skills/lista/scripts/moolah.js --chain <bsc|eth> vaults [keyword]
```
Returns JSON with `vaults[]` containing `apy`, `emissionApy`, `totalApy`, `depositsUsd`, `zone`, `utilization`, `collaterals[]` per vault.

**Fallback — curl** (if Node.js unavailable):
```bash
curl -s "https://api.lista.org/api/moolah/vault/list?pageSize=100&chain=bsc"
```
Note: curl may not include emissionApy. If missing, show LISTA bonus as "—" and use only base apy.

## C.1.5 — Conditional query detection

Detect whether the user's message implies a subset query. If yes, set `filter_mode = true` and determine the filter/sort to apply **after** fetching all vaults (C.1):

| User intent | Action |
|---|---|
| "最高年化" / "highest APY" | sort totalApy desc, take 1 |
| "最低年化" / "lowest APY" | sort totalApy asc, take 1 |
| "前 N 個" / "top N" | sort totalApy desc, take N |
| "年化高於 X%" / "APY above X%" | filter totalApy > X/100 |
| "<asset> vault" / "<asset> 金庫" | filter assetSymbol contains asset |
| "<zone> vault" / "<zone> 金庫" | filter by zone |
| "TVL 最大" / "largest TVL" | sort depositsUsd desc, take 1 |

Exclude vaults with `depositsUsd < $100` before any sort/filter.

In C.3 output when `filter_mode = true`:
- Render only the matching vaults, each inside its correct zone section. If all results share the same zone, only that zone header appears. If results span multiple zones, render one zone section per represented zone.
- Replace report title with a context-specific title:
  - `💰 Lista Lending — 最高年化金庫` / `💰 Lista Lending — Highest APY Vault` (superlative APY)
  - `💰 Lista Lending — <asset> Vault 收益` / `💰 Lista Lending — <asset> Vault Yield` (asset filter)
  - `💰 Lista Lending — 年化 > X% 金庫` / `💰 Lista Lending — APY > X% Vaults` (threshold)
- If no vaults match: output `（無符合條件的金庫）` / `(No matching vaults)` between the `- - - - -` separators.
- All separators, zone headers, legend line, data source line remain unchanged.

Note: the existing `keyword` parameter in C.1 handles asset filter at fetch time; conditional query detection refines further at render time.

## C.2 — Compute

- `totalApy = apy + (emissionApy if emissionEnabled else 0)`
- Sort by `totalApy` descending within each zone.
- Group by zone: 0=Classic, 3=Smart Lending, 1=Alpha, 4=Aster (see `domain.md` for zone definitions).
- For each vault, list top 3 underlying markets by `allocation` weight from `collaterals[]`.

## C.3 — Output template

⛔ STOP BEFORE OUTPUTTING. You MUST copy the template below character-for-character. Substitute `<placeholder>` values with real data. Change NOTHING else — no bullet points, no overview section, no preamble, no trailing remarks. Your response must start with the exact first line shown in the template.

### English

```
💰 Lista Lending — Vault Yield
<YYYY-MM-DD HH:MM> UTC  |  <NETWORK>
━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 Classic (Audited)

- - - - -

#1  WBNB Vault (WBNB)
Base APY: 4.2%
LISTA bonus: 2.1%
Total APY: 6.3%
TVL: ＄18.2M
Utilization: 52%
Top markets: slisBNB/WBNB 39% ⚡, PT-slisBNBx/WBNB 21% 🔒


#2  USD1 Vault (USD1)
Base APY: 3.1%
LISTA bonus: 1.8%
Total APY: 4.9%
TVL: ＄8.3M
Utilization: 61%
Top markets: BTCB/USD1 44%, WBNB/USD1 32%


#3  U Vault (U)
Base APY: 2.5%
LISTA bonus: 0%
Total APY: 2.5%
TVL: ＄5.1M
Utilization: 48%
Top markets: slisBNB/U 52%, BTCB/U 30%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Alpha (Higher Risk)

- - - - -

#1  WBTC Vault (WBTC)
Base APY: 14.2%
LISTA bonus: 0%
Total APY: 14.2%
TVL: ＄420K
Utilization: 78%
Top markets: WBTC/USD1 100%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Aster (Partner Assets)

- - - - -

#1  ASTER Vault (ASTER)
Base APY: 8.5%
LISTA bonus: 0%
Total APY: 8.5%
TVL: ＄120K
Utilization: 45%
Top markets: ASTER/USDT 100%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Smart Lending  |  🔒 Fixed Rate

Data: <DATA_SOURCE>  |  <NETWORK>
```

Notes:
- One `- - - - -` group per zone. Omit a zone section entirely if no vaults exist in that zone.
- If user filtered by asset, show only matching vaults and replace title with: `💰 Lista Lending — <ASSET> Vault Yield`.
- If `emissionApy` is 0 or emission is disabled, show `0%` for LISTA bonus / LISTA 加成.

### 繁體中文

```
💰 Lista Lending — Vault 收益
<YYYY-MM-DD HH:MM> UTC  |  <NETWORK>
━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 Classic（已審計）

- - - - -

#1  WBNB 金庫（WBNB）
基礎年化：4.2%
LISTA 加成：2.1%
總年化：6.3%
TVL：＄18.2M
利用率：52%
底層市場：slisBNB/WBNB 39% ⚡、PT-slisBNBx/WBNB 21% 🔒


#2  USD1 金庫（USD1）
基礎年化：3.1%
LISTA 加成：1.8%
總年化：4.9%
TVL：＄8.3M
利用率：61%
底層市場：BTCB/USD1 44%、WBNB/USD1 32%


#3  U 金庫（U）
基礎年化：2.5%
LISTA 加成：0%
總年化：2.5%
TVL：＄5.1M
利用率：48%
底層市場：slisBNB/U 52%、BTCB/U 30%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Alpha（較高風險）

- - - - -

#1  WBTC 金庫（WBTC）
基礎年化：14.2%
LISTA 加成：0%
總年化：14.2%
TVL：＄420K
利用率：78%
底層市場：WBTC/USD1 100%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Aster（合作夥伴資產）

- - - - -

#1  ASTER 金庫（ASTER）
基礎年化：8.5%
LISTA 加成：0%
總年化：8.5%
TVL：＄120K
利用率：45%
底層市場：ASTER/USDT 100%

- - - - -

━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Smart Lending  |  🔒 固定利率

資料來源：<DATA_SOURCE>  |  <NETWORK>
```
