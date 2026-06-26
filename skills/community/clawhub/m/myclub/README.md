# myclub

Fetch sports schedules from [myclub.fi](https://myclub.fi), including practice times, game dates, locations, and registration status.

This is an independent open-source project and is not affiliated with myClub.

## Features

- Auto-discovers all accounts and clubs linked to your myclub.fi login
- Fetches upcoming practices, games, tournaments, and other events
- Supports flexible date ranges (`this week`, `next month`, custom dates)
- Returns structured JSON or human-readable text output
- Zero external dependencies — uses only Python standard library

## Requirements

- Python 3.10+

## Quick Start

1. Store your credentials (one-time):

```bash
python3 scripts/fetch_myclub.py setup --username your_email@example.com --password your_password
```

2. Discover your accounts and clubs:

```bash
python3 scripts/fetch_myclub.py discover
```

3. Fetch your schedule:

```bash
python3 scripts/fetch_myclub.py fetch --account "Account Name" --period "this week"
```

## Security

- Credentials are stored locally in `~/.myclub-config.json` with owner-only permissions (`0600`)
- Only connects to `id.myclub.fi` (auth) and `*.myclub.fi` (data)
- No telemetry, no third-party data sharing

## License

See [LICENSE](../LICENSE) in the project root.

## Source

[github.com/hanninen/myclub-skill](https://github.com/hanninen/myclub-skill)
