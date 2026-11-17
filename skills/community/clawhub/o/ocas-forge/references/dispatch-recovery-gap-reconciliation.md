# Dispatch Recovery Gap Reconciliation

**Confirmed:** 2026-07-14T07:58Z recovery of `dispatch-wave-20260714T073950Z.json`.

## Problem

During a prior-wave-misclassification recovery, you run the genuine 3-pipeline
(Forge no-op scan -> real Mentor heartbeat -> real Praxis ingest). The ocas-praxis
post-ingest checklist MANDATES `gap_backfill.py` to catch gaps. But:

- `gap_backfill.py` is **mtime-based**: it only finds journals with
  `mtime > last_ingest_run`.
- Journal files carry mtimes ~7h12m BEHIND their content timestamps
  (ocas-mentor gotcha #100). The just-run ingest's outputs
  (`mentor-light-*`, `forge-scan-*`) have file-mtimes far behind their content
  timestamps and behind the freshly-advanced `last_ingest_run`.
- So `gap_backfill.py` prints `Found 0 unevaluated journals (mtime > last_ingest_run)`
  **even though** those outputs are MISSING from the **DISPATCH eval store** --
  the real Praxis ingest writes only to the praxis-eval store
  (`commons/data/ocas-praxis/journals_evaluated.jsonl`), never to the dispatch
  eval store (`commons/data/ocas-dispatch/journals_evaluated.jsonl`).
- The next dispatcher scan re-detects those missing dispatch-eval files -> re-fires.

**A `0` from gap_backfill during recovery is a false all-clear. Do not trust it.**

## Correct procedure

After the genuine ingest (and after `gap_backfill.py` if you ran it), run a full
**two-store on-disk reconciliation** instead of relying on gap_backfill's mtime
scan:

1. Glob `commons/journals/ocas-*/YYYY-MM-DD/*.json` (profile-scoped:
   `<hermes-home>/profiles/indigo/commons/journals/`).
2. Skip `dispatch-wave-*` meta-journals (they are bridged separately).
3. For every on-disk file, require membership in BOTH stores:
   - praxis-eval store, key `journal_id` = `ocas-<skill>/<DATE>/<file>.json`
   - dispatch-eval store, key `filename` = **same** full relative path
4. Any file missing from either store is a genuine gap -> bridge it into BOTH
   via `scripts/bridge_eval_both_stores.py --action cross_skill_mitigation <relpath> ...`.
5. Verify GENUINE GAP = 0: re-glob and confirm every file is in both stores.

## Gotcha: the KEY-SHAPE pitfall

The eval stores key on the **full relative path** (`ocas-mentor/2026-07-14/mentor-light-XXXX.json`),
NOT the basename. The idempotency guard MUST compare the full relative path.
Comparing `os.path.basename()` against full-path `filename` values always yields
"missing" and re-adds duplicates (this run silently accumulated 1,384 duplicate
lines across re-dispatch cycles historically). Build membership sets from the
full relative value and dedupe on it.

## Verified reconciliation script pattern

Write to `/tmp/reconcile.py` (NOT inline heredoc with `| python3` -- pipe-to-interpreter
is blocked in cron mode). Anchor on `.../commons/journals/`, not `.../commons/`.
Use `read_retry` (reject <1000-line transient truncations) when loading the eval
files. For each store, load the keyed set; compute the on-disk set; bridge the
symmetric difference into BOTH stores with `--action cross_skill_mitigation`.
Print final GENUINE GAP count before exiting.

In the 2026-07-14 run this caught **9** genuine dispatch-eval residuals
(3 `mentor-light` outputs + 1 `forge-scan` + 5 `ocas-custodian` outputs) that
`gap_backfill.py` had reported as 0. After bridging, GENUINE GAP = 0 and the
dispatcher did not re-fire.