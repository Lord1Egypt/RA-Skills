# Re-detection verify-and-bridge SOP (concrete command sequence)

Companion to `session-20260725-emailplusjournal-redetection-nomint.md`. That file
describes the high-level pattern; this one gives the EXACT verification commands
used on the 2026-07-25 combined email+journal re-detection and two nuances that are
easy to get wrong. Use this when a dispatcher fire carries BOTH `new_emails` AND
`new_journals` and you suspect it is a re-detection of an already-closed wave.

**Hard rule: do NOT call `run_mixed_wave_closure.py`** — it mints a dispatch-wave
journal and re-fires the dispatcher. For a pure no-mint re-detection, close by
bridging residual gaps + advancing gate state only.

## Step 1 — Email gate (prove triage already happened)

Raw grep counts of a thread ID in `evidence.jsonl` are NOT proof of triage. A thread
can appear 100+ times from stale/unstructured lines while still lacking a real
`action=` decision. ALWAYS use the verifier:

```bash
cd $HERMES_HOME/../indigo
python3 skills/ocas-dispatch/scripts/verify_evidence_threads.py \
  --evidence commons/data/ocas-dispatch/evidence.jsonl \
  <thread_id_1> <thread_id_2> ...
```

PASS criterion: every thread prints `in_evidence(structured)  action=<token>`
(e.g. `action=escalate`, `action=none`). Any thread printing `NOT_IN_EVIDENCE` or
`in_evidence(structured)` with NO `action=` token = genuine Path B gap → triage it
first. On 2026-07-25 all four <operator> threads passed (Docusign → escalate, the other
three → none).

Also confirm dispatch-owned `verified_second_wave` flags (NOT the two top-level
GWS-snapshot files, which stay `null` under the monitor re-fire bug):
```bash
for f in owner/last_email_check.json last_email_check_owner.json last_email_check_indigo.json; do
  python3 -c "import json; print('$f', json.load(open('commons/data/ocas-dispatch/$f')).get('verified_second_wave'))"
done
```

## Step 2 — Journal gate (prove pipelines already ran)

For each `details.new_files` journal, grep BOTH eval stores by BARE relpath (no
`commons/journals/` prefix):
```bash
J=ocas-mentor/2026-07-25/mentor-light-20260725T183032Z.json
grep -c "$J" commons/data/ocas-praxis/journals_evaluated.jsonl
grep -c "$J" commons/data/ocas-dispatch/journals_evaluated.jsonl
```
If present in both → the named journal is a re-detection. Do NOT re-run Forge /
Mentor / Praxis.

## Step 3 — Discover orphaned gaps (the subtle one)

The monitor `latest_mtime` can be set to the mtime of a journal that was NEVER
bridged — a prior closure advanced the gate to "cover" a genuine-gap journal without
actually bridging it. So a "looks advanced" gate can still hide unbridged journals.

Find any today-journal whose mtime is at/above the gate state but absent from both
stores:
```bash
JDIR=commons/journals/ocas-mentor/2026-07-25
for p in "$JDIR"/*.json; do
  b=$(basename "$p"); REL="ocas-mentor/2026-07-25/$b"
  d=$(grep -c "$REL" commons/data/ocas-praxis/journals_evaluated.jsonl)
  e=$(grep -c "$REL" commons/data/ocas-dispatch/journals_evaluated.jsonl)
  [ "$d" = "0" ] || [ "$e" = "0" ] && echo "UNBRIDGED: $REL"
done
```
These are genuine gaps even though the gate timestamp looks fine. On 2026-07-25 this
surfaced `mentor-light-20260725T183753Z.json` and `...T184032Z.json`.

## Step 4 — Bridge noop heartbeats

For any unbridged `mentor-light-*` journal carrying `gap_detected: false` and NO
gap-evaluation fields (a pure heartbeat), bridge as a noop — do NOT re-run pipelines:
```bash
python3 skills/ocas-forge/scripts/bridge_eval_inline.py \
  ocas-mentor/2026-07-25/mentor-light-20260725T183753Z.json \
  ocas-mentor/2026-07-25/mentor-light-20260725T184032Z.json \
  --action cross_skill_noop_mentor_heartbeat --require-exists
```
`--require-exists` skips relpaths whose file is missing on disk (prevents phantom
eval entries). The `--action` value is a free-form label, not a magic string.

## Step 5 — Close (sweep → verify → advance → re-verify)

```bash
python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date 2026-07-25
python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date 2026-07-25
# require: GENUINE GAP (excluding custodian): 0
python3 skills/ocas-forge/scripts/advance_gate_state.py --date 2026-07-25
# re-sweep + re-verify (a tail journal can land during the advance)
python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date 2026-07-25
python3 skills/ocas-forge/scripts/closure_closeout_check.py \
  --named ocas-mentor/2026-07-25/mentor-light-20260725T183032Z.json --date 2026-07-25
# require: === gates ALL CLOSED ===
```
`advance_gate_state.py` recomputes max mtime programmatically (+5s pad) — never
hand-type the literal (truncation re-fires the wave forever).

## Real case 2026-07-25 (summary)

- Named journal `183032Z` already in both eval stores → re-detection.
- Email gate PASSED (verify_evidence_threads: escalate + 3×none).
- Found `183753Z` + `184032Z` noop heartbeats absent from stores → bridged both.
- Gate [2] stale because `184032Z` (mtime 1785004835) arrived after the prior
  advance (which had only padded past `183753Z`). `advance_gate_state --date` covered
  it. Final closeout: `=== gates ALL CLOSED ===`.
- No dispatch-wave journal minted. Email threads required no <operator> input.
