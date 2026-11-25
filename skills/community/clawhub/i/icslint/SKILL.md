---
name: icslint
description: Lint an iCalendar (.ics) file against RFC 5545's actual requirements and the documented import failures of Google, Outlook and Apple Calendar. Use when asked to check, validate or lint an .ics or calendar file, debug a calendar import failure, or check calendar files in CI — for example "check this .ics file", "why did Google Calendar fail to import this calendar", or "lint these calendar files before I ship them". Checks structure, required properties, date/time forms, TZID and VTIMEZONE form, and RRULE syntax, each finding citing an RFC 5545 section or a named importer source. Not for ham-radio ADIF logs (that is adifcheck) or Darwin Core / GBIF occurrence files (that is dwccheck).
license: MIT
compatibility: Requires Python 3.10+. Zero dependencies; runs fully offline with no timezone database. Network is needed only to install.
---

# icslint

## What this tool does

icslint checks `.ics` files against the requirements RFC 5545 actually states, plus the import failures Google, Outlook and Apple Calendar are documented to have — 67 rules covering serialisation (CRLF, folding, UTF-8), the VCALENDAR envelope, required properties, date/time value forms, TZID/VTIMEZONE form, RRULE syntax and form cross-checks, and TEXT escaping. Every finding names the file, the physical line, the component, the rule ID, the severity, a plain-language explanation, and its source: an RFC 5545 section, or a named, dated importer source labelled "Importer behaviour" — the two are never blended silently. It reports only; it never edits, fixes or converts the file.

## Install

```bash
pip install git+https://github.com/RakTikoo/icslint
```

This provides the `icslint` command.

## Run

Check one file, or a folder (scanned recursively for `*.ics` files):

```bash
icslint check examples/broken.ics
icslint check path/to/calendars --format json
```

`--format json` emits the same findings as JSON for CI tooling. `--strict` makes warnings fail the run as well as errors.

## Reading the results

Findings print one per line: `file:line: ERROR|WARNING RULE-ID [COMPONENT[UID=...]] explanation (source)`. The last line is the tally, printed with real singular/plural forms and both counts always shown: `icslint: 1 file checked, 2 errors, 1 warning`, `icslint: 1 file checked, 1 error, 0 warnings`, `icslint: 2 files checked, 2 errors, 1 warning` — or `icslint: 1 file checked, no findings` when every file is clean. Severity is calibrated: an ERROR is an RFC MUST / MUST NOT / REQUIRED / ABNF violation, or a hard import failure a named source documents; a WARNING is an RFC SHOULD / SHOULD NOT, an importer-documented soft failure, or an RFC MUST that importers routinely waive through a defined fallback. The exit code is the verdict:

- `0` — no errors (warnings allowed, unless `--strict` is on).
- `1` — at least one error, or any warning under `--strict`.
- `2` — usage error or unreadable input, always a one-line message, never a traceback.

Zero findings on a file is a meaningful result: legal constructs such as a missing SUMMARY, a missing DTEND, floating times, lowercase property names, `X-` properties, or an RRULE with neither COUNT nor UNTIL are deliberately silent.

## Limits

- **No recurrence expansion.** icslint never generates the instances an RRULE describes. It checks the rule's syntax and the form cross-checks the spec states, but it will not tell you whether an EXDATE matches a real occurrence, whether a RECURRENCE-ID names a generated instance, or whether a recurrence set is empty.
- **No DST / VTIMEZONE transition semantics.** VTIMEZONE components are checked for existence and form only. The tool never judges whether an offset is correct for a zone, whether a local time falls in a DST gap or a repeated hour, or what instant a TZID time really is; it stays silent on DTEND-versus-DTSTART ordering whenever comparing them would need a zone's offsets (same-form pairs only).
- **No fixing, no conversion.** The tool reports; it never edits your file.
- Citations say what the source actually says: where an importer source's own lint is more lenient than icslint (for example warning where icslint errors on a duplicate UID or a missing DTSTAMP), the error rests on the RFC MUST, and the finding does not imply the importer source calls it an error. One rule, S04 (a fold splitting a multi-byte UTF-8 character), is robustness advice rather than an RFC violation, and its finding says so.
