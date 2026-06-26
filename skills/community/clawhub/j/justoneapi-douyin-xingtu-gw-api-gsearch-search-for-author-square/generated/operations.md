# Douyin Creator Marketplace (Xingtu) Creator Search operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/gsearch/search_for_author_square`.

## `gwApiGsearchSearchForAuthorSquareV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/gsearch/search_for_author_square/v1`
- Summary: Creator Search
- Description: Get Douyin Creator Marketplace (Xingtu) creator Search data, including filters, returning profile, and audience, for discovery, comparison, and shortlist building.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `keyword` | `query` | no | `string` | n/a | Search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |
| `searchType` | `query` | no | `string` | `NICKNAME` | Search criteria type.

Available Values:
- `NICKNAME`: By Nickname
- `CONTENT`: By Content |
| enum | values | no | n/a | n/a | `NICKNAME`, `CONTENT` |
| `followerRange` | `query` | no | `string` | n/a | Follower range (e.g., 10-100). |
| `kolPriceType` | `query` | no | `string` | n/a | KOL price type.

Available Values:
- `视频1_20s`: Video 1-20s
- `视频21_60s`: Video 21-60s
- `视频60s以上`: Video > 60s
- `定制短剧单集`: Mini-drama episode
- `千次自然播放量`: CPM naturally
- `短直种草视频`: Short-live seeding video
- `短直预热视频`: Short-live warm-up video
- `短直明星种草`: Celebrity short-live seeding
- `短直明星预热`: Celebrity short-live warm-up
- `明星视频`: Celebrity video
- `合集视频`: Collection video
- `抖音短视频共创_主投稿达人`: Douyin short video co-creation - main creator
- `抖音短视频共创_参与达人`: Douyin short video co-creation - participant |
| enum | values | no | n/a | n/a | `视频1_20s`, `视频21_60s`, `视频60s以上`, `定制短剧单集`, `千次自然播放量`, `短直种草视频`, `短直预热视频`, `短直明星种草`, `短直明星预热`, `明星视频`, `合集视频`, `抖音短视频共创_主投稿达人`, `抖音短视频共创_参与达人` |
| `kolPriceRange` | `query` | no | `string` | n/a | KOL price range (e.g., 10000-50000). |
| `contentTag` | `query` | no | `string` | n/a | Content tag filter. |

### Request body

No request body.

### Responses

- `200`: OK
