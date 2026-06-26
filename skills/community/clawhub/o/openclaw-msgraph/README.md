# OpenClaw Microsoft Graph Skill

![Tests](https://img.shields.io/badge/tests-114%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-82%25-green)

Connect your Microsoft 365 personal account (Outlook, Calendar) to OpenClaw via the **Microsoft Graph API** with secure PKCE authentication.

## Features

- 📧 **Email Management**: List inbox, read messages, move to folders, search
- 📅 **Calendar**: View upcoming events, create events with attendees, manage calendars
- 🔐 **Secure Auth**: PKCE flow — no client secret needed, tokens stored locally
- 🚀 **Ready to Use**: One-time browser login, auto token refresh
- ✅ **Well Tested**: 114 tests, 82% code coverage

## Quick Start

### 1. Register Your App (Azure Portal)

1. Go to [Azure Portal](https://portal.azure.com) → **Azure Active Directory** → **App registrations** → **New registration**
2. Name: `OpenClaw` | Account type: **Personal Microsoft accounts only**
3. Go to **Authentication** → **Add a platform** → **Single-page application**
4. Add redirect URI: `http://localhost:8765/`
5. Go to **API permissions** → **Microsoft Graph** → add **Delegated permissions**:
   - `Mail.Read`, `Mail.ReadWrite`
   - `Calendars.Read`, `Calendars.ReadWrite`
   - `User.Read`
6. Copy your **Application (client) ID**

### 2. Configure

Copy `config.example.ini` to `config.ini` and set your Client ID:

```ini
[msgraph]
CLIENT_ID = your-client-id-here
tenant = consumers
scopes = Mail.ReadWrite Calendars.ReadWrite offline_access User.Read
redirect_port = 8765
```

### 3. Authenticate

```bash
python scripts/auth.py login
# Browser opens → Sign in with your Microsoft account → Done!
# Tokens saved to ~/.openclaw/msgraph-tokens.json
```

### 4. Use It

```bash
# Check auth status
python scripts/auth.py status

# List inbox
python scripts/mail.py inbox --count 20

# Read a message
python scripts/mail.py read <message_id>

# Upcoming events (next 7 days)
python scripts/cal.py list

# Create an event
python scripts/cal.py create \
  --subject "Team Meeting" \
  --start "2026-03-10T14:00" \
  --end "2026-03-10T15:00"
```

## Documentation

- **[Detailed Setup Guide](references/SETUP.md)** — Azure app registration, troubleshooting
- **[Skill Guide](skill.md)** — Commands, workflows, folder organization
- **[API Reference](references/api.md)** — Microsoft Graph endpoints, scopes

## Dev & Testing

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Run Tests

```bash
python -m pytest tests/ -v
python -m pytest tests/ --cov=scripts --cov-report=html
```

**Coverage:** 82% across all modules

- `auth.py`: 64% (interactive browser flow hard to test)
- `cal.py`: 93% (calendar operations)
- `graph_api.py`: **100%** (HTTP utilities)
- `mail.py`: 83% (email operations)
- `utils.py`: **100%** (formatting helpers)

## Architecture

```
scripts/
├── auth.py        # PKCE OAuth, token management
├── mail.py        # Email commands (inbox, read, move, search)
├── cal.py         # Calendar commands (list, create, delete)
├── graph_api.py   # Shared HTTP utilities for Graph API
└── utils.py       # Formatting & parsing helpers
```

## Auth Flow

1. User runs `auth.py login`
2. Script generates PKCE challenge and opens browser
3. User signs in to Microsoft account
4. Browser redirects to `http://localhost:8765/`
5. Script captures authorization code
6. Script exchanges code for access token (with PKCE proof)
7. Refresh token stored locally, access token auto-refreshed

## Error Handling

- **401 Unauthorized**: Token expired → auto-refreshes
- **403 Forbidden**: Missing permissions → check Azure Portal
- **404 Not Found**: Invalid resource ID → verify message/event IDs

## Folder Organization

Well-known folder names work directly: `inbox`, `drafts`, `sentitems`, `deleteditems`, `junk`, `archive`

Custom folder names resolved by display name lookup.

## Requirements

- Python 3.7+
- Microsoft account (personal or work/school depending on Azure app config)
- No external dependencies (uses stdlib: `urllib`, `json`, `datetime`, `hashlib`, `base64`, `configparser`, `argparse`)

## License

MIT — See [LICENSE](LICENSE)

## Contributing

Found a bug? Have a feature request? Open an issue or submit a PR!

## Support

- Check [Troubleshooting](references/SETUP.md#troubleshooting) section
- Review [Skill Guide](skill.md) for workflows
- Check test files for usage examples
