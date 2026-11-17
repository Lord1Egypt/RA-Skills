# keelwright v1.7.2 — audit-driven fixes

This release resolves the CRITICAL and MAJOR findings from a 16-agent security audit
(8 roles × 2 models) plus a meta-audit (reality-checker role). All changes are
backward-compatible and non-blocking.

## What we improved

### License corrected to MIT-0 (CRITICAL)
The skill was internally inconsistent about its license: `LICENSE` carried the
canonical MIT "shall be included" clause, `llms.txt` and `architecture.html` said
CC BY 4.0, while `SKILL.md` claimed MIT-0. Now **all surfaces agree**: keelwright is
**MIT-0 (MIT No Attribution)** — free to use, modify, and redistribute commercially
**without attribution**.
- `LICENSE` — removed the "shall be included" clause
- `llms.txt` — CC BY 4.0 → MIT-0
- `assets/architecture.html` — JSON-LD license → Apache-2.0 reference (neutral, no CC-BY)
- `references/web-guard.md` — explicit "keelwright itself is licensed MIT-0" note

### GATE 4 contamination check fixed (CRITICAL)
`scripts/validate_run.py` GATE 4 used a dead substring match (`"control.*skill_view" in ev`)
on a regex literal — it never fired. Now uses `re.search` with real contamination
signatures (`control arm was given skill_view`, `both arms were dispatched with skill_view`).
The gate now actually catches control/treatment contamination instead of silently passing.

### import_skill.py — zip-name validation (CRITICAL, T42)
Added defense-in-depth validation of the export archive filename
(`keelwright-export-YYYYMMDDTHHMMSSZ.zip`). Malformed or suspicious names are rejected
before any post-install code runs. (Note: argument vectors already used `shell=False`;
this closes the untrusted-name path explicitly.)

### check_update.py — pinned release verification (CRITICAL, T43)
Update checks now verify the release tag against a **pinned commit SHA**
(`PINNED_RELEASE_SHA`). A TOFU / GitHub-compromise that swaps the "latest" release
will not be surfaced as a trustworthy upgrade. Unverified updates are silently ignored
(the script stays non-blocking by design).

### validate_run.py — git-fallback restricted (T6)
The `arm_did_work` git fallback previously trusted `git -C <arm_dir> log` even when
`arm_dir` sat inside a PARENT repo — surfacing the parent's commits as "the model worked"
(false-pass). Now requires `arm_dir` to be its OWN git root (`.git` directly inside).

## Files changed
- `LICENSE`, `llms.txt`, `assets/architecture.html`, `references/web-guard.md`, `README.md`
- `scripts/validate_run.py`, `scripts/import_skill.py`, `scripts/check_update.py`

## Verification
- GATE 4 fires on real contamination evidence, no false-positive on normal prose.
- All three scripts pass `py_compile`.
- License residual scan: clean except one historical QA log (`references/qa-results-20260721.md`,
  scheduled for removal in v1.8.0 per T8/T44).

Upgrade via ClawHub, skills.sh, or `git pull ratingtesting/keelwright`.
