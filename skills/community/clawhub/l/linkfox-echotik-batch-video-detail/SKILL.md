---
name: linkfox-echotik-batch-video-detail
description: 批量查询TikTok视频详情数据，包括视频描述、播放量（总量及近1天/7天/30天增量）、点赞（总量及增量）、评论、分享、收藏、视频销量与GMV、视频时长与分辨率、发布日期、达人信息（ID/账号/头像）、是否带货/投流/AI视频、关联商品与类目，支持通过视频ID或TikTok视频URL批量获取。当用户提到TikTok视频详情、批量查询TikTok视频、TikTok视频播放量详情、TikTok视频销量详情、TikTok视频数据分析、批量获取TikTok视频信息、EchoTik视频详情、TikTok video detail, batch video lookup, TikTok video analytics detail, TikTok video views detail, TikTok video sales detail时触发此技能。即使用户未明确提及"EchoTik"，只要其需求涉及根据视频ID或视频URL批量获取TikTok视频的详细播放与营销数据，也应触发此技能。
---

# EchoTik TikTok Batch Video Detail

This skill batch-fetches detailed performance metrics for TikTok videos you already have IDs or URLs for, helping sellers and marketers compare videos side-by-side using views, likes, comments, shares, video sales/GMV, and creator data.

## Core Concepts

This tool retrieves full detail metrics for a batch of TikTok videos in a single call. You identify videos by ID and/or by TikTok video URL; the backend extracts the `videoId` from each URL and merges it with any IDs you supplied, then returns per-video analytics.

**Input options** (at least one is needed; both can be combined):
- `videoIds` — array of TikTok video IDs (up to 1000)
- `videoUrls` — array of TikTok video URLs (e.g. `https://www.tiktok.com/@<unique_id>/video/<videoId>` or `https://www.tiktok.com/video/<videoId>`); the trailing `videoId` is extracted from each URL and merged with `videoIds` (up to 1000)

**Multi-period metrics**: views and likes are each reported as a cumulative total plus `1d / 7d / 30d` increments, so you can read both lifetime performance and recent momentum.

**Engagement & attribution**: comments, shares, favorites, estimated video sales (units), and estimated video sales GMV (amount) are returned per video.

**Flag fields** (`salesFlagText` / `isAdText` / `createdByAiText`): human-readable 是/否 (AI: 是/否/未知) labels for selling / ad / AI-generated videos.

**vs. search**: This is detail **lookup for known videos** (you already have IDs/URLs). To *discover* videos by region/filter (no IDs needed), use `linkfox-echotik-list-video`.

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| videoId | string | 视频ID |
| videoDesc | string | 视频描述/文案 |
| officialUrl | string | TikTok官方视频地址 |
| coverUrl | string | 视频封面URL |
| duration | integer | 视频时长(秒) |
| width | string | 视频宽度(px) |
| height | string | 视频高度(px) |
| ratio | string | 视频清晰度(如 540p/720p) |
| dataSize | string | 视频文件大小 |
| createDate | string | 视频发布日期(yyyy-MM-dd HH:mm:ss) |
| userId | string | 达人ID |
| uniqueId | string | TikTok账号ID(unique_id) |
| avatar | string | 达人头像URL |
| totalViewsCnt | integer | 总播放量 |
| totalViews1dCnt | integer | 近1天播放量增量 |
| totalViews7dCnt | integer | 近7天播放量增量 |
| totalViews30dCnt | integer | 近30天播放量增量 |
| totalDiggCnt | integer | 总点赞数 |
| totalDigg1dCnt | integer | 近1天点赞增量 |
| totalDigg7dCnt | integer | 近7天点赞增量 |
| totalDigg30dCnt | integer | 近30天点赞增量 |
| totalCommentsCnt | integer | 总评论数 |
| totalSharesCnt | integer | 总分享数 |
| totalFavoritesCnt | integer | 总收藏数 |
| totalVideoSaleCnt | integer | 视频销量(件,估算) |
| totalVideoSaleGmvAmt | integer | 视频销售GMV(估算金额) |
| salesFlagText | string | 是否带货视频(是/否) |
| isAdText | string | 是否投流视频(是/否) |
| createdByAiText | string | 是否AI视频(是/否/未知) |
| productCategoryList | string | 关联商品分类(JSON字符串,空为`[]`) |
| videoProducts | string | 视频带货商品(JSON字符串,空为`[]`) |
| region | string | 视频所在区域代码 |
| sourceType | string | 数据来源(如 Tiktok) |
| sourceTool | string | 来源工具(如 EchoTik-视频列表) |

## Parameter Guide

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| videoIds | array&lt;string&gt; | No* | - | TikTok视频ID列表，最多1000个 |
| videoUrls | array&lt;string&gt; | No* | - | TikTok视频URL列表（形如 `https://www.tiktok.com/@<unique_id>/video/<videoId>` 或 `https://www.tiktok.com/video/<videoId>`）；从每个URL提取末尾videoId并合并到videoIds，与videoIds不互斥，最多1000个 |

\* 至少提供 `videoIds` / `videoUrls` 中的一个；两者可同时传入，服务端合并去重后查询。

## 调用方式

- **API 端点**：`POST /echotik/batchVideoDetail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_batch_video_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-batch-video-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

**1. Batch lookup by video IDs**
```json
{
  "videoIds": ["7030893014180531462", "6768504823336815877", "7425631540178160939"]
}
```

**2. Batch lookup by video URLs**
```json
{
  "videoUrls": [
    "https://www.tiktok.com/@sageandintuition/video/7030893014180531462",
    "https://www.tiktok.com/@<unique_id>/video/6768504823336815877"
  ]
}
```

**3. Mixed IDs and URLs (merged server-side)**
```json
{
  "videoIds": ["7030893014180531462"],
  "videoUrls": ["https://www.tiktok.com/@<unique_id>/video/6768504823336815877"]
}
```

## Display Rules

1. **Present a comparison table**: Show one row per video with video description (truncated if long), views, likes, comments, shares, video sales, video GMV, publish date, and creator
2. **Link to original**: When `officialUrl` is available, provide it so users can view the video on TikTok
3. **Cover image**: If `coverUrl` is present, mention that video thumbnails are available
4. **Duration formatting**: Convert `duration` (seconds) to a readable format (e.g. "2:45" for 165 seconds)
5. **Multi-period metrics**: When relevant, surface the 1d/7d/30d views/likes breakdowns alongside the lifetime totals
6. **Estimation notice**: Video sales and GMV are estimated values — remind users these are approximations
7. **Flag badges**: Render `salesFlagText` (带货), `isAdText` (投流), and `createdByAiText` (AI) so users can scan video types at a glance
8. **Missing video handling**: If a requested video returns no record, list which IDs/URLs had no data so the user can verify them
9. **Result count**: Always inform the user of `total` records returned

## Important Limitations

- **Batch cap**: Up to 1000 videos per request
- **Lookup only**: This tool does not search/discover videos by region or filter — it resolves specific IDs/URLs you already have. To discover videos, use `linkfox-echotik-list-video`
- **URL extraction**: For `videoUrls`, only the trailing `videoId` is extracted — ensure each URL ends with the video ID
- **Estimated data**: Sales, GMV, and attribution figures are analytics estimates, not exact platform figures
- **JSON-string fields**: `productCategoryList` / `videoProducts` are returned as JSON strings (empty when none, e.g. `[]`) — parse before display if needed
- **No secondary processing**: Results are live queries, not stored in a database; secondary SQL/data processing is not available

## User Expression & Scenario Quick Reference

### Applicable Scenarios

| User Says | Scenario |
|-----------|----------|
| "查询这些TikTok视频的详情" | Batch detail by video IDs |
| "拉这些TikTok视频链接的播放量/销量" | Batch detail by video URLs |
| "批量分析这些TikTok视频的表现" | Batch lookup, surface metrics |
| "这些TikTok视频哪个播放量/销量最高" | Batch lookup, compare columns |
| "这些TikTok视频是不是带货/投流/AI" | Batch lookup, read flag fields |

### Not Applicable Scenarios

- Discovering videos by region/filter (use `linkfox-echotik-list-video`)
- TikTok product detail lookup (use `linkfox-echotik-batch-product-detail`)
- Resolving a TikTok video download link (use `linkfox-echotik-get-video-download-url`)
- TikTok creator/seller (store) analytics (use `linkfox-echotik-seller-detail` / `linkfox-echotik-list-seller`)
- Non-TikTok platform video data

### Boundary Judgment

When users say "分析这些TikTok视频", check whether they already have specific video IDs or TikTok video URLs (this skill) or want to *find* videos by region/filter (the list-video skill). If they paste a list of IDs/URLs and want views/likes/sales/GMV details, this skill applies. If they ask "找热门TikTok视频" or "按区域搜视频", it does not — use `linkfox-echotik-list-video` to discover first.

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
