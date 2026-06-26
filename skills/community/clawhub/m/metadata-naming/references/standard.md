# Metadata Naming Standard

## Purpose

Use this standard to name files and folders in a way that is:
- readable by humans
- sortable by default
- safe for scripts
- stable across sync, backup, and migration flows

## Naming Modes

### 1. Relaxed mode

Use for manually managed documents.

Characteristics:
- mixed language allowed
- spaces allowed when the environment supports them
- visual markers may include `( )`, `#`, `@`, `&`

Pattern:
```text
(YYYY-MM-DD)Title(vX.Y.Z)#tag@source&note.ext
```

### 2. Strict mode

Use for automation, inventories, skills, repos, snapshots, and shared standards.

Characteristics:
- ASCII only
- no spaces
- block separator: `__`
- inner separator: `-` or `.`

Pattern:
```text
YYYYMMDD[-HHMMSS]__prefix__title__version__tags__source__note.ext
```

## Recommended Defaults

### Long-lived entry files

Use when a file is updated in place and should keep one stable identity.

```text
<data_type>__<source_name>__<slug>.md
```

Examples:
```text
skill__workspace__favorites-curator.md
repo__github__openclaw-backup-tool.md
app__brew__codex.md
```

### Snapshots and reports

Use when each run should create a new artifact.

```text
YYYYMMDD__report__topic.md
YYYYMMDD-HHMMSS__snapshot__topic.json
```

Examples:
```text
20260311__report__favorites-digest.md
20260311-095914__snapshot__favorites.json
```

## Metadata Blocks

Use blocks in this order when needed:
1. time
2. prefix
3. title
4. version
5. tags
6. source_or_author
7. note

## Block Guidance

### time
- `YYYYMMDD` for day-level
- `YYYYMMDD-HHMMSS` for run-level
- place first for lexical sorting

### prefix
- short taxonomy such as `repo`, `skill`, `app`, `doc`, `report`, `snapshot`

### title
- main identity block
- short, stable, searchable
- prefer lowercase slug form in strict mode

### version
- use semver where available, such as `v0.1.0`

### tags
- small set only
- join inside the block with `.` or `-`

### source_or_author
- source system, publisher, owner, or author
- examples: `github`, `brew`, `workspace`, `vendor-name`

### note
- optional
- only include if it materially improves retrieval

## Allowed Characters In Strict Mode

Prefer:
- `a-z`
- `0-9`
- `-`
- `_`
- `.`

Avoid:
- spaces
- non-ASCII characters
- shell-sensitive punctuation

## Decision Rules

Use stable entry naming when:
- the file represents one canonical object
- the content is refreshed in place
- dedupe and merge matter more than history in filenames

Use timestamp naming when:
- each run should create a new artifact
- chronology matters
- auditability matters

## Standard Sentence

Use fixed-order metadata blocks. Use stable identity naming for long-lived entries and timestamped naming for snapshots. Default to ASCII, no spaces, `__` between blocks, and `-` or `.` inside blocks.
