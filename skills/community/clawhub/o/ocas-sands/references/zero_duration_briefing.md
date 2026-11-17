# Zero-Duration Events in Sands Briefings

## The bug (caught 2026-07-23, evening-brief run)

An event with `start == end` (e.g. `"12:45"` → `"12:45"`) is a **zero-duration**
artifact — almost always a UCSF MyChart double-import where the end time was
never captured. The skill's `span_minutes()` helper has a midnight-crossing
guard:

```python
def span_minutes(start_hhmm, end_hhmm):
    s = to_min(start_hhmm)
    e = to_min(end_hhmm)
    if e <= s:          # 12:45 -> 12:45 triggers this
        e += 1440       # expands to a 24-hour span (765 -> 2205)
    return s, e
```

For a zero-duration event this guard wrongly expands it into a **24-hour busy
span**. Two consequences:

1. **False conflicts** — the 24h span overlaps every later event. In the
   2026-07-23 run a `12:45 Appointment` was reported as overlapping `Gym`
   (13:30–15:30) by 120 minutes. There was no real conflict.
2. **Polluted free-hours** — `calc_free_hours` treated the 24h span as a full-day
   block, deflating the free-hours number.

## The fix

Exclude zero-duration events from BOTH conflict detection and free-hours math
**before** calling `span_minutes`. Flag them as `zero_duration` warnings in the
report instead.

```python
# at parse time
zero_duration = is_timed and (start_hhmm == end_hhmm)

# conflict detection: only compare durational events
durational_events = [e for e in timed_events if not e.get('zero_duration')]

# free hours: skip zero-duration events
if ev.get('zero_duration'):
    continue
```

Both `templates/sands_briefing_morning.py` (patched 2026-07-23) and
`templates/sands_briefing_evening.py` (written correct from the start) do this.

## Evening-brief run-completion persistence (2026-07-23 recipe)

The briefing templates are pure generators. The calling cron run must persist:

1. Dated brief JSON →
   `{journal_dir}/{target_date}_evening_brief.json` (full record: observation,
   events, summary_note, briefing_payload).
2. `evidence.jsonl` — append via
   `scripts/append_jsonl.py` (NEVER `write_file` — it overwrites).
   Fields: `timestamp`, `command: sands.briefing.generate`, `mode: evening`,
   `target_date`, `status`, `degraded`, `auth_account`, `auth_fallback_used`,
   `total_events`, `conflicts_detected`, `zero_duration_warnings`, `free_hours`.
3. `action.jsonl` — same `append_jsonl.py` helper (briefing.generate is an
   Action Journal command).
4. `config.json` — set `last_evening_brief` to the run timestamp.

Cron-mode note: `execute_code` is blocked in cron. Write the generator to
`/tmp/`, run it with `terminal("python3 /tmp/...py")`, read its stdout/JSON.
