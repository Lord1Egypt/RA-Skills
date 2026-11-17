# ICS Export How-To + Meeting Audit Methodology

## Exporting your calendar (2 minutes)

**Google Calendar** — web → Settings → *Import & export* → *Export* → downloads a
zip of per-calendar `.ics` files. (Alternatively, a single calendar → Settings →
"Export calendar" for just that one.)

**Outlook (desktop/M365)** — File → Save Calendar → date range: choose 2–3 months →
detail: Full details → .ics.

**Outlook (web)** — Calendar → Share calendar is *not* it; use "Export calendar"
under Settings → ~ or open calendar in OWA → … → Export.

**Apple Calendar** — select calendar in the list → File → Export → Export.

**Zoom/Teams recurring links** export as regular VEVENTs with RRULEs if they were
created from the calendar; meetings scheduled inside the app may only appear in the
app — export from the app or sync it to your calendar first.

Share exports of colleagues only with consent; attendee lists are personal data.

## What the audit looks for

### Volume metrics
- **meeting h/week** — the headline; >8h/wk for an IC or >12h for a lead needs active management
- **double-booked min/week** — systematic double-booking means either delegation
  failure or calendar anarchy; either is fixable once visible
- **per-series person-hours** — `hours × attendees × frequency`: the honest price tag
  that turns "it's just 30 minutes" into "that's 4% of the team's week"

### Placement metrics (the hidden story)
- **focus blocks** — count of ≥90-min meeting-free windows per week. Research on
  task switching puts meaningful recovery/immersion needs in the 90-min range; days
  with zero such blocks are effectively meeting-only days regardless of total hours
- **fragmentation** — work minutes minus the longest block: how much of the day is
  shattered into <90-min shards
- Two calendars with identical meeting hours can differ 2× in focus blocks — that's
  why `stats` and `focus` are separate commands

### Series health signals
- attendance decay (many declines/absentees in later occurrences)
- cancellation/reschedule rate
- status-shape ("sync", "check-in", "touchpoint" with 4+ people and no artifacts)
- length mismatch (60-min slots that consistently end early)

## The prescription rules (explicit, so you can argue with them)

| Rule | Trigger | Rationale |
|---|---|---|
| KILL/ASYNC | status-shaped name keywords | information transfer doesn't need synchronized time; replace with a written thread |
| SHORTEN | avg ≥55 min | Parkinson's law: meetings expand to the slot; 45/25 defaults recover ~25% with no measured cost |
| DE-DENSITY | weekly + ≥30min + recurring | weekly cadence is a habit, not a requirement; biweekly halves cost, quarterly reviews catch drift |
| BATCH | fragmented worst-day | clustering scattered meetings frees whole half-days; scattering destroys them |

Missing (deliberately): automatic "decline" advice — prescriptions are inputs to a
human decision, not verdicts.

## Running the change

1. Measure 4 weeks (`--weeks 4`). Don't argue from one bad week.
2. `simulate` before proposing. Numbers defuse politics: "the math says 6 h/week back"
   is not an accusation.
3. Change one thing at a time (kill one series, shorten one block). Re-measure in a
   month. Meeting culture regrows like weeds; re-audit quarterly.
4. For teams: collect exports (consensually), run `team`, look for load asymmetry —
   often one person silently absorbs the meeting load for the group.

## Privacy notes

- Everything runs locally on exported files; nothing is uploaded by this tool.
- Calendar exports contain names, emails, and meeting titles — treat them as sensitive;
  delete the `.ics` files after the audit or store them somewhere access-controlled.
- The `team` command aggregates per-person; share results as aggregates, and let
  individuals opt out of the export.

## ICS parsing limitations (honest list)

- Recurrence handled: FREQ DAILY/WEEKLY, INTERVAL, COUNT, UNTIL, BYDAY, EXDATE.
- MONTHLY/YEARLY expand via approximation (interval × 4 / × 52 weeks) — good enough
  for load stats, not for exact calendars; flagged in output.
- No timezone conversion: times are treated as local wall-clock. If your export
  contains multi-timezone travel, do the audit on a period without travel.
- Declined-event filtering relies on STATUS:CANCELLED (removals). Some servers encode
  declines per-attendee (PARTSTAT) — those still count; check `list` for surprises.
