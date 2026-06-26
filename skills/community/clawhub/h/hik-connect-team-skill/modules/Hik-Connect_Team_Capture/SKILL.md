---
name: hctopen-capture
description: |
  HCTOpen device capture and decryption skill. Supports capture for specified device channel, and provides encrypted image decryption functionality. The returned capture address is cloud address instead of local address, can be accessed directly.
  Use when: Need to get device real-time image or decrypt encrypted device image.
  
  ⚠️ Security Requirement: Must set environment variables: Hik-Connect Team OpenAPI AppKey, Hik-Connect Team OpenAPI SecretKey. (API Domain is automatically obtained from token response)

parameters:
  - name: device-serial
    type: string
    description: "Device serial number"
    required: true
  - name: channel-no
    type: string
    description: "Channel number, default is 1"
    default: "1"

responses:
  - success: true
    template: "Preview image generated for you, click link below to view:"
    media: "image_card"

metadata:
  openclaw:
    emoji: "📸"
    requires:
      env: ["HIK_CONNECT_TEAM_OPENAPI_APP_KEY", "HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY"]
      pip: ["requests", "pycryptodome", "Pillow"]
    primaryEnv: "HIK_CONNECT_TEAM_OPENAPI_APP_KEY"
    warnings:
      - "May read ~/.openclaw/*.json for credentials (env vars have priority)"
    config:
      configFileRead:
        paths:
          - "~/.openclaw/config.json"
          - "~/.openclaw/gateway/config.json"
          - "~/.openclaw/channels.json"
        priority: "lower than environment variables"
        description: "Reads Hik-Connect Team credentials from OpenClaw config files as fallback"
---

# HCTOpen Capture

HCT is short for Hik-Connect for Teams, meaning Hik-Connect Team mode.
HCTOpen is short for Hik-Connect for Teams OpenAPI.

This Skill provides device real-time capture functionality, suitable for anomaly verification, real-time screen preview and other scenarios.

> **Note!!!**: This skill only provides capture capability. If device has stream encryption enabled causing image not viewable, user needs to manually decrypt in HCT!!! Skill has no decryption capability.
> **Important Pre-check Information**:
> - **Check device status before capturing**: Use the device detail function in the resource management module to verify if stream encryption is enabled
> - **Example command**: `python scripts/device_detail.py {device_serial}`
> - If `Stream Encryption` shows `Enabled`, you must disable it first before capture
---

## ⚠️ Security Warning (Read Before Use)

| # | Check Item                | Status      | Description                                                                                                              |
|---|---------------------------|-------------|--------------------------------------------------------------------------------------------------------------------------|
| 1 | **Credential Permission** | ⚠️ Required | Please use credentials with **capture permission**, avoid using super admin credentials                                  |
| 2 | **Image Encryption**      | ⚠️ Note     | If device has image encryption enabled, returned URL may not be directly viewable, user needs to manually decrypt in HCT |
| 3 | **Token Cache**           | ✅ Encrypted | Token cached in system temp directory, only current user can read (600 permission)                                       |
| 4 | **API Domain**            | ✅ Auto      | API domain is automatically obtained from token response (no longer requires manual configuration)                       |

---

## 🚀 Quick Start

```bash
# Scenario 1: Capture image for specified device serial number (channel number defaults to 1)
python scripts/capture_pic.py L33721705

# Scenario 2: Capture image for specified device serial number and channel number
python scripts/capture_pic.py D72821502,2
```

---

## 🛠 Workflow

```mermaid
graph TD
    A[Start Script] --> B{Check Environment Variables}
    B -- Missing --> C[Report Error and Exit]
    B -- Pass --> D[Get AccessToken]
    D --> E{Is Token Valid?}
    E -- Cache Valid --> F[Use Cache Directly]
    E -- Expired/No Cache --> G[Call API to Get New Token]
    G --> H[Save to Local Cache]
    F --> I[Send Capture Request]
    H --> I
    I --> J{Parse Return Result}
    J -- Success --> K[Print Capture URL and Encryption Status]
    J -- Failed --> L[Print Error Message]
    K --> M[Output JSON Result]
    L --> M
    M --> N[End]
```

---

## 📋 API Parameter Details

### 1. Device Capture Request Parameters

**Endpoint**: `POST /api/hccgw/resource/v1/device/capturePic`

| Parameter Name | Type   | Description          | Required | Default | Notes                    |
|----------------|--------|----------------------|----------|---------|--------------------------|
| `deviceSerial` | String | Device serial number | **Yes**  | -       | Device unique identifier |
| `channelNo`    | String | Channel number       | No       | "1"     | Default is 1             |

### 2. API Return Data Description

| Field Name    | Type    | Description             | Notes                                            |
|---------------|---------|-------------------------|--------------------------------------------------|
| `captureUrl`  | String  | Capture preview address | Directly accessible image URL (if not encrypted) |
| `isEncrypted` | Integer | Is encrypted            | 0-not encrypted, 1-encrypted                     |

---

## 📝 Output Example

### Capture Success Example:
```text
[2026-04-25 22:25:18] Requesting capture: Device=D72821502, Channel=1
[SUCCESS] Capture successful: https://hpc-sgp-prod-s3-hccvis.oss-ap-southeast-1.aliyuncs.com/hccopen/capture/2026-04-25/D72821502/1/c4d29884-5d0c-47d9-8db7-3ccccd6eaf3b.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20260425T142521Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Credential=LTAI5tQckMpJxMb4qoHXJySP%2F20260425%2Foss-ap-southeast-1%2Fs3%2Faws4_request&X-Amz-Signature=6dbe52fb30120e3fb65a9e5bed420e5e1dea07c5a78a15eca47f105809babb69

[JSON Output]
{
  "success": true,
  "captureUrl": "https://hpc-sgp-prod-s3-hccvis.oss-ap-southeast-1.aliyuncs.com/hccopen/capture/2026-04-25/D72821502/1/c4d29884-5d0c-47d9-8db7-3ccccd6eaf3b.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20260425T142521Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Credential=LTAI5tQckMpJxMb4qoHXJySP%2F20260425%2Foss-ap-southeast-1%2Fs3%2Faws4_request&X-Amz-Signature=6dbe52fb30120e3fb65a9e5bed420e5e1dea07c5a78a15eca47f105809babb69",
  "isEncrypted": 0
}
======================================================================
Done
======================================================================
```

---

## 📂 File Structure

```text
├── scripts/
│   └── capture_pic.py      # Device capture core execution script
└── SKILL.md                # Skill usage documentation
```

---

## ❓ FAQ

- **Q: Why can't the image be opened?**
  - A: **There are two main possible reasons:**
    1. **Device has stream encryption enabled**: First check using device detail script (`python scripts/device_detail.py {device_serial}`). If it shows `Stream Encryption: Enabled`, you must disable it in HCT platform first
    2. **The returned image's `isEncrypted` field is 1**: This means the captured image is encrypted, same solution - disable stream encryption and retry
- **Q: How long is capture URL valid?**
  - A: Valid for 15 minutes, please view or download as soon as possible.
- **Q: What if "Device offline" is shown?**
  - A: Capture function requires device to be online, please first confirm device status through resource management module.
- **Q: Returned image is a URL address?**
  - A: If user didn't explicitly mention needing URL address, default to returning image to user.

---

---
**Error Codes**:

| Return Code | Return Message          | Description                                                 |
|-------------|-------------------------|-------------------------------------------------------------|
| OPEN000554  | Device Offline          | Device is offline, please check device online status        |
| OPEN000555  | Device Response Timeout | Device response timeout, please check device network status |
| OPEN000556  | Device Capture Failed   | Device capture failed                                       |
---