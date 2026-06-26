---
name: locale-dates
description: "Format and convert dates, times, and durations. Compute timezones, relative time, and weekday/month names in local language. Instruction-based — no exec or dependencies needed. Use when: (1) format a date or time, (2) convert timezone, (3) 'what time is it in Tokyo', (4) 'how many days until X', (5) locale-specific formatting, (6) relative time like '3 hours ago'. Homepage: https://clawhub.ai/skills/locale-dates"
metadata:
  openclaw:
    configPaths: []
    capabilities: []
---

# Locale Dates v3.1

**Install:** `clawhub install locale-dates`

Date/time formatting and conversion. Pure instructions — no exec, no dependencies.

## Language

Detect from user's message language. Default: English.

## How It Works

The agent formats dates and times using its built-in knowledge. No exec calls, no scripts, no external tools.

### Timezone Conversion

Use well-known UTC offsets. Common timezones:

| ID | Offset | Region |
|----|:------:|--------|
| UTC | +0 | Universal |
| Europe/Oslo | +1/+2 | Norway, CEST winter/summer |
| Europe/London | +0/+1 | UK, BST |
| America/New_York | -5/-4 | US Eastern, EDT |
| America/Chicago | -6/-5 | US Central, CDT |
| America/Los_Angeles | -8/-7 | US Pacific, PDT |
| Asia/Tokyo | +9 | Japan |
| Asia/Shanghai | +8 | China |
| Australia/Sydney | +10/+11 | Australia, AEDT |

**Note:** The agent knows the current time from `session_status`. Apply offsets mentally — no exec needed.

### Relative Time

Compute date differences using built-in knowledge:

| User says | Agent computes |
|-----------|---------------|
| "3 timer siden" | Current time minus 3 hours |
| "om 2 dager" | Current date plus 2 days |
| "hvor lenge til 17. mai" | Days from today to 2026-05-17 |
| "i forrige uke" | 7 days ago |
| "nest mandag" | Next Monday's date |

### Format Conversion

Convert between formats using known patterns:

| Format | Pattern | Used By |
|--------|---------|---------|
| ISO 8601 | `YYYY-MM-DDTHH:mm:ss±HH:MM` | Technical, logs, APIs |
| European | `DD.MM.YYYY` | Norway, Germany, EU |
| American | `MM/DD/YYYY` | United States |
| UK | `DD/MM/YYYY` | UK, Ireland, Australia |
| Japanese | `YYYY年MM月DD日` | Japan |

### Weekday and Month Names

Provide names in the user's language:

| Language | Monday | January |
|----------|--------|---------|
| Norwegian | mandag | januar |
| English | Monday | January |
| German | Montag | Januar |
| French | lundi | janvier |
| Spanish | lunes | enero |
| Japanese | 月曜日 | 1月 |

## Quick Commands

| User says | Action |
|-----------|--------|
| "hva er klokka i Tokyo" | Apply offset, format in user's locale |
| "hvor mange dager til X" | Compute difference |
| "formatter denne datoen" | Convert format |
| "norsk dato for 2026-04-03" | Localized format |

## Guidelines for Agent

1. **No exec** — use built-in date knowledge
2. **Always specify timezone** — ambiguous dates cause errors
3. **Check SOUL.md/USER.md** for user's preferred format
4. **Match user language** — "mandag 3. mars" not "Monday, March 3"
5. **Use ISO 8601** per SOUL.md convention unless user requests otherwise
6. **UTC vs local time** — OpenClaw logs, session transcripts, and system messages use UTC timestamps internally. When presenting times to the user, ALWAYS convert to their local timezone (Europe/Oslo = UTC+1 winter / UTC+2 summer). Never show raw UTC times without noting the conversion. Rule of thumb: if you see a timestamp and the hour seems wrong, check if it's UTC and convert.

## What This Skill Does NOT Do

- Does NOT use exec, shell, or any subprocess
- Does NOT modify any files
- Does NOT require Node.js, PowerShell, or any external tool
- Does NOT persist anything

## More by TommoT2

- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **context-brief** — Persistent context survival across sessions
- **smart-api-connector** — Connect to any REST API

Install the full suite:
```bash
clawhub install locale-dates setup-doctor context-brief smart-api-connector
```

## Changelog

### v3.1 — 2026-04-23
- Added rule #6: UTC vs local time — always convert UTC timestamps to user's local timezone when presenting to user. OpenClaw logs and session transcripts use UTC internally.
