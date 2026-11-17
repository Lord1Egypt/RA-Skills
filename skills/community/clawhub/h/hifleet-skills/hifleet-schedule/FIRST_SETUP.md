# First setup

## A. Welcome

HiFleet **liner schedule** skill: query sailing schedules for **general/bulk**, **Ro-Ro**, and **container** lines.

Requires **API Key only** (no mailbox).

## B. API Key

1. Obtain `hifleet_api_key` on [mytonnages.hifleet.com](https://mytonnages.hifleet.com).  
2. Save in `config.json`:

```json
{
  "hifleet_api_key": "your-key",
  "hifleet_liner_api_base": "https://api.hifleet.com/openclaw/vessel/charter/liner"
}
```

Or set environment variable **`HIFLEET_API_KEY`**.

## C. How to ask

| You ask | Skill |
|---------|--------|
| Liner / line schedule between two ports | **hifleet-schedule** |
| Ro-Ro or container sailing | **hifleet-schedule** |
| Public open tonnage / cargo | **hifleet-opentonnages** |

## D. Unlock

Contact details on schedule rows may be masked until user confirms points spend → **`SCHEDULE_API.md`** §3 unlock.
