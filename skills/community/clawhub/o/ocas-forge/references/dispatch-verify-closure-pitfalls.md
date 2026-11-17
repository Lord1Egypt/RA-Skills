# Dispatch Verification-Closure Path Pitfalls

Confirmed 2026-07-14 during a genuine explicit-run `new_journals` dispatch
(Forge + Mentor + Praxis). The 3-pipeline run and eval bridging succeeded,
but the optional post-run verify/closure script produced false alarms from
two path-composition bugs. Documented so future dispatch-run sessions don't
reproduce them when they hand-write a closure verifier.

## Trap 1 — Phantom-guard base segment (false phantoms)

The eval stores key journals by skill-first relpath:

```
ocas-forge/2026-07-14/forge-scan-XXXX.json
```

But the journal FILES live under `{agent_root}/commons/journals/`, i.e.

```
{agent_root}/commons/journals/ocas-forge/2026-07-14/forge-scan-XXXX.json
```

There is a `journals/` segment between `commons/` and the skill name.

**Bug:** `os.path.join(COMMONS, rel)` where `COMMONS = .../commons` and
`rel = "ocas-forge/..."` resolves to `.../commons/ocas-forge/...` — file
absent → every bridged journal reported as a PHANTOM.

**Fix:** `JOURNALS_ROOT = os.path.join(AGENT_ROOT, "commons", "journals")`
and check `os.path.exists(os.path.join(JOURNALS_ROOT, rel))`.

(Profile-scoped path is `{agent_root}/commons/journals/`; legacy root
`<hermes-home>/commons/journals/` also carries a stale copy. Prefer the
profile path for the authoritative check. Both must be the anchor, not
`commons/` alone.)

## Trap 2 — Recursive-glob nesting artifact (false gaps)

**Bug:** `glob.glob(os.path.join(JROOT, "**", "*.json"), recursive=True)`
over the journals tree descends into self-nested `journals/journals/
journals/...` symlink self-references and returns the SAME file under
mangled relpaths like
`journals/journals/ocas-praxis/2026-07-14/praxis-cron-XXXX.json`. A
post-dispatch gap walk then reports dozens of false "unevaluated" gaps
(all the same file repeated).

**Fix:** walk per-skill with a bounded `os.listdir`, never recursive glob:

```python
for skill in os.listdir(JROOT):
    datedir = os.path.join(JROOT, skill, "2026-07-14")
    if not os.path.isdir(datedir):
        continue
    for fn in os.listdir(datedir):
        if not fn.endswith(".json"):
            continue
        rel = f"{skill}/2026-07-14/{fn}"
        # skip meta-artifacts before gap classification
        if "dispatch-wave" in fn or "forge-scan" in fn:
            continue
        ...
```

## Why this matters

Both traps fire ONLY in the verify/closure step — the part you write by
hand, not the pipeline scripts. The pipeline itself is correct; the
closure verifier must replicate the exact path algebra the pipeline uses.
When a closure reports phantoms/gaps, first re-check these two traps before
assuming a real missed bridge.

## Trap 3 — Whole-file scan floods legacy false phantoms (confirmed 2026-07-14)

A closure scan that checks membership of **every** eval-file entry (or that
reconciles the entire 21k-line `journals_evaluated.jsonl` against on-disk
journals) returns a flood of ~12,700 false "phantoms" — all from entries
written in June BEFORE key normalization stabilized:

- Pre-normalization filenames: `r_20260613_journal-scan-1781340171.json`,
  `jrn_20260624_111548.json`, `scan-0904.json`, literal 16-hex thread IDs.
  These predate the `ocas-<skill>/YYYY-MM-DD/<name>.json` relpath convention
  and the on-disk files were renamed/moved long ago, so the basename no
  longer resolves to a real path.
- `commons/journals/...`-prefixed keys: `commons/journals/ocas-lucid/...`.
  Joined onto `JOURNALS_ROOT` they become `.../commons/journals/commons/
  journals/...` — missing. This is Trap 1's prefix variant, en masse.
- `journals/ocas-forge/...`-prefixed keys (extra `journals/` segment) —
  Trap 1 variant again.
- Corrupted tokens leaked by a **prior `bridge_eval_both_stores.py --help`
  misuse** (see ocas-dispatch `cron-triage-workflow.md`): literal `--files`
  and `--help` strings were written as eval entries. They appear as phantom
  basenames forever. Do NOT try to "fix" them — they are known historical
  corruption, harmless to dispatch re-detection, and unscoped historical
  `--fix` cleanup is explicitly forbidden (it would touch tens of thousands
  of unrelated legacy entries).

**Fix — bound the closure scan to the CURRENT wave, never the whole file:**

```python
import datetime, glob, os
JROOT = os.path.join(AGENT_ROOT, "commons", "journals")
# Wave floor = the dispatcher's latest_ts (or the stale last_ingest_run we
# just advanced past). Only journals NEWER than this are this wave's concern.
floor_dt = datetime.datetime(2026, 7, 14, 11, 23, 0, tzinfo=datetime.timezone.utc)
floor = floor_dt.timestamp()
DATE = "2026-07-14"
missing = []
for skill in os.listdir(JROOT):
    datedir = os.path.join(JROOT, skill, DATE)   # current date ONLY
    if not os.path.isdir(datedir):
        continue
    for fn in os.listdir(datedir):
        if not fn.endswith(".json"):
            continue
        if "dispatch-wave" in fn:                # meta-artifact, skip
            continue
        fp = os.path.join(datedir, fn)
        if os.path.getmtime(fp) < floor:         # current-wave window only
            continue
        rel = f"{skill}/{DATE}/{fn}"
        # check BOTH stores by basename; report only real current-wave misses
        if basename not in praxis_members or basename not in dispatch_members:
            missing.append(rel)
```

Report `GENUINE GAP = len(set(missing))` for the bounded set. If it is 0,
the wave is closed — regardless of how many legacy phantoms a whole-file
scan would have printed. The whole-file flood is noise, not a missed bridge.

**Rule of thumb:** the closure verifier exists to prove the *current wave's*
journals are in both stores. Anything older than the wave floor is someone
else's historical debt and must not appear in your gap count.