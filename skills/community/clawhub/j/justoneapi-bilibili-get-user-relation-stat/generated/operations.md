# Bilibili User Relation Stats operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `get-user-relation-stat`.

## `getUserRelationStat`

- Method: `GET`
- Path: `/api/bilibili/get-user-relation-stat/v1`
- Summary: User Relation Stats
- Description: Get Bilibili user Relation Stats data, including following counts, for creator benchmarking and audience growth tracking.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `wmid` | `query` | yes | `string` | n/a | Bilibili User ID (WMID). |

### Request body

No request body.

### Responses

- `200`: OK
