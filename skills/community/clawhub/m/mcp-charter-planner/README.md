# @velocibot/mcp-charter-planner

MCP tool for planning BVI (British Virgin Islands) sailing charters. Returns complete itineraries with real anchorages, weather considerations, provisioning lists, and local tips.

## Features

- **Real BVI Anchorages**: The Baths, Norman Island, Jost Van Dyke, Anegada, Cooper Island, North Sound, and more
- **Experience-Based Routing**: Routes tailored for beginner, intermediate, and expert sailors
- **Seasonal Weather**: Trade wind patterns, hurricane season awareness, swell risks
- **Smart Provisioning**: Guest-count-scaled provisioning lists with BVI-specific tips
- **Local Knowledge**: Customs clearance, mooring ball protocols, national park fees, restaurant recommendations

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "charter-planner": {
      "command": "npx",
      "args": ["-y", "@velocibot/mcp-charter-planner"]
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "charter-planner": {
      "command": "mcp-charter-planner"
    }
  }
}
```

## Tool: plan_charter

**Input:**
| Parameter   | Type     | Required | Description                                    |
|-------------|----------|----------|------------------------------------------------|
| start_date  | string   | yes      | Charter start date (YYYY-MM-DD)               |
| end_date    | string   | yes      | Charter end date (YYYY-MM-DD)                 |
| guests      | number   | yes      | Number of guests (1–20)                        |
| experience  | string   | yes      | "beginner", "intermediate", or "expert"        |
| interests   | string[] | no       | e.g., ["snorkeling", "fishing", "photography"] |

**Example:**
```json
{
  "start_date": "2026-04-01",
  "end_date": "2026-04-08",
  "guests": 4,
  "experience": "intermediate",
  "interests": ["snorkeling", "cuisine"]
}
```

**Output includes:**
- `itinerary` — Day-by-day plan with locations, activities, sailing notes
- `weather_notes` — Seasonal conditions, wind, swell, and hurricane risk
- `provisioning` — Complete shopping list scaled to guests and duration
- `tips` — Experience-appropriate tips on customs, mooring, safety, and local knowledge

## BVI Anchorages Covered

| Anchorage | Island | Highlights |
|-----------|--------|------------|
| The Baths | Virgin Gorda | Granite boulders, snorkeling grottos |
| The Bight | Norman Island | Pirates Bight, Willy T, The Caves |
| Great Harbour | Jost Van Dyke | Foxy's Bar, customs clearance |
| White Bay | Jost Van Dyke | Soggy Dollar Bar, Painkillers |
| Setting Point | Anegada | Lobster dinners, Horseshoe Reef |
| Cooper Island | Cooper Island | Eco-resort, microbrewery |
| North Sound | Virgin Gorda | Bitter End Yacht Club, Saba Rock |
| Cane Garden Bay | Tortola | Beach bars, Callwood Rum Distillery |
| Soper's Hole | Tortola | Provisioning, fuel, customs |
| The Dogs | The Dogs | World-class diving |

## Important BVI Information

- **Customs**: Clear in at Road Town, Jost Van Dyke, or Spanish Town ($4/person/day cruising permit)
- **Mooring Balls**: $25–35/night at most anchorages
- **National Park Fees**: $5/person at The Baths, The Dogs, and other parks
- **Hurricane Season**: June 1 – November 30 (peak Aug–Oct)
- **Currency**: USD accepted everywhere

## License

MIT
