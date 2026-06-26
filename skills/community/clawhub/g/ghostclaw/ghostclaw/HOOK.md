---
name: ghostclaw-reviewer
description: "Automatically review codebase vibes and architecture after significant commands"
homepage: https://github.com/ev3lynx727/ghostclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "👻",
        "events": ["command", "system"],
        "install": [{ "id": "ghostclaw", "kind": "skill", "label": "Ghostclaw Architectural Reviewer" }],
      },
  }
---

# Ghostclaw Hook

The `ghostclaw` skill can operate as an OpenClaw hook, integrating directly into the event system to provide continuous, underlying architectural oversight of your projects.

## What It Does

When enabled as a hook, Ghostclaw operates in the background:

1. **Listens to Events** - Reacts to both user commands (e.g., after a major refactor or file generation) and system events (periodic checks).
2. **Performs Vibe Checks** - Analyzes the codebase context related to the event to score architectural health.
3. **Silent or Proactive Feedback** - Can silently log its findings or proactively open PRs if issues cross a threshold.

## Hook Events

Ghostclaw can bind to the following OpenClaw events:

### Command Events (`command`)

Triggers after the agent completes a command turn.

- **Use Case**: Quick vibe check on newly modified files.
- **Action**: Ghostclaw runs a scaled-down analysis on the affected files to ensure new code doesn't violate established architectural patterns (e.g., preventing a controller from importing a database module directly).

### System Events (`system`)

Triggers on periodic system heartbeats or cron schedules.

- **Use Case**: Deep, repository-wide architectural scanning.
- **Action**: Ghostclaw runs a full structural analysis, comparing current metrics against historical trends to detect regressions in "vibe health."

## Implementation

To run Ghostclaw as a hook, the handler script maps OpenClaw's event payloads to the underlying Python CLI engine.

Example invocation triggered by a hook event:

```bash
python -m ghostclaw.cli.ghostclaw /path/to/repo --event-context json_payload
```

## Configuration

You can enable this hook via the CLI:

```bash
openclaw hooks enable ghostclaw-reviewer
```

Or configure it in your `~/.openclaw/config/openclaw.json`:

```json
{
  "hooks": {
    "internal": {
      "entries": {
        "ghostclaw-reviewer": { 
          "enabled": true,
          "options": {
            "strictMode": true,
            "autoCreatePRs": false
          }
        }
      }
    }
  }
}
```

## Disabling

If the architectural ghost becomes too demanding, disable it via:

```bash
openclaw hooks disable ghostclaw-reviewer
```
