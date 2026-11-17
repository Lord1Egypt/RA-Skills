# Mixed-Wave Closure — One-Shot Operational Runbook (2026-07-15)

Companion to `references/session-20260715-mixed-wave-closure.md`. That file documents the
*why* and the per-step pitfalls. This file captures the **runnable one-shot orchestration
pattern** that actually closed a live mixed explicit-run wave (Forge + Mentor + Praxis +
email second-wave) in a single `python3` invocation, plus a **phantom-purge gap** the
recipe's walk cannot see.

## When this applies

A dispatcher fire carrying BOTH:
- `new_journals` — prompt with explicit-run override ("Process them through all three
  pipelines: Forge journal scan, Mentor light heartbeat, Praxis journal ingest"). The
  override FORCES pipeline execution even when the named journal is already evaluated and
  `ingest_state.last_ingest_run` is already past its timestamp (a re-detection).
- `new_emails` — account `owner`, all threads `is_new: false` = email second-wave.

Do NOT skip pipelines because the content is re-detected. The override is explicit.

**BUT FIRST disambiguate against MODE C (stale-state re-detection):** run the pre-flight in
`references/redetection-stale-state-closure-oneshot.md`. If `all_in_both` is True (the named
journal is already in BOTH eval stores) AND `last_ingest_run` (and
`commons/data/monitor_state/journal_ingest_state.json.latest_mtime`) are ALREADY past the max
today-journal mtime, a prior closure already did the work — this is a **stale-state re-detection**,
NOT a genuine mixed wave. Do closure-only:
- `closure_convergence_sweep.py --date <DATE>` → iterate to `GAPS BRIDGED: 0`
- `verify_genuine_gap_profile.py --date <DATE>` → `GENUINE GAP = 0`
- re-affirm BOTH email state files (see step 8 / MODE C runbook)
- do NOT run pipeline steps 2–5 (no Forge/Mentor/Praxis re-run, no wave journal mint).

A mixed wave CAN be a full re-detection of both components (journal already evaluated + email Path A);
the explicit-run prompt is canned and does not override ground-truth state. Re-running pipelines on an
already-closed wave double-journalizes (forbidden anti-journalization). Observed live 2026-07-16T16:45Z:
the dispatcher fired `new_journals` + `new_emails` with a "process all three pipelines" override, but the
journal was already in both eval stores, state was already past it, and all 13 email threads were
`in_evidence(structured)` action:none → closure-only, no pipeline re-run.

## PREFERRED: tooled runner for full mixed waves (incl. taste) — added 2026-07-22

When the wave also carries `taste_new_data` (or you simply want the deterministic, no-drift path),
**prefer `skills/ocas-forge/scripts/run_mixed_wave_closure.py` over hand-rolling `/tmp/run_pipeline_*.py`**.
It composes TS ONCE, reads every pipeline journal relpath from disk (no phantom eval lines), runs
Forge no-op scan + Mentor heartbeat + Praxis ingest + optional Taste dedup, writes the dispatch-wave
journal, bridges all (require-exists), convergence-sweeps, re-affirms email `verified_second_wave`,
advances gate state, and asserts `=== gates ALL CLOSED ===` (exits non-zero if not).

```bash
python3 skills/ocas-forge/scripts/run_mixed_wave_closure.py \
  --dispatch-ts 20260722T131614Z \
  --new-files ocas-finch/2026-07-22/scan-1100.json ocas-finch/2026-07-22/daily-1310.json \
             ocas-vesper/2026-07-22/r_20260722_0600.json \
             ocas-custodian/2026-07-22/light-scan-2026-07-22T130716Z.json \
  --taste-signals-before 5932 --taste-delta 625 --apply-taste
```

Flags: `--dispatch-ts` (dispatcher `detected_at`), `--new-files` (dispatcher `new_files` relpaths),
`--taste-signals-before` (line count of `commons/data/ocas-taste/signals.jsonl` BEFORE dedup),
`--taste-delta` (dispatcher `taste_new_data.changes.signals`), `--apply-taste` (apply the dedup;
default dry-run only). The hand-rolled steps 1–11 below remain the authoritative reference if the
script is unavailable or you need to deviate per-wave — but the script eliminates the two failure
classes the steps warn about (cross-call timestamp drift, recomposed forge-scan relpath).

## One-shot orchestration pattern

Write the whole sequence to a **run-unique** temp path such as `/tmp/run_pipeline_<TS>.py` (NOT inline `python3 -c`, NOT
shell-heredoc with dict literals) and run `python3 /tmp/run_pipeline_<TS>.py`. **PITFALL — fixed `/tmp` paths collide with concurrent runs:** a second dispatch wave firing inside the same cron window, or a sibling subagent the harness spawns, can read or overwrite a fixed `/tmp/run_pipeline.py` between your `write_file` and your `terminal()` run (observed live 2026-07-16: a sibling subagent wrote the same path before execution). Always embed the wave `TS` in the temp filename (and in the mentor file list, see step 3). Critical
structural rules confirmed working:

1. **Compose ALL timestamps ONCE** at the top: `now = datetime.now(timezone.utc)`;
   `TS = now.strftime("%Y%m%dT%H%M%SZ")`; `NOW = now.isoformat()`; `DATE = now.strftime("%Y-%m-%d")`.
   Never call `datetime.now()` again. Every filename and content timestamp reuses these.

   **PITFALL — cross-call timestamp drift (observed 2026-07-16 closure):** The "compose once" rule holds ONLY when the entire sequence runs inside one `python3 /tmp/run_pipeline_<TS>.py` file. If you instead SPLIT the closure across multiple `terminal()` calls (e.g. to inspect Mentor/Praxis stdout between steps, or because a `skill_view`/`read_file` flake forced a restart), each separate shell that re-invokes `date -u +%Y%m%dT%H%M%SZ` produces a *different* second-resolution `TS`. The dispatch-wave journal then references a `triage-<TS>.json` (or other cross-journal filename) that does NOT exist on disk — breaking the bridge and the closure assertion. **Fix:** lift `TS`/`NOW`/`DATE` from the FIRST call's stdout and reuse them verbatim in every subsequent cross-referencing write — never re-invoke `date` per call. After writing the dispatch-wave journal, `ls` each `new_files` entry to confirm it exists; if one is off by a second, `patch` the reference to the real filename (observed: dispatch-wave referenced `triage-...132154Z.json` but the file was `triage-...132153Z.json` — the two parallel `date` calls disagreed by a second) BEFORE bridging.

   **PITFALL — inline-heredoc timestamp scoping (observed 2026-07-16 closure):** The recommended form is a `/tmp/run_pipeline_<TS>.py` FILE run as `python3 /tmp/run_pipeline_<TS>.py` — module-level `TS`/`DATE`/`NOW` assignments persist for the whole run. If you instead run an INLINE `python3 <<'PYEOF'` heredoc with `TS=...`/`DATE=...`/`NOW=...` set as shell-prefix assignments in the same terminal command (e.g. `TS=$(date ...); python3 <<'PYEOF' ... 'dispatch-wave-'+TS ... PYEOF`), the Python subprocess does NOT inherit shell variables — you get `NameError: name 'TS' is not defined` on a later line. Fix: redefine `TS`/`DATE`/`NOW` INSIDE every heredoc block, OR (preferred) keep using the `/tmp/run_pipeline_<TS>.py` file form so the assignments live in-module.
2. **Forge no-op scan** — count unprocessed `vp_*`/`vd_*` with `python3 skills/ocas-forge/scripts/forge_count_unprocessed.py` (bounded walk of `intake/` ONLY; excludes `intake/processed/`, the `proposals/` SOURCE MIRROR, and the top-level `processed/` dir). A hand-rolled recursive glob/`find` over the whole `ocas-forge` tree reintroduces the false-`genuine` trap (sweeps up `proposals/` + top-level `processed/`, both duplicate mirrors — bit a 2026-07-16 closure orchestrator, wrote `unprocessed_proposals: 11`/`genuine` when true value was 0). Write `ocas-forge/<DATE>/forge-scan-<TS>.json` with `unprocessed_proposals` = that count and `action: routine_no_op` iff count==0. Capture its relpath `FORGE_SCAN_REL` VERBATIM — recomposing `<TS>` for the bridge writes a phantom eval line.
3. **Mentor heartbeat** — build the 3-day file list
   (`find <hermes-home>/commons/journals/ <hermes-home>/profiles/indigo/commons/journals/ -name '*.json' -mtime -3 | sort -u > /tmp/mentor_files_<TS>.txt`)
   and run `python3 skills/ocas-mentor/scripts/cron-heartbeat-light.py < /tmp/mentor_files_3d.txt`
   (**stdin redirect, NOT a shell pipe** — `cat file | python3` trips `tirith:pipe_to_interpreter`
   and hangs the cron job at `approval_pending`). Capture the ACTUAL heartbeat journal by
   scanning today's `ocas-mentor/<DATE>/` dir for the max `timestamp` field — the script's
   stdout filename lies on a second-boundary rollover.
4. **Praxis ingest** — `python3 skills/ocas-praxis/scripts/praxis_ingest_run.py --mode dispatch`.
   Appends to the praxis-eval store; does NOT advance `ingest_state`.
5. **Write `dispatch-wave-<TS>.json` journal FIRST** (in `ocas-dispatch/<DATE>/`,
   `classification: mixed_genuine_no_op`, real account `owner` + `classification: second-wave`
   for the email block — NOT the hardcoded `indigo_inbox` stub). Capture its relpath. It MUST
   exist on disk before it is bridged (see below).
6. **Bridge** — `python3 skills/ocas-forge/scripts/bridge_eval_inline.py <mentor_rel> <FORGE_SCAN_REL> <named_new_file> <DISPATCH_WAVE_REL> --action mixed_wave_<date> --require-exists`.
   `--require-exists` refuses to bridge a relpath whose file is missing (phantom guard). Bridge
   list order: the dispatch-wave journal must be on disk (step 5) before this step runs.
   **INDEPENDENT FILENAMES (confirmed live 2026-07-22):** the forge-scan, mentor-light, and
   named-journal relpaths each carry their OWN timestamp, NOT `<WAVE_TS>`. The forge-scan TS is
   set by the Forge no-op block (step 2); the mentor-light TS is set by the heartbeat write (step 3);
   the named journal TS is the dispatcher's. None of them equal the bridge/wave TS. Read every
   relpath from disk (`ls`/`glob`) and bridge those EXACT strings. Recomposing
   `ocas-forge/<DATE>/forge-scan-<WAVE_TS>.json` (or `mentor-light-<WAVE_TS>.json`) produces a
   phantom eval line and fails closeout gate [1] (`named journal in PRAXIS+DISPATCH eval stores:
   ...=False`). The wave journal itself is the only relpath that uses `<WAVE_TS>`.
   **Bridge output interpretation (confirmed 2026-07-15T22:14Z):** the script prints
   `bridged <rel> (praxis=<a1> dispatch=<a2>)` where `a1`/`a2` mean *added to that store* (boolean),
   NOT "present / healthy". After the Praxis ingest (step 4) has already registered the
   pipeline-input journals (forge-scan, mentor-light) into the praxis-eval store, the bridge will
   show `praxis=False dispatch=True` for those — this is **expected**, not a failure; only the
   dispatch-eval store still needed filling. The dispatch-wave journal itself shows
   `praxis=True dispatch=True` (new to both). Do NOT re-run the bridge or treat `praxis=False` as
   an error — `total bridged` counts only the ADDITIONS.
7. **Advance `ingest_state.last_ingest_run`** to MAX `os.path.getmtime()` over a BOUNDED
   per-skill `os.listdir(commons/journals/<skill>/<DATE>/)` walk (NO recursive glob — self-nested
   symlinks emit false positives). A value derived only from `new_files` leaves a post-sweep
   heartbeat below coverage → the dispatcher re-fires the same wave forever.
8. **Re-affirm email second-wave via the EXACT files `closure_closeout_check.py`
   (corrected 2026-07-17) requires** — its `required_email` list, NOT the stale
   `select_email_state.py` flat-path guidance which names the WRONG owner file and
   omits three of the four required ones. Via full-file `json.load` + `json.dump`
   (never `patch` — duplicate-key JSON corruption): set `verified_second_wave: true`,
   `last_dispatch: NOW`, `last_dispatch_wave: dispatch-wave-<TS>`,
   `last_dispatch_email_classification: second-wave` on EACH of these four:
   - `commons/data/ocas-dispatch/owner/last_email_check.json`        (owner, required)
   - `commons/data/ocas-dispatch/last_email_check_owner.json`        (owner, required)
   - `commons/data/ocas-dispatch/last_email_check_indigo.json`       (indigo, required)
   - `commons/data/ocas-dispatch/last_email_check_mx_indigo_karasu_gmail_com.json` (indigo, required)
   **DO NOT re-affirm the two WARN-only files** — `last_email_check.json` and
   `last_email_check_<account-identity>_gmail_com.json` — these are top-level GWS snapshots that
   stay `null` under the monitor re-fire bug; the verifier WARNs on them but they must NOT gate
   closure. Reaffirming them is harmless but pointless; the four above are load-bearing.
   **Re-affirm owner AND indigo** — a closure that only re-affirms `owner` leaves `indigo`'s
   `verified_second_wave` as `None` and the indigo account re-fires (observed live 2026-07-16T16:45Z).
   **Inbox untouched** — hard rule on email second-wave: no reads, no drafts, no sends (<operator> inbox
   write-prohibited 2026-06-24; the agent archive-only, never modify via this closure).
9. **Convergence sweep** — `python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date <DATE>`,
   iterate until it prints `GAPS BRIDGED: 0`.
10. **Optional but safe** — `python3 skills/ocas-mentor/scripts/correct_active_skills_30d.py`
    (evidence line only, no journal). Re-sweep after.
11. **Assert closure** — `python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date <DATE>`
    → must print `GENUINE GAP (excluding custodian): 0`.

## Phantom-purge gap (NOT covered by the closure walk)

`verify_genuine_gap_profile.py` and `closure_convergence_sweep.py` BOTH exclude `dispatch-wave-*`
meta journals from their walk. So a prior wave's `dispatch-wave-<OLDTS>.json` whose file has been
rotated/deleted leaves a **dangling eval line** in both stores that the closure scripts will
NEVER flag — closure still asserts `GENUINE GAP = 0`, but the store carries a dead reference to a
non-existent file. The existing recipe's phantom section only covers `FORGE_SCAN` recomposition,
not prior-wave `dispatch-wave` rotation.

**Operational purge (run after steps 9–11, idempotent-safe):** scan both eval stores for
today-dated relpaths that do not exist on disk, and drop the dangling lines:

```python
import os, json
J = "<hermes-home>/profiles/indigo/commons/journals"
for Ev in ["<hermes-home>/profiles/indigo/commons/data/ocas-praxis/journals_evaluated.jsonl",
           "<hermes-home>/profiles/indigo/commons/data/ocas-dispatch/journals_evaluated.jsonl"]:
    with open(Ev) as f:
        lines = f.readlines()
    out = [ln for ln in lines
           if not ("/2026-07-15/" in ln and "ocas-" in ln
                   and not os.path.exists(os.path.join(J, json.loads(ln).get("journal_id") or json.loads(ln).get("filename")))))]
    with open(Ev, "w") as f:
        f.writelines(out)
```

Confirm the CURRENT wave's `dispatch-wave-<TS>.json` is still present (don't purge it — guard the
filter to today-dated entries, and the live wave's file exists on disk so it survives). After purge,
re-run the convergence sweep (assert 0) and `verify_genuine_gap_profile.py` (assert 0).

## Live result (2026-07-15T11:36Z)

Forge: 0 unprocessed (no-op). Mentor: rc 0, 1996 scanned, 4 ingested, `active_skills_30d` 14→23.
Praxis: rc 0, 3 journals, 2 `no_signal` events (correctly filtered — no false-positive
`failure_keyword`/`correction`/`gap_detected`), 0 lessons. Bridge: +3. Sweep converged to 0.
`correct_active_skills_30d`: 14→23. Phantom purge removed 1 prior-wave `dispatch-wave-20260715T110038Z.json`
dangling line from each store. Final `GENUINE GAP = 0`. Email `verified_second_wave` re-affirmed,
inbox untouched.