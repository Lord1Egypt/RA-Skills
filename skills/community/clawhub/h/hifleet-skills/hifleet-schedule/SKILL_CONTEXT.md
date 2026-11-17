# Skill context

## What this skill does

**HiFleet liner schedule** queries on `api.hifleet.com`: fixed sailing schedules by load/discharge port and laycan window.

**Covers (user wording)**:

| Type | Examples |
|------|----------|
| **General / bulk** | breakbulk, general cargo liner, 散杂货船期 |
| **Ro-Ro** | car carrier, PCTC, Ro-Ro, 滚装船期 |
| **Container** | container line, feeder, 集装箱船期 |

All use the same **`SCHEDULE_API.md`** (`{liner}/ports/suggest`, `{liner}/schedules`, `{liner}/unlock`).

**Port ID**: user-named load/discharge ports → **`GET {liner}/ports/suggest`** only (see **`references/charter_port_suggest.md`**); **not** `portguide/getPort/token`.

**Live position / AIS ETA / destination** (when user asks beyond schedule list fields): cross-call parent **`hifleet-skills`** → **`references/position_api.md`** (use row **`mmsi`**); see **`SCHEDULE_API.md`** §5.

**Not in this skill**: public open tonnage/cargo (**`hifleet-opentonnages`**).

## Requirements

- **`hifleet_api_key`** (or `HIFLEET_API_KEY`) — billed per call on HiFleet.  
- **No email** configuration.

## One-liner

**Schedule skill = HiFleet liner sailings (bulk / Ro-Ro / container); needs API Key only.**
