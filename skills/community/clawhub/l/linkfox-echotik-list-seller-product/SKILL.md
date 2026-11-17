---
name: linkfox-echotik-list-seller-product
description: 查询某个TikTok Shop店铺（卖家）的在售商品列表，通过sellerId获取该店铺全部商品，返回商品标题、价格、多周期(1天/7天/15天/30天/60天/90天/总)销量与销售额(GMV)、评分、评论数、佣金比例、上架时间、带货方式、品类等指标。当用户提到TikTok店铺商品、TikTok店铺在售商品、TikTok卖家商品列表、TikTok店铺选品、查看TikTok店铺卖什么、TikTok店铺商品分析、EchoTik店铺商品、TikTok Shop seller products, TikTok store products, TikTok seller product list, EchoTik store product list时触发此技能。即使用户未明确提及"EchoTik"或"TikTok"，只要其需求涉及查看某个TikTok Shop店铺（已知sellerId）的在售商品及其销量/价格/佣金表现，也应触发此技能。
---

# EchoTik TikTok Seller Product List

This skill lists the in-store products of a single TikTok Shop seller (store) by its `sellerId`, helping cross-border sellers and marketers see exactly what a store sells and how each product performs — multi-period sales and GMV, price, rating, reviews, and commission rate.

## Core Concepts

EchoTik is a TikTok Shop analytics platform. Given a store's `sellerId`, this tool returns that store's product catalog with per-product metrics: title, image, price (and SPU average / min / max), sales volume and GMV across 1d/7d/15d/30d/60d/90d/total windows, rating, review count, commission rate, listing date, sales channel, and category.

**Where to get a `sellerId`**: Obtain it from the **EchoTik TikTok Seller Search** skill (`linkfox-echotik-list-seller`), which lists and filters TikTok Shop stores by region, category, GMV, trend, and store type; or from the **EchoTik TikTok Seller Detail** skill (`linkfox-echotik-seller-detail`).

**Pagination quirk**: `pageSize` must be a multiple of 10 (max 100). The official upstream API caps a single page at 10; this tool internally pulls multiple pages of 10 and merges them, so `pageSize=50` returns up to 50 merged products.

## Data Fields

The response's `products` array contains product objects. Key fields:

| Field | Description |
|-------|-------------|
| productId / asin | Product unique ID |
| title / productName | Product title |
| imageUrl / coverUrl | Product image URL |
| productImageUrls | Product image URL list |
| price | Product price |
| spuAvgPrice | SPU average price |
| minPrice / maxPrice | Min / max price |
| currency | Currency |
| totalSaleCnt | Total sales volume |
| totalSale1dCnt / 7dCnt / 15dCnt / 30dCnt / 60dCnt / 90dCnt | Sales volume (1d/7d/15d/30d/60d/90d, incremental) |
| totalSaleGmvAmt | Total GMV (revenue) |
| totalSaleGmv1dAmt / 7dAmt / 15dAmt / 30dAmt / 60dAmt / 90dAmt | GMV (1d/7d/15d/30d/60d/90d, incremental) |
| monthlySalesUnits | Monthly sales |
| productRating | Product rating |
| ratings / reviewCount | Review count |
| productCommissionRate | Commission rate (decimal, e.g. 0.05 = 5%) |
| categoryName / categoryIds | Product category name / ID list |
| salesFlagText | Main sales channel (video/livestream) |
| salesTrendFlagText | Sales trend |
| firstCrawlDt / availableDate | Listing date (YYYYMMDD integer / date string) |
| discount / offMarkText / freeShippingText | Discount / promo mark / free-shipping flag |
| isSShopText | S-store flag |
| salePropsInfo | Sales attribute info (variants: propId/propName/propValue) |
| region | Marketplace code |
| sourceTool / sourceType | Source tool / type |

Top-level fields: `errcode`, `errmsg`, `total`, `columns`, `type`, `costToken`.

## Parameter Guide

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| sellerId | string | Yes | - | TikTok Shop store ID. Obtain from the Seller Search / Seller Detail skill. Max length 1000 |
| sellerProductSortField | integer | No | 1 | Sort field: 1=total sales, 2=total GMV, 3=SPU avg price, 4=7-day sales, 5=7-day GMV |
| sortType | integer | No | 1 | Sort order: 0=ascending, 1=descending |
| pageNum | integer | No | 1 | Page number (starts at 1) |
| pageSize | integer | No | 50 | Page size — must be a multiple of 10, max 100 |

## 调用方式

- **API 端点**：`POST /echotik/listSellerProduct`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_list_seller_product.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-list-seller-product-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## Usage Examples

**1. List a store's top products by total sales**
```json
{
  "sellerId": "7495514739648989419",
  "sellerProductSortField": 1,
  "sortType": 1,
  "pageSize": 20,
  "pageNum": 1
}
```

**2. Rank a store's products by 7-day GMV (recent momentum)**
```json
{
  "sellerId": "7495514739648989419",
  "sellerProductSortField": 5,
  "sortType": 1
}
```

**3. Cheapest products in a store (price ascending)**
```json
{
  "sellerId": "7495514739648989419",
  "sellerProductSortField": 3,
  "sortType": 0
}
```

## Display Rules

1. **Present data clearly**: Show products in a table with key columns — product image, title, price, total sales, 30-day sales/GMV, rating, review count, and commission rate
2. **Sales & GMV granularity**: When relevant, show total sales and total GMV; mention multi-period breakdowns (1d/7d/15d/30d/60d/90d) are available in the saved JSON
3. **Commission formatting**: Display `productCommissionRate` as a percentage for readability (e.g. show 0.05 as "5%")
4. **Currency awareness**: Include the `currency` field when displaying prices and GMV
5. **Image reference**: When `imageUrl` is present, surface it so the user can visually compare products
6. **Result count**: Always inform the user of `total` records and the current page; suggest pagination or tighter sorting when the result set is large
7. **No secondary processing**: Results are live queries, not stored in a database; secondary SQL/data processing is not available

## Important Limitations

1. **sellerId required**: `sellerId` is mandatory; obtain it from the EchoTik TikTok Seller Search skill (`linkfox-echotik-list-seller`) or Seller Detail skill (`linkfox-echotik-seller-detail`), or a known store link/ID.
2. **Store-scoped only**: This lists one store's products; to discover/filter products across all TikTok Shop, use the EchoTik TikTok Product Search skill (`linkfox-echotik-list-product`).
3. **pageSize rule**: Must be a multiple of 10 (max 100). Other values may be rejected or adjusted.
4. **Listing date format**: `firstCrawlDt` uses `YYYYMMDD` integers (e.g. `20240504`).
5. **No region/keyword filter**: This tool only takes a `sellerId` and sort/pagination — it does not accept keyword, region, or category filters (the store's marketplace is inferred from the seller).
6. **Data real-time nature**: Results are live queries, not stored in a database; secondary SQL/data processing is not available.

## User Expression & Scenario Quick Reference

**Applicable** — See what a specific TikTok Shop store sells:

| User Says | Scenario |
|-----------|----------|
| "TikTok店铺商品" / "TikTok store products" | List a store's products by sellerId |
| "这个TikTok店铺在卖什么" | View a store's product catalog |
| "查看这家TikTok店铺的商品" | Deep-dive a store found via search/detail |
| "TikTok店铺销量最高的商品" | Sort store products by total sales |
| "TikTok店铺近期爆款" | Sort by 7-day sales/GMV |
| "这家店哪些商品佣金高" | Review commission rate per product |

**Not applicable** — Needs beyond one store's product list:

- Discovering/filtering products across all TikTok Shop (use EchoTik TikTok Product Search)
- Listing or filtering TikTok Shop stores (use EchoTik TikTok Seller Search)
- A single store's full profile (use EchoTik TikTok Seller Detail)
- TikTok creator/influencer or video analytics
- Amazon, Shopee, or other non-TikTok platform data

**Boundary judgment**: When users say "这个店铺卖什么" or "查看店铺商品" with a known store (sellerId or store link), this skill applies. If they want to search products across TikTok Shop by keyword/region/category, use the Product Search skill instead.

## 算力消耗规则

消耗 5 算力。

> 用户会因算力消耗而支付费用。请充分评估：当需要高频调用本技能，或用户对算力消耗量预期不足时，务必提醒用户，由用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.


---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
