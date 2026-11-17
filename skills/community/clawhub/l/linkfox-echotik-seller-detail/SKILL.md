---
name: linkfox-echotik-seller-detail
description: 查询TikTok Shop店铺（卖家）详情，通过sellerId获取单个店铺的完整档案，返回总销量、多周期(1天/7天/30天/90天)销量与销售额(GMV)、粉丝数、评分、评价数、好评率、送达率、回复率、在店商品数、带货达人数、带货视频数、直播数、价格区间、商品分类、预估上架时间等指标。当用户提到TikTok店铺详情、TikTok卖家详情、TikTok店铺分析、TikTok店铺数据、TikTok店铺档案、TikTok Shop store detail、TikTok seller detail、EchoTik store profile时触发此技能。即使用户未明确提及"EchoTik"或"TikTok"，只要其需求涉及查询某个TikTok Shop店铺的完整详情/档案（已知sellerId），也应触发此技能。
---

# EchoTik TikTok Seller Detail

This skill fetches the full profile of a single TikTok Shop store (seller) by its `sellerId`, helping cross-border sellers and marketers deep-dive one store's performance — sales, multi-period GMV, followers, ratings, fulfillment, and influencer/video/livestream reach.

## Core Concepts

EchoTik is a TikTok Shop analytics platform. This tool returns one store's complete detail object: total and incremental (1d/7d/30d/90d) sales volume and GMV, followers, rating, reviews, positive-feedback / response / delivery rates, product counts, price range, categories, and promoting-influencer / video / livestream counts.

**Where to get a `sellerId`**: This skill requires a store's `sellerId`. Obtain it from the **EchoTik TikTok Seller Search** skill (`linkfox-echotik-list-seller`), which lists and filters TikTok Shop stores by region, category, GMV, trend, and store type.

**Listing date**: `firstCrawlDt` uses a compact integer format `YYYYMMDD` (e.g. `20240504` for May 4, 2024).

## Data Fields

The response is a flat store object (top level also carries `errcode`, `errmsg`, `costToken`, `columns`, `type`).

| Field | Description |
|-------|-------------|
| sellerId | Store ID |
| sellerName | Store name |
| sellerLink | Store link |
| coverUrl | Store cover image URL |
| region | Marketplace code |
| categoryId / categoryL2Id / categoryL3Id | Level-1 / 2 / 3 category ID |
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
| salesFlagText | Main sales channel (视频带货 / 直播带货) |
| salesTrendFlagText | Sales trend (上升 / 下降 / 平稳) |
| shopIdentityLabel | Store identity label (e.g. OFFICIAL SHOP) |
| shopTypeText | Brand store flag (是 / 否) |
| fromFlagText | Local/cross-border flag (本土 / 跨境) |
| productCategoryList | Product categories (JSON string) |
| mostProductCategoryList | TOP1 product category (JSON string) |
| firstCrawlDt | Estimated listing time (YYYYMMDD) |
| userId | Influencer UID |
| sourceType | Source type (e.g. Tiktok) |
| sourceTool | Source tool |
| costToken | Tokens consumed |
| columns | Render column definitions (display metadata) |
| type | Render style (e.g. tableListWorkbenches) |

## Parameter Guide

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| sellerId | string | Yes | - | TikTok Shop store ID. Obtain it from the Seller Search skill's results. Max length 1000 |

## 调用方式

- **API 端点**：`POST /echotik/sellerDetail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_seller_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-seller-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Fetch a store's full profile**
```json
{
  "sellerId": "7495514739648989419"
}
```

**2. Deep-dive a store found via Seller Search**
```
先用店铺搜索列出美国GMV前列店铺，再查看其中 medicube US Store（sellerId 7495514739648989419）的完整详情
```

## Display Rules

1. **Present a clear store profile**: Show store name, region, seller link, cover image, and identity label (e.g. OFFICIAL SHOP)
2. **Sales & GMV granularity**: Show total sales and total GMV; surface the multi-period breakdown (1d/7d/30d/90d) for both volume and GMV so the user sees momentum
3. **Store health metrics**: Show followers, rating, review count, positive-feedback rate, response rate, and delivery rate together
4. **Store attributes**: Show `fromFlagText` (本土/跨境), `salesFlagText` (视频/直播带货), `salesTrendFlagText` (trend), and `shopTypeText` (brand store) for benchmarking
5. **Reach metrics**: Surface `totalIflCnt` (influencers), `totalVideoCnt` (videos), `totalLiveCnt` (livestreams), and product counts
6. **Store link**: When `sellerLink` is present, surface it so the user can open the store
7. **No secondary processing**: Results are live queries, not stored in a database; secondary SQL/data processing is not available

## Important Limitations

1. **sellerId required**: `sellerId` is mandatory; obtain it from the EchoTik TikTok Seller Search skill (`linkfox-echotik-list-seller`) or a known store link/ID
2. **Single store only**: This returns one store's detail; to list and filter stores, use the Seller Search skill
3. **Listing date format**: `firstCrawlDt` uses `YYYYMMDD` integers (e.g. `20240504`)
4. **Category IDs**: `categoryId` / `categoryL2Id` / `categoryL3Id` are internal IDs, not human-readable names
5. **Data real-time nature**: Results are live queries, not stored in a database; secondary SQL/data processing is not available

## User Expression & Scenario Quick Reference

**Applicable** — Deep-dive one TikTok Shop store's full profile:

| User Says | Scenario |
|-----------|----------|
| "TikTok店铺详情" / "TikTok store detail" | Fetch one store's full profile by sellerId |
| "查看这个TikTok店铺的数据" | Deep-dive a store found via search |
| "分析medicube这家TikTok店" | Single-store performance analysis |
| "这个TikTok店铺的GMV和粉丝数" | Store-level sales/GMV/follower metrics |

**Not applicable** — Needs beyond a single store detail:

- Listing or filtering TikTok Shop stores by region/GMV/trend (use EchoTik TikTok Seller Search)
- TikTok product search or product rankings (use EchoTik product search/rank skills)
- TikTok creator/influencer analytics (follower counts, engagement of creators)
- TikTok video performance analytics (views, likes on specific videos)
- Amazon, Shopee, or other non-TikTok platform data
- Store-level operations: order/logistics/ads management

**Boundary judgment**: When users say "分析这家店铺" or "查看店铺详情" with a known store (sellerId or store link), this skill applies. If they want to discover or list stores by criteria, use the Seller Search skill instead.

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
