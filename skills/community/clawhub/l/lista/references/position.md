> Follow the FORMAT ENFORCEMENT rules from SKILL.md. Output must match templates character-for-character.

# Report A — Position Report

Generates a full position report with collateral, debt, LTV, LTV gap, liquidation price, and strategy recommendations.

## A.1 — Fetch position data

Run once per address using MCP:

```
lista_get_position({ wallet: "<address>" })
```

Returns `holdings.objs[]` (active markets with `marketId`, `collateralSymbol`, `loanSymbol`, `collateralPrice`, `loanPrice`, `zone`, `termType`), `collaterals[]` (per-market amount/usdValue), and `borrows[]` (per-market pre-computed debt amount/usdValue).

If `holdings.objs` is empty → "No active positions."

Then fetch LLTV per unique loan token — use `keyword` to avoid fetching all 100+ markets:

```
lista_get_borrow_markets({ keyword: "<loanSymbol>", pageSize: 50 })
```

Match each returned market by `id` to the user's active market IDs. Use the `lltv` field. If a market is not found on page 1, paginate with `page: 2`.

**Fallback — moolah.js** (if MCP unavailable):
```bash
node skills/lista/scripts/moolah.js --chain <bsc|eth> dashboard <address>
```
Returns JSON with `positions[]` containing pre-computed metrics (`ltv`, `healthFactor`, `liqPriceUsd`, `buffer`, `riskLevel`, `netEquityUsd`). All values are human-readable — no conversion needed.

**Fallback — curl**: Position data requires API calls. Without MCP or Node.js, report cannot run.

## A.2 — Compute metrics

Join data by marketId and compute per `references/domain.md`. Amounts are human-readable — no 1e18 conversion needed.

## A.3 — Recommendations

Generate 1–3 concise suggestions per address based on actual numbers. Use the unified ltvGap thresholds from `references/domain.md`.

**🔴 DANGER (ltvGap <= danger threshold):**
- Repay debt or add collateral immediately. Show amounts to widen ltvGap past the warning threshold.

**🟡 WARNING (danger < ltvGap <= warning threshold):**
- Partial repayment or top-up recommended. Show amounts to reach 🟢 SAFE zone (ltvGap > warning threshold).

**🟢 SAFE — yield enhancement (ltvGap > warning threshold):**
- Suggest leveraging via /lista-loop.
- Supply-only: Mention borrowing to amplify yield.

## A.4 — Output template

⛔ STOP BEFORE OUTPUTTING. You MUST copy the template below character-for-character. Substitute `<placeholder>` values with real data. Change NOTHING else — no bullet points, no overview section, no preamble, no trailing remarks. Your response must start with the exact first line shown in the template.

### English

```
Lista Lending — Position Report
Generated: <YYYY-MM-DD HH:MM> UTC  |  <NETWORK>
━━━━━━━━━━━━━━━━━━━━━━━━━

Address 1: 0xAbCd…5678

- - - - -

#1  BTCB / U
Risk: 🟢 SAFE
Collateral: 398.85 BTCB (~＄38.25M)
Debt: 18,020,988 U (~＄18.02M)
Net equity: ~＄20.23M
LTV / LLTV: 47.1% / 86.0%
LTV gap: 38.9% (threshold: 5.0%)
Liq. price: BTCB < ＄52,500 (now ＄96,000)


#2  slisBNB/BNB LP / BNB
Risk: 🟢 SAFE (correlated)
Collateral: 120.00 LP (~＄78,143 @ ＄651.19/LP)
Debt: 50.00 BNB (~＄34,550)
Net equity: ~＄43,593
LTV / LLTV: 44.2% / 86.0%
LTV gap: 41.8% (threshold: 0.5%)
Liq. price: LP < ＄335 (now ＄651.19)

- - - - -

Address 1 summary: 2 active positions  |  Net equity ~＄20.2M

Recommendations:
  1. LTV is comfortable — consider /lista-loop to amplify yield.

━━━━━━━━━━━━━━━━━━━━━━━━━

Total: <N> addresses  |  <M> active positions  |  Combined net equity ~＄X
Threshold: LLTV >= 90% → D 0.5% W 1.0% | LLTV < 90% → D 5.0% W 10.0%

Data: <DATA_SOURCE>  |  <NETWORK>
```

Notes:
- Supply-only positions: Debt, LTV / LLTV, LTV gap, Liq. price show `—`.
- LP collateral: show LP price in the Collateral line, e.g. `120.00 LP (~＄78,143 @ ＄651.19/LP)`.
- If user filtered by asset, replace title with: `Lista Lending — <ASSET> Position Report`.

### 繁體中文

```
Lista Lending — 持倉報告
產生時間：<YYYY-MM-DD HH:MM> UTC  |  <NETWORK>
━━━━━━━━━━━━━━━━━━━━━━━━━

地址 1：0xAbCd…5678

- - - - -

#1  BTCB / U
風險：🟢 安全
抵押品：398.85 BTCB（約 ＄38.25M）
負債：18,020,988 U（約 ＄18.02M）
淨資產：約 ＄20.23M
LTV / 清算線：47.1% / 86.0%
LTV 差距：38.9%（閾值：5.0%）
清算價格：BTCB < ＄52,500（現 ＄96,000）


#2  slisBNB/BNB LP / BNB
風險：🟢 安全（相關對）
抵押品：120.00 LP（約 ＄78,143 @ ＄651.19/LP）
負債：50.00 BNB（約 ＄34,550）
淨資產：約 ＄43,593
LTV / 清算線：44.2% / 86.0%
LTV 差距：41.8%（閾值：0.5%）
清算價格：LP < ＄335（現 ＄651.19）

- - - - -

地址 1 小結：2 個活躍持倉  |  淨資產約 ＄20.2M

持倉建議：
  1. LTV 尚在安全範圍，可考慮使用 /lista-loop 提高槓桿收益。

━━━━━━━━━━━━━━━━━━━━━━━━━

總計：<N> 個地址  |  <M> 個活躍持倉  |  合計淨資產約 ＄X
預警閾值：LLTV >= 90% → D 0.5% W 1.0% | LLTV < 90% → D 5.0% W 10.0%

資料來源：<DATA_SOURCE>  |  <NETWORK>
```
