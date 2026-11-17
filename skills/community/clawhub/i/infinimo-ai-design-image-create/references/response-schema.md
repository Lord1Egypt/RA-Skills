# AI Image Generation — Response Schema

## Common envelope

| Field | Type | Description |
|-------|------|-------------|
| status | integer | `1` = success, `0` = failure |
| code | integer | Business code; success usually `200`; `2001` = invalid Token; `2002` = insufficient credits |
| msg | string | Message |
| data | object | Payload |
| pointInfo | object | Credits `{ type, point }` |

---

## GET /aigc/ec_media/image/create/dic

### ImageCreateDic (data)

| Field | Type | Description |
|-------|------|-------------|
| models | array | Model list |
| sizes | array | Resolution list |
| ratios | array | Aspect ratio list |

### TypeRespString (models / sizes / ratios items)

| Field | Type | Description |
|-------|------|-------------|
| id | string | Option id for submit |
| title | string | Display name |

### models optional fields (web UI)

| Field | Type | Description |
|-------|------|-------------|
| point | number | Credits per image |
| level | integer | Required membership tier |
| levelText | string | Tier label |

---

## POST /upload/image

### Upload response data

| Field | Type | Description |
|-------|------|-------------|
| url | string | Full image URL (preferred) |
| path | string | Relative path; prepend Base URL |

---

## POST /aigc/ec_media/image/create

### Request body ImageCreateParam

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | yes | Prompt |
| model | string | no | Model id |
| ratio | string | no | Ratio id |
| size | string | no | Size id |
| images | string[] | no | Reference image URLs |

### Response data

On success, `data` is usually `{}`; fetch outputs from logs.

---

## GET /aigc/ec_media/image/create/logs

### PageListImageResultV2 (data)

| Field | Type | Description |
|-------|------|-------------|
| count | integer | Total count |
| more | integer | `1` = has more, `0` = none |
| start | integer | Next page index |
| items | array | Record list |

### ImageResultV2 (items)

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Record id |
| urls | string[] | Output URLs; empty while pending |
| fail | boolean | `true` on failure |
| param | ImageCreateParam | Original submit params |
| time | string | Created at |

### param (ImageCreateParam)

| Field | Description |
|-------|-------------|
| prompt | Prompt |
| model | Model id |
| ratio | Ratio id |
| size | Size id |
| images | Reference URL array |

---

## GET /aigc/ec_media/image/log/delete

| Parameter | Description |
|-----------|-------------|
| id | Record id to delete |

Success: `status: 1`.

---

## WebSocket (optional)

- URL: `wss://www.clawec.com/api/aigc/socket`
- After connect: `{"type":"login","id":"<TOKEN>"}`
- On `{"type":"image_result_refresh"}` → re-fetch logs
