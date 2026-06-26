---
name: iCal Calendar
description: Query `.ics` calendar files, raw iCal strings, or remote iCal feeds with the local `icali` CLI. Use when a user asks for natural-language calendar lookups such as what's on a day, week, or time window, whether a person appears in upcoming meetings, or when filtering iCal events by summary, description, location, date range, status, or component type.
homepage: https://github.com/docmarionum1/iCaLI
metadata:
  openclaw:
    requires:
      bins:
        - icali
---

# iCal Calendar

Use this skill when the user explicitly wants `.ics` or iCal data, or when the available source is an iCal file, string, or feed.

## Source selection

Before querying, identify the real iCal source:

- Local file: `icali --file "/absolute/path/to/calendar.ics"`
- Remote feed: `icali --url "https://example.com/calendar.ics"`
- Raw iCal text: `icali --string "BEGIN:VCALENDAR..."`
- The positional source argument also works, but explicit `--file` or `--url` is usually clearer in agent logs

Never invent a calendar source. If the source is not provided, look for one in the workspace or prior context. If none is available, say you need the `.ics` path, URL, or raw iCal text.

## CLI facts that matter

Prefer `--json` unless the user explicitly wants raw CLI output.

Important flags:

- `--date YYYY-MM-DD` for one calendar day
- `--from YYYY-MM-DD [--to YYYY-MM-DD]` for a date range
- `--from-datetime YYYY-MM-DDTHH:mm [--to-datetime YYYY-MM-DDTHH:mm]` for a local time window
- `--today` as a shortcut for the active timezone
- `--tz <IANA zone>` or `--utc`
- `--search <pattern>` for OR search across `summary`, `description`, and `location`
- `--field <k=v>` for exact field targeting with AND semantics across repeats
- `--field-any <k=v>` for OR search across named fields
- `--limit <n>` for the next few matches
- `--exclude-status <s>` to drop cancelled items
- `--type <name>` where the default is `event`

Semantics:

- Range windows are half-open: items match when they overlap `[from, to)` or `[from-datetime, to-datetime)`
- `--to` and `--to-datetime` are exclusive
- `--from` and `--from-datetime` may be used without an end value for open-ended upcoming queries
- `--date` cannot be combined with range flags
- Repeated `--field` filters are ANDed
- Repeated `--field-any` groups are ANDed, while fields inside one `--field-any` group are ORed
- `--search` is shorthand for OR search across `summary`, `description`, and `location`
- `--exclude-status` matches statuses case-insensitively and may be repeated
- Date matching uses the active timezone, so set `--tz` when local day boundaries matter
- All-day events still use exclusive end semantics

## Default workflow

1. Determine the source and timezone that should govern phrases like "today", "this week", "tomorrow morning", or "upcoming".
2. Translate the request into:
   - a source flag
   - a date or datetime window
   - a text filter or field-specific filter
   - optional `--exclude-status CANCELLED`
   - optional `--limit`
   - `--json`
3. Run `icali`.
4. Post-process the JSON in the agent:
   - confirm the interpreted range in plain English
   - keep only the matches that answer the user's question
   - summarize clearly instead of dumping raw JSON

## Natural-language patterns

### What's on my calendar today

Use:

```bash
icali --file "/path/to/calendar.ics" --today --json
```

If the timezone should be explicit:

```bash
icali --file "/path/to/calendar.ics" --today --tz Europe/London --json
```

### What's on my calendar on a specific day

Use:

```bash
icali --file "/path/to/calendar.ics" --date 2026-04-14 --json
```

### What's on my calendar this week

Translate the phrase into an exact week window, then use a date range:

```bash
icali --file "/path/to/calendar.ics" --from 2026-04-13 --to 2026-04-20 --json
```

State the interpreted range in the answer, especially if the locale or timezone affects week boundaries.

### What's on my calendar this afternoon

Use a local datetime window:

```bash
icali --file "/path/to/calendar.ics" --from-datetime 2026-04-11T12:00 --to-datetime 2026-04-11T18:00 --json
```

### Do I have any upcoming meetings with Stacey

Prefer `--search` plus an open-ended future window:

```bash
icali --file "/path/to/calendar.ics" --from 2026-04-11 --search "/stacey/i" --exclude-status CANCELLED --json
```

If the user asks for only the next few:

```bash
icali --file "/path/to/calendar.ics" --from 2026-04-11 --search "/stacey/i" --exclude-status CANCELLED --limit 3 --json
```

### Find events matching a topic in specific fields

Use `--field` when the field itself matters:

```bash
icali --file "/path/to/calendar.ics" --field "summary=/review/i" --json
```

Use `--field-any` when the match may appear in one of several fields:

```bash
icali --file "/path/to/calendar.ics" --field-any "summary,description,location=/review/i" --json
```

### Exclude cancelled events from a normal lookup

Use:

```bash
icali --file "/path/to/calendar.ics" --from 2026-04-11 --to 2026-04-18 --exclude-status CANCELLED --json
```

## Query design guidance

Prefer these defaults:

- For day questions: `--date` or `--today`
- For week or multi-day questions: `--from` and `--to`
- For time-of-day questions: `--from-datetime` and `--to-datetime`
- For person or topic matching: `--search "/name/i"`
- For meeting-oriented questions: add `--exclude-status CANCELLED`
- For "next few" phrasing: add `--limit`

Use fielded matching only when needed:

- `--search` is the simplest natural-language default
- `--field` is for exact field targeting
- `--field-any` is for named-field OR matching

Avoid these mistakes:

- Do not answer without identifying the real `.ics` source
- Do not omit timezone handling when day boundaries or local times matter
- Do not use `--date` when the user asked for a range
- Do not use repeated `--field` flags when the user really wants OR semantics
- Do not forget that `--to` and `--to-datetime` are exclusive

## Output expectations

Return a normal calendar answer, not a CLI transcript.

Include:

- the interpreted date or datetime window
- the matching events in chronological order
- whether cancelled items were excluded when that affects the result
- a clear "no matches" answer when nothing qualifies

If the request is underspecified, say exactly what is missing:

- missing iCal source
- ambiguous timezone
- no accessible `.ics` file or feed found
