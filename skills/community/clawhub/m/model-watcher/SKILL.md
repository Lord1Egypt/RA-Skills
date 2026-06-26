---
name: model-watcher
description: Discover, store, and inspect AI model catalog entries from one or more sources. Use when the user wants to sync a model catalog into SQLite, see newly discovered models, list models first seen recently or in a given month, inspect one model, or view simple catalog stats.
---

# Model Watcher

Maintain a local catalog of discovered AI models and query that catalog with a small CLI.

This skill covers discovery, storage, and inspection of model entries.
It does not define scheduling or notification behavior.

## Quick Usage

```bash
python3 skills/model-watcher/scripts/model_watcher.py scan
python3 skills/model-watcher/scripts/model_watcher.py brief-new
python3 skills/model-watcher/scripts/model_watcher.py recent --days 7
python3 skills/model-watcher/scripts/model_watcher.py monthly --month 2026-03
python3 skills/model-watcher/scripts/model_watcher.py stats
python3 skills/model-watcher/scripts/model_watcher.py show --model-id provider/model-name
```

Default database path:

```text
skills/model-watcher/data/model-watcher.db
```

Override with `--db /path/to/file.db` when needed.

## Commands

### `scan`

Sync source data into the local SQLite database.

Expected result:
- fetch latest catalog data from the configured source implementation
- normalize key fields
- upsert model records
- record `new`, `updated`, and `missing` events
- print one run summary

Example:

```bash
python3 skills/model-watcher/scripts/model_watcher.py scan
```

Example output:

```text
run_id: a32cd157-c617-4682-8ae6-5765439e6fd9
source: openrouter
models_total: 344
new: 0 | updated: 0 | missing: 0
```

### `brief-new`

Show models from the latest run that recorded `new` events.

Use this when a compact list of newly discovered models is needed.

Example:

```bash
python3 skills/model-watcher/scripts/model_watcher.py brief-new --limit 3
```

Example output:

```text
OpenRouter new models from run a32cd157-c617-4682-8ae6-5765439e6fd9: 3
- x-ai/grok-4.20-multi-agent-beta — xAI: Grok 4.20 Multi-Agent Beta
  first seen: 2026-03-13 05:43:20 UTC
  provider: x-ai | context: 2000000 | modality: text+image->text
  pricing: in 0.000002, out 0.000006, extras 2
```

### `recent`

List models whose `first_seen_at` is within the last N days.

Example:

```bash
python3 skills/model-watcher/scripts/model_watcher.py recent --days 7
```

Example output:

```text
OpenRouter models first seen in last 7 day(s): 12
- provider/model-a — Model A
  first seen: 2026-03-12 08:00:00 UTC
  provider: provider | context: 128000 | modality: text->text
  pricing: in 0.000001, out 0.000002
```

### `monthly`

List models whose `first_seen_at` falls within a given month.

Example:

```bash
python3 skills/model-watcher/scripts/model_watcher.py monthly --month 2026-03
```

Example output:

```text
OpenRouter models first seen in 2026-03: 18
- provider/model-b — Model B
  first seen: 2026-03-10 03:20:00 UTC
  provider: provider | context: 256000 | modality: text+image->text
  pricing: in 0.000003, out 0.000009
```

### `stats`

Show simple catalog totals and top provider counts.

Example:

```bash
python3 skills/model-watcher/scripts/model_watcher.py stats
```

Example output:

```text
OpenRouter active models: 344
Added in last 7 days: 12
Added in 2026-03: 18
Top providers:
- openai: 60
- qwen: 50
- google: 27
```

### `show`

Show one stored model entry.

Example:

```bash
python3 skills/model-watcher/scripts/model_watcher.py show --model-id openai/gpt-4o-mini
```

Example output:

```text
model_id: openai/gpt-4o-mini
name: OpenAI: GPT-4o Mini
provider: openai
created_at: 2026-03-01 00:00:00 UTC
first_seen_at: 2026-03-13 05:43:20 UTC
last_seen_at: 2026-03-13 05:43:20 UTC
context_length: 128000
modality: text+image->text
pricing: in 0.00000015, out 0.0000006
description:
Compact multimodal model optimized for low cost and fast response.
```

## Data Model

The database schema is documented in `references/schema.md`.

Keep the schema extensible for multiple future sources.
Keep source-specific collection logic in scripts, not in this file.

## Notes

- Prefer compact, factual output.
- Prefer stable ids and `first_seen_at` for reporting.
- Treat `new` as the primary discovery signal.
- Do not put scheduling, cron, or user-facing notification policy into this skill.
