---
name: linkfox-kalodata-tiktok-livestream
description: 通过kalodata数据搜索TikTok电商直播排行榜并查询指定直播的详细数据，支持按地区、货币、语言与日期范围查看高排名、高销量的TikTok带货直播，并可用livestreamId获取直播销售额、观看人数、时长、GPM及带货商品数。当用户提到TikTok直播榜单、TikTok直播排行、TikTok带货直播榜、TikTok热销直播、TikTok直播排名、TikTok直播详情、TikTok直播数据、直播观看人数、kalodata直播搜索、kalodata直播榜、TikTok livestream ranking, TikTok live ranking, TikTok top livestreams, TikTok live shopping ranking, TikTok livestream detail, kalodata livestream search/detail, live analytics时触发此技能。即使用户未明确提及"kalodata"，只要其需求涉及查看TikTok平台的直播排行榜或某个TikTok直播的详细数据，也应触发此技能。
---

# Kalodata - TikTok Livestream Search & Detail

This skill supports a two-step TikTok livestream workflow via the Kalodata data source:

1. Browse TikTok Shop livestream leaderboards to discover top-performing shoppable livestreams (带货直播).
2. Fetch one livestream's full performance detail by `livestreamId`.

Use the search (rank) endpoint when the user wants rankings, hot livestreams, or livestream discovery. Use the detail endpoint when the user already has a `livestreamId` or has selected one livestream from a ranking result.

## Core Concepts

The livestream ranking endpoint returns a paginated leaderboard filtered by `region`, `dateRange`, `language`, `currency`, and optional `sortField`. The default ranking order is by `revenue` (GMV) descending. Each livestream row includes identity, timing, scale, and creator fields. Results are paginated with `pageNumber` (1-5) and `pageSize` (5-100). The response does **not** include a total count — paginate until a page returns fewer than `pageSize` items. Money fields (`revenue`, `unit_price`) are returned as **strings** on the ranking endpoint.

The livestream detail endpoint fetches **one** shoppable TikTok livestream by `livestreamId`. It returns a **1-element array** with the single livestream's full detail (12 fields), including `viewers`, numeric `revenue`, `gpm`, and `product_number`. There is no pagination and no `total`. The `livestreamId` usually comes from the ranking response field `livestream_id`.

> **Field names/types differ between the two endpoints**: DETAIL uses `viewers` (RANK uses `views`); DETAIL `revenue` is a **number** (RANK `revenue` is a **string**); DETAIL has `gpm` and lacks `unit_price` (RANK has `unit_price` and lacks `gpm`). Do not assume field names/types carry over between the two endpoints.

Both endpoints may reflect a statistical delay (T+1). See `references/api.md` for full request and response details.

## Data Fields

**Ranking rows** (each item in `data` from `/kalodata/livestream/rank`):

| Field | Type | Description |
|-------|------|-------------|
| livestream_id | string | Livestream unique ID; pass this as `livestreamId` for detail lookup |
| livestream_title | string | Livestream title |
| creator_id | string | Creator unique ID (string to preserve precision) |
| creator_handle | string | Creator handle / username |
| livestream_start_time | integer | Start time, epoch milliseconds |
| livestream_end_time | integer | End time, epoch milliseconds |
| livestream_duration | integer | Duration in seconds |
| revenue | string | Total revenue / GMV in the requested `currency` — **returned as a string**, e.g. `"185590.52"` |
| unit_price | string | Average unit price in the requested `currency` — **returned as a string**, e.g. `"265.89"` |
| views | integer | Total views (note: RANK uses `views`) |
| record_type | string | Record type (e.g. `SHORT`) |

**Detail rows** (the single item in `data` from `/kalodata/livestream/detail`):

| Field | Type | Description |
|-------|------|-------------|
| livestream_id | string | Livestream unique ID (matches the requested `livestreamId`) |
| livestream_title | string | Livestream title (e.g. `24 HOUR STREAM`) |
| creator_id | string | Creator unique ID (string to preserve precision) |
| creator_handle | string | Creator handle / username (e.g. `pokepiglt`) |
| livestream_start_time | integer | Start time, epoch milliseconds |
| livestream_end_time | integer | End time, epoch milliseconds |
| livestream_duration | integer | Duration in seconds |
| record_type | string | Record type (e.g. `SHORT`) |
| viewers | integer | Total viewers (note: DETAIL uses `viewers`, NOT `views`) |
| revenue | number | Livestream revenue / GMV as a **number** in the requested `currency` (e.g. `185590.52`) — a number here, a string on the RANK endpoint |
| gpm | number | GMV per mille (revenue per 1,000 impressions) — DETAIL-only, absent from RANK |
| product_number | integer | Number of products sold/promoted during the livestream |

> **Money fields are strings on RANK, numbers on DETAIL.** Parse RANK `revenue`/`unit_price` (`float()`, `Number()`, or `ConvertFrom-Json`) before numeric comparison or formatting. Use the exact field name for the endpoint you are reading (`views` on RANK, `viewers` on DETAIL).

## Parameter Guide

**Livestream ranking (`/kalodata/livestream/rank`)** — all parameters optional:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| pageNumber | integer | No | Page number, 1-5 |
| pageSize | integer | No | Page size, 5-100 |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |
| category_id | string | No | Category ID filter |
| shop_id | string | No | Shop ID filter |
| creator_id | string | No | Creator ID filter |
| product_id | string | No | Product ID filter |
| followers_range | string | No | Creator follower range filter |
| sortField | object | No | Sorting specification; pass `{}` for the default ranking order |

**Livestream detail (`/kalodata/livestream/detail`)**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| livestreamId | string | Yes | Target livestream's unique ID (camelCase), e.g. `7661409374878878494`. Typically obtained from the ranking field `livestream_id` |
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |

## 调用方式

- **API 端点**：`POST /kalodata/livestream/rank`（榜单）或 `POST /kalodata/livestream/detail`（详情）（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/kalodata_livestream_search.py '<JSON 参数>' [--inline]`（榜单）或 `python scripts/kalodata_livestream_detail.py '<JSON 参数>' [--inline]`（详情）
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-kalodata-tiktok-livestream-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
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

**1. Browse top TikTok livestreams in the US**
```json
{"region":"US","dateRange":"last7Day","pageSize":10,"pageNumber":1}
```

**2. Fetch one livestream's detail**
```json
{"livestreamId":"7661409374878878494","region":"US","dateRange":"last7Day"}
```

**3. Discovery-to-detail workflow**
```text
Run kalodata_livestream_search.py first, choose a row's livestream_id, then pass that value as livestreamId to kalodata_livestream_detail.py.
```

## Display Rules

1. **Present data only**: Show the ranking in a clear table (livestream title, creator handle, revenue, views, duration, unit price, start/end times) and the detail as one grouped profile, without subjective business advice.
2. **Ranking order**: The default order is `revenue` (GMV) descending; there is no explicit `rank` field — position is implied by order. Preserve it unless the user explicitly requests a supported `sortField`.
3. **Currency awareness**: Display the requested `currency` alongside `revenue`/`unit_price` (rank) or `revenue`/`gpm` (detail).
4. **Money as strings on RANK**: RANK `revenue` and `unit_price` are returned as **strings** (e.g. `"185590.52"`) — parse them before numeric comparison or formatting. DETAIL `revenue` is a number. Use the exact field name when extracting with `jq` / `ConvertFrom-Json`.
5. **Viewers vs views**: Use `views` for ranking rows and `viewers` for detail rows — do not mix them.
6. **GPM**: `gpm` is GMV per mille (detail-only) — present with appropriate precision (e.g. `903.79`), not as a percentage.
7. **Time fields**: `livestream_start_time`/`livestream_end_time` are epoch **milliseconds**; `livestream_duration` is **seconds**. Format human-readable local times when displaying.
8. **Time window**: Always label which `dateRange` the data covers (e.g. "last 7 days").
9. **Pagination hint**: The ranking response has no total/page count; if a full page is returned, suggest the user can request the next page (up to `pageNumber` 5).
10. **Single entity**: The detail is one livestream — do not present it as a ranking or leaderboard.

## Important Limitations

- **Ranking is not keyword search**: It browses a livestream leaderboard filtered by region/time; it does not search livestreams by keyword.
- **Detail requires `livestreamId`**: It cannot find a livestream by title alone. Obtain `livestreamId` from the ranking field `livestream_id`.
- **Max 5 pages, page size 5-100**: `pageNumber` is limited to 1-5; out of range returns `errcode 501, errmsg "page_number 范围为 1-5，当前: <n>"`. `pageSize` must be between 5 and 100.
- **No total/page count**: Neither response includes `total` or page-count fields; paginate the ranking until a page returns fewer than `pageSize` items.
- **Field names/types differ between endpoints**: DETAIL uses `viewers` (RANK uses `views`); DETAIL `revenue` is a **number** (RANK `revenue` is a **string**); DETAIL has `gpm` and lacks `unit_price` (RANK has `unit_price` and lacks `gpm`). Do not assume field names/types carry over.
- **Data delay**: Both endpoints may have a statistical delay (T+1).
- **Transient upstream errors**: The gateway may occasionally return `errcode 501, errmsg "调用 Kalodata 接口失败: Kalodata API HTTP 554: "` (a transient upstream Kalodata error). Retry the same parameters once or twice; do not change parameters.
- **Unsupported sort/filter**: If a requested `sortField` is not accepted by the gateway, do NOT attempt workarounds — inform the user and fall back to the default ranking order.
- **Use the matching Kalodata skills for non-livestream entities**: creator/product/video/shop rankings or details.

## User Expression & Scenario Quick Reference

**Applicable** -- TikTok livestream ranking or livestream detail lookup:

| User Says | Scenario |
|-----------|----------|
| "TikTok直播排行榜", "TikTok直播排行" | Livestream ranking lookup |
| "TikTok热销直播", "top TikTok livestreams" | Livestream leaderboard by region |
| "近7天TikTok直播榜", "美国TikTok直播排名" | Time-windowed / region-filtered ranking |
| "Kalodata直播榜" | Direct data source reference |
| "TikTok直播详情", "TikTok直播数据" | Single livestream detail lookup |
| "这场直播的观看人数", "这场直播卖了多少钱" | Viewers / revenue / GPM for a specific livestream |
| "TikTok livestream detail", "kalodata livestream search/detail" | Direct detail/rank fetch |

**Not applicable** -- Needs beyond TikTok livestreams:

- TikTok creator/product/video/shop rankings or details (use the corresponding Kalodata skills)
- A livestream's detail without a known `livestreamId` (first obtain the ID via the ranking endpoint)
- Amazon / Shopify / 1688 / other platforms' livestream data
- TikTok ad campaign management or content creation

**Boundary judgment**: When users say "直播榜" or "直播排行" in a TikTok Shop / TikTok e-commerce context, use the ranking endpoint. When they ask about a *specific* livestream's detailed metrics (revenue, viewers, duration, GPM) and a `livestreamId` is available (or can be obtained from the ranking), use the detail endpoint.

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
