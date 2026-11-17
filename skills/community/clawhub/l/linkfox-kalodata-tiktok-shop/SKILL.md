---
name: linkfox-kalodata-tiktok-shop
description: 通过kalodata数据搜索TikTok电商店铺排行榜并查询指定店铺的详细信息，支持按地区、货币、语言与日期范围查看高排名、高销量的TikTok Shop店铺（小店），并可用shopId获取销售额、销量、在售商品数、自营/分销/商城渠道收入及达人合作数。当用户提到TikTok店铺榜单、TikTok店铺排行、TikTok小店排行、TikTok热销店铺、TikTok店铺排名、TikTok Shop店铺榜、kalodata店铺搜索、kalodata店铺榜、TikTok店铺详情、TikTok小店资料、店铺销售额、店铺销量、TikTok shop ranking, TikTok shop leaderboard, TikTok top shops, TikTok store ranking, TikTok shop detail, TikTok store detail, kalodata shop search/detail时触发此技能。即使用户未明确提及"kalodata"，只要其需求涉及查看TikTok平台的店铺排行榜或某个TikTok店铺的详细数据，也应触发此技能。
---

# Kalodata - TikTok Shop Search & Detail

This skill supports a two-step TikTok shop workflow via the Kalodata data source:

1. Browse TikTok Shop store (店铺) leaderboards to discover high-performing stores.
2. Fetch one store's full detail by `shopId`.

Use the search (ranking) endpoint when the user wants rankings, store discovery, or store comparison. Use the detail endpoint when the user already has a `shopId` or has selected one store from a ranking result.

## Core Concepts

The shop ranking endpoint returns a paginated leaderboard filtered by `region`, `dateRange`, `language`, and `currency`. The default ranking order is by `revenue` (GMV) descending, and each row carries an explicit `rank` position. Each shop row includes identity, scale, revenue channel split, and growth.

The shop detail endpoint fetches **one** store by `shopId`. It returns the store's identity, scale, revenue channel split, and creator/video/live counts. The `shopId` usually comes from the ranking response field `shop_id`.

> ⚠️ **Field names differ between the shop RANK and shop DETAIL endpoints.** Detail uses `self_account_revenue` (rank uses `self_promotion_revenue`), `shoppingmall_revenue` with no internal underscore (rank uses `shopping_mall_revenue`), and `seller_type` (rank uses `shop_type`). Detail returns `creator_number`/`video_number`/`live_number`/`product_number` (rank does not), and does **not** return `rank`/`revenue_growth_rate`/`on_sell_product_count`. Always use the exact endpoint field names.

Both endpoints may reflect a statistical delay (T+1). See `references/api.md` for full request and response details.

## Data Fields

**Ranking rows** include:

| Field | Description |
|-------|-------------|
| rank | Rank position (1 = top by revenue) |
| shop_name | Shop display name |
| shop_id | Shop unique ID; pass this as `shopId` for detail lookup |
| shop_type | Shop type (e.g. `BRAND`) |
| revenue | Total GMV in the requested currency |
| sales_volumn | Sales volume; field is spelled `volumn` |
| on_sell_product_count | Number of products currently on sale |
| unit_price | Average unit price in the requested currency |
| revenue_growth_rate | Revenue growth rate (%), can be negative |
| self_promotion_revenue | Revenue from self-promotion (店铺自营/自播自推) |
| affiliate_revenue | Revenue from affiliate (达人分销) |
| shopping_mall_revenue | Revenue from the shopping mall (商城) |

**Detail rows** include:

| Field | Description |
|-------|-------------|
| shop_id | Shop unique ID (string to preserve precision) |
| shop_name | Shop display name |
| seller_type | Seller/shop type (e.g. `BRAND`) — note: `seller_type`, not `shop_type` |
| region | Market region (e.g. `US`) |
| revenue | Total revenue / GMV in the requested currency |
| sales_volumn | Sales volume; field is spelled `volumn` |
| product_number | Number of products on sale |
| unit_price | Average unit price in the requested currency |
| self_account_revenue | Revenue from self-account (店铺自营/自播自推) — note: `self_account_revenue`, not `self_promotion_revenue` |
| affiliate_revenue | Revenue from affiliate (达人分销) |
| shoppingmall_revenue | Revenue from the shopping mall (商城) — note: NO underscore between `shopping` and `mall` |
| creator_number | Number of creators cooperating with the shop (达人合作数) |
| video_number | Number of related videos |
| live_number | Number of related livestreams |

> **Revenue channel split**: on the rank endpoint `revenue` = `self_promotion_revenue` + `affiliate_revenue` + `shopping_mall_revenue`; on the detail endpoint `revenue` ≈ `self_account_revenue` + `affiliate_revenue` + `shoppingmall_revenue`. Components may round independently of `revenue` (e.g. `shoppingmall_revenue` returns `10431.0` on detail vs `10431.39` on rank), so treat the split as approximate, not an exact equality.

## Parameter Guide

**Shop ranking (`/kalodata/shop/rank`)**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| pageNumber | integer | No | Page number, 1-5 |
| pageSize | integer | No | Page size, 5-100 |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |
| category_ids | array<string> | No | Category ID list filter |
| revenue_range | string | No | Revenue / GMV range filter |
| shop_type | string | No | Shop type filter: `BRAND` or `RETAILER` |
| sortField | object | No | Sorting specification; pass `{}` for default revenue ranking |

**Shop detail (`/kalodata/shop/detail`)**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| shopId | string | Yes | Shop unique ID from ranking field `shop_id` |
| category_id | string | No | Optional category ID dimension |
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |

## 调用方式

- **API 端点**：`POST /kalodata/shop/rank` 或 `POST /kalodata/shop/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/kalodata_shop_search.py '<JSON 参数>' [--inline]` 或 `python scripts/kalodata_shop_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-kalodata-tiktok-shop-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 <= 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况

- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## Usage Examples

**1. Top TikTok shops in the US over the last 7 days**
```json
{"region":"US","dateRange":"last7Day","pageSize":10,"pageNumber":1}
```

**2. Fetch one shop's detail**
```json
{"shopId":"7495514739648989419","region":"US","dateRange":"last7Day","currency":"USD"}
```

**3. Discovery-to-detail workflow**
```text
Run kalodata_shop_search.py first, choose a row's shop_id, then pass that value as shopId to kalodata_shop_detail.py.
```

## Display Rules

1. Present ranking results in a table with rank, shop name, shop type, revenue, sales volume, product count, unit price, and growth rate.
2. Present detail results as one grouped profile: identity, scale, revenue channel split, and creator/video/live counts.
3. Always label `dateRange`, `region`, and `currency` when showing metrics.
4. Revenue channel breakdown is approximate (see Data Fields note); present the split as a breakdown, not an exact equality.
5. Use the exact field name `sales_volumn`. On detail use `shoppingmall_revenue` (no underscore) and `self_account_revenue`; on rank use `shopping_mall_revenue` and `self_promotion_revenue`. Do not mix the two endpoints' field names.
6. Show `creator_number`, `video_number`, `live_number`, `product_number` as plain integer counts.
7. Preserve ranking order unless the user explicitly requests a supported `sortField`.

## Important Limitations

- Ranking is not keyword search; it browses leaderboards by region and time window.
- Detail requires `shopId`; it cannot find a shop by name alone. Obtain `shopId` from the ranking `shop_id` field or the user.
- The ranking response does not include total/page count; paginate until a page returns fewer than `pageSize` items.
- `pageNumber` is limited to 1-5 and `pageSize` is limited to 5-100.
- Detail has no pagination; `data` is a 1-element array for a single shop, with no `total`.
- Field names differ between the rank and detail endpoints (see Data Fields) — use the exact names when extracting.
- Transient upstream errors may appear as `errcode 501` with a Kalodata HTTP 554 message. Retry the same parameters once or twice; do not change parameters automatically.
- Use the matching Kalodata product/video/creator/livestream skills for non-shop entities.

## User Expression & Scenario Quick Reference

**Applicable** -- TikTok Shop store ranking or single-store detail:

| User Says | Scenario |
|-----------|----------|
| "TikTok店铺排行榜", "TikTok小店排行" | Store ranking lookup |
| "TikTok热销店铺", "top TikTok shops" | Store leaderboard by region |
| "近7天TikTok店铺榜", "美国TikTok店铺排名" | Time-windowed / region-filtered ranking |
| "TikTok店铺详情", "TikTok小店资料" | Single-store detail lookup |
| "店铺销售额", "店铺销量", "店铺达人合作数" | Store revenue / sales / creator count |
| "kalodata shop search/detail" | Direct data source reference |

**Not applicable** -- Needs beyond TikTok Shop stores:

- TikTok creator/product/video/livestream rankings or details
- Amazon / Shopify / 1688 / other platforms' store data
- TikTok ad campaign management or content creation

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
