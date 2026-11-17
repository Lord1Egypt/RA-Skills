# Re-Detection Stale-State Closure — One-Shot Runbook (MODE C)

When a dispatcher fire re-enqueues a `new_journals` item whose journal is ALREADY present in BOTH
eval stores, but `ingest_state.last_ingest_run` is BEHIND the journal's mtime, the monitor keeps
re-firing the same wave forever. This is the **stale-state loop** (MODE C). Re-running
Forge/Mentor/Praxis double-writes journals (anti-journalization gate violation). Response: **closure-only**.

Confirmed live occurrences: 2026-07-14T14:59Z, 2026-07-15T21:20Z, 2026-07-16T03:40Z, 2026-07-16T04:35Z (the 04:35Z case is the `lir == nf_mtime` sub-case — named journal `mentor-light-20260716T043113Z.json` fully bridged at exactly `last_ingest_run` 04:31:13, re-fired by later heartbeats at 04:35:57 / 04:42:03).

## Pre-flight (read-only, date-agnostic)

```python
python3 << 'PYEOF'
import os, json, datetime
PROFILE="<hermes-home>/profiles/indigo"
JDIR=f"{PROFILE}/commons/journals"
PRAXIS_EV=f"{PROFILE}/commons/data/ocas-praxis/journals_evaluated.jsonl"
DISPATCH_EV=f"{PROFILE}/commons/data/ocas-dispatch/journals_evaluated.jsonl"
STATE=f"{PROFILE}/commons/data/ocas-praxis/ingest_state.json"
# new_files from dispatcher.py output (relative to commons/journals/)
new_files=["ocas-mentor/2026-07-16/mentor-light-20260716T033554Z.json"]
def in_store(p, rel):
    if not os.path.exists(p): return False
    with open(p) as f: return any(rel in ln for ln in f)
all_in_both = all(in_store(PRAXIS_EV, r) and in_store(DISPATCH_EV, r) for r in new_files)
st = json.load(open(STATE))          # NEVER read_file — stale-cache pitfall
lir = st.get("last_ingest_run")
mts = [os.path.getmtime(f"{JDIR}/{r}") for r in new_files if os.path.exists(f"{JDIR}/{r}")]
nf_dt = datetime.datetime.fromtimestamp(max(mts), tz=datetime.timezone.utc) if mts else None
lir_dt = datetime.datetime.fromisoformat(lir.replace("Z", "+00:00")) if lir else None
print("all new_files in BOTH eval stores:", all_in_both)
print("last_ingest_run:", lir, "| max new_file mtime:", nf_dt.isoformat() if nf_dt else "n/a")
# MODE C umbrella: named journal already in BOTH eval stores. That ALONE makes it
# closure-only — the named journal is already processed; any re-fire comes from
# later siblings. The lir-vs-nf_mtime relationship only selects the sub-step.
# Two sub-cases (both closure-only, no pipeline re-run, no wave journal mint):
#   (a) lir_dt <  nf_dt -> the NAMED journal is the unbridged gap (state strictly behind it)
#   (b) lir_dt >= nf_dt -> named journal is bridged; re-fire caused by LATER siblings
#                          (mentor-cron heartbeats land ~every 5 min) with mtime > last_ingest_run.
#                          This INCLUDES the common lir > nf_mtime case (state already PAST the
#                          named journal, fully closed by a prior run) AND the lir == nf_mtime case.
#                          The named journal's eval status is a RED HERRING for the real gap.
# MODE C trigger is `all_in_both` ALONE (2026-07-16 fix): the old code used `lir_dt <= nf_dt`,
# which misclassified the common lir > nf_mtime case (state already past the named journal, already
# closed) as NOT Mode C and routed sessions into Mode A/B — re-running pipelines and double-journalizing.
# The named journal being in BOTH eval stores is the definitive signal that it is already done.
if all_in_both and lir_dt and nf_dt:
    if lir_dt < nf_dt:
        print(">>> MODE C (a): named journal evaluated, state BEHIND its mtime -> closure-only; bridge named journal + ungated sweep")
    else:
        print(">>> MODE C (b): named journal evaluated AND last_ingest_run >= its mtime -> state already at/above named journal (incl. the common lir > nf_mtime fully-closed case); re-fire from LATER siblings, NOT the named file. Closure-only: run ungated closure_convergence_sweep.py (catches later heartbeats), advance state past max today mtime. NO pipeline re-run, NO wave journal mint.")
else:
    print(">>> NOT Mode C (named journal NOT in both eval stores) — inspect Mode A (fresh explicit-run) / Mode B (prior-wave misclassification)")
PYEOF
```

If MODE C: do NOT load Forge/Mentor/Praxis. Do NOT run `praxis_ingest_run.py`. Do NOT mint/rewrite a
`dispatch-wave-*.json`. Proceed to closure.

## Closure sequence

```bash
DATE=2026-07-16   # date of the re-detected journal
SCRIPTS=<hermes-home>/profiles/indigo/skills/ocas-forge/scripts
# 1. Convergence sweep (ungated) — loop until it bridges 0
while true; do
  out=$(python3 "$SCRIPTS/closure_convergence_sweep.py" --date "$DATE" 2>&1)
  echo "$out" | tail -2
  echo "$out" | grep -q "GAPS BRIDGED: 0" && break
done
# 2. Assert genuine gap = 0
python3 "$SCRIPTS/verify_genuine_gap_profile.py" --date "$DATE" 2>&1 | tail -2
```

Then advance `last_ingest_run` past ALL today's non-`dispatch-wave` journal mtimes (a heartbeat
may land during the sweep):

```python
python3 << 'PYEOF'
import os, json, datetime
PROFILE="<hermes-home>/profiles/indigo"
JDIR=f"{PROFILE}/commons/journals"
STATE=f"{PROFILE}/commons/data/ocas-praxis/ingest_state.json"
DATE="2026-07-16"
max_mt=0.0
for skill in os.listdir(JDIR):
    d=os.path.join(JDIR, skill, DATE)
    if not os.path.isdir(d): continue
    for fn in os.listdir(d):
        if fn.startswith("dispatch-wave-"): continue   # meta-journal excluded
        fp=os.path.join(d, fn)
        if fp.endswith(".json"):
            max_mt=max(max_mt, os.path.getmtime(fp))
max_iso=datetime.datetime.fromtimestamp(max_mt, tz=datetime.timezone.utc).isoformat()
st=json.load(open(STATE))
st["last_ingest_run"]=max_iso
st["note"]="Mode C stale-state closure: advanced past max today-journal mtime"
ev=f"{PROFILE}/commons/data/ocas-praxis/journals_evaluated.jsonl"
n=sum(1 for _ in open(ev))
st["journals_evaluated_count"]=n; st["last_eval_file_line"]=n
json.dump(st, open(STATE, "w"), indent=2)
print("last_ingest_run ->", max_iso)
PYEOF
```

## Monitor gate state — MANDATORY (the actual re-enqueue stopper)

The closure sequence above advances `commons/data/ocas-praxis/ingest_state.json`
(`last_ingest_run`). That file does NOT gate `monitor_journals.py`. The monitor reads a
SEPARATE state file:

    <hermes-home>/commons/data/monitor_state/journal_ingest_state.json   (key: "latest_mtime")

`monitor_journals.py` enqueues a `new_journals` item whenever the max on-disk journal mtime
exceeds `journal_ingest_state.json.latest_mtime`. If that file is stale (below the max journal
mtime), the monitor RE-ENQUEUES `new_journals` on its next cron tick REGARDLESS of what
`praxis/ingest_state.json` or the eval stores report. Advancing only the praxis state therefore
does NOT stop the re-fire — the dispatcher keeps getting re-fed the same wave.

CONFIRMED 2026-07-16: a re-detection closure advanced `praxis/ingest_state.json` but the monitor
kept re-enqueuing until `journal_ingest_state.json.latest_mtime` was also advanced past the max
journal mtime (15:20:28Z mentor-cron heartbeat). Only after BOTH files were advanced did
`monitor_journals.py` exit 1 (no enqueue) and `monitor_queue.jsonl` stay at 0 bytes.

Advance BOTH in the same closure (and in every post-advance re-sweep re-advance):

```python
import os, json, datetime
MON_STATE="<hermes-home>/commons/data/monitor_state/journal_ingest_state.json"
mt=max_mt   # the max today-journal mtime computed above
ms={}
if os.path.exists(MON_STATE): ms=json.load(open(MON_STATE))
ms["latest_mtime"]=mt
ms["checked_at"]=datetime.datetime.fromtimestamp(mt, tz=datetime.timezone.utc).isoformat()
os.makedirs(os.path.dirname(MON_STATE), exist_ok=True)
json.dump(ms, open(MON_STATE, "w"), indent=2)
print("monitor_state.latest_mtime ->", ms["latest_mtime"])
```

## POST-ADVANCE re-sweep (critical — do not skip)

A mentor-cron heartbeat lands ~every 5 min. After advancing state, re-run the convergence sweep.
If it bridges >0 (a heartbeat landed between your pre-advance sweep and the state write), re-advance
state to the new max mtime and sweep again. Iterate until `GAPS BRIDGED: 0`, THEN assert
`GENUINE GAP = 0`. A single pass is NEVER permanently stable.

```bash
DATE=2026-07-16
SCRIPTS=<hermes-home>/profiles/indigo/skills/ocas-forge/scripts
while true; do
  out=$(python3 "$SCRIPTS/closure_convergence_sweep.py" --date "$DATE" 2>&1)
  echo "$out" | tail -2
  bridged=$(echo "$out" | grep "GAPS BRIDGED:" | grep -o '[0-9]*')
  [ "$bridged" = "0" ] && break
  # re-advance state to new max mtime
  python3 << 'PYEOF'
import os, json, datetime
PROFILE="<hermes-home>/profiles/indigo"
JDIR=f"{PROFILE}/commons/journals"; STATE=f"{PROFILE}/commons/data/ocas-praxis/ingest_state.json"
DATE="2026-07-16"
max_mt=0.0
for skill in os.listdir(JDIR):
    d=os.path.join(JDIR, skill, DATE)
    if not os.path.isdir(d): continue
    for fn in os.listdir(d):
        if fn.startswith("dispatch-wave-"): continue
        fp=os.path.join(d, fn)
        if fp.endswith(".json"): max_mt=max(max_mt, os.path.getmtime(fp))
st=json.load(open(STATE))
st["last_ingest_run"]=datetime.datetime.fromtimestamp(max_mt, tz=datetime.timezone.utc).isoformat()
json.dump(st, open(STATE, "w"), indent=2)
PYEOF
done
python3 "$SCRIPTS/verify_genuine_gap_profile.py" --date "$DATE" 2>&1 | tail -2
```

## Email second-wave re-affirm (only if the wave also carried `new_emails`, all `is_new:false`)

Re-affirm the account state file. Re-read the FULL file first, then write the complete object
(never `patch` — duplicate-key JSON corruption pitfall). No inbox reads, no drafts, no sends
(<operator> inbox hard rule 2026-06-24).

**Re-affirm BOTH accounts — never just one.** The re-fire loop enqueues `new_emails` for the
owner AND indigo accounts together; a closure that only re-affirms `owner` leaves `indigo`'s
`verified_second_wave` as `None`, so the indigo account re-fires (and a later wave must re-patch it).
Observed live 2026-07-16T16:45Z: a prior closure advanced `owner`'s state but left `indigo`'s
`verified_second_wave` = None; this session had to re-affirm `indigo` separately.

**Account-field identity check (pitfall, confirmed 2026-07-16T19:24Z closure):** the `account`
field INSIDE these state files can be MISLABELED — a <operator> file
(`last_email_check_<account-identity>_gmail_com.json` and/or top-level `last_email_check.json`) was
found carrying `account: <agent-email>` (the agent's address), a pre-existing residual
error. A closure script that only `set-if-absent` PRESERVES the mislabel silently. **Fix:** derive
the expected account from the file's intended owner — owner flat + top-level = `<user-google-email>`;
indigo flat + top-level = `<agent-email>` — and EXPLICITLY REPAIR any mismatch (overwrite
the wrong value rather than skipping when present). Routing keys off the FILENAME, not this field, so
the mislabel stays silent until something reads `account` for identity — correct it on sight.

**AUTHORITATIVE re-affirm set — MUST MATCH `closure_closeout_check.py` (CORRECTED 2026-07-17).**
The 2026-07-17 verifier REQUIRES exactly four dispatch-owned email-state files for gate [3] and only
**WARNS** on the two top-level GWS-snapshot files. Re-affirm ONLY the four required in the code block
below. Do NOT use the older 2026-07-15 "authoritative flat paths" set
(`last_email_check_<account-identity>_gmail_com.json` + top-level `last_email_check.json`) — the verifier
only WARNS on those two and REQUIRES these four instead. **Following the old flat-only set leaves
gate [3] failing** (the verifier requires `owner/last_email_check.json` + `last_email_check_owner.json`,
which the old prose omitted), so the wave re-fires forever. **SUPERSEDES the 2026-07-15
"subdir is stale for reads" note** — the 2026-07-17 verifier correction explicitly requires the
`owner/last_email_check.json` subdir copy, so the earlier "stale for reads" claim is now wrong.
- required (satisfies gate [3]): `owner/last_email_check.json`, `last_email_check_owner.json`,
  `last_email_check_indigo.json`, `last_email_check_mx_indigo_karasu_gmail_com.json`
- warn-only (do NOT rely on to close; they stay null under the monitor re-fire bug):
  `last_email_check.json`, `last_email_check_<account-identity>_gmail_com.json`

```python
import json, datetime, os
NOW=datetime.datetime.now(datetime.timezone.utc)
TS=NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
DISP="<hermes-home>/profiles/indigo/commons/data/ocas-dispatch"
note=("MODE C mixed re-detection closure: journal already evaluated (GENUINE GAP=0), both state "
      "gates advanced. All threads is_new:false and verified present in evidence.jsonl (Path A). "
      "No inbox reads/drafts/sends (READ-ONLY + 2026-06-24 hard rule). Re-affirmed verified_second_wave.")
# REQUIRED set per closure_closeout_check.py (2026-07-17 correction) — gate [3] needs ALL four True
files=[
  ("owner",  f"{DISP}/owner/last_email_check.json"),                       # required (subdir copy)
  ("owner",  f"{DISP}/last_email_check_owner.json"),                       # required (flat)
  ("indigo", f"{DISP}/last_email_check_indigo.json"),                      # required (flat, indigo)
  ("indigo", f"{DISP}/last_email_check_mx_indigo_karasu_gmail_com.json"),  # required (flat, indigo)
]
for acct, p in files:
    try:
        s=json.load(open(p))
    except FileNotFoundError:
        print(f"SKIP (absent): {p}"); continue
    s["verified_second_wave"]=True
    s["last_dispatch"]=TS
    s["last_dispatch_wave"]="closure-redetection"
    s["last_dispatch_email_classification"]="second-wave"
    s["last_dispatch_note"]=note
    json.dump(s, open(p,"w"), indent=2)
    json.load(open(p))  # validate round-trip
    print(f"{acct:6s} {p.split('/')[-1]:50s} verified_second_wave={s.get('verified_second_wave')} (actionable preserved: {s.get('actionable')})")
```

The email re-fire loop itself is NOT stoppable by the state file — `monitor_email.py` enqueues whenever
`actionable > 0` regardless of `is_new`, and the inbox stays unread (write prohibited). The state
re-affirm suppresses the WORK each cycle; flag the root cause for <operator> authorization to fix at source
(gate monitor on `has_new`, or count only `is_new` threads as actionable).

## Final verification (close-out self-check)

Before declaring the closure done, run one consolidated check that ALL gates are set. A closure
that leaves any single gate stale re-fires the wave. Every condition below must print True/0:

```python
import os, json, datetime
PROFILE="<hermes-home>/profiles/indigo"
JDIR=f"{PROFILE}/commons/journals"
DATE="2026-07-16"  # date of the re-detected journal
named=f"ocas-mentor/{DATE}/mentor-light-20260716T184039Z.json"  # <- the wave's named journal (example)
PRAXIS_EV=f"{PROFILE}/commons/data/ocas-praxis/journals_evaluated.jsonl"
DISPATCH_EV=f"{PROFILE}/commons/data/ocas-dispatch/journals_evaluated.jsonl"
PRAXIS_STATE=f"{PROFILE}/commons/data/ocas-praxis/ingest_state.json"
MON_STATE=f"{PROFILE}/commons/data/monitor_state/journal_ingest_state.json"
MON_STATE_PROFILE=f"{PROFILE}/commons/data/monitor_state/journal_ingest_state.json"
def in_store(p, rel):
    with open(p) as f: return any(rel in ln for ln in f)
print("named journal in PRAXIS+DISPATCH eval stores:", in_store(PRAXIS_EV, named), in_store(DISPATCH_EV, named))
st=json.load(open(PRAXIS_STATE))
mr=json.load(open(MON_STATE)); mp=json.load(open(MON_STATE_PROFILE))
lir_dt=datetime.datetime.fromisoformat(st["last_ingest_run"].replace("Z","+00:00"))
mon_dt=datetime.datetime.fromtimestamp(mr["latest_mtime"], tz=datetime.timezone.utc)
monp_dt=datetime.datetime.fromtimestamp(mp["latest_mtime"], tz=datetime.timezone.utc)
max_mt=0.0
for skill in os.listdir(JDIR):
    d=os.path.join(JDIR, skill, DATE)
    if not os.path.isdir(d): continue
    for fn in os.listdir(d):
        if fn.startswith("dispatch-wave-"): continue
        if fn.endswith(".json"): max_mt=max(max_mt, os.path.getmtime(os.path.join(d, fn)))
max_dt=datetime.datetime.fromtimestamp(max_mt, tz=datetime.timezone.utc)
print("praxis last_ingest_run >= max today mtime :", lir_dt >= max_dt)
print("monitor ROOT    latest_mtime >= max       :", mon_dt >= max_dt)
print("monitor PROFILE latest_mtime >= max       :", monp_dt >= max_dt)
# gate [3] REQUIRED set (closure_closeout_check.py 2026-07-17 correction) — all must be True
required=["owner/last_email_check.json","last_email_check_owner.json",
           "last_email_check_indigo.json","last_email_check_mx_indigo_karasu_gmail_com.json"]
for fn in required:
    p=f"{PROFILE}/commons/data/ocas-dispatch/{fn}"
    print(f"email (required) {fn:50s} verified_second_wave={json.load(open(p)).get('verified_second_wave')}")
# warn-only (null expected, do NOT block closure): last_email_check.json, last_email_check_<account-identity>_gmail_com.json
```

Plus: `python3 skills/ocas-forge/scripts/forge_count_unprocessed.py` must print `0`, and
`verify_genuine_gap_profile.py --date <DATE>` must print `GENUINE GAP (excluding custodian): 0`.
If any check fails, return to the relevant step (re-sweep, re-advance, or re-affirm) rather than
declaring closure.

## Guardrails
- Never mint a second `dispatch-wave-*.json` in a re-detection — it orphans the existing one and re-fires.
- Use the REAL eval-store paths (`commons/data/ocas-*/journals_evaluated.jsonl`), NOT
  `commons/journals/ocas-dispatch/journals_evaluated.jsonl` (does not exist).
- Advance state from max mtime of ALL non-`dispatch-wave` journals, then sweep ONCE MORE after advancing.
- Read state via `json.load`, never `read_file` (stale-cache pitfall).
- Advance BOTH `ocas-praxis/ingest_state.json` AND `commons/data/monitor_state/journal_ingest_state.json` (separate file that gates `monitor_journals.py`). Advancing only one leaves the monitor re-enqueuing the same wave.
- The convergence sweep and gap-verify scripts are the authoritative closure tools — both exist on disk
  and are ungated (no mtime filter), so they catch journals a cutoff-gated sweep would skip.
- **State-exactly-pinned-to-named-journal (`lir == nf_mtime`) is STILL a re-fire (confirmed 2026-07-16T04:35Z):** The dispatcher can re-enqueue a `new_journals` item whose journal is in BOTH eval stores AND whose mtime equals `last_ingest_run` exactly. The original Mode C pre-flight required `lir < nf_mtime`, which misclassifies this as "NOT Mode C" and sends you to Mode A/B (pipeline re-run + wave-journal mint = double-journalization). The true cause is OTHER later journals (mentor-cron heartbeats at 04:35:57 / 04:42:03) with mtime ABOVE `last_ingest_run` that were never bridged. **Fix:** treat `all_in_both AND lir >= nf_mtime` as Mode C; diagnose the real gap via the ungated `closure_convergence_sweep.py` (walks ALL today-dated journals, not just the named one) and check `verify_genuine_gap_profile.py` — the genuine gap count reveals the later siblings. Do NOT re-run Forge/Mentor/Praxis and do NOT mint a new `dispatch-wave` journal.