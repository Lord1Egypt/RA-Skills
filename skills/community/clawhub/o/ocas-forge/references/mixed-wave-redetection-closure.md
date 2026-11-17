# Mixed-Wave Re-Detection Closure (closure-only)

## Trigger
A dispatcher fire carrying BOTH a `new_journals` item AND a `new_emails` item, where
a **different, LATER wave** (its `dispatch-wave-*.json` `timestamp` is AFTER this fire's
`detected_at`) has **already fully processed** the same `new_files` + email threads.
This is the "newer concurrent wave already closed this detection" exception
(ocas-forge SKILL.md, confirmed 2026-07-14T14:59Z). It is common: the dispatcher scans
every ~5 min, so a wave that landed minutes after the current detection is the normal
re-fire cause — NOT a prior-wave misclassification (don't confuse with the recovery case
in `references/session-20260714-dispatch-recovery.md`, which rewrites a misclassified wave).

## Do NOT
- Re-run Forge scan / Mentor heartbeat / Praxis ingest.
- Mint a new `dispatch-wave-*.json` or rewrite the existing one.
  Both orphan the existing wave journal and re-fire the dispatcher.

## Detection (pre-flight)
1. `grep` `commons/journals/ocas-dispatch/<DATE>/dispatch-wave-*.json` for entries with
   `timestamp > detected_at` referencing the same journal paths / email threads.
2. Confirm that wave ran the pipeline: a `forge-scan-*.json` for the window exists,
   a Mentor heartbeat ran, Praxis ingest appended (or its `outcome` says pipelines ran).
3. Confirm both dispatcher `new_files` are present in BOTH eval stores
   (`commons/data/ocas-praxis/journals_evaluated.jsonl` key `journal_id`,
    `commons/data/ocas-dispatch/journals_evaluated.jsonl` key `filename`).
4. Confirm `ingest_state.json` `last_ingest_run` is past the `new_file` mtimes.
If all four hold → clean re-detection. Closure-only.

## Closure-only procedure (verified 2026-07-15)
`bridge_eval_inline.py` EXISTS and works as of 2026-07-15 (idempotent dual-store append
with `--require-exists` phantom guard — see Support File Map). Prefer it over the manual
append below; the manual `append_unique_eval` is the fallback only if the script is missing.

```python
def append_unique_eval(fpath, key_field, key_val, action_taken, source, backfill_at):
    if os.path.exists(fpath):
        with open(fpath) as f:
            for line in f:
                if key_val in line:
                    return False
    with open(fpath, "a") as f:
        f.write(json.dumps({key_field: key_val, "action_taken": action_taken,
                            "source": source, "backfill_at": backfill_at}) + "\n")
    return True
# PRAXIS_EV: key_field="journal_id";  DISPATCH_EV: key_field="filename"
# relpath form: "ocas-mentor/2026-07-15/mentor-light-20260715T030357Z.json"
```

Steps:
1. **Bridge residual one-sided gaps** — a journal present in one eval store but missing
   from the other (typically post-dispatch `mentor-light-*` heartbeats the prior wave's
   bridge skipped). Append to the missing store with `action_taken: post_dispatch_cleanup`.
   Also bridge the prior wave's `triage-*.json` evidence journal if it is one-sided.
2. **Infinite mentor-cron convergence loop** — the Mentor light heartbeat cron writes a
   new `mentor-light-*.json` every ~5 min, so a single bridge pass can NEVER be
   permanently stable: a heartbeat lands *during* the pass. Handle with a bounded
   per-skill `os.listdir` sweep (NOT recursive `glob`/`os.walk` — self-nested `journals/`
   symlinks emit false positives): for every `*.json` (exclude `dispatch-wave-*`) with
   mtime > `last_ingest_run` and missing from a store, append it; then advance
   `last_ingest_run` to the max bridged mtime; repeat until a sweep adds 0.
3. **Advance `last_ingest_run`** via full-file `json.load` + `write_file` (never `read_file`
   — stale copy; never `patch` — duplicate-key corruption). Set it to ISO of the max mtime
   among ALL today-dated journals in `commons/journals/<skill>/<DATE>/` (bounded per-skill
   `os.listdir`, NOT recursive glob) — NOT just the `new_files` or the residuals you bridged.
   A value derived only from the detected files leaves any post-sweep mentor-cron heartbeat
   (which lands ~every 5 min, including during the state write) below `last_ingest_run`
   coverage, and the dispatcher re-fires the same files every cycle. Resync
   `journals_evaluated_count` + `last_eval_file_line` to actual eval-file line counts.
3b. **RE-SWEEP after the state advance** — the Step 3 `json.load`+`write_file` is a separate
   operation; a heartbeat can land between your Step-2 convergence and the Step-3 write.
   Run `scripts/closure_convergence_sweep.py --date <DATE>` again and iterate to 0 additions
   BEFORE asserting. Do NOT declare closure between the state write and this re-sweep — a gap
   slipped in there silently re-fires the next scan. (Confirmed 2026-07-15: advanced state to
   the max mtime of all 117 today journals, re-swept to 0, then asserted `GENUINE GAP = 0`.)
4. **Re-affirm email second-wave state** (`commons/data/ocas-dispatch/<acct>/last_email_check.json`)
   via full-file `write_file`: `last_dispatch = NOW`, `last_dispatch_wave = <prior wave id>`,
   `last_dispatch_note = "re-detection closure; prior wave already triaged; no re-triage, no sends"`.
   Inbox untouched (hard rule 2026-06-24).
5. **Assert closure**: `python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py
   --date <DATE>` → must print `GENUINE GAP (excluding custodian): 0`. Re-run the
   convergence loop if >0.