# Device Support Reference

## Supported Devices

### Lighting ✅
| Category | Examples | Notes |
|----------|----------|-------|
| Ceiling Lights | Mi LED Ceiling Light, Philips Ceiling Light | Full on/off/brightness/color control |
| Table Lamps | Mi Bedside Lamp, Mi Desk Lamp | Full control |
| Floor Lamps | Mi Floor Lamp | Full control |
| Bulbs | Mi LED Bulb, Philips Hue (via ecosystem) | Full on/off/brightness |

### Climate ✅
| Category | Examples | Notes |
|----------|----------|-------|
| Air Conditioners | Mi Air Conditioner, various IR-based ACs | Temperature, mode, fan speed |
| Heaters | Mi Smart Heater, Mi Oil Heater | Temperature control |
| Fans | Mi Smart Fan, Mi Standing Fan | On/off, speed |

### Sensors ✅
| Category | Examples | Notes |
|----------|----------|-------|
| Temperature/Humidity | Mi Temperature and Humidity Sensor | Readings |
| Door/Window | Mi Door/Window Sensor | Open/close status |
| Motion | Mi Motion Sensor | Detected/idle |
| Water Leak | Mi Water Leak Sensor | Detected/safe |

### Smart Locks ✅
| Category | Examples | Notes |
|----------|----------|-------|
| Door Locks | Xiaomi Smart Door Lock, Aqara Smart Lock | Lock/unlock, auto-lock settings |

### Plugs & Switches ✅
| Category | Examples | Notes |
|----------|----------|-------|
| Smart Plugs | Mi Smart Plug, Aqara Plug | On/off, power monitoring |
| Wall Switches | Mi Wall Switch, Aqara Wall Switch | On/off |

### Appliances ⚠️
| Category | Examples | Notes |
|----------|----------|-------|
| Refrigerators | Mi Refrigerator | Basic on/off, temperature |
| Washers | Mi Washing Machine | Start/stop, basic modes |
| Projectors | Mi Laser Projector | On/off, input selection |

## NOT Supported ❌

- **Bluetooth devices** (direct BLE connection)
- **Infrared (IR) devices** (TVs, AC remotes via IR blaster)
- **Virtual devices** (scenes, automations created in Mi Home)
- **Wearable devices** (Mi Band, etc.)
- **Air Purifiers** (some models may work)
- **Robot Vacuums** (different integration path)

## Local vs Cloud Control

### With Central Hub Gateway ✅
- Commands go through the local hub
- Faster response (< 1 second)
- Works without internet
- Requires: Hub firmware 3.3.0_0023+

### Without Central Hub
- Commands go through Xiaomi Cloud
- Slower response (1-3 seconds)
- Requires internet connection
- May have latency during cloud outages

### LAN Control (Partial Alternative)
Enable in Xiaomi Home integration settings:
Settings → Devices & Services → Xiaomi Home → Configure → LAN Control

⚠️ Note: LAN control only works for IP devices (WiFi), not BLE Mesh/ZigBee devices.

## Entity Naming Convention

In Home Assistant, Xiaomi devices appear as:
- `light.xiaomi_xxx` - Lights
- `climate.xiaomi_xxx` - AC/Heaters
- `sensor.xiaomi_temperature` - Sensors
- `binary_sensor.xiaomi_door` - Door/Window sensors
- `lock.xiaomi_lock` - Smart locks
- `switch.xiaomi_plug` - Plugs/Switches
