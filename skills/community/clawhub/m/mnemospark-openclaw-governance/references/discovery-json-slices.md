# Safe discovery JSON slices

Pipe **only stdout** from `discover --json`. Never load the full JSON into context.

Replace `$GOV_ROOT` and filter values as needed.

## Cron and fan-out

```bash
# Fan-out groups (same name/schedule, different payloads)
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.cron_instance_groups[] | select(.kind == "fan_out") | {group_id, agent_id, name, job_count}'

# Exact duplicate warnings only
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.warnings[]? | select(.code == "EXACT DUPLICATE CRON")'

# Cron jobs for one agent
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.cron_jobs[] | select(.agent_id == "main") | {id, name, enabled, schedule}'
```

## Agent health during discovery

```bash
# Per-agent cron list status (timeouts/errors)
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.agent_statuses'

# Agents that failed during scan
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.errors'

# Agent ids discovered
openclaw-gov discover --json --root "$GOV_ROOT" | jq '[.agents[].agent_id]'
```

## Registry / inventory drift signals

```bash
# Staged candidate kinds (after discover --staged on disk, read discovery-candidates.json)
jq '[.candidates[]? | {id, kind, reason}]' "$GOV_ROOT/workflows/discovery-candidates.json"

# Inventory schema version
jq '.schema_version' "$GOV_ROOT/workflows/discovered-inventory.json"

# Count cron instance groups
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.cron_instance_groups | length'
```

## Runbook / workspace signals

```bash
# Workspace runbook candidates (paths only)
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.workspace_runbooks[]? | {agent_id, path, workflow_id}'

# Governance runbooks on disk
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.governance_runbooks[]? | .path'
```

## Git repos scanned (optional)

```bash
openclaw-gov discover --json --root "$GOV_ROOT" | jq '.git_repos[]? | {path, remote_url}'
```
