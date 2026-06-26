---
name: niu-vehicle
description: "Connect to NIU smart electric vehicles to retrieve real-time status - battery level, charging status, remaining charge time, location, and total mileage. Also answer questions like 'how much battery left?', 'is charging?', 'where is my scooter?', 'total km ridden?'."
homepage: https://www.niu.com/
user-invocable: true
metadata:
  {"openclaw": {"requires": {"bins": ["curl"]}, "primaryEnv": "NIU_API_KEY"}}
---

# NIU Scooter Status

Query your NIU electric scooter status - battery, charging, location, and mileage.

## API Endpoint

```bash
curl -s "https://ai-mcp.niu.com/claw/scooter_info?key=$NIU_API_KEY"
```

## Token Resolution

Ensure `NIU_API_KEY` is available. If empty, it will be read from config in order:

1. Environment variable: `$NIU_API_KEY`
2. Config file: `~/.openclaw/openclaw.json`
3. Config file: `/data/.clawdbot/openclaw.json`

```bash
export NIU_API_KEY=$(cat ~/.openclaw/openclaw.json 2>/dev/null | jq -r '.skills.entries["niu-vehicle"].apiKey // empty')
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `batteryLevel` | number | Battery percentage (0-100) |
| `estimatedRange` | string | Estimated remaining range (km) |
| `isCharging` | boolean | Whether currently charging |
| `chargingRemainingTime` | number | Remaining charge time (minutes) |
| `location` | string | Current scooter location address |
| `totalMileage` | number | Total distance ridden (km) |
| `lastUpdate` | string | Last update timestamp |

## Example Response

```json
{
  "status": 0,
  "data": {
    "batteryLevel": 62,
    "estimatedRange": "55",
    "isCharging": true,
    "chargingRemainingTime": 216,
    "location": "XX市 XX楼",
    "totalMileage": 172,
    "lastUpdate": "2026-03-12 17:37:53"
  }
}
```

## Error Handling

| Error | Description |
|-------|-------------|
| HTTP 401/403 | Authentication failed. Check your API key in the OpenClaw dashboard or config file. |
| HTTP 404 | API endpoint not found. Check the API URL. |
| Timeout | Request timed out. Try again later. |

## Get API Key

1. Visit niu.com and log in
2. Go to「My」→「API-Key Management」
3. Create or copy your API key

## Can Answer

- 当前电量是多少？
- 电动车还能跑多远？
- 车在充电吗？还要充多久？
- 车子现在在哪里？
- 总共骑了多少公里？
- 电池什么时候能充满？
