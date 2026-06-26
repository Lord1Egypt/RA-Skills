# Configuration Reference

## Quick Start

The skill works with zero configuration using the `standard` preset. To
customize, add a `memory_structure` block to your workspace configuration.

## Presets

### minimal

Best for: single-project agents, simple setups, users who want structure
without complexity.

Creates: `MEMORY.md` (routing table) + `memory/daily/` (platform default)

```json
{ "memory_structure": { "preset": "minimal" } }
```

### standard (default)

Best for: multi-project agents, users who work across several topics or
with multiple contacts.

Creates: `MEMORY.md` + `memory/daily/` + `memory/topics/` + `memory/contacts/`

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
          "description": "Maximum MEMORY.md size in KB before warning"
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

### minimal
```
memory/
  MEMORY.md
  daily/
    YYYY-MM-DD.md
```

### standard
```
memory/
  MEMORY.md
  daily/
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
memory/
  MEMORY.md
  daily/
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
