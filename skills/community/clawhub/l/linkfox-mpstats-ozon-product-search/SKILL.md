---
name: linkfox-mpstats-ozon-product-search
version: 1.0.1
category: product-sourcing
description: MPSTATS Ozon 俄罗斯站商品搜索与反查。按俄语关键词、SKU、品牌名或卖家名在 MPSTATS 数据库中检索 Ozon 商品，返回商品 ID、标题、品牌和卖家信息，是 Ozon 选品与竞品链路的起点。当用户提到 Ozon 选品、Ozon 商品搜索、俄罗斯电商选品、Ozon 关键词搜索、Ozon SKU 查询、Ozon 品牌搜品、Ozon 卖家搜品、MPSTATS Ozon、Ozon product search, MPSTATS Ozon, Russian marketplace, Ozon SKU lookup, Ozon keyword search, Ozon brand/seller search 时触发此技能。即使用户未明确提到"MPSTATS"，只要其意图是在 Ozon 俄罗斯站按关键词/品牌/卖家发现或反查商品，也应触发此技能。
---

# MPSTATS Ozon Product Search

This skill searches Ozon (Russia) products in the MPSTATS analytics database by Russian keyword, SKU list, brand name, or seller name. It is the **entry point** for Ozon product discovery and competitor lookup — downstream drill-downs (brand/category/seller/detail/trend) typically start from the IDs returned here.

## Core Concepts

**MPSTATS Ozon coverage**: Ozon is Russia's largest general-category marketplace. MPSTATS indexes Ozon product listings and sales history. This endpoint returns the **basic identity card only** — 10 fields: `productId` / `title` / `productPageUrl` / `imageUrl` / `brand` / `brandId` / `sellerName` / `sellerId` plus `sourceType` / `sourceTool`. Per-SKU price / sales / rating / stock / turnover / ranking are **not** returned here — the backend `OzonProductSearchItem` DTO is intentionally narrow. For those metrics, chain into `mpstats-ozon-product-detail` (batch full card, 36 fields) or the `brand/category/seller-products` drill-downs (39 fields).

**Language requirement**: Keywords, brand names, and seller names must be in **Russian** (Cyrillic) — or the Latin-script form actually used on the Ozon storefront (e.g., `adidas`). If the user supplies an English or Chinese keyword, translate it to Russian first and note the translation.

**At-least-one input rule**: The input schema marks all four filters as optional, but the tool's business rule requires at least one of `keyword` / `productIds` / `brandNames` / `sellerNames` to be supplied. The four can be combined to narrow results.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| keyword | string | conditional | Russian search keyword, e.g., `кроссовки` (sneakers) |
| productIds | array<integer\|string> | conditional | Ozon SKU list |
| brandNames | array<string> | conditional | Brand display names (Russian or Latin) |
| sellerNames | array<string> | conditional | Seller display names (Russian) |
| startDate | string | no | Stats window start, `YYYY-MM-DD`; defaults to one year ago |
| endDate | string | no | Stats window end, `YYYY-MM-DD`; defaults to yesterday, **cannot** be today or future |
| page | integer | no | Page number, starts at 1 |
| pageSize | integer | no | Rows per page, 1-100, default 100 |

At least one of `keyword` / `productIds` / `brandNames` / `sellerNames` must be supplied.

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, response structure, and error codes. You can also execute `scripts/mpstats_ozon_product_search.py` directly for ad-hoc queries.

## Usage Examples

**1. Keyword search — sneakers in Russian**
```json
{"keyword": "кроссовки", "pageSize": 50}
```

**2. SKU batch reverse lookup**
```json
{"productIds": [1786874757, 151623766, 142257239]}
```

**3. Brand-scoped discovery**
```json
{"brandNames": ["adidas", "Xiaomi"], "keyword": "наушники"}
```

**4. Seller-scoped discovery**
```json
{"sellerNames": ["ООО Ромашка"], "pageSize": 100}
```

**5. Dated window for period-specific search**
```json
{"keyword": "футболка", "startDate": "2025-02-01", "endDate": "2025-02-28"}
```

## How to Chain with Other Ozon Skills

1. **Keyword → drill-down**: Search → pick `productId` → call `mpstats-ozon-product-detail` (batch metrics) or `mpstats-ozon-product-trend` (single-SKU time-series).
2. **Brand discovery → brand drill-down**: Use this skill to confirm the exact brand display name, then call `mpstats-ozon-brand-products` for full sales / stock / rating metrics.
3. **Seller scouting → seller drill-down**: Confirm the seller via this skill, read the `sellerId` from the result, then call `mpstats-ozon-seller-products` for the seller's full SKU map.

## Display Rules

1. **Lead with identity columns** — this endpoint returns only 10 identity fields. Headline the table with `productId`, `title`, `brand`, `sellerName`; include `productPageUrl` / `imageUrl` as secondary columns. Do **not** add price / sales / rating / stock columns — they are not in the response.
2. **Russian titles** — preserve the original Russian title; optionally offer an English or Chinese translation on user request.
3. **Pagination** — when `total` exceeds the page size, tell the user the total count and suggest the next page or a narrower keyword.
4. **Route to drill-downs for any business metric** — business metrics are never in this response. If the user asks for sales / price / rating / stock / turnover / ranking, **always** route to `mpstats-ozon-product-detail` (single or batch) or the `*-products` drill-downs. Do not fabricate or estimate from identity fields.
5. **Error handling** — when `code` / `errcode` is non-200, explain the reason from `msg` / `errmsg` and suggest adjusting inputs (supply at least one of the four filters, use Russian, narrow date range).

## Important Limitations

- **At least one filter required** — empty payloads are rejected by the tool's business rule even though `required` is empty in inputSchema.
- **Russian / Latin only** — non-Russian keywords generally return empty results.
- **Date range** — `endDate` cannot be today or a future date; data is T-1.
- **Result cap per page** — `pageSize` max is 100; paginate for larger sets.
- **No business metrics** — price / sales / rating / stock / turnover / ranking are **not** in this endpoint's response at all. The backend `OzonProductSearchItem` DTO declares exactly 10 identity fields. This is a hard contract, not a sparse payload — do not assume missing metric fields could be filled in by re-calling with different dates.

## User Expression & Scenario Quick Reference

**Applicable** — Ozon product discovery / identity resolution:

| User Says | Scenario |
|-----------|----------|
| "Search Ozon for sneakers / headphones / ..." | Keyword discovery |
| "I have a list of Ozon SKUs, pull their names" | Batch SKU reverse lookup |
| "What does brand X sell on Ozon" | Brand-scoped candidate listing |
| "What does seller Y sell on Ozon" | Seller-scoped candidate listing |
| "Translate this keyword to Russian and search Ozon" | Cross-language discovery |

**Not applicable** — Needs beyond discovery:

- Reliable per-SKU sales / revenue / stock / rating metrics → use `mpstats-ozon-product-detail` (batch card) or the `*-products` drill-down skills.
- Time-series trend for a single SKU → use `mpstats-ozon-product-trend`.
- Wildberries or other non-Ozon Russian marketplaces → not covered here.
- Category-tree navigation / Russian category path lookup → use `mpstats-ozon-category-products` with a known path.

**Boundary judgment**: If the user wants to **find or identify** Ozon products, start here. If they already have an ID or a dimension (brand / category / seller) and want **metrics** under it, go to the corresponding drill-down skill directly.

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
