---
name: linkfox-geekbi-temu-shop
description: 使用 GeekBI 查询和筛选 Temu 公开市场店铺。用户显式提到 GeekBI、linkfox-geekbi-temu-shop，或需要平均客单价、动销、粉丝数、商品数、销量或销售额的日/周/月变化与增长等 GeekBI 差异指标时触发。普通 Temu 店铺搜索或排行使用 linkfox-temu-store-query；除非用户明确要求跨数据源对比，不要同时调用两条付费店铺数据 skill。
---

# Temu Shop Discovery & Benchmarking

This skill searches public Temu marketplace shops for competitor discovery and store-level benchmarking. Use only the endpoints needed for the user's request, and read `references/api.md` for the complete request and response contract.

The site-list and category-list endpoints are helper capabilities for shop search. A request solely for site or category metadata must not auto-select this skill. If the user explicitly invokes this skill, or the skill is already active, either helper may be called independently.

## Endpoints

### `/geekbi/temu/mallSearch`

| Intent | Endpoint | Script |
|---|---|---|
| Discover and benchmark shops | `/geekbi/temu/mallSearch` | `geekbi_temu_mall_search.py` |

#### Request

- `regionId` selects the marketplace. Resolve it from a non-null positive `sites[].regionId`; never substitute `siteId`.
- `catIds` is an integer array of shop category IDs. Populate it only from valid `categories[].catId` values.
- Shop search returns paginated `items[]`. The default marketplace is `regionId: 211` (United States), with `page: 1` and `size: 20`.
- `regionId`, `page`, and `size` select the marketplace and page. `size` is 1–200 and `page * size` must not exceed 10,000.
- `keyword` matches the shop name. `catIds` is an integer array, not a comma-separated string.
- Range filters use paired `*Min` / `*Max` fields for `mallSold`, `mallSales`, `mallStar`, `reviewNum`, `goodsNum`, `followerNum`, and `avgPrice`. Never make a minimum greater than its maximum.
- `mallStarMin/Max` must remain within 0–5. `hostingMode` is `1` (full-managed) or `2` (semi-managed).
- `mallOpenTimeMin/Max` use ISO-8601 date-time strings. If both are supplied, both must parse and the minimum must not exceed the maximum.
- `order` is `asc` or `desc`. Use a `sort` field only after the API or an established workflow confirms it.

#### Response

| Path | Meaning |
|---|---|
| `items[].mallId` / `items[].mallName` | Shop identity |
| `items[].mallSold` / `items[].mallSales` | Historical cumulative unit sales and revenue |
| `items[].mallStar` / `items[].reviewNum` | Shop rating and historical review count |
| `items[].goodsNum` / `items[].followerNum` | Active product count and follower count |
| `items[].avgPrice` | Average order value in the selected site's currency |
| `items[].catIds` / `items[].catItems` | Main category IDs and category paths |
| `items[].day*` / `week*` / `month*` | Returned period metrics and growth rates |

### `/geekbi/temu/siteList`

| Intent | Endpoint | Script |
|---|---|---|
| Resolve Temu marketplaces | `/geekbi/temu/siteList` | `geekbi_temu_site_list.py` |

#### Request

- Site list takes `{}`. Reuse only a non-null positive `sites[].regionId`, never `siteId`.

#### Response

| Path | Meaning |
|---|---|
| `sites[].regionId` | Marketplace ID accepted by shop search |
| `sites[].siteId` | Upstream internal ID; do not use as the marketplace selector |

### `/geekbi/temu/categoryList`

| Intent | Endpoint | Script |
|---|---|---|
| Browse the category tree | `/geekbi/temu/categoryList` | `geekbi_temu_category_list.py` |

#### Request

- `parentCatId` drills into the category tree. Omit it for top-level categories, then reuse a returned `catId` to fetch children.
- Category list takes `{}` for top-level categories or `{"parentCatId": <catId>}` for children. Reuse only a non-null valid `catId`.

#### Response

| Path | Meaning |
|---|---|
| `categories[].catId` | Category ID accepted in `catIds` or as the next `parentCatId` |

## Shared Workflow Rules

- Use site/category helpers only when the user has not already supplied a valid ID. Do not run a paid search merely to answer a helper-only request.
- Stop and explain when no valid helper ID is returned; do not guess an ID or launch the shop search with a mismatched site/category.

| Path | Meaning |
|---|---|
| `errcode` / `errmsg` | Gateway business status; verified success is `200` / `ok` |

Business fields may be absent or `null`. Preserve the runtime JSON type and do not replace missing values with zero.

## 调用方式

- **API 端点**：`POST /geekbi/temu/mallSearch`、`POST /geekbi/temu/siteList` 或 `POST /geekbi/temu/categoryList`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/geekbi_temu_mall_search.py '<JSON 参数>' [--inline]`、`python scripts/geekbi_temu_site_list.py '{}' [--inline]` 或 `python scripts/geekbi_temu_category_list.py '<JSON 参数>' [--inline]`
- **成本约束**：店铺搜索消耗 15 算力/次，站点/品类列表不消耗算力；同一端点同一参数组合使用 24h 本地缓存，同一会话默认只调用一次。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制真实请求，付费端点可能再次扣算力，免费辅助端点仅强制刷新。失败、空结果或瞬时错误不得自动重试，也不得自动换关键词、翻页、改站点或筛选条件连续试探；需要继续付费检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-geekbi-temu-shop-<timestamp>.json`；`<cwd>` 为脚本执行时的当前工作目录，`<session>` 取自环境变量 `SESSION_ID`，未设置时自动生成。当前目录不可写时直接报错，不回退到用户目录或系统临时目录。
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

## Usage Examples

```bash
# Resolve regionId (use sites[].regionId, not siteId)
python scripts/geekbi_temu_site_list.py '{}'

# Browse top-level categories, then fetch one node's children
python scripts/geekbi_temu_category_list.py '{}'
python scripts/geekbi_temu_category_list.py '{"parentCatId":1}'

# Verified non-empty US shop search
python scripts/geekbi_temu_mall_search.py '{"regionId":211,"page":1,"size":3,"mallStarMin":4}'
```

## Display Rules

1. State the selected marketplace (`regionId`, site name, and currency when available), filters, current page, and page size.
2. Present shop name, `mallId`, rating, historical sales and revenue, average order value, followers, active products, hosting mode, categories, and opening time when returned.
3. Label monetary values with the selected site's currency. Do not assume USD merely because the default marketplace is the United States.
4. Keep category IDs and shop IDs available for follow-up work, but do not expose `siteId` as a marketplace selector.
5. Treat rate fields as percentages only where the response contract identifies them as rates; do not silently convert units.
6. Preserve `null`, missing fields, and `extraFields` rather than inventing values.

## Important Limitations

- This skill researches public Temu market data; it does not access or operate a seller account.
- Search can access only the first 10,000 matching records, with `size` from 1 to 200.
- The API does not publish an exhaustive sort-field enum. Do not improvise unsupported sort names.
- Category-name resolution may require multiple category-list calls from the top level down.
- A shop row is a current upstream snapshot; do not infer causality or future performance from one page alone.
- Do not automatically call helper endpoints when the user already supplied valid IDs.
- Do not retry a paid endpoint with changed filters after an empty result without user confirmation.

## User Expression & Scenario Quick Reference

**Applicable**: “用 GeekBI 查 Temu 店铺”, “比较 Temu 店铺平均客单价和动销”, “看粉丝/商品数/销量/销售额的日周月增长”, “linkfox-geekbi-temu-shop”.

**Adjacent**: Within an active shop-search workflow, resolve an unknown marketplace or category through the helper endpoints. If the user explicitly invokes this skill, either helper may also be called independently without launching a shop search.

**Not an automatic trigger**: A request solely to enumerate Temu sites, `regionId` values, categories, or `catId` values, unless the user explicitly invokes this skill or the skill is already active.

**Not applicable**: Generic Temu shop search/ranking without GeekBI-specific metrics (use `linkfox-temu-store-query`); Temu seller-center orders, inventory changes, listing publication, fulfillment, account authorization, advertising operations, product-level research, or research on another marketplace. Unless the user explicitly requests cross-source comparison, do not call both paid shop-data skills.

## 算力消耗规则

店铺搜索每次消耗 15 算力；站点列表和品类列表不消耗算力。

> 用户会为店铺搜索支付算力。高频调用、翻页或改条件重搜前，必须让用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
