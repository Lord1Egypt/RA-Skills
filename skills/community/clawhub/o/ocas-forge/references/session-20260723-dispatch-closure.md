# Session 2026-07-23 — Dispatch re-fire closure (post-dispatch-gap)

> **Fast-path (reusable):** If `dispatcher.py` reports `has_work: true` but every thread in `new_threads` is `is_new: false` AND the account's `last_email_check.json` already has `verified_second_wave: True` / `actionable: 0`, it is a second-wave re-fire — do NOT re-triage. Run the email-evidence gate (`verify_evidence_threads.py`) then the closure verification below. Full first-line fast-path guide: `ocas-dispatch/references/refire-fastpath.md`.

**Context:** Autonomous cron run of `dispatcher.py` re-fired a wave that had already
been processed. Dispatcher output: `has_work: true`, 2 dispatches —
`new_emails` (<operator> acct) + `new_journals` (ocas-dispatch journal
`dispatch-wave-20260723T042044Z.json`).

**Key realization:** This is the same recurring re-fire loop, but the "gap" was not
the named wave journal (already in both eval stores) — it was two **post-dispatch
mentor-cron heartbeats** that landed after the wave was written and were absent
from both eval stores, leaving gate [2] (state advance) stale.

## Diagnosis sequence (reproducible)

```bash
cd $HERMES_HOME/../indigo

# 1. Monitor state vs newest journal mtime — re-fire root cause
cat ~/.hermes/commons/data/monitor_state/journal_ingest_state.json
cat $HERMES_HOME/../indigo/commons/data/monitor_state/journal_ingest_state.json
stat -c '%Y %n' commons/journals/ocas-dispatch/2026-07-23/dispatch-wave-20260723T042044Z.json

# 2. Named wave already in both eval stores?
for rel in ocas-dispatch/2026-07-23/dispatch-wave-20260723T042044Z.json; do
  grep -c "$rel" commons/data/ocas-dispatch/journals_evaluated.jsonl
  grep -c "$rel" commons/data/ocas-praxis/journals_evaluated.jsonl
done

# 3. Which today-mentor journals are MISSING from both stores?
for rel in ocas-mentor/2026-07-23/mentor-light-20260723T042059Z.json \
           ocas-mentor/2026-07-23/mentor-light-20260723T042304Z.json \
           ocas-mentor/2026-07-23/mentor-light-20260723T042555Z.json; do
  echo "$rel dispatch=$(grep -c "$rel" commons/data/ocas-dispatch/journals_evaluated.jsonl) \
praxis=$(grep -c "$rel" commons/data/ocas-praxis/journals_evaluated.jsonl)"
done

# 4. Inspect the missing ones — are they noop heartbeats?
for f in ocas-mentor/2026-07-23/mentor-light-20260723T042304Z.json \
         ocas-mentor/2026-07-23/mentor-light-20260723T042555Z.json; do
  echo "== $f =="; python3 -c "import json;o=json.load(open('commons/journals/$f')); \
    print({k:o.get(k) for k in ['run_id','gap_detected','entities_observed','evaluated_count']})"
done
```

**Noop-heartbeat test (generalized 2026-07-23):** A post-dispatch mentor-light is a
safe noop-bridge IFF it carries **NO** `gap_detected` / `evaluated_count` / gap-
evaluation fields. `entities_observed` may be `["ocas-mentor"]` **OR**
`["ocas-dispatch","ocas-mentor"]` (or list other skills) — the presence of other
skills in `entities_observed` does NOT make it genuine. Only a heartbeat that
actually carries `gap_detected: true` or an evaluated-event list is a real gap.

## Closure sequence (verified, reaches `=== gates ALL CLOSED ===`)

```bash
cd $HERMES_HOME/../indigo

# A. MANDATORY email-evidence gate (mixed wave)
python3 skills/ocas-dispatch/scripts/verify_evidence_threads.py \
  --evidence commons/data/ocas-dispatch/evidence.jsonl <thread-id>
# expect: "in_evidence(structured)  action=none"

# B. Bridge the missing noop heartbeats into BOTH eval stores
python3 skills/ocas-forge/scripts/bridge_eval_inline.py \
  ocas-mentor/2026-07-23/mentor-light-20260723T042304Z.json \
  ocas-mentor/2026-07-23/mentor-light-20260723T042555Z.json \
  --action cross_skill_noop_mentor_heartbeat
# (--action is a free-form label, not a magic string)

# C. Iterate convergence sweep to 0 additions
for i in 1 2 3 4 5; do
  python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date 2026-07-23
done

# D. Assert genuine gap = 0
python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date 2026-07-23 \
  | grep -i "GENUINE GAP"

# E. Advance gate state (REQUIRES --date, no default)
python3 skills/ocas-forge/scripts/advance_gate_state.py --date 2026-07-23

# F. Re-run closeout — require literal "=== gates ALL CLOSED ==="
python3 skills/ocas-forge/scripts/closure_closeout_check.py \
  --named ocas-dispatch/2026-07-23/dispatch-wave-20260723T042044Z.json --date 2026-07-23
```

## Email triage (cron autonomous, <operator> acct)

- Thread `<thread-id>` "Re: Roller shade - <operator-last>" (Daniel Ringkamp /
  example-co.test) → `action:none`. Confirmed already `in_evidence(structured) action=none`.
- No draft, no reply, inbox untouched (hard rule 2026-06-24). Not legal/financial/
  urgent → no escalation. Nothing Chronicle-worthy (informational only).

## Outcome
Zero genuine new work, zero drafts, zero escalations, inbox untouched. Wave closed
via post-dispatch-gap closure (noop-bridge of 2 heartbeats, no pipeline re-run).
