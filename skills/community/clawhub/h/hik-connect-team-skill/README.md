# Hik-Connect Team (HCT) Skills

Welcome to the **Hik-Connect Team (HCT) Skills**. This is a comprehensive developer skill set designed for **Hik-Connect for Teams (HCT)**, providing a modular and efficient way to manage and control HCT devices through the **HCTOpen OpenAPI** system.

## 🌟 Overview

The HCT Skills empowers developers to integrate professional security and management features into their own applications or automated workflows. It handles the complexities of authentication, token management, and standardized communication with Hikvision's cloud services.

### Key Features
- **Resource Management**: Discover devices, get details, and enumerate channels.
- **Access Control (ACS)**: Remotely open/close doors and manage access states.
- **Real-time Capture**: Trigger and retrieve live snapshots from cameras.
- **Video Streaming**: Generate secure, time-limited URLs for live video previews.
- **Alarm Management**: Subscribe to events and receive real-time notifications via Webhooks.

---

## 🛠 Modules & Capabilities

The Skills is divided into specialized modules, each with its own dedicated scripts and documentation:

| Module                                                          | Description                 | Key Scripts                                            |
|:----------------------------------------------------------------|:----------------------------|:-------------------------------------------------------|
| [**📦 Resource**](./modules/Hik-Connect_Team_Resource/SKILL.md) | Manage your asset inventory | `list_devices.py`, `device_detail.py`, `list_doors.py` |
| [**🚪 ACS**](./modules/Hik-Connect_Team_ACS/SKILL.md)           | Remote door control         | `acs_control.py`                                       |
| [**📸 Capture**](./modules/Hik-Connect_Team_Capture/SKILL.md)   | Instant image snapshots     | `capture_pic.py`                                       |
| [**🎥 Video**](./modules/Hik-Connect_Team_Video/SKILL.md)       | Live stream URL generation  | `get_video_url.py`                                     |
| [**🔔 Alarm**](./modules/Hik-Connect_Team_Alarm/SKILL.md)       | Webhook & Event management  | `webhook_manager.py`, `event_manager.py`               |

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.8+**
- **Node.js** (Required only for the Alarm/Webhook service)
- **HCT Developer Credentials**: You must have `HIK_CONNECT_TEAM_OPENAPI_APP_KEY` and `HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY` from the Hik-Connect HCT Developer Platform. The API domain will be automatically obtained from the token response.

### 2. Installation
Install the required Python dependencies:
```bash
pip3 install requests tabulate pycryptodome Pillow
```

### 3. Configuration

**Credentials only need to be configured ONCE. The system will automatically find and use them.**

#### Method A: Environment Variables (Recommended)
Set in your shell profile or before running scripts:
```bash
export HIK_CONNECT_TEAM_OPENAPI_APP_KEY="Your Hik-Connect Team OpenAPI AppKey"
export HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY="Your Hik-Connect Team OpenAPI SecretKey"
```

#### Method B: OpenClaw Config Files (Fallback)
If environment variables are not set, the system will automatically search for credentials in OpenClaw config files:

```
Config search order (first found wins):
1. ~/.openclaw/config.json
2. ~/.openclaw/gateway/config.json
3. ~/.openclaw/channels.json ⭐ Recommended
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

**Note**: API domain is automatically obtained from token response.

---

## 🔒 Credential Priority

**The skill obtains credentials in the following order (highest to lowest priority):**

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
│ 3. Error Handling (When no valid credentials)               │
│    Program exits with error message                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Usage Examples

### Example 1: List All Devices
```bash
cd "Hik-Connect Team Skills/modules/Hik-Connect_Team_Resource/scripts"
python list_devices.py
```

### Example 2: Remote Door Opening
```bash
cd "Hik-Connect Team Skills/modules/Hik-Connect_Team_ACS/scripts"
python acs_control.py --action-type 1 --element-list "your_door_resource_id"
```

### Example 3: Capture Device Image
```bash
cd "Hik-Connect Team Skills/modules/Hik-Connect_Team_Capture/scripts"
python capture_pic.py DEVICE_SERIAL
```

### Example 4: Get a Live Video Stream
```bash
cd "Hik-Connect Team Skills/modules/Hik-Connect_Team_Video/scripts"
python get_video_url.py --device-serial "SERIAL123" --resource-id "RES_ID_456"
```

### Example 5: Setting Up Alarms

The Alarm module requires a **public HTTPS URL** to receive webhook pushes from HCT platform.

#### Option A — Same Server as OpenClaw (Simplest)
1. Configure reverse proxy to route `/hikvision/webhook` to `127.0.0.1:3090`
2. Start Webhook server: `node modules/Hik-Connect_Team_Alarm/scripts/server.js`
3. Register URL: `python modules/Hik-Connect_Team_Alarm/scripts/webhook_manager.py save --url "https://your-domain.com/hikvision/webhook" --secret "your_secret"`
4. Subscribe: `python modules/Hik-Connect_Team_Alarm/scripts/event_manager.py subscribe`

#### Option B — Use a Tunnel Tool (ngrok/cpolar)
1. Run `ngrok http 3090` on OpenClaw server
2. Copy the tunnel URL
3. Start Webhook server and register the tunnel URL

> **Note**: Tunnel URLs change on restart for free tiers — you must re-register the Webhook after each restart.

#### Option C — Different Server with Public URL
If you have a separate public server and OpenClaw's port 3090 is reachable from it:
1. On your server, configure a reverse proxy to forward `/hikvision/webhook` to `<OpenClaw_SERVER_IP>:3090`
2. Start the Webhook server on OpenClaw server: `node modules/Hik-Connect_Team_Alarm/scripts/server.js`
3. Register your public URL: `python modules/Hik-Connect_Team_Alarm/scripts/webhook_manager.py save --url "https://your-domain.com/hikvision/webhook" --secret "your_secret"`
4. Subscribe to events: `python modules/Hik-Connect_Team_Alarm/scripts/event_manager.py subscribe`

> **⚠️ Third-party webhook receiver services (Pipedream, AWS Lambda URL, etc.) are NOT recommended** — they only receive requests, they cannot forward to your internal OpenClaw server.

### About Alarm Message Format

When alarm messages are pushed to OpenClaw, the AI agent may inherently attempt to translate, summarize, or reformat the raw data. This behavior is difficult to completely avoid.

**If you need a specific alarm message format:**
- Explicitly instruct the AI agent: "Do not process/modify/summarize the alarm data, return it as-is"
- If the format is still not ideal, directly tell the AI your preferred format (e.g., "Show alarm messages in a table", "Use the raw JSON format", etc.)

The raw alarm data from HCT platform contains complete information — the AI's processing is optional and can be overridden by your instructions.

---

## 🔒 Security Recommendations

### 1. Use Minimal Permission Credentials
- Create dedicated `HIK_CONNECT_TEAM_OPENAPI_APP_KEY`/`HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY` with only necessary API permissions
- Do not use main account credentials
- Rotate credentials regularly (recommended every 90 days)

### 2. Environment Variable Security
```bash
# Recommended: Use .env file (do not commit to version control)
echo "HIK_CONNECT_TEAM_OPENAPI_APP_KEY=your_key" >> .env
echo "HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY=your_secret" >> .env
chmod 600 .env

# Load environment variables
source .env
```

### 3. Disable Token Caching (High Security)
```bash
export HIK_CONNECT_TEAM_TOKEN_CACHE=0
python3 scripts/xxx.py ...
```

### 4. Regular Cache Cleanup
```bash
# Clear all cached Tokens
rm -rf /tmp/hctopen_global_token_cache/
```

### 5. Config File Scanning
The skill reads Hikvision configuration from (only when env vars not set):
```
~/.openclaw/config.json
~/.openclaw/gateway/config.json
~/.openclaw/channels.json
```

**Config Format**:
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

**Security Recommendations**:
- ✅ Use dedicated Hikvision credentials, do not share with other services
- ✅ Set environment variables to override config file scanning if needed
- ✅ Regularly review credential permissions in config files
- ❌ Do not store main account credentials in config files

---

## ✅ Security Audit Checklist

### Pre-Installation Checks
- [ ] **Review Code** — Read `lib/token_manager.py` and module scripts
- [ ] **Verify API Domain** — Confirm domain is Hikvision official endpoint
- [ ] **Prepare Test Credentials** — Create dedicated app with only necessary permissions
- [ ] **Check Config Files** — Review `~/.openclaw/*.json` for sensitive credentials
- [ ] **Confirm Cache Location** — Ensure `/tmp/hctopen_global_token_cache/` is acceptable

### Installation Configuration
- [ ] **Use Environment Variables** — Prefer `HIK_CONNECT_TEAM_OPENAPI_APP_KEY` etc.
- [ ] **Disable Caching** (Optional) — Set `HIK_CONNECT_TEAM_TOKEN_CACHE=0` for high security
- [ ] **Minimal Permission Credentials** — Do not use main account credentials
- [ ] **Isolated Environment** (Optional) — Run in container/VM

### Post-Installation Verification
- [ ] **Verify Cache Permissions** — Confirm cache file permissions are 600
- [ ] **Test Functionality** — Verify with test device
- [ ] **Monitor Logs** — Check API calls are normal
- [ ] **Secure Credential Storage** — Use key manager

### Ongoing Maintenance
- [ ] **Rotate Credentials** — Recommended every 90 days
- [ ] **Review Dependencies** — Check `requests` etc. for security updates
- [ ] **Clear Cache** — Clear cache in high security environments
- [ ] **Monitor for Anomalies** — Watch for unusual API calls or errors

---

## 🔒 Security & Best Practices

- **Least Privilege**: Use credentials with only the permissions necessary for your specific task.
- **Token Caching**: Skills automatically caches access tokens in system temp directory (600 permissions) to minimize API calls.
- **HTTPS**: All Webhook endpoints **must** use HTTPS.
- **Stream Encryption**: If devices have "Stream Encryption" enabled, you must manually decrypt in HCT platform or app.

---

## 📂 Project Structure

```text
Hik-Connect_Team_Skills/
├── README.md                    # This overview document
├── SKILL.md                     # Technical integration guide
├── lib/                         # Shared libraries
│   ├── token_manager.py         # Token management & base client
│   └── README_TOKEN_MANAGER.md  # Token manager documentation
└── modules/                     # Functional sub-modules
    ├── Hik-Connect_Team_Resource/
    ├── Hik-Connect_Team_ACS/
    ├── Hik-Connect_Team_Capture/
    ├── Hik-Connect_Team_Video/
    └── Hik-Connect_Team_Alarm/
```

For detailed information on each module, please refer to the `SKILL.md` file within each module's directory.

---


