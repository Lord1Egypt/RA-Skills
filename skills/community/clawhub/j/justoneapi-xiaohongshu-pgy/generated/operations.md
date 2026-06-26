# Xiaohongshu Creator Marketplace (Pugongying) operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

## `apiPgyKolDataCoreDataV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/pgy/kol/data/core_data/v1`
- Summary: Creator Core Metrics
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Core Metrics data, including engagement and content metrics, for benchmarking, vetting, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `business` | `query` | no | `string` | `DAILY_NOTE` | Business type.

Available Values:
- `DAILY_NOTE`: Daily notes
- `COOPERATE_NOTE`: Cooperative notes |
| enum | values | no | n/a | n/a | `DAILY_NOTE`, `COOPERATE_NOTE` |
| `noteType` | `query` | no | `string` | `PHOTO_TEXT_AND_VIDEO` | Type of note.

Available Values:
- `PHOTO_TEXT_AND_VIDEO`: Photo and Video
- `PHOTO_TEXT`: Photo and Text
- `VIDEO`: Video only |
| enum | values | no | n/a | n/a | `PHOTO_TEXT_AND_VIDEO`, `PHOTO_TEXT`, `VIDEO` |
| `dateType` | `query` | no | `string` | `DAY_30` | Time range for data.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `advertiseSwitch` | `query` | no | `string` | `ALL` | Advertisement filter.

Available Values:
- `ALL`: All notes
- `ORGANIC_ONLY`: Organic notes only |
| enum | values | no | n/a | n/a | `ALL`, `ORGANIC_ONLY` |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarCooperatorBloggerV2V1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/cooperator/blogger/v2/v1`
- Summary: Creator Search
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Search data, including filters, returning profile, and audience, for discovery, comparison, and shortlist building.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `searchType` | `query` | no | `string` | `NICKNAME` | Search criteria type.

Available Values:
- `NICKNAME`: Search by nickname
- `NOTE`: Search by note content |
| enum | values | no | n/a | n/a | `NICKNAME`, `NOTE` |
| `keyword` | `query` | no | `string` | n/a | Search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number. |
| `fansNumberLower` | `query` | no | `integer` | n/a | Minimum number of fans. |
| `fansNumberUpper` | `query` | no | `integer` | n/a | Maximum number of fans. |
| `fansAge` | `query` | no | `string` | `ALL` | Target fans age group.

Available Values:
- `ALL`: All ages
- `LT_18`: Under 18
- `AGE_18_24`: 18 to 24
- `AGE_25_34`: 25 to 34
- `AGE_35_44`: 35 to 44
- `GT_44`: Above 44 |
| enum | values | no | n/a | n/a | `ALL`, `LT_18`, `AGE_18_24`, `AGE_25_34`, `AGE_35_44`, `GT_44` |
| `fansGender` | `query` | no | `string` | `ALL` | Target fans gender.

Available Values:
- `ALL`: All genders
- `MALE_HIGH`: Mainly Male
- `FE_MALE_HIGH`: Mainly Female |
| enum | values | no | n/a | n/a | `ALL`, `MALE_HIGH`, `FE_MALE_HIGH` |
| `gender` | `query` | no | `string` | `ALL` | KOL's gender.

Available Values:
- `ALL`: All genders
- `MALE`: Male
- `FEMALE`: Female |
| enum | values | no | n/a | n/a | `ALL`, `MALE`, `FEMALE` |
| `contentTag` | `query` | no | `string` | n/a | Content categories, separated by commas. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarCooperatorUserBloggerUserIdV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/cooperator/user/blogger/userId/v1`
- Summary: Creator Profile
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | Blogger's user ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataUserIdFansOverallNewHistoryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1`
- Summary: Follower Growth History
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower Growth History data, including historical points, trend signals, and growth metrics, for trend tracking, audience analysis, and creator performance monitoring.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `dateType` | `query` | no | `string` | `DAY_30` | Time range for data.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `increaseType` | `query` | no | `string` | `FANS_TOTAL` | Type of growth data.

Available Values:
- `FANS_TOTAL`: Total fans
- `FANS_INCREASE`: New fans increase |
| enum | values | no | n/a | n/a | `FANS_TOTAL`, `FANS_INCREASE` |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataUserIdFansProfileV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_profile/v1`
- Summary: Follower Distribution
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower distribution data, including audience demographics, interests, and distribution metrics, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataV2CostEffectiveV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV2/costEffective/v1`
- Summary: Cost Effectiveness Analysis
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) cost Effectiveness Analysis data, including pricing, reach, and engagement efficiency indicators, for campaign evaluation.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataV2KolContentTagsV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV2/kolContentTags/v1`
- Summary: Creator Content Tags
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Content Tags data, including topic labels that describe publishing themes and content focus, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataV2KolFeatureTagsV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV2/kolFeatureTags/v1`
- Summary: Creator Feature Tags
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Feature Tags data, including platform tags, category labels, and classification signals, for segmentation, discovery, and creator classification.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataV2NotesDetailV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV2/notesDetail/v1`
- Summary: User Published Notes
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) user Published Notes data, including note metadata and engagement signals, for creator monitoring and campaign research.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `advertiseSwitch` | `query` | no | `string` | `ALL` | Advertisement filter.

Available Values:
- `ALL`: All notes
- `ORGANIC_ONLY`: Organic notes only |
| enum | values | no | n/a | n/a | `ALL`, `ORGANIC_ONLY` |
| `orderType` | `query` | no | `string` | `LATEST` | Sorting order.

Available Values:
- `LATEST`: Latest
- `MOST_READ`: Most read
- `MOST_INTERACT`: Most interactions |
| enum | values | no | n/a | n/a | `LATEST`, `MOST_READ`, `MOST_INTERACT` |
| `noteType` | `query` | no | `string` | `ALL` | Type of note.

Available Values:
- `ALL`: All types
- `COOPERATION`: Cooperation notes
- `PHOTO_TEXT`: Photo and Text
- `VIDEO`: Video only |
| enum | values | no | n/a | n/a | `ALL`, `COOPERATION`, `PHOTO_TEXT`, `VIDEO` |
| `isThirdPlatform` | `query` | no | `string` | `NO` | Whether from third-party platform.

Available Values:
- `NO`: No
- `YES`: Yes |
| enum | values | no | n/a | n/a | `NO`, `YES` |
| `pageNumber` | `query` | no | `integer` | `1` | Page number. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataV3DataSummaryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV3/dataSummary/v1`
- Summary: Data Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) Summary data, including activity, engagement, and audience growth, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `business` | `query` | no | `string` | `DAILY_NOTE` | Business type.

Available Values:
- `DAILY_NOTE`: Daily notes
- `COOPERATE_NOTE`: Cooperative notes |
| enum | values | no | n/a | n/a | `DAILY_NOTE`, `COOPERATE_NOTE` |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataV3FansSummaryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV3/fansSummary/v1`
- Summary: Follower Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower Summary data, including growth and engagement metrics, for audience analysis and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolDataV3NotesRateV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1`
- Summary: Note Performance Metrics
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `business` | `query` | no | `string` | `DAILY_NOTE` | Business type.

Available Values:
- `DAILY_NOTE`: Daily notes
- `COOPERATE_NOTE`: Cooperative notes |
| enum | values | no | n/a | n/a | `DAILY_NOTE`, `COOPERATE_NOTE` |
| `noteType` | `query` | no | `string` | `PHOTO_TEXT_AND_VIDEO` | Type of note.

Available Values:
- `PHOTO_TEXT_AND_VIDEO`: Photo and Video
- `PHOTO_TEXT`: Photo and Text
- `VIDEO`: Video only |
| enum | values | no | n/a | n/a | `PHOTO_TEXT_AND_VIDEO`, `PHOTO_TEXT`, `VIDEO` |
| `dateType` | `query` | no | `string` | `DAY_30` | Time range for data.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `advertiseSwitch` | `query` | no | `string` | `ALL` | Advertisement filter.

Available Values:
- `ALL`: All notes
- `ORGANIC_ONLY`: Organic notes only |
| enum | values | no | n/a | n/a | `ALL`, `ORGANIC_ONLY` |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarKolGetSimilarKolV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/get_similar_kol/v1`
- Summary: Similar Creators
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) similar Creators data, including audience signals, for creator discovery, benchmarking, and shortlist building.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `pageNum` | `query` | no | `integer` | `1` | Page number for results. |

### Request body

No request body.

### Responses

- `200`: OK

## `apiSolarNoteNoteIdDetailV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/note/noteId/detail/v1`
- Summary: Note Details
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note Details data, including media and engagement signals, for content analysis, archiving, and campaign review.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `noteId` | `query` | yes | `string` | n/a | Note's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolDataCoreV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-core-data/v1`
- Summary: Creator Core Metrics
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Core Metrics data, including engagement and content metrics, for benchmarking, vetting, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `business` | `query` | no | `string` | `_0` | Business type.

Available Values:
- `_0`: Normal notes
- `_1`: Cooperation notes |
| enum | values | no | n/a | n/a | `_0`, `_1` |
| `noteType` | `query` | no | `string` | `_3` | Note type.

Available Values:
- `_1`: Photo and Text
- `_2`: Video
- `_3`: Photo and Video |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `dateType` | `query` | no | `string` | `_1` | Date type.

Available Values:
- `_1`: Last 30 days
- `_2`: Last 90 days |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `adSwitch` | `query` | no | `string` | `_1` | Ad filter.

Available Values:
- `_1`: Full traffic (All notes)
- `_0`: Natural traffic (Organic notes) |
| enum | values | no | n/a | n/a | `_1`, `_0` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolCostEffectiveV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-cost-effective/v1`
- Summary: Cost Effectiveness Analysis
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) cost Effectiveness Analysis data, including pricing, reach, and engagement efficiency indicators, for campaign evaluation.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

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

## `getKolDataSummaryV2`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-data-summary/v2`
- Summary: Data Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) summary data, including activity, engagement, and audience growth, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `business` | `query` | yes | `string` | n/a | Business type.

Available Values:
- `_0`: Normal notes
- `_1`: Cooperation notes |
| enum | values | no | n/a | n/a | `_0`, `_1` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolFansPortraitV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-fans-portrait/v1`
- Summary: Follower Distribution
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower distribution data, including audience demographics, interests, and distribution metrics, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

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

## `getKolFansSummaryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-fans-summary/v1`
- Summary: Follower Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower summary data, including core metrics, trend signals, and performance indicators, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

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

## `getKolFansTrendV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-fans-trend/v1`
- Summary: Follower Growth History
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower growth history data, including historical audience changes over time, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `dateType` | `query` | yes | `string` | n/a | Date type.

Available Values:
- `_1`: Last 30 days
- `_2`: Last 60 days |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `increaseType` | `query` | yes | `string` | n/a | Increase type.

Available Values:
- `_1`: Total fans
- `_2`: New fans increase |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getXiaohongshuPgyKolInfoV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-info/v1`
- Summary: Creator Profile
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

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

## `getKolNoteListV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-note-list/v1`
- Summary: Creator Note List
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Note List data, including content metadata, publish time, and engagement indicators, for content analysis.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `page` | `query` | no | `integer` | `1` | Page number. |
| `adSwitch` | `query` | yes | `string` | n/a | Ad filter.

Available Values:
- `_1`: Full traffic (All notes)
- `_0`: Natural traffic (Organic notes) |
| enum | values | no | n/a | n/a | `_1`, `_0` |
| `orderType` | `query` | yes | `string` | n/a | Sorting order.

Available Values:
- `_1`: Latest
- `_2`: Most read
- `_3`: Most interactions |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `noteType` | `query` | no | `string` | `_4` | Note type.

Available Values:
- `_1`: Photo and Text notes
- `_2`: Video notes
- `_3`: Cooperation notes
- `_4`: All types |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3`, `_4` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKolNoteRateV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-note-rate/v1`
- Summary: Note Performance Metrics
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `dateType` | `query` | no | `string` | `_1` | Date type.

Available Values:
- `_1`: Last 30 days
- `_2`: Last 90 days |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `noteType` | `query` | no | `string` | `_3` | Note type.

Available Values:
- `_1`: Photo and Text
- `_2`: Video
- `_3`: Photo and Video |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `adSwitch` | `query` | no | `string` | `_1` | Ad filter.

Available Values:
- `_1`: Full traffic (All notes)
- `_0`: Natural traffic (Organic notes) |
| enum | values | no | n/a | n/a | `_1`, `_0` |
| `business` | `query` | no | `string` | `_0` | Business type.

Available Values:
- `_0`: Normal notes
- `_1`: Cooperation notes |
| enum | values | no | n/a | n/a | `_0`, `_1` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK

## `getXiaohongshuPgyNoteDetailV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-note-detail/v1`
- Summary: Note Details
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note Details data, including media and engagement signals, for content analysis, archiving, and campaign review.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `noteId` | `query` | yes | `string` | n/a | Note ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
