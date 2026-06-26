# Xiaohongshu Creator Marketplace (Pugongying) Creator Feature Tags operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/dataV2/kolFeatureTags`.

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
