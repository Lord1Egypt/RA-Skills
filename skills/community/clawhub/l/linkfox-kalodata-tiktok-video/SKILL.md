---
name: linkfox-kalodata-tiktok-video
description: 通过kalodata数据搜索TikTok电商热门带货视频榜单并查询指定视频的详细数据，支持按地区、货币、语言、日期范围与GMV范围查看高排名/高播放/热销带货视频，并可按GMV排序，或用videoId获取播放、点赞、评论、分享、销售额、GPM及广告投放指标。当用户提到TikTok视频搜索、TikTok视频榜单、TikTok视频排行、TikTok热门视频、TikTok带货视频排行、TikTok爆量视频、TikTok视频详情、TikTok带货视频数据、视频播放量、GMV筛选、视频互动数据、TikTok video search, TikTok video ranking, TikTok viral video chart, TikTok video detail, video analytics, kalodata video search/detail时触发此技能。即使用户未明确提及"kalodata"，只要其需求涉及查看TikTok平台热门带货视频榜单或某个TikTok视频的详细带货与互动数据，也应触发此技能。
---

# Kalodata - TikTok Video Search & Detail

This skill supports a two-step TikTok video workflow via the Kalodata data source:

1. Browse TikTok Shop video leaderboards to discover high-performing shoppable videos.
2. Fetch one video's full performance detail by `videoId`.

Use the search endpoint when the user wants rankings, hot videos, viral videos, or video discovery. Use the detail endpoint when the user already has a `videoId` or has selected one video from a ranking result.

## Core Concepts

The video ranking endpoint returns a paginated leaderboard filtered by `region`, `dateRange`, `language`, `currency`, and optional GMV range `revenue_range`. Use `sortField` to sort by `revenue`. Each video row includes identity, engagement, revenue, ad-performance, and creator fields. Results are paginated with `pageNumber` (1-5) and `pageSize` (5-100).

The video detail endpoint fetches **one** shoppable TikTok video by `videoId`. It returns the video's engagement metrics, monetization metrics, advertising metrics, creator identity, region, duration, and linked product count. The `videoId` usually comes from the ranking response field `video_id`.

Both endpoints may reflect a statistical delay (T+1). See `references/api.md` for full request and response details.

## Data Fields

**Ranking rows** include:

| Field | Description |
|-------|-------------|
| video_id | Video unique ID; pass this as `videoId` for detail lookup |
| video_title | Video title / caption |
| views | Video view count |
| digg_count / comment_count / share_count | Likes, comments, and shares |
| revenue | Total GMV in the requested currency |
| revenue_growth_rate | Revenue growth rate (%) |
| ad / ad_view_ratio / ad_revenue_ratio / ads_roas | Ad and advertising performance fields |
| belonged_creator_id / belonged_creator_handle | Creator identity |
| creator_debut | Creator debut date |

**Detail rows** additionally include:

| Field | Description |
|-------|-------------|
| video_region | Video region; may be empty |
| sales_volumn | Sales volume; field is spelled `volumn` |
| video_gpm | GMV per mille (revenue per 1000 views) |
| ads_views / ad_cpa / ads_period | Ad views, CPA, and ad running period |
| duration | Video duration in seconds |
| product_number | Number of products linked in the video |

## Parameter Guide

**Video ranking (`/kalodata/video/rank`)**

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
| revenue_range | string | No | GMV range because response field `revenue` is total GMV; examples: `1-100`, `>1000`, `<100` |
| followers_range | string | No | Creator follower range filter |
| ads_roas | number | No | Advertising ROAS filter |
| sortField | object | No | GMV sorting specification, e.g. `{"field":"revenue","type":"DESC"}` |

**Video detail (`/kalodata/video/detail`)**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| videoId | string | Yes | TikTok video ID from ranking field `video_id` or a TikTok video URL |
| region | string | No | Market region code, e.g. `US` |
| dateRange | string | No | Time window, e.g. `last7Day`, `last30Day` |
| language | string | No | Response language, e.g. `zh-CN`, `en-US` |
| currency | string | No | Currency for monetary metrics, e.g. `USD` |

## 调用方式

- **API 端点**：`POST /kalodata/video/rank` 或 `POST /kalodata/video/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/kalodata_video_search.py '<JSON 参数>' [--inline]` 或 `python scripts/kalodata_video_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-kalodata-tiktok-video-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Browse top TikTok videos in the US**
```json
{"region":"US","dateRange":"last7Day","pageSize":10,"pageNumber":1,"currency":"USD"}
```

**2. Filter by GMV and rank by GMV**
```json
{"region":"US","dateRange":"last7Day","revenue_range":"1-100","sortField":{"field":"revenue","type":"DESC"},"pageSize":10,"pageNumber":1,"currency":"USD"}
```

**3. Fetch one video's detail**
```json
{"videoId":"7659161409279806734","region":"US","dateRange":"last7Day","currency":"USD"}
```

**4. Discovery-to-detail workflow**
```text
Run kalodata_video_search.py first, choose a row's video_id, then pass that value as videoId to kalodata_video_detail.py.
```

## Display Rules

1. Present ranking results in a table with title, video ID, views, engagement, revenue, ad indicators, and creator handle.
2. Present detail results as one grouped profile: identity, engagement, monetization, ads, creator, duration, and linked products.
3. Always label `dateRange`, `region`, and `currency` when showing metrics.
4. Use the exact field name `sales_volumn`.
5. `video_gpm` is GMV per mille; do not display it as a percentage.
6. Preserve ranking order unless the user explicitly requests a supported `sortField`.

## Important Limitations

- Ranking is not keyword search; it browses leaderboards by region and time window.
- The backend supports GMV range filtering through `revenue_range`; `revenue` in the response is GMV, not profit or ad spend.
- Detail requires `videoId`; it cannot find a video by title alone.
- The ranking response does not include total/page count; result count is `data.length`.
- `pageNumber` is limited to 1-5 and `pageSize` is limited to 5-100.
- Transient upstream errors may appear as `errcode 501` with a Kalodata HTTP 554 message. Retry the same parameters once or twice; do not change parameters automatically.
- Use the matching Kalodata product/creator/shop/livestream skills for non-video entities.

## User Expression & Scenario Quick Reference

**Applicable** -- TikTok video ranking or video detail lookup:

| User Says | Scenario |
|-----------|----------|
| "TikTok视频榜单", "TikTok视频排行" | Video ranking lookup |
| "TikTok热门视频", "TikTok爆量视频" | Top or viral video ranking |
| "TikTok带货视频排行", "top TikTok videos" | Region-specific shoppable video leaderboard |
| "TikTok视频详情", "TikTok带货视频数据" | Single video detail lookup |
| "视频播放量", "视频互动数据", "视频GPM" | Video engagement or monetization metrics |
| "kalodata video search/detail" | Direct data source reference |

**Not applicable** -- Needs beyond TikTok videos:

- TikTok product / creator / shop / livestream rankings or details
- Keyword-based video or product search
- TikTok advertising / ad campaign management
- Video editing, video download, or content creation

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
