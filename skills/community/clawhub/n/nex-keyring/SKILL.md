---
name: nex-keyring
description: Local API key and secret rotation management system for tracking and securing all API credentials, tokens, and database passwords. Monitor API keys from popular services (OpenAI, Cloudflare, Firebase, GitHub, Stripe, Telegram, DashScope/Qwen, TransIP) and custom credentials. Never stores actual key values, only cryptographic hashes for change detection. Track rotation status and days since last rotation with automatic risk level assessment (FRESH under 30 days, OK 30-90 days, STALE 90-180 days, CRITICAL over 180 days). Detect stale credentials that haven't been rotated recently and enforce organization-specific rotation policies (typical: 90 days for API keys, 180 days for infrastructure tokens). Scan .env files and environment variables to auto-detect and register all API keys and secrets with appropriate service categories and rotation policies. Generate audit logs for every access, rotation, and modification event for compliance documentation. Export credential registries (metadata only, never actual keys) in CSV, JSON, or Markdown formats for security audits. Ideal for DevOps engineers, system administrators, and development teams managing multiple credentials across systems and services.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🔑"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-keyring.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Keyring

Local API key and secret rotation tracker. Monitor and manage all your API keys, webhooks, and credentials in one place. Track rotation status, detect stale keys, and enforce security policies. All data stays securely on your machine.

## When to Use

Use this skill when the user asks about:

- API keys, secrets, tokens, or credentials
- Key rotation, rotation status, or rotation policies
- Which API keys haven't been rotated recently
- Stale or overdue credentials
- Tracking API keys from specific services (OpenAI, Cloudflare, Firebase, etc.)
- Scanning .env files for secrets
- Importing keys from environment files
- Security audit or credential management
- Credential expiration or rotation history
- Monitoring webhook or database secrets
- Password, wachtwoord, sleutel (Dutch for "key")
- API security or secret management

Trigger phrases: "API key", "secret rotation", "which keys need rotation", "stale credentials", ".env file", "rotate key", "track secrets", "credential management", "security audit", "API token", "webhook", "database password", "rotation status", "scan environment"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory (~/.nex-keyring), initializes the database, and verifies dependencies.

## Available Commands

The CLI tool is `nex-keyring`. All commands output plain text.

### Add a Secret

Register a new API key or secret:

```bash
nex-keyring add --name "OpenAI API Key" --service openai --category API --env-var OPENAI_API_KEY --rotation 90
nex-keyring add --name "Cloudflare Token" --service cloudflare --description "Production API token" --rotation 180
nex-keyring add --name "Database Password" --service postgresql --category DATABASE --used-in "production app"
```

**Options:**
- `--name` (required): Secret name (must be unique)
- `--service`: Service name (e.g., openai, cloudflare, firebase)
- `--category`: API, DATABASE, SSH, OAUTH, WEBHOOK, SMTP, DNS, HOSTING, AI, PAYMENT, OTHER
- `--env-var`: Environment variable name to track (e.g., OPENAI_API_KEY)
- `--rotation`: Rotation policy in days (default: 90, or service preset)
- `--description`: Human-readable description
- `--tags`: Comma-separated tags for organization
- `--used-in`: Project or script names using this key

### List Secrets

Show all tracked secrets:

```bash
nex-keyring list
nex-keyring list --service openai
nex-keyring list --category API
nex-keyring list --category DATABASE
```

### Show Secret Details

Display detailed information (never shows actual key values):

```bash
nex-keyring show "OpenAI API Key"
nex-keyring show "Cloudflare Token"
```

Shows:
- Service and category
- Creation and last rotation dates
- Rotation policy and days since rotation
- Risk level (FRESH, OK, STALE, CRITICAL)
- Environment variable tracking
- Usage context

### Check Rotation Status

Check which keys need rotation:

```bash
nex-keyring check
nex-keyring check --service openai
nex-keyring check --all
```

Reports overdue and stale keys with:
- Days since last rotation
- Risk level assessment
- Rotation recommendations

### Mark as Rotated

Record a rotation event:

```bash
nex-keyring rotate "OpenAI API Key"
nex-keyring rotate "OpenAI API Key" --hash abc123def456... --notes "Routine rotation"
```

The tool prompts for the new key hash if not provided. Hash is used to detect key changes without storing the actual key.

### Scan Environment

Scan .env files or environment variables for API keys:

```bash
nex-keyring scan --env-file .env
nex-keyring scan --env-file /path/to/.env.production
nex-keyring scan --environment
```

Detects:
- Known service patterns (OPENAI_, CF_, FIREBASE_, etc.)
- Whether values are set
- Key names for tracking

### Import from .env

Auto-register all keys from a .env file:

```bash
nex-keyring import .env
nex-keyring import .env.production --auto-register
```

Creates tracked secrets for each detected key with appropriate service detection and rotation policies.

### Show Stale/Overdue Keys

List all keys needing attention:

```bash
nex-keyring stale
```

Shows:
- Stale secrets (>90 days without rotation)
- Overdue secrets (past their rotation policy)
- Days since last rotation
- Risk levels

### View Rotation History

Check rotation history for a specific key:

```bash
nex-keyring history "OpenAI API Key"
nex-keyring history "Cloudflare Token"
```

Displays:
- All rotation events with dates
- Who/what rotated the key (manual/auto)
- Rotation notes

### Export Secrets

Export secret registry (metadata only, never actual keys):

```bash
nex-keyring export --format json
nex-keyring export --format csv --output registry.csv
nex-keyring export --format markdown --output registry.md
```

Formats: JSON, CSV, Markdown (metadata only, no sensitive data)

### View Audit Log

Show all actions on tracked secrets:

```bash
nex-keyring audit
nex-keyring audit --limit 100
nex-keyring audit --secret "OpenAI API Key"
```

Tracks:
- All secret accesses
- Rotation events
- Creation and deletion
- Modifications

### Statistics

Overview of tracked secrets:

```bash
nex-keyring stats
```

Shows:
- Total tracked secrets
- Stale and overdue counts
- Breakdown by category and service

### Configuration

Show system configuration:

```bash
nex-keyring config
```

Displays:
- Data storage location
- Encryption method
- Default rotation policies
- Service presets

## Data Security

- **No key storage**: Never stores actual API key values, only hashes for change detection
- **Local only**: All data stored in ~/.nex-keyring, never transmitted
- **Encryption**: Uses Fernet (recommended) or base64 obfuscation if cryptography unavailable
- **Audit trail**: Complete audit log of all access and modifications
- **Safe exports**: Exported data contains metadata only, no sensitive values

## Service Presets

Automatic rotation policies for common services:

- Cloudflare: 180 days
- OpenAI: 90 days
- Resend: 90 days
- Firebase: 180 days
- GitHub: 90 days
- TransIP: 365 days
- DashScope/Qwen: 90 days
- Stripe: 90 days
- Telegram: 365 days

Custom policies can be set per secret.

## Risk Levels

Secrets are assessed based on time since last rotation:

- **FRESH**: < 30 days (green status)
- **OK**: 30-90 days (normal)
- **STALE**: 90-180 days (warning)
- **CRITICAL**: > 180 days (action required)

## Examples

**Scenario: Onboard new API keys**

```bash
# Scan your .env file
nex-keyring scan --env-file .env

# Import all found keys
nex-keyring import .env

# Review what was added
nex-keyring list

# Check current rotation status
nex-keyring check
```

**Scenario: Identify overdue keys**

```bash
# Show all stale and overdue secrets
nex-keyring stale

# Check specific service
nex-keyring check --service stripe
```

**Scenario: Rotate a key**

```bash
# Show current details
nex-keyring show "OpenAI API Key"

# After rotating the key in OpenAI dashboard:
nex-keyring rotate "OpenAI API Key" --notes "Monthly rotation"

# Verify rotation was recorded
nex-keyring history "OpenAI API Key"
```

**Scenario: Export for audit**

```bash
# Export metadata for security review
nex-keyring export --format csv --output audit_$(date +%Y%m%d).csv

# View rotation history for compliance
nex-keyring audit --limit 200
```

## Dependencies

- Python 3.8+
- SQLite3 (built-in)
- Optional: `cryptography` (for Fernet encryption, recommended)

Install cryptography for stronger encryption:

```bash
pip install cryptography
```

Without it, keys are obfuscated with base64 (not recommended for production).

---

Built by [Nex AI](https://nex-ai.be) | MIT-0 License
