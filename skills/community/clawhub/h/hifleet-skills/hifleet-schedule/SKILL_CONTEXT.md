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

**Not in this skill**: mailbox open tonnage/cargo (**`hifleet-mytonnages`**), ETA / pre-arrival search (**`hifleet-mytonnages`** route C).

## Requirements

- **`hifleet_api_key`** (or `HIFLEET_API_KEY`) — billed per call on HiFleet.  
- **No email** configuration.

## One-liner

**Schedule skill = HiFleet liner sailings (bulk / Ro-Ro / container); needs API Key only.**
