---
name: google-calendar-cli
description: Google Calendar management via the gog CLI tool. Create, list, update, and delete calendar events with color support, OAuth authentication, and scripting capabilities. Use when working with Google Calendar events, scheduling meetings, checking availability, or managing calendar entries from the command line.
---

# Google Calendar CLI

Manage Google Calendar events efficiently using the gog command-line tool.

## Prerequisites

### Install gog
```bash
brew install steipete/tap/gogcli
```

### Authentication Setup
```bash
# Set up OAuth credentials
gog auth credentials /path/to/client_secret.json

# Add your Google account with calendar access
gog auth add you@gmail.com --services calendar

# Verify authentication
gog auth list
```

## Quick Start

### List Events
```bash
# List events from primary calendar (today's events)
gog calendar events primary --from "2026-01-01T00:00:00Z" --to "2026-01-01T23:59:59Z"

# List events for next 7 days
gog calendar events primary --from "$(date -u +%Y-%m-%dT00:00:00Z)" --to "$(date -u -v+7d +%Y-%m-%dT23:59:59Z)"
```

### Create Event
```bash
# Create a basic event
gog calendar create primary --summary "Team Meeting" --from "2026-01-15T14:00:00+01:00" --to "2026-01-15T15:00:00+01:00"

# Create with color
gog calendar create primary --summary "Important Deadline" --from "2026-01-20T00:00:00+01:00" --to "2026-01-20T23:59:59+01:00" --event-color 11
```

### Update Event
```bash
# Update event title and color
gog calendar update primary <eventId> --summary "Updated Meeting Title" --event-color 4
```

## Event Colors

| Color ID | Hex Code | Typical Use |
|----------|----------|-------------|
| 1 | #a4bdfc | Meetings, Work |
| 2 | #7ae7bf | Personal, Health |
| 3 | #dbadff | Social, Events |
| 4 | #ff887c | Deadlines, Urgent |
| 5 | #fbd75b | Reminders |
| 6 | #ffb878 | Travel |
| 7 | #46d6db | Fun, Leisure |
| 8 | #e1e1e1 | General |
| 9 | #5484ed | Work Projects |
| 10 | #51b749 | Completed, Done |
| 11 | #dc2127 | Critical, High Priority |

```bash
# View all colors
gog calendar colors
```

## Common Workflows

### Find Available Time Slots
```bash
# List all events to visualize availability
gog calendar events primary --from "2026-01-15T00:00:00Z" --to "2026-01-21T23:59:59Z" --json
```

### Schedule Recurring Concept
Note: gog CLI doesn't support direct recurring events, but you can script them:
```bash
# Create multiple events via scripting (example)
for i in {1..5}; do
  DATE=$(date -v+${i}d +%Y-%m-%d)
  gog calendar create primary --summary "Daily Standup" \
    --from "${DATE}T09:00:00+01:00" --to "${DATE}T09:30:00+01:00" \
    --event-color 1
done
```

### Bulk Operations
```bash
# Set default account to avoid repetition
export GOG_ACCOUNT=you@gmail.com

# Then run commands without --account
gog calendar events primary --from "..." --to "..."
```

## Tips for Effective Use

1. **Use ISO 8601 timestamps**: Always include timezone offset
2. **JSON output for scripting**: Add `--json` flag for machine-readable output
3. **Batch with --no-input**: Use `--no-input` for automated scripts
4. **Primary calendar shortcut**: Use "primary" as the calendar ID for your main calendar

## Example Script: Weekly Agenda Check
```bash
#!/bin/bash
# Get this week's events
START=$(date -u -v-Monday +%Y-%m-%dT00:00:00Z)
END=$(date -u -v+Sunday +%Y-%m-%dT23:59:59Z)
gog calendar events primary --from "$START" --to "$END" --json
```
