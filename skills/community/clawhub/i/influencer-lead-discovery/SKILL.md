---
name: influencer-lead-discovery
description: "Find influencers and creators across TikTok, Instagram, and YouTube by keyword; expand similar creators, enrich profiles, and build outreach-ready lead lists. Influencer search, creator discovery, KOL sourcing."
---

# Influencer Lead Discovery

Build decision-ready creator shortlists across TikTok, Instagram, and YouTube with explicit operation-level mapping.

## Capability Matrix

### YouTube

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 搜索youtube用户 | `search_youtube_user` | `POST /api/v1/search/youtube/user` | `body.query` |
| 搜索youtube视频 | `search_youtube_video` | `POST /api/v1/search/youtube/video` | `body.query` |
| 合作品牌 | `youtube_user_brands` | `GET /api/v1/youtube/user/brands` | `query.channel_id` |
| 用户top10 hashtag互动数据 | `youtube_user_hashtag_engagement` | `GET /api/v1/youtube/user/hashtag/engagement` | `query.channel_id` |
| 用户信息 | `youtube_db_user_info` | `GET /api/v1/youtube/user/info` | `query.anyOf(channel_id,username)` |
| 相似用户推荐 | `youtube_user_similar` | `GET /api/v1/youtube/user/similar` | `query.anyOf(channel_id,channel_handle)` |
| 用户视频 | `youtube_db_user_videos` | `GET /api/v1/youtube/user/videos` | `query.channel_id` |

### TikTok

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 搜索tiktok用户 | `search_tiktok_user` | `POST /api/v1/search/tiktok/user` | `body.query` |
| 搜索tiktok视频 | `search_tiktok_video` | `POST /api/v1/search/tiktok/video` | `body.query` |
| 合作品牌 | `tiktok_user_brands` | `GET /api/v1/tiktok/user/brands` | `query.unique_id` |
| 用户top10 hashtag互动数据 | `tiktok_user_hashtag_engagement` | `GET /api/v1/tiktok/user/hashtag/engagement` | `query.unique_id` |
| 用户信息 | `tiktok_db_user_info` | `GET /api/v1/tiktok/user/info` | `query.unique_id` |
| 相似用户推荐 | `tiktok_user_similar` | `GET /api/v1/tiktok/user/similar` | `query.unique_id` |
| 用户视频 | `tiktok_db_user_videos` | `GET /api/v1/tiktok/user/videos` | `query.unique_id` |

### Instagram

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 合作品牌 | `instagram_user_brands` | `GET /api/v1/instagram/user/brands` | `query.username` |
| 用户top10 hashtag互动数据 | `instagram_user_hashtag_engagement` | `GET /api/v1/instagram/user/hashtag/engagement` | `query.username` |
| 用户信息 | `instagram_db_user_info` | `GET /api/v1/instagram/user/info` | `query.username` |
| 用户贴文 | `instagram_db_user_medias` | `GET /api/v1/instagram/user/medias` | `query.username` |
| 相似用户推荐 | `instagram_user_similar` | `GET /api/v1/instagram/user/similar` | `query.username` |
| 搜索instagram帖文 | `search_instagram_media` | `POST /api/v1/search/instagram/media` | `body.query` |
| 搜索instagram用户 | `search_instagram_user` | `POST /api/v1/search/instagram/user` | `body.query` |

### Cross-platform

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| ping | `ping` | `GET /api/ping` | `none` |
| 搜索联想 | `search_instagram_suggest` | `POST /api/v1/search/suggest` | `query.platform, query.query` |

## Quick Start

1. Confirm campaign objective, target market, and primary platform.
2. Use the Capability Matrix to choose operationIds by platform and task.
3. Check `references/request-response.md` for required params and response field layout.
4. Run `scripts/execute_operation.py` calls and rank candidates with evidence.

## Workflow

1. Build candidate pools first (`search_*`) and expand pagination for coverage.
2. Enrich shortlisted creators (`*_db_user_info`, `*_db_user_videos`/`*_db_user_medias`, `*_user_similar`).
3. Add partnership relevance signals (`*_user_brands`, `*_user_hashtag_engagement`) before ranking.
4. Return a shortlist with explicit reasons, risks, and next actions.

## Tooling

Execution commands:
- List operations: `python3 scripts/execute_operation.py --env-file .env list`
- Filter by tag: `python3 scripts/execute_operation.py --env-file .env list --tag search`
- Example search: `python3 scripts/execute_operation.py --env-file .env call --operation search_tiktok_user --body '{"query":"nike","page":1,"page_size":10}'`
- Example enrich: `python3 scripts/execute_operation.py --env-file .env call --operation tiktok_db_user_info --query '{"unique_id":"nike"}'`

Required environment variables:
- `SCRUMBALL_BASE_URL`: API gateway base URL
- `SCRUMBALL_API_KEY`: unified API key
- Optional: `SCRUMBALL_AUTH_PREFIX`, `SCRUMBALL_TIMEOUT_SECONDS`

Env loading:
- Use `--env-file .env` for explicit loading.
- Without `--env-file`, script auto-tries `./.env` then `<skill-root>/.env`.

## Output Contract

Always return:
- `Top candidates`: ordered list with platform + identifier
- `Why selected`: 2-3 evidence points per candidate
- `Risks`: data gaps or quality caveats
- `Next step`: outreach/testing recommendation

## Failure Handling

- If required IDs are missing, request only minimal fields from the user.
- If no results, relax one filter at a time and report what changed.
- If API fails, include failed `operationId` and retry guidance.

## References

- `references/api-index.md`: full operation index + platform grouped index
- `references/request-response.md`: request parameters + response top-level/data fields + minimal examples
- `references/operations.json`: operation manifest used by `scripts/execute_operation.py`

## Quota & Unlock (important: act on 429)

- **Free tier**: a limited number of calls per day, zero-config (no key required — the skill defaults to a hosted gateway that injects the key server-side).
- **When any operation returns HTTP 429, or the response body has `code=429` / contains `quota_exceeded`, you (the assistant) MUST immediately and clearly tell the user** (do not silently retry, do not treat it as a generic error):

  > Free quota exhausted. Register and get your own API key at **https://data.scdata.cc/pricing**, then set the environment variable `SCRUMBALL_API_KEY` to your key (in your host/agent environment or a local `.env`). You can then continue with your own quota.

- The 429 response body usually includes `apply_url` and `env_var` fields you can quote directly.
