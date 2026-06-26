# Cross-Domain Branch

Use this branch for summaries, dashboards, sync, and automation maintenance.

## Scope

- rebuild monthly health calendar rows
- rebuild weekly health assessment rows
- create dashboard blocks over the monthly table
- run narrow refreshes after upstream changes

## Order

1. Identify the target artifact:
   - monthly calendar
   - weekly assessment
   - dashboard
2. Refresh only the minimum upstream dependency set.
3. Rebuild the target artifact.
4. Stop.

## Rules

- prefer summary-layer tables first
- do not reopen all raw-domain logic on the first pass
- rebuild the narrowest date window possible
- report partial refreshes explicitly

## Runbook

Assume all commands run from `skills/healthcare-feishu/scripts/` and use an environment-specific config JSON.

### 1. Rebuild monthly calendar rows

Narrow refresh for a specific date window:

```bash
python3 rebuild_monthly_calendar.py <config.json> \
  --identity user \
  --start-date 2026-04-29 \
  --end-date 2026-04-30 \
  --json
```

Behavior:

- reads `nutrition_daily_history`, `sleep_recovery`, and `exercise_workout`
- aggregates into `monthly_health_calendar`
- upserts by `Date`
- writes `Date` as `YYYY-MM-DD 00:00:00`

### 2. Rebuild weekly assessment rows

Single explicit week:

```bash
python3 rebuild_weekly_assessment.py <config.json> \
  --identity user \
  --week-end 2026-05-03 \
  --json
```

Backfill all complete weeks visible from the upstream summary layer:

```bash
python3 rebuild_weekly_assessment.py <config.json> \
  --identity user \
  --backfill-full-weeks \
  --json
```

Behavior:

- reads `nutrition_daily_history`, `sleep_recovery`, and `exercise_workout`
- aggregates into `weekly_health_assessment`
- upserts by `Week Start` + `Week End`
- uses `weekly_thresholds` from config when present, otherwise script defaults

### 3. Build or refresh monthly dashboard

```bash
node build_monthly_dashboard.js <config.json> \
  --identity user
```

Optional dry run:

```bash
node build_monthly_dashboard.js <config.json> \
  --identity user \
  --dry-run
```

Behavior:

- reads `feishu.active_base.token`
- reads `feishu.tables.monthly_health_calendar.name`
- creates or reuses `Monthly Health Calendar Overview`
- creates missing blocks and updates existing blocks by block name
- fails fast on same-name type mismatches instead of silently mutating them

### 4. Recommended execution order

For a normal monthly refresh:

1. rebuild the smallest monthly date window needed
2. rebuild the affected weekly window if the date change crosses a full week boundary
3. refresh the monthly dashboard

### 5. Safety notes

- keep table names and pinned `table_id` values in config, not in code
- if a Base has same-name table collisions, prefer pinned `table_id`
- do not delete existing summary rows unless the user explicitly asks for destructive cleanup
- treat `base +record-delete` as a separate explicit operation, not part of routine rebuilds
