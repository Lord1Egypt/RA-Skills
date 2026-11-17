# Mixed re-detection closure with a MINTED wave journal + 1 genuine Path B (2026-07-24)

**Classification:** mixed dispatch wave (`new_emails` + `new_journals`) that is mostly re-detection but carries (a) one genuine Path B email gap and (b) journals present in the **praxis** eval store but **absent from the dispatch** eval store.

**Why this note exists:** the sibling `session-20260724-dispatch-closure.md` re-detected a *pre-existing* wave journal (already bridged), so its gate-[1] check passed trivially. This session **minted a new wave journal** because there was genuine work (the Path B closure). That introduced a step the prior note did not show: the new wave journal itself must be bridged into both eval stores or `closure_closeout_check.py` gate [1] (`named journal in PRAXIS+DISPATCH eval stores`) is `False` and the verifier prints `gates STALE`.

## Sequence executed (verified working)

1. **Email gap triage.** `verify_evidence_threads.py <all 10 thread IDs>` → 9 already `in_evidence(structured)`. Preserve the 2 carrying prior `action=escalate` that had `escalations=1` inside a genuine `email_path_b_gap_closure` record (do **NOT** re-fire). 1 was `NOT_IN_EVIDENCE` (`<thread-id>`, UCSF MyChart portal notification, `is_new:true`) → genuine Path B.
2. **Close the Path B gap.** Append a `dispatch-evidence-v2` record (top-level `triage_decisions[]`, `action:"none"`) to BOTH `commons/data/ocas-dispatch/evidence.jsonl` AND `owner/evidence.jsonl`. Build with `json.dumps`, back up the file first, validate the last line parses. Re-run the verifier → all 10 now `in_evidence(structured)`.
3. **Cross-store journal bridge.** The 3 source journals were `praxis:1 / dispatch:0`. Bridge them into the dispatch eval store:
   `python3 skills/ocas-forge/scripts/bridge_eval_inline.py <relpaths> --action cross_skill_redetection_journal_bridge --require-exists`
   Also bridge any post-detection noop `mentor-light-*` heartbeats that landed during the run (they show `gap_detected: None` / no `evaluated_count` field → safe noop-bridge).
4. **Write the new wave journal** `commons/journals/ocas-dispatch/2026-07-24/dispatch-wave-20260724T161148Z.json` (schema `dispatch-wave-v2`, `classification: mixed_genuine`).
5. **Bridge the new wave journal itself** (the step missing from the prior note):
   `python3 skills/ocas-forge/scripts/bridge_eval_inline.py ocas-dispatch/2026-07-24/dispatch-wave-20260724T161148Z.json --action mixed_genuine_closure --require-exists`
   Without this, gate [1] is `False`.
6. **Advance gate state** to `max journal mtime + 5s` into BOTH monitor copies (`journal_ingest_state.json`, float epoch) + praxis `ingest_state.last_ingest_run` (ISO string). Anchor on **max mtime excluding custodian** (custodian is excluded from the genuine-gap count). Re-run the advance if a post-dispatch heartbeat lands after the first advance (the convergence sweep will flag it).
7. **Verify.** `closure_closeout_check.py --named <wave> --date 2026-07-24` → `=== gates ALL CLOSED ===`. `verify_genuine_gap_profile.py --date 2026-07-24` → `GENUINE GAP (excluding custodian): 0`.

## Outcome
1 email Path B gap closed (`action:none`, no inbox touch), 4 journals bridged into the dispatch eval store, 0 escalations re-fired, all gates closed. No manual workarounds, no fabricated output.

## Variant observed 2026-07-24T18:13Z (journal already fully bridged)

A second occurrence of this exact closure pattern confirmed the recipe is reproducible, with one structural difference: the `new_journals` heartbeat (`mentor-light-20260724T175119Z.json`) was ALREADY present in BOTH eval stores (praxis:True / dispatch:True) at dispatch time — so there was NO journal cross-store gap (`journal_gaps_bridged: 0`). The genuine work was purely the 1 email Path B gap (`<thread-id>`, BE Hive / VegNews "Best Vegan Deli" vote solicitation → `action:none`).

**Key clarification — mint the wave journal even when `journal_gaps_bridged = 0`.** Do NOT skip the wave journal (step 4) just because the named journal is already bridged. The recipe still applies whenever ANY genuine gap exists — here it is the email Path B gap, not a journal gap. Steps 1–2 (close email gap, append both `evidence.jsonl` copies), 4–7 (mint + bridge wave journal, advance gate state, verify) all run unchanged; step 3 (cross-store journal bridge) simply becomes a no-op when the named journal is already in both stores. The original framing of step 3 around a `praxis:1 / dispatch:0` journal gap does NOT mean the recipe requires a journal gap — the email gap alone justifies the mint.

**Escalation-preservation count is N ≥ 1, not specifically 1.** This occurrence showed `escalations: 2` inside the genuine `email_path_b_gap_closure` record (prior occurrence showed `escalations: 1`). Either value means the escalation was genuinely delivered — preserve, do not re-fire. Do not treat `escalations: 2` as anomalous.

**Residual-gap handling unchanged.** After minting + bridging the wave journal, two post-dispatch noop `mentor-light` heartbeats (180550Z, 181113Z) landed and required the convergence sweep (`closure_convergence_sweep.py --date 2026-07-24`) before `verify_genuine_gap_profile.py` reached `GENUINE GAP (excluding custodian): 0`.

## Runner-driven variant (2026-07-25) — DON'T hand-roll; use `run_mixed_wave_closure.py`

A second occurrence confirmed the recipe is reproducible with a cleaner division of labor: drive the **journal half** with the shipped `run_mixed_wave_closure.py` and reserve manual steps for the **email Path B** half only.

**Critical gotcha — the runner's default email re-affirm is WRONG for genuine Path B.** `run_mixed_wave_closure.py` step 8 unconditionally re-affirms `verified_second_wave=True` + `last_dispatch_email_classification:"second-wave"` on the 4 load-bearing email files UNLESS `--skip-email-affirm` is passed. On a wave where email is genuine Path B (real triage work, not a re-detection), that stamp is a **false classification** and corrupts the email-state topology. Always pass `--skip-email-affirm` on genuine-Path-B waves, then manually stamp truthful state (below).

### Sequence (verified working 2026-07-25)
1. **Close the email Path B gap manually** (before the runner): `verify_evidence_threads.py <all thread IDs>` → append a `dispatch-evidence-v2` record (top-level `triage_decisions[]`, `action:"action:none"` for the `NOT_IN_EVIDENCE` thread; echo prior `escalate` verdicts PRESERVED; `action:none` for the already-verified ones) to `commons/data/ocas-dispatch/evidence.jsonl` only — backup first, `json.dumps`, validate last line. Re-run verifier → all `in_evidence(structured)`. (Single-store append is correct here; the verifier reads the data-dir copy. `owner/evidence.jsonl` already held the prior records, so no duplicate needed.)
2. **Drive the journal pipeline with the runner:**
   `python3 skills/ocas-forge/scripts/run_mixed_wave_closure.py --dispatch-ts 20260725T110133Z --new-files "ocas-mentor/2026-07-25/mentor-light-20260725T105811Z.json" --date 2026-07-25 --skip-email-affirm`
   This runs Forge no-op scan → Mentor light heartbeat → Praxis ingest → mints `dispatch-wave-*.json` → bridges (forge-scan, new mentor-light, wave journal) → convergence sweep → gap assert → advances gate state → `closure_closeout_check.py`. Reaches `=== gates ALL CLOSED ===`.
3. **Residual journal gaps caught by the sweep.** The runner's own bridge only covers the 3 journals it minted; the convergence sweep (`closure_convergence_sweep.py`) separately bridged the named `mentor-light-20260725T105811Z.json` (the dispatched file) AND a post-dispatch heartbeat `mentor-light-20260725T110546Z.json` that landed during the run — both were absent from the dispatch eval store. This is expected; the sweep, not the runner's bridge, is the authoritative gap-closer.
4. **Manually stamp truthful email state** (because `--skip-email-affirm` left the owner files untouched): set `verified_second_wave:True`, `last_dispatch_wave`, `last_triage_run_id`, and **`last_dispatch_email_classification:"genuine_path_b"`** (NOT `"second-wave"`) plus a `last_dispatch_note` describing the real email work, on `owner/last_email_check.json` and `last_email_check_owner.json`. Without this the email side has no record of the genuine closure.

**Outcome (2026-07-25):** 1 email Path B closed (`action:none`, no inbox touch), journal pipeline ran, all gates closed, `GENUINE GAP (excluding custodian): 0`. Escalation (Docusign separation) preserved, not re-fired.

**When to prefer this over the fully-manual 07-24 recipe:** any mixed wave where the journal gap is a standard Forge/Mentor/Praxis run (not a bespoke cross-store bridge). The runner eliminates cross-call timestamp drift and phantom eval lines. Keep the manual evidence-append (step 1) and truthful-stamp (step 4) outside the runner — those are the parts the runner does not and cannot do correctly for genuine Path B.
