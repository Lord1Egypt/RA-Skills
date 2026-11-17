# Spot — Watch Sweep Behavior

## Pre-sweep guard
Before loading records or invoking any platform script, check `watch.jsonl`. If the file is missing, empty, or contains zero records with `active: true`, write a brief Observation journal with `sweep_result: skipped`, `skip_reason: no_active_watches`, `watch_count: 0` and return immediately. Increment a `skipped_sweeps` metric in `metrics.jsonl`.

## Sweep procedure

1. Load all active WatchRecords from `watch.jsonl`.
   - **Expiration check**: For each record, compare target date(s) and time_window against current date/time. If the latest possible slot has passed, skip and note "expired — window passed". **Auto-deactivate expired watches** by setting `active: false`. If ALL records are expired, write Observation journal with `sweep_result: skipped`, `skip_reason: all_expired` and return.

2. For each record, call the platform script with venue, dates/range, and party_size.

3. Filter results to the record's `time_window` if set.

4. Compare found times against `last_found`. If new times exist, write an InsightProposal to Vesper and update `last_found` + `last_checked`.
   - **Change detection must compare the FULL set of found times, not just the window subset.** A sweep that finds 7 window slots matching the previous 7 window slots should still flag `changed: true` if the total slot count changed (e.g., 7 evening-only → 34 full-day). The `last_found` field stores ALL found times, not just window-filtered ones — this is what enables detecting total-set changes.
   - **Stale last_found recovery**: If `last_found` data is significantly different from what the browser returns (e.g., different count, different time ranges), treat this as new availability even if the window count happens to match. Update `last_found` to the full current set and write an Action journal.
   - **Browser crash fallback**: If browser check crashes and `last_known` data exists, use `last_found` from previous sweep. Update `last_checked` and note crash reason. Do NOT write InsightProposal when using fallback data.

5. Always update `last_checked`, even when no availability found or using fallback data.

6. Write journal entry: Observation type if no new availability; Action type if InsightProposal written. Include `watch_count` in every sweep journal.

## Sweep frequency guidance
When `watch.jsonl` has zero active records, relax the cron interval (e.g., every 2 hours instead of every 15 minutes). Skipped sweeps cost ~50 tokens vs ~3000 for full sweeps.