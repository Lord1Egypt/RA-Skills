# Recurring Events

A recurring event is an event that repeats automatically on a rule, e.g. "a weekly sync every Monday at 9:00" - create it once and it keeps recurring.
This document explains how to modify/delete one **occurrence** of a recurring event versus the whole **series** - the two target different objects and must not be confused.

## Core concept: one occurrence vs. the whole series

A recurring event consists of three parts:

| Concept | What it is | Where you see it |
|---------|------------|------------------|
| **Master event** | The whole series (including the rule) | `read` shows the 🆕 series master event ID line; `list --from` expands occurrences; creation-filter lists can return masters |
| **One occurrence** | A single instance of the series | One line per item in `list`, marked 🔁(series) |
| **An individually modified occurrence** (exception) | One occurrence modified/cancelled on its own | `list` marks 🔁(modified) / 🔁(cancelled) |

**Core rule**: modify/delete/move on "one occurrence" affects only that occurrence; changing the rule or deleting the whole series must operate on the **master event** (the 🆕 series master event ID in `read` output).

## Structured recurrence input

The model converts the user's recurrence request into a Microsoft Graph `recurrencePattern` object. Pass that object as JSON with `--repeat`, or save it to a UTF-8 file and use `--repeat-file pattern.json` to avoid shell quoting problems. The file contains the pattern itself, without a `pattern`, `range`, or `recurrence` wrapper. Natural-language rule strings are rejected.

| Request | JSON pattern |
|---------|--------------|
| Every 2 days | `{"type":"daily","interval":2}` |
| Every Friday | `{"type":"weekly","interval":1,"daysOfWeek":["friday"],"firstDayOfWeek":"monday"}` |
| Monday and Wednesday every 2 weeks | `{"type":"weekly","interval":2,"daysOfWeek":["monday","wednesday"],"firstDayOfWeek":"monday"}` |
| Every weekday | `{"type":"weekly","interval":1,"daysOfWeek":["monday","tuesday","wednesday","thursday","friday"],"firstDayOfWeek":"monday"}` |
| Every 3 months on the 15th | `{"type":"absoluteMonthly","interval":3,"dayOfMonth":15}` |
| Last Friday of each month | `{"type":"relativeMonthly","interval":1,"index":"last","daysOfWeek":["friday"]}` |
| September 21 every year | `{"type":"absoluteYearly","interval":1,"month":9,"dayOfMonth":21}` |
| Last Wednesday of November every year | `{"type":"relativeYearly","interval":1,"month":11,"index":"last","daysOfWeek":["wednesday"]}` |

These patterns use the six [Microsoft Graph recurrence pattern types](https://learn.microsoft.com/en-us/graph/api/resources/recurrencepattern?view=graph-rest-1.0). The CLI requires every applicable field shown above; it never infers an interval, weekday, week boundary, or ordinal from the event start date.

- `interval` is a positive integer (maximum 2,147,483,647); `dayOfMonth` is 1–31 and `month` is 1–12. Boolean values, fractional numbers, and numeric strings are invalid. A yearly month/day combination must be a possible date; February 29 is allowed.
- `daysOfWeek` is a nonempty list of distinct lowercase names: `monday` through `sunday`. `firstDayOfWeek` takes one of those names and is required for `weekly`.
- `index` is required for relative patterns: `first`, `second`, `third`, `fourth`, or `last`. It does not accept `fifth`.
- Relative monthly/yearly patterns with multiple weekdays select the first date that matches the pattern in that month; they do not create one occurrence per weekday. Clarify the user's intended rule before choosing this shape.
- Unknown fields, duplicate JSON keys, fields for another pattern type, and missing fields produce an error. The CLI does not silently ignore supplied data.

End conditions work with either `--repeat` or `--repeat-file`. Omit both for no end, or choose exactly one:

- `--repeat-until 2026-12-31`: inclusive final date, in exact `YYYY-MM-DD` form, no earlier than the event start date.
- `--repeat-times 5`: 5 occurrences in total, as a positive integer (maximum 2,147,483,647).

These rules also apply when updating a series: a new pattern rebuilds the range. To retain an existing end date or count, read it and supply the corresponding option explicitly; omitting both makes the series open-ended.

The backend derives `range.startDate` from the explicit event start and sets the recurrence time zone to the effective event time zone. The model resolves ambiguous recurrence wording; the backend validates and submits these concrete fields.

## Common operations

| What you want | How |
|---------------|-----|
| Change one occurrence's time (this occurrence only) | `update <occurrenceID> --start ... --end ...` (creates an "exception"; the rest stays) |
| Delete one occurrence (this occurrence only) | `delete <occurrenceID>` (do not add `--series`) |
| Change the whole series rule | `read` to get the series master event ID → `update <masterID> --repeat-file pattern.json` |
| Remove recurrence (back to single) | `update <masterID> --repeat ""` |
| Delete the whole series | `delete <masterID>` (warns) or `delete <occurrenceID> --series` |
| Next occurrence | `next <occurrenceID or masterID>` |
| Shift the whole series by days | `move <masterID> --days N` (warns) |

## Things to watch out for

- **Changing the whole series rule resets** occurrences that were individually modified/deleted before (a warning is shown; warn the user first)
- Moving one occurrence to a time that **overlaps an adjacent occurrence** is rejected ("adjacent occurrence conflict") - the new time must be no earlier than the previous occurrence and no later than the next one
- A deleted occurrence **cannot be accessed again** (reports "does not exist"); re-run `list` to confirm
- Graph's six pattern types do not cover hourly recurrence or intervals counted in working days. Explain the limitation; do not approximate the user's rule silently.
