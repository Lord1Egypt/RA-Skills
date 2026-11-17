# Ingestion Workflow

Follow this process whenever the user sends travel content to save.

## 1. Preserve the Raw Input

- If the input is a short, unambiguous place name, it may go straight into a place entry.
- If the input contains several places, subjective notes, screenshots, copied guides, or uncertainty, create an `_inbox/` note first.
- If the input includes an image, store or reference the image under `assets/` and record OCR/extracted text in the inbox note.
- Prefer `scripts/butler.py ingest-text --db travel-db --text TEXT --apply` for uncertain text so the raw capture is preserved before any extraction.

## 2. Extract Entities

Identify:

- places and aliases
- city, neighborhood, address, coordinates, or map hints
- food, dishes, cuisines, shop type, and use case
- source URL, platform, author, screenshot, or user quote
- preferences or constraints expressed by the user
- trip dates, companions, budget, pace, and must-go items

Keep `city` to one city name. Put province, district, street, and detailed address in separate fields or notes.

## 3. Check Duplicates

Before creating a new atomic entry, search existing files for:

- exact or fuzzy name match
- aliases or translated names
- same source URL
- same address, map link, or coordinates
- same screenshot evidence
- distinctive dishes or notes in the same city

If a likely match exists, update that entry and append new evidence. If uncertain, create a new entry with `status: needs-review` and link the possible duplicate in the body.

## 4. Enrich Actively

When available, use network, OCR, map, or search tools to fill missing facts:

- official name and aliases
- address and city
- coordinates
- hours and closure days
- reservation method
- official website or map link
- signature dishes or reason to visit
- current open/closed status

Record `last_verified` and source details. Never silently replace user-provided facts when external data conflicts; preserve both and add a conflict note.

## 5. Write Entries

Use `scripts/create_entry.py` for new records where possible. Keep filenames stable and readable:

```text
places/shanghai-sushi-example-place-20260614-abc123.md
guides/tokyo-ramen-guide-20260614-def456.md
```

Use relative links between related entries. Prefer one entry per durable object, not one giant city document.

For routine place saves, prefer `scripts/butler.py add-place` because it checks duplicates, refreshes generated files, and runs validation automatically.

## 6. Refresh Indexes

Indexes are derived views. Update or regenerate them after meaningful changes:

- `indexes/cities.md`
- `indexes/tags.md`
- `indexes/sources.md`

If an index seems stale, trust atomic entries and regenerate the index.

For Notion sync, `scripts/notion_sync.py push|sync` refreshes `notion-sync/_records.jsonl` from Markdown entries before planning by default. To refresh only the local compact mirror, run `scripts/build_records_from_places.py --apply`.
