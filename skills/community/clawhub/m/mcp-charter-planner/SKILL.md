---
name: mcp-charter-planner
description: Plan BVI sailing charters with real anchorages, weather-aware routing, provisioning lists, and local knowledge. Returns complete itineraries tailored by experience level. Use when planning Caribbean sailing trips or charter vacations.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: ⛵
---

# BVI Charter Planner

Generate complete British Virgin Islands sailing charter itineraries with real anchorages, weather considerations, and local tips.

## Setup

```json
{
  "mcpServers": {
    "charter-planner": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-charter-planner"]
    }
  }
}
```

## Tool: `plan_charter`

| Parameter  | Type   | Required | Description |
|------------|--------|----------|-------------|
| days       | number | yes      | Trip duration (3-14 days) |
| guests     | number | yes      | Number of guests |
| experience | string | no       | beginner, intermediate, or expert |
| interests  | string | no       | Preferences: snorkeling, dining, remote, nightlife |

### Returns

- Day-by-day itinerary with real BVI anchorages (The Baths, Norman Island, Jost Van Dyke, Anegada, etc.)
- Experience-appropriate routing and sail distances
- Seasonal weather patterns (trade winds, hurricane season, swell risks)
- Guest-count-scaled provisioning lists with BVI-specific tips
- Customs clearance, mooring ball protocols, national park fees
- Restaurant and activity recommendations

## When to Use

- Charter vacation planning
- Sailing trip research
- BVI travel preparation
- Group trip logistics
