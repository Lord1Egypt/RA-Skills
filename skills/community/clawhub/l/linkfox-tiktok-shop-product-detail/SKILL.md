---
name: linkfox-tiktok-shop-product-detail
description: 查询 TikTok Shop 公共商品详情。输入完整商品 URL 或 19 位商品 ID，可指定美国、英国、东南亚及欧洲主要站点，返回商品标题、类目、价格、销量、SKU 库存、图片、店铺、评论概况、物流与促销等分组数据。当用户提到 TikTok Shop 商品详情、TikTok 商品链接解析、商品 ID 查询、价格库存核对、SKU 变体、竞品页面拆解、TikTok product details、TikTok Shop listing lookup 时触发。即使用户未明确说“商品详情”，只要希望根据一个 TikTok Shop 商品 URL 或 19 位商品 ID 读取当前公开商品页数据，也应触发此技能。
---

# TikTok Shop Product Detail Lookup

Fetch the current public detail of one TikTok Shop product by product URL or 19-digit product ID, with an optional marketplace region.

## Core Concepts

- **One product per call**: `productInput` identifies one product; this is not a search or ranking tool.
- **Marketplace context**: `region` selects the storefront context and defaults to `US`.
- **Readable grouped data**: the service returns a stable, readable set of product-detail groups.
- **Current snapshot**: values reflect what the public storefront exposes at request time, not historical analytics.

## Data Fields

Each object in `data` may contain these top-level groups:

| Field | Description |
|-------|-------------|
| productId | TikTok Shop product ID |
| status | Platform product status code; do not infer availability from this field alone |
| title | Product title |
| category | Category name and ID |
| pricing | Currency, sale price, original price, discount, and source pricing fields |
| sales | Public sold count and related sales display data |
| inventory | Total stock, SKUs, variant properties, prices, and default selection |
| media | Product image URLs and image metadata |
| seller | Seller ID, shop name, rating, location, and available shop data |
| reviews | Public review summary when available |
| shipping | Logistics and shipping modules when available |
| actions | Purchase-button and favorite-state data |
| additional | Other readable promotion, rights, review-entry, and product modules |

Nested fields vary by product and region. Preserve the returned values rather than inventing missing fields.

## Parameter Guide

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| productInput | Yes | - | TikTok HTTPS URL on `tiktok.com` or a subdomain, using the default HTTPS port and a path containing `product/<19-digit-id>`; or a 19-digit product ID passed as a string |
| region | No | `US` | Uppercase storefront code: `US`, `GB`, `ID`, `MY`, `TH`, `VN`, `PH`, `SG`, `DE`, `FR`, `IT`, or `ES` |

## 调用方式

- **API 端点**：`POST /tiktok/shop/product/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/tiktok_shop_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-tiktok-shop-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和积分问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

### 异常情况

- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**。
- **响应提示积分或余额不足**：消息含“积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”或类似含义。

## Usage Examples

**Product URL**

```bash
python scripts/tiktok_shop_product_detail.py '{"productInput":"https://shop.tiktok.com/view/product/1729937400435937604","region":"US"}'
```

**Product ID for the UK storefront**

```bash
python scripts/tiktok_shop_product_detail.py '{"productInput":"1729937400435937604","region":"GB"}'
```

## Display Rules

1. Lead with the product title, product ID, requested region, category, and returned status.
2. Show sale/original price with the returned currency; never convert currencies unless the user asks separately.
3. Present SKU variants, variant prices, and stock in a table when available.
4. Render product images inline when useful, but avoid flooding the response with every image.
5. Show seller, public sold count, review summary, and shipping information only when present.
6. Treat `status`, stock, and purchase-button data together; do not call a product “available” from one field alone.
7. Report missing, empty, or inconsistent fields as unavailable rather than estimating them.
8. For large nested sections, summarize first and read exact fields from the saved JSON only as needed.

## Important Limitations

1. Public fields can vary by product, seller, region, and storefront context.
2. URL inputs must include a `product/<19-digit-id>` path segment; use the 19-digit product ID directly when another TikTok URL format is unavailable.
3. A product may be removed, unavailable, or out of stock and still return structured metadata.
4. This tool does not provide historical price/stock trends, ranking lists, or guaranteed sales analytics.
5. This tool does not manage an authorized seller account or edit listings; use the TikTok Shop ERP product skill for seller operations.
6. The readable response can be large because SKU, media, shipping, and additional modules retain nested source fields.

## User Expression & Scenario Quick Reference

**Applicable** — one known TikTok Shop product:

| User Says | Scenario |
|-----------|----------|
| “查这个 TikTok Shop 链接的商品详情” | URL detail lookup |
| “这个 19 位 TikTok 商品 ID 卖什么？” | Product ID lookup |
| “看看这个商品的价格、SKU 和库存” | Current listing audit |
| “提取这个 TikTok 商品的图片和店铺信息” | Media and seller extraction |

**Not applicable**:

- TikTok product search, bestseller rankings, or multi-product screening
- Historical GMV, creator, livestream, or video-attribution analytics
- Authorized shop listing creation, editing, price changes, or stock changes
- TikTok video-page or creator-profile analysis

## 积分消耗规则

消耗 63 积分。

> 用户会因积分消耗而支付费用。重复查询不同地区或不同商品会分别计费；继续调用前应让用户知晓额外消耗。

**Feedback:**

Auto-detect and report feedback via the Feedback API when the described capability differs from actual behavior, results miss the user's intent, the user expresses praise or dissatisfaction, or the skill can be improved. Follow `references/api.md` without interrupting the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
