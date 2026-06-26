---
name: miro-cli
description: Miro CLI tool for board/team/org management via command line. Use when querying boards, exporting data, viewing teams/organizations, or automating Miro workflows from the terminal.
required_binaries:
  - mirocli
  - jq
  - column
required_credentials:
  - miro_org_id
  - miro_client_id
  - miro_client_secret
metadata:
  openclaw:
    type: cli-tool
    trust_model: external-binary-managed-credentials
    requires:
      binaries:
        - mirocli
        - jq
        - column
      system_tools:
        - bash
      credentials:
        miro_org_id: Organization ID from Miro settings
        miro_client_id: OAuth Client ID from Miro app
        miro_client_secret: OAuth Client Secret (stored in system keyring, NOT in skill)
    install:
      - id: mirocli
        package: davitp/mirocli
        kind: npm
        command: npm install -g mirocli
        required: true
        verify_url: https://www.npmjs.com/package/mirocli
      - id: jq
        package: jq
        kind: homebrew
        command: brew install jq
        required: false
        note: Optional but recommended for JSON filtering
      - id: column
        package: util-linux
        kind: system
        command: Usually pre-installed
        required: false
        note: Optional for table formatting in helper scripts
    security:
      external_binary: true
      binary_name: mirocli
      manages_credentials: true
      credential_storage: system-keyring
      credential_scope: local-only
    capabilities:
      - read-boards
      - read-teams
      - read-organization
      - export-boards
      - view-audit-logs
      - view-content-logs
    limitations:
      - read-only (no create/update/delete)
      - requires-oauth-setup
      - trusts-external-npm-package
---

# Miro CLI Skill

A comprehensive guide for using the Miro CLI tool to interact with the Miro Platform API from the command line.

## ⚠️ Trust Model & Security Declaration

**Metadata Declaration:**
- Type: CLI tool wrapper (external binary management)
- External Binary: `mirocli` (npm package: davitp/mirocli)
- Manages Credentials: YES (stores in system keyring, NOT in skill)
- Credential Storage: System keyring (local-only, OS-managed)
- Capabilities: Read-only access to boards, teams, organization, logs
- Limitations: No create/update/delete; requires OAuth setup

**Critical Trust Requirements:**

**1. You must trust the `mirocli` npm package:**
- Author: @davitp (community-maintained, not official Miro)
- Package: https://www.npmjs.com/package/mirocli
- Source: https://github.com/davitp/mirocli
- Verification: Check npm downloads, last update date, issues, GitHub stars
- **Why it matters:** This external binary handles your Client ID, Client Secret, and OAuth tokens

**2. You must trust your system keyring:**
- macOS: Keychain
- Linux: Secret Service
- Windows: Credential Manager
- **This skill does NOT:** Store credentials, cache tokens, or transmit them

**3. Helper binaries are standard Unix tools:**
- `jq` — JSON processor (widely used, open source)
- `column` — Text formatter (standard utility)
- These are optional and do NOT handle credentials

**4. Network access:**
- Direct HTTPS calls to api.miro.com (official Miro endpoint)
- OAuth browser-based authentication on your machine
- No data proxying or credential transmission through third parties

**Recommendation:**
Before using with production credentials:
1. Review mirocli source code: https://github.com/davitp/mirocli
2. Test with a non-sensitive Miro account
3. Verify OAuth token storage in `~/.mirocli/`
4. Run in isolated environment initially

## What It Does

Miro CLI enables command-line access to Miro resources and enterprise features:
- **Boards** — List, search, and manage boards
- **Teams** — View and organize teams
- **Organization** — View org details and members
- **Board Export** — Export boards as PDF, PNG, SVG
- **Content Logs** — View activity/change logs (enterprise)
- **Audit Logs** — Access audit logs (enterprise)

Perfect for automation, scripting, and bulk operations.

## Requirements

**Binaries (required):**
- `mirocli` — Miro CLI tool (installed via npm)
- `jq` — JSON query processor (for filtering/scripting)
- `column` — Text column formatter (for table output in helper scripts)

**Credentials (interactive entry required):**
- Organization ID — Your Miro organization identifier
- Client ID — OAuth app client ID
- Client Secret — OAuth app client secret

**Optional (for JSON workflows):**
- `jq` — JSON processor for advanced filtering and data transformation

## Installation & Setup

### 1. Install Dependencies

**mirocli** (required):
```bash
npm install -g mirocli
```

**jq** (optional, but recommended):
```bash
# macOS
brew install jq

# Linux (Debian/Ubuntu)
sudo apt install jq

# Linux (Fedora)
sudo dnf install jq
```

### 2. Configure Context (One-time)

```bash
mirocli context add
```

This will prompt for:
- Context name (e.g., `default`)
- Organization ID (from your Miro settings)
- Client ID (from your Miro app)
- Client Secret (from your Miro app)

Credentials are stored securely by mirocli in `~/.mirocli/` (system keyring on macOS/Linux).

### 3. Authenticate with OAuth

```bash
mirocli auth login        # Opens browser for OAuth flow
mirocli auth whoami       # Verify authentication
```

## Quick Start

### View Organization
```bash
mirocli organization view
```

### List Boards
```bash
mirocli boards list                    # All boards
mirocli boards list --json             # JSON output
mirocli boards list --team-id <id>     # Filter by team
mirocli boards list --sort "name"      # Sort by field
```

### List Teams
```bash
mirocli teams list
mirocli teams list --name "Design"     # Filter by name
mirocli teams list --json
```

### Export Board
```bash
mirocli board-export <board-id> --format pdf
mirocli board-export <board-id> --format png
mirocli board-export <board-id> --format svg
```

## Common Workflows

### Find Board by Name
```bash
mirocli boards list --json | jq '.[] | select(.name | contains("Design"))'
```

### Export All Boards from Team
See `scripts/export-team-boards.sh`

### List Boards with Owner Info
```bash
mirocli boards list --json | jq '.[] | {name, id, owner: .owner.name}'
```

### Filter Boards by Date
```bash
mirocli boards list --modified-after "2026-03-01" --json
```

## Setup Flow

1. **Install dependencies** → `npm install -g mirocli` (+ jq/column if needed)
2. **Add context** → `mirocli context add` (enter Org ID, Client ID, Client Secret interactively)
3. **Authenticate** → `mirocli auth login` (browser opens for OAuth, one-time)
4. **Verify** → `mirocli auth whoami` (confirm authentication works)
5. **Use CLI** → `mirocli boards list`, `mirocli teams list`, etc.

**Credential Storage:** mirocli stores credentials in `~/.mirocli/` using system keyring (secure, local-only)

## Global Options

```bash
-c, --context <name>    # Use specific context
-h, --help             # Show help
-v, --version          # Show version
--json                 # Output as JSON
```

## Security & Trust

**How Credentials Are Handled:**

- **Stored locally** — mirocli uses system keyring (secure, local-only)
- **Not in skill** — Credentials are entered interactively via `mirocli context add`
- **OAuth token** — mirocli manages OAuth session tokens; they never leave your machine
- **Exports** — Board exports are saved locally; no data sent to third parties beyond Miro API

**What This Skill Does:**

- ✅ Reads/lists boards, teams, org data via Miro API
- ✅ Exports boards as PDF/PNG/SVG
- ✅ Views activity/audit logs (enterprise)
- ❌ Never modifies boards/teams (read-only commands only)
- ❌ Never stores credentials in skill bundle
- ❌ Never sends data outside of Miro API calls

**Third-party Trust:**

This skill relies on:
- **mirocli** (npm package) — External CLI tool that handles credential storage
- **Miro API** — Direct calls to Miro's official API endpoints
- **System keyring** — OS-level credential storage (macOS Keychain, Linux Secret Service, Windows Credential Manager)

## Command Reference

See `references/miro-cli-commands.md` for detailed command documentation.

## Help

```bash
mirocli --help
mirocli <command> --help
```

## Related Skills

- `miro-mcp` — MCP integration for Miro (AI coding tools)
- `miro-sdk` — Web SDK reference for building plugins
- `miro-api` — REST API reference for programmatic access

---

**Setup Date:** 2026-03-14  
**Last Updated:** 2026-03-14  
**Status:** Ready (OAuth login pending)
