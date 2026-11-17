---
name: linkfox-shopee-product-detail
description: 查询单个 Shopee 公共商品详情。输入带有 -i.数字店铺ID.数字商品ID 的商品直链，支持新加坡、印度尼西亚、马来西亚、菲律宾、泰国、台湾、越南和巴西站点，返回来源当前可获取的价格、折扣、销量、库存、SKU 变体、图片、品牌、类目、店铺与评分等结构化数据。当用户提到 Shopee 商品详情、虾皮商品链接解析、价格库存核对、SKU 变体、竞品页面拆解、Shopee product details、Shopee listing lookup 时触发。即使用户未明确说“商品详情”，只要提供 Shopee 商品直链并希望读取当前公开页面数据，也应触发此技能。
---

# Shopee Product Detail Lookup

Fetch the current public detail of one Shopee product from a supported marketplace URL.

## Core Concepts

- **One product per call**: `productUrl` identifies one listing; this is not a keyword-search tool.
- **Market from URL**: the storefront, currency, and locale are inferred from the URL.
- **Direct-listing mode**: the tool auto-detects the supplied product URL and requests exactly one matching listing row.
- **Current snapshot**: available price, inventory, sales, rating, and shop values reflect the public page at request time.

## Data Fields

Each object in `data` can contain:

| Group | Representative fields |
|-------|------------------------|
| Identity | `itemId`, `shopId`, `url`, `name`, `brand`, `categoryId`, `categoryBreadcrumb` |
| Media | `image`, `images`, `videos` |
| Pricing | `price`, `priceBeforeDiscount`, `priceMin`, `priceMax`, `discountPercent`, `currency` |
| Demand | `sold`, `soldDisplayed`, `rating`, `ratingCount`, `ratingDistribution`, `likedCount` |
| Inventory | `stock`, `tierVariations`, `models` |
| Shop | `shopName`, `shopRating`, `shopLocation`, `isMall`, official and verification signals, nested `shop` data |
| Content | `description`, `attributes`, category data, availability and condition when supplied |

Less-common and newly introduced top-level fields are preserved in the returned product object. Fields may be absent or `null`.

## Parameter Guide

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| productUrl | Yes | - | Shopee HTTPS product URL whose path ends with `-i.<numeric shopId>.<numeric itemId>` |

Supported hosts: `shopee.sg`, `shopee.co.id`, `shopee.com.my`, `shopee.ph`, `shopee.co.th`, `shopee.tw`, `shopee.vn`, and `shopee.com.br`.

## 调用方式

- **API 端点**：`POST /shopee/product/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/shopee_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-shopee-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

- `LINKFOX_AGENT_API_KEY` 与 `LINKFOXAGENT_API_KEY` 均未配置。
- 响应状态为 401 或 402。
- 响应提示算力、余额、套餐或配额不足。

## Usage Example

```bash
python scripts/shopee_product_detail.py '{"productUrl":"https://shopee.sg/%28LENECT-OFFICIAL-STORE%29-Flash-I-Aurora-Dual-Highlighter-7.2g-COCOMO-i.9641401.29691169956"}'
```

## Display Rules

1. Lead with the listing name, item ID, shop, marketplace, current price, currency, stock, and public sold count.
2. Show current/original price and discount exactly as returned; do not convert currencies unless requested.
3. Present SKU models and per-variant stock in a compact table when available.
4. Render a small selection of images inline when useful instead of flooding the response.
5. Treat Shopee Mall, official-shop, and verified-seller flags independently.
6. State when descriptions, models, inventory, sold count, or other enrichment fields are unavailable.
7. Read exact large nested sections from the saved JSON only when the user needs them.

## Important Limitations

1. The URL must use a documented `-i.<shopId>.<itemId>` path; canonical `/product/<shopId>/<itemId>` URLs are not accepted by this tool.
2. Customer review rows are not returned. `ratingCount` and `ratingDistribution` are only aggregate signals when the source supplies them.
3. Public fields vary by market, listing state, seller, and source-page completeness. Indonesia, Singapore, Malaysia, Thailand, and the Philippines usually expose richer detail on the cloud source; Vietnam, Brazil, and Taiwan may return a lighter record.
4. `models` provides variant stock, while a separate price for every individual variant may be unavailable.
5. Invalid, removed, or market-mismatched listings return an error rather than a successful empty list.
6. This tool does not search Shopee, provide historical trends, or manage an authorized seller account.

## User Expression & Scenario Quick Reference

**Applicable** — one known Shopee listing:

| User Says | Scenario |
|-----------|----------|
| “查这个虾皮商品链接” | Listing detail lookup |
| “看一下价格、销量和库存” | Current listing audit |
| “提取变体、图片和品牌” | SKU and content extraction |
| “这个店铺是不是官方店？” | Public shop-signal check |

**Not applicable**:

- Keyword search, rankings, or bulk product screening
- Full customer-review collection or sentiment mining
- Historical price and inventory monitoring
- Authorized seller listing, order, promotion, or account operations

## 算力消耗规则

消耗 53 算力。

> 用户会因算力消耗而支付费用。重复查询不同商品会分别计费；继续调用前应让用户知晓额外消耗。

**Feedback:**

Auto-detect and report feedback via the Feedback API when the described capability differs from actual behavior, results miss the user's intent, the user expresses praise or dissatisfaction, or the skill can be improved. Follow `references/api.md` without interrupting the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
