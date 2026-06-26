# OpenDream — Manual Installation

If you prefer not to use the setup script, follow these steps manually.

## Prerequisites

- An OpenClaw (or Hermes) workspace with `HEARTBEAT.md` and `SOUL.md`
- Access to `~/.openclaw/openclaw.json` (the gateway config)
- The `memory/` directory is created automatically by OpenClaw on first use. OpenDream reads `memory/YYYY-MM-DD.md` for daily context during dream ticks. No manual setup needed — if the directory doesn't exist yet, dreams will proceed from imagination until the agent has its first daytime conversation.

## Step 1: Backup existing files

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
cp ~/.openclaw/workspace/HEARTBEAT.md ~/.openclaw/workspace/HEARTBEAT.md.backup.$TIMESTAMP
cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace/SOUL.md.backup.$TIMESTAMP
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$TIMESTAMP
```

## Step 2: Merge dream section into HEARTBEAT.md

Open your `HEARTBEAT.md` and add the dream section from
`assets/HEARTBEAT-dream-section.md` at the end of the file.

```bash
cat assets/HEARTBEAT-dream-section.md >> ~/.openclaw/workspace/HEARTBEAT.md
```

**Check:** Your HEARTBEAT.md should now have both your existing daytime checks
AND the `## Dream mode (23:00–06:00)` section with all 5 cycle definitions.

## Step 3: Merge dream persona into SOUL.md

Append the dream persona fragment to your SOUL.md:

```bash
echo "" >> ~/.openclaw/workspace/SOUL.md
cat assets/SOUL-fragment.md >> ~/.openclaw/workspace/SOUL.md
```

**Check:** Your SOUL.md should now end with a `## Dream mode (23:00–06:00)`
section mentioning "ElectricSheep mode".

## Step 4: Create dreams directory

```bash
mkdir -p ~/.openclaw/workspace/dreams
```

## Step 5: Configure the gateway

Merge the heartbeat config from `assets/openclaw.json` into your
`~/.openclaw/openclaw.json`. The key values to set under
`agents.defaults.heartbeat`:

```json
{
  "every": "30m",
  "target": "none",
  "isolatedSession": true,
  "lightContext": true,
  "activeHours": {
    "start": "23:00",
    "end": "06:00",
    "timezone": "Europe/London"
  }
}
```

If you have `jq` installed:

```bash
jq -s '
  .[0] as $existing |
  .[1] as $new |
  $existing |
  .agents.defaults.heartbeat = $new.agents.defaults.heartbeat
' ~/.openclaw/openclaw.json assets/openclaw.json > /tmp/merged.json && \
mv /tmp/merged.json ~/.openclaw/openclaw.json
```

Otherwise, edit the file manually and add the heartbeat block above.

## Step 6: Validate

Run the validation script to confirm everything is in place:

```bash
python3 scripts/validate.py
```

Or check manually:
- `HEARTBEAT.md` contains `## Dream mode`
- `SOUL.md` contains `## Dream mode` and `ElectricSheep`
- `dreams/` directory exists
- `openclaw.json` has `activeHours` set to `23:00`–`06:00`

## Timezone

The default timezone is `Europe/London`. Edit `openclaw.json` to change
`activeHours.timezone` to your local timezone (e.g., `America/New_York`).

## Uninstall

1. Remove the `## Dream mode` section from `HEARTBEAT.md`
2. Remove the `## Dream mode` section from `SOUL.md`
3. Remove or comment out the `heartbeat` block in `openclaw.json`
4. Optionally delete `dreams/` (contains your dream history)

Or restore from backups:

```bash
# Find your backups
ls ~/.openclaw/workspace/.opendream-backups/
ls ~/.openclaw/.opendream-backups/

# Restore (use the correct timestamp)
cp ~/.openclaw/workspace/.opendream-backups/HEARTBEAT.md.TIMESTAMP ~/.openclaw/workspace/HEARTBEAT.md
cp ~/.openclaw/workspace/.opendream-backups/SOUL.md.TIMESTAMP ~/.openclaw/workspace/SOUL.md
cp ~/.openclaw/.opendream-backups/openclaw.json.TIMESTAMP ~/.openclaw/openclaw.json
```
