---
name: linkfox-mpstats-ozon-product-detail
description: MPSTATS Ozon 俄罗斯站单个 SKU 全量详情查询。传入一个 Ozon 商品 ID（productId），返回该 SKU 的价格、折扣、Ozon Card 价、评分、评论数、库存、销量、销售额、潜在销售额/损失销售额、上架日期、图片等完整商品卡。当用户提到 Ozon 商品详情、Ozon SKU 详情、Ozon 价格/评分/销量/库存核对、单个 Ozon SKU 查询、竞品 Ozon 基础数据拉取、Ozon 竞品卡片、MPSTATS Ozon detail, Ozon SKU detail, Ozon product card, single Ozon SKU lookup, Russian marketplace product detail 时触发此技能。即使用户未明确说"MPSTATS"，只要意图是按单个 Ozon SKU 拉取全量商品卡数据，也应触发此技能。
---

# MPSTATS Ozon Product Detail (Single SKU)

This skill fetches the full product card for one Ozon (Russia) SKU via MPSTATS. Returned fields include price, Ozon Card price, discount, rating, reviews, stock, monthly sales units, monthly sales revenue, lost profit, potential revenue, first listing date, image, and more.

## Core Concepts

**Single-SKU semantics**: Pass exactly one `productId` in a call. `productIds` arrays/lists are no longer accepted by this skill; for multiple SKUs, make separate calls only after confirming the extra credit cost with the user.

**Fulfillment model per SKU**: Each product card carries `deliveryScheme`:
- `FBO` — Fulfillment by Ozon (stock in Ozon warehouses)
- `FBS` — Fulfillment by Seller (seller-shipped)

Pass `includeFbs: true` to allow FBS SKUs and FBS-scoped metrics into the response; `false` (or omitted) keeps the result FBO-centric. This switch applies to the whole request.

**Previous-period comparison**: The card includes `previousSalesUnits` / `previousRevenue` — sales and revenue from the equal-length period immediately before `[startDate, endDate]` — ready for MoM / period-over-period diffs without extra calls.

**Revenue potential**: `revenuePotential` projects what the SKU could have earned if it had been in stock every day of the window; compare with `monthlySalesRevenue` to quantify stock-out drag, together with `lostProfit` / `lostProfitPercent`.

**Date window**: `startDate` / `endDate` define the period for all period-aggregated metrics. Latest selectable date is **yesterday** (T-1); today and future dates are rejected.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| productId | integer\|string | yes | Single Ozon SKU ID |
| startDate | string | no | Stats window start, `YYYY-MM-DD`; latest = yesterday |
| endDate | string | no | Stats window end, `YYYY-MM-DD`; latest = yesterday |
| includeFbs | boolean | no | `true` to include FBS data; `false` = FBO-only |

## 调用方式

- **API 端点**：`POST /mpstats/ozon/productDetail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/mpstats_ozon_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-mpstats-ozon-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Single-SKU detail**
```json
{"productId": 1786874757}
```

**2. Single-SKU lookup with period**
```json
{
  "productId": 1786874757,
  "startDate": "2025-03-01",
  "endDate": "2025-03-31",
  "includeFbs": true
}
```

**3. FBO-only snapshot**
```json
{"productId": 1786874757, "includeFbs": false}
```

**4. SKU discovered upstream — full card**
```json
{"productId": <productId from mpstats-ozon-product-search>}
```

## How to Chain with Other Ozon Skills

1. **Search → detail**: Use `mpstats-ozon-product-search` to resolve a keyword / brand / seller into candidate `productId`s, choose one SKU, then pass that `productId` here for full metrics.
2. **Detail vs trend**: This endpoint is a **period aggregate** per SKU; for day-by-day time-series on a single SKU, use `mpstats-ozon-product-trend`.
3. **Detail vs drill-downs**: When the input dimension is a brand / category / seller (not a single SKU), prefer `brand-products` / `category-products` / `seller-products` — they already return aggregated metrics per SKU under that dimension.

## Display Rules

1. **Compact table** — lead with `productId`, `title`, `price`, `monthlySalesUnits`, `monthlySalesRevenue`, `rating`, `reviewCount`, `balance`, `deliveryScheme`, `firstDate`. Pull `revenuePotential` / `lostProfit` / `lostProfitPercent` in when the user asks about stock-out impact.
2. **Currency** — Ozon native currency is **RUB**; the `currency` field carries the symbol. Do not silently relabel.
3. **Failure handling** — the response carries `successCount` / `failedCount` / `failures`; when `failedCount > 0`, list the failed `productId` from `failures` to the user rather than silently dropping it.
4. **Period-over-period** — when both current and `previous*` fields are present, render them side-by-side or as diff; don't report a single-period number as "trend".
5. **With-stock vs all-days** — `salesPerDayWithStock` / `dailySalesRevenueWithStock` only count days that had inventory; distinguish from the plain `salesPerDay` / `dailySalesRevenue`.
6. **Delivery model** — prefer the per-SKU `deliveryScheme` value over assuming FBO.
7. **No business advice** — present data; do not extrapolate "this SKU is worth selling" without a wider analysis.

## Important Limitations

- **Single-SKU input only** — pass `productId`, not `productIds`; arrays/lists are invalid. For multiple SKUs, call once per SKU only after confirming the added credit cost.
- **Ozon-only** — this tool does not cover Wildberries or other Russian marketplaces.
- **T-1 data** — `endDate` must not be today or future.
- **FBS coverage** — some categories have partial FBS coverage; if the input set is FBS-heavy, expect sparser cards.
- **Field set differs from brand/seller** — this endpoint does **not** return `brandId`, `country`, `category`, `minPrice` / `maxPrice` / `averagePrice`, `balanceFbs`, `frozenStocks`, `warehousesCount`, `daysInSite` / `daysInStock` / `turnoverDays`, `position` / `categoryPosition` / `revenueSharePercent`, `isFbs`. Use `brand-products` / `category-products` / `seller-products` if those are needed.
- **No translation** — titles are returned in Russian; translate on demand when presenting to Chinese / English users.

## User Expression & Scenario Quick Reference

**Applicable** — Per-SKU Ozon card lookup:

| User Says | Scenario |
|-----------|----------|
| "Pull Ozon details for this SKU" | Single card fetch |
| "What's the price / rating / stock of Ozon SKU 1786874757" | Single-SKU card |
| "Competitor's Ozon listing, give me sales & rating" | Competitor card audit |
| "Compare FBO vs FBO+FBS metrics for this SKU" | Fulfillment-model comparison |

**Not applicable** — Needs beyond per-SKU card:

- Keyword-based discovery → use `mpstats-ozon-product-search`
- Day-by-day time-series for one SKU → use `mpstats-ozon-product-trend`
- Listing copy / reviews / images analysis beyond URL → out of scope
- Brand / category / seller drill-down with filters → use the matching drill-down skill

**Boundary judgment**: If the user already has a single **SKU** and wants sales / price / stock / rating, this is the skill. If they provide multiple SKUs, process them one at a time only after confirming the added credit cost. If they don't yet have SKUs, route through the search or drill-down skills first.

## 算力消耗规则

按动态规则计费：消耗算力 = 12。`productId` 为空返回 0

> **重要**：本技能的服务按倍数动态计算，可能一次性消耗大量算力，必须提醒用户，由用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
