# Model Watcher schema

## Database

Default path:

`skills/model-watcher/data/model-watcher.db`

## Tables

### models
Current known state per source model.

Fields:
- `source` TEXT — source id, V1 always `openrouter`
- `model_id` TEXT — canonical source model id
- `canonical_slug` TEXT — OpenRouter canonical slug when present
- `name` TEXT
- `provider` TEXT — parsed from `model_id` prefix when possible
- `description` TEXT
- `created_at` TEXT — API `created` mapped to UTC ISO timestamp when present
- `first_seen_at` TEXT — first time this watcher saw the model
- `last_seen_at` TEXT — latest successful scan containing the model
- `last_changed_at` TEXT — latest scan where normalized content changed
- `is_active` INTEGER — 1 active / 0 missing from latest scan
- `context_length` INTEGER
- `modality` TEXT
- `input_modalities_json` TEXT
- `output_modalities_json` TEXT
- `pricing_json` TEXT
- `top_provider_json` TEXT
- `raw_json` TEXT — normalized raw source payload
- `content_hash` TEXT — hash of selected material fields for change detection

Primary key:
- `(source, model_id)`

### runs
One row per sync run.

Fields:
- `run_id` TEXT PRIMARY KEY
- `source` TEXT
- `started_at` TEXT
- `finished_at` TEXT
- `status` TEXT — `ok` / `error`
- `models_total` INTEGER
- `new_count` INTEGER
- `updated_count` INTEGER
- `missing_count` INTEGER
- `error_message` TEXT

### events
Change log for reporting.

Fields:
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `run_id` TEXT
- `source` TEXT
- `model_id` TEXT
- `event_type` TEXT — `new` / `updated` / `missing`
- `event_at` TEXT
- `summary_json` TEXT

Indexes:
- `(event_type, event_at)`
- `(model_id, event_at)`
