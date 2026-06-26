# Imou Open API Reference – Device Video

This document summarizes the APIs used by the Imou Device Video skill. All requests must include header `Client-Type: OpenClaw`.

---

## 1. Base URL and Request Format

- **Base URL**: `https://openapi.lechange.cn` (configurable via `IMOU_BASE_URL`).
- **Method**: POST to `{base_url}/openapi/{method}`.
- **Body**: JSON. Same structure as device-manage: `system` (ver, appId, sign, time, nonce), `id`, `params`.
- **Sign**: MD5 of `time:{time},nonce:{nonce},appSecret:{appSecret}` (UTF-8), 32-char lowercase hex.

Response: `result.code` "0" means success. If `bindDeviceLive` returns code **LV1001** (live address already exists), use `liveList` to get the existing HLS URL for the device/channel/streamId.

---

## 2. accessToken – Get Admin Token

- **Doc**: https://open.imou.com/document/pages/fef620/
- **params**: `{}`.
- **Response data**: `accessToken`, `expireTime` (seconds). Token valid 3 days.

---

## 3. bindDeviceLive – Create Device Live Source

- **Doc**: https://open.imou.com/document/pages/1bc396/
- **URL**: `POST {base_url}/openapi/bindDeviceLive`

**params**:

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| token     | String | Y        | accessToken |
| deviceId  | String | Y        | Device serial |
| channelId | String | Y        | Channel ID (e.g. "0") |
| streamId  | int    | Y        | 0: main stream, 1: sub stream |
| liveMode  | String | N        | "proxy" or omit |

**Response data**: `liveToken`, `liveStatus`, `liveType`, `deviceId`, `channelId`, `coverUpdate`, `streams` (array of `{ hls`, `coverUrl`, `streamId }`), `job`. If code is **LV1001**, live already exists—use liveList to get the HLS URL.

---

## 4. liveList – Get Live List

- **Doc**: https://open.imou.com/document/pages/b0e047/
- **URL**: `POST {base_url}/openapi/liveList`

**params**:

| Param      | Type   | Required | Description |
|------------|--------|----------|-------------|
| token      | String | Y        | accessToken |
| queryRange | String | Y        | Range "1-N", N positive (e.g. "1-100") |

**Response data**: `count`, `lives` (array). Each item: `liveToken`, `liveStatus`, `liveType`, `deviceId`, `channelId`, `coverUpdate`, `streams` (array of `{ hls`, `coverUrl`, `streamId }`), `job`, etc. Match by deviceId, channelId, streamId to get existing HLS.

---

## 5. createDeviceRecordHls – Create Record Playback HLS URL

- **Doc**: https://open.imou.com/document/pages/185646/
- **URL**: `POST {base_url}/openapi/createDeviceRecordHls`

**params**:

| Param      | Type   | Required | Description |
|------------|--------|----------|-------------|
| token      | String | Y        | accessToken |
| deviceId   | String | Y        | Device serial |
| channelId  | String | Y        | Channel ID |
| streamId   | int    | N        | 0 main, 1 sub; default main |
| beginTime  | String | Y        | yyyy-MM-dd HH:mm:ss (no cross-day) |
| endTime    | String | Y        | yyyy-MM-dd HH:mm:ss |
| recordType | String | Y        | localRecord \| cloudRecord |

**Response data**: `url` (HLS URL). URL has limited validity; use soon after obtaining.

---

## 6. queryLocalRecords – Query Local Record Clips

- **Doc**: https://open.imou.com/document/pages/396dce/
- **URL**: `POST {base_url}/openapi/queryLocalRecords`

**params**:

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| token     | String | Y        | accessToken |
| deviceId  | String | Y        | Device serial |
| channelId | String | Y        | Channel ID |
| beginTime | String | Y        | yyyy-MM-dd HH:mm:ss |
| endTime   | String | Y        | yyyy-MM-dd HH:mm:ss |
| type      | String | N        | "All" for all types |
| count     | int    | Y        | Max 100 per request (some devices limit to 32) |

**Response data**: `records` (array). Each: `recordId`, `fileLength`, `channelID`, `beginTime`, `endTime`, `type`, `streamType`. Paginate by using last record’s endTime + 1s as next beginTime.

---

## 7. queryCloudRecords – Query Cloud Record Clips

- **Doc**: https://open.imou.com/document/pages/8e0e35/
- **URL**: `POST {base_url}/openapi/queryCloudRecords`

**params**:

| Param      | Type   | Required | Description |
|------------|--------|----------|-------------|
| token      | String | Y        | accessToken |
| deviceId   | String | Y        | Device serial |
| channelId  | String | Y        | Channel ID |
| beginTime  | String | Y        | yyyy-MM-dd HH:mm:ss |
| endTime    | String | Y        | yyyy-MM-dd HH:mm:ss |
| queryRange | String | Y        | "1-N", N max 100 |

**Response data**: `records` (array). Each: `recordId`, `deviceId`, `channelId`, `beginTime`, `endTime`, `size`, `thumbUrl`, `encryptMode`, `recordRegionId`. Paginate by using last record’s endTime as next beginTime.
