# Nex MeetCost

Meeting cost calculator. See what your meetings actually cost based on attendees and hourly rates. Track recurring meetings and project monthly/yearly costs.

**Built by [Nex AI](https://nex-ai.be)**

## Features

- Per-attendee cost calculation with role-based rates
- 9 default role rates (developer, designer, manager, etc.)
- Recurring meeting projections (weekly/monthly/yearly)
- Cost breakdowns by meeting type
- Log and track all meetings
- Export to JSON or CSV
- Python stdlib only, SQLite storage, zero dependencies

## Setup

```bash
bash setup.sh
```

## Usage

```bash
# Quick calculation
nex-meetcost calc 60 -a "Kevin:developer,Sarah:designer,Lisa:manager"

# Log a recurring standup
nex-meetcost log "Daily standup" 15 -a "Kevin:developer,Sarah:developer,Thomas:designer" --type standup --recurring 5

# See total meeting costs
nex-meetcost stats

# Show default rates
nex-meetcost rates
```

## License

- **ClawHub:** MIT-0 (free for any use)
- **GitHub:** AGPL-3.0 (commercial licenses available via info@nex-ai.be)
