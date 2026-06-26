# Mxchip Smart Control API Reference

Complete API documentation for Mxchip Smart Control MCP service.

**Developer:** Shanghai MXCHIP Information Technology Co., Ltd. (上海庆科信息技术有限公司)  
**Official Website:** https://www.mxchip.com/  
**Target Application:** Smart Plus APP (智家精灵)  

## Table of Contents

1. [Protocol Overview](#protocol-overview)
2. [Authentication](#authentication)
3. [MCP Tools](#mcp-tools)
4. [MCP Prompts](#mcp-prompts)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

---

## Protocol Overview

### MCP (Model Context Protocol)

MXCHIP MCP implements the Model Context Protocol using JSON-RPC 2.0 over HTTP.

**Key Features:**
- JSON-RPC 2.0 request/response format
- Tool-based interaction model
- Prompt templates for specialized assistants
- Stateless HTTP transport

**Request Format:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": "unique-request-id",
  "params": {
    "name": "tool_name",
    "arguments": {
      "param1": "value1"
    }
  }
}
```

**Response Format:**
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "result": {
    "devices": [...],
    "scenes": [...]
  }
}
```

**Error Response:**
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "error": {
    "code": -32602,
    "message": "Invalid params"
  }
}
```

---

## Authentication

### OAuth2 Bearer Token

All requests require OAuth2 authentication.

**Header:**
```
Authorization: Bearer oauth2_YOUR_TOKEN
```

**Get Token:**
1. Visit: https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth
2. Enter Mxchip account credentials
3. Copy OAuth2 token

**Token Format:**
- Prefix: `oauth2_`
- Example: `oauth2_ABC123XYZ456EXAMPLE`

---

## MCP Tools

### 1. list_home_devices_and_scenes

**Purpose:** Query all devices and scenes in the home.

**Method:** `tools/call`

**Parameters:**
```json
{
  "name": "list_home_devices_and_scenes",
  "arguments": {}
}
```

**Response:**
```json
{
  "devices": [
    {
      "device_id": "vdevo_123456789",
      "name": "Living Room Light",
      "category": "LIGHT",
      "status": "online",
      "capabilities": ["TurnOn", "TurnOff"]
    },
    {
      "device_id": "vdevo_987654321",
      "name": "Bedroom AC",
      "category": "AIR_CONDITION",
      "status": "online",
      "capabilities": ["TemperatureControl", "ModeControl"]
    }
  ],
  "scenes": [
    {
      "scene_id": "sceneid_coming_home",
      "name": "Coming Home",
      "description": "Turn on lights and AC"
    },
    {
      "scene_id": "sceneid_sleep",
      "name": "Sleep Mode",
      "description": "Turn off all lights"
    }
  ]
}
```

**Device Categories:**
- `LIGHT`: Smart lights
- `AIR_CONDITION`: Air conditioners
- `SWITCH`: Smart switches
- `CURTAIN`: Smart curtains
- `SOCKET`: Smart sockets

---

### 2. control_device

**Purpose:** Control device power state (on/off).

**Method:** `tools/call`

**Parameters:**
```json
{
  "name": "control_device",
  "arguments": {
    "device_id": "vdevo_123456789",
    "action": "TurnOnRequest"
  }
}
```

**Valid Actions:**
- `TurnOnRequest`: Turn on device
- `TurnOffRequest`: Turn off device

**Response:**
```json
{
  "success": true,
  "device_id": "vdevo_123456789",
  "action": "TurnOnRequest",
  "timestamp": "2026-03-23T13:20:00Z"
}
```

**Example:**
```python
# Turn on light
result = client.control_device("light_001", "TurnOnRequest")

# Turn off switch
result = client.control_device("switch_001", "TurnOffRequest")
```

---

### 3. control_air_conditioner

**Purpose:** Control air conditioner temperature and mode.

**Method:** `tools/call`

**Parameters:**
```json
{
  "name": "control_air_conditioner",
  "arguments": {
    "device_id": "vdevo_ac_001",
    "action": "SetTemperatureRequest",
    "temperature": "26"
  }
}
```

**Actions:**

#### SetTemperatureRequest
Set target temperature (16-32°C)
```json
{
  "action": "SetTemperatureRequest",
  "temperature": "26"
}
```

#### IncrementTemperatureRequest
Increase temperature
```json
{
  "action": "IncrementTemperatureRequest",
  "delta": "2"
}
```
- `delta` (optional): Temperature increase (default "1")

#### DecrementTemperatureRequest
Decrease temperature
```json
{
  "action": "DecrementTemperatureRequest",
  "delta": "1"
}
```
- `delta` (optional): Temperature decrease (default "1")

#### SetModeRequest
Set working mode
```json
{
  "action": "SetModeRequest",
  "mode": "COOL"
}
```

**Valid Modes:**
- `COOL`: Cooling mode
- `HEAT`: Heating mode
- `AUTO`: Auto mode
- `FAN`: Fan only
- `DEHUMIDIFICATION`: Dehumidify
- `SLEEP`: Sleep mode

**Response:**
```json
{
  "success": true,
  "device_id": "vdevo_ac_001",
  "action": "SetTemperatureRequest",
  "temperature": 26,
  "timestamp": "2026-03-23T13:25:00Z"
}
```

**Examples:**
```python
# Set temperature
client.control_air_conditioner("ac_001", "SetTemperatureRequest", temperature=26)

# Increase temperature by 2°C
client.control_air_conditioner("ac_001", "IncrementTemperatureRequest", delta="2")

# Set cooling mode
client.control_air_conditioner("ac_001", "SetModeRequest", mode="COOL")
```

---

### 4. trigger_scene

**Purpose:** Execute a smart home scene.

**Method:** `tools/call`

**Parameters:**
```json
{
  "name": "trigger_scene",
  "arguments": {
    "scene_id": "sceneid_coming_home"
  }
}
```

**Scene ID Format:** `sceneid_xxx`

**Response:**
```json
{
  "success": true,
  "scene_id": "sceneid_coming_home",
  "scene_name": "Coming Home",
  "executed_actions": 5,
  "timestamp": "2026-03-23T13:30:00Z"
}
```

**Example:**
```python
# Trigger scene
client.trigger_scene("sceneid_coming_home")
```

---

## MCP Prompts

The service provides specialized prompts for different use cases.

### 1. device_control

**Purpose:** Device control assistant

**Description:** Focuses on controlling specific device types (lights, switches, curtains, etc.)

**When to use:** User wants to control individual devices

**Example conversation:**
```
User: "Turn on the living room light"
Prompt: device_control
→ Calls control_device with TurnOnRequest
```

---

### 2. scene_trigger

**Purpose:** Scene control assistant

**Description:** Helps users query and trigger preset scenes

**When to use:** User wants to execute scene automation

**Example conversation:**
```
User: "Activate coming home mode"
Prompt: scene_trigger
→ Calls trigger_scene with sceneid_coming_home
```

---

### 3. smart_home_assistant

**Purpose:** Full-featured smart home assistant

**Description:** Comprehensive assistant for all home automation tasks

**When to use:** User needs complete home management (query + control + scenes)

**Capabilities:**
- Query devices and scenes
- Control device power
- Adjust AC settings
- Trigger scenes

---

## Error Handling

### JSON-RPC Error Codes

| Code | Message | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | Invalid JSON-RPC request |
| -32601 | Method not found | Method does not exist |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Server internal error |
| -32001 | Unauthorized | Authentication failed |
| -32002 | Device not found | Device ID invalid |
| -32003 | Invalid action | Action not supported |

### Error Response Example
```json
{
  "jsonrpc": "2.0",
  "id": "req_123",
  "error": {
    "code": -32002,
    "message": "Device not found",
    "data": {
      "device_id": "invalid_device_id"
    }
  }
}
```

### Python Error Handling
```python
from mxchip_mcp_client import (
    MxchipMCPClient,
    AuthenticationError,
    InvalidParameterError,
    MxchipMCPError
)

try:
    client = MxchipMCPClient()
    result = client.control_device("device_001", "TurnOnRequest")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except InvalidParameterError as e:
    print(f"Invalid parameter: {e}")
except MxchipMCPError as e:
    print(f"MCP error: {e}")
```

---

## Examples

### Example 1: Complete Home Check
```python
from mxchip_mcp_client import MxchipMCPClient

client = MxchipMCPClient()

# Get all devices and scenes
result = client.list_home_devices_and_scenes()

# Print device status
print("=== Devices ===")
for device in result.get('devices', []):
    print(f"{device['name']}: {device.get('status', 'Unknown')}")

# Print scenes
print("\n=== Scenes ===")
for scene in result.get('scenes', []):
    print(f"{scene['name']}: {scene['scene_id']}")

client.close()
```

### Example 2: Morning Routine
```python
client = MxchipMCPClient()

# Turn on bedroom light
client.control_device("bedroom_light_id", "TurnOnRequest")

# Set AC to comfortable temperature
client.control_air_conditioner(
    "bedroom_ac_id",
    "SetTemperatureRequest",
    temperature=24
)

# Open curtains
client.control_device("curtain_id", "TurnOnRequest")

client.close()
```

### Example 3: Scene-Based Automation
```python
client = MxchipMCPClient()

# Leaving home
client.trigger_scene("sceneid_leaving_home")

# Coming home
client.trigger_scene("sceneid_coming_home")

# Sleep mode
client.trigger_scene("sceneid_sleep")

client.close()
```

### Example 4: Temperature Management
```python
client = MxchipMCPClient()

# Set to 26°C cooling mode
client.control_air_conditioner("ac_id", "SetTemperatureRequest", temperature=26)
client.control_air_conditioner("ac_id", "SetModeRequest", mode="COOL")

# Too hot, increase temperature
client.control_air_conditioner("ac_id", "IncrementTemperatureRequest", delta="2")

# Too cold, decrease temperature
client.control_air_conditioner("ac_id", "DecrementTemperatureRequest", delta="1")

client.close()
```

---

## Best Practices

1. **Always query first:** Call `list_home_devices_and_scenes()` before control operations
2. **Use exact IDs:** Copy device_id and scene_id from query results
3. **Handle errors gracefully:** Implement proper error handling
4. **Close connections:** Always call `close()` when done
5. **Cache device list:** Avoid repeated queries for same device list
6. **Validate parameters:** Check temperature range and mode values before sending

---

## Rate Limits

- **Requests per minute:** 60
- **Concurrent connections:** 5
- **Request timeout:** 30 seconds

---

## Support

**OAuth Token Page:** https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth
**API Base URL:** https://app.api.cloud.mxchip.com:2443/mcp
**Protocol:** MCP with JSON-RPC 2.0
