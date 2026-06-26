# Xiaohongshu Creator Marketplace (Pugongying) Creator Search operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/cooperator/blogger/v2`.

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
