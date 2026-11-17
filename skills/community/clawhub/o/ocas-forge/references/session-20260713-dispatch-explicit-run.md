# Session 2026-07-13 — Explicit-Run Multi-Skill Dispatch (Caller-Side Bridge)

Verified end-to-end procedure for a dispatcher `new_journals` fire that carries an
**explicit run instruction** (e.g. "run Forge journal scan / run Mentor light heartbeat /
run Praxis journal ingest"). Per the 2026-07-11 / 07-13 override rule, the explicit
instruction takes precedence over the no-op shortcut: all three pipelines MUST run, and the
caller bridges outputs into BOTH eval files. The `run_dispatch_pipeline.py` script is
insufficient here — it bridges the praxis eval only and writes a redundant `mentor-light`
no-op instead of running the real heartbeat.

## Pre-flight classification (do BEFORE writing any journal)
- A dispatcher `new_file` may be a `dispatch-wave-*.json` **prior-wave artifact** — detect
  by comparing its content `timestamp` to the dispatch `detected_at`. If content ts <
  detected_at → skip entirely (do not grep, do not register). The mtime can be newer
  (touched on write) while the content timestamp is older — use content, not mtime.
- Grep each genuine `new_file` against BOTH eval files. Confirmed field shapes: praxis eval
  keys on `journal_id`; dispatch eval keys on `filename`.
- Emails: if ALL threads `is_new:false` → email second-wave → no triage, no sends (hard rule).

## Step 1 — Forge scan (no-op)
- Scan `commons/data/ocas-forge/intake/` and `intake/processed/` for `vp_*.json` / `vd_*.json`.
  The `proposals/` dir is a SOURCE MIRROR — do NOT count it (it overcounts; correct value is
  0 when all are already in `intake/processed/`).
- If 0 unprocessed → write a `forge-scan-{TS}.json` no-op journal via `write_file` (atomic;
  avoids heredoc/pipe pitfalls). Path: `commons/journals/ocas-forge/YYYY-MM-DD/forge-scan-{TS}.json`.

## Step 2 — Mentor light heartbeat (real run)
- Build a feed of today/yesterday journal paths:
  `find commons/journals -name "*.json" \( -path "*YYYY-MM-DD*" -o -path "*YYYY-MM-DD-1*" \) | grep -v dispatch-wave | sort -u > /tmp/mentor_feed.txt`.
  Do NOT pipe `find` into `python3` (tirith:pipe_to_interpreter blocks it in cron).
- Run: `python3 skills/ocas-mentor/scripts/cron-heartbeat-light.py < /tmp/mentor_feed.txt`
  (subprocess stdin — never `cat file | python3`).
- The script writes its OWN journal `commons/journals/ocas-mentor/YYYY-MM-DD/mentor-light-{run_id}.json`.
  Capture its actual filename by content-timestamp scan (max `timestamp` field), NOT `ls -t`
  (mtimes lag content ~7h12m in this environment).
- ANTI-JOURNALIZATION: do NOT write a second mentor-light journal yourself.

## Step 3 — Praxis journal ingest (real run)
- Must run from the script dir so `from praxis_common import ...` resolves:
  `cd skills/ocas-praxis/scripts && python3 praxis_ingest_run.py`.
- Scans today/yesterday journals not in praxis eval; routine healthy mentor-light heartbeats
  are filtered to `no_signal`. It auto-registers what it processes into the PRAXIS eval only
  (not the dispatch eval, not the state file).

## Step 4 — Bridge to BOTH eval files (caller-side, idempotent)
- Collect the set: all pipeline output journals (forge-scan, the heartbeat's mentor-light,
  praxis-dispatch) + every genuine `new_file` gap the pipelines processed.
- Append to praxis eval with field `journal_id`; append to dispatch eval with field `filename`.
  Idempotent: skip if already present (grep -qF by basename).
- **Phantom guard:** after appending, assert `os.path.exists(commons/journals/<relpath>)` for
  every newly-added entry. A phantom entry (pointing at a non-existent file) is worse than a miss.
- **CONFIRMED: neither `praxis_ingest_run.py` nor `cron-heartbeat-light.py` writes
  `ingest_state.json`.** The caller must advance `last_ingest_run` past the max mtime of all
  processed journals, and resync `journals_evaluated_count` / `last_eval_file_line` to the
  real eval-file line counts.

## Step 5 — Dispatch-wave meta-journal
- Write `commons/journals/ocas-dispatch/YYYY-MM-DD/dispatch-wave-{TS}.json` via `write_file`.
  `classification` e.g. `full_pipeline_with_second_wave_emails`. Do NOT register it in the
  praxis eval as a behavioral event (filter `no_op` outcomes as `no_signal`); it needs only
  lightweight dispatch-eval tracking if missing.

## Step 6 — Verification + post-dispatch cleanup
- Grep each bridged journal in BOTH eval files (expect 1:1).
- `os.walk` commons/journals for any `.json` with mtime >= `last_ingest_run` NOT in praxis
  eval (exclude `dispatch-wave-*` and bare `.json`); append any found with source
  `post-dispatch-cleanup`.
- Report counts, phantoms (must be 0), and final `last_ingest_run`.

## This session's result (sanity baseline)
- Forge: 0 unprocessed proposals → no-op. Mentor: 61 new files ingested, own journal
  `mentor-light-20260713T125530Z`. Praxis: 4 routine `no_signal` journals. One genuine gap
  (`mentor-light-20260713T124005Z`) bridged. `last_ingest_run` advanced to 2026-07-13T12:55:55Z.
  All 6 bridged journals present in both eval files; 0 phantoms; post-dispatch cleanup 0 gaps.

## Second explicit-run wave (16:47Z) — confirmation + bidirectional one-sided gap
A second dispatcher `new_journals` + `new_emails` fire at 2026-07-13T16:50Z executed the full
pipeline again (Forge no-op: 0 proposals; Mentor: 13 ingested, 0 errors; Praxis: 6 journals / 5
events, 1 medium custodian execution-failure + 4 no_signal). Two genuine one-sided eval gaps closed
in the bridge step — proving the gap can straddle BOTH orientations simultaneously:
- `ocas-custodian/2026-07-13/esc-loop-20260713T164733Z.json` — present in PRAXIS eval (event_recorded by ingest), MISSING from dispatch eval → added to dispatch eval.
- `ocas-mentor/2026-07-13/mentor-light-20260713T164718Z.json` — present in DISPATCH eval (bridged 16:54), MISSING from praxis eval → added to praxis eval.
Takeaway: a genuine (non-re-detection) dispatch can leave the two detected `new_files` split across
the two eval files in OPPOSITE directions. The bridge Step 4 (per-file, both-eval idempotent append)
handles this; the EXCEPTION re-detection shortcut's one-sided-gap list must also enumerate the
dispatch-only orientation (see SKILL.md EXCEPTION bullet). Emails: both accounts' threads were
`is_new:false` → email second-wave → no triage, no sends (hard rule confirmed). 22 pre-existing
phantom entries remain in praxis eval; left untouched per the unscoped-cleanup warning.
Final: `last_ingest_run` advanced to 2026-07-13T17:00:19Z; all bridged journals 1:1 in both eval
files; 0 phantoms from this run.

## 2026-07-14 — `bridge_explicit_run.py` does NOT close post-dispatch cron gaps
The canonical `bridge_explicit_run.py` presents `DONE` as if the wave is closed, but it only
bridges its own produced outputs (forge-scan, the heartbeat journal it runs, dispatch-wave) plus
the dispatcher's `new_files`. It does NOT perform the mandatory final gap walk (cron-gap pattern
#155 / #7 — journals written by sibling cron pipelines inside the wave window that aren't in its
`bridge` list). In a 2026-07-14 explicit-run wave, a cron `mentor-light-20260714T064522Z.json`
(06:45:22Z, predating the script's own heartbeat at 06:48:43Z) was left UNBRIDGED and only surfaced
as a genuine gap when `close_gap_profile.py --date 2026-07-14` was run separately. It had to be
manually bridged: `python3 skills/ocas-dispatch/scripts/bridge_eval_both_stores.py --action
post_dispatch_cleanup ocas-mentor/2026-07-14/mentor-light-20260714T064522Z.json`.

**Operational rule:** After `bridge_explicit_run.py` returns `DONE`, ALWAYS run
`python3 skills/ocas-dispatch/scripts/close_gap_profile.py --date <DATE>` and, for any genuine
(non-custodian) gap reported, bridge it with `bridge_eval_both_stores.py --action post_dispatch_cleanup <rel_path>`.
Do not treat `DONE` as closure — verify GENUINE GAP = 0 before exiting the wave. (The 4 typical
remaining gaps are `ocas-custodian/*`, self-bridged by their own cron, excluded by design.)