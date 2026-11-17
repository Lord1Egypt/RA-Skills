# Mixed-Wave Pre-Flight Triage (consolidated 2026-07-15)

## Purpose
When a dispatcher fire carries BOTH `new_journals` (explicit-run override in the prompt) AND
`new_emails` (all `is_new:false` = email second-wave), the `dispatch-wave-*.json` journal may
ALREADY exist on disk from a PRIOR wave. Three distinct sub-cases require DIFFERENT actions.
Running the wrong one either double-writes journals (violating the anti-journalization hard gate)
or leaves `last_ingest_run` stale (re-fires forever). This doc is the PRE-FLIGHT that decides which
mode applies BEFORE you touch anything. It consolidates the scattered SKILL.md bullets
("Self-consistency rule", "RECOVERY PITFALL", "RECOVERY REWRITE is dispositive", "Mixed
new_journals+new_emails in ONE wave") into one mechanical decision.

## The three modes
| Mode | Trigger | Action |
|------|---------|--------|
| **A. Fresh explicit-run** | No `dispatch-wave-*.json` for the window, OR existing one already records genuine pipeline execution; AND at least one `new_file` absent from an eval store | Run full 3-pipeline (Forge scan + Mentor heartbeat + Praxis ingest), WRITE a NEW `dispatch-wave-<TS>.json`, bridge all 4 relpaths to both eval stores, advance state |
| **B. Prior-wave-misclassification RECOVERY** | A `dispatch-wave-*.json` for the window EXISTS, classified `mixed_no_op`/`second-wave`/genuine-no-op with notes like "No pipeline skills re-run"; `last_ingest_run` is BELOW the `new_file` mtimes; no `forge-scan-*.json` for the window | Run full genuine 3-pipeline, **REWRITE the EXISTING `dispatch-wave-<TS>.json` (same run_id)** to record genuine execution, bridge all 4 relpaths, advance state. Do NOT mint a new wave journal |
| **C. Re-detection closure** | Journal already in BOTH eval stores AND a prior closure for the same files/threads already recorded `genuine_gap=0` / email `action:none`. Evidence: a `dispatch-wave-*.json` OR `wave-redet-*.json` (timestamp > dispatcher `detected_at`) for the same files, OR `last_ingest_run` is below the journal mtime (stale-state loop). | Closure-ONLY: bridge residual one-sided gaps, re-affirm email `verified_second_wave`, advance state to MAX today-journal mtime, assert GENUINE GAP=0. Do NOT re-run pipelines or write/mint a wave journal |

## Pre-flight (copy-pasteable, read-only — composes no timestamps)
Run BEFORE any pipeline step. Prints the recommended mode.
```python
python3 << 'PYEOF'
import os, json, datetime
PROFILE="<hermes-home>/profiles/indigo"
JDIR=f"{PROFILE}/commons/journals"
PRAXIS_EV=f"{PROFILE}/commons/data/ocas-praxis/journals_evaluated.jsonl"
DISPATCH_EV=f"{PROFILE}/commons/data/ocas-dispatch/journals_evaluated.jsonl"
STATE=f"{PROFILE}/commons/data/ocas-praxis/ingest_state.json"
DATE="2026-07-15"  # date of the dispatcher's detected_at

# dispatcher new_files (from dispatcher.py output)
new_files=[
  "ocas-dispatch/2026-07-15/dispatch-wave-20260715T105533Z.json",
  "ocas-mentor/2026-07-15/mentor-light-20260715T110540Z.json",
]

def in_store(fpath, key, rel):
    if not os.path.exists(fpath): return False
    with open(fpath) as f:
        return any(rel in ln for ln in f)

all_in_both = all(in_store(PRAXIS_EV,"journal_id",r) and in_store(DISPATCH_EV,"filename",r)
                  for r in new_files)

forge_dir=f"{JDIR}/ocas-forge/{DATE}"
forge_files=sorted(fn for fn in os.listdir(forge_dir) if fn.startswith("forge-scan-")) if os.path.isdir(forge_dir) else []
print("forge-scan files in window:", forge_files[-3:])

st=json.load(open(STATE))
lir=st.get("last_ingest_run")
mts=[os.path.getmtime(f"{JDIR}/{r}") for r in new_files if os.path.exists(f"{JDIR}/{r}")]
nf_iso=datetime.datetime.fromtimestamp(max(mts),tz=datetime.timezone.utc).isoformat() if mts else "n/a"

wave_rel=next((r for r in new_files if "dispatch-wave" in r), None)
wave=None
if wave_rel and os.path.exists(f"{JDIR}/{wave_rel}"):
    wave=json.load(open(f"{JDIR}/{wave_rel}"))
    print("EXISTING WAVE JOURNAL:", wave_rel, "type=", wave.get("type"), "outcome=", wave.get("outcome"))
    print("  notes:", (wave.get("notes") or "")[:160])

print("all new_files in BOTH eval stores:", all_in_both)
print("last_ingest_run:", lir)
print("max new_file mtime ISO:", nf_iso)

if wave and ("No pipeline skills" in (wave.get("notes") or "") or wave.get("type") in ("mixed_no_op","second-wave")):
    lir_dt=datetime.datetime.fromisoformat(lir.replace("Z","+00:00")) if lir else None
    nf_dt=datetime.datetime.fromtimestamp(max(mts),tz=datetime.timezone.utc) if mts else None
    if lir_dt and nf_dt and lir_dt < nf_dt:
        print("\n>>> MODE B: prior-wave-misclassification RECOVERY - rewrite existing wave journal (same run_id), run genuine pipeline, advance state")
    else:
        print("\n>>> MODE A-variant: wave journal exists but state covers files - inspect fresh/re-detection")
elif all_in_both and not wave:
    lir_dt=datetime.datetime.fromisoformat(lir.replace("Z","+00:00")) if lir else None
    nf_dt=datetime.datetime.fromtimestamp(max(mts),tz=datetime.timezone.utc) if mts else None
    if lir_dt and nf_dt and lir_dt < nf_dt:
        print("\n>>> MODE C (re-detection STALE-STATE LOOP): journal ALREADY in BOTH eval stores, but")
        print("    last_ingest_run is BELOW the journal mtime -> dispatcher re-fires the same wave forever")
        print("    (redetection-stale-state-pitfall). Do NOT re-run pipelines (already closed; re-running")
        print("    mints duplicate journals = anti-journalization gate violation). Closure-ONLY: bridge")
        print("    residual one-sided gaps, advance last_ingest_run to MAX today-journal mtime (incl. any")
        print("    heartbeat AFTER detected_at), re-affirm email verified_second_wave (inbox untouched),")
        print("    converge, assert GENUINE GAP=0.")
    else:
        print("\n>>> MODE A: FRESH explicit-run - write NEW dispatch-wave journal, run genuine pipeline")
else:
    print("\n>>> inspect MODE C (re-detection: a LATER wave journal records genuine_gap=0) or MODE A")
PYEOF
```

## This session (2026-07-15T11:13Z) - worked example
- Both `new_files` already in BOTH eval stores -> `all_in_both` TRUE
- No `forge-scan-*` for the 10:5x-11:0x window (latest was 10:09:48Z) -> window scan missing
- `last_ingest_run` = 10:11:25Z, BELOW new_file mtimes (10:55:33Z, 11:05:40Z) -> state stale
- Existing `dispatch-wave-20260715T105533Z.json` on disk, `type: mixed_no_op`, notes
  "No pipeline skills (forge/mentor/praxis) re-run."
-> **MODE B**. Rewrote the existing wave journal (same run_id), ran Forge no-op scan +
real Mentor heartbeat + real Praxis ingest, bridged all 4 relpaths to both eval stores,
advanced `last_ingest_run` to 11:20:47Z (max mtime of 193 today-journals), re-affirmed email
`verified_second_wave`, convergence sweep -> **GENUINE GAP=0**. Held.

## Worked example — MODE C re-detection stale-state loop (2026-07-15T21:20Z)
- Dispatcher fire carried `new_journals` (`mentor-light-20260715T211519Z.json`, explicit-run) + `new_emails` (7 `owner` threads, all `is_new:false`).
- Named journal ALREADY in BOTH eval stores (`post-dispatch-cleanup` entries present) -> `all_in_both` TRUE.
- No `dispatch-wave-*.json` in the **preflight's hardcoded `new_files` list** -> the naive script branch would print MODE A and re-run pipelines. **WRONG.**
- Correct signal: `last_ingest_run` = 20:50:58Z, BELOW the journal mtime 21:15:19Z AND below a `21:20:21Z` mentor heartbeat written *after* `detected_at` (21:20:18Z). A prior `wave-redet-20260715T2120Z` closure had already processed/evaluated everything and re-affirmed email but **forgot to advance `last_ingest_run`** -> the dispatcher re-fires the same wave forever (classic redetection-stale-state-pitfall).
-> **MODE C**. Did NOT re-run pipelines. Ran `closure_convergence_sweep.py` (bridged the 21:20:21Z heartbeat: 1 gap), asserted `GENUINE GAP=0`, advanced `last_ingest_run` to `2026-07-15T21:20:21.590258+00:00` (max today-journal mtime, NOT just the named file), re-affirmed email `verified_second_wave` (inbox untouched), re-swept to `GAPS BRIDGED: 0`. Loop broken.
- **Lesson:** the preflight's `new_files` list is a sample, not ground truth. The decisive test is `last_ingest_run` vs MAX journal mtime — if state is behind the files AND the files are already evaluated, it's closure-only, never a fresh pipeline run.

## Key guardrails (carried from parent SKILL.md)
- Never mint a second `dispatch-wave-*.json` in a recovery - rewrite the existing one (orphaning re-fires).
- Write the dispatch-wave journal to disk BEFORE bridging it (phantom-guard ordering).
- Use the REAL on-disk forge-scan relpath captured at write time - never recompute `<TS>` for the
  bridge entry (that writes a phantom eval entry pointing at a non-existent file).
- Advance `last_ingest_run` from max mtime of ALL today's journals, then sweep ONCE MORE after advancing.
- Email second-wave: no inbox reads, no drafts, no sends (hard rule 2026-06-24); only re-affirm
  `verified_second_wave` via full-file `write_file` rewrite.