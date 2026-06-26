# Imou Open API Reference – Device Config (Security)

This document summarizes the APIs used by the Imou Device Config skill. All requests must include header `Client-Type: OpenClaw`.

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

`code` "0" means success.

---

## 2. accessToken – Get Admin Token

- **Doc**: https://open.imou.com/document/pages/fef620/
- **URL**: `POST {base_url}/openapi/accessToken`
- **params**: `{}`

**Response data**: `accessToken`, `expireTime` (seconds). Token valid 3 days.

---

## 3. Enable Definition (device capability switches)

- **Doc**: https://open.imou.com/document/pages/389c19/

Relevant for this skill:

| enableType    | Description     | Scope   |
|---------------|-----------------|---------|
| closeCamera   | Privacy mode    | channel |
| motionDetect  | Motion detect   | channel |

Scope: device / channel / all. Use channelId when scope is channel.

---

## 4. getDeviceCameraStatus – Get Enable Status

- **Doc**: https://open.imou.com/document/pages/2e535e/
- **URL**: `POST {base_url}/openapi/getDeviceCameraStatus`

**params**:

| Param      | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| token      | String | Y        | accessToken                          |
| deviceId   | String | Y        | Device serial                        |
| channelId  | String | Y        | Channel ID (required for channel scope) |
| enableType | String | Y        | e.g. closeCamera, motionDetect (lowercase) |

**Response data**: `status` (on/off), `enableType`. Only for accessType=PaaS devices.

---

## 5. setDeviceCameraStatus – Set Enable Status

- **Doc**: https://open.imou.com/document/pages/8214a7/
- **URL**: `POST {base_url}/openapi/setDeviceCameraStatus`

**params**:

| Param      | Type    | Required | Description                          |
|------------|---------|----------|--------------------------------------|
| token      | String  | Y        | accessToken                          |
| deviceId   | String  | Y        | Device serial                        |
| channelId  | String  | N        | Omit for device-level; required for channel-level |
| enableType | String  | Y        | e.g. closeCamera, motionDetect      |
| enable     | Boolean | Y        | true = on, false = off               |

**Response**: result.code "0", no data.

---

## 6. deviceAlarmPlan – Get Motion Detection Plan

- **Doc**: https://open.imou.com/document/pages/4d571d/
- **URL**: `POST {base_url}/openapi/deviceAlarmPlan`

**params**:

| Param     | Type   | Required | Description   |
|-----------|--------|----------|---------------|
| token     | String | Y        | accessToken   |
| deviceId  | String | Y        | Device serial |
| channelId | String | Y        | Channel ID    |

**Response data**: `channelId`, `rules` (array). Each rule: `enable` (Boolean), `beginTime`, `endTime` (HH:mm:ss), `period` (e.g. Monday, Tuesday, …).

---

## 7. modifyDeviceAlarmPlan – Set Motion Detection Plan

- **Doc**: https://open.imou.com/document/pages/542ccc/
- **URL**: `POST {base_url}/openapi/modifyDeviceAlarmPlan`

**params**:

| Param     | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| token     | String | Y        | accessToken                                      |
| deviceId  | String | Y        | Device serial                                    |
| channelId | String | Y        | Channel ID                                       |
| rules     | Array  | Y        | Each item: period, beginTime, endTime (HH:mm:ss). period: Monday–Sunday or "Monday,Wednesday,Friday" |

**Response**: result.code "0", no data.

---

## 8. setDeviceAlarmSensitivity – Set Motion Detection Sensitivity

- **Doc**: https://open.imou.com/document/pages/83f1b4/
- **URL**: `POST {base_url}/openapi/setDeviceAlarmSensitivity`

**params**:

| Param     | Type    | Required | Description        |
|-----------|---------|----------|--------------------|
| token     | String  | Y        | accessToken        |
| deviceId  | String  | Y        | Device serial      |
| channelId | String  | Y        | Channel ID         |
| sensitive | Integer | Y        | 1–5 (1=lowest, 5=highest) |

**Response**: result.code "0", no data.

---

## 9. IoT Thing-Model APIs (productId not empty)

For devices with productId, use thing model APIs for property query/set and event (service) invoke.

### 9.1 getProductModel – Get Product Thing Model

- **Doc**: https://open.imou.com/document/pages/2a238c/
- **URL**: `POST {base_url}/openapi/getProductModel`

**params**:

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| token     | String | Y        | accessToken |
| productId | String | Y        | From listDeviceDetailsByPage/ByIds response |

**Response data**: Full thing model (schema, profile, properties, services, events). Each property has `ref`, `identifier`, `name`, `dataType`; each service has `ref`, `identifier`, `name`, `inputData`/`outputData`. Use refs in get/set Property and iotDeviceControl.

### 9.2 getIotDeviceProperties – Get Property Values

- **Doc**: https://open.imou.com/document/pages/919bcf/
- **URL**: `POST {base_url}/openapi/getIotDeviceProperties`

**params**:

| Param      | Type   | Required | Description |
|------------|--------|----------|-------------|
| token      | String | Y        | accessToken |
| productId  | String | Y        | Product ID  |
| deviceId   | String | Y        | Device serial |
| properties | Array  | Y        | Property ref strings, e.g. ["3301","3302"] |

**Response data**: `productId`, `deviceId`, `name`, `properties` (ref -> value), `status` (online/offline).

### 9.3 setIotDeviceProperties – Set Property Values

- **Doc**: https://open.imou.com/document/pages/532cdf/
- **URL**: `POST {base_url}/openapi/setIotDeviceProperties`

**params**:

| Param      | Type   | Required | Description |
|------------|--------|----------|-------------|
| token      | String | Y        | accessToken |
| productId  | String | Y        | Product ID  |
| deviceId   | String | Y        | Device serial |
| properties | Object | Y        | ref -> value, e.g. {"3301":1,"3302":2}. bool as 0/1. |

**Response**: result.code "0", no data.

### 9.4 iotDeviceControl – Invoke Service (Event/Command)

- **Doc**: https://open.imou.com/document/pages/fa0726/
- **URL**: `POST {base_url}/openapi/iotDeviceControl`

**params**:

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| token     | String | Y        | accessToken |
| productId | String | Y        | Product ID  |
| deviceId  | String | Y        | Device serial |
| ref       | String | Y        | Service ref from thing model |
| content   | Object | Y        | Input params ref -> value; {} if no input |

**Response data**: `content` with `outputData`, `service` etc. per thing model.

Motion / privacy for IoT devices are defined in the product thing model (Property or Service). Resolve refs from getProductModel then use get/set Property or iotDeviceControl as needed.
