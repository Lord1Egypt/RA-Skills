---
name: hopkin-skill
description: Query ad platform data (Meta, Google, LinkedIn, Reddit) using the Hopkin CLI. Use this skill when the user asks about ad accounts, campaigns, ad performance, or any advertising platform data.
version: 0.1.0
---

# Hopkin CLI Skill

## When to Use

Use this skill when the user:
- Asks about ad accounts, campaigns, ad sets, ads, or ad performance
- Wants to query Meta Ads, Google Ads, LinkedIn Ads, or Reddit Ads data
- Needs cross-platform advertising reports or comparisons
- References Hopkin, MCP ad servers, or ad platform APIs
- Asks to list, inspect, or analyze advertising entities

Do NOT use this skill for:
- General marketing questions unrelated to ad platform data
- Creating or modifying campaigns (Hopkin is read-only)
- Non-advertising analytics (website analytics, SEO, etc.)

## Setup

### Installation

Before using Hopkin, ensure it's installed and up to date:

```bash
# Install globally from npm
npm install -g @hopkin/cli

# Or if already installed, check if an update is needed (do this if last check was >7 days ago)
npm outdated -g @hopkin/cli && npm install -g @hopkin/cli@latest
```

### Authentication

Check if the user is authenticated before making any data requests:

```bash
hopkin auth status --json
```

If not authenticated, ask the user for their API key:

```bash
hopkin auth set-key <API_KEY>
```

Users can get an API key from https://app.hopkin.ai/settings/api-keys

### Discover Available Commands

After authenticating, run `hopkin --help` to see all platforms, commands, and global flags. This also automatically refreshes the tool cache if it's stale (cache lasts 7 days).

```bash
hopkin --help
```

Then drill down into a specific platform to see its resources and commands:

```bash
hopkin meta --help
hopkin google --help
hopkin linkedin --help
hopkin reddit --help
```

And further into a resource to see its verbs and a specific command to see its flags:

```bash
hopkin meta campaigns --help
hopkin meta campaigns list --help
```

Always use `--help` to discover what's available before guessing command names — platforms differ in their resource naming and available tools.

## How to Use

### Query Data

The CLI follows a consistent pattern:

```
hopkin <platform> <resource> [verb] [flags]
```

- **platform**: `meta`, `google`, `linkedin`, `reddit`
- **resource**: `ad-accounts`, `campaigns`, `adsets`, `ads`, etc.
- **verb**: `list`, `get` (defaults to `list` if omitted)
- **flags**: `--reason` (required for most commands), `--account`, `--limit`, etc.

### Common Commands

```bash
# List ad accounts
hopkin meta ad-accounts list --reason "checking accounts" --json
hopkin google accounts list --reason "listing accounts" --json

# List campaigns for an account
hopkin meta campaigns list --account <ACCOUNT_ID> --reason "reviewing campaigns" --json

# Get performance insights
hopkin meta insights --account <ACCOUNT_ID> --reason "performance review" --json

# Ping a platform (health check)
hopkin meta ping --reason "connectivity test" --json
```

### Format Output

Always use `--json` when processing data programmatically. Other formats are available:

```bash
# JSON (best for parsing)
hopkin meta ad-accounts list --reason "..." --json

# CSV (for spreadsheet export)
hopkin meta ad-accounts list --reason "..." --format csv

# TSV
hopkin meta ad-accounts list --reason "..." --format tsv

# Filter specific fields
hopkin meta ad-accounts list --reason "..." --json --fields id,name,currency

# Fetch all pages (for large result sets)
hopkin meta ad-accounts list --reason "..." --json --all
```

## Important Notes

- **Read-only**: Hopkin cannot modify campaigns, change budgets, or edit ads. It only reads data.
- **`--reason` flag**: Most commands require `--reason "..."` for audit trail purposes. Always include a brief, honest description of why you're querying the data.
- **Account IDs**: Many commands require `--account <ID>`. List accounts first to discover available IDs.
- **Pagination**: Results are paginated by default (25 per page). Use `--all` to fetch everything, or `--limit N` to control page size.
- **Caching**: The MCP servers cache data. Pass `--refresh` to a command if the user needs real-time data.
- **Platform differences**: Not all platforms have the same resources. Google has `accounts` (not `ad-accounts`), LinkedIn has `campaign-groups` and `creatives` (not `adsets` and `ads`). Always check `hopkin <platform> --help` first.

## Update Check

Before each session where you use Hopkin, check if the CLI needs updating. Do this if you haven't checked in the last 7 days:

```bash
hopkin --version
npm view @hopkin/cli version
```

If the npm version is newer, update:

```bash
npm install -g @hopkin/cli@latest
```

## Troubleshooting

```bash
# Check auth status
hopkin auth status --json

# Debug a failing command
hopkin meta ad-accounts list --reason "debug" --json --debug

# Re-authenticate
hopkin auth set-key <NEW_KEY>

# Re-discover available commands (also refreshes tool cache)
hopkin --help
```
