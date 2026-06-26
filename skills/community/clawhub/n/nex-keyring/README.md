# Nex Keyring

**Local API Key & Secret Rotation Tracker**

Monitor and manage all your API keys, webhooks, and credentials in one place. Track rotation status, detect stale keys, and enforce security policies. All data stays securely on your machine.

## Features

- **Track All Secrets**: Register API keys, database passwords, webhooks, SSH keys, and more
- **Rotation Policies**: Define custom rotation schedules for each secret
- **Risk Assessment**: Automatic detection of stale (FRESH, OK, STALE, CRITICAL) credentials
- **Service Detection**: Automatic recognition of popular services (OpenAI, Cloudflare, Firebase, Stripe, etc.)
- **Environment Scanning**: Scan .env files and environment variables for API keys
- **Rotation History**: Complete audit trail of all rotation events
- **Secure Local Storage**: All data stays in ~/.nex-keyring, never transmitted
- **Export Capabilities**: Export metadata-only reports in JSON, CSV, or Markdown
- **Encryption Ready**: Supports Fernet encryption (recommended) or base64 obfuscation

## Installation

### Step 1: Run Setup Script

```bash
bash setup.sh
```

The setup script will:
- Check Python 3 availability
- Create the data directory (~/.nex-keyring)
- Initialize the SQLite database
- Verify or recommend the cryptography library

### Step 2: Verify Installation

```bash
nex-keyring config
```

You should see configuration details and available service presets.

## Quick Start

### Register a Secret

```bash
nex-keyring add --name "OpenAI API Key" --service openai --env-var OPENAI_API_KEY --rotation 90
```

### List All Secrets

```bash
nex-keyring list
```

### Check Rotation Status

```bash
nex-keyring check
```

Shows all keys that need rotation based on their policies.

### Import from .env File

```bash
nex-keyring import .env
```

Automatically detects and registers all API keys found in your .env file.

### Show Secret Details

```bash
nex-keyring show "OpenAI API Key"
```

Displays metadata, rotation status, and risk level (never shows actual key values).

### Mark as Rotated

```bash
nex-keyring rotate "OpenAI API Key"
```

Records the rotation event. The tool prompts for the new key hash for change detection.

### Find Stale Keys

```bash
nex-keyring stale
```

Lists all keys that haven't been rotated recently or are past their rotation deadline.

## Command Reference

| Command | Description |
|---------|-------------|
| `add` | Register a new secret |
| `list` | List tracked secrets (with filters) |
| `show` | Show detailed secret information |
| `check` | Check rotation status |
| `rotate` | Mark a secret as rotated |
| `scan` | Scan .env files or environment |
| `stale` | Show stale/overdue secrets |
| `history` | View rotation history |
| `audit` | View audit log |
| `import` | Import secrets from .env |
| `export` | Export secret registry |
| `stats` | Show statistics |
| `config` | Show configuration |

## Service Presets

Predefined rotation policies:

- **90 days**: OpenAI, Resend, GitHub, DashScope
- **180 days**: Cloudflare, Firebase
- **365 days**: TransIP, Telegram

Custom policies can be specified per secret.

## Risk Levels

Secrets are automatically categorized by how long since last rotation:

- **FRESH**: < 30 days (last rotated recently)
- **OK**: 30-90 days (within normal window)
- **STALE**: 90-180 days (approaching limit)
- **CRITICAL**: > 180 days (urgent action needed)

## Database

Nex Keyring uses SQLite for local storage with these tables:

### secrets
- Core secret metadata
- Service and category classification
- Rotation policy and last rotation date
- Environment variable tracking
- Usage context and tags

### rotation_history
- Complete rotation event log
- Old and new key hashes
- Rotation source (manual/auto) and notes

### audit_log
- All actions on secrets
- View, rotate, add, remove, update operations
- Complete audit trail

## Data Security

**What Nex Keyring Never Stores:**
- Actual API key values
- Plain text credentials
- Passwords or tokens

**What Nex Keyring Tracks:**
- Secret name and service
- Key prefix (first 4 chars) for identification
- SHA256 hash for change detection
- Rotation history and dates
- Access audit log

**Encryption:**
- If `cryptography` is installed: Uses Fernet encryption
- Otherwise: Base64 obfuscation (recommended to install cryptography)

**Local Storage:**
- All data in `~/.nex-keyring/`
- Database file: `~/.nex-keyring/keyring.db`
- Never transmitted anywhere

## Export Formats

### JSON
```bash
nex-keyring export --format json
```
Structured metadata for programmatic access.

### CSV
```bash
nex-keyring export --format csv --output registry.csv
```
Spreadsheet format for security reviews.

### Markdown
```bash
nex-keyring export --format markdown --output registry.md
```
Human-readable report format.

## Examples

### Scenario: Initial Setup with Existing .env

```bash
# Scan your .env file
nex-keyring scan --env-file .env

# Import all found keys
nex-keyring import .env

# Review imported secrets
nex-keyring list

# Check current rotation status
nex-keyring check
```

### Scenario: Identify Overdue Keys

```bash
# Find keys past their rotation deadline
nex-keyring stale

# Focus on a specific service
nex-keyring check --service openai

# Show detailed status
nex-keyring show "OpenAI API Key"
```

### Scenario: Rotate a Key

```bash
# Before rotation - check current status
nex-keyring show "Cloudflare Token"

# After rotating in Cloudflare dashboard:
nex-keyring rotate "Cloudflare Token" --notes "Quarterly security rotation"

# Verify the rotation was recorded
nex-keyring history "Cloudflare Token"
```

### Scenario: Audit and Compliance

```bash
# Export for security audit
nex-keyring export --format csv --output audit_2026_Q1.csv

# View all recent actions
nex-keyring audit --limit 200

# Filter to specific secret
nex-keyring audit --secret "Stripe API Key"
```

### Scenario: Manage Multiple Teams

```bash
# Track keys used in production
nex-keyring add --name "Prod OpenAI Key" --used-in "production-api,worker-service"

# Track keys used in staging
nex-keyring add --name "Staging OpenAI Key" --used-in "staging-api"

# List all production keys
nex-keyring list | grep production

# Find all keys used by a specific service
nex-keyring audit | grep "worker-service"
```

## Troubleshooting

### Database locked error
- Ensure only one instance of nex-keyring is running
- Delete `~/.nex-keyring/keyring.db-wal` if it exists and retry

### Encryption warnings
Install cryptography for stronger encryption:
```bash
pip install cryptography
```

### Permission errors on .env scanning
Ensure the .env file is readable:
```bash
chmod 600 .env
nex-keyring scan --env-file .env
```

## Directory Structure

```
~/.nex-keyring/
├── keyring.db              # SQLite database
├── keyring.db-wal         # Write-ahead log (temporary)
├── keyring.db-shm         # Shared memory (temporary)
└── exports/               # Export directory
    ├── registry_*.json
    ├── registry_*.csv
    └── registry_*.md
```

## Dependencies

### Required
- Python 3.8+
- SQLite3 (built-in)

### Recommended
- `cryptography` - For Fernet encryption (strongly recommended for production)

Install cryptography:
```bash
pip install cryptography
```

## Configuration

### Defaults
- **Default Rotation Policy**: 90 days
- **Strict Policy**: 30 days
- **Stale Threshold**: > 90 days
- **Critical Threshold**: > 180 days

### Environment Variables
- `NEX_KEYRING_HOME`: Override default data directory
- `NEX_KEYRING_DB`: Override database path

### Service Presets
Edit `lib/config.py` `SERVICE_PRESETS` dict to customize:

```python
SERVICE_PRESETS = {
    "cloudflare": 180,
    "openai": 90,
    # Add or modify services here
}
```

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

---

Built by [Nex AI](https://nex-ai.be)
