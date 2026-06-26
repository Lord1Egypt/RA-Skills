---
name: imou-device-config
description: >
  imou / Imou / 乐橙 / lechange 设备安防配置技能。支持设备动检计划、动检灵敏度、隐私模式（close camera）开关。
  Manages device channel security configuration: motion detection schedule, motion detection sensitivity, and privacy mode (close camera) enable/disable.
  For thing-model devices (productId non-empty), the skill prioritizes reading the product thing model and performs device configuration based on that model definition (properties, services).
  Use when: imou device config, Imou security config, lechange thing model, 乐橙 设备配置, 乐橙 动检计划, 乐橙 隐私模式, 乐橙 物模型 属性设置.
  Requires Imou developer account; set IMOU_APP_ID, IMOU_APP_SECRET, optional IMOU_BASE_URL.
metadata:
  openclaw:
    emoji: "⚙️"
    requires:
      env: ["IMOU_APP_ID", "IMOU_APP_SECRET", "IMOU_BASE_URL"]
      pip: ["requests"]
    primaryEnv: "IMOU_APP_ID"
    install:
      - id: "python-requests"
        kind: "pip"
        package: "requests"
        label: "Install requests"
---

# Imou Device Config（乐橙设备配置）

Manage device channel security configuration: motion detection plan, motion detection sensitivity, and privacy mode (close camera) enable/disable. Supports both PaaS devices (productId empty) and IoT thing-model devices (productId non-empty). **For thing-model devices, the skill prioritizes reading the product thing model and completes all device-related configuration based on that model definition** (Property get/set, Service invoke).

## Search Aliases

- imou
- Imou
- 乐橙
- lechange
- easy4ip
- imou-device-config
- 乐橙设备配置
- 乐橙动检计划
- 乐橙隐私模式
- 乐橙物模型

## Quick Start

Install dependency:
```bash
pip install requests
```

Set environment variables (required):
```bash
export IMOU_APP_ID="your_app_id"
export IMOU_APP_SECRET="your_app_secret"
export IMOU_BASE_URL="your_base_url"
```

**API Base URL (IMOU_BASE_URL)** (required; no default—must be set explicitly):
- **Mainland China**: Register a developer account at [open.imou.com](https://open.imou.com) and use the base URL below. Get `appId` and `appSecret` from [App Information](https://open.imou.com/consoleNew/myApp/appInfo).
- **Overseas**: Register a developer account at [open.imoulife.com](https://open.imoulife.com) and use the base URL for your data center (view in [Console - Basic Information - My Information](https://open.imoulife.com/consoleNew/basicInfo/myInfo)). Get `appId` and `appSecret` from [App Information](https://open.imoulife.com/consoleNew/myApp/appInfo). See [Development Specification](https://open.imoulife.com/book/http/develop.html).

| Region         | Data Center     | Base URL |
|----------------|-----------------|----------|
| Mainland China | —               | `https://openapi.lechange.cn` |
| Overseas       | East Asia       | `https://openapi-sg.easy4ip.com:443` |
| Overseas       | Central Europe  | `https://openapi-fk.easy4ip.com:443` |
| Overseas       | Western America | `https://openapi-or.easy4ip.com:443` |

Run (PaaS devices, productId empty):
```bash
# Get motion detection plan for a channel
python3 {baseDir}/scripts/device_config.py plan get DEVICE_SERIAL CHANNEL_ID

# Set motion detection plan (rules: period, beginTime, endTime)
python3 {baseDir}/scripts/device_config.py plan set DEVICE_SERIAL CHANNEL_ID --rules '[...]'

# Set motion detection sensitivity (1-5, 1=lowest, 5=highest)
python3 {baseDir}/scripts/device_config.py sensitivity set DEVICE_SERIAL CHANNEL_ID 3

# Get privacy mode (closeCamera) status
python3 {baseDir}/scripts/device_config.py privacy get DEVICE_SERIAL CHANNEL_ID

# Set privacy mode on/off
python3 {baseDir}/scripts/device_config.py privacy set DEVICE_SERIAL CHANNEL_ID on
python3 {baseDir}/scripts/device_config.py privacy set DEVICE_SERIAL CHANNEL_ID off
```

IoT thing-model devices (productId not empty) – **read product model first**, then configure by model:
```bash
# Step 1: Read product thing model (required; get Property/Service refs from model)
python3 {baseDir}/scripts/device_config.py iot model PRODUCT_ID [--verbose] [--json]

# Step 2: Property get/set and service invoke based on model definition
# Get Property values (refs from model)
python3 {baseDir}/scripts/device_config.py iot property-get PRODUCT_ID DEVICE_SERIAL '["3301","3302"]' [--json]

# Set Property values
python3 {baseDir}/scripts/device_config.py iot property-set PRODUCT_ID DEVICE_SERIAL '{"3301":1,"3302":2}'

# Invoke Service (event/command)
python3 {baseDir}/scripts/device_config.py iot service PRODUCT_ID DEVICE_SERIAL SERVICE_REF [--content '{}']
```

## Capabilities

1. **Motion detection plan**: Get or set alarm plan per channel (PaaS). Rules include period (Monday–Sunday), beginTime, endTime (HH:mm:ss).
2. **Motion detection sensitivity**: Set sensitivity level 1–5 for a channel (PaaS).
3. **Privacy mode**: Get or set closeCamera enable (privacy mode) per channel (PaaS).
4. **IoT thing-model**: For devices with productId: **read product thing model first**, then **property query** (get by refs from model), **property set** (set ref->value per model), **event/command** (invoke Service by ref from model, with input content per model). Configuration is driven by the thing model definition; refs and capabilities must be resolved from the model.

## Device Types and Configuration Strategy

- **productId empty (PaaS)**: Use enable APIs (`getDeviceCameraStatus` / `setDeviceCameraStatus`), `deviceAlarmPlan`, `modifyDeviceAlarmPlan`, `setDeviceAlarmSensitivity`. Only devices with `accessType=PaaS` support these.
- **productId not empty (thing-model device)**: **Prioritize reading the product thing model first** (`iot model PRODUCT_ID`). All device configuration (property query/set, event/command dispatch) is then performed **based on the thing model definition**: use Property refs and Service refs from the model for `iot property-get`, `iot property-set`, and `iot service`. Do not assume refs or capabilities; always resolve them from the product model.

## Request Header

All requests to Imou Open API must include the header `Client-Type: OpenClaw` for platform identification.

## API References

| API | Doc |
|-----|-----|
| Dev spec | https://open.imou.com/document/pages/c20750/ |
| Get accessToken | https://open.imou.com/document/pages/fef620/ |
| Enable definition | https://open.imou.com/document/pages/389c19/ |
| Set enable | https://open.imou.com/document/pages/8214a7/ |
| Get enable | https://open.imou.com/document/pages/2e535e/ |
| Get alarm plan | https://open.imou.com/document/pages/4d571d/ |
| Set alarm plan | https://open.imou.com/document/pages/542ccc/ |
| Set alarm sensitivity | https://open.imou.com/document/pages/83f1b4/ |
| IoT thing model overview | https://open.imou.com/document/pages/1acdf4/ |
| Get product model | https://open.imou.com/document/pages/2a238c/ |
| Get IoT Property | https://open.imou.com/document/pages/919bcf/ |
| Set IoT Property | https://open.imou.com/document/pages/532cdf/ |
| IoT Service | https://open.imou.com/document/pages/fa0726/ |

See `references/imou-config-api.md` for request/response formats.

## Tips

- **Token**: Fetched automatically per run; valid 3 days. Do not cache across runs unless you implement expiry handling.
- **Enable types**: Privacy mode uses `closeCamera` (channel scope). Motion enable uses `motionDetect` (channel). See enable definition doc for full list.
- **Alarm plan rules**: Each rule has `period` (e.g. "Monday" or "Monday,Wednesday,Friday"), `beginTime`, `endTime` (HH:mm:ss).
- **Thing-model first**: For productId non-empty devices, always read the product thing model first (`iot model PRODUCT_ID`); then use the model's Property/Service definitions (refs, dataTypes, inputData/outputData) for all get/set and service invoke. Do not hardcode refs across products.
- **IoT refs**: Property and Service refs are strings (e.g. "3301") from the model. For bool properties use 0/1 in set. Service `content` is input params by ref per model; use `{}` when the service has no input.

## Data Outflow

| Data | Sent to | Purpose |
|------|---------|--------|
| appId, appSecret | Imou Open API | Obtain accessToken |
| accessToken, deviceId, channelId, productId, etc. | Imou Open API | Get/set plan, sensitivity, enable; IoT model, property get/set, service invoke |

All requests go to the configured `IMOU_BASE_URL`. No other third parties.
