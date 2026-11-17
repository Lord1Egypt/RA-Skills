# Conflict Detection

Run conflict detection:
- Automatically after `sands.event.create` and `sands.event.modify`
- On demand via `sands.schedule.conflicts`

## Definition

A conflict exists when:
- Two events overlap by any amount of time, OR
- Travel time to an event would need to begin before the preceding event ends, OR
- The same event appears on multiple calendars (cross-calendar duplicate), OR
- The same event appears twice on the *same* calendar (intra-calendar duplicate)

All-day events are treated as low-priority background blocks: they do not trigger conflicts with timed events unless the user explicitly asks.

## Cross-Calendar Duplicates

When the same event appears on multiple calendars (e.g., Personal + Family), detect by matching `summary` + `start` time + `location`. Normalize to local time before comparing — different calendars may store the same event with different UTC offsets (e.g., one at `-07:00`, another at `Z`), making them appear to be at different times when they are actually the same.

### Location Normalization

Calendar APIs may store the same venue with slightly different location strings. Before comparing locations for duplicate detection, normalize both:

1. **Strip ZIP/postal codes** — `"MacMillan Pier, Provincetown, MA 02657, USA"` → `"MacMillan Pier, Provincetown, MA"` (trim trailing `\d{5}(-\d{4})?, USA`)
2. **Lowercase both** for case-insensitive comparison
3. **Check substring containment** — If one location is fully contained within the other (after ZIP stripping), treat as matching
4. **If locations don't match exactly**, check landmark overlap — both mentioning "MacMillan Pier" even if one has street address and the other doesn't

### Fuzzy Title Matching

Events describing the same activity may have different titles across calendars:
- `"Dolphin Fleet Sunset Whale Watch"` (Personal) vs `"Whale Watching"` (Family)

When locations match (after normalization above) and start times are within 10 minutes, use fuzzy title matching:
- **Shared keyword overlap**: both titles contain `"whale"` → high confidence they're the same event
- **Title containment**: stripping qualifiers from one title (`"Dolphin Fleet Sunset "`) reveals the core subject matches the other
- Check if both titles reference the same noun (e.g., both contain "pier", "dinner", "appointment", "flight")

Flag as severity **DUPLICATE** with both calendar names in the conflict note. Recommend removing the copy from the non-canonical calendar (typically the family/shared calendar, keeping the primary calendar's copy).

## Intra-Calendar Duplicates

The same event can appear *twice on the same calendar*, typically caused by:
- **Booking platform double-imports** — Fresha, UCSF MyChart, and similar platforms sometimes create both a detailed event and a separate auto-generated summary event at the same time.
- **Calendar sync artifacts** — Syncing the same booking source via two different paths (e.g., email invite + calendar feed).

Detect by matching `summary.lower()` + `start_local` within the same `cal_id`. When found:
- If one has correct duration and the other is zero-duration → the zero-duration one is almost certainly the artifact. Recommend deleting it.
- If both have identical duration and details → recommend deleting one (they're the same booking).
- If both have different details (e.g., one has location, one doesn't) → keep the more detailed one, delete the sparser one.

Flag as severity **DUPLICATE** with `intra_calendar: true` in the evidence log.

## Resolution

Do not auto-resolve conflicts. Present them with a flexibility assessment and candidate resolutions for the user to choose from. See `references/flexibility_rules.md`.

## Zero-Duration Events

A zero-duration event has `start == end` (e.g., `2026-06-11T14:45:00-07:00` for both). These do not produce overlap conflicts by the standard definition, but they are almost always a data quality issue — the end time was likely not set correctly during creation.

**Action:** Flag as a `zero_duration` warning in the conflict report. Include the event title, start time, and a note suggesting the user verify the intended duration. Do not treat as a conflict — treat as a data integrity note.

Example:
```
WARNING: [NEW PATIENT VISIT with Niti Shahi] zero_duration: start == end at 2026-06-11T14:45-07:00. The description mentions 3:00 PM — the end time may not have been set correctly.
```

## Validation

Before creating any event:
- Confirm no exact-duplicate title+time exists on that calendar
- Confirm the slot is not blocked by a work busy period (warn, do not block)
- Confirm the end time is after the start time (non-zero duration)

Before inserting travel:
- Gap must be >= calculated travel time + buffer. If not, surface conflict instead of creating a truncated or overlapping travel block.

## Timezone Normalization for Cross-Calendar Comparison

**Critical:** Different calendars may store the same event in different timezones. The Family calendar often stores in UTC (`Z`), while Personal stores in local time (`-07:00`). Before comparing events across calendars:

1. Parse each event's start/end with its original timezone offset
2. Convert to the user's local timezone (`America/Los_Angeles`) for display
3. For cross-calendar duplicate detection, compare `(summary.lower(), start_local, location.lower())` — NOT the raw UTC timestamps

**Same event ID across calendars:** If the same Google Calendar event ID appears on both Personal and Family, it's the same event visible through shared calendar membership — NOT a sync artifact. Check the event ID, not just the time+title, to distinguish true duplicates from shared membership.

## Back-to-Back Chain Detection

A "chain" is 3+ consecutive timed events on the same calendar day with gaps ≤ 15 minutes between them. These warrant surfacing because:
- Zero-gap chains (Event B starts exactly when Event A ends) leave no room for travel
- Even 5-15 min gaps may be insufficient for transit between different locations

**Detection:**
1. Sort all timed events for each day by start time
2. Calculate gap = next_event.start - current_event.end
3. Chain = sequence where all gaps ≤ 15 min and length ≥ 3
4. Report the full chain with times and flag gaps of 0 min specifically

## Detection Algorithm (Cron-Compatible Pattern)

```python
# 1. Fetch all timed events (exclude all-day) from relevant calendars
# 2. Normalize all start/end to local timezone for display; keep UTC for comparison
# 3. Sort by start_utc
# 4. Check all pairs for overlap: a.start < b.end AND b.start < a.end
# 5. For each overlap, calculate overlap_minutes
# 6. Classify each event per flexibility_rules.md
# 7. Check for zero-duration (duration_min == 0)
# 8. Check for cross-calendar duplicates: group by (summary.lower(), start_local, location.lower()) across different cal_ids
#    - Compare event IDs: same ID = shared membership, not duplicate
#    - Different ID + same time+title = true cross-calendar duplicate
# 9. Check for intra-calendar duplicates: group by (summary.lower(), start_local) within the same cal_id
# 10. Detect back-to-back chains: 3+ events on same day with gaps ≤ 15 min
```

## Cron Mode Execution

When `execute_code` is blocked (cron jobs), run the conflict analysis manually:
1. Fetch events from each calendar via `mcp_google_workspace_get_events`
2. Convert all times to local timezone (PDT/PST) — Family calendar often stores in UTC
3. Sort by start time and check adjacent pairs for overlap
4. Classify flexibility using `references/flexibility_rules.md`
5. Write evidence via `scripts/append_jsonl.py` helper (NEVER `write_file` on JSONL)
6. Update `config.json last_conflict_scan` timestamp

The manual path is reliable for ≤30 events across 3 calendars. For larger datasets, write the analysis script to `/tmp/` and execute via `terminal`.