---
name: hik-connect-team Skills
description: |
  Hik-Connect for Teams (HCT) Developer Skills.
  Integrates a series of skills for managing and controlling HCT devices, including resource management, access control, device capture, video streaming, and alarm push.
  Use when: Need to perform batch management, remote control, real-time monitoring, media resource acquisition, or alarm push configuration for devices under Hik-Connect for Teams mode.

  ⚠️ Global Requirement: All sub-modules require configuration of environment variables:
  - Hik-Connect Team OpenAPI AppKey
  - Hik-Connect Team OpenAPI SecretKey  
  - Hik-Connect Team OpenAPI Domain (auto-obtained from token response)
---

# Hik-Connect Team Skills

## 1. Introduction
`Hik-Connect_Team_Skills` is a full-featured integration Skills designed specifically for **Hik-Connect for Teams (HCT)** developers. Based on the **HCTOpen OpenAPI** system, it encapsulates core capabilities from basic resource management to advanced alarm push through Python scripts.

This Skills adopts a modular design with built-in automated **Token maintenance mechanisms**, **dynamic path searching**, and **standardized error handling**, aiming to help developers quickly build HCT-based automated O&M, security monitoring, and business integration systems.

---

## 2. Core Modules Deep Dive

This Skills consists of five core sub-modules, each providing deep support for specific business scenarios:

| Module Name                                                                | Core Functions                                            | Core Scripts                                                                       | Applicable Scenarios                                                                                                                          |
|:---------------------------------------------------------------------------|:----------------------------------------------------------|:-----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| [**📦 Resource Management**](./modules/Hik-Connect_Team_Resource/SKILL.md) | Device discovery, detail acquisition, channel enumeration | `list_devices.py`<br>`device_detail.py`<br>`device_channels.py`<br>`list_doors.py` | Asset inventory, obtaining device serial numbers and channel IDs, access control resources, synchronizing organizational structure resources. |
| [**🚪 Access Control (ACS)**](./modules/Hik-Connect_Team_ACS/SKILL.md)     | Remote open/close, normally open/normally closed control  | `acs_control.py`                                                                   | Remote office collaboration, unattended entrance management, access control linkage in emergencies.                                           |
| [**📸 Device Capture**](./modules/Hik-Connect_Team_Capture/SKILL.md)       | Real-time trigger capture, obtain image URL               | `capture_pic.py`                                                                   | Anomaly verification, real-time screen preview, manual secondary verification of AI recognition results.                                      |
| [**🎥 Video Streaming**](./modules/Hik-Connect_Team_Video/SKILL.md)        | Obtain real-time video stream                             | `get_video_url.py`                                                                 | Real-time monitoring embedding, remote video inspection, third-party monitoring large screen integration.                                     |
| [**🔔 Alarm Push (Alarm)**](./modules/Hik-Connect_Team_Alarm/SKILL.md)     | Webhook subscription, fine-grained event management       | `webhook_manager.py`<br>`event_manager.py`                                         | Real-time alarm notification, third-party system integration (e.g., Feishu/DingTalk robots).                                                  |

---

## 3. Environment Preparation and Global Configuration

### 3.1 Credential Configuration

Before using any module, credentials must be configured. The system supports two methods:

#### Method A: Environment Variables (Recommended)

```bash
# Required: Obtain from Hik-Connect HCT Developer Platform
export HIK_CONNECT_TEAM_OPENAPI_APP_KEY="Your Hik-Connect Team OpenAPI AppKey"
export HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY="Your Hik-Connect Team OpenAPI SecretKey"
# Note: API domain is automatically obtained from token response (no longer required)

# Optional: Token cache configuration (enabled by default to reduce API call frequency)
export HIK_CONNECT_TEAM_TOKEN_CACHE="1"  # 1=Enabled, 0=Disabled
```

#### Method B: OpenClaw Config Files (Fallback)

If environment variables are not set, the system will automatically search for credentials in OpenClaw config files:

```
Config search order (first found wins):
1. ~/.openclaw/config.json
2. ~/.openclaw/gateway/config.json
3. ~/.openclaw/channels.json
```

Config format:
```json
{
  "channels": {
    "hik_connect_team_openapi": {
      "appKey": "Your Hik-Connect Team OpenAPI AppKey",
      "secretKey": "Your Hik-Connect Team OpenAPI SecretKey",
      "enabled": true
    }
  }
}
```

**Recommended: Save to `~/.openclaw/channels.json`** — This is the dedicated file for channel credentials.

**⚠️ Security Note**: Storing credentials in config files is convenient but introduces some risk. Environment variables are recommended for better security.


### 3.2 Dependency Installation
This Skills is developed based on Python 3.8+. It is recommended to install necessary dependencies using the following command:
```bash
pip3 install requests tabulate pycryptodome Pillow
```

---

## 🔒 Config File Reading Details

**Credential Priority** (Highest to Lowest):

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Environment Variables (Highest Priority - Recommended)    │
│    ├─ HIK_CONNECT_TEAM_OPENAPI_APP_KEY                              │
│    └─ HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY                           │
│    ✅ Advantage: No config file reading, fully isolated    │
├─────────────────────────────────────────────────────────────┤
│ 2. OpenClaw Config Files (Only when env vars not set)        │
│    ├─ ~/.openclaw/config.json                               │
│    ├─ ~/.openclaw/gateway/config.json                       │
│    └─ ~/.openclaw/channels.json                             │
│    ⚠️ Note: Only reads channels.hik_connect_team_openapi field    │
├─────────────────────────────────────────────────────────────┤
```

## 4. Directory Structure Description
```text
Hik-Connect_Team_Skills/
├── SKILL.md                # This guide file (Full-featured integration guide)
├── lib/                    # Core library
│   └── token_manager.py    # Encapsulates HCTOpenClient base class, handles Token refresh, request retries, and path searching
└── modules/                # Functional sub-modules
    ├── Hik-Connect_Team_Resource/  # Resource Management: Devices, channels, details
    ├── Hik-Connect_Team_ACS/       # Access Control: Open/close, normally open/normally closed
    ├── Hik-Connect_Team_Capture/   # Device Capture: Real-time trigger, URL acquisition
    ├── Hik-Connect_Team_Video/     # Video Streaming: Real-time preview address acquisition
    └── Hik-Connect_Team_Alarm/     # Alarm Push: Webhook management, event subscription
```

---

## 5. Security and Best Practices

1.  **Token Security**: The Skills automatically caches Tokens locally. Please ensure the security of the running environment to prevent unauthorized reading of cache files in the `lib/` directory.
2.  **HTTPS Mandatory Requirement**: All Webhook callbacks from the HCT platform must use HTTPS. It is recommended to use `ngrok` or `cpolar` with SSL certificates for secure access.
3.  **Signature Verification**: In the Alarm module, be sure to configure `signSecret` and implement HMAC-SHA256 signature verification on your receiving end to prevent forged alarm pushes.
4.  **Error Handling**: All scripts return standard JSON format. If `success` is `false`, please check the `message` field for detailed error reasons.

---
