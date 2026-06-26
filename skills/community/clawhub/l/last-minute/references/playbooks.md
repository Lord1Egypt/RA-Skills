# Playbooks — last-minute

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| dep-date | `--dep-date` | Default: **today** |
| sort-type | `--sort-type` | Default: **6** (earliest departure) |
| dep-hour-start | `--dep-hour-start` | Default: **current hour + 1** |
| dep-hour-end | `--dep-hour-end` | Default: 23 |
| dep-date-start | `--dep-date-start` | Optional: 3-day window start |
| dep-date-end | `--dep-date-end` | Optional: 3-day window end |

---

## Playbook A: Same-Day Urgent

**Trigger:** User says "fly today", "当天机票", "马上飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --dep-hour-start {now+1} --sort-type 6
```

**Output:** Flights departing within hours, earliest first.

---

## Playbook B: Tomorrow Morning

**Trigger:** User says "tomorrow morning flight", "明早航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --dep-hour-start 6 --dep-hour-end 12 --sort-type 6
```

**Output:** Morning flights for tomorrow, earliest departure first.

---

## Playbook C: Within 3 Days Bargain

**Trigger:** User says "last minute deal this week", "这几天有便宜票吗".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {today} --dep-date-end {today+3} --sort-type 3
```

**Output:** Cheapest flights within the next 3 days.

---

## Playbook D: Broad Search (no last-minute found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 6
flyai keyword-search --query "{origin} to {destination} last minute flights today"
```

**Output:** Broader search without hour filter + keyword fallback.
