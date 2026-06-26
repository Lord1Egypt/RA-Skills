# MQTT Topics Best Practices

## Topic Structure

### Standard MQTT Topic Hierarchy

```
<root>/<device_type>/<device_name>/<property>
```

### Recommended Prefixes

| Prefix | Usage |
|--------|-------|
| `zigbee2mqtt/` | Zigbee2MQTT devices |
| `homie/` | Homie Convention devices |
| `homeassistant/` | Home Assistant |
| `tasmota/` | Tasmota devices |
| `openclaw/` | OpenClaw own topics |

## Zigbee2MQTT Topics

### Bridge Topics

```
zigbee2mqtt/bridge/info           # Bridge information
zigbee2mqtt/bridge/state          # Bridge status (online/offline)
zigbee2mqtt/bridge/log            # Bridge logs
zigbee2mqtt/bridge/request/info   # Request info
zigbee2mqtt/bridge/request/devices # Request device list
zigbee2mqtt/bridge/permit_join    # Allow device join
zigbee2mqtt/bridge/remove/<id>    # Remove device
zigbee2mqtt/bridge/rename/<id>   # Rename device
```

### Device Topics

```
zigbee2mqtt/<friendly_name>       # Device status (JSON)
zigbee2mqtt/<friendly_name>/set   # Control device
zigbee2mqtt/<friendly_name>/get   # Query value
zigbee2mqtt/<friendly_name>/availability  # Online/Offline status
```

## Control Commands

### On/Off

```json
// Publish to <device>/set
{ "state": "ON" }
{ "state": "OFF" }
{ "toggle": "" }
```

### Brightness

```json
{ "brightness": 0-255 }
{ "brightness": 50 }  // ~20%
```

### Color (RGB)

```json
{ "color": { "r": 255, "g": 128, "b": 0 } }
```

### Color Temperature

```json
{ "color_temp": 370 }  // Kelvin (warm to cool)
```

### Color (XY)

```json
{ "color": { "x": 0.5, "y": 0.5 } }
```

## Sensors

### Temperature

```json
{
  "temperature": 23.5,
  "humidity": 45,
  "pressure": 1013
}
```

### Motion

```json
{
  "occupancy": true,
  "occupancy_timeout": 60
}
```

### Battery

```json
{ "battery": 85 }
```

## QoS Recommendations

| QoS | Use Case |
|-----|-----------|
| 0 | Status updates, sensor values (loss acceptable) |
| 1 | Control commands (must arrive) |
| 2 | Critical commands (exactly once) |

## Retained Messages

- **Bridge State**: retain=true
- **Device Status**: retain=true
- **Sensor Data**: retain=false (too many updates)
- **Control Commands**: retain=false

## LWT (Last Will & Testament)

Recommended LWT topics:

```
openclaw/client/<clientId>/status  # Online/Offline
zigbee2mqtt/bridge/status          # Bridge online
```

LWT payload:
```json
{ "status": "offline", "reason": "unexpected", "timestamp": "..." }
```

## Error Codes

| Code | Description |
|------|-------------|
| `-32600` | Invalid JSON |
| `-32601` | Method not found |
| `-32602` | Invalid params |
| `-32603` | Internal error |