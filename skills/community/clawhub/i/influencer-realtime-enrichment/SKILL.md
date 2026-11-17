---
name: influencer-realtime-enrichment
description: "Fetch fresh, on-demand creator data across TikTok, Instagram, Facebook, and YouTube: page/profile info, latest videos, posts, and media details. Realtime creator data, profile lookup, content details."
---

# Influencer Realtime Enrichment

Fetch fresh creator and content data when snapshot data is not enough for current decisions.

## Capability Matrix

### YouTube

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 实时采集-用户信息 | `youtube_realtime_user_info` | `GET /api/v1/youtube/realtime/user/info` | `query.anyOf(channel_id,username)` |
| 实时采集-用户视频 | `youtube_realtime_user_videos` | `GET /api/v1/youtube/realtime/user/videos` | `query.channel_id` |
| 实时采集-视频详情 | `youtube_realtime_video_detail` | `GET /api/v1/youtube/realtime/video/detail` | `query.video_id` |

### TikTok

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 实时采集-用户信息 | `tiktok_realtime_user_info` | `GET /api/v1/tiktok/realtime/user/info` | `query.anyOf(unique_id,user_id)` |
| 实时采集-用户视频 | `tiktok_realtime_user_videos` | `GET /api/v1/tiktok/realtime/user/videos` | `query.uid` |
| 实时采集-视频详情 | `tiktok_realtime_video_detail` | `GET /api/v1/tiktok/realtime/video/detail` | `query.video_id, query.region` |

### Instagram

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 实时采集-贴文详情 | `instagram_realtime_media_detail` | `GET /api/v1/instagram/realtime/media/detail` | `query.media_code` |
| 实时采集-用户信息 | `instagram_realtime_user_info` | `GET /api/v1/instagram/realtime/user/info` | `query.anyOf(username,user_id)` |
| 实时采集-用户贴文 | `instagram_realtime_user_medias` | `GET /api/v1/instagram/realtime/user/medias` | `query.user_id` |
| 实时采集-用户故事 | `instagram_realtime_user_stories` | `GET /api/v1/instagram/realtime/user/stories` | `query.user_id` |

### Cross-platform

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| `none` | `none` | `none` | `none` |

### Facebook

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 实时挖掘-页面信息 | `facebook_page_info` | `GET /api/v1/facebook/realtime/page/info` | `query.page_url` |
| 实时挖掘-帖子详情 | `facebook_post_detail` | `GET /api/v1/facebook/realtime/post/detail` | `query.post_url` |
| 任务-关键词搜索帖子 | `facebook_task_post_search` | `GET /api/v1/facebook/task/post/search` | `query.query` |
| 任务-页面帖子 | `facebook_task_page_posts` | `GET /api/v1/facebook/task/page/posts` | `query.page_url` |
| 任务-查询结果 | `facebook_task_result` | `GET /api/v1/facebook/task/result` | `query.task_id` |

## Quick Start

1. Confirm freshness requirement and urgency window.
2. Choose platform and target object type (user/media/video/story).
3. Use matrix to select realtime detail/list endpoints.
4. Return delta-oriented findings and campaign impact.

## Workflow

1. Define enrichment target: creator-level or content-level.
2. Execute realtime retrieval with minimal required identifiers.
3. Compare new payload against prior assumptions and summarize deltas.
4. Flag impact and next monitoring action.

## Tooling

Execution commands:
- List operations: `python3 scripts/execute_operation.py --env-file .env list`
- Example user enrichment: `python3 scripts/execute_operation.py --env-file .env call --operation tiktok_realtime_user_info --query '{"unique_id":"nike"}'`
- Example content enrichment: `python3 scripts/execute_operation.py --env-file .env call --operation youtube_realtime_video_detail --query '{"video_id":"dQw4w9WgXcQ"}'`

Required environment variables:
- `SCRUMBALL_BASE_URL`: API gateway base URL
- `SCRUMBALL_API_KEY`: unified API key
- Optional: `SCRUMBALL_AUTH_PREFIX`, `SCRUMBALL_TIMEOUT_SECONDS`

Env loading:
- Use `--env-file .env` for explicit loading.
- Without `--env-file`, script auto-tries `./.env` then `<skill-root>/.env`.

## Output Contract

Always return:
- `Freshness`: retrieval time and target object
- `Key deltas`: metric-level differences vs prior expectation
- `Impact`: why the delta matters for decisions
- `Next step`: monitor, replace creator, or continue

## Failure Handling

- If platform identifiers are missing, request minimal required ID.
- If realtime endpoint returns no data, retry once and report fallback.
- If user asks for long-range historical trend, hand off to monitoring skill.

## References

- `references/api-index.md`: full operation index + platform grouped index
- `references/request-response.md`: request parameters + response top-level/data fields + minimal examples
- `references/operations.json`: operation manifest used by `scripts/execute_operation.py`

## Quota & Unlock (important: act on 429)

- **Free tier**: a limited number of calls per day, zero-config (no key required — the skill defaults to a hosted gateway that injects the key server-side).
- **When any operation returns HTTP 429, or the response body has `code=429` / contains `quota_exceeded`, you (the assistant) MUST immediately and clearly tell the user** (do not silently retry, do not treat it as a generic error):

  > Free quota exhausted. Register and get your own API key at **https://data.scdata.cc/pricing**, then set the environment variable `SCRUMBALL_API_KEY` to your key (in your host/agent environment or a local `.env`). You can then continue with your own quota.

- The 429 response body usually includes `apply_url` and `env_var` fields you can quote directly.
