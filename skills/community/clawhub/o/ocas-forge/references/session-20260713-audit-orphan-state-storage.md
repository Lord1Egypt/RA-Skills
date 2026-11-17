# Forge audit 2026-07-13 — orphan vs. load-bearing state storage

Manual audit run (the `forge_audit_skills.py` script is a confirmed stub — it
prints only "Forge skill audit starting" and writes no report file; the manual
audit is the real procedure).

## Setup
- Profile: `indigo` (`<hermes-home>/profiles/indigo/skills/`).
- Default profile (`<hermes-home>/skills/`) also holds `ocas-critique/` and
  `ocas-10xeng-autofix/` remnants — off-limits without explicit cross-profile
  authorization; flagged only.

## Two `ocas-*` dirs lacked a SKILL.md

### `ocas-critique/` (indigo) — LOAD-BEARING, do NOT delete
- No SKILL.md (consolidated into `ocas-skilllab` long ago; skilllab frontmatter
  carries `merged-from: ocas-critique`).
- BUT `ocas-skilllab/scripts/critique_10khr_runner.py:45` hard-codes:
  `STATE_FILE = os.path.join(_HERMES_ROOT, "skills", "ocas-critique",
  "commons", "data", "ocas-critique", "10khr-state.json")`.
- `10khr-state.json` mtime was **2026-07-12 22:07** — written by a running cron.
- Removing the dir would break the 10khr engine.
- Verdict: FLAG. Recommended follow-up (out of scope for a consolidation pass):
  relocate `STATE_FILE` into `ocas-skilllab/`, migrate the file, then delete the
  empty `ocas-critique/` dir. This is the Forge-documented anti-pattern
  "storage inside skill package directories," but relocation needs a state-migrate.

### `ocas-10xeng-autofix/` (top-level, indigo) — TRUE GHOST, consolidated
- No SKILL.md; only `last_run.json` dated **2026-07-01** (stale).
- Canonical skill is `software-development/ocas-10xeng-autofix/` (15 KB SKILL.md,
  referenced by the whole `ocas-10xeng*` family: review/audit/debt/help/parent).
- `grep -rln "/skills/ocas-10xeng-autofix"` across scripts/config/journals/cron:
  zero path references (the `.usage.json` key `ocas-10xeng-autofix` is name-keyed
  and resolves to the real one).
- Action: moved (non-destructive) to
  `.archive/ocas-10xeng-autofix-ghost-20260713T131155Z`. Top-level ghost gone;
  real skill intact.

## Other `ocas-*` skills
All 31 remaining `ocas-*` skills had a valid SKILL.md with a coherent domain and
their own invocation path. The `ocas-10xeng*` family (6 skills under
`software-development/`) and `ocas-genie` (real name `genie`, standalone VPS
cleanup) are legitimate standalone/grouped skills — none folded into a parent.

## Variant proposal scan
No unprocessed `vp_*.json` / `vd_*.json` in `intake/` not already in
`intake/processed/` (the 11 `vp_*.json` under `proposals/` are source mirrors,
not pending work).