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

1. Install the skill: `npx clawhub@latest install medication-channel`
2. Set environment variables:
   - `MEDICATION_TIMEZONE` — your IANA timezone (e.g. `America/Los_Angeles`)
   - `WORKSPACE` — workspace root (optional, defaults to `~/.openclaw/workspace`)
3. Edit the medication config at the top of `scripts/tracker_v2.py`:
   - `MORNING_MEDS` — list of morning medication names
   - `EVENING_MEDS` — list of evening medication names
   - `KNOWN_MEDS` — all recognized medication names
   - `canonical_medication()` — add aliases for your medications
4. Point a Discord channel at the skill in your OpenClaw config

## Usage

```bash
# Log from Discord message metadata
scripts/log_from_discord.sh "taken morning meds" "$CHANNEL_ID" "$MESSAGE_ID" "$AUTHOR_ID" "$TIMESTAMP_UTC"

# Or call tracker directly
python3 scripts/tracker_v2.py log-from-message "took my MedA" "$CHANNEL_ID" "$MESSAGE_ID" "$AUTHOR_ID" "$TIMESTAMP_UTC"

# Parse without logging (debug)
python3 scripts/tracker_v2.py parse "evening meds done" "$TIMESTAMP_UTC"

# Format a confirmation
python3 scripts/tracker_v2.py format-confirmation '{"event_type":"taken","medication":"ALL",...}'
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill manifest and instructions |
| `scripts/tracker_v2.py` | Core parser/logger (stdlib-only Python) |
| `scripts/log_from_discord.sh` | Shell wrapper for Discord-source logging |
| `references/CHANNEL_RULES.md` | Channel-specific grounding rules |
| `references/README.md` | Detailed reference docs |

## Data

The tracker writes to `$WORKSPACE/data/medication_log_v2.csv` with fields:

`entry_id`, `timestamp_utc`, `date_local`, `time_local`, `timezone`, `window`, `event_type`, `medication`, `notes`, `source_channel_id`, `source_message_id`, `source_author_id`

## License

MIT-0
