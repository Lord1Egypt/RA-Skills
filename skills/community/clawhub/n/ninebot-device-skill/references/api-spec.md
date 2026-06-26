# Ninebot Vehicle Query – API Assumptions (PLACEHOLDER)

> ⚠️ This file is a **placeholder** API spec for development. Replace with real endpoints/fields once available.

## Base URL

```
https://cn-cbu-gateway.ninebot.com
```

## Auth (API Key)

- 使用 Ninebot device service API key（环境变量 `NINEBOT_DEVICESERVICE_KEY` 或 config.json）
- 默认请求头：`Authorization: Bearer <API_KEY>`（可在 config 中改 header/prefix）

### 1) Device List (AI)
- **Method:** GET
- **Path:** `/ai-skill/api/device/info/get-device-list`
- **Params:** 无
- **Response JSON (example):**
```json
{
  "code": 1,
  "desc": "成功",
  "data": [
    {"sn": "SN123", "deviceName": "九号M5", "img": "..."},
    {"sn": "SN456", "deviceName": "", "img": "..."}
  ],
  "t": 1773140131339
}
```

**Devices path:** `data`  
**Device fields:** `sn`, `deviceName`

### 3) Device Dynamic Info (AI)
- **Method:** POST
- **Path:** `/ai-skill/api/device/info/get-device-dynamic-info`
- **Params (JSON):**
  - `sn` (device sn)
- **Response JSON (example):**
```json
{
  "code": 1,
  "desc": "Successfully",
  "data": {
    "dumpEnergy": 57,
    "estimateMileage": 50.4,
    "locationInfo": {"locationDesc": "北京市海淀区东升(地区)镇后屯东路"},
    "chargingState": 0,
    "powerStatus": 1,
    "remainChargeTime": "5分钟",
    "wnumber": "4MDAZ2606J0012"
  },
  "t": 1773131267279
}
```

**Battery path:** `data.dumpEnergy`  
**Status path:** `data.powerStatus`  
**Location path:** `data.locationInfo.locationDesc`

---

## Config Mapping (for scripts/ninebot_query.py)

You can override any field via a JSON config file. See `config.example.json` for a ready-to-copy template:

```json
{
  "base_url": "https://cn-cbu-gateway.ninebot.com",
  "apiKey": "your_ninebot_device_service_key_here",
  "auth": {
    "api_key_header": "Authorization",
    "api_key_prefix": "Bearer "
  },
  "devices": {
    "method": "GET",
    "path": "/ai-skill/api/device/info/get-device-list",
    "payload": {},
    "list_path": "data",
    "sn_field": "sn",
    "name_field": "deviceName"
  },
  "device_info": {
    "method": "POST",
    "path": "/ai-skill/api/device/info/get-device-dynamic-info",
    "payload": {"sn": "{sn}"},
    "battery_path": "data.dumpEnergy",
    "status_path": "data.powerStatus",
    "location_path": "data.locationInfo.locationDesc",
    "extra_fields": {
      "estimateMileage": "data.estimateMileage",
      "chargingState": "data.chargingState",
      "remainChargeTime": "data.remainChargeTime",
    }
  }
}
```
