# Closure Gap-Scan Parse Pitfall

## Source
Observed live 2026-07-22T1206Z during a mixed `new_journals`+`new_emails` dispatch closure.
A hand-rolled `verify_genuine_gap_profile.py` → `bridge_eval_inline.py` loop printed
`GENUINE GAP = 0` iterations forever because it never extracted a real path.

## `verify_genuine_gap_profile.py --date <DATE>` output format

Two distinct line shapes:

1. **Per-gap line** (one per genuinely-missing journal):
   ```
   GAP  ocas-mentor/2026-07-22/mentor-light-20260722T120023Z.json dispatch=False praxis=True
   ```
   - `GAP` followed by **TWO spaces**, then the **relative path** (the thing you must bridge),
     then `<store>=True/False` flags for each eval store it is missing from.
   - `custodian=`-prefixed paths are NON-genuine (the monitor re-detects custodian scans constantly).
     Ignore them.

2. **Summary line** (one, at the end):
   ```
   GENUINE GAP (excluding custodian): 1
   ```
   This is a **COUNT**, not a path. It carries no relative path.

## The bug
A loop that did:
```python
genuine = [l.strip() for l in lines if l.strip().startswith("GENUINE") and "custodian=" not in l]
genuine = [l.split("GENUINE",1)[1].strip() for l in genuine]
```
matched ONLY the summary line, extracted the string `"GAP (excluding custodian): 1"`,
and passed that as a bridge target. `bridge_eval_inline.py` then "bridged" a bogus token,
the real `ocas-mentor/.../mentor-light-20260722T120023Z.json` gap stayed open, the verifier
kept reporting `GENUINE GAP = 1`, and `=== gates ALL CLOSED ===` was never reached until the
path was bridged by hand.

## Correct patterns

**Preferred — use the documented sweep script** (it iterates internally until 0 additions):
```bash
python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date <DATE>
# then re-assert:
python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date <DATE>   # require GENUINE GAP = 0
```

**If you must hand-roll** the bridge loop, parse the `GAP <relpath>` lines, not the summary:
```python
genuine = []
for l in lines:
    s = l.strip()
    if s.startswith("GAP ") and "custodian=" not in s:
        rel = s[len("GAP "):].split()[0]   # first token after "GAP  " is the relpath
        genuine.append(rel)
# then: python3 skills/ocas-forge/scripts/bridge_eval_inline.py --action cross_skill_mitigation <genuine...>
```
- The relpath is the **first whitespace-delimited token after `GAP  `** (note the two spaces).
- Do NOT split on `"GENUINE"` — that only ever yields the count string.

## Verification gate
After bridging, re-run `verify_genuine_gap_profile.py --date <DATE>` and require the literal
`GENUINE GAP (excluding custodian): 0` line. The bridge's own `total bridged: N` printout is
NOT authoritative — only the re-run gap checker is.
