# Acceptance - Home Filter Replacement Tracker

## Required Files

- `SKILL.md`
- `skill.json`
- `ACCEPTANCE.md`

## Metadata Checks

- Version is `1.0.0`.
- License is `MIT-0`.
- Language is `en`.
- `hasExecutableCode` is `false`.
- `requires_api` is `false`.
- `no_network` is `true`.
- `no_credentials` is `true`.
- Skill type is prompt-flow or equivalent document-only prompt workflow.

## Content Checks

- Provides a household filter map.
- Includes locations, sizes or models, replacement intervals, last-changed dates, and next due dates.
- Builds 90-day and 12-month calendar views.
- Generates a shopping list.
- Creates a reusable replacement log format.
- Flags unknown filters and details requiring verification.
- States that manuals, landlord rules, and professional guidance take priority.
- Avoids risky maintenance instructions.

## Negative Checks

- No executable code.
- No API or network dependency.
- No credential collection.
- No instruction to open sealed systems or perform unsafe work.
- No CJK characters.

## Clean Scan Evidence

- SKILL.md: English only, no CJK/non-ASCII characters, no secrets, no credentials, no API keys, no tokens, no passwords, no personal data.
- skill.json: valid JSON, English only, all required safety fields present (hasExecutableCode: false, requires_api: false, no_network: true, no_credentials: true).
- ACCEPTANCE.md: English only, no secrets, no executable content.
- Directory: exactly 3 files (SKILL.md, skill.json, ACCEPTANCE.md). No package files, scripts, binaries, .env, .git, node_modules, or hidden configs.
- No executable code, no network calls, no API dependencies, no credential requirements.

## Install-First Success Path

1. **Input:** User provides home systems with replaceable filters, known filter details (size, model, brand, location), last replacement dates, and preferred intervals.
2. **Steps:** Skill builds a filter inventory, captures location/size/model/brand for each, records last replacement dates, assigns intervals using manual/landlord/technician guidance, calculates next due dates, builds 90-day and 12-month calendars, generates a consolidated shopping list, creates a reusable replacement log, and flags items needing verification.
3. **Output:** A Home Filter Replacement Tracker with Filter Inventory table, Due Soon lists (now, 30 days, 90 days), 12-Month Calendar, Shopping List, Replacement Log Template, Reminder Checklist, and Verification Flags for filters needing manual, landlord, or professional confirmation.
