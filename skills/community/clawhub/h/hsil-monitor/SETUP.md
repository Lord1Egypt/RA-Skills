# Setup

## Requirements
- `curl`
- `jq`
- coreutils (`sort`, `awk`, `sed`, `date`, `mv`)
- `openclaw` (for scheduling)

## Installation
The skill is typically installed via ClawdHub:
```bash
clawhub install hsil-monitor
```

## Configuration
The skill is agent-driven and performs its own setup. To configure:
1. Trigger the skill and ask it to "run setup".
2. The agent will verify write access to `~/.config/hsil-monitor` (or `$HSIL_MONITOR_HOME`).
3. You will be prompted for:
   - Timezone (e.g., `Asia/Hong_Kong`)
   - Daily schedule time (e.g., `08:30`)
   - Indexes to monitor (e.g., `HSI`, `HSCEI`, `HSTECH`)
   - Bilingual or English-only mode
   - Backfill days and Deep-read preference
4. The agent writes `config.json` and offers to schedule the daily cron job.

## Storage
By default, all configuration and state are stored in:
`~/.config/hsil-monitor/`

You can override this by setting the `HSIL_MONITOR_HOME` environment variable.
