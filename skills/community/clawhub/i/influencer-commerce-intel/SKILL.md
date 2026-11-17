---
name: influencer-commerce-intel
description: "TikTok Shop product selection and creator commerce intelligence: sales and GMV data, goods/live/video-ad monetization signals, product details, creator commerce potential. Product research, TikTok e-commerce."
---

# Influencer Commerce Intel

Analyze creator commerce performance and monetization potential with direct mapping to commerce endpoints.

## Capability Matrix

### YouTube

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| `none` | `none` | `none` | `none` |

### TikTok

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| 实时采集-商品详情 | `tiktok_realtime_product_detail` | `GET /api/v1/tiktok/realtime/product/detail` | `query.product_id, query.region` |
| 用户带货商品列表 | `tiktok_user_shop_goods_list` | `GET /api/v1/tiktok/user/shop/goods/list` | `query.unique_id` |
| 用户带货直播列表 | `tiktok_user_shop_live_list` | `GET /api/v1/tiktok/user/shop/live/list` | `query.unique_id` |
| 用户带货数据 | `tiktok_user_shop_sale` | `GET /api/v1/tiktok/user/shop/sale` | `query.unique_id` |
| 用户带货视频广告列表 | `tiktok_user_shop_video_ad_list` | `GET /api/v1/tiktok/user/shop/video/ad/list` | `query.unique_id` |

### Instagram

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| `none` | `none` | `none` | `none` |

### Cross-platform

| Capability | operationId | Interface | Minimum input |
|---|---|---|---|
| `none` | `none` | `none` | `none` |

## Quick Start

1. Confirm commerce objective (GMV growth, product seeding, ad ROI).
2. Use the Capability Matrix to pick commerce operationIds.
3. Validate required query/body fields in `references/request-response.md`.
4. Run calls and summarize opportunity + risk + pilot plan.

## Workflow

1. Build a commerce snapshot first (`tiktok_user_shop_sale`, goods/live/ad lists).
2. Deep dive top products with `tiktok_realtime_product_detail` when needed.
3. Evaluate conversion consistency, category fit, and monetization durability.
4. Return recommendation with expected KPI and test scope.

## Tooling

Execution commands:
- List operations: `python3 scripts/execute_operation.py --env-file .env list`
- Sale snapshot: `python3 scripts/execute_operation.py --env-file .env call --operation tiktok_user_shop_sale --query '{"unique_id":"nike"}'`
- Goods list: `python3 scripts/execute_operation.py --env-file .env call --operation tiktok_user_shop_goods_list --query '{"unique_id":"nike","page":1,"page_size":20}'`

Required environment variables:
- `SCRUMBALL_BASE_URL`: API gateway base URL
- `SCRUMBALL_API_KEY`: unified API key
- Optional: `SCRUMBALL_AUTH_PREFIX`, `SCRUMBALL_TIMEOUT_SECONDS`

Env loading:
- Use `--env-file .env` for explicit loading.
- Without `--env-file`, script auto-tries `./.env` then `<skill-root>/.env`.

## Output Contract

Always return:
- `Commerce summary`: top performance signals
- `Opportunity`: product/category/content opportunity
- `Risk`: instability, low signal confidence, or limited sample
- `Next step`: pilot recommendation and expected KPI

## Failure Handling

- If identifiers are incomplete, request `unique_id` first.
- If one commerce dimension is missing, continue with available dimensions and reduce confidence.
- If user asks broad creator discovery, hand off to lead-discovery skill.

## References

- `references/api-index.md`: full operation index + platform grouped index
- `references/request-response.md`: request parameters + response top-level/data fields + minimal examples
- `references/operations.json`: operation manifest used by `scripts/execute_operation.py`

## Quota & Unlock (important: act on 429)

- **Free tier**: a limited number of calls per day, zero-config (no key required — the skill defaults to a hosted gateway that injects the key server-side).
- **When any operation returns HTTP 429, or the response body has `code=429` / contains `quota_exceeded`, you (the assistant) MUST immediately and clearly tell the user** (do not silently retry, do not treat it as a generic error):

  > Free quota exhausted. Register and get your own API key at **https://data.scdata.cc/pricing**, then set the environment variable `SCRUMBALL_API_KEY` to your key (in your host/agent environment or a local `.env`). You can then continue with your own quota.

- The 429 response body usually includes `apply_url` and `env_var` fields you can quote directly.
