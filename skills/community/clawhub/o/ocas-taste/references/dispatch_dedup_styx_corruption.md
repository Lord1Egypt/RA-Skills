# dispatch_taste_dedup — Styx Corruption Incident (2026-07-22)

## What happened
During the daily 13:12 `taste:scan` cron, after the Styx delta wrote 49 new signals,
`dispatch_taste_dedup.py` was run (it is described in SKILL.md as "run after EVERY
dispatch-triggered scan"). It deleted **47 of 49** just-ingested Styx signals and
corrupted `signals.jsonl` to 437 styx signals with mass `(merchant,date)` duplicates.

## Root cause
`dispatch_taste_dedup.py` dedups on key `(venue_name, event_date[:10], extraction_source)`.
- Email/calendar signals carry `event_date` (ISO datetime).
- **Styx signals carry `date` (YYYY-MM-DD), NOT `event_date`.**

So every Styx signal's key collapsed to `(venue_name, None, 'styx')`, and the dedup kept
only the first per venue — silently destroying the rest.

## Recovery recipe (used successfully)
1. Roll back to the last known-good snapshot: the daily cron writes
   `signals.jsonl.bak.delta.YYYYMMDDTHHMMSS` and `items.jsonl.bak.delta.YYYYMMDDTHHMMSS`.
   ```bash
   cd ~/.hermes/commons/data/ocas-taste
   cp signals.jsonl signals.jsonl.corrupt.<date>.bak
   cp items.jsonl  items.jsonl.corrupt.<date>.bak
   cp signals.jsonl.bak.delta.<YYYYMMDDTHHMMSS> signals.jsonl
   cp items.jsonl.bak.delta.<YYYYMMDDTHHMMSS>  items.jsonl
   ```
2. Verify the snapshot is clean: `python3 scripts/verify_taste_delta.py` → expect only the
   pre-existing 1 orphan (a stale June-20 Rainbow Grocery signal), zero dupes.
3. Re-run the Styx delta with the corrected script (atomic, self-healing):
   `python3 $HERMES_HOME/../indigo/skills/ocas-taste/scripts/styx_delta_corrected.py`
4. Re-verify: `python3 scripts/verify_taste_delta.py` → must print `VERIFY PASSED (EXIT=0)`.

## Durable rules (do NOT violate)
- **Never run `dispatch_taste_dedup.py` on the daily 13:12 job.** It is for DISPATCH WAVES
  only (those signals have `event_date`). The daily job's Styx signals do not.
- After ANY Styx delta write, the only mandatory post-check is `verify_taste_delta.py`.
  Do not run other dedup tools unless you have confirmed they handle the Styx `date` field.
- A "N created" return from an ingestion script is **testimony, not proof**. Always verify.

## Other delta bugs caught and fixed in `styx_delta_corrected.py`
- Styx `transaction_merchants` has **duplicate rows per transaction**; dedup candidates by
  `(norm(name), date)` before enriching or you emit 2-3 identical signals.
- Append linked signals to `new_signals` — an earlier version only linked in memory and
  dropped them on write.
- `items_by_name` join must use the same normalization as the lookup (`norm()` strips
  non-alphanumerics), or pre-existing orphans won't be healed.
- Write signals + items **atomically** (rebuild both files in memory, overwrite once), so a
  crash mid-run can't leave a half-written store. Roll back by restore-from-snapshot, not
  by hand-editing jsonl.
