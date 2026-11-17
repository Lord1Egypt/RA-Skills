---
name: linkfox-echotik-list-seller
description: 搜索和分析TikTok Shop店铺（卖家）数据，按区域、类目、近30日GMV、销售趋势、上架时间、本土/跨境店铺等条件筛选店铺，返回销量、销售额(GMV)、粉丝数、评分、评价数、好评率、送达率、回复率、带货达人数、带货视频数、直播数、在店商品数等指标，覆盖16个TikTok Shop站点。当用户提到TikTok店铺搜索、TikTok卖家分析、TikTok Shop店铺排行、TikTok店铺销量、TikTok店铺GMV、TikTok带货店铺、EchoTik店铺数据、TikTok Shop seller search, TikTok shop list, TikTok seller analytics, EchoTik seller, TikTok store data时触发此技能。即使用户未明确提及"EchoTik"或"TikTok"，只要其需求涉及在TikTok Shop上按条件筛选或分析店铺/卖家表现指标，也应触发此技能。
---

# EchoTik TikTok Seller Search

This skill searches and analyzes TikTok Shop seller (store) data, helping cross-border sellers and marketers discover top-performing stores, benchmark competitors, and evaluate store-level performance across TikTok marketplaces.

## Core Concepts

EchoTik is a TikTok Shop analytics platform. This tool lists TikTok Shop stores (sellers) with rich filtering, returning store metrics: total sales, GMV (1d/7d/30d/90d), followers, rating, reviews, positive-feedback rate, delivery rate, response rate, number of promoting influencers, videos, livestreams, and product counts.

**Listing date**: `firstCrawlDt` / `minFirstCrawlDt` / `maxFirstCrawlDt` use a compact integer format `YYYYMMDD` (e.g., `20240101` for January 1, 2024).

**Pagination quirk**: `pageSize` must be a multiple of 10 (max 100). The official upstream API caps a single page at 10; this tool internally pulls multiple pages of 10 and merges them, so `pageSize=50` returns up to 50 merged sellers.

## Data Fields

| Field | Description |
|-------|-------------|
| sellerId | Store ID |
| sellerName | Store name |
| sellerLink | Store link |
| coverUrl | Store cover image URL |
| region | Marketplace code |
| totalSaleCnt | Total sales volume |
| totalSale1dCnt / 7dCnt / 30dCnt / 90dCnt | Sales volume (1d/7d/30d/90d, incremental) |
| totalSaleGmvAmt | Total GMV (revenue) |
| totalSaleGmv1dAmt / 7dAmt / 30dAmt / 90dAmt | GMV (1d/7d/30d/90d, incremental) |
| followersCount | Follower count |
| rating | Store rating |
| reviewCount | Review count |
| positiveFeedbackRate | Positive feedback rate |
| responseRate | Response rate |
| deliveryRate | Delivery rate |
| totalProductCnt | Historical product count (incl. delisted) |
| totalCrawlProductCnt | Current in-store product count |
| spuAvgPrice | Avg SKU price in store |
| minPrice / maxPrice | Min / max price |
| totalIflCnt | Number of promoting influencers |
| totalVideoCnt | Number of promo videos |
| totalLiveCnt | Number of livestreams |
| salesFlagText | Main sales channel (video/livestream) |
| salesTrendFlagText | Sales trend (flat/rising/falling) |
| shopIdentityLabel | Store identity label |
| shopTypeText | Brand store flag |
| fromFlagText | Local/cross-border flag |
| productCategoryList | Product categories |
| mostProductCategoryList | TOP1 product category |
| firstCrawlDt | Estimated listing time |
| userId | Influencer UID |

## Parameter Guide

### Required & Region

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| region | string | Yes | - | Marketplace code. See supported list below |

### Category Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| categoryId | string | Level-1 store category ID |
| categoryL2Id | string | Level-2 store category ID |
| categoryL3Id | string | Level-3 store category ID |

### GMV & Sales Trend

| Parameter | Type | Description |
|-----------|------|-------------|
| minTotalSaleGmv30dAmt / maxTotalSaleGmv30dAmt | number | 30-day GMV range |
| salesTrendFlag | integer | 7-day sales trend: 0=flat, 1=rising, 2=falling |

### Seller Type & Sales Channel

| Parameter | Type | Description |
|-----------|------|-------------|
| fromFlag | integer | Store origin: 1=local store, 2=cross-border store |
| salesFlag | integer | Main sales channel: 1=video, 2=livestream |

### Listing Date

| Parameter | Type | Description |
|-----------|------|-------------|
| minFirstCrawlDt / maxFirstCrawlDt | integer | Estimated listing date range (YYYYMMDD, e.g. 20240101) |

### Sorting & Pagination

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| sellerSortField | integer | 2 | Sort field: 1=total sales, 2=total GMV, 3=avg SKU price |
| sortType | integer | 1 | Sort order: 0=ascending, 1=descending |
| pageNum | integer | 1 | Page number (starts at 1) |
| pageSize | integer | 50 | Page size — must be a multiple of 10, max 100 |

### Supported Marketplaces

US (United States), ID (Indonesia), TH (Thailand), PH (Philippines), MY (Malaysia), VN (Vietnam), GB (United Kingdom), MX (Mexico), SG (Singapore), SA (Saudi Arabia), BR (Brazil), ES (Spain), JP (Japan), DE (Germany), IT (Italy), FR (France)

When the user doesn't specify a marketplace, ask or default to **US**.

## 调用方式

- **API 端点**：`POST /echotik/listSeller`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_list_seller.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-list-seller-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Top US stores by total GMV**
```json
{
  "region": "US",
  "sellerSortField": 2,
  "sortType": 1,
  "pageSize": 20,
  "pageNum": 1
}
```

**2. Rising cross-border stores in Southeast Asia**
```json
{
  "region": "ID",
  "fromFlag": 2,
  "salesTrendFlag": 1,
  "sellerSortField": 2,
  "sortType": 1
}
```

**3. High-GMV livestream-driven stores**
```json
{
  "region": "US",
  "salesFlag": 2,
  "minTotalSaleGmv30dAmt": 100000,
  "sellerSortField": 2,
  "sortType": 1
}
```

**4. Recently listed stores**
```json
{
  "region": "GB",
  "minFirstCrawlDt": 20250101,
  "sellerSortField": 1,
  "sortType": 1
}
```

## Display Rules

1. **Present data clearly**: Show results in a table with key columns — store name, region, total sales, 30-day GMV, followers, rating, review count, and number of promoting influencers
2. **GMV & sales granularity**: When relevant, show 30-day GMV and total sales; mention multi-period breakdowns (1d/7d/30d/90d) are available in the saved JSON
3. **Store link**: When `sellerLink` is present, surface it so the user can open the store
4. **Store attributes**: Show `fromFlagText` (local/cross-border), `salesFlagText` (video/livestream), and `salesTrendFlagText` (trend) to help benchmark competitors
5. **Result count**: Always inform the user of `total` records and the current page; suggest pagination or tighter filters when the result set is large
6. **No secondary processing**: Results are live queries, not stored in a database; secondary SQL/data processing is not available

## Important Limitations

1. **Region required**: `region` is mandatory; no default is applied by the API.
2. **pageSize rule**: Must be a multiple of 10 (max 100). Other values may be rejected or adjusted.
3. **Category IDs**: `categoryId` / `categoryL2Id` / `categoryL3Id` are internal IDs, not human-readable names — obtain them from prior results or the category taxonomy.
4. **Listing date format**: `minFirstCrawlDt` / `maxFirstCrawlDt` use `YYYYMMDD` integers (e.g. `20240101`).
5. **Data real-time nature**: Results are live queries, not stored in a database; secondary SQL/data processing is not available.
6. **Single-store detail**: For one store's full profile, use the store-detail skill with the `sellerId` returned here.

## User Expression & Scenario Quick Reference

**Applicable** — TikTok Shop store/seller discovery and benchmarking:

| User Says | Scenario |
|-----------|----------|
| "TikTok店铺排行" / "TikTok top stores" | List stores sorted by GMV/sales |
| "找TikTok带货店铺" | Filter by sales channel (video/livestream) |
| "TikTok本土店铺/跨境店铺分析" | Filter by fromFlag |
| "近期新开的TikTok店铺" | Filter by listing date |
| "TikTok销量上升的店铺" | Filter by salesTrendFlag=rising |
| "东南亚TikTok店铺" | Region-specific store listing |

**Not applicable** — Needs beyond store listing:

- Single product search or product rankings (use EchoTik product search/rank skills)
- TikTok creator/influencer analytics (follower counts, engagement of creators)
- TikTok video performance analytics (views, likes on specific videos)
- Amazon, Shopee, or other non-TikTok platform data
- Store-level operations: order/logistics/ads management

**Boundary judgment**: When users say "找店铺" or "竞品店铺", if the intent is to list and filter TikTok Shop stores by sales, GMV, or store attributes, this skill applies. If they want a single store's deep profile, use the store-detail skill with a known `sellerId`.

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
