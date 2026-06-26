# Medication Channel — Skill

A deterministic Discord medication event tracker for OpenClaw.

## What It Does

Logs medication events (taken/missed/extra) from a Discord channel using a Python script that handles:
- Natural-language parsing of medication reports
- Morning/evening window inference
- Timezone-aware timestamps from source Discord metadata
- Deduplication by source message ID
- Structured CSV logging

## Setup

1. Install the skill into your OpenClaw workspace
2. Set environment variables:
   - `MEDICATION_TIMEZONE` — your IANA timezone (e.g. `America/Los_Angeles`)
   - `WORKSPACE` — workspace root (optional, defaults to `~/.openclaw/workspace`)
3. Edit the medication config at the top of `scripts/tracker_v2.py`:
   - `MORNING_MEDS` — list of morning medication names
   - `EVENING_MEDS` — list of evening medication names
   - `KNOWN_MEDS` — all recognized medication names
   - `canonical_medication()` — add aliases for your medications
4. Point a Discord channel at the skill in your OpenClaw config

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill manifest and instructions |
| `scripts/tracker_v2.py` | Core parser/logger |
| `scripts/log_from_discord.sh` | Shell wrapper for Discord-source logging |
| `references/CHANNEL_RULES.md` | Channel-specific grounding rules |
| `references/README.md` | This file |

## Data

The tracker writes to `$WORKSPACE/data/medication_log_v2.csv` with fields:

`entry_id`, `timestamp_utc`, `date_local`, `time_local`, `timezone`, `window`, `event_type`, `medication`, `notes`, `source_channel_id`, `source_message_id`, `source_author_id`

## License

MIT-0
