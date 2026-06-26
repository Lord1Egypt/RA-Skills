---
name: linkfox-mpstats-ozon-brand-products
version: 1.0.0
category: product-sourcing
description: MPSTATS Ozon 俄罗斯站按品牌下钻商品列表。按 Ozon 品牌展示名（俄语/拉丁）返回该品牌下全部商品的销量、销售额、价格、评分、库存、周转、损失销售额等完整指标，支持多维数值筛选、排序、货币换算。用于品牌对标、竞品分析、品牌商品结构研究、ASIN 级（productId 级）爆款拆解。当用户提到 Ozon 品牌下钻、Ozon 品牌商品、Ozon 竞品品牌分析、品牌结构、品牌 SKU、品牌爆款、Ozon 品牌销售、MPSTATS brand, Ozon brand products, brand drill-down, brand competitor analysis, Russian marketplace brand SKUs, brand revenue share 时触发此技能。即使用户未明确说"MPSTATS"，只要意图是按 Ozon 品牌看该品牌下所有商品及其销量/价格/评分表现，也应触发此技能。
---

# MPSTATS Ozon Brand Products

This skill drills into all Ozon (Russia) products sold under a given brand display name, returning each SKU's sales, revenue, price, rating, stock, turnover, lost profit, and more. Built for brand competitor audits, brand SKU structure analysis, and bestseller dissection.

## Core Concepts

**Brand display name**: `brandName` must match what's shown on the Ozon storefront — typically Russian (Cyrillic) or Latin (`adidas`, `Xiaomi`). Do **not** pass a category path, a seller ID, or an internal brand code here. If unsure of the exact spelling, resolve via `mpstats-ozon-product-search` first.

**Filters are AND-combined**: The `filters` array supports multiple numeric conditions ANDed together. Each filter is `{field, op, value, value2?}`. Common fields and operators are in the Filter Reference below.

**Currency & rate**: Default currency is **RUB**. Set `currency: "USD"` (or another code) to have monetary fields converted server-side; `currencyRate` lets you override the default rate if desired.

**FBO / FBS mix**: `includeFbs: true` folds FBS (seller-shipped) stock + sales into the numbers; `false` keeps them FBO-only.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| brandName | string | yes | Ozon brand display name (Russian or Latin) |
| startDate | string | no | Stats window start, `YYYY-MM-DD`; latest = yesterday |
| endDate | string | no | Stats window end, `YYYY-MM-DD`; latest = yesterday |
| page | integer | no | Page number, starts at 1 |
| pageSize | integer | no | Rows per page, 1-100, default 100 |
| sortField | string | no | snake_case column: `sales`, `revenue`, `final_price`, `balance`, `rating`, ... |
| sortDirection | string | no | `asc` or `desc` |
| currency | string | no | Currency code, default `RUB`; e.g. `USD`, `EUR`, `CNY` |
| currencyRate | integer | no | Custom rate when non-default currency is used |
| includeFbs | boolean | no | Include FBS data |
| filters | array | no | Numeric filter conditions (see below) |

## Filter Reference

Each `filters` entry: `{"field": "<snake_case>", "op": "<OP>", "value": <num>, "value2": <num?>}`.

**Common fields**: `sales` (monthly units), `final_price` (selling price RUB), `rating` (0-5), `comments` (review count), `balance` (stock), `revenue` (sales amount RUB), `days_in_stock`, `turnover_days`, `lost_profit`, `category_position`.

**Operators**: `GTE`, `LTE`, `GT`, `LT`, `EQ`, `NOT_EQ`, `BETWEEN` (requires `value2` as the upper bound).

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, response structure, and error codes. You can also execute `scripts/mpstats_ozon_brand_products.py` directly for ad-hoc queries.

## Usage Examples

**1. Top-50 by sales for brand `adidas`**
```json
{
  "brandName": "adidas",
  "sortField": "sales",
  "sortDirection": "desc",
  "pageSize": 50
}
```

**2. High-rating, mid-price filter**
```json
{
  "brandName": "Xiaomi",
  "filters": [
    {"field": "rating", "op": "GTE", "value": 4.5},
    {"field": "final_price", "op": "BETWEEN", "value": 1000, "value2": 5000}
  ],
  "sortField": "revenue",
  "sortDirection": "desc"
}
```

**3. USD-converted output**
```json
{
  "brandName": "Nike",
  "currency": "USD",
  "sortField": "revenue"
}
```

**4. Include FBS + only in-stock items**
```json
{
  "brandName": "adidas",
  "includeFbs": true,
  "filters": [{"field": "balance", "op": "GT", "value": 0}]
}
```

**5. Lost-profit hunters (out-of-stock pain)**
```json
{
  "brandName": "Nike",
  "filters": [{"field": "lost_profit", "op": "GTE", "value": 100000}],
  "sortField": "lost_profit",
  "sortDirection": "desc"
}
```

## Display Rules

1. **Compact brand table** — key columns: `productId`, `title`, `price`, `monthlySalesUnits`, `monthlySalesRevenue`, `rating`, `reviewCount`, `balance`, `turnoverDays`, `lostProfit`.
2. **Revenue share context** — `revenueSharePercent` is the SKU's share **within this brand result set**, 0-100; clarify the base when presenting.
3. **Currency labeling** — always state the currency in the table header; if `currency` was overridden, note "已按 USD 换算".
4. **Russian titles** — preserve original; translate on user request.
5. **Pagination** — report total and guide the user to next page or narrower filters when total exceeds the returned page.
6. **No business advice** — present the data; don't project future sales from a snapshot.

## Important Limitations

- **Exact brand-name match** — no fuzzy search; typos return empty results. Verify via `mpstats-ozon-product-search` if unsure.
- **Page cap** — max 100 rows per page; paginate for larger brands.
- **Date window** — `endDate` cannot be today or a future date (T-1 data).
- **Currency conversion** — server-side; historical rates may differ slightly from the user's reference rate.
- **Russian-only titles** — translate only when asked.

## User Expression & Scenario Quick Reference

**Applicable** — Brand-scoped Ozon product metrics:

| User Says | Scenario |
|-----------|----------|
| "Show me adidas's top-selling Ozon SKUs" | Brand bestseller drill |
| "What does Xiaomi sell on Ozon, sorted by revenue" | Brand revenue structure |
| "Which brand-X SKUs have rating ≥4.5 and stock >0" | Brand quality filter |
| "Are brand-X's stockouts causing big lost profit" | Lost-profit hunter |
| "Convert brand-X's Ozon sales to USD" | Currency-normalized audit |

**Not applicable** — Needs beyond brand drill-down:

- Unknown exact brand name → first use `mpstats-ozon-product-search`
- Category-level comparison across brands → use `mpstats-ozon-category-products`
- Seller-scoped analysis → use `mpstats-ozon-seller-products`
- Single-SKU time-series → use `mpstats-ozon-product-trend`
- Wildberries / other Russian marketplaces → not covered

**Boundary judgment**: Use this skill when the question centers on **one brand** and you want the per-SKU rollup under it. For "which brand dominates category X" use category drill-down and compare brand rows server-side.

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
