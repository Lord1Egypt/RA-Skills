---
name: pipeworx-holidays
description: Public holidays for 100+ countries — look up by year, check if today is a holiday, or find the next upcoming ones
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🗓️"
    homepage: https://pipeworx.io/packs/holidays
---

# Public Holidays

Get official public holidays for over 100 countries via the Nager.Date API. Look up all holidays in a year, check if today is a holiday, or find the next upcoming holidays for a country.

## Tools

| Tool | Description |
|------|-------------|
| `get_holidays` | All public holidays for a country and year (e.g., US 2025) |
| `is_today_holiday` | Check if today is a public holiday in a given country |
| `next_holidays` | Upcoming public holidays for a country from today forward |

## When to use

- Scheduling features that need to account for public holidays
- "Is Monday a bank holiday in the UK?" — check with `is_today_holiday`
- Travel planning — see what holidays fall during a trip
- Payroll and HR tools that need country-specific holiday calendars

## Example: German holidays in 2025

```bash
curl -s -X POST https://gateway.pipeworx.io/holidays/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_holidays","arguments":{"country":"DE","year":2025}}}'
```

Returns date, name (English), local name (German), and whether it's a fixed or floating holiday.

## Setup

```json
{
  "mcpServers": {
    "pipeworx-holidays": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/holidays/mcp"]
    }
  }
}
```
