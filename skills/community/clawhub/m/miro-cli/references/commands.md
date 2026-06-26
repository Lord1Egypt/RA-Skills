# Miro CLI Command Reference

## Prerequisites

Before running any commands, ensure:
1. **mirocli installed:** `npm install -g mirocli` (verify package on https://www.npmjs.com/package/mirocli)
2. **Context added:** `mirocli context add` (prompts for Org ID, Client ID, Client Secret)
3. **Authenticated:** `mirocli auth login` (one-time OAuth flow)

**Credential Storage:**
- Credentials are managed by the external `mirocli` binary, not by this skill
- mirocli stores them in `~/.mirocli/` using system keyring (macOS Keychain, Linux Secret Service, Windows Credential Manager)
- **This skill does not store, cache, or transmit credentials**
- **You are trusting the mirocli binary to handle credentials securely**

## Trust Model

**What This Skill Does:**
- ✅ Documents how to use the `mirocli` command-line tool
- ✅ Provides helper shell scripts that call `mirocli` 
- ✅ Shows how to parse/filter output with `jq`
- ❌ Does NOT store credentials
- ❌ Does NOT execute code in your environment (shells scripts explicitly call external tools)
- ❌ Does NOT modify your system (aside from optional PATH suggestion)

**What You're Trusting:**
- **mirocli npm package** — External binary from npm registry (verify on npmjs.com)
- **System keyring** — Your OS's credential storage (controlled by your OS, not this skill)
- **Miro API** — Direct HTTPS calls to api.miro.com (official Miro endpoint)
- **jq binary** — JSON processor (standard Unix tool, pre-installed on most systems)
- **column binary** — Text formatter (standard Unix tool, pre-installed on most systems)

**What Can Go Wrong:**
- If mirocli is compromised, your Client ID/Secret/tokens could be at risk
- If you add scripts to PATH without understanding, you could accidentally run wrong commands
- If your system keyring is compromised, stored credentials could be exposed

**Recommendations:**
- Run mirocli commands in an isolated environment first
- Use a non-production Miro account for testing
- Review mirocli source code: https://github.com/davitp/mirocli
- Check npm package page for author, downloads, issues, recent updates

## Authentication Commands

```bash
mirocli auth login              # OAuth authentication (one-time)
mirocli auth whoami             # Display current user
mirocli auth token              # Show session token
mirocli auth state              # Check authentication status
mirocli auth info               # Show OAuth setup info
```

## Organization Commands

```bash
mirocli organization view       # View organization details
mirocli org view                # Shorthand
```

**Output includes:** Name, ID, owner, member count, subscription level

## Team Commands

### List Teams
```bash
mirocli teams list              # List all teams
mirocli teams list --json       # JSON output (for scripting)
mirocli teams list --name "Marketing"  # Filter by name
mirocli teams list -n "Design"         # Shorthand
```

**Filters:**
- `--name` — Team name (substring match)
- `--owner-id` — Filter by owner ID
- `--sort` — Sort field (name, created, modified)

**Output fields:** ID, name, owner, description, member count

## Board Commands

### List Boards
```bash
mirocli boards list             # All boards in organization
mirocli boards list --json      # JSON output (for scripting)
```

**Common filters:**
```bash
mirocli boards list --team-id <id>              # Filter by team
mirocli boards list --owner-id <id>             # Filter by owner
mirocli boards list --modified-after "2026-01-01"  # Date filter
mirocli boards list --sort "name"               # Sort by field
mirocli boards list --sort "modified" --desc    # Descending sort
```

**Sorting options:** `name`, `created`, `modified`

**Output fields:** ID, name, owner, description, created, modified, team ID

### Get Board Details
```bash
# Single board info is included in list output
mirocli boards list --board-id <id> --json | jq '.[] | select(.id == "<id>")'
```

## Board Export Commands (Enterprise)

### Export Board
```bash
mirocli board-export <board-id> --format pdf
mirocli board-export <board-id> --format png
mirocli board-export <board-id> --format svg
mirocli be <board-id> --format pdf              # Shorthand
```

**Formats:** `pdf`, `png`, `svg`

**Options:**
- `--output <path>` — Save to specific file
- `--format` — Output format (required)

## Content Logs (Enterprise)

### View Content Logs
```bash
mirocli content-logs            # All content logs
mirocli content-logs --board-id <id>    # Logs for specific board
mirocli content-logs --from "2026-01-01"        # Logs from date
mirocli content-logs --to "2026-03-14"          # Logs until date
mirocli cl --json               # JSON output, shorthand
```

**Filters:**
- `--board-id` — Filter by board
- `--from` — Start date (ISO 8601)
- `--to` — End date (ISO 8601)
- `--action` — Filter by action type

## Audit Logs (Enterprise)

### View Audit Logs
```bash
mirocli audit-logs              # All audit logs
mirocli audit-logs --from "2026-01-01"         # Logs from date
mirocli audit-logs --to "2026-03-14"           # Logs until date
mirocli al --action "board.updated"            # Filter by action
mirocli al --json               # JSON output
```

**Filters:**
- `--from` — Start date (ISO 8601)
- `--to` — End date (ISO 8601)
- `--action` — Filter by action (e.g., "board.updated", "board.created")
- `--user-id` — Filter by user

## Context Commands

### Manage Contexts
```bash
mirocli context add             # Add new context (interactive)
mirocli ctx add                 # Shorthand
mirocli -c <context-name> <command>     # Use specific context
```

**Example:** Multiple Miro organizations
```bash
mirocli context add             # Create "production" context
mirocli -c production boards list        # Use production context
mirocli -c default boards list           # Use default context
```

## Global Options

```bash
-c, --context <name>    # Specify context (default: default)
-h, --help             # Show help
-v, --version          # Show version
--json                 # JSON output (all list commands)
```

## Date Formats

Use ISO 8601 format:
- `2026-03-14` — Date only
- `2026-03-14T10:30:00Z` — Date and time (UTC)
- `2026-03-14T10:30:00-06:00` — Date and time with timezone

## JSON Output Examples

### Pretty-print all boards
```bash
mirocli boards list --json | jq '.'
```

### Get only board names and IDs
```bash
mirocli boards list --json | jq '.[] | {name, id}'
```

### Find board by name
```bash
mirocli boards list --json | jq '.[] | select(.name | contains("Design"))'
```

### Get owner names for all boards
```bash
mirocli boards list --json | jq '.[] | {name, owner: .owner.name}'
```

### Count boards by owner
```bash
mirocli boards list --json | jq 'group_by(.owner.name) | map({owner: .[0].owner.name, count: length})'
```

## Help

```bash
mirocli --help                  # Global help
mirocli <command> --help        # Command-specific help

# Examples:
mirocli boards --help
mirocli auth --help
mirocli organization --help
mirocli board-export --help
```

## Troubleshooting

**"No authenticated sessions"** → Run `mirocli auth login` first

**"Permission denied"** → Check organization/board permissions

**"Unknown command"** → Run `mirocli --help` to see available commands

**"Invalid context"** → Run `mirocli context add` to create a context
