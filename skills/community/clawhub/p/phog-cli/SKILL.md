---
name: posthog-cli
description: Manage PostHog product analytics from the terminal. Use when the user asks about PostHog analytics, feature flags, experiments, surveys, dashboards, insights, error tracking, logs, queries, or product health metrics. Also use when the user wants to analyze their product data, check active users, review traffic sources, or run HogQL queries against PostHog.
license: MIT
compatibility: Requires Python 3.10+ and pip. The CLI command is `posthog` (installed via `pip install phog-cli`).
metadata:
  author: nelsongallardo
  version: "0.1.0"
  repository: https://github.com/nelsongallardo/posthog-cli
---

# PostHog CLI (phog-cli)

A community-built CLI for PostHog product analytics. Not affiliated with PostHog Inc.

## Installation

```bash
pip install phog-cli
```

The CLI command is `posthog`. Verify with `posthog --version`.

## Authentication

Check if already authenticated, then login if needed:

```bash
posthog auth status
posthog auth login          # auto-detects US/EU cloud
```

For self-hosted: `posthog auth login --host https://posthog.company.com`

For non-interactive/CI use, set environment variables instead:

```bash
export POSTHOG_API_KEY="phx_..."
export POSTHOG_HOST="https://us.posthog.com"
export POSTHOG_PROJECT_ID="12345"
```

## Project Selection

Most commands need an active project:

```bash
posthog project list
posthog project switch <project-id>
posthog project current
```

## Global Flags

Use with ANY command:

- `--json` / `-j` — Machine-readable JSON output. **Always use this when parsing output programmatically.**
- `--yes` / `-y` — Skip confirmation prompts. **Always use this for non-interactive automation.**
- `--help` — Show help for any command.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `posthog activity summary` | Full product health report (WAU, events, traffic, pages, browsers) |
| `posthog activity users` | Active users over time (daily/weekly/monthly) |
| `posthog activity events` | Top events by volume |
| `posthog flag list` | List feature flags |
| `posthog flag create --key KEY --name NAME` | Create a feature flag |
| `posthog experiment list` | List A/B experiments |
| `posthog experiment results ID` | View experiment results |
| `posthog survey list` | List surveys |
| `posthog dashboard list` | List dashboards |
| `posthog insight list` | List saved insights |
| `posthog insight query ID` | Execute a saved insight's query |
| `posthog error list` | List error tracking issues |
| `posthog log query` | Query logs |
| `posthog query run --hogql "SQL"` | Run a HogQL query |
| `posthog query generate "question"` | Generate HogQL from natural language |
| `posthog search persons --search "email"` | Search persons |
| `posthog api get /path/` | Raw API escape hatch |

For detailed command options, see [references/commands.md](references/commands.md).

## Common Workflows

### Product Health Check

```bash
posthog --json activity summary --date-from -30d
```

Returns WAU trends, all custom events with unique user counts, weekly trend breakdowns, traffic sources, top pages, and browser stats in a single call.

### Custom Analytics with HogQL

HogQL is a SQL-like language for querying PostHog data.

```bash
# Count distinct users for a specific event
posthog query run --hogql "SELECT count(distinct person_id) FROM events WHERE event = 'purchase' AND timestamp > now() - interval 30 day"

# Weekly trends
posthog query run --hogql "SELECT toStartOfWeek(timestamp) as week, count() as c FROM events WHERE event = 'signup' AND timestamp > now() - interval 90 day GROUP BY week ORDER BY week"

# Traffic sources
posthog query run --hogql "SELECT properties.\$referring_domain as source, count(distinct person_id) as users FROM events WHERE event = '\$pageview' AND timestamp > now() - interval 30 day AND properties.\$referring_domain IS NOT NULL AND properties.\$referring_domain != '' GROUP BY source ORDER BY users DESC LIMIT 10"

# Funnel conversion
posthog query run --hogql "SELECT count(distinct person_id) as started, countIf(distinct person_id, person_id IN (SELECT distinct person_id FROM events WHERE event = 'purchase' AND timestamp > now() - interval 30 day)) as converted FROM events WHERE event = 'add_to_cart' AND timestamp > now() - interval 30 day"
```

**HogQL essentials:**
- Events table: `events` — columns: `event`, `timestamp`, `person_id`, `properties`
- Access properties: `properties.$current_url`, `properties.$browser`, `properties.$referring_domain`
- System events are `$`-prefixed: `$pageview`, `$pageleave`, `$autocapture`, `$set`
- Custom events have no prefix: `purchase`, `signup`, `file_upload`
- Time: `now()`, `toStartOfWeek(timestamp)`, `toStartOfMonth(timestamp)`
- Distinct users: `count(distinct person_id)`

### Feature Flag Rollout

```bash
posthog flag create --key new-feature --name "New Feature" --rollout-percentage 10
posthog flag update <id> --rollout-percentage 50
posthog flag update <id> --rollout-percentage 100
```

### Run an Experiment

```bash
posthog experiment create --name "CTA Test" --feature-flag-key cta-test
posthog experiment update <id> --launch
posthog experiment results <id> --refresh
posthog experiment update <id> --end
```

### Raw API Escape Hatch

For anything the CLI doesn't cover:

```bash
posthog api get /path/
posthog api post /path/ --data '{"key": "value"}'
posthog api patch /path/ --data '{"key": "value"}'
posthog api delete /path/
```

## Error Handling

- `API error 401` — Invalid credentials. Run `posthog auth login`.
- `API error 404` — Resource not found or wrong endpoint path.
- `No active project` — Run `posthog project list` then `posthog project switch <id>`.
- All errors exit with code 1 and print to stderr.

## Notes

- This is a community-built CLI (`pip install phog-cli`), not an official PostHog product.
- PostHog has US (`us.posthog.com`) and EU (`eu.posthog.com`) cloud regions — the CLI auto-detects on login.
- Config stored at `~/.config/posthog-cli/config.json` (600 permissions).
- Environment variables override config: `POSTHOG_API_KEY`, `POSTHOG_HOST`, `POSTHOG_PROJECT_ID`.
