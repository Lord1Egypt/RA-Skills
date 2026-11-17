# Notion Sync Folder Standard

Keep all Notion sync state in `travel-db/notion-sync/`. Do not create nested directories inside that folder.

## Fixed Files

- `_README.md`: human-facing usage and migration notes.
- `_config.example.json`: configuration shape; never store real tokens.
- `_schema.md`: local JSONL fields and Notion property mapping.
- `_records.jsonl`: primary machine-readable compact store; one JSON object per line.
- `_index.md`: human-readable grouped index.
- `_ledger.jsonl`: sync-only page IDs, hashes, and timestamps.
- `_conflicts.md`: manual conflict queue.
- `_sync_log.jsonl`: append-only sync run summaries for dry-run and apply.

## Record Weights

- `light`: simple shop/place save. Keep it only in `_records.jsonl` and `_index.md`.
- `standard`: medium record with address, source, reservation notes, or several tags. Still keep it in JSONL unless it needs sections.
- `detailed`: long guide, long OCR, trip plan, rich notes, multi-person feedback, conflicts, or anything that benefits from Markdown sections. Add `detail_file`.

Promote a record to `detailed` when notes exceed about 800 characters, evidence has more than 3 items, OCR/image text is long, the record is a trip plan, or the user asks for more narrative context.

## Detail File Naming

Detailed files stay directly under `notion-sync/`:

```text
place-20260614-shanghai-sushi-abc123.md
guide-20260614-tokyo-ramen-def456.md
trip-20260614-tokyo-3days-ghi789.md
```

Use lowercase ASCII where practical. Chinese names may remain in the `name` field; keep filenames short and stable.

## Machine Reading Order

1. Read `_records.jsonl` for search, filtering, and quick recommendations.
2. Read `_ledger.jsonl` only when syncing.
3. Read `_sync_log.jsonl` only when diagnosing previous sync runs.
4. Read detailed Markdown only when `record_weight` is `detailed`, `detail_file` is set, or the user's question needs long notes.
5. Treat `_index.md` as a human view derived from `_records.jsonl`.

## Human Migration Rule

The whole Notion mirror should be portable by copying one folder: `travel-db/notion-sync/`.
