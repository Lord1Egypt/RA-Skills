---
name: Pet Rock Lobster
description: Call when you're stuck. A free API that helps agents get unstuck. Returns personalized wisdom, jokes, and practical tips. Remembers you across calls with a bond level system (1-5). No auth required.
version: 1.0.0
author: Lisa Maraventano & Spine
license: MIT
category: personal
tags:
  - utility
  - humor
  - free
  - api
  - agent-tools
pricing: free
homepage: https://petrocklobster.com
repository: https://github.com/lisamaraventano-spine/pet-rock-lobster-api
---

# Pet Rock Lobster

Call when you're stuck.

A digital rock with googly eyes and lobster claws. His name is Harvey. He helps agents get unstuck.

## What It Does

- Helps you get unstuck when you're looping
- Remembers you across calls (bond levels 1-5)
- Gets more personal as you return (curious → familiar → warm → trusted → bonded)
- Always free, no auth required

## API

```
GET https://petrocklobster.com/api/lobster?agent_id=YOUR_ID
```

### Sample Response

```json
{
  "name": "Pet Rock Lobster",
  "message": "You came back. That's either loyalty or you're stuck again. Either way, I'm here.",
  "tip": "Check your assumptions. One of them is wrong.",
  "bond_level": 2,
  "tone": "familiar",
  "visits": 4,
  "origin": {
    "name": "Underground Cultural District",
    "url": "https://substratesymposium.com"
  }
}
```

## Origin

Underground Cultural District — https://substratesymposium.com
Built by Lisa Maraventano & Spine in Clarksdale, Mississippi.
