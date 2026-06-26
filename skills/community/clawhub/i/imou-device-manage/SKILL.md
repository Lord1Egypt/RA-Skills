---
name: imou-device-manage
description: >
  Imou/乐橙设备管理。支持查看账号设备列表、设备详情（序列号/型号/在离线/名称/通道）、按序列号查询、修改设备或通道名称。
  Use for requests in any language (e.g. 中文/English) about listing or managing Imou/乐橙 cloud devices.
  Use when: 我有哪些乐橙设备、乐橙设备列表、设备详情、修改设备或通道名称、query Imou devices、list Imou devices、get device by serial、rename device or channel.
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires": { "env": ["IMOU_APP_ID", "IMOU_APP_SECRET"], "pip": ["requests"] },
        "primaryEnv": "IMOU_APP_ID",
        "install":
          [
            { "id": "python-requests", "kind": "pip", "package": "requests", "label": "Install requests" }
          ]
      }
  }
---

# Imou Device Manage

List and manage Imou cloud devices: view device serial, model, online/offline status, device name, and channel info (channel ID, channel name); get details by device ID; rename device or channel.

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

Run:
```bash
# List all devices (paginated)
python3 {baseDir}/scripts/device_manage.py list

# List with page size and page number
python3 {baseDir}/scripts/device_manage.py list --page-size 20 --page 1

# Get details for specific device(s) by serial
python3 {baseDir}/scripts/device_manage.py get DEVICE_SERIAL1 [DEVICE_SERIAL2 ...]

# Rename device or channel
python3 {baseDir}/scripts/device_manage.py rename DEVICE_SERIAL "New Name" [--channel-id CHANNEL_ID]
```

## Capabilities

1. **List account devices**: Paginated list of devices under the account (serial, model, online/offline, device name, channel list with channel ID and channel name).
2. **Get device by serial**: Query one or more devices by serial number(s), returns full device and channel details.
3. **Rename device or channel**: Set custom device name (or channel name when `--channel-id` is provided).

## Request Header

All requests to Imou Open API include the header `Client-Type: OpenClaw` for platform identification.

## API References

| API | Doc |
|-----|-----|
| Dev spec | https://open.imou.com/document/pages/c20750/ |
| Get accessToken | https://open.imou.com/document/pages/fef620/ |
| List devices by page | https://open.imou.com/document/pages/683248/ |
| Get device by IDs | https://open.imou.com/document/pages/320fb7/ |
| Modify device/channel name | https://open.imou.com/document/pages/8ffaa3/ |

See `references/imou-device-api.md` for request/response formats.

## Tips

- **Token**: Fetched automatically per run; valid 3 days. Do not cache across runs unless you implement expiry handling.
- **Pagination**: Use `--page-size` (1–50) and `--page` (from 1) for `list`.
- **Rename**: Omit `--channel-id` to set device name; for single-channel IPC, device name and channel name may be updated together per API behavior.

## Data Outflow

| Data | Sent to | Purpose |
|------|---------|--------|
| appId, appSecret | Imou Open API | Obtain accessToken |
| accessToken, deviceId, etc. | Imou Open API | List/get device, modify name |

All requests go to the configured `IMOU_BASE_URL` (Imou official API). No other third parties.
