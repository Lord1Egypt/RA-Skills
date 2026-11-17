---
name: linkfox-kalodata-tiktok-product
description: 通过kalodata数据查询TikTok电商商品排行榜并查询指定商品的详细数据，支持按地区、货币、语言与日期范围查看高排名/热销商品，并可用productId获取价格区间、销量、销售额、佣金率、上下架时间及所属店铺。当用户提到TikTok商品榜单、TikTok商品排行、TikTok热销榜、TikTok爆品排行、TikTok选品榜单、kalodata商品榜、TikTok商品详情、TikTok商品资料、商品价格、商品销量、TikTok product ranking, TikTok bestseller chart, TikTok top products, kalodata product rank, TikTok product detail, kalodata product detail, product analytics时触发此技能。即使用户未明确提及"kalodata"，只要其需求涉及查看TikTok平台的商品排行榜或某个TikTok商品的详细数据，也应触发此技能。
---

# Kalodata - TikTok Product Search & Detail

This skill supports a two-step TikTok Shop product workflow via the Kalodata data source:

1. Browse TikTok Shop product leaderboards to discover top-ranked and best-selling products.
2. Fetch one product's full detail by `productId`.

Use the ranking endpoint when the user wants best-seller rankings, hot products, or product discovery. Use the detail endpoint when the user already has a `productId` or has selected one product from a ranking result.

## Core Concepts

The product ranking endpoint returns a paginated leaderboard filtered by `region`, `dateRange`, `currency`, `language`, and optional `sortField`. Each product row includes identity, price, sales volume, revenue (split across video, live, and showcase channels), revenue growth rate, commission rate, and launch date. Results are paginated with `pageNumber` (1-5) and `pageSize` (5-100).

The product detail endpoint fetches **one** TikTok Shop product by `productId`. It returns the product's price range, sales, revenue (with channel split), commission rate, launch date, review count, category hierarchy, owning shop, and associated video/live/creator counts. The `productId` usually comes from the ranking response field `product_id`.

Both endpoints may reflect a statistical delay (T+1). See `references/api.md` for full request and response details.

## Data Fields

**Ranking rows** include:

| Field | Description |
|-------|-------------|
| product_id | Product unique ID; pass this as `productId` for detail lookup |
| product_name | Product title |
| unit_price | Price per unit (currency follows region, e.g. USD for US) |
| sales_volumn | Units sold (field is spelled `volumn`) |
| revenue | Total revenue / GMV; equals video + live + showcase revenue |
| video_revenue | Revenue from the video channel |
| live_revenue | Revenue from the live-stream channel |
| showcase_revenue | Revenue from the showcase / 橱窗 channel |
| revenue_growth_rate | Revenue growth rate (%) |
| commission_rate | Commission rate as a direct percentage (25.0 = 25%) |
| launch_date | Product launch date (YYYY-MM-DD) |

**Detail rows** additionally include:

| Field | Description |
|-------|-------------|
| product_region | Product market region (e.g. `us`) |
| product_shop_id | ID of the shop this product belongs to |
| pri_cate_id / sec_cate_id / ter_cate_id | Primary / secondary / tertiary category IDs |
| min_price / max_price | Minimum / maximum price in the requested currency |
| product_review_count | Number of product reviews |
| delivery_type | Delivery type (e.g. `local`) |
| video_number / live_number / creator_number | Associated video / live / creator counts |
| shopping_mall_revenue | Revenue from the shopping mall (商城) channel |

> Detail revenue channel split: `revenue` = `video_revenue` + `live_revenue` + `shopping_mall_revenue`.

## Parameter Guide

**Product ranking (`/kalodata/product/rank`)**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| region | string | No | TikTok Shop market region code, e.g. `US`. Default `US` when unspecified |
| dateRange | string | No | Relative time window, e.g. `last7Day`, `last30Day` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| category_ids | array<string> | No | Category ID list filter |
| shop_id | string | No | Shop ID filter |
| creator_id | string | No | Creator ID filter |
| video_id | string | No | Return products associated with the specified video |
| livestream_id | string | No | Return products associated with the specified livestream |
| revenue_range | string | No | Revenue / GMV range filter |
| is_affiliate | string | No | Affiliate filter: `PUBLIC_PLAN` or `NON_AFFILIATE` |
| commission_rate | number | No | Affiliate commission rate, e.g. `0.15` |
| is_tts_product | integer | No | Fully managed product filter: `1` or `0` |
| unit_price_range | string | No | Product unit-price range filter |
| sortField | object | No | Sorting specification; omit for default ranking |
| pageNumber | integer | No | Page number, 1-5 |
| pageSize | integer | No | Page size, 5-100 |

**Product detail (`/kalodata/product/detail`)**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| productId | string | Yes | TikTok product ID from ranking field `product_id` (string to preserve precision) |
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |

## 调用方式

- **API 端点**：`POST /kalodata/product/rank` 或 `POST /kalodata/product/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/kalodata_product_search.py '<JSON 参数>' [--inline]` 或 `python scripts/kalodata_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-kalodata-tiktok-product-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Browse top TikTok products in the US (last 7 days)**
```json
{"region":"US","dateRange":"last7Day","pageSize":20,"pageNumber":1,"currency":"USD"}
```

**2. Fetch one product's detail**
```json
{"productId":"1729508370969629931","region":"US","dateRange":"last7Day","currency":"USD"}
```

**3. Discovery-to-detail workflow**
```text
Run kalodata_product_search.py first, choose a row's product_id, then pass that value as productId to kalodata_product_detail.py.
```

## Display Rules

1. Present ranking results in a table with product name, product ID, price, sales volume, revenue (with channel split), growth rate, commission rate, and launch date.
2. Present detail results as one grouped profile: identity, price range, sales, revenue (channel split), commission, category hierarchy, owning shop, and associated video/live/creator counts.
3. Always label `dateRange`, `region`, and `currency` when showing monetary metrics.
4. Use the exact field name `sales_volumn`.
5. `commission_rate` is a direct percentage (25.0 = 25%), not basis points — show with a % sign.
6. `revenue_growth_rate` is a percentage — show with a % sign.
7. Revenue channel split: ranking `revenue` = `video_revenue` + `live_revenue` + `showcase_revenue`; detail `revenue` = `video_revenue` + `live_revenue` + `shopping_mall_revenue`. Present the split when useful.
8. Preserve ranking order unless the user explicitly requests a supported `sortField`.

## Important Limitations

- Ranking is not keyword search; it browses leaderboards by region and time window.
- Detail requires `productId`; it cannot find a product by name alone. Obtain `productId` from the ranking `product_id` first.
- The ranking response does not include `total` or page count; result count is `data.length`.
- `pageNumber` is limited to 1-5 and `pageSize` is limited to 5-100.
- A valid-but-empty request (e.g. an unsupported `region`) may return `errcode 200` with no `data` field and still be billed.
- Transient upstream errors may appear as `errcode 501` with a Kalodata HTTP 5xx message (e.g. 522/554). Retry the same parameters once or twice; do not change parameters automatically.
- Use the matching Kalodata video/creator/shop/livestream skills for non-product entities.

## User Expression & Scenario Quick Reference

**Applicable** -- TikTok product ranking or product detail lookup:

| User Says | Scenario |
|-----------|----------|
| "TikTok商品榜单", "TikTok商品排行" | Product ranking lookup |
| "TikTok热销榜", "TikTok爆品排行", "TikTok选品榜单" | Best-seller / hot product ranking |
| "kalodata商品榜", "kaloda排行" | Direct data source reference |
| "TikTok商品详情", "TikTok商品资料" | Single product detail lookup |
| "商品价格", "商品销量" | Product price / sales |
| "kalodata product rank/detail", "product analytics" | Direct product detail reference |

**Not applicable** -- Needs beyond TikTok products:

- TikTok video / creator / shop / livestream rankings or details
- Keyword-based product search
- Amazon / Shopify / 1688 product research (use the platform-specific skills)
- TikTok advertising / ad campaign management or content creation

## 算力消耗规则

每次调用消耗 7.0 算力。

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
