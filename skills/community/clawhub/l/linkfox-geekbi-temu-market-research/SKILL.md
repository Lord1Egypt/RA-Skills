---
name: linkfox-geekbi-temu-market-research
description: 使用 GeekBI 分析 Temu 公开市场的类目机会与搜索关键词需求，支持按蓝海指数、累计销量、累计销售额、价格、商品数和店铺数筛选，并分析日/周/月趋势。当用户提到 Temu 类目市场、类目机会、搜索词、蓝海词、需求趋势、Temu category research、keyword research 或 demand research 时触发。仅查询 Temu 类目 ID、catId 或类目树时使用 linkfox-temu-category-search。本 skill 不用于商品详情、店铺明细或评论分析。
---

# Temu Category & Keyword Demand Research

This skill researches Temu category opportunities and buyer-demand keywords from public marketplace data. Use only the endpoints needed for the user's request, and read `references/api.md` for the full request and response contract.

The site-list and category-list endpoints are helper capabilities. A helper-only request must not auto-select this skill unless the user explicitly invokes it or the skill is already active.

## Core Concepts

- `regionId` selects the marketplace. Resolve it from a non-null positive `sites[].regionId`; never substitute `siteId`. The gateway default is `regionId: 211` (United States).
- `dsr` is a supply-demand signal, not a standalone go/no-go score. Cross-check demand scale, recent growth, item/shop supply, and price.
- Search responses are paginated `items[]`. Defaults are `page: 1` and `size: 20`; `size` is 1–200 and `page * size` must not exceed 10,000. `order` has no gateway default; when supplied, it must be `asc` or `desc` (case-insensitive).
- Range filters are limited to `dsr`, `totalSold`, `avgPrice`, `totalSales`, `itemCount`, and `mallCount`, each with `Min` / `Max`. Never make a minimum greater than its maximum; all except `dsr` must be non-negative.
- Use site/category helpers only when the user has not supplied a valid ID. Stop if no unambiguous ID is returned.
- Do not launch a paid search merely to answer a site-list or category-tree request.

| Intent | Endpoint | Script |
|---|---|---|
| Compare category demand and competition | `/geekbi/temu/categorySearch` | `geekbi_temu_category_search.py` |
| Discover and compare buyer-demand keywords | `/geekbi/temu/keywordSearch` | `geekbi_temu_keyword_search.py` |
| Resolve Temu marketplaces | `/geekbi/temu/siteList` | `geekbi_temu_site_list.py` |
| Browse the category tree | `/geekbi/temu/categoryList` | `geekbi_temu_category_list.py` |

## Endpoint: `/geekbi/temu/categorySearch`

### Request

- Category research uses `keyword` to compare market capacity and competition. Use the separate category-list helper with `parentCatId` when a trusted category tree must be traversed; `categorySearch` itself does not accept `catLevel` or `parentCatId`.
- Use `keyword` for a Chinese or English category name. `catLevel` and `parentCatId` are response/helper concepts, not `categorySearch` request fields.
- Filter or rank broad demand with `totalSold`; use `dsr` for candidate discovery. Treat `monthSoldRate` and `monthSalesRate` as response fields for recent-growth analysis, not as range-filter request fields.
- `itemCount` and `mallCount` can be filtered with Min/Max fields. Period `*ItemCount` and `*MallCount` values are response-only changes and can be negative.

```bash
# Compare US pet-related categories by cumulative demand
python scripts/geekbi_temu_category_search.py '{"regionId":211,"keyword":"宠物","totalSoldMin":1000,"sort":"totalSold","order":"desc","page":1,"size":20}'
```

### Response

| Path | Meaning |
|---|---|
| `items[].catId` / `items[].parentCatItems[]` | Category identity and verified hierarchy |
| `items[].totalSold` / `totalSales` / `avgPrice` | Cumulative demand, revenue, and average price |
| `items[].itemCount` / `mallCount` | Product and shop supply |
| `items[].semiManagedItemCount` / `semiManagedMallCount` | Semi-managed supply counts |
| `items[].day*` / `week*` / `month*` | Period demand, supply changes, and growth rates |
| `errcode` / `errmsg` | Gateway business status; verified success is `200` / `ok` |

## Endpoint: `/geekbi/temu/keywordSearch`

### Request

- Keyword research uses `keyword` for a specific phrase or `catIds` for category-led discovery. Combine them only when the user explicitly wants a phrase within a category.
- Resolve `catIds` from valid `categories[].catId` values or a verified category-search result. Prefer level-1 or level-2 IDs for broad discovery.
- Search a supplied phrase with `keyword` without silently translating or replacing it.
- For category-led discovery, use `catIds` from the category helper. Multiple IDs match any supplied category.
- Rank hot terms with `totalSold` and blue-ocean candidates with `dsr`. Analyze recent demand from returned `monthSoldRate` or `monthSalesRate`; these period metrics are not range-filter request fields. Use `firstOnSaleTimeMin/Max` for market recency.
- `firstOnSaleTimeMin/Max` use ISO-8601 timestamps and describe the earliest associated product listing time.

```bash
# Discover dress-related demand terms within a verified category
python scripts/geekbi_temu_keyword_search.py '{"regionId":211,"keyword":"dress","catIds":[27011],"totalSoldMin":1000,"sort":"totalSold","order":"desc","page":1,"size":20}'
```

### Response

| Path | Meaning |
|---|---|
| `items[].keyword` / `items[].cnKeyword` | Search phrase and optional Chinese form |
| `items[].catIds` / `items[].catItems[]` | Categories associated with a keyword |
| `items[].totalSold` / `totalSales` / `avgPrice` | Cumulative demand, revenue, and average price |
| `items[].itemCount` / `mallCount` | Product and shop supply |
| `items[].semiManagedItemCount` / `semiManagedMallCount` | Semi-managed supply counts |
| `items[].day*` / `week*` / `month*` | Period demand, supply changes, and growth rates |
| `items[].firstOnSaleTime` | Earliest associated product listing time; not keyword creation time |
| `errcode` / `errmsg` | Gateway business status; verified success is `200` / `ok` |

## Endpoint: `/geekbi/temu/siteList`

### Request

```bash
# Resolve a non-US marketplace; use regionId, not siteId
python scripts/geekbi_temu_site_list.py '{}'
```

### Response

| Path | Meaning |
|---|---|
| `sites[].regionId` | IDs accepted by the research endpoints |
| `errcode` / `errmsg` | Gateway business status; verified success is `200` / `ok` |

## Endpoint: `/geekbi/temu/categoryList`

### Request

```bash
# Resolve a trusted category path when only a category name is known
python scripts/geekbi_temu_category_list.py '{}'
python scripts/geekbi_temu_category_list.py '{"parentCatId":27011}'
```

### Response

| Path | Meaning |
|---|---|
| `categories[].catId` | IDs accepted by the research endpoints |
| `errcode` / `errmsg` | Gateway business status; verified success is `200` / `ok` |

Fields can be absent or `null`. Preserve runtime JSON types and raw rate values; do not replace missing values with zero.

## 调用方式

- **API 端点**：`POST /geekbi/temu/categorySearch`、`POST /geekbi/temu/keywordSearch`、`POST /geekbi/temu/siteList` 或 `POST /geekbi/temu/categoryList`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/geekbi_temu_category_search.py '<JSON 参数>' [--inline]`、`python scripts/geekbi_temu_keyword_search.py '<JSON 参数>' [--inline]`、`python scripts/geekbi_temu_site_list.py '{}' [--inline]` 或 `python scripts/geekbi_temu_category_list.py '<JSON 参数>' [--inline]`
- **成本约束**：类目搜索和关键词搜索各消耗 15 算力/次，站点列表和品类列表不消耗算力；同一端点同一参数组合使用 24h 本地缓存，同一会话默认只调用一次。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制真实请求，付费端点可能再次扣算力，免费辅助端点仅强制刷新。失败、空结果或瞬时错误不得自动重试，也不得自动换关键词、翻页、改站点或筛选条件连续试探；需要继续付费检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-geekbi-temu-market-research-<timestamp>.json`；`<cwd>` 为脚本执行时的当前工作目录，`<session>` 取自环境变量 `SESSION_ID`，未设置时自动生成。当前目录不可写时直接报错，不回退到用户目录或系统临时目录。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层状态字段、常见业务计数、忽略 `columns` 后最大业务列表的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

### 异常情况

- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY` 或兼容键 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**。
- **响应提示算力或余额不足**：消息含“算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”或类似含义。

## Display Rules

1. State marketplace name, `regionId`, currency, filters, sort, page, and page size.
2. For categories, show the full category path, `catId`, level, demand/revenue, average price, item/shop supply, semi-managed supply, and relevant growth fields.
3. For keywords, show the phrase, associated category path/IDs, demand/revenue, average price, item/shop supply, semi-managed supply, earliest listing time, and relevant growth fields.
4. Label monetary values with the selected site's currency. Keep raw rate units explicit and do not silently convert them.
5. Mark incomplete pagination as a sample. Keep IDs available for downstream product, shop, or keyword research.
6. Preserve `null`, missing fields, and upstream extensions rather than inventing values.

## Important Limitations

- This skill researches public Temu market data; it does not access or operate a seller account.
- `total` can be capped at 10,000. A partial page or uncompleted pagination is not the entire marketplace.
- `dsr`, growth, sales, or supply alone cannot prove an opportunity or predict future performance.
- `firstOnSaleTime` is the earliest associated product listing time, not keyword creation time.
- The category tree can require several `parentCatId` calls; do not guess intermediate IDs.
- Do not automatically call helpers when valid IDs are already available.
- Do not retry paid endpoints with changed filters or another page after empty results without user confirmation.

## User Expression & Scenario Quick Reference

**Applicable**: “查 Temu 美国站宠物类目机会”, “找月需求增长的蓝海类目”, “挖 Temu 连衣裙热搜词”, “比较关键词供需和价格带”, “Temu category/keyword demand research”.

**Adjacent**: Resolve an unknown non-US marketplace before research. For category-led keyword discovery, resolve a trusted `catId` from the category tree or a verified category result.

**Not an automatic trigger**: A request solely to enumerate Temu sites, `regionId` values, category-tree nodes, or `catId` values does not auto-trigger this skill. Route category-tree/`catId`-only requests to `linkfox-temu-category-search`. If this GeekBI skill was explicitly invoked or is already active, its site/category helpers may be called independently.

**Not applicable**: Temu product detail, shop-only benchmarking, review analysis, seller-center operations, listing changes, fulfillment, advertising, or research on another marketplace.

## 算力消耗规则

类目搜索和关键词搜索每次各消耗 15 算力；站点列表和品类列表不消耗算力。

> 用户会为类目搜索和关键词搜索支付算力。高频调用、翻页或改条件重搜前，必须让用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
