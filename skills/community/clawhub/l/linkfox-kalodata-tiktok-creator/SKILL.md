---
name: linkfox-kalodata-tiktok-creator
description: 通过kalodata数据搜索TikTok电商达人榜单并查询指定达人的详细资料，支持按地区、货币、语言与日期范围查看高排名带货达人，并可用creatorId获取粉丝数、视频/直播销售额与GPM、联系方式及关联店铺。当用户提到TikTok达人搜索、TikTok达人榜单、TikTok达人排行、TikTok网红排行、TikTok达人详情、TikTok达人资料、达人主页数据、达人联系方式、TikTok creator search, TikTok creator ranking, TikTok influencer leaderboard, TikTok creator detail, creator analytics, kalodata creator search/detail时触发此技能。即使用户未明确提及"kalodata"，只要其需求涉及查看TikTok平台达人排行榜或某个TikTok达人的详细带货数据，也应触发此技能。
---

# Kalodata - TikTok Creator Search & Detail

This skill supports a two-step TikTok creator workflow via the Kalodata data source:

1. Browse creator leaderboards to discover high-performing TikTok Shop creators.
2. Fetch one creator's full profile and performance detail by `creatorId`.

Use the search endpoint when the user wants rankings, influencer discovery, or creator comparison. Use the detail endpoint when the user already has a `creatorId` or has selected one creator from a ranking result.

## Core Concepts

The creator ranking endpoint returns a paginated leaderboard filtered by `region`, `dateRange`, `language`, and `currency`. The default ranking order is by `revenue` (GMV) descending. Each creator row includes identity, audience, content views, sales volume, video/live revenue, and revenue growth rate.

The creator detail endpoint fetches **one** creator by `creatorId`. It returns the creator's identity, audience, revenue split, video/live metrics, product/shop counts, and contact channels. The `creatorId` usually comes from the ranking response field `creator_id`.

Both endpoints may reflect a statistical delay (T+1). See `references/api.md` for full request and response details.

## Data Fields

**Ranking rows** include:

| Field | Description |
|-------|-------------|
| creator_nickname | Creator display name |
| creator_handle | TikTok handle |
| creator_id | Creator unique ID; pass this as `creatorId` for detail lookup |
| creator_followers | Follower count, returned as a string |
| content_views | Total content views, returned as a string |
| sales_volumn | Sales volume; field is spelled `volumn` |
| revenue | Total GMV in the requested currency |
| video_revenue | Revenue from videos |
| live_revenue | Revenue from livestreams |
| revenue_growth_rate | Revenue growth rate (%) |

**Detail rows** additionally include:

| Field | Description |
|-------|-------------|
| creator_region / creator_status / creator_bio | Creator profile metadata |
| new_followers | New followers in the requested date window |
| unit_price | Average unit price in the requested currency |
| video_number / video_views / video_gpm | Video count, views, and GPM |
| live_number / live_views / live_gpm | Livestream count, views, and GPM |
| product_number / shop_number | Associated product and shop counts |
| creator_contact_* | Email and social contact fields; often empty |

## Parameter Guide

**Creator ranking (`/kalodata/creator/rank`)**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| pageNumber | integer | No | Page number, 1-5 |
| pageSize | integer | No | Page size, 5-100 |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |
| category_ids | array<integer> | No | Category ID list filter |
| shop_id | string | No | Shop ID filter |
| revenue_range | string | No | Revenue / GMV range filter |
| creator_type | string | No | Creator type filter |
| followers_range | string | No | Follower range filter |
| engagement_rate | string | No | Engagement-rate filter |
| sortField | object | No | Sorting specification; pass `{}` for default revenue ranking |

**Creator detail (`/kalodata/creator/detail`)**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| creatorId | string | Yes | Creator unique ID from ranking field `creator_id` |
| shop_id | string | No | Shop ID filter |
| category_ids | array<integer> | No | Category ID list filter |
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |

## 调用方式

- **API 端点**：`POST /kalodata/creator/rank` 或 `POST /kalodata/creator/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/kalodata_creator_search.py '<JSON 参数>' [--inline]` 或 `python scripts/kalodata_creator_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-kalodata-tiktok-creator-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Browse top TikTok creators in the US**
```json
{"region":"US","dateRange":"last7Day","pageSize":10,"pageNumber":1,"currency":"USD"}
```

**2. Fetch one creator's detail**
```json
{"creatorId":"7153432386608251946","region":"US","dateRange":"last7Day","currency":"USD"}
```

**3. Discovery-to-detail workflow**
```text
Run kalodata_creator_search.py first, choose a row's creator_id, then pass that value as creatorId to kalodata_creator_detail.py.
```

## Display Rules

1. Present ranking results in a table with nickname, handle, followers, content views, sales volume, revenue, video/live revenue, and growth rate.
2. Present detail results as one grouped profile: identity, audience, revenue, video, live, products/shops, and contact.
3. Always label `dateRange`, `region`, and `currency` when showing metrics.
4. Treat `creator_followers` and `content_views` as string-typed counts; parse before numeric comparison.
5. Use the exact field name `sales_volumn`.
6. Show contact fields only when populated; otherwise say no contact was provided.
7. Preserve ranking order unless the user explicitly requests a supported `sortField`.

## Important Limitations

- Ranking is not keyword search; it browses leaderboards by region and time window.
- Detail requires `creatorId`; it cannot find a creator by nickname or handle alone.
- The ranking response does not include total/page count; paginate until a page returns fewer than `pageSize` items.
- `pageNumber` is limited to 1-5 and `pageSize` is limited to 5-100.
- Transient upstream errors may appear as `errcode 501` with a Kalodata HTTP 554 message. Retry the same parameters once or twice; do not change parameters automatically.
- Use the matching Kalodata product/video/shop/livestream skills for non-creator entities.

## User Expression & Scenario Quick Reference

**Applicable** -- TikTok creator ranking or creator profile lookup:

| User Says | Scenario |
|-----------|----------|
| "TikTok达人排行榜", "TikTok网红榜" | Creator ranking lookup |
| "TikTok带货达人榜", "top TikTok creators" | Creator leaderboard by region |
| "近7天TikTok达人榜" | Time-windowed ranking |
| "TikTok达人详情", "达人主页数据" | Creator detail lookup |
| "达人联系方式", "creator contact" | Contact channels |
| "kalodata creator search/detail" | Direct data source reference |

**Not applicable** -- Needs beyond TikTok creators:

- TikTok product/video/shop/livestream rankings or details
- Amazon / Shopify / 1688 / other platforms' creator or product data
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
