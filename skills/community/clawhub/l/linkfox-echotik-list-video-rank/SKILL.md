---
name: linkfox-echotik-list-video-rank
description: 查询TikTok视频排行榜，按日榜、周榜或月榜以及区域与视频排名指标获取热门视频榜单，返回播放量、点赞、评论、分享、收藏、视频销量与GMV等指标，覆盖16个TikTok Shop站点。当用户提到TikTok视频排行、TikTok热门视频榜单、TikTok视频排名、TikTok日榜、TikTok周榜、TikTok月榜、TikTok带货视频排行、TikTok视频销量排行、TikTok视频GMV排行、EchoTik视频排行、TikTok video ranking, TikTok top videos chart, TikTok video leaderboard, TikTok viral video ranking时触发此技能。即使用户未明确提及"EchoTik"或"视频排行"，只要其需求涉及按日期获取TikTok视频榜单或视频排名，也应触发此技能。
---

# EchoTik - TikTok Video Ranking

This skill queries TikTok Shop **video ranking** data via the EchoTik data source, helping cross-border sellers and marketers discover top-performing videos in daily, weekly, or monthly rankings. Unlike `linkfox-echotik-list-video` (which lists videos by region with free filters), this tool returns a **dated ranking** of videos sorted by a chosen metric.

## Core Concepts

EchoTik is a TikTok Shop analytics platform. This tool returns ranked video lists for a selected day, week, or month, ordered by a selected ranking metric.

**Required input**: `date`, `rankType`, `region`, and `videoRankField` are all mandatory. There are no defaults for required fields.

**Related skill**: To list videos by region with free filters (creator / product / views range / ad / AI flags) instead of a dated ranking, use `linkfox-echotik-list-video`. This skill is for ranked, date-scoped video charts.

## Data Fields

The response `data[*]` video object has 25 documented fields. Metric names begin with `total` but represent the **ranking period's** cumulative value. Key fields:

| Field | Description |
|-------|-------------|
| videoId / officialUrl / coverUrl | Video ID / TikTok URL / cover image URL |
| videoDesc / duration / createDate | Description / duration (seconds) / publish date |
| userId / uniqueId / nickName / avatar | Creator ID / TikTok account ID / nickname / avatar |
| category / region | Creator category / marketplace code |
| totalViewsCnt / totalDiggCnt / totalCommentsCnt | Period views / likes / comments |
| totalSharesCnt / totalFavoritesCnt | Period shares / favorites |
| totalVideoSaleCnt / totalVideoSaleGmvAmt | Period video sales (units, estimated) / sales GMV (estimated) |
| salesFlagText / createdByAiText | Selling video flag / AI video flag (是/否) |
| productCategoryList / videoProducts | Selling product categories / products |
| sourceType / sourceTool | Product source / source tool |

> Full field list with types is in `references/api.md`. This shape **differs** from `linkfox-echotik-list-video` (no width/height/ratio, no 1d/7d/30d breakdowns, no `isAdText`).

## Parameter Guide

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| date | string | Yes | - | Query date, `YYYY-MM-DD` |
| rankType | integer | Yes | - | Ranking type (see values below) |
| region | string | Yes | - | Marketplace code. See supported list below |
| videoRankField | integer | Yes | - | Ranking metric (see values below) |
| productCategoryId | string | No | - | Level-1 product category ID for filtering sales-video rankings |
| createdByAi | string | No | - | AI-video filter: `true` or `false` |
| pageNum | integer | No | 1 | Page number, starts at 1 |
| pageSize | integer | No | 50 | Page size — must be a multiple of 10, max 100 |

### rankType values

| Value | Meaning |
|-------|---------|
| 1 | Daily ranking (day) |
| 2 | Weekly ranking (week) |
| 3 | Monthly ranking (month) |

### videoRankField values

| Value | Meaning | Verified |
|-------|---------|----------|
| 1 | Rank by views (播放量) | ✓ 200 |
| 2 | Rank by video sales (视频销量) | ✓ 200 |

> **Metric sparsity**: when ranking by a given `videoRankField`, the other metric fields may return 0 (ranking by sales → views/likes/comments can be 0; ranking by views → sales/GMV can be 0).

### Supported Marketplaces

US (United States), ID (Indonesia), TH (Thailand), PH (Philippines), MY (Malaysia), VN (Vietnam), GB (United Kingdom), MX (Mexico), SG (Singapore), SA (Saudi Arabia), BR (Brazil), ES (Spain), JP (Japan), DE (Germany), IT (Italy), FR (France)

When the user doesn't specify a marketplace, ask or default to **US**.

## 调用方式

- **API 端点**：`POST /echotik/listVideoRank`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_list_video_rank.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-list-video-rank-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Top US videos by views on a given day**
```json
{
  "date": "2026-08-10",
  "rankType": 1,
  "region": "US",
  "videoRankField": 1,
  "pageNum": 1,
  "pageSize": 20
}
```

**2. Weekly UK video ranking**
```json
{
  "date": "2026-08-10",
  "rankType": 2,
  "region": "GB",
  "videoRankField": 1
}
```

**3. Monthly US sales ranking filtered to AI videos**
```json
{
  "date": "2026-08-01",
  "rankType": 3,
  "region": "US",
  "videoRankField": 2,
  "createdByAi": "true",
  "productCategoryId": "601450",
  "pageNum": 1,
  "pageSize": 20
}
```

## Display Rules

1. **Present data in tables**: Show video description (truncated if long), views, likes, comments, shares, video sales, video GMV, publish date, and creator ID.
2. **Rank order**: Results are already ranked by the chosen `videoRankField`; preserve and surface the ranking order.
3. **Link to original**: When `officialUrl` is available, provide it so users can view the video on TikTok.
4. **Estimation notice**: Video sales and GMV are estimated values; remind users these are approximations.
5. **Result count**: Always inform the user of `total` records and the current page; suggest pagination when the result set is large.

## Important Limitations

1. **All four required fields**: `date`, `rankType`, `region`, `videoRankField` are mandatory; no defaults are applied.
2. **Ranking data lags 1–2 days**: Recent ranking data may be unavailable and return `errcode:10000` ("no matching data"). Use an earlier date if needed.
3. **Ranking vs. listing**: This is a dated ranking. For region-scoped video listing with free filters (creator / views range / ad / AI flags), use `linkfox-echotik-list-video`.
4. **No secondary processing**: Results are live queries; secondary SQL/data processing is not available.

## User Expression & Scenario Quick Reference

**Applicable** — TikTok video ranking / charts:

| User Says | Scenario |
|-----------|----------|
| "TikTok视频排行" / "TikTok top video chart" | Video ranking by selected period and metric |
| "本周TikTok最火的视频" | Weekly ranking (`rankType:2`) |
| "本月TikTok带货视频榜" | Monthly sales ranking (`rankType:3`) |
| "TikTok带货视频排行" | Ranked selling videos (inspect sales/GMV columns) |
| "英国TikTok视频榜单" | region=GB ranking |

**Not applicable** — Needs beyond dated video ranking:

- Region-scoped video listing with free filters (use `linkfox-echotik-list-video`)
- Videos for one specific product by `productId` (use `linkfox-echotik-product-video`)
- Video download URL resolution (use `linkfox-echotik-get-video-download-url`)
- TikTok product / seller rankings

**Boundary judgment**: When users say "视频排行/视频榜单/最火视频" with a date or region context, this skill applies. If they want to filter videos by creator, views range, or ad/AI flags without a ranking, use `linkfox-echotik-list-video`.

## 算力消耗规则

消耗 5 算力。

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
