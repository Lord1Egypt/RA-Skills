---
name: linkfox-mpstats-ozon-product-trend
version: 1.0.0
category: product-sourcing
description: MPSTATS Ozon 俄罗斯站单个 SKU 的分日时间序列表现。按日期粒度返回一个 Ozon 商品的销量、价格、库存、评分等指标，可选附带搜索位次/可见性数据，用于验证增长趋势、季节性、异常波动。当用户提到 Ozon 趋势、Ozon 销量趋势、Ozon 价格走势、Ozon 分日数据、Ozon 库存走势、Ozon 搜索位次、Ozon 商品历史、MPSTATS trend, Ozon daily performance, Ozon time series, Ozon search visibility, Russian marketplace product history 时触发此技能。即使用户未明确说"MPSTATS"，只要意图是看某个 Ozon 商品的分日/时间段走势，也应触发此技能。
---

# MPSTATS Ozon Product Trend (Daily Time-Series)

This skill returns a daily time-series of a single Ozon (Russia) SKU — sales units, price, stock, rating, and optionally search-position / visibility metrics. It is the go-to for validating growth, seasonality, or anomalies for a specific product.

## Core Concepts

**Single-SKU scope**: Each call analyzes exactly **one** `productId`. For batch per-SKU snapshots (period aggregates), use `mpstats-ozon-product-detail` instead.

**Daily granularity**: The response is an array of daily points (top-level field `data`) across the `[startDate, endDate]` window. Each point carries a `hasData` boolean — if `hasData=false`, the day has no observation (distinct from `sales=0` with `hasData=true`).

**T-1 delay**: MPSTATS trend data is delayed by one day; the latest selectable end date is **yesterday**. Today or future dates are rejected.

**Search-visibility add-on**: Set `includeSearchStats: true` to append search-position / visibility signals. Some niches (especially small categories) may not have search-stats coverage — expect partial or empty fields in those cases.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| productId | integer | yes | Ozon SKU (numeric) |
| startDate | string | no | Window start, `YYYY-MM-DD`; latest = yesterday |
| endDate | string | no | Window end, `YYYY-MM-DD`; latest = yesterday |
| includeFbs | boolean | no | Include FBS data alongside FBO |
| includeSearchStats | boolean | no | Attach search position / visibility signals |

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, response structure, and error codes. You can also execute `scripts/mpstats_ozon_product_trend.py` directly for ad-hoc queries.

## Usage Examples

**1. Monthly trend for a SKU**
```json
{
  "productId": 1786874757,
  "startDate": "2025-03-01",
  "endDate": "2025-03-31"
}
```

**2. Trend with search visibility**
```json
{
  "productId": 1786874757,
  "startDate": "2025-02-01",
  "endDate": "2025-02-28",
  "includeSearchStats": true
}
```

**3. Combined FBO+FBS trend**
```json
{
  "productId": 151623766,
  "startDate": "2025-01-01",
  "endDate": "2025-01-31",
  "includeFbs": true
}
```

## How to Chain with Other Ozon Skills

1. **Discovery → trend**: Use `mpstats-ozon-product-search` to find a SKU, then check growth / volatility here before committing.
2. **Aggregate vs time-series**: `mpstats-ozon-product-detail` gives a one-number-per-metric period view; this skill shows the day-by-day shape behind those numbers.
3. **Drill-down → trend**: After `brand-products` / `category-products` / `seller-products` surfaces a hot SKU, use this skill to validate whether the hotness is recent, seasonal, or sustained.

## Display Rules

1. **Prefer a simple table or sparkline-friendly output** — one row per date with `date`, `price`, `sales`, `balance`, `rating`, `comments`; do not overfit a 90-point series into a single paragraph.
2. **Use `hasData` to distinguish gaps from zero sales** — `hasData=false` means the day has no observation; don't report it as a zero-sale day.
3. **Call out anomalies** — large single-day spikes or stockouts (`balance=0` runs where `hasData=true`) should be flagged factually, not as buying advice.
4. **Currency is RUB** unless upstream layer is already converting (the `currency` field per point carries the symbol, e.g. `₽`); state the currency when showing price movement.
5. **Revenue is not returned per day** — if the user asks for daily revenue, estimate via `sales * price` and note it's an estimate.
6. **`includeSearchStats` gaps** — when no search-visibility fields come back, note "搜索位次数据在该赛道暂不可用" rather than silently omitting.
7. **No business advice** — present the shape; leave "should we buy this listing?" to the user.

## Important Limitations

- **Single SKU per call** — cannot pass a list of `productId`s; loop at the Agent layer if needed.
- **T-1 data** — `endDate` cannot be today or a future date.
- **Search stats optional** — `includeSearchStats=true` doesn't guarantee coverage for all niches.
- **Ozon-only** — Wildberries and other Russian marketplaces are not covered.
- **Missing days** — the series may have nulls / gaps where no data was captured; do not treat nulls as zero sales.

## User Expression & Scenario Quick Reference

**Applicable** — Single-SKU temporal analysis:

| User Says | Scenario |
|-----------|----------|
| "What's the sales trend of Ozon SKU 1786874757 last month" | Monthly time-series |
| "Is this Ozon listing seasonal or stable" | Seasonality check |
| "Did this Ozon product have stockouts recently" | Stock anomaly detection |
| "Price walk for this Ozon product over Q1" | Price movement |
| "Did this listing's search position improve" | Search visibility (requires `includeSearchStats`) |

**Not applicable** — Needs beyond single-SKU time-series:

- Batch snapshot of many SKUs → `mpstats-ozon-product-detail`
- Brand / category / seller drill-down → matching `*-products` skill
- Pre-IDed discovery → `mpstats-ozon-product-search`

**Boundary judgment**: Use this skill when the question starts with "how did this ONE product change over time". For multi-SKU comparisons or dimension-level filtering, go elsewhere.

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
