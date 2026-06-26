---
name: parallel-monitor
description: "Continuously track the web for changes via the Parallel Monitor API. Creates a recurring research task that runs on a cadence and emits events on change — with optional webhook delivery. Use for 'monitor', 'track', 'watch', or 'alert me when' requests."
homepage: https://parallel.ai
---

# Parallel Monitor

Continuously track the web for changes. A monitor is a recurring research task that runs on a cadence (hourly / daily / weekly / every two weeks) and emits an event each cycle. Optionally deliver events to a webhook.

## When to Use

Trigger this skill when the user asks for:
- "monitor [thing]", "track changes to [thing]", "watch [page/topic]"
- "alert me when [X] changes / files / launches / posts"
- "keep an eye on [pricing page / competitor / SEC filings]"
- Recurring research that should re-run automatically without re-prompting

**Use Search for one-off lookups; use Monitor when the user wants ongoing observation.**

## Quick Start

```bash
parallel-cli monitor create "Track price changes for iPhone 16 Pro" --json
```

## CLI Reference

### Basic Usage

```bash
parallel-cli monitor create "<objective>" [options]
parallel-cli monitor list --json
parallel-cli monitor get mon_xxx --json
parallel-cli monitor update mon_xxx [options] --json
parallel-cli monitor delete mon_xxx
parallel-cli monitor events mon_xxx --json
parallel-cli monitor simulate mon_xxx --json
```

### Common Flags (create / update)

| Flag | Description |
|------|-------------|
| `-c, --cadence` | `hourly`, `daily` (default), `weekly`, `every_two_weeks` |
| `--webhook <url>` | Webhook URL for event delivery (required for `simulate`) |
| `--output-schema <json>` | JSON schema for structured event output |
| `--json` | Output as JSON |

### Examples

**Create a basic monitor (daily cadence):**
```bash
parallel-cli monitor create "Track new SEC filings from Tesla" --json
```

**Hourly monitor with webhook delivery:**
```bash
parallel-cli monitor create "New AI funding announcements" \
  --cadence hourly \
  --webhook https://example.com/hooks/funding \
  --json
```

**Structured-output monitor:**
```bash
parallel-cli monitor create "Track iPhone 16 Pro pricing on apple.com" \
  --output-schema '{"properties":{"price_usd":{"type":"number"},"in_stock":{"type":"boolean"}}}' \
  --json
```

**List existing monitors (default 10):**
```bash
parallel-cli monitor list --json
```

**Inspect events from a monitor:**
```bash
parallel-cli monitor events mon_xxx --json
```

**Test webhook delivery without waiting for a real cycle:**
```bash
parallel-cli monitor simulate mon_xxx --json
```

(`simulate` requires a `--webhook` was set on the monitor; otherwise it errors.)

**Update cadence on an existing monitor:**
```bash
parallel-cli monitor update mon_xxx --cadence weekly --json
```

**Delete a monitor:**
```bash
parallel-cli monitor delete mon_xxx
```

## Best-Practice Prompting

### Objective
Write 1-3 sentences describing:
- What signal the monitor should look for (e.g., "price changes", "new filings", "site outage")
- What "change" means (numeric threshold, new entity appearing, status flip)
- Source preference if relevant (e.g., "from sec.gov", "on the official pricing page")

### Cadence
Pick the slowest cadence that still catches the signal in time:
- `hourly` — breaking news, pricing fluctuations, status pages
- `daily` (default) — most ongoing tracking
- `weekly` / `every_two_weeks` — slow-moving topics, regulatory filings, executive changes

### Output Schema (optional)
Provide a JSON schema when you want structured per-event output (e.g., `{price_usd, in_stock}`). The Monitor API will populate that schema each cycle, making downstream automation easier.

## Response Format

`monitor create` and `monitor list` return JSON with fields like:
- `monitor_id` — `mon_xxx`
- `objective` — the natural-language description
- `cadence` — current schedule
- `webhook` — delivery URL (if set)
- `created_at` / `updated_at` — timestamps
- `last_event_at` — most recent event timestamp (if any)

`monitor events` returns an array of `{event_id, observed_at, output}` objects.

## Output Handling

When relaying monitor results to the user:
- Always echo the `monitor_id` so the user can manage the monitor later
- Default `monitor list` to `-n 10` to avoid megabyte-scale dumps in long-lived workspaces
- For `events` output, summarize the trend across cycles, not just the latest event

## Running Out of Context?

For long-running monitor management sessions, save state and use `sessions_spawn`:

```bash
parallel-cli monitor list --json -o /tmp/monitors.json
```

Then spawn a sub-agent:
```json
{
  "tool": "sessions_spawn",
  "task": "Read /tmp/monitors.json and produce a summary of active monitors grouped by cadence.",
  "label": "monitor-summary"
}
```

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Unexpected error (network, parse) |
| 2 | Invalid arguments |
| 3 | API error (non-2xx) |

## Prerequisites

Requires `parallel-cli` (installed and authenticated). If `parallel-cli --version` fails, or if a later command fails with an authentication error, tell the user to see https://docs.parallel.ai/integrations/cli and stop.

## References

- [API Docs](https://docs.parallel.ai)
- [Monitor API Reference](https://docs.parallel.ai/api-reference/monitor)
