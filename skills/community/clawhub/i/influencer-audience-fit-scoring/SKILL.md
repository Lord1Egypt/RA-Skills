---
name: influencer-audience-fit-scoring
description: "Pre-campaign audience quality and follower authenticity (fake-follower detection) analysis across TikTok, Instagram, and YouTube: geography, language, age, gender, interests; compare creators. Audience analysis, fake followers, creator vetting."
---

# Influencer Audience Fit Scoring

Evaluate whether a creator's audience matches campaign targeting with transparent dimension-by-dimension scoring.

## Capability Matrix

### YouTube

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 年龄(age) | `audience_youtube_age` | `GET /api/v1/audience/youtube/age` | `query.channel_id` |
| 营销路径(brand opportunities) | `audience_youtube_brand_opportunities` | `GET /api/v1/audience/youtube/brand_opportunities` | `query.channel_id` |
| 社交人格(content style) | `audience_youtube_content_style` | `GET /api/v1/audience/youtube/content_style` | `query.channel_id` |
| 粉丝真实性(follower authenticity) | `audience_youtube_follower_authenticity` | `GET /api/v1/audience/youtube/follower_authenticity` | `query.channel_id` |
| 性别(gender) | `audience_youtube_gender` | `GET /api/v1/audience/youtube/gender` | `query.channel_id` |
| 整体性别(gender overall) | `audience_youtube_gender_overall` | `GET /api/v1/audience/youtube/gender_overall` | `query.channel_id` |
| 地理位置(geography) | `audience_youtube_geography` | `GET /api/v1/audience/youtube/geography` | `query.channel_id` |
| 互动行为(interactive behavior) | `audience_youtube_interactive_behavior` | `GET /api/v1/audience/youtube/interactive_behavior` | `query.channel_id` |
| 兴趣(interest) | `audience_youtube_interest` | `GET /api/v1/audience/youtube/interest` | `query.channel_id` |
| 语言(language) | `audience_youtube_language` | `GET /api/v1/audience/youtube/language` | `query.channel_id` |
| 评级等级(rating tier) | `audience_youtube_rating_tier` | `GET /api/v1/audience/youtube/rating_tier` | `query.channel_id` |

### TikTok

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 年龄(age) | `audience_tiktok_age` | `GET /api/v1/audience/tiktok/age` | `query.unique_id` |
| 营销路径(brand opportunities) | `audience_tiktok_brand_opportunities` | `GET /api/v1/audience/tiktok/brand_opportunities` | `query.unique_id` |
| 社交人格(content style) | `audience_tiktok_content_style` | `GET /api/v1/audience/tiktok/content_style` | `query.unique_id` |
| 设备占比(device) | `audience_tiktok_device` | `GET /api/v1/audience/tiktok/device` | `query.unique_id` |
| 粉丝真实性(follower authenticity) | `audience_tiktok_follower_authenticity` | `GET /api/v1/audience/tiktok/follower_authenticity` | `query.unique_id` |
| 性别(gender) | `audience_tiktok_gender` | `GET /api/v1/audience/tiktok/gender` | `query.unique_id` |
| 整体性别(gender overall) | `audience_tiktok_gender_overall` | `GET /api/v1/audience/tiktok/gender_overall` | `query.unique_id` |
| 地理位置(geography) | `audience_tiktok_geography` | `GET /api/v1/audience/tiktok/geography` | `query.unique_id` |
| 互动行为(interactive behavior) | `audience_tiktok_interactive_behavior` | `GET /api/v1/audience/tiktok/interactive_behavior` | `query.unique_id` |
| 兴趣(interest) | `audience_tiktok_interest` | `GET /api/v1/audience/tiktok/interest` | `query.unique_id` |
| 语言(language) | `audience_tiktok_language` | `GET /api/v1/audience/tiktok/language` | `query.unique_id` |
| 评级等级(rating tier) | `audience_tiktok_rating_tier` | `GET /api/v1/audience/tiktok/rating_tier` | `query.unique_id` |

### Instagram

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 年龄(age) | `audience_instagram_age` | `GET /api/v1/audience/instagram/age` | `query.username` |
| 营销路径(brand opportunities) | `audience_instagram_brand_opportunities` | `GET /api/v1/audience/instagram/brand_opportunities` | `query.username` |
| 社交人格(content style) | `audience_instagram_content_style` | `GET /api/v1/audience/instagram/content_style` | `query.username` |
| 设备占比(device) | `audience_instagram_device` | `GET /api/v1/audience/instagram/device` | `query.username` |
| 粉丝真实性(follower authenticity) | `audience_instagram_follower_authenticity` | `GET /api/v1/audience/instagram/follower_authenticity` | `query.username` |
| 性别(gender) | `audience_instagram_gender` | `GET /api/v1/audience/instagram/gender` | `query.username` |
| 整体性别(gender overall) | `audience_instagram_gender_overall` | `GET /api/v1/audience/instagram/gender_overall` | `query.username` |
| 地理位置(geography) | `audience_instagram_geography` | `GET /api/v1/audience/instagram/geography` | `query.username` |
| 互动行为(interactive behavior) | `audience_instagram_interactive_behavior` | `GET /api/v1/audience/instagram/interactive_behavior` | `query.username` |
| 兴趣(interest) | `audience_instagram_interest` | `GET /api/v1/audience/instagram/interest` | `query.username` |
| 语言(language) | `audience_instagram_language` | `GET /api/v1/audience/instagram/language` | `query.username` |
| 评级等级(rating tier) | `audience_instagram_rating_tier` | `GET /api/v1/audience/instagram/rating_tier` | `query.username` |

### Cross-platform

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| `none` | `none` | `none` | `none` |

## Quick Start

1. Define ICP constraints (region, age, gender, interest, language, authenticity threshold).
2. Select platform and creator identifier (`unique_id`, `username`, `channel_id`).
3. Use Capability Matrix to pull required audience dimensions by platform.
4. Score fit and confidence separately; return go/test/no-go decision.

## Workflow

1. Build target profile with hard filters and soft weights.
2. Fetch audience dimensions (geography/language/age/gender/interest/behavior/authenticity/rating tier).
3. Compute weighted fit score and independent data-confidence score.
4. Compare candidates on same platform and explain strongest/weakest dimensions.

## Tooling

Execution commands:
- List operations: `python3 scripts/execute_operation.py --env-file .env list`
- Example interest call: `python3 scripts/execute_operation.py --env-file .env call --operation audience_tiktok_interest --query '{"unique_id":"nike"}'`
- Example language call: `python3 scripts/execute_operation.py --env-file .env call --operation audience_youtube_language --query '{"channel_id":"UC_x5XG1OV2P6uZZ5FSM9Ttw"}'`

Required environment variables:
- `SCRUMBALL_BASE_URL`: API gateway base URL
- `SCRUMBALL_API_KEY`: unified API key
- Optional: `SCRUMBALL_AUTH_PREFIX`, `SCRUMBALL_TIMEOUT_SECONDS`

Env loading:
- Use `--env-file .env` for explicit loading.
- Without `--env-file`, script auto-tries `./.env` then `<skill-root>/.env`.

## Output Contract

Always return:
- `Fit score`: numeric score and confidence
- `Score breakdown`: geography/language/age/gender/interest/authenticity
- `Decision`: go / test / no-go
- `Action`: what to validate next

## Failure Handling

- If target profile is vague, ask for ICP before scoring.
- If one dimension is missing, continue scoring and lower confidence.
- If cross-platform comparison is requested, warn about comparability limits.

## References

- `references/api-index.md`: full operation index + platform grouped index
- `references/request-response.md`: request parameters + response top-level/data fields + minimal examples
- `references/operations.json`: operation manifest used by `scripts/execute_operation.py`

## Quota & Unlock (important: act on 429)

- **Free tier**: a limited number of calls per day, zero-config (no key required — the skill defaults to a hosted gateway that injects the key server-side).
- **When any operation returns HTTP 429, or the response body has `code=429` / contains `quota_exceeded`, you (the assistant) MUST immediately and clearly tell the user** (do not silently retry, do not treat it as a generic error):

  > Free quota exhausted. Register and get your own API key at **https://data.scdata.cc/pricing**, then set the environment variable `SCRUMBALL_API_KEY` to your key (in your host/agent environment or a local `.env`). You can then continue with your own quota.

- The 429 response body usually includes `apply_url` and `env_var` fields you can quote directly.
