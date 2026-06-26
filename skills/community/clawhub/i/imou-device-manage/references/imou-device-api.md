# Imou Open API Reference – Device Management

This document summarizes the APIs used by the Imou Device Manage skill. All requests must include header `Client-Type: OpenClaw`.

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

## 3. listDeviceDetailsByPage – Paginated Device List

- **Doc**: https://open.imou.com/document/pages/683248/
- **URL**: `POST {base_url}/openapi/listDeviceDetailsByPage`

**params**:

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| token     | String | Y        | accessToken |
| pageSize  | int    | Y        | 1–50        |
| page      | long   | Y        | Page index, from 1 |
| source    | String | N        | `bind` \| `share` \| `bindAndShare` (default) |

**Response data**:

| Field       | Type   | Description        |
|-------------|--------|--------------------|
| count       | int    | Device count       |
| deviceList  | Array  | List of devices    |

Each device includes: `deviceId`, `deviceName`, `deviceModel`, `deviceStatus` (online/offline/sleep/upgrading), `channelList` (each with `channelId`, `channelName`, `channelStatus`), etc.

---

## 4. listDeviceDetailsByIds – Get Devices by Serial(s)

- **Doc**: https://open.imou.com/document/pages/320fb7/
- **URL**: `POST {base_url}/openapi/listDeviceDetailsByIds`

**params**:

| Param      | Type  | Required | Description |
|------------|------|----------|-------------|
| token      | String | Y      | accessToken |
| deviceList | Array  | Y      | Each item: `{ "deviceId": "<serial>" }` or `{ "deviceId": "<serial>", "channelId": ["0", ...] }`. `channelId` is optional; omit to return all channels. |

**Response data**: Same shape as listDeviceDetailsByPage (`count`, `deviceList`).

---

## 5. modifyDeviceName – Rename Device or Channel

- **Doc**: https://open.imou.com/document/pages/8ffaa3/
- **URL**: `POST {base_url}/openapi/modifyDeviceName`

**params**:

| Param      | Type   | Required | Description |
|------------|--------|----------|-------------|
| token      | String | Y        | accessToken |
| deviceId   | String | Y        | Device serial |
| name       | String | Y        | New name (max 64 chars) |
| channelId  | String | N        | Channel ID; empty = set device name (for single-channel IPC, channel name may be updated too) |
| productId  | String | N        | Optional in API; **must be included when device info exists** (e.g. from listDeviceDetailsByPage/listDeviceDetailsByIds) and the device has productId. Required when renaming a sub-device. |
| subDeviceId| String | N        | Required when renaming a sub-device |

**Implementation rule**: When the caller has device data (e.g. from a prior list or get), `productId` must be sent if present on the device object.

**Response**: `result.code` "0", no `data` field.
