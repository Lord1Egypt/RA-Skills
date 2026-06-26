# Nex Timetrack

Billable time logger for freelancers and agencies. Track time with a live timer or log manually. Manage clients, projects, and rates. Generate billing summaries with optional 15-minute rounding.

**Built by [Nex AI](https://nex-ai.be)**

## Features

- Live timer (start/stop) or manual time entry
- Client and project management with cascading rates
- 12 activity categories (development, design, meeting, etc.)
- Billing summaries with optional 15-minute rounding
- Full-text search across all entries
- Export to JSON or CSV for invoicing
- Python stdlib only, SQLite storage, zero dependencies

## Setup

```bash
bash setup.sh
```

## Usage

```bash
# Start a timer
nex-timetrack start "API integration" --client "Bakkerij Peeters" --category development

# Check timer
nex-timetrack status

# Stop and save
nex-timetrack stop --notes "Finished payment flow"

# Log time manually
nex-timetrack log "Design review" 1h30m --client "Lux Interiors" --category design

# Add a client with default rate
nex-timetrack client-add "Bakkerij Peeters" --rate 95 --email "jan@bakkerijpeeters.be"

# Add a project
nex-timetrack project-add "Website Redesign" --client "Bakkerij Peeters" --budget 40

# Billing summary
nex-timetrack summary --client "Bakkerij Peeters" --date-from 2026-04-01 --round-up

# Export for invoicing
nex-timetrack export csv --client "Bakkerij Peeters"
```

## Rate Cascade

Rates resolve: entry > project > client > default (85 EUR/h).

## License

- **ClawHub:** MIT-0 (free for any use)
- **GitHub:** AGPL-3.0 (commercial licenses available via info@nex-ai.be)
