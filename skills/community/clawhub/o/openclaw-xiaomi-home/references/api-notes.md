# Home Assistant API Notes

## Authentication

All API requests require a Long-Lived Access Token in the Authorization header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Base URL

```
http://localhost:8123/api
```

## Key Endpoints

### States

```bash
# Get all states
GET /api/states

# Get single entity state
GET /api/states/{entity_id}

# Example
curl -H "Authorization: Bearer $HA_TOKEN" \
     http://localhost:8123/api/states/light.living_room
```

### Services

```bash
# Call a service
POST /api/services/{domain}/{service}

# Light examples
POST /api/services/light/turn_on
{"entity_id": "light.living_room", "brightness": 255}

POST /api/services/light/turn_off
{"entity_id": "light.living_room"}

# Climate examples
POST /api/services/climate/set_temperature
{"entity_id": "climate.living_room_ac", "temperature": 26}

POST /api/services/climate/set_hvac_mode
{"entity_id": "climate.living_room_ac", "hvac_mode": "cool"}

# Lock examples
POST /api/services/lock/lock
{"entity_id": "lock.front_door"}

POST /api/services/lock/unlock
{"entity_id": "lock.front_door"}
```

### Config

```bash
GET /api/config
```

### Events

```bash
# Listen to events (Server-Sent Events)
GET /api/events
```

## Entity ID Format

```
{domain}.{device_name}_{identifier}
```

Examples:
- `light.living_room_ceiling`
- `climate.bedroom_ac`
- `sensor.kitchen_temperature`
- `binary_sensor.front_door`
- `lock.front_door`
- `switch.tv_plug`

## Common Domains

| Domain | Type |
|--------|------|
| `light` | Lights |
| `switch` | Plugs, Switches |
| `climate` | AC, Heaters |
| `sensor` | Sensors (readings) |
| `binary_sensor` | Binary sensors (on/off) |
| `lock` | Smart locks |
| `cover` | Curtains, Blinds |
| `fan` | Fans |
| `scene` | Scenes |
| `automation` | Automations |

## Error Responses

```json
{
  "code": "not_found",
  "message": "Entity not found"
}
```

## Rate Limits

- No strict rate limit for local API
- Recommended: max 10 calls/second
- Cloud API (Xiaomi) may have stricter limits
