# LG ThinQ API: Technical Reference

This document provides detailed API documentation for LG ThinQ Connect integration.

## Table of Contents

1. [Headers](#1-required-headers)
2. [Public Constants](#2-public-constants)
3. [Regional Discovery](#3-regional-discovery)
4. [Device Endpoints](#4-device-endpoints)
5. [Control Logic](#5-control-logic-x-conditional-control)
6. [Common Payloads](#6-common-payloads)
7. [CLI Tool](#7-cli-tool-lg_api_toolpy)
8. [Error Codes](#8-error-codes)

---

## 1. Required Headers

All API requests require these headers:

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer {LG_PAT}` - Personal Access Token |
| `x-api-key` | Yes | Fixed: `v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3` |
| `x-client-id` | Yes | Fixed: `test-client-123456` |
| `x-country` | Yes | 2-letter ISO code (IN, US, GB, etc.) |
| `x-message-id` | Yes | Tracking ID (22 chars) |
| `Content-Type` | Yes | `application/json` |

### x-message-id

**Purpose**: Tracking ID for API requests. Used by LG API for error tracking and debugging.

**Format**: UUID v4 (url-safe base64, 22 characters)
- Example: `fNvdZ1brTn-wWKUlWGoSVw`

**Usage**:
- Can be static (same value reused for all requests)
- Or generated per-request for unique tracking
- Default value in `references/public_api_constants.json`

### x-conditional-control

**Purpose**: Optimistic locking for device control commands. Prevents race conditions when multiple clients control the same device.

**When to use**: For `POST /devices/{id}/control` requests.

**Logic**:
1. Fetch current device state
2. Record the current value of the property you want to change
3. Include header with snapshot of that value
4. If device state changed since your read, API rejects the command

**Header format**:
```
x-conditional-control: {"snapshot": {"category.property": "previousValue"}}
```

**Example**:
```
x-conditional-control: {"snapshot": {"operation.airConOperationMode": "POWER_OFF"}}
```

**Why use it**: Prevents conflicting commands (e.g., turning on an already-on device).

---

## 2. Public Constants

These are public developer kit constants, NOT secrets. Stored in `references/public_api_constants.json`.

| Variable | Value | Description |
|----------|-------|-------------|
| `LG_API_KEY` | `v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3` | Fixed API key |
| `LG_CLIENT_ID` | `test-client-123456` | Client identifier |
| `LG_MESSAGE_ID` | `fNvdZ1brTn-wWKUlWGoSVw` | Default tracking ID |
| `LG_SERVICE_PHASE` | `OP` | Service configuration |

---

## 3. Regional Discovery

Call `/route` first to find your regional API server. Results are cached in `.api_server_cache` for subsequent calls.

**Endpoint**: `https://api-kic.lgthinq.com/route`

**Route selection by country**:
- Americas (US, CA, MX, BR, AR, CL, CO): `https://api-aic.lgthinq.com/route`
- EMEA (GB, FR, DE, IT, ES, RU, ZA, AE, SA, TR): `https://api-eic.lgthinq.com/route`
- Asia/Other: `https://api-kic.lgthinq.com/route`

**Caching**:
- API server URL is cached in `.api_server_cache` file
- Priority: `LG_API_SERVER` env var > `.api_server_cache` > route API call

**Headers**:
```
x-api-key: v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3
x-country: IN
x-service-phase: OP
x-message-id: fNvdZ1brTn-wWKUlWGoSVw
```

**Response**:
```json
{
  "messageId": "...",
  "response": {
    "apiServer": "https://api-kic.lgthinq.com",
    "mqttServer": "...",
    "webSocketServer": "..."
  }
}
```

---

## 4. Device Endpoints

Base URL: `{apiServer}` (from route discovery)

### List Devices
```
GET /devices
Headers: Authorization, x-api-key, x-client-id, x-country, x-message-id
```

### Get Device Profile
```
GET /devices/{deviceId}/profile
Headers: Authorization, x-api-key, x-client-id, x-country, x-message-id
Response: Device capabilities, controllable properties, modes
```

### Get Device State
```
GET /devices/{deviceId}/state
Headers: Authorization, x-api-key, x-client-id, x-country, x-message-id
Response: Current device state
```

### Control Device
```
POST /devices/{deviceId}/control
Headers: Authorization, x-api-key, x-client-id, x-country, x-message-id, x-conditional-control
Body: {"category": {"property": "value"}}
```

---

## 5. Control Logic (x-conditional-control)

The `x-conditional-control` header implements optimistic locking:

### Without conditional control:
```
1. User: "Set temp to 24"
2. AC: OK, set to 24
3. (Someone else changes AC to 26)
4. User: "Turn off"
5. ⚠️ Error: Command conflicts with current state
```

### With conditional control:
```
1. User: "Set temp to 24"
2. Read state: temp=24, mode=cool
3. Command: set temp=26 with snapshot(temp=24)
4. AC: OK, set to 26 (was 24)
5. User: "Turn off"
6. Read state: temp=26, mode=cool
7. Command: power off with snapshot(mode=cool)
8. AC: OK, power off
```

### Implementation:
```python
def control_property(device_id, category, property_name, value):
    # 1. Read current state
    state = get_state(device_id)
    current = state.get(category, {}).get(property_name)
    
    # 2. Build snapshot
    snapshot = {f"{category}.{property_name}": current}
    
    # 3. Build payload
    payload = {category: {property_name: value}}
    
    # 4. Build header
    headers = {
        "x-conditional-control": json.dumps({"snapshot": snapshot})
    }
    
    # 5. Send command
    return post(f"/devices/{device_id}/control", payload, headers)
```

---

## 6. Common Payloads

### Air Conditioner

| Action | Payload |
|--------|---------|
| Power ON | `{"operation": {"airConOperationMode": "POWER_ON"}}` |
| Power OFF | `{"operation": {"airConOperationMode": "POWER_OFF"}}` |
| Set Temp 24°C | `{"temperature": {"coolTargetTemperature": 24}}` |
| Fan High | `{"airFlow": {"windStrength": "HIGH"}}` |
| Cool Mode | `{"operation": {"airConOperationMode": "COOL"}}` |

---

## 7. CLI Tool (lg_api_tool.py)

The primary interface for OpenClaw. Abstracts header management and snapshot logic.

### Commands

```bash
# Configuration
check-config              # Human-friendly validation
validate                  # Machine-readable validation
save-route               # Discover and cache API server to .api_server_cache

# Discovery
list-devices             # List all connected devices

# Device Operations
get-profile <id>         # Get device capabilities
get-state <id>           # Get current state
control <id> <cat> <prop> <value>  # Control device

# Utilities
--help                   # Show help
--debug                  # Show API calls/headers
```

### Examples

```bash
# Validate setup
python scripts/lg_api_tool.py check-config

# Save API route
python scripts/lg_api_tool.py save-route

# List devices
python scripts/lg_api_tool.py list-devices

# Get device profile
python scripts/lg_api_tool.py get-profile abc123...

# Control device (turn on)
python scripts/lg_api_tool.py control abc123... operation airConOperationMode POWER_ON

# Debug output
python scripts/lg_api_tool.py list-devices --debug
```

---

## 8. Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | - |
| 400 | Bad request | Check payload format |
| 401 | Unauthorized | LG_PAT expired or invalid |
| 403 | Forbidden | Check credentials/permissions |
| 404 | Not found | Check device ID |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry later |

---

## Security Notes

- **LG_PAT**: Never paste into chat. Store securely in shell env.
- **LG_COUNTRY**: 2-letter ISO code.
- **Credentials**: Never duplicate into skill folders.
- **Shell Env Preferred**: Set `LG_PAT` and `LG_COUNTRY` in shell environment. `.env` in project root supported.
- **API Server Cache**: Cached in `.api_server_cache` (not `.env`) to avoid conflicts.
