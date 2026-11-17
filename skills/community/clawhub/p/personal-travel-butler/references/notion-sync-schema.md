# Notion Sync Schema

Use one Notion data source named `Travel Entries` and one local compact record store: `travel-db/notion-sync/_records.jsonl`.

## Required Notion Properties

| Notion property | Type | Local field |
| --- | --- | --- |
| `Name` | title | `name` |
| `Travel ID` | rich_text | `id` |
| `Type` | select | `type` |
| `Status` | select | `status` |
| `Record Weight` | select | `record_weight` |
| `City` | rich_text | `city` |
| `Tags` | multi_select | `tags` |
| `Priority` | number | `priority` |
| `Summary` | rich_text | `summary` |
| `Detail File` | rich_text | `detail_file` |
| `Updated At` | date | `updated_at` |

## Optional Notion Properties

Newly created Notion databases include these columns. Existing databases may not have them; sync scripts should skip missing optional columns instead of failing.

| Notion property | Type | Local field |
| --- | --- | --- |
| `Notes` | rich_text | `notes` |
| `Evidence` | rich_text | JSON-serialized `evidence` |
| `Source` | rich_text | JSON-serialized `source` |
| `Address` | rich_text | `address` |
| `Province` | rich_text | `province` |
| `Sync Hash` | rich_text | last pushed content hash |
| `Phone` | rich_text | `phone` |
| `Website` | url | `website` |

## `_records.jsonl` Fields

Each line is one JSON object:

```json
{"id":"place-20260614-abc123","notion_page_id":null,"type":"place","status":"active","record_weight":"light","name":"Example","city":"Shanghai","tags":["sushi"],"priority":3,"summary":"Why it matters.","notes":"","detail_file":null,"source":[{"title":"Original note","url":null}],"evidence":[{"source":"Original note","date":"2026-06-14","note":"User wanted to save it."}],"address":null,"province":null,"phone":null,"website":null,"updated_at":"2026-06-14","last_synced_at":null}
```

Required local fields:

- `id`
- `type`
- `status`
- `record_weight`
- `name`
- `city`
- `tags`
- `priority`
- `summary`
- `notes`
- `detail_file`
- `source`
- `evidence`
- `updated_at`

Optional sync fields:

- `notion_page_id`
- `last_synced_at`
- `address`
- `province`
- `phone`
- `website`

Keep `evidence` and `source` as arrays. Items may be strings or JSON objects; do not flatten structured evidence objects before writing `_records.jsonl`.

Use `scripts/notion_schema.py check --db travel-db` to inspect optional Notion columns. Use `scripts/notion_schema.py migrate --db travel-db --apply` to add missing optional columns to an existing Notion data source.

## `_ledger.jsonl` Fields

Each line is one sync bookkeeping object:

```json
{"id":"place-20260614-abc123","notion_page_id":"...","local_hash":"...","notion_hash":"...","last_synced_at":"2026-06-14T12:00:00Z","last_direction":"push"}
```

The ledger is not content. Use it only to detect single-sided changes and conflicts.
