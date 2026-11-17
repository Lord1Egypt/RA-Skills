---
name: personal-travel-butler
description: Manage a personal travel Markdown database for food finds, places, guides, screenshots, preferences, Notion synchronization, and trip planning. Use when the user sends travel tips, restaurant or place names, location text, itinerary ideas, images/screenshots, asks to store or organize travel knowledge, wants Notion sync setup or sync scripts, or wants recommendations and travel plans grounded in the local travel-db.
---

# Personal Travel Butler

## Overview

Use this skill to maintain the user's local, human-readable travel knowledge base and answer travel questions from it. Keep the system layer (`personal-travel-butler/`) separate from the database layer (`travel-db/`).

## Database Location

Use `../travel-db` relative to this skill folder unless the user explicitly points to another database. Treat Markdown files as the source of truth; generated indexes are rebuildable views.

When running from a local Hermes install, this skill may be symlinked from `~/.hermes/skills/personal-travel-butler` to the user's local `personal-travel-butler` folder. If relative lookup is unclear, ask the user for the project root and use its sibling `travel-db` folder as the database path.

Use `../travel-db/notion-sync` for Notion interoperability. Keep it as one flat folder: machines should read `_records.jsonl` first, humans should scan `_index.md`, and detailed Markdown files should exist only for records that need long-form notes.

## Core Workflow

1. Capture the user's raw input before restructuring it.
2. Extract places, restaurants, dishes, guide items, constraints, and preferences.
3. Search existing Markdown entries for likely duplicates by name, aliases, city, address, coordinates, source URL, and distinctive notes.
4. Actively enrich missing facts when tools and permissions allow: address, coordinates, hours, reservation method, official links, signature dishes, transit hints, and current status.
5. Preserve source evidence and verification dates. Do not overwrite conflicting facts; add a conflict note and mark the field or entry as `needs-review`.
6. Create or update atomic Markdown entries, then refresh generated indexes and the Notion compact mirror when useful.
7. When answering or planning, cite local entries first and clearly separate local knowledge from newly checked external information.

## Hermes Usage

When invoked from Hermes, do not ask the user to paste Notion tokens or credentials into chat. Read local Notion settings from the project root `.env` through the provided scripts.

If the user asks whether Notion is connected:

1. Do not run `scripts/notion_setup.py --apply`.
2. Do not create a new Notion database.
3. Run `scripts/notion_check.py --db <project-root>/travel-db`.
4. If the check succeeds, answer that Notion is connected.
5. If the check fails, report the exact error briefly and suggest checking `.env` locally, without printing token values.

Use `scripts/notion_setup.py --apply` only for the first-time setup when `NOTION_TRAVEL_DATA_SOURCE_ID` is not configured. If it is already configured, the setup script should be treated as complete.

## Input Handling

- For text: save the original text in `_inbox/` when it contains multiple facts or uncertain entities, then split stable entities into atomic entries.
- For place names or map links: create or update a place entry, enrich with current facts, and record the lookup source.
- For images/screenshots: store the image under `assets/`, record OCR/extracted text in `_inbox/`, then create entries from the extracted facts.
- For preferences: update `preferences/` entries rather than burying personal constraints in place notes.
- For trip planning requests: read `preferences/`, relevant `places/`, `guides/`, and `trips/` before recommending.

## Resources

- Read `references/database-schema.md` before creating or updating entries.
- Read `references/ingestion-workflow.md` for text, location, and image intake rules.
- Read `references/recommendation-workflow.md` before generating recommendations or itineraries.
- Read `references/notion-sync-folder-standard.md` before changing Notion sync files.
- Read `references/notion-integration.md` before configuring Notion tokens, data source IDs, or live API calls.
- Read `references/notion-sync-schema.md` before mapping Notion properties to local fields.
- Use `scripts/create_entry.py` to create entry skeletons with stable IDs and valid frontmatter.
- Use `scripts/validate_db.py` to check required fields, duplicate IDs, links, and basic database integrity.
- Use `scripts/notion_check.py` to validate Notion sync folder structure and, when credentials are present, Notion schema access.
- Use `scripts/notion_setup.py` to create the Notion travel database and required properties under a shared parent page.
- Use `scripts/notion_sync.py` for dry-run-first Notion push/pull/sync plans.
- `scripts/notion_sync.py push|sync` refreshes `_records.jsonl` from Markdown entries before planning by default. Use `--strict` to block overwrites after Notion-side edits, and `--filter-city` or `--filter-tag` for selective sync.
- Use `scripts/notion_schema.py check|migrate` to inspect or add optional Notion columns for an existing data source.
- Use `scripts/build_records_from_places.py --apply` only when you want to refresh the compact mirror and generated local indexes without calling Notion.
- Use `scripts/notion_compact.py` to keep simple Notion records in `_records.jsonl` without creating extra Markdown files.
- Use `scripts/notion_promote.py` when a light or standard record deserves a detailed Markdown file.

## Command-First Usage

Prefer `scripts/butler.py` for common operations. Only edit Markdown directly when the command surface cannot express the requested change.

| User intent | Preferred command |
| --- | --- |
| Check health / diagnose sync | `python3 personal-travel-butler/scripts/butler.py doctor --db travel-db` |
| Repair local derived files only | `python3 personal-travel-butler/scripts/butler.py doctor --db travel-db --fix-local` |
| Save a new place | `python3 personal-travel-butler/scripts/butler.py add-place --db travel-db --name NAME --city CITY --tag TAG --evidence EVIDENCE` |
| Update an existing place | `python3 personal-travel-butler/scripts/butler.py update-place --db travel-db --id PLACE_ID --evidence EVIDENCE` |
| Capture uncertain raw text | `python3 personal-travel-butler/scripts/butler.py ingest-text --db travel-db --text TEXT --apply` |
| Check duplicates | `python3 personal-travel-butler/scripts/butler.py duplicates --db travel-db --name NAME --city CITY` |
| Refresh local mirror and indexes | `python3 personal-travel-butler/scripts/butler.py refresh --db travel-db --apply` |
| Dry-run Notion sync safely | `python3 personal-travel-butler/scripts/butler.py sync --db travel-db` |
| Apply Notion sync safely | `python3 personal-travel-butler/scripts/butler.py sync --db travel-db --apply` |
| Check optional Notion columns | `python3 personal-travel-butler/scripts/butler.py schema --db travel-db check` |
| Add optional Notion columns | `python3 personal-travel-butler/scripts/butler.py schema --db travel-db migrate --apply` |

For weak-agent reliability:

- Run `butler.py add-place` instead of manually creating a Markdown file.
- Run `butler.py update-place` when a duplicate exists.
- Run `butler.py sync` before `butler.py sync --apply`.
- Never run `notion_setup.py --apply` unless doing first-time setup with no existing data source.

## Writing Rules

- Prefer one atomic Markdown file per place, restaurant, guide, trip, or preference record.
- Keep YAML frontmatter valid and boring: simple strings, lists, numbers, booleans, or null.
- Use relative links and paths so the database remains compatible with Obsidian and plain editors.
- Preserve the user's original wording in evidence or inbox notes.
- Record confidence and source when enriching from external information.
- Keep `city` to one normalized city name only, such as `文昌` or `深圳`. Put province, district, street, or address details in separate fields/body notes.
- Keep indexes derived; do not treat index files as authoritative records.
- Keep Notion sync lightweight: simple store records stay in `_records.jsonl`; only detailed records get standalone Markdown files in `notion-sync/`. Markdown entries under `places/`, `guides/`, `trips/`, and `preferences/` are treated as source material for the compact Notion mirror.
- Do not run `scripts/notion_setup.py --apply` again when `NOTION_TRAVEL_DATA_SOURCE_ID` is already configured. Use `scripts/notion_check.py --db travel-db` to verify the existing Notion database, then use `scripts/notion_sync.py sync --db travel-db` for synchronization.
- Never paste, echo, summarize, or store Notion tokens in chat output. If a token appears in chat, advise rotating it and moving the new token into local `.env`.
