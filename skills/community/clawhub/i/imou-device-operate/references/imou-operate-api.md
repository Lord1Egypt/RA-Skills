# Imou Open API Reference – Device Operate

This document summarizes the APIs used by the Imou Device Operate skill. All requests must include header `Client-Type: OpenClaw`.

---

## 1. Base URL and Request Format

- **Base URL**: `https://openapi.lechange.cn` (configurable via `IMOU_BASE_URL`).
- **Method**: POST to `{base_url}/openapi/{method}`.
- **Body**: JSON.

Request body structure:

```json
{
  "system": {
    "ver": "1.0",
    "appId": "<appId>",
    "sign": "<md5_sign>",
    "time": <utc_seconds>,
    "nonce": "<32_char_uuid>"
  },
  "id": "<request_unique_id>",
  "params": { ... }
}
```

**Sign**: MD5 of string `time:{time},nonce:{nonce},appSecret:{appSecret}` (UTF-8), 32-char lowercase hex. `time` is UTC timestamp in **seconds**.

Response structure:

```json
{
  "result": { "code": "0", "msg": "...", "data": { ... } },
  "id": "<request_id>"
}
```

`code` "0" means success. See [global return codes](https://open.imou.com/document/pages/254965/) for errors.

---

## 2. accessToken – Get Admin Token

- **Doc**: https://open.imou.com/document/pages/fef620/
- **URL**: `POST {base_url}/openapi/accessToken`
- **params**: `{}` (empty object).

**Response data**:

| Field         | Type   | Description                    |
|---------------|--------|--------------------------------|
| accessToken   | String | Admin access token            |
| expireTime    | Long   | Expiry time in **seconds**    |

Token is valid for 3 days. Request a new one when it expires or when API returns TK1002.

---

## 3. setDeviceSnapEnhanced – Device Snapshot (Enhanced)

- **Doc**: https://open.imou.com/document/pages/09fe83/
- **URL**: `POST {base_url}/openapi/setDeviceSnapEnhanced`

Supports snapshot frequency 1 per second. Client request interval should be ≥ 1s. Snapshot URL in response is valid for 2 hours.

**params**:

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| token     | String | Y        | accessToken |
| deviceId  | String | Y        | Device serial |
| channelId | String | Y        | Channel ID (e.g. "0") |

**Response data**:

| Field | Type   | Description        |
|-------|--------|--------------------|
| url   | String | Snapshot image URL (downloadable, 2h valid) |

---

## 4. controlMovePTZ – PTZ Move Control

- **Doc**: https://open.imou.com/document/pages/66c489/
- **URL**: `POST {base_url}/openapi/controlMovePTZ`

Device must have PT or PTZ capability.

**params**:

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| token     | String | Y        | accessToken |
| deviceId  | String | Y        | Device serial |
| channelId | String | Y        | Channel ID (e.g. "0") |
| operation | String | Y        | 0=up, 1=down, 2=left, 3=right, 4=up-left, 5=down-left, 6=up-right, 7=down-right, 8=zoom in, 9=zoom out, 10=stop |
| duration  | Long   | Y        | Move duration in **milliseconds** |

**Response**: `result.code` "0"; no `data` field.
