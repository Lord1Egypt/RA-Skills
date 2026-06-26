---
name: Luma Events Enhanced
description: Fetch upcoming events from Luma (lu.ma) for any city. Use when the user asks about tech events, startup meetups, networking events, conferences, or things happening in cities around the world. Returns events with details including venue, date, hosts, ticket status, and links.
version: 1.1.1
author: Clawd (forked and enhanced by Pepe)
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Luma Events Enhanced Skill

This skill allows the agent to fetch upcoming events from Luma (lu.ma) without authentication. It supports multiple cities, date filtering, and JSON output. Events are automatically persisted to `~/.openclaw/workspace/memory/luma-events.json` and old events are pruned (>24h past start) to keep storage manageable.

## Capabilities

- `fetch_events(city, days=30, max_events=20, json=False)` – Fetch events for a city (or list of cities). Returns human-readable text or JSON.
- `get_persisted_events()` – Read stored events from memory file (useful for follow-up questions).
- `prune_old_events(hours=24)` – Remove events that ended more than N hours ago.

## Usage

The agent typically runs the CLI:

```bash
python3 scripts/fetch_events.py <city> [cities...] [--days N] [--max N] [--json]
```

### Parameters

- **`city`**: City slug (lowercase, hyphenated), e.g., `bengaluru`, `mumbai`, `san-francisco`, `new-york`, `lisbon`, `porto`.
- **`--days N`**: Only include events occurring within the next N days (default: 30).
- **`--max N`**: Maximum number of events to return per city (default: 20).
- **`--json`**: Output raw JSON instead of formatted text.

### Output

Human-readable output prints each event with:
- 🎯 Event name
- 📍 Venue and city
- 📅 Date and time (local to event)
- 👥 Hosts (up to 2)
- 👤 Guest count
- 🎫 Ticket status (Free/Paid/Sold Out/Available with spots)
- 🔗 Direct lu.ma link

JSON output includes an array of event objects with fields:
- `city`, `name`, `start`, `end`, `url`, `venue`, `hosts[]`, `guestCount`, `ticketStatus` (`free`/`paid`/`sold_out`), `spotsRemaining`, `isFree`, `lastFetched`

### Persistence

After fetching, events are merged into `~/.openclaw/workspace/memory/luma-events.json` by event URL. On each run, the file is pruned to remove events older than 24 hours past their start time. This allows the agent to maintain context without re-fetching.

## Examples

### Find tech events this week
```bash
python3 scripts/fetch_events.py bengaluru --days 7
```

### Check multiple cities for AI events
```bash
python3 scripts/fetch_events.py bengaluru mumbai san-francisco --days 14 --json | jq '.[] | .events[] | select(.event.name | contains("AI"))'
```

### Get next 5 events in a city
```bash
python3 scripts/fetch_events.py new-york --max 5
```
### Check if events are selling out
```bash
python3 ~/clawd/skills/luma/scripts/fetch_events.py mumbai --json | jq '.[] | .events[] | select(.ticket_info.is_near_capacity)'
```

## Example Queries

**User:** "What tech events are happening in Bangalore this weekend?"
→ Fetch Bengaluru events for next 7 days, save to memory

**User:** "Any AI meetups in Mumbai next month?"
→ Fetch Mumbai events for next 30 days, filter for AI-related, save to memory

**User:** "Compare startup events in SF vs NYC"
→ Fetch both cities, compare, save both to memory

## Notes

- Luma public pages embed event data in `__NEXT_DATA__` script tag; no API key required.
- If a city page does not expose an `events` array (e.g., Porto), the skill returns an empty result.
- Rate limiting: Be respectful; do not hammer Luma servers.
- Timezones: Event times are in the event's local timezone as provided by Luma.

## Troubleshooting

- **No upcoming events found** → City may not be supported by current Luma page format. This is expected.
- **Could not find __NEXT_DATA__** → Luma changed HTML structure or blocked the request; try later.
- **Timeouts** → Network issue; retry or check connectivity.

## Dependencies

- Python 3.6+ (stdlib only: `urllib`, `json`, `re`, `argparse`, `datetime`, `os`, `sys`)

## Changelog

### v1.1.1 (2026-03-08)
- Republished with explicit fork lineage to `regalstreak/luma` on ClawHub.
- No code changes; metadata-only patch release.

### v1.1.0 (2026-02-20)
- Changed persistence path to `~/.openclaw/workspace/memory/luma-events.json`.
- Automatic pruning of events older than 24 hours past their start.
- Friendly output for unsupported cities (e.g., Porto).
- Removed obsolete `README.md`; consolidated docs in `SKILL.md`.

### v1.0.0 (2026-01-29)
- Initial release
- Support for multiple cities
- Human-readable and JSON output
- Date filtering (--days)
- Event limit per city (--max)
- Event persistence to memory file
