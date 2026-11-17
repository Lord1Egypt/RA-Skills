---
name: linkfox-etsy-product-detail
description: 查询单个 Etsy Listing 的公共商品详情。输入 Etsy 商品直链，返回商品标题与描述、价格区间、币种、主图与图片集、变体、库存上限、类目、发货地与预计送达、店铺资料、评论数量、评分及买家反馈标签等数据。当用户提到 Etsy 商品详情、Etsy listing 解析、Etsy 商品链接查询、竞品 Listing 拆解、价格图片提取、店铺与评论概况、Etsy product details、Etsy listing lookup 时触发。即使用户未明确说“商品详情”，只要提供带数字 listing ID 的 Etsy 商品直链并希望读取当前公开商品页信息，也应触发此技能。
---

# Etsy Product Detail Lookup

Fetch the current public detail of one Etsy listing from its direct product URL for listing research and competitor-page audits.

## Core Concepts

- **Direct listing URL required**: use an Etsy HTTPS URL whose path is `/listing/<numeric-id>` or `/listing/<numeric-id>/<one-slug-segment>`, with an optional trailing slash and query string.
- **One listing per call**: this is a detail lookup, not Etsy keyword search or bulk screening.
- **Structured public-page data**: the response groups listing, price, media, shop, delivery, and review-summary fields.
- **Current snapshot**: values reflect what the public listing exposes when queried and may be absent or inconsistent.

## Data Fields

| Field | Description |
|-------|-------------|
| productId / productUrl | Etsy listing ID and canonical/product URL |
| title / description | Listing title and description sections |
| image / images | Primary image and full image list |
| price / lowPrice / highPrice / oldPrice | Current, range, and previous price strings when available |
| currency | Returned currency code |
| maxQuantity / variants | Reported maximum quantity and variation options |
| category | Etsy category breadcrumb |
| countryShippingFrom | Shipping origin country |
| deliveryDaysMin / deliveryDaysMax | Estimated delivery window; may be null or omitted |
| shopId / shopName / shopUrl / shopSales | Shop identity and public sales data |
| reviews / star / shopReviews | Listing review count, rating, and shop review count |
| highlightsTags / reviewsTags | Buyer-feedback highlights and tag frequencies |
| reviewsScores | Dynamic review-score breakdown; keys vary by listing |
| yearsOnEtsy | Public shop tenure |
| hasRatingsBadge / hasConvosBadge / hasShippingBadge | Public shop/listing badge flags |
| moreLikeUrl / searchPosition | Related-link or source-position fields when available |

The tool returns aggregate review signals, not individual review records.

## Parameter Guide

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| productUrl | Yes | - | Public HTTPS Etsy listing URL on `etsy.com` or a subdomain, without embedded credentials, using the default HTTPS port; the path is `/listing/<numeric-id>` with at most one slug segment, and an optional trailing slash/query string |

Search pages, shop pages, non-Etsy hosts, and listing URLs without a numeric listing ID are not valid inputs.

## 调用方式

- **API 端点**：`POST /etsy/product/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/etsy_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-etsy-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

### 异常情况

- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**。
- **响应提示算力或余额不足**：消息含“算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”或类似含义。

## Usage Examples

```bash
python scripts/etsy_product_detail.py '{"productUrl":"https://www.etsy.com/listing/1710567856/its-okay-to-make-some-mistakes-shirt"}'
```

## Display Rules

1. Lead with title, listing ID, shop name, category, price range, and currency.
2. Show the primary image inline and offer the remaining image count rather than rendering every image by default.
3. Present variants and quantity only when returned; an empty variants list is a valid result.
4. Keep listing reviews and shop reviews distinct, and label buyer-feedback tags as aggregate signals.
5. Show delivery estimates only when both source values are meaningful; preserve nulls as unavailable.
6. Do not normalize or convert price strings without an explicit user request.
7. Treat missing, empty, or implausible shop fields as extraction uncertainty; do not silently repair them.
8. For long descriptions and image arrays, summarize first and extract exact content from the saved JSON on demand.

## Important Limitations

1. Public Etsy page structure changes can cause fields to be absent, empty, or occasionally misidentified.
2. `star`, price fields, delivery estimates, shop metadata, and badges are not guaranteed for every listing.
3. The response includes review counts, tags, and aggregate scores, but not individual buyer reviews.
4. This tool does not provide historical prices, Etsy keyword rankings, or guaranteed sales estimates.
5. This tool does not search Etsy; use the Etsy product-query skill when the user needs keyword or multi-filter discovery.

## User Expression & Scenario Quick Reference

**Applicable** — one known Etsy listing URL:

| User Says | Scenario |
|-----------|----------|
| “查这个 Etsy 商品链接的详情” | Listing detail lookup |
| “提取这个 Etsy Listing 的标题、描述和图片” | Listing-content extraction |
| “看看它的价格区间、变体和发货信息” | Offer and delivery audit |
| “这个 Etsy 商品的店铺和评论概况如何？” | Shop and review-summary lookup |

**Not applicable**:

- Etsy keyword search, category discovery, or multi-product screening
- Etsy shop search/ranking without a specific listing URL
- Individual review retrieval or sentiment analysis from full review text
- Listing creation, editing, order management, or other seller-account operations

## 算力消耗规则

消耗 6 算力。

> 用户会因算力消耗而支付费用。重复查询其他 Listing 会分别计费；继续调用前应让用户知晓额外消耗。

**Feedback:**

Auto-detect and report feedback via the Feedback API when the described capability differs from actual behavior, results miss the user's intent, the user expresses praise or dissatisfaction, or the skill can be improved. Follow `references/api.md` without interrupting the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
