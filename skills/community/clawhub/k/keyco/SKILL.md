---
name: keyco
description: Manage Keyco assets, DUBs (QR/NFC/BLE/Virtual beacons), workflows, lifecycle events, users, and analytics. Use when the user asks about Keyco, asset management, DUB tracking, asset lifecycle, workflow automation, or mentions qrdub.com / keyco.io. Supports reading inventory, checking compliance, running reports, and creating lifecycle events via the Keyco CLI.
license: MIT
---

# Keyco Skill

This skill uses the Keyco CLI to manage assets (DUBs), workflows, lifecycle events, users, notifications, and analytics through the Keyco platform (api.qrdub.com).

## When to Use This Skill

Invoke this skill when the user:
- Asks about Keyco assets, DUBs, or inventory
- Needs to look up a specific asset by UUID
- Wants to check asset lifecycle events, maintenance, or compliance
- Requests workflow status, asset assignments, or utilization reports
- Asks for analytics (weekly digest, stale assets, summaries)
- Wants to manage notifications, groups, or API keys
- Mentions `api.qrdub.com`, `keyco.io`, `kc_live_*`, or the `keyco` CLI
- Wants to script asset operations (bulk ops, CI/CD automation)

## Prerequisites

Before running any command, verify the CLI is installed and configured:

1. Check if `keyco` is on PATH: `which keyco`
2. Check configuration: `keyco status`
3. **If either check fails, run the setup script** — it handles install + configure in one shot:
   ```bash
   bash scripts/setup-keyco.sh
   ```
   The script will:
   - Install `@keyco/cli` globally via npm if missing (falling back to `sudo npm` if needed)
   - Skip install if already present
   - Walk the user through `keyco configure` if no valid API key is set
   - Verify connectivity at the end

   Always offer to run this script before failing — don't ask the user to manually install or configure.

## Core Workflow

### 1. Identify the user's intent
Map their request to one of the Keyco domains:
| Intent | Command family |
|---|---|
| Look up asset / inventory | `keyco dub get`, `keyco dub list`, `keyco dub search` |
| Asset location / tracking | `keyco dub location history`, `keyco dub map-data` |
| Lifecycle events | `keyco lifecycles create`, `keyco lifecycles get` |
| Workflows | `keyco workflows list`, `keyco workflows get`, `keyco workflows dubs` |
| Users & assignments | `keyco user list`, `keyco user assigned-dubs`, `keyco user unassigned-dubs` |
| Analytics & reports | `keyco analytics summary`, `keyco analytics weekly-digest`, `keyco analytics stale-assets` |
| Groups | `keyco groups list`, `keyco groups dubs` |
| Notifications | `keyco notifications list`, `keyco notifications unread-count` |
| API keys | `keyco api-keys list`, `keyco api-keys create` |

### 2. Run commands with `--output json` for programmatic parsing
Always append `--output json` when you need to parse or transform the data. Use `--output table` only when displaying directly to the user.

### 3. Handle errors
- **401 / 403**: API key missing, expired, or lacking required scope — tell the user to run `keyco configure` or create a key with the needed scope
- **404**: Resource doesn't exist — double-check the UUID with the user
- **429**: Rate limited — back off and retry
- **Connection errors**: Check `keyco status` to verify reachability

### 4. Summarize results for the user
Don't just dump raw JSON — extract the key fields and present them clearly. Offer follow-up actions (e.g., "Want me to check its location history too?").

## Data Integrity — IMPORTANT

The following operations have been intentionally removed from the Keyco CLI because they bypass authoritative scan/heartbeat events and break the audit trail:

- Manual DUB location updates
- Marking workflows complete out-of-band
- Advancing workflow steps without a verified DUB scan

**Never** try to work around these restrictions. If the user asks to "set" or "update" a DUB's location or manually complete a workflow, explain that these actions must happen via the physical scan/event flow (QR scan, NFC tap, BLE heartbeat) to preserve audit integrity. Direct them to support@keycomagix.com if they need an override for legitimate reasons.

## Output Format

When presenting asset data to the user:

```
Asset: <dubname>
UUID: <uuid>
Type: <QR | Pro | Active | Virtual>
Status: <active | inactive>
Group: <group name>
Assigned to: <user email or "Unassigned">
Last seen: <timestamp>
```

When running analytics, lead with the top-line numbers, then break down by category.

## Examples

**User:** "What assets does alice@company.com have?"
→ `keyco user list --output json` to find her user ID, then
→ `keyco user assigned-dubs --user-id <UUID> --output json`
→ Summarize: "Alice has N assets assigned: [list]"

**User:** "Create a maintenance event for DUB ee6f2f42-31b1-4f90-9440-e91fb02ac7c4 due next Friday"
→ Compute the absolute date from "next Friday"
→ `keyco lifecycles create --event-type MAINTENANCE --name "Maintenance" --assigned-dub ee6f2f42-31b1-4f90-9440-e91fb02ac7c4 --due-date 2026-04-24`
→ Confirm creation to the user with the returned event ID

**User:** "Show me this week's analytics"
→ `keyco analytics weekly-digest --output json`
→ Summarize top-line metrics (total assets, active workflows, open lifecycle events, utilization %)

**User:** "Find any stale assets"
→ `keyco analytics stale-assets --output json`
→ Report the count and list the first few, offering to create maintenance events or reassign them

**User:** "Import 50 assets from this CSV"
→ Explain that bulk CSV import goes through `POST /api/imports/upload` (not yet in CLI) — suggest they use the dashboard at https://dashboard.qrdub.com or loop over `keyco lifecycles create` / asset endpoints individually

## Scripting Recipes

For multi-step tasks, compose commands with standard shell tools:

```bash
# Export all DUBs as JSON
keyco dub list --size 1000 --output json > all-dubs.json

# Find assets with no assigned user
keyco user unassigned-dubs --output json | jq '.[] | .uuid'

# Stale asset count for CI
STALE=$(keyco analytics stale-assets --output json | jq '.totalElements')
echo "$STALE stale assets detected"
```

## References

- [Full CLI command reference](references/cli-commands.md)
- [API scope reference](references/scopes.md)
- [Data integrity guidelines](references/data-integrity.md)
- Keyco docs: https://docs.qrdub.com
- Keyco dashboard: https://dashboard.qrdub.com
