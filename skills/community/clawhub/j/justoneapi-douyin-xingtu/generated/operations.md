# Douyin Creator Marketplace (Xingtu) operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

## `getAuthorCommerceSeedingBaseInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-commerce-seed-base-info/v1`
- Summary: Author Commerce Seeding Base Info
- Description: Get Douyin Creator Marketplace (Xingtu) author Commerce Seeding Base Info data, including baseline metrics, commercial signals, and seeding indicators, for product seeding analysis, creator vetting, and campaign planning.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `range` | `query` | yes | `string` | n/a | Time range. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getAuthorCommerceSpreadInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-commerce-spread-info/v1`
- Summary: Author Commerce Spread Info
- Description: Get Douyin Creator Marketplace (Xingtu) author Commerce Spread Info data, including spread metrics, for creator evaluation for campaign planning and media buying.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getAuthorContentHotKeywordsV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-content-hot-keywords/v1`
- Summary: KOL Content Keyword Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Content Keyword Analysis data, including core metrics, trend signals, and performance indicators, for content theme analysis and creator positioning research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `keywordType` | `query` | no | `string` | `0` | Type of keywords. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getAuthorHotCommentTokensV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-hot-comment-tokens/v1`
- Summary: KOL Comment Keyword Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Comment Keyword Analysis data, including core metrics, trend signals, and performance indicators, for audience language analysis and comment-topic research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolAudienceDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-audience-distribution/v1`
- Summary: Audience Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) audience Distribution data, including demographic and interest-based audience segmentation, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolConvertAbilityV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-convert-ability/v1`
- Summary: Conversion Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Analysis data, including conversion efficiency and commercial performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `range` | `query` | yes | `string` | n/a | Time range.

Available Values:
- `_1`: Last 7 days
- `_2`: Last 30 days
- `_3`: Last 90 days |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolConvertVideosOrProductsV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-convert-videos-or-products/v1`
- Summary: Conversion Resources
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `detailType` | `query` | yes | `string` | n/a | Resource type.

Available Values:
- `_1`: Video Data
- `_2`: Product Data |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `page` | `query` | yes | `integer` | n/a | Page number. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolCpInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-cp-info/v1`
- Summary: Cost Performance Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) cost Performance Analysis data, including pricing, exposure, and engagement efficiency indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolDailyFansV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-daily-fans/v1`
- Summary: Follower Growth Trend
- Description: Get Douyin Creator Marketplace (Xingtu) follower Growth Trend data, including historical audience changes over time, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `startDate` | `query` | yes | `string` | n/a | Start Date (yyyy-MM-dd). |
| `endDate` | `query` | yes | `string` | n/a | End Date (yyyy-MM-dd). |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolFansDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-fans-distribution/v1`
- Summary: Follower Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) follower distribution data, including audience demographics, interests, and distribution metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `fansType` | `query` | no | `string` | `_1` | Fans type.

Available Values:
- `_1`: Fans Portrait
- `_2`: Fans Group Portrait
- `_5`: Iron Fans Portrait |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_5` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getDouyinXingtuKolInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-info/v1`
- Summary: Creator Profile
- Description: Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `platformChannel` | `query` | no | `string` | `_1` | Platform channel.

Available Values:
- `_1`: Short Video
- `_10`: Live Streaming |
| enum | values | no | n/a | n/a | `_1`, `_10` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolLinkInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-link-info/v1`
- Summary: Creator Link Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) creator Link Metrics data, including creator ranking, traffic structure, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `industryTag` | `query` | no | `string` | n/a | Industry Tag. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolLinkStructV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-link-struct/v1`
- Summary: Creator Link Structure
- Description: Get Douyin Creator Marketplace (Xingtu) creator Link Structure data, including engagement and conversion metrics, for creator performance analysis.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolMarketingInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-marketing-info/v1`
- Summary: Marketing Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) marketing metrics data, including rate card details and commercial service metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `platformChannel` | `query` | no | `string` | `_1` | Platform channel.

Available Values:
- `_1`: Short Video
- `_10`: Live Streaming |
| enum | values | no | n/a | n/a | `_1`, `_10` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolRecVideosV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-rec-videos/v1`
- Summary: Recommended Videos
- Description: Get Douyin Creator Marketplace (Xingtu) recommended videos data, including video performance metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolShowItemsV2V1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-show-items-v2/v1`
- Summary: Showcase Items
- Description: Get Douyin Creator Marketplace (Xingtu) showcase items data, including core metrics, trend signals, and performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `onlyAssign` | `query` | no | `boolean` | `false` | Whether true is Xingtu video, false is personal video. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolSpreadInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-spread-info/v1`
- Summary: Spread Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) spread metrics data, including audience, content performance, and commercial indicators, for quick evaluation.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `type` | `query` | no | `string` | `_1` | Spread info type.

Available Values:
- `_1`: Personal Video
- `_2`: Xingtu Video |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `range` | `query` | no | `string` | `_2` | Time range.

Available Values:
- `_2`: Last 30 days
- `_3`: Last 90 days |
| enum | values | no | n/a | n/a | `_2`, `_3` |
| `flowType` | `query` | no | `string` | `1` | Flow type. |
| `onlyAssign` | `query` | no | `boolean` | `false` | Only assigned notes. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolTouchDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-touch-distribution/v1`
- Summary: Audience Touchpoint Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) audience touchpoint distribution data, including segment breakdowns, audience composition, and distribution signals, for traffic analysis and existing integration compatibility.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getDouyinXingtuVideoDetailV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-video-detail/v1`
- Summary: Video Details
- Description: Get Douyin Creator Marketplace (Xingtu) video Details data, including performance fields from the legacy Douyin Xingtu endpoint, for content review and integration compatibility.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `detailId` | `query` | yes | `string` | n/a | Video detail ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiAggregatorGetAuthorCommerceSeedBaseInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/aggregator/get_author_commerce_seed_base_info/v1`
- Summary: Author Commerce Seeding Base Info
- Description: Get Douyin Creator Marketplace (Xingtu) author Commerce Seeding Base Info data, including baseline metrics, commercial signals, and seeding indicators, for product seeding analysis, creator vetting, and campaign planning.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `range` | `query` | no | `string` | `DAY_90` | Time range.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiAggregatorGetAuthorCommerceSpreadInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/aggregator/get_author_commerce_spread_info/v1`
- Summary: Author Commerce Spread Info
- Description: Get Douyin Creator Marketplace (Xingtu) author Commerce Spread Info data, including spread metrics, for creator evaluation for campaign planning and media buying.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiAggregatorGetAuthorOrderExperienceV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1`
- Summary: Creator Order Experience
- Description: Get Douyin Creator Marketplace (Xingtu) creator Order Experience data, including commercial history and transaction-related indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `period` | `query` | no | `string` | `DAY_30` | Time period.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiAuthorGetAuthorBaseInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/author/get_author_base_info/v1`
- Summary: Creator Profile
- Description: Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiAuthorGetAuthorMarketingInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/author/get_author_marketing_info/v1`
- Summary: Marketing Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) marketing metrics data, including rate card details and commercial service metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiAuthorGetAuthorPlatformChannelInfoV2V1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/author/get_author_platform_channel_info_v2/v1`
- Summary: Creator Channel Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) creator Channel Metrics data, including platform distribution and channel performance data used, for creator evaluation.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiAuthorGetAuthorShowItemsV2V1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/author/get_author_show_items_v2/v1`
- Summary: Showcase Items
- Description: Get Douyin Creator Marketplace (Xingtu) showcase Items data, including products and videos associated with the account, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |
| `onlyAssign` | `query` | no | `boolean` | `false` | Whether to only include assigned items. |
| `flowType` | `query` | no | `string` | `EXCLUDE` | Flow type filter.

Available Values:
- `EXCLUDE`: Exclude
- `INCLUDE`: Include |
| enum | values | no | n/a | n/a | `EXCLUDE`, `INCLUDE` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpAuthorAudienceDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1`
- Summary: Audience Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) audience Distribution data, including demographic and interest-based audience segmentation, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |
| `linkType` | `query` | no | `string` | `CONNECTED` | Link type filter.

Available Values:
- `CONNECTED`: Connected
- `AWARE`: Aware
- `INTERESTED`: Interested
- `LIKE`: Like
- `FOLLOW`: Follow |
| enum | values | no | n/a | n/a | `CONNECTED`, `AWARE`, `INTERESTED`, `LIKE`, `FOLLOW` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpAuthorCpInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_cp_info/v1`
- Summary: Cost Performance Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) cost Performance Analysis data, including pricing, exposure, and engagement efficiency indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpAuthorLinkStructV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_link_struct/v1`
- Summary: Creator Link Structure
- Description: Get Douyin Creator Marketplace (Xingtu) creator Link Structure data, including engagement and conversion metrics, for creator performance analysis.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpAuthorRecVideosV2V1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_rec_videos_v2/v1`
- Summary: Recommended Videos
- Description: Get Douyin Creator Marketplace (Xingtu) recommended Videos data, including content references used, for creator evaluation.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpAuthorTouchDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_touch_distribution/v1`
- Summary: Audience Touchpoint Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) audience Touchpoint Distribution data, including segment breakdowns, audience composition, and distribution signals, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpAuthorVideoDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_video_distribution/v1`
- Summary: Video Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) video Distribution data, including content performance breakdowns across published videos, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpCheckAuthorDisplayV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/check_author_display/v1`
- Summary: Creator Visibility Status
- Description: Get Douyin Creator Marketplace (Xingtu) creator Visibility Status data, including availability status, discovery eligibility, and campaign display signals, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpGetAuthorConvertAbilityV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_convert_ability/v1`
- Summary: Conversion Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Analysis data, including conversion efficiency and commercial performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |
| `range` | `query` | no | `string` | `DAY_30` | Time range.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpGetAuthorConvertVideosOrProductsV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1`
- Summary: Conversion Resources
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |
| `industryId` | `query` | no | `string` | `ALL` | Industry category.

Available Values:
- `ALL`: All
- `ELECTRONICS_AND_APPLIANCES`: Electronics and Appliances
- `FOOD_AND_BEVERAGE`: Food and Beverage
- `CLOTHING_AND_ACCESSORIES`: Clothing and Accessories
- `HEALTHCARE_AND_MEDICAL`: Healthcare and Medical
- `BUSINESS_SERVICES`: Business Services
- `LOCAL_SERVICES`: Local Services
- `REAL_ESTATE`: Real Estate
- `HOME_AND_BUILDING_MATERIALS`: Home and Building Materials
- `EDUCATION_AND_TRAINING`: Education and Training
- `TRAVEL_AND_TOURISM`: Travel and Tourism
- `PUBLIC_SERVICES`: Public Services
- `GAMES`: Games
- `RETAIL`: Retail
- `TRANSPORTATION_EQUIPMENT`: Transportation Equipment
- `AUTOMOTIVE`: Automotive
- `AGRICULTURE_FORESTRY_FISHERY`: Agriculture Forestry Fishery
- `CHEMICAL_AND_ENERGY`: Chemical and Energy
- `ELECTRONICS_AND_ELECTRICAL`: Electronics and Electrical
- `MACHINERY_EQUIPMENT`: Machinery Equipment
- `CULTURE_SPORTS_ENTERTAINMENT`: Culture Sports Entertainment
- `MEDIA_AND_INFORMATION`: Media and Information
- `LOGISTICS`: Logistics
- `TELECOMMUNICATIONS`: Telecommunications
- `FINANCIAL_SERVICES`: Financial Services
- `CATERING_SERVICES`: Catering Services
- `SOFTWARE_TOOLS`: Software Tools
- `FRANCHISING_AND_INVESTMENT`: Franchising and Investment
- `BEAUTY_AND_COSMETICS`: Beauty and Cosmetics
- `MOTHER_BABY_AND_PET`: Mother Baby and Pet
- `DAILY_CHEMICALS`: Daily Chemicals
- `PHYSICAL_BOOKS`: Physical Books
- `SOCIAL_AND_COMMUNICATION`: Social and Communication
- `MEDICAL_INSTITUTIONS`: Medical Institutions |
| enum | values | no | n/a | n/a | `ALL`, `ELECTRONICS_AND_APPLIANCES`, `FOOD_AND_BEVERAGE`, `CLOTHING_AND_ACCESSORIES`, `HEALTHCARE_AND_MEDICAL`, `BUSINESS_SERVICES`, `LOCAL_SERVICES`, `REAL_ESTATE`, `HOME_AND_BUILDING_MATERIALS`, `EDUCATION_AND_TRAINING`, `TRAVEL_AND_TOURISM`, `PUBLIC_SERVICES`, `GAMES`, `RETAIL`, `TRANSPORTATION_EQUIPMENT`, `AUTOMOTIVE`, `AGRICULTURE_FORESTRY_FISHERY`, `CHEMICAL_AND_ENERGY`, `ELECTRONICS_AND_ELECTRICAL`, `MACHINERY_EQUIPMENT`, `CULTURE_SPORTS_ENTERTAINMENT`, `MEDIA_AND_INFORMATION`, `LOGISTICS`, `TELECOMMUNICATIONS`, `FINANCIAL_SERVICES`, `CATERING_SERVICES`, `SOFTWARE_TOOLS`, `FRANCHISING_AND_INVESTMENT`, `BEAUTY_AND_COSMETICS`, `MOTHER_BABY_AND_PET`, `DAILY_CHEMICALS`, `PHYSICAL_BOOKS`, `SOCIAL_AND_COMMUNICATION`, `MEDICAL_INSTITUTIONS` |
| `range` | `query` | no | `string` | `DAY_30` | Time range.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `detailType` | `query` | no | `string` | `VIDEO` | Resource type.

Available Values:
- `VIDEO`: Video
- `PRODUCT`: Product |
| enum | values | no | n/a | n/a | `VIDEO`, `PRODUCT` |
| `page` | `query` | no | `integer` | `1` | Page number. |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpGetAuthorDailyFansV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_daily_fans/v1`
- Summary: Follower Growth Trend
- Description: Get Douyin Creator Marketplace (Xingtu) follower Growth Trend data, including historical audience changes over time, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `startDate` | `query` | yes | `string` | n/a | Start Date (yyyy-MM-dd). |
| `endDate` | `query` | yes | `string` | n/a | End Date (yyyy-MM-dd). |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpGetAuthorFansDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_fans_distribution/v1`
- Summary: Follower Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) follower Distribution data, including audience segmentation and location and demographic breakdowns, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `authorType` | `query` | no | `string` | `FAN` | Author type filter.

Available Values:
- `FAN`: Fan
- `DIE_HARD_FAN`: Die Hard Fan |
| enum | values | no | n/a | n/a | `FAN`, `DIE_HARD_FAN` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpGetAuthorLinkInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_link_info/v1`
- Summary: Creator Link Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) creator Link Metrics data, including creator ranking, traffic structure, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |
| `industryTag` | `query` | no | `string` | `ALL` | Industry tag.

Available Values:
- `ALL`: All
- `ELECTRONICS_AND_APPLIANCES`: Electronics and Appliances
- `FOOD_AND_BEVERAGE`: Food and Beverage
- `CLOTHING_AND_ACCESSORIES`: Clothing and Accessories
- `HEALTHCARE_AND_MEDICAL`: Healthcare and Medical
- `BUSINESS_SERVICES`: Business Services
- `LOCAL_SERVICES`: Local Services
- `REAL_ESTATE`: Real Estate
- `HOME_AND_BUILDING_MATERIALS`: Home and Building Materials
- `EDUCATION_AND_TRAINING`: Education and Training
- `TRAVEL_AND_TOURISM`: Travel and Tourism
- `PUBLIC_SERVICES`: Public Services
- `GAMES`: Games
- `RETAIL`: Retail
- `TRANSPORTATION_EQUIPMENT`: Transportation Equipment
- `AUTOMOTIVE`: Automotive
- `AGRICULTURE_FORESTRY_FISHERY`: Agriculture Forestry Fishery
- `CHEMICAL_AND_ENERGY`: Chemical and Energy
- `ELECTRONICS_AND_ELECTRICAL`: Electronics and Electrical
- `MACHINERY_EQUIPMENT`: Machinery Equipment
- `CULTURE_SPORTS_ENTERTAINMENT`: Culture Sports Entertainment
- `MEDIA_AND_INFORMATION`: Media and Information
- `LOGISTICS`: Logistics
- `TELECOMMUNICATIONS`: Telecommunications
- `FINANCIAL_SERVICES`: Financial Services
- `CATERING_SERVICES`: Catering Services
- `SOFTWARE_TOOLS`: Software Tools
- `FRANCHISING_AND_INVESTMENT`: Franchising and Investment
- `BEAUTY_AND_COSMETICS`: Beauty and Cosmetics
- `MOTHER_BABY_AND_PET`: Mother Baby and Pet
- `DAILY_CHEMICALS`: Daily Chemicals
- `PHYSICAL_BOOKS`: Physical Books
- `SOCIAL_AND_COMMUNICATION`: Social and Communication
- `MEDICAL_INSTITUTIONS`: Medical Institutions |
| enum | values | no | n/a | n/a | `ALL`, `ELECTRONICS_AND_APPLIANCES`, `FOOD_AND_BEVERAGE`, `CLOTHING_AND_ACCESSORIES`, `HEALTHCARE_AND_MEDICAL`, `BUSINESS_SERVICES`, `LOCAL_SERVICES`, `REAL_ESTATE`, `HOME_AND_BUILDING_MATERIALS`, `EDUCATION_AND_TRAINING`, `TRAVEL_AND_TOURISM`, `PUBLIC_SERVICES`, `GAMES`, `RETAIL`, `TRANSPORTATION_EQUIPMENT`, `AUTOMOTIVE`, `AGRICULTURE_FORESTRY_FISHERY`, `CHEMICAL_AND_ENERGY`, `ELECTRONICS_AND_ELECTRICAL`, `MACHINERY_EQUIPMENT`, `CULTURE_SPORTS_ENTERTAINMENT`, `MEDIA_AND_INFORMATION`, `LOGISTICS`, `TELECOMMUNICATIONS`, `FINANCIAL_SERVICES`, `CATERING_SERVICES`, `SOFTWARE_TOOLS`, `FRANCHISING_AND_INVESTMENT`, `BEAUTY_AND_COSMETICS`, `MOTHER_BABY_AND_PET`, `DAILY_CHEMICALS`, `PHYSICAL_BOOKS`, `SOCIAL_AND_COMMUNICATION`, `MEDICAL_INSTITUTIONS` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpGetAuthorSpreadInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_spread_info/v1`
- Summary: Spread Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) spread metrics data, including exposure, spread, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |
| `range` | `query` | no | `string` | `DAY_30` | Time range.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `type` | `query` | no | `string` | `PERSONAL_VIDEO` | Video type.

Available Values:
- `PERSONAL_VIDEO`: Personal video
- `XINTU_VIDEO`: Xingtu video |
| enum | values | no | n/a | n/a | `PERSONAL_VIDEO`, `XINTU_VIDEO` |
| `onlyAssign` | `query` | no | `boolean` | `false` | Whether to only include assigned videos. |
| `flowType` | `query` | no | `string` | `EXCLUDE` | Flow type filter.

Available Values:
- `EXCLUDE`: Exclude
- `INCLUDE`: Include |
| enum | values | no | n/a | n/a | `EXCLUDE`, `INCLUDE` |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpItemReportDetailV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1`
- Summary: Item Report Details
- Description: Get Douyin Creator Marketplace (Xingtu) item Report Details data, including key metrics and report fields used, for item performance analysis.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `itemId` | `query` | yes | `string` | n/a | Item's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpItemReportThAnalysisV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/item_report_th_analysis/v1`
- Summary: Item Report Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) item Report Analysis data, including performance interpretation, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `itemId` | `query` | yes | `string` | n/a | Item's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataSpItemReportTrendV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/item_report_trend/v1`
- Summary: Item Report Trends
- Description: Get Douyin Creator Marketplace (Xingtu) item Report Trend data, including time-based changes in item performance metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `itemId` | `query` | yes | `string` | n/a | Item's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiDataGetAuthorHotCommentTokensV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data/get_author_hot_comment_tokens/v1`
- Summary: KOL Comment Keyword Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Comment Keyword Analysis data, including core metrics, trend signals, and performance indicators, for audience language analysis and comment-topic research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `gwApiGauthorGetAuthorContentHotKeywordsV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1`
- Summary: KOL Content Keyword Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Content Keyword Analysis data, including core metrics, trend signals, and performance indicators, for content theme analysis and creator positioning research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK

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

## `searchKolSimpleV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/search-kol-simple/v1`
- Summary: KOL Keyword Search
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Keyword Search data, including matching creators and discovery data, for creator sourcing and shortlist building.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `keyword` | `query` | yes | `string` | n/a | Search keywords. |
| `platformSource` | `query` | yes | `string` | n/a | Platform source.

Available Values:
- `_1`: Douyin
- `_2`: Toutiao
- `_3`: Xigua |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `page` | `query` | yes | `integer` | n/a | Page number. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
