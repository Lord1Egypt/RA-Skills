# Douban Movie Subject Details operations

Generated from JustOneAPI OpenAPI for platform key `douban`.

Endpoint group: `get-subject-detail`.

## `getSubjectDetailV1`

- Method: `GET`
- Path: `/api/douban/get-subject-detail/v1`
- Summary: Subject Details
- Description: Get Douban subject Details data, including title, rating, and cast, for title enrichment and catalog research.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `subjectId` | `query` | yes | `string` | n/a | The unique ID for a movie or TV subject on Douban. |

### Request body

No request body.

### Responses

- `200`: OK
