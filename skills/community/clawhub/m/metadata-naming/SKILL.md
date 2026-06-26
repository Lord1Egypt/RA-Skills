---
name: metadata-naming
description: Define, apply, or review a reusable metadata-based filename standard for files, folders, inventories, archives, and generated catalogs. Use when the user wants to extract a naming convention into a standard, normalize filenames, choose between human-readable and machine-friendly naming, or create naming rules for repositories, skills, software inventories, snapshots, and long-lived records.
---

# Metadata Naming

Turn loose filename habits into a stable naming standard that is easy to read, sort, parse, and reuse.

## Use This Standard

Follow this split by file purpose:
- Use stable identity naming for long-lived entries that are updated in place.
- Use timestamp naming for snapshots, archives, exports, and reports.
- Prefer ASCII, no spaces, and fixed separator rules when filenames will be processed by scripts or moved across systems.

## Core Metadata Blocks

Use these blocks in a fixed order when a filename needs richer metadata:
- time
- prefix
- title
- version
- tags
- source_or_author
- note

Not every block is required. Keep only the fields that improve retrieval or automation.

## Two Modes

### Relaxed mode

Use for human-managed documents where readability matters more than strict parsing.

Conventions:
- Chinese or mixed-language titles are allowed.
- Spaces are allowed when the surrounding system tolerates them.
- Typical visual markers:
  - time: `(2026-03-11)` or `(20260311-093500)`
  - version: `(v1.2.0)`
  - tags: `#tag`
  - source or author: `@name`
  - note: `&note`

Example:
```text
(2026-03-11)Favorites Curator(v0.1.0)#skill#favorites@workspace&initial publish
```

### Strict mode

Use by default for standards, skills, inventories, generated files, syncable folders, and anything a script will read.

Conventions:
- ASCII only
- no spaces
- top-level separator: `__`
- intra-block separator: `-` or `.`
- lowercase slug-style titles unless there is a strong reason not to

General template:
```text
YYYYMMDD[-HHMMSS]__prefix__title__version__tags__source__note.ext
```

Examples:
```text
20260311__skill__favorites-curator__v0.1.0__favorites.catalog__workspace.md
20260311__repo__openclaw-backup-tool__v0.1.0__backup.tool__github.md
20260311__app__codex__v0.112.0__cli.ai__brew.md
```

## Default Rule For Long-Lived Entries

For catalogs, inventories, and canonical records, prefer stable filenames over timestamped filenames.

Use this template:
```text
<data_type>__<source_name>__<slug>.md
```

Examples:
```text
skill__workspace__favorites-curator.md
repo__github__openclaw-backup-tool.md
app__brew__codex.md
```

Use this rule when the content is refreshed in place and the filename should not drift over time.

## Default Rule For Snapshots And Reports

Use timestamp-first filenames for time-series artifacts.

Templates:
```text
YYYYMMDD__report__topic.md
YYYYMMDD-HHMMSS__snapshot__topic.json
```

Examples:
```text
20260311__report__favorites-digest.md
20260311-095914__snapshot__favorites.json
```

## Block Rules

### Time
- Use `YYYYMMDD` for day-level tracking.
- Use `YYYYMMDD-HHMMSS` for run-level uniqueness.
- Put time first when sort order matters.

### Prefix
- Use short taxonomy values such as `repo`, `skill`, `app`, `doc`, `snapshot`, `report`.
- Keep the vocabulary stable once chosen.

### Title
- Make this the main identity.
- Prefer short, stable, searchable slugs.
- Move extra description into tags or notes.

### Version
- Use semver when available: `v0.1.0`, `v2.3.4`.
- Omit the block when versioning is irrelevant.

### Tags
- Use compact, low-noise tags.
- Join multiple tags with `.` or `-` inside the same block.

### Source Or Author
- Use the source system, publisher, owner, or author when it improves retrieval.
- Examples: `github`, `brew`, `workspace`, `openclaw`, `vendor-name`.

### Note
- Keep it short.
- Do not put long prose into filenames.
- Use only when the note materially changes retrieval value.

## Standard Principle

Use fixed-order metadata blocks. Use stable identity filenames for long-lived entries and timestamped filenames for snapshots. Default to ASCII, no spaces, `__` between blocks, and `-` or `.` inside blocks so names stay sortable, parseable, and portable.

## References

Read `references/standard.md` when you need the normalized standard, examples, and decision rules in a reference-friendly format.
