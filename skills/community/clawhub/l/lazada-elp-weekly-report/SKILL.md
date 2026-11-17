---
name: "lazada-elp-weekly-report"
description: "Generate Chinese and English weekly reports for Lazada LazFlash ELP module across 6 SEA countries from dashboard xlsx data."
---

# Lazada ELP Weekly Report Generation

## Overview

Generate bilingual (Chinese + English) weekly reports for the Everyday Low Price (ELP) module under the LazFlash channel, covering 6 SEA countries: PH, ID, TH, MY, SG, VN.

## Input Files

1. **Weekly Data.xlsx** — Dashboard raw data containing:
   - 6 country-specific Performance Summary tabs (e.g. `PH-Performance Summary`, `ID-Performance Summary `, etc.)
   - 1 Traffic Performance tab (all countries in one sheet)
2. **Dashboard User Guide.docx** — Dashboard structure and metric definitions
3. **Weekly Report Demo.docx** — Previous report example for structure/style reference

## Country Configuration

| Country | Price Anchor | ~USD | Notes |
|---------|-------------|------|-------|
| PH | PHP199 | ~$3.3 | — |
| ID | IDR50k | ~$2.8 | — |
| TH | THB149 | ~$4.5 | — |
| MY | RM30 | ~$7.4 | Free shipping threshold $7 |
| SG | SGD4.99 | ~$3.9 | Free shipping threshold $10 |
| VN | VND100k | ~$3.8 | — |

## Data Extraction

### Performance Summary (per country tab)

#### Direct-read Metrics

| Metric | Cell | Format |
|--------|------|--------|
| 整体成功招商商品数 (Total enrolled items) | B7 | Integer |
| 整体成功招商商品数环比 (Enrolled items WoW) | C7 | % |
| 大盘动销率 (Platform sell-through rate) | B4 | % |
| 大盘动销率环比 (Platform sell-through rate WoW) | C4 | pt |
| 大盘动销商品数 (Platform selling items) | B8 | Integer |
| 大盘动销商品数环比 (Platform selling items WoW) | C8 | % |
| 频道动销率 (LazFlash sell-through rate) | B14 | % |
| 频道动销率环比 (LazFlash sell-through rate WoW) | C14 | pt |
| 频道动销商品数 (LazFlash selling items) | B17 | Integer |
| 频道动销商品数环比 (LazFlash selling items WoW) | C17 | % |
| 日均平台订单数 (Daily avg platform orders) | B23 | Integer |
| 日均平台订单数环比 (Daily avg platform orders WoW) | C23 | % |
| 日均平台GMV (Daily avg platform GMV) | B24 | Integer (USD) |
| 日均平台GMV环比 (Daily avg platform GMV WoW) | C24 | % |
| 频道引导订单数 (LazFlash-guided orders) | B32 | Integer |
| 频道引导订单数环比 (LazFlash-guided orders WoW) | C32 | % |
| 频道引导GMV (LazFlash-guided GMV) | B33 | Integer (USD) |
| 频道引导GMV环比 (LazFlash-guided GMV WoW) | C33 | % |

#### Calculated Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| OrderC | B23 / SUM(D26:J26) | Daily avg platform orders / sum of 7-day venture_ord |
| GMVC | B24 / SUM(D27:J27) | Daily avg platform GMV / sum of 7-day venture_gmv |
| 占比频道整体订单数 (Share of LazFlash total orders) | B32 / SUM(D37:J37) | Guided orders / sum of 7-day venture_guided_ord |
| 占比频道整体GMV (Share of LazFlash total GMV) | B33 / SUM(D38:J38) | Guided GMV / sum of 7-day venture_guided_gmv |

### Traffic Performance (single tab, rows by country)

Country row mapping: ID=2, MY=3, PH=4, SG=5, TH=6, VN=7

| Metric | Column | Format |
|--------|--------|--------|
| DAU | B | Integer |
| DAU环比 (DAU WoW) | C | % |
| DAU占比频道 (DAU share in LazFlash channel) | E | % |
| UVCR | F | % |
| UVCR环比 (UVCR WoW) | G | pt |
| UVCR对比频道均值 (UVCR vs channel avg) | I | pt |

## Data Validation Rules

1. **NEVER fabricate or estimate data.** If a cell is empty/null, mark as "缺失" / "N/A" — do not guess.
2. **WoW format**: Use "%" for volume/count metrics, use "pt" for rate metrics.
3. **Division safety**: Before computing calculated metrics, verify denominator is non-zero and non-null.
4. **Cross-check**: If a WoW value seems implausible (e.g. >100% or <-90%), flag it for review.

## Report Output Structure

### Chinese Report Template

```
周报周期：MM.DD-MM.DD

PH(PHP199, 约$3.3)
本周洞察：[Multi-sentence analysis based on data. Highlight notable WoW changes. If a metric has large WoW fluctuation but root cause cannot be determined from data alone, write "建议进一步分析波动原因".]
招商概览：整体成功招商商品数[X]，环比[X%]。
大盘表现：大盘动销商品数[X]（环比[X%]），动销率[X%]（环比[Xpt]）；日均平台订单数[X]（环比[X%]），OrderC [X%]；日均平台GMV $[X]（环比[X%]），GMVC [X%]。
频道表现：频道动销商品数[X]（环比[X%]），动销率[X%]（环比[Xpt]）；频道引导订单数[X]（环比[X%]），占比频道整体订单数[X%]；频道引导GMV $[X]（环比[X%]），占比频道整体GMV [X%]。
模块效率：DAU [X]（环比[X%]，占比频道[X%]），UVCR [X%]（环比[Xpt]，较频道整体[Xpt]）。

[Repeat for each country: ID, TH, MY, SG, VN]
```

### English Report Template

```
Report Period: MM.DD-MM.DD

PH(PHP199, ~$3.3)
Key Insight: [Multi-sentence analysis. Highlight notable WoW changes. If a metric has large WoW fluctuation but root cause cannot be determined from data alone, write "Further analysis recommended to investigate the fluctuation."]
Enrollment Overview: Total successfully enrolled items: [X] (WoW [X%]).
Platform Performance: Platform selling items: [X] (WoW [X%]), sell-through rate [X%] (WoW [Xpt]); Daily average platform orders: [X] (WoW [X%]), OrderC [X%]; Daily average platform GMV: $[X] (WoW [X%]), GMVC [X%].
LazFlash Performance: LazFlash selling items: [X] (WoW [X%]), sell-through rate [X%] (WoW [Xpt]); LazFlash-guided orders: [X] (WoW [X%]), accounting for [X%] of total LazFlash orders; LazFlash-guided GMV: $[X] (WoW [X%]), accounting for [X%] of total LazFlash GMV.
Module Efficiency: DAU [X] (WoW [X%], [X%] of LazFlash channel), UVCR [X%] (WoW [Xpt], [Xpt] vs channel average).

[Repeat for each country: ID, TH, MY, SG, VN]
```

## Key Insight Writing Guidelines

The "本周洞察" / "Key Insight" section should:
1. Be **data-driven** — reference specific metrics and their WoW changes
2. Identify **patterns** — e.g. enrollment down but sell-through rate up; or all metrics declining together
3. Flag **anomalies** — if any metric has unusually large WoW change (>20% or >5pt), mention it
4. If the cause of a large fluctuation **cannot be determined from the data alone**, explicitly state:
   - Chinese: "建议进一步分析波动原因"
   - English: "Further analysis recommended to investigate the fluctuation"
5. Compare module performance **vs channel average** where relevant (UVCR comparison)
6. Keep it concise but informative — typically 2-4 sentences

## Execution Steps

1. Read Weekly Data.xlsx, identify all sheet names
2. Match each country to its Performance Summary tab (handle trailing spaces in sheet names)
3. For each country: extract all direct-read metrics from Performance Summary tab
4. Compute calculated metrics (OrderC, GMVC, order share, GMV share)
5. Read Traffic Performance tab for traffic metrics
6. Validate data completeness — flag any missing values
7. Generate "本周洞察" / "Key Insight" for each country based on data patterns
8. Assemble Chinese report following template
9. Assemble English report following template
10. Output both reports

## Technical Notes

- Use `openpyxl` with `data_only=True` to read computed values
- Sheet names may have trailing spaces (e.g. `ID-Performance Summary `) — use `.strip().startswith(country + '-')` for matching
- Traffic Performance country order: ID(row2), MY(row3), PH(row4), SG(row5), TH(row6), VN(row7)
- Percentage values in cells are stored as decimals (e.g. 0.6317 = 63.17%)
- WoW values in C column are pre-formatted strings (e.g. "+8.53pt", "-25.3%")
