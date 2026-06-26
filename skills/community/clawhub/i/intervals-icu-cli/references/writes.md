# Write Patterns

Use these patterns when creating events, workouts, or wellness records through the `intervals` CLI.

## Preferred Pattern Order

1. `--file -` with stdin when the payload can be generated in one step
2. `mktemp` when the payload needs inspection or reuse
3. A named file only when the user explicitly wants a persistent file

## Event Creation

Use `events create` for planned sessions on a specific date.

Stdin example:

```bash
printf '%s\n' '{"category":"WORKOUT","start_date_local":"2026-03-16T00:00:00","type":"Run","name":"10km @ 5:00/km","moving_time":3000,"description":"- 10km 5:00/km Pace"}' | intervals events create --file - --format json
```

Temp file example:

```bash
tmp="$(mktemp)"
cp "{baseDir}/examples/events/create-10km-run.json" "$tmp"
intervals events create --file "$tmp" --format json
rm -f "$tmp"
```

## Event Upsert

Use `events upsert` when a stable `uid` exists and duplicates would be harmful.

```bash
printf '%s\n' '{"uid":"example-10km-run-2026-03-16","category":"WORKOUT","start_date_local":"2026-03-16T00:00:00","type":"Run","name":"10km @ 5:00/km","moving_time":3000,"description":"- 10km 5:00/km Pace"}' | intervals events upsert --file - --format json
```

## Workout Library Creation

Use `workouts create` for reusable templates, not calendar scheduling.

```bash
printf '%s\n' '{"name":"10km @ 5:00/km","description":"- 10km 5:00/km Pace","type":"Run","moving_time":3000}' | intervals workouts create --file - --format json
```

## Wellness Writes

Single day:

```bash
printf '%s\n' '{"restingHR":48,"weight":78.2,"sleepSecs":27000}' | intervals wellness put --date 2026-03-12 --file - --format json
```

Bulk:

```bash
printf '%s\n' '[{"id":"2026-03-11","restingHR":49,"weight":78.4},{"id":"2026-03-12","restingHR":48,"weight":78.2,"sleepSecs":27000}]' | intervals wellness bulk-put --file - --format json
```

## Verify Writes

After a write, prefer a read:

```bash
intervals events list --oldest 2026-03-16 --newest 2026-03-16 --format json
intervals workouts list --format json
intervals wellness get --date 2026-03-12 --format json
```
