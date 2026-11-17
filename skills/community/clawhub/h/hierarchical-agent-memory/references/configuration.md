# Configuration Reference

## Quick Start

The skill works with zero configuration using the `standard` preset. To
customize, add a `memory_structure` block to your workspace configuration.

## Presets

### minimal

Best for: single-project agents, simple setups, users who want structure
without complexity.

Creates: `MEMORY.md` (routing table). Daily notes stay at OpenClaw's own `memory/YYYY-MM-DD.md`.

```json
{ "memory_structure": { "preset": "minimal" } }
```

### standard (default)

Best for: multi-project agents, users who work across several topics or
with multiple contacts.

Creates: `MEMORY.md` + `memory/topics/` + `memory/contacts/`. Daily notes stay at `memory/YYYY-MM-DD.md`.

```json
{ "memory_structure": { "preset": "standard" } }
```

### full

Best for: long-running agents that need historical recall ("what happened
in February?"), users who value complete archival records.

Creates: everything in `standard` + `memory/weekly/` + `memory/monthly/`
+ `memory/yearly/` with automated distillation cron jobs.

```json
{ "memory_structure": { "preset": "full" } }
```

## Overriding Preset Defaults

Start with a preset, then override individual settings:

```json
{
  "memory_structure": {
    "preset": "standard",
    "time_layers": true,
    "distillation": {
      "weekly": { "enabled": true },
      "monthly": { "enabled": false },
      "yearly": { "enabled": false },
      "timezone": "America/New_York"
    }
  }
}
```

This gives you `standard` plus weekly summaries, but skips monthly and yearly.

## Full Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "hierarchical-agent-memory configuration",
  "type": "object",
  "properties": {
    "memory_structure": {
      "type": "object",
      "properties": {
        "preset": {
          "type": "string",
          "enum": ["minimal", "standard", "full"],
          "default": "standard",
          "description": "Base configuration preset"
        },
        "routing_table": {
          "type": "boolean",
          "default": true,
          "description": "Maintain MEMORY.md as a lean routing table"
        },
        "routing_table_max_kb": {
          "type": "number",
          "default": 3,
          "minimum": 1,
          "maximum": 10,
          "description": "Maximum size in KB of the hand-maintained part of MEMORY.md, excluding dreaming-managed entries"
        },
        "topics": {
          "type": "boolean",
          "default": true,
          "description": "Enable topic-based working memory"
        },
        "topics_path": {
          "type": "string",
          "default": "topics/",
          "description": "Directory for topic files relative to memory/"
        },
        "contacts": {
          "type": "boolean",
          "default": true,
          "description": "Enable contact files"
        },
        "contacts_path": {
          "type": "string",
          "default": "contacts/",
          "description": "Directory for contact files relative to memory/"
        },
        "time_layers": {
          "type": "boolean",
          "default": false,
          "description": "Enable weekly/monthly/yearly archival layers"
        },
        "distillation": {
          "type": "object",
          "description": "Settings for time-based distillation (requires time_layers: true)",
          "properties": {
            "weekly": {
              "type": "object",
              "properties": {
                "enabled": { "type": "boolean", "default": true },
                "schedule": { "type": "string", "default": "0 2 * * 0", "description": "Cron expression" }
              }
            },
            "monthly": {
              "type": "object",
              "properties": {
                "enabled": { "type": "boolean", "default": true },
                "schedule": { "type": "string", "default": "0 2 1 * *" }
              }
            },
            "yearly": {
              "type": "object",
              "properties": {
                "enabled": { "type": "boolean", "default": true },
                "schedule": { "type": "string", "default": "0 2 1 1 *" }
              }
            },
            "timezone": {
              "type": "string",
              "description": "IANA timezone (e.g., America/Chicago). Defaults to system timezone."
            }
          }
        }
      }
    }
  }
}
```

## Directory Structure by Preset

The daily-note location is not configurable. OpenClaw reads and writes
`memory/YYYY-MM-DD.md` (plus `memory/YYYY-MM-DD-HHMM.md` from the
session-memory hook), and this skill uses those files as its intake layer.
`MEMORY.md` lives at the workspace root, not inside `memory/`.

### minimal
```
MEMORY.md
memory/
  YYYY-MM-DD.md
```

### standard
```
MEMORY.md
memory/
  YYYY-MM-DD.md
  topics/
    project-name.md
    infrastructure.md
  contacts/
    person-name.md
```

> Session files (`memory/sessions/`) are managed by the companion skill
> `agent-session-state`, not by this skill.

### full
```
MEMORY.md
memory/
  YYYY-MM-DD.md
  topics/
    project-name.md
    infrastructure.md
    archive/
      completed-project.md
  contacts/
    person-name.md
  weekly/
    YYYY-WNN.md
  monthly/
    YYYY-MM.md
  yearly/
    YYYY.md
```

> `memory/dreaming/` (phase reports) and `DREAMS.md` are written by OpenClaw's
> dreaming feature, not by this skill, and overlap with the `full` preset's
> archives. Prefer `standard` when dreaming is on (the default from 2026.8.1).
