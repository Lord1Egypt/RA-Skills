# Conflict Scan Report Output Format

Template for `sands.schedule.conflicts` cron output. Produces a structured, scannable report.

## Template Structure

```markdown
## 🗓️ Daily Schedule Conflict Scan — {date} ({time} {tz})

**Scan window:** {start_date} – {end_date} ({tz})
**Calendars queried:** {list}
**Events scanned:** {total} total ({timed} timed, {all_day} all-day)

---

### 🚨 CONFLICTS ({count})

#### {n}. {severity_emoji} {day}, {time_range} — {overlap_type} ({minutes} min)

| Event | Calendar | Flexibility | Signals |
|-------|----------|-------------|---------|
| {title_a} | {cal_a} | **{flex_a}** | {signals_a} |
| {title_b} | {cal_b} | **{flex_b}** | {signals_b} |

**→ Resolution:** {specific recommendation}

---

### 🔁 CROSS-CALENDAR DUPLICATES ({count})

| Title | Calendar A | Calendar B | Start |
|-------|-----------|-----------|-------|
| {title} | ✅ | ✅ | {start} |

**→ Recommendation:** Remove from {non_canonical} calendar — {canonical} is the canonical source.

---

### ⚪ ZERO-DURATION WARNINGS ({count})

| Event | Calendar | Start | Note |
|-------|----------|-------|------|
| {title} | {cal} | {time} | {assessment} |

---

### ⚠️ TIGHT BACK-TACK CHAINS ({count})

**{date}:** {chain description with times}
{Gap analysis and recommendation}

---

### 📊 SUMMARY

| Category | Count |
|----------|-------|
| Full conflicts | N |
| Overlapping bookings | N |
| Cross-calendar duplicates | N |
| Zero-duration warnings | N |
| Tight back-to-back chains | N |

### 🎯 RECOMMENDED ACTIONS

1. **{Date}:** {actionable step}
```

## Severity Emojis

- 🔴 Full overlap (same time, different events)
- 🟡 Partial overlap (some shared time)
- ⚪ Zero-duration / data quality
- 🔁 Duplicate (cross-calendar)
- ⚠️ Back-to-back / travel concern

## Conflict Detail Format

For each conflict, always include:
1. Day and time range in user's timezone
2. Overlap duration in minutes
3. Both events with their calendar source
4. Flexibility classification with specific signals
5. A concrete resolution recommendation

## Evidence Log Format

The evidence record for each scan should include:
```json
{
  "timestamp": "ISO timestamp",
  "command": "sands.schedule.conflicts",
  "calendar_ids": ["list"],
  "event_count": N,
  "timed_events": N,
  "all_day_events": N,
  "overlaps_found": N,
  "cross_calendar_duplicates": N,
  "intra_calendar_duplicates": N,
  "zero_duration_warnings": N,
  "gap_detected": bool,
  "degraded": [],
  "calendar_errors": {},
  "conflicts": [...],
  "cross_calendar_duplicates": [...],
  "zero_duration_warnings": [...],
  "back_to_back_chains": [...]
}
```

## Back-to-Back Chain Detection

A "chain" is 3+ consecutive events on the same day with gaps ≤ 15 minutes. Report:
- Date
- Full chain as a single line: `Event A (time) → Event B (time) → Event C (time)`
- Note gaps of 0 min (events touching) vs small gaps (5-15 min)
- Flag if no travel time exists between presumably different locations
